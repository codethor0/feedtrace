#!/usr/bin/env python3
"""Reproduce the sanitized R9 predictive benchmark."""

from __future__ import annotations

import argparse
from pathlib import Path

from feedtrace.predictive import run_benchmark


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        required=True,
        help="Path to R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory that will receive benchmark outputs",
    )
    args = parser.parse_args()
    outputs = run_benchmark(args.data, args.output_dir)
    for key, path in outputs.items():
        print(f"{key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
