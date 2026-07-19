#!/usr/bin/env python3
"""Build a local review ZIP of the public repository (no GitHub release)."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from feedtrace.checksums import write_checksums, write_public_manifest

SKIP = {".venv", ".git", "__pycache__", ".pytest_cache", ".ruff_cache", "dist", "build"}
MANIFEST_VERSION = "0.1.0-preprint"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("../feedtrace-repository-audit/FeedTrace_Public_Repo_Review.zip"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    write_public_manifest(
        root, root / "release" / "PUBLIC_MANIFEST.json", MANIFEST_VERSION
    )
    write_checksums(
        root,
        root / "release" / "SHA256SUMS.txt",
        exclude_names={".secrets.baseline"},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if any(part in SKIP for part in path.parts):
                continue
            archive.write(path, Path("feedtrace") / path.relative_to(root))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
