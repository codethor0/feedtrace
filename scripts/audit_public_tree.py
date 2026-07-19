#!/usr/bin/env python3
"""Scan the public repository for prohibited artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from feedtrace.public_audit import forbidden_data_files, scan_public_tree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    findings = scan_public_tree(args.root)
    bad_files = forbidden_data_files(args.root)
    if not findings and not bad_files:
        print("PASS: public-boundary scan clean")
        return 0
    print("FAIL: public-boundary findings")
    for finding in findings:
        print(f"  - {finding.path}:{finding.line} [{finding.rule}]")
    for path in bad_files:
        print(f"  - {path} [forbidden_filename]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
