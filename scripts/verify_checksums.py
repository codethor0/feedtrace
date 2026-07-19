#!/usr/bin/env python3
"""Verify SHA-256 checksums for the public repository tree."""

from __future__ import annotations

import argparse
from pathlib import Path

from feedtrace.checksums import verify_checksums, write_checksums


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--sums", type=Path, default=Path("release/SHA256SUMS.txt"))
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write a fresh checksum list instead of verifying",
    )
    args = parser.parse_args()
    if args.write:
        count = write_checksums(
            args.root, args.sums, exclude_names={".secrets.baseline"}
        )
        print(f"Wrote {count} checksums to {args.sums}")
        return 0
    ok, problems = verify_checksums(args.root, args.sums)
    if ok:
        print("PASS: all checksums match")
        return 0
    print("FAIL:")
    for problem in problems:
        print(f"  - {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
