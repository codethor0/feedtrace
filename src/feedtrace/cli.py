"""Console entry points for the public FeedTrace package."""

from __future__ import annotations

import argparse
from pathlib import Path

from feedtrace.checksums import verify_checksums, write_checksums
from feedtrace.predictive import run_benchmark
from feedtrace.public_audit import forbidden_data_files, scan_public_tree
from feedtrace.validation import verify_numeric


def reproduce_benchmark() -> None:
    parser = argparse.ArgumentParser(
        description="Reproduce the sanitized R9 predictive benchmark."
    )
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outputs = run_benchmark(args.data, args.output_dir)
    for key, path in outputs.items():
        print(f"{key}: {path}")


def verify_numeric_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Numerical-tolerance verification against frozen R9 baselines."
    )
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
    ok, problems = verify_numeric(
        data_path=args.data,
        baseline_dir=args.baseline_dir,
        reproduced_dir=args.reproduced,
        rtol=args.rtol,
        atol=args.atol,
    )
    if ok:
        print("PASS: all numeric values within tolerance and structural fields exact.")
        raise SystemExit(0)
    print("FAIL:")
    for problem in problems:
        print(f"  - {problem}")
    raise SystemExit(1)


def verify_checksums_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Verify SHA-256 checksums for the public repository tree."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--sums", type=Path, default=Path("release/SHA256SUMS.txt"))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        count = write_checksums(
            args.root, args.sums, exclude_names={".secrets.baseline"}
        )
        print(f"Wrote {count} checksums to {args.sums}")
        raise SystemExit(0)
    ok, problems = verify_checksums(args.root, args.sums)
    if ok:
        print("PASS: all checksums match")
        raise SystemExit(0)
    print("FAIL:")
    for problem in problems:
        print(f"  - {problem}")
    raise SystemExit(1)


def audit_public_tree_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Scan the public repository for prohibited artifacts."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    findings = scan_public_tree(args.root)
    bad_files = forbidden_data_files(args.root)
    if not findings and not bad_files:
        print("PASS: public-boundary scan clean")
        raise SystemExit(0)
    print("FAIL: public-boundary findings")
    for finding in findings:
        print(f"  - {finding.path}:{finding.line} [{finding.rule}]")
    for path in bad_files:
        print(f"  - {path} [forbidden_filename]")
    raise SystemExit(1)
