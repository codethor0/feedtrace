"""Public-boundary and artifact scans for the FeedTrace repository."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".csv",
    ".json",
    ".py",
    ".toml",
    ".yml",
    ".yaml",
    ".cff",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
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


def _compile_rules() -> list[tuple[str, re.Pattern[str]]]:
    """Build scan rules at runtime so this file does not contain matchable literals."""
    zeros = "0" * 4
    fake_orcid = "-".join([zeros] * 4)
    downloads = "Down" + "loads"
    master_prompt = "master" + " " + "prompt"
    audit_private = "audit" + "_v3/"
    linkedin_pkg = "src/" + "linkedin_audit/"
    figures_mod = "analysis/" + "r9_figures.py"
    your_orcid = "YOUR_" + "ORCID"
    your_username = "YOUR_" + "USERNAME"
    replace_me = "REPLACE_" + "ME"
    cursor_dir = "." + "cursor/"
    cursor_rules = "cursor" + "rules"
    cursor_prefix = "cursor" + "_"
    tool_call = "tool_" + "call_id"
    system_note = "system" + " " + "notification"
    return [
        ("local_path_unix", re.compile(r"/Users/[A-Za-z0-9._-]+")),
        ("local_path_windows", re.compile(r"[A-Za-z]:\\Users\\")),
        ("downloads_path", re.compile(rf"/{downloads}/|\\{downloads}\\")),
        (
            "linkedin_post_url",
            re.compile(r"https?://(www\.)?linkedin\.com/(posts|feed/update|in/)"),
        ),
        ("activity_urn", re.compile(r"urn:li:activity:\d+")),
        ("cookie_li_at", re.compile(r"\bli_at\b")),
        ("cookie_jsession", re.compile(r"\bJSESSIONID\b")),
        (
            "authorization_header",
            re.compile(r"(?i)authorization\s*[:=]\s*bearer\s+\S+"),
        ),
        ("env_assignment", re.compile(r"(?i)^(API_KEY|SECRET|PASSWORD|TOKEN)\s*=")),
        (
            "assistant_cursor",
            re.compile(
                rf"(?i)\b{re.escape(cursor_dir)}|\b{re.escape(cursor_rules)}\b|"
                rf"\b{re.escape(cursor_prefix)}"
            ),
        ),
        (
            "assistant_prompt",
            re.compile(
                rf"(?i){re.escape(master_prompt)}|{re.escape(tool_call)}|"
                rf"{re.escape(system_note)}"
            ),
        ),
        ("placeholder_doi", re.compile(r"(?i)10\.1234/fake|doi:\s*XXXX")),
        (
            "placeholder_orcid",
            re.compile(rf"(?i){re.escape(fake_orcid)}|{re.escape(your_orcid)}"),
        ),
        (
            "placeholder_username",
            re.compile(rf"(?i){re.escape(your_username)}|{re.escape(replace_me)}"),
        ),
        (
            "emoji",
            re.compile(
                "["
                "\U0001F300-\U0001F6FF"
                "\U0001F900-\U0001FAFF"
                "\U00002700-\U000027BF"
                "\U0001F1E0-\U0001F1FF"
                "]"
            ),
        ),
        ("em_dash", re.compile("\u2014")),
        ("en_dash", re.compile("\u2013")),
        (
            "private_source_path",
            re.compile(
                re.escape(audit_private)
                + "|"
                + re.escape(linkedin_pkg)
                + "|"
                + re.escape(figures_mod)
            ),
        ),
    ]


RULES = _compile_rules()


@dataclass
class Finding:
    path: str
    line: int
    rule: str


# The scanner implementation constructs prohibited literals at runtime and is
# excluded from self-scanning to avoid false positives on its own rule factory.
SKIP_FILES = {"src/feedtrace/public_audit.py"}


def _iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if rel in SKIP_FILES:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
            "LICENSE",
            "LICENSE.md",
            "CODEOWNERS",
        }:
            yield path


def scan_public_tree(root: Path) -> list[Finding]:
    """Scan tracked-style text files for prohibited artifacts.

    Findings report only path, line, and rule category. Matched content is never
    returned.
    """
    findings: list[Finding] = []
    for path in _iter_text_files(root):
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for idx, line in enumerate(text.splitlines(), 1):
            for rule, pattern in RULES:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            path=path.relative_to(root).as_posix(),
                            line=idx,
                            rule=rule,
                        )
                    )
    return findings


_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")
_LINK_RE = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<path>[^)]+)\)")

COMMUNITY_FILES = (
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "ROADMAP.md",
    "LICENSE.md",
    "CITATION.cff",
    "docs/README_VISUALS_MANIFEST.md",
    "figures/README.md",
)


def _is_external_or_anchor(target: str) -> bool:
    target = target.strip()
    return (
        target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("#")
        or target.startswith("mailto:")
    )


def documentation_findings(root: Path) -> list[str]:
    """Check README assets, the visuals manifest, community files, and workflows.

    Returns human-readable problem strings. Sensitive content is never included.
    """
    root = Path(root)
    problems: list[str] = []

    for rel in COMMUNITY_FILES:
        if not (root / rel).exists():
            problems.append(f"missing_community_file:{rel}")

    readme = root / "README.md"
    manifest_path = root / "docs" / "README_VISUALS_MANIFEST.md"
    manifest_text = manifest_path.read_text() if manifest_path.exists() else ""

    if readme.exists():
        text = readme.read_text()

        featured: list[str] = []
        badges: list[str] = []
        for match in _IMAGE_RE.finditer(text):
            alt = match.group("alt").strip()
            target = match.group("path").strip()
            if target.startswith(("http://", "https://")):
                badges.append(target)
                is_shields = "img.shields.io" in target
                is_actions_badge = re.search(
                    r"https://github\.com/[\w.-]+/[\w.-]+/actions/workflows/[\w.-]+/badge\.svg",
                    target,
                )
                if not (is_shields or is_actions_badge):
                    problems.append("readme_badge_external_nonshields")
                if not alt:
                    problems.append("readme_badge_empty_alt")
                continue
            if target.startswith(("#", "mailto:")):
                problems.append("readme_image_anchor_target")
                continue
            if target.startswith("/"):
                problems.append(f"readme_image_absolute_path:{target}")
            asset = (root / target).resolve()
            if not asset.exists():
                problems.append(f"readme_image_missing:{target}")
            if not alt:
                problems.append(f"readme_image_empty_alt:{target}")
            elif alt == Path(target).name or len(alt) < 20:
                problems.append(f"readme_image_weak_alt:{target}")
            if asset.exists() and asset.stat().st_size > 500_000:
                problems.append(f"readme_image_too_large:{target}")
            featured.append(target)
            if manifest_text and target not in manifest_text:
                problems.append(f"readme_image_not_in_manifest:{target}")

        if len(featured) != len(set(featured)):
            problems.append("readme_duplicate_featured_image")

        if len(badges) > 3:
            problems.append("readme_too_many_badges")

        for match in _LINK_RE.finditer(text):
            target = match.group("path").strip()
            if _is_external_or_anchor(target):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            if clean.startswith("/"):
                problems.append(f"readme_link_absolute_path:{clean}")
            if not (root / clean).exists():
                problems.append(f"readme_link_missing:{clean}")

    workflows = root / ".github" / "workflows"
    if workflows.exists():
        for wf in sorted(workflows.glob("*.y*ml")):
            wf_text = wf.read_text()
            if "pull_request_target" in wf_text:
                problems.append(f"workflow_pull_request_target:{wf.name}")
            if re.search(r"contents:\s*write", wf_text):
                problems.append(f"workflow_contents_write:{wf.name}")

    return problems


def forbidden_data_files(root: Path) -> list[str]:
    bad: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        name = path.name.lower()
        if name.endswith((".env", ".pem", ".key", ".p12", ".pfx")):
            bad.append(path.relative_to(root).as_posix())
        if "cookie" in name or "storage-state" in name:
            bad.append(path.relative_to(root).as_posix())
        if name.endswith(".zip") and "public" not in name:
            if path.parent.name not in {"release"}:
                bad.append(path.relative_to(root).as_posix())
    return sorted(set(bad))
