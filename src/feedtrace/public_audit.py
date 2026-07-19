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
