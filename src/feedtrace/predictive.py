"""Sanitized non-race predictive benchmark with separate conformal calibration.

This module never reads or constructs race or topic labels, post text, URLs,
viewer identities, or authentication material.
"""

from __future__ import annotations

import json
import math
import socket
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import numpy as np
import pandas as pd
from sklearn import __version__ as sklearn_version
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import RidgeCV

from feedtrace import __version__ as package_version
from feedtrace.schema import load_sanitized_table

SEED = 20260719
ALPHA = 0.10
FEATURES = [
    "log_age_h",
    "word_count",
    "hashtag_count",
    "has_img",
    "has_vid",
    "has_doc",
    "posts_prev_24h",
]


def prepare_modeling_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the published original-post and positive-impression filters."""
    data = df.copy()
    data["created_at"] = pd.to_datetime(data["created_at"], utc=True, errors="coerce")
    data["feed_impressions"] = pd.to_numeric(data["feed_impressions"], errors="coerce")
    data = data[data["is_original_post"].astype(bool) & (data["feed_impressions"] > 0)].copy()
    data["age_h"] = pd.to_numeric(data["feed_impressions_post_age_hours"], errors="coerce")
    data = data.dropna(subset=["created_at", "age_h"]).sort_values("created_at").reset_index(
        drop=True
    )
    data["log_impr"] = np.log(data["feed_impressions"].astype(float))
    data["log_age_h"] = np.log1p(data["age_h"].clip(lower=0))
    for col in ["word_count", "hashtag_count"]:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
    data["has_img"] = data["has_image"].astype(bool).astype(int)
    data["has_vid"] = data["has_video"].astype(bool).astype(int)
    data["has_doc"] = data["has_document"].astype(bool).astype(int)
    times = data["created_at"].to_numpy()
    data["posts_prev_24h"] = [
        float((times[:i] >= times[i] - np.timedelta64(24, "h")).sum())
        for i in range(len(data))
    ]
    return data


def conformal_quantile(scores: np.ndarray, alpha: float = ALPHA) -> tuple[float, int]:
    """Finite-sample split-conformal order statistic for absolute residuals."""
    n = len(scores)
    if n == 0:
        raise ValueError("Calibration scores are empty")
    order = min(n, math.ceil((n + 1) * (1 - alpha)))
    return float(np.partition(scores, order - 1)[order - 1]), order


def pinball(actual: np.ndarray, predicted_quantile: np.ndarray, tau: float) -> float:
    diff = actual - predicted_quantile
    return float(np.mean(np.maximum(tau * diff, (tau - 1) * diff)))


def period(frame: pd.DataFrame) -> dict[str, Any]:
    return {
        "n": int(len(frame)),
        "start_utc": frame["created_at"].iloc[0].isoformat(),
        "end_utc": frame["created_at"].iloc[-1].isoformat(),
    }


def chronological_split(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    n = len(data)
    train_end = int(n * 0.60)
    calibration_end = int(n * 0.80)
    train = data.iloc[:train_end]
    calibration = data.iloc[train_end:calibration_end]
    test = data.iloc[calibration_end:]
    return train, calibration, test



def _assert_within_output_dir(output_dir: Path, path: Path) -> Path:
    """Ensure every written path resolves inside the requested output directory."""
    output_dir = output_dir.resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(output_dir)
    except ValueError as exc:
        raise ValueError(
            f"Refusing to write outside the requested output directory: {resolved}"
        ) from exc
    return resolved


@contextmanager
def _network_disabled() -> Iterator[None]:
    """Block outbound network use during the public benchmark."""
    original = socket.socket

    def blocked(*_args: Any, **_kwargs: Any) -> socket.socket:
        raise RuntimeError("Network access is disabled during the FeedTrace benchmark")

    socket.socket = blocked  # type: ignore[assignment, method-assign]
    try:
        yield
    finally:
        socket.socket = original  # type: ignore[method-assign]


def run_benchmark(data_path: Path, output_dir: Path) -> dict[str, Path]:
    """Fit models, calibrate intervals, evaluate on the untouched test set."""
    with _network_disabled():
        return _run_benchmark_offline(data_path, output_dir)


def _run_benchmark_offline(data_path: Path, output_dir: Path) -> dict[str, Path]:
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = load_sanitized_table(Path(data_path))
    data = prepare_modeling_frame(raw)
    train, calibration, test = chronological_split(data)

    x_train = train[FEATURES].astype(float).to_numpy()
    y_train = train["log_impr"].to_numpy()
    x_cal = calibration[FEATURES].astype(float).to_numpy()
    y_cal = calibration["log_impr"].to_numpy()
    x_test = test[FEATURES].astype(float).to_numpy()
    y_test = test["log_impr"].to_numpy()

    models = {
        "ridge": RidgeCV(alphas=np.logspace(-3, 3, 25)),
        "random_forest": RandomForestRegressor(
            n_estimators=500, min_samples_leaf=5, random_state=SEED
        ),
        "gradient_boosting": GradientBoostingRegressor(
            n_estimators=300, max_depth=3, learning_rate=0.05, random_state=SEED
        ),
    }

    rows: list[dict[str, Any]] = []
    sensitivity_rows: list[dict[str, Any]] = []
    for name, model in models.items():
        model.fit(x_train, y_train)
        cal_pred = model.predict(x_cal)
        test_pred = model.predict(x_test)
        cal_residual = y_cal - cal_pred
        q_abs, q_order = conformal_quantile(np.abs(cal_residual))
        lower = test_pred - q_abs
        upper = test_pred + q_abs
        q50 = test_pred + np.quantile(cal_residual, 0.50)
        q90 = test_pred + np.quantile(cal_residual, 0.90)
        rows.append(
            {
                "model": name,
                "n_train": len(train),
                "n_calibration": len(calibration),
                "n_test": len(test),
                "train_start_utc": period(train)["start_utc"],
                "train_end_utc": period(train)["end_utc"],
                "calibration_start_utc": period(calibration)["start_utc"],
                "calibration_end_utc": period(calibration)["end_utc"],
                "test_start_utc": period(test)["start_utc"],
                "test_end_utc": period(test)["end_utc"],
                "mae_log": float(np.mean(np.abs(test_pred - y_test))),
                "rmse_log": float(np.sqrt(np.mean((test_pred - y_test) ** 2))),
                "pinball_q50": pinball(y_test, q50, 0.50),
                "pinball_q90": pinball(y_test, q90, 0.90),
                "split_conformal_90_coverage": float(
                    np.mean((y_test >= lower) & (y_test <= upper))
                ),
                "mean_interval_width_log": float(np.mean(upper - lower)),
                "calibration_abs_residual_quantile": q_abs,
                "calibration_order_statistic": q_order,
                "baseline_train_median_mae": float(
                    np.mean(np.abs(np.median(y_train) - y_test))
                ),
            }
        )

        for block_index, indices in enumerate(
            np.array_split(np.arange(len(calibration)), 4), 1
        ):
            scores = np.abs(cal_residual[indices])
            q_block, order_block = conformal_quantile(scores)
            block_lower = test_pred - q_block
            block_upper = test_pred + q_block
            cal_block = calibration.iloc[indices]
            sensitivity_rows.append(
                {
                    "model": name,
                    "calibration_block": block_index,
                    "n_calibration_block": len(indices),
                    "block_start_utc": cal_block["created_at"].iloc[0].isoformat(),
                    "block_end_utc": cal_block["created_at"].iloc[-1].isoformat(),
                    "order_statistic": order_block,
                    "abs_residual_quantile": q_block,
                    "test_coverage": float(
                        np.mean((y_test >= block_lower) & (y_test <= block_upper))
                    ),
                    "mean_interval_width_log": float(
                        np.mean(block_upper - block_lower)
                    ),
                }
            )

    benchmark = pd.DataFrame(rows)
    sensitivity = pd.DataFrame(sensitivity_rows)
    benchmark_path = _assert_within_output_dir(
        output_dir, output_dir / "R9_PREDICTIVE_BENCHMARK.csv"
    )
    sensitivity_path = _assert_within_output_dir(
        output_dir, output_dir / "R9_PREDICTIVE_INTERVAL_BLOCK_SENSITIVITY.csv"
    )
    metadata_path = _assert_within_output_dir(
        output_dir, output_dir / "R9_PREDICTIVE_INTERVAL_METADATA.json"
    )
    benchmark.to_csv(benchmark_path, index=False)
    sensitivity.to_csv(sensitivity_path, index=False)

    metadata = {
        "seed": SEED,
        "alpha": ALPHA,
        "outcome": "natural log of strictly positive recorded impressions",
        "features": FEATURES,
        "split_rule": "first 60% train, next 20% calibration, final 20% test, chronological",
        "train": period(train),
        "calibration": period(calibration),
        "test": period(test),
        "calibration_score": "absolute residual on calibration observations only",
        "quantile_rule": "ceil((n_calibration + 1) * (1 - alpha))-th order statistic",
        "test_used_for_fitting_or_calibration": False,
        "exchangeability_caveat": (
            "Chronological data may violate exchangeability; the algorithm uses a "
            "valid separate calibration set and finite-sample order statistic, but "
            "the usual marginal coverage guarantee requires calibration and test "
            "examples to be exchangeable."
        ),
        "input_file": Path(data_path).name,
        "software_versions": {
            "feedtrace": package_version,
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn_version,
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
    return {
        "benchmark": benchmark_path,
        "sensitivity": sensitivity_path,
        "metadata": metadata_path,
    }
