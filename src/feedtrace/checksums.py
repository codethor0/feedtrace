"""SHA-256 helpers for public release integrity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

# Files intentionally omitted from the public manifest: the manifest cannot list
# its own stable checksum (self-reference), and .secrets.baseline is a mutable
# tool artifact. SHA256SUMS.txt is the authoritative integrity list instead.
MANIFEST_EXCLUDE_NAMES = {
    "PUBLIC_MANIFEST.json",
    "SHA256SUMS.txt",
    ".secrets.baseline",
}

SKIP_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "reproduced",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_public_files(root: Path, output: Path | None = None):
    root = Path(root)
    output_resolved = Path(output).resolve() if output is not None else None
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if output_resolved is not None and path.resolve() == output_resolved:
            continue
        yield path


def write_checksums(root: Path, output: Path, exclude_names: set[str] | None = None) -> int:
    exclude_names = exclude_names or set()
    root = Path(root)
    rows: list[str] = []
    for path in iter_public_files(root, output=output):
        if path.name in exclude_names:
            continue
        rel = path.relative_to(root).as_posix()
        rows.append(f"{sha256_file(path)}  {rel}")
    Path(output).write_text("\n".join(rows) + ("\n" if rows else ""))
    return len(rows)


def write_public_manifest(
    root: Path, manifest_path: Path, version: str
) -> int:
    """Write a deterministic public manifest of tracked-style files.

    The manifest lists every public file except its own path, the checksum list,
    and the mutable secrets baseline, each with its SHA-256 and byte size.
    """
    root = Path(root)
    manifest_path = Path(manifest_path)
    entries: list[dict[str, object]] = []
    for path in iter_public_files(root):
        if path.name in MANIFEST_EXCLUDE_NAMES:
            continue
        rel = path.relative_to(root).as_posix()
        entries.append(
            {
                "path": rel,
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    entries.sort(key=lambda entry: entry["path"])
    document = {"version": version, "file_count": len(entries), "files": entries}
    manifest_path.write_text(json.dumps(document, indent=2) + "\n")
    return len(entries)


def verify_checksums(root: Path, sums_file: Path) -> tuple[bool, list[str]]:
    problems: list[str] = []
    root = Path(root)
    for line in Path(sums_file).read_text().splitlines():
        if not line.strip():
            continue
        expected, _, rel = line.partition("  ")
        path = root / rel
        if not path.exists():
            problems.append(f"missing:{rel}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            problems.append(f"mismatch:{rel}")
    return not problems, problems
