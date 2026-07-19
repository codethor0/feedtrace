"""Numerical-tolerance verification against frozen baselines."""

from pathlib import Path

from feedtrace.validation import verify_numeric

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sanitized" / "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv"
BASELINE = ROOT / "results" / "model_outputs"


def test_numeric_verification_pass(tmp_path):
    from feedtrace.predictive import run_benchmark

    out = tmp_path / "reproduced"
    run_benchmark(DATA, out)
    ok, problems = verify_numeric(DATA, BASELINE, reproduced_dir=out)
    assert ok, problems
