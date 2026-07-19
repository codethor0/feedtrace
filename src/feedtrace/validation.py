"""Numerical-tolerance verification for the corrected R9 predictive benchmark."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pandas as pd

from feedtrace.predictive import run_benchmark

CSV_KEYS = {
    "R9_PREDICTIVE_BENCHMARK.csv": ["model"],
    "R9_PREDICTIVE_INTERVAL_BLOCK_SENSITIVITY.csv": ["model", "calibration_block"],
}
JSON_EXACT_FIELDS = [
    "split_rule",
    "quantile_rule",
    "test_used_for_fitting_or_calibration",
]
JSON_EXACT_NESTED = {
    "train": ["n", "start_utc", "end_utc"],
    "calibration": ["n", "start_utc", "end_utc"],
    "test": ["n", "start_utc", "end_utc"],
}


def compare_frame(
    name: str,
    expected: pd.DataFrame,
    actual: pd.DataFrame,
    keys: list[str],
    rtol: float,
    atol: float,
) -> tuple[bool, list[str], float, float]:
    problems: list[str] = []
    if sorted(expected.columns) != sorted(actual.columns):
        problems.append(
            f"{name}: column mismatch "
            f"(expected {sorted(expected.columns)}, got {sorted(actual.columns)})"
        )
        return False, problems, 0.0, 0.0

    expected = expected.sort_values(keys).reset_index(drop=True)
    actual = actual.sort_values(keys).reset_index(drop=True)
    if len(expected) != len(actual):
        problems.append(f"{name}: row count differs ({len(expected)} vs {len(actual)})")
        return False, problems, 0.0, 0.0

    max_abs = 0.0
    max_rel = 0.0
    for col in expected.columns:
        exp_col = expected[col]
        act_col = actual[col]
        if pd.api.types.is_numeric_dtype(exp_col) and pd.api.types.is_numeric_dtype(act_col):
            for i in range(len(exp_col)):
                e, a = exp_col.iloc[i], act_col.iloc[i]
                if pd.isna(e) and pd.isna(a):
                    continue
                diff = abs(float(a) - float(e))
                rel = diff / max(abs(float(e)), 1e-12)
                max_abs = max(max_abs, diff)
                max_rel = max(max_rel, rel)
                if diff > atol + rtol * abs(float(e)):
                    problems.append(
                        f"{name}[{col}] row {i}: expected {e}, got {a} "
                        f"(abs {diff:.3e}, rel {rel:.3e})"
                    )
        else:
            for i in range(len(exp_col)):
                if str(exp_col.iloc[i]) != str(act_col.iloc[i]):
                    problems.append(
                        f"{name}[{col}] row {i}: expected '{exp_col.iloc[i]}', "
                        f"got '{act_col.iloc[i]}'"
                    )
    return not problems, problems, max_abs, max_rel


def compare_metadata(expected: dict, actual: dict) -> tuple[bool, list[str]]:
    problems: list[str] = []
    for field in JSON_EXACT_FIELDS:
        if expected.get(field) != actual.get(field):
            problems.append(
                f"metadata[{field}]: expected {expected.get(field)!r}, got {actual.get(field)!r}"
            )
    for parent, children in JSON_EXACT_NESTED.items():
        for child in children:
            e = expected.get(parent, {}).get(child)
            a = actual.get(parent, {}).get(child)
            if e != a:
                problems.append(
                    f"metadata[{parent}.{child}]: expected {e!r}, got {a!r}"
                )
    return not problems, problems


def verify_numeric(
    data_path: Path,
    baseline_dir: Path,
    reproduced_dir: Path | None = None,
    rtol: float = 1e-6,
    atol: float = 1e-9,
) -> tuple[bool, list[str]]:
    """Compare reproduced outputs against frozen baselines within tolerance."""
    tmp = None
    if reproduced_dir is None:
        tmp = tempfile.TemporaryDirectory()
        out = Path(tmp.name)
        run_benchmark(data_path, out)
    else:
        out = Path(reproduced_dir)

    ok = True
    problems: list[str] = []
    for name, keys in CSV_KEYS.items():
        expected = pd.read_csv(baseline_dir / name)
        actual = pd.read_csv(out / name)
        passed, frame_problems, max_abs, max_rel = compare_frame(
            name, expected, actual, keys, rtol, atol
        )
        print(f"  {name}: max abs dev {max_abs:.3e}, max rel dev {max_rel:.3e}")
        ok = ok and passed
        problems.extend(frame_problems)

    exp_meta = json.loads((baseline_dir / "R9_PREDICTIVE_INTERVAL_METADATA.json").read_text())
    act_meta = json.loads((out / "R9_PREDICTIVE_INTERVAL_METADATA.json").read_text())
    passed, meta_problems = compare_metadata(exp_meta, act_meta)
    print(
        "  R9_PREDICTIVE_INTERVAL_METADATA.json: structural fields "
        f"{'match' if passed else 'DIFFER'}"
    )
    ok = ok and passed
    problems.extend(meta_problems)

    if tmp is not None:
        tmp.cleanup()
    return ok, problems
