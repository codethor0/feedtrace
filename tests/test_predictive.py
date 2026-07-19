"""Predictive benchmark invariants."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from feedtrace.predictive import (
    ALPHA,
    FEATURES,
    SEED,
    chronological_split,
    conformal_quantile,
    prepare_modeling_frame,
    run_benchmark,
)
from feedtrace import predictive as predictive_mod
from feedtrace.schema import load_sanitized_table

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sanitized" / "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv"


def test_seed_and_alpha():
    assert SEED == 20260719
    assert ALPHA == 0.10


def test_conformal_order_statistic():
    scores = np.arange(1, 236, dtype=float)
    q, order = conformal_quantile(scores, alpha=0.10)
    assert order == 213
    assert q == float(scores[212])


def test_deterministic_split_sizes():
    raw = load_sanitized_table(DATA)
    data = prepare_modeling_frame(raw)
    assert len(data) == 1173
    train, calibration, test = chronological_split(data)
    assert len(train) == 703
    assert len(calibration) == 235
    assert len(test) == 235
    assert FEATURES == [
        "log_age_h",
        "word_count",
        "hashtag_count",
        "has_img",
        "has_vid",
        "has_doc",
        "posts_prev_24h",
    ]


def test_output_directory_confinement(tmp_path):
    out = tmp_path / "reproduced"
    paths = run_benchmark(DATA, out)
    for path in paths.values():
        path.resolve().relative_to(out.resolve())
    bench = pd.read_csv(paths["benchmark"])
    assert set(bench["model"]) == {"ridge", "random_forest", "gradient_boosting"}
    assert int(bench.loc[bench["model"] == "ridge", "calibration_order_statistic"].iloc[0]) == 213


def test_assert_within_output_dir_rejects_escape(tmp_path):
    out = tmp_path / "reproduced"
    out.mkdir()
    with pytest.raises(ValueError, match="outside"):
        predictive_mod._assert_within_output_dir(out, tmp_path / "escape.csv")


def test_network_disabled_during_benchmark():
    with predictive_mod._network_disabled():
        with pytest.raises(RuntimeError, match="Network access is disabled"):
            import socket

            socket.socket()
