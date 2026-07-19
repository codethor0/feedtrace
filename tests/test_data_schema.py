"""Schema and inventory tests for the sanitized public table."""

from pathlib import Path

import pandas as pd
import pytest

from feedtrace.schema import FORBIDDEN_COLUMNS, REQUIRED_COLUMNS, inventory_counts, load_sanitized_table

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sanitized" / "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv"


def test_required_columns_exact():
    df = load_sanitized_table(DATA)
    assert list(df.columns) == REQUIRED_COLUMNS


def test_inventory_counts():
    df = load_sanitized_table(DATA)
    counts = inventory_counts(df)
    assert counts["inventory_rows"] == 1192
    assert counts["originals"] == 1174
    assert counts["reposts"] == 18
    assert counts["missing_created_at"] == 1


def test_no_duplicate_rows():
    df = load_sanitized_table(DATA)
    assert not df.duplicated().any()


def test_forbidden_columns_absent():
    df = pd.read_csv(DATA)
    lowered = {str(c).lower() for c in df.columns}
    for name in FORBIDDEN_COLUMNS:
        assert name not in lowered


def test_pilot_denominators_documented():
    # Pilot denominators are paper-level; ensure public table does not invent them.
    df = load_sanitized_table(DATA)
    assert "members_reached" not in df.columns
    assert len(df) == 1192
