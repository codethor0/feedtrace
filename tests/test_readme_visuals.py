"""Tests for README visuals, the visuals manifest, figures, and clean history."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

from feedtrace.public_audit import documentation_findings

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANIFEST = ROOT / "docs" / "README_VISUALS_MANIFEST.md"
FIGURES_README = ROOT / "figures" / "README.md"
RENDERED = ROOT / "figures" / "rendered"

IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")
FEATURED_SIZE_LIMIT = 500_000


def _readme_images():
    """Local (non-badge) README figures only; external images are badges."""
    return [
        m
        for m in IMAGE_RE.finditer(README.read_text())
        if not m.group("path").strip().startswith(("http://", "https://"))
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_readme_has_four_to_six_featured_visuals():
    images = _readme_images()
    assert 4 <= len(images) <= 6, f"expected 4-6 featured visuals, found {len(images)}"


def test_readme_image_paths_exist_and_relative():
    for match in _readme_images():
        target = match.group("path").strip()
        assert not target.startswith(("http://", "https://")), target
        assert not target.startswith("/"), target
        assert (ROOT / target).exists(), target


def test_readme_alt_text_meaningful():
    for match in _readme_images():
        alt = match.group("alt").strip()
        target = match.group("path").strip()
        assert alt, f"empty alt text for {target}"
        assert alt != Path(target).name, target
        assert len(alt) >= 20, f"alt text too short for {target}"


def test_no_duplicate_featured_figures():
    paths = [m.group("path").strip() for m in _readme_images()]
    assert len(paths) == len(set(paths))


def test_featured_figures_within_size_limit():
    for match in _readme_images():
        path = ROOT / match.group("path").strip()
        assert path.stat().st_size <= FEATURED_SIZE_LIMIT, path


def test_no_absolute_local_paths_in_readme_and_manifest():
    for doc in (README, MANIFEST, FIGURES_README):
        text = doc.read_text()
        assert "/Users/" not in text, doc
        assert "C:\\Users\\" not in text, doc


def test_every_featured_figure_in_manifest_with_checksum():
    manifest_text = MANIFEST.read_text()
    figures_text = FIGURES_README.read_text()
    for match in _readme_images():
        target = match.group("path").strip()
        digest = _sha256(ROOT / target)
        assert target in manifest_text, f"{target} missing from visuals manifest"
        assert digest in manifest_text, f"checksum for {target} missing/wrong in manifest"
        assert digest in figures_text, f"checksum for {target} missing/wrong in figures/README"


def test_figures_readme_documents_every_rendered_figure():
    figures_text = FIGURES_README.read_text()
    for png in sorted(RENDERED.glob("*.png")):
        assert png.name in figures_text, f"{png.name} not documented in figures/README.md"
        assert _sha256(png) in figures_text, f"checksum for {png.name} missing/wrong"


def test_rendered_figures_have_no_private_metadata():
    forbidden = [b"/Users/", b"cursor", b"Cursor", b"@gmail.com", b"Users-thor"]
    for png in sorted(RENDERED.glob("*.png")):
        data = png.read_bytes()
        for needle in forbidden:
            assert needle not in data, f"{png.name} contains {needle!r}"


def test_documentation_audit_clean():
    problems = documentation_findings(ROOT)
    assert problems == [], problems


def test_public_manifest_matches_tree():
    import json

    from feedtrace.checksums import (
        MANIFEST_EXCLUDE_NAMES,
        iter_public_files,
        sha256_file,
    )

    manifest = json.loads((ROOT / "release" / "PUBLIC_MANIFEST.json").read_text())
    listed = {entry["path"]: entry for entry in manifest["files"]}
    assert manifest["file_count"] == len(manifest["files"])

    tree = {
        p.relative_to(ROOT).as_posix(): p
        for p in iter_public_files(ROOT)
        if p.name not in MANIFEST_EXCLUDE_NAMES
    }
    assert set(listed) == set(tree), set(listed).symmetric_difference(set(tree))
    for rel, entry in listed.items():
        assert entry["sha256"] == sha256_file(tree[rel]), rel
        assert entry["bytes"] == tree[rel].stat().st_size, rel


def test_git_history_has_no_tool_or_personal_metadata():
    if not (ROOT / ".git").exists():
        return
    log = subprocess.run(
        ["git", "log", "--all", "--format=%an%n%ae%n%cn%n%ce%n%b"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    lowered = log.lower()
    assert "co-authored-by" not in lowered
    assert "cursor" not in lowered
    assert "@gmail.com" not in lowered
    emails = subprocess.run(
        ["git", "log", "--all", "--format=%ae%n%ce"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    # noreply@github.com is GitHub's own service identity, used as the committer
    # of squash merges and of the synthetic merge commit checked out in CI.
    allowed_service = {"noreply@github.com"}
    for email in emails:
        assert (
            email.endswith("users.noreply.github.com") or email in allowed_service
        ), email
