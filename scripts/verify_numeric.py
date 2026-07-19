#!/usr/bin/env python3
"""Numerical-tolerance verification against frozen R9 baselines."""

from __future__ import annotations

import argparse
from pathlib import Path

from feedtrace.validation import verify_numeric


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv"),
    )
    parser.add_argument(
        "--baseline-dir",
        type=Path,
        default=Path("results/model_outputs"),
    )
    parser.add_argument("--reproduced", type=Path, default=None)
    parser.add_argument("--rtol", type=float, default=5e-4)
    parser.add_argument("--atol", type=float, default=1e-9)
    args = parser.parse_args()

    print(
        f"Comparing against baseline {args.baseline_dir} "
        f"(rtol={args.rtol}, atol={args.atol}):"
    )
    ok, problems = verify_numeric(
        data_path=args.data,
        baseline_dir=args.baseline_dir,
        reproduced_dir=args.reproduced,
        rtol=args.rtol,
        atol=args.atol,
    )
    if ok:
        print("\nPASS: all numeric values within tolerance and structural fields exact.")
        return 0
    print("\nFAIL:")
    for problem in problems:
        print(f"  - {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
