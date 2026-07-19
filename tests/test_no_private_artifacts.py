"""Metadata, license, citation, extension, and manifest integrity tests."""

from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]

APPROVED_EXTENSIONS = {
    "",
    ".md",
    ".txt",
    ".csv",
    ".json",
    ".py",
    ".toml",
    ".yml",
    ".yaml",
    ".cff",
    ".png",
    ".svg",
    ".pdf",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".baseline",
}


def _iter_files():
    skip = {".venv", ".git", "__pycache__", ".pytest_cache", ".ruff_cache", "dist", "build", "reproduced"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip for part in path.parts):
            continue
        yield path


def test_licenses_present():
    assert (ROOT / "LICENSE.md").exists()
    assert (ROOT / "LICENSES" / "MIT.txt").exists()
    assert (ROOT / "LICENSES" / "CC-BY-4.0.txt").exists()


def test_citation_cff_valid_enough():
    text = (ROOT / "CITATION.cff").read_text()
    data = yaml.safe_load(text)
    assert data["cff-version"] == "1.2.0"
    assert data["version"] == "0.1.0-preprint"
    assert data["authors"][0]["family-names"] == "Thor"
    assert "doi" not in data
    assert "orcid" not in str(data).lower()
    assert "repository-code" not in data
    assert "YOUR_" not in text


def test_approved_extensions_and_sizes():
    for path in _iter_files():
        suffix = path.suffix.lower()
        name = path.name
        if name.startswith(".") and suffix == "":
            continue
        if name in {".gitignore", ".gitattributes", ".editorconfig", ".secrets.baseline"}:
            continue
        if name == "CODEOWNERS":
            continue
        assert suffix in APPROVED_EXTENSIONS or name.endswith(".baseline"), path
        assert path.stat().st_size > 0, path
        assert path.stat().st_size < 25_000_000, path


def test_git_internals_not_tracked():
    import subprocess

    if not (ROOT / ".git").exists():
        return
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert not any(path == ".git" or path.startswith(".git/") for path in tracked)


def test_ci_is_read_only_and_pinned():
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
    assert "contents: read" in text
    assert "pull_request_target" not in text
    assert re.search(r"actions/checkout@[0-9a-f]{40}", text)
    assert re.search(r"actions/setup-python@[0-9a-f]{40}", text)
    assert "${{ secrets." not in text


def test_codeowners_assigns_active_owner():
    text = (ROOT / ".github" / "CODEOWNERS").read_text()
    active = [
        line
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    # Ownership must be assigned to a concrete GitHub handle, not a placeholder.
    assert active, "CODEOWNERS must assign an active owner before push"
    for line in active:
        assert "@" in line
        assert "YOUR_" not in line
        assert "owner-github-username" not in line
    assert any(line.strip().startswith("*") for line in active)


def test_readme_states_unresolved_and_independence():
    text = (ROOT / "README.md").read_text()
    assert "Not affiliated" in text
    assert "Unresolved" in text
    assert "preliminary" in text.lower()
