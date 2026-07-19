"""Schema validation for the sanitized non-race analytic table."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS: list[str] = [
    "created_at",
    "is_original_post",
    "feed_impressions",
    "feed_impressions_post_age_hours",
    "word_count",
    "hashtag_count",
    "has_image",
    "has_video",
    "has_document",
]

FORBIDDEN_COLUMNS: tuple[str, ...] = (
    "full_post_text",
    "feed_post_text",
    "analysis_text",
    "post_url",
    "activity_urn",
    "external_url",
    "reposted_author",
    "viewer",
    "race_label",
    "race_flag",
    "black_centered",
)


class SchemaError(ValueError):
    """Raised when a public input file fails schema validation."""


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SchemaError(f"Missing required columns: {missing}")
    forbidden = [c for c in df.columns if str(c).lower() in FORBIDDEN_COLUMNS]
    if forbidden:
        raise SchemaError(f"Forbidden columns present: {forbidden}")
    extras = [c for c in df.columns if c not in REQUIRED_COLUMNS]
    if extras:
        raise SchemaError(f"Unexpected columns outside the public allowlist: {extras}")


def load_sanitized_table(path: Path) -> pd.DataFrame:
    """Load and validate the public sanitized analytic table."""
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    df = pd.read_csv(path)
    validate_columns(df)
    if len(df) == 0:
        raise SchemaError("Sanitized table is empty")
    if df.duplicated().any():
        raise SchemaError("Sanitized table contains duplicate rows")
    return df


def inventory_counts(df: pd.DataFrame) -> dict[str, int]:
    originals = int(df["is_original_post"].astype(bool).sum())
    created = df["created_at"]
    as_str = created.where(~created.isna(), other="").astype(str).str.strip()
    missing_created = int((created.isna() | as_str.isin({"", "nan", "NaT", "None"})).sum())
    return {
        "inventory_rows": int(len(df)),
        "originals": originals,
        "reposts": int(len(df) - originals),
        "missing_created_at": missing_created,
        "missing_feed_impressions": int(df["feed_impressions"].isna().sum()),
    }
