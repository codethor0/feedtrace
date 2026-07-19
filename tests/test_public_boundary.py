"""Public-boundary and privacy scans."""

from pathlib import Path

from feedtrace.figure_inventory import inventory_rendered_figures
from feedtrace.public_audit import forbidden_data_files, scan_public_tree
from feedtrace.schema import inventory_counts, load_sanitized_table

ROOT = Path(__file__).resolve().parents[1]


def test_public_boundary_clean():
    findings = scan_public_tree(ROOT)
    assert findings == [], [(f.path, f.line, f.rule) for f in findings[:20]]


def test_no_forbidden_data_files():
    assert forbidden_data_files(ROOT) == []


def test_figure_inventory_complete():
    inv = inventory_rendered_figures(ROOT)
    assert inv.ok, (inv.missing, inv.unexpected)
    assert len(inv.present) == 24


def test_frozen_scientific_counts():
    df = load_sanitized_table(
        ROOT / "data" / "sanitized" / "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv"
    )
    counts = inventory_counts(df)
    assert counts["inventory_rows"] == 1192
    assert counts["originals"] == 1174
    assert counts["reposts"] == 18
    assert counts["missing_created_at"] == 1
    # Repost rows may lack feed impressions; all originals have them.
    assert counts["missing_feed_impressions"] == 18
    originals = df[df["is_original_post"].astype(bool)]
    assert originals["feed_impressions"].isna().sum() == 0
