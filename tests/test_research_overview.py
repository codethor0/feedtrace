"""Tests for the chart-driven research-overview dashboard and its documentation."""

from __future__ import annotations

import hashlib
import json
import math
import re
import struct
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
SVG = ASSETS / "feedtrace-research-overview.svg"
PNG = ASSETS / "feedtrace-research-overview.png"
SQUARE = ASSETS / "feedtrace-research-overview-square.png"
README = ROOT / "README.md"
DOC = ROOT / "docs" / "RESEARCH_OVERVIEW_DIAGRAM.md"
SANITIZED = ROOT / "data" / "sanitized" / "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv"
CONCENTRATION = ROOT / "data" / "aggregate" / "concentration" / "CONCENTRATION_BY_STRATUM.csv"
MIXTURE = ROOT / "data" / "aggregate" / "mixture_models" / "MIXTURE_DIAGNOSTICS.csv"
BREAKS = ROOT / "data" / "aggregate" / "structural_breaks" / "STRUCTURAL_BREAK_SENSITIVITY.csv"
MULTIPLICITY = ROOT / "data" / "aggregate" / "multiplicity" / "R9_MULTIPLICITY_REPORTING_AUDIT.csv"

DOCUMENTED_FEED = (1200, 1350)
DOCUMENTED_SQUARE = (1080, 1080)

EMOJI_RE = re.compile(
    "["
    "\U0001f300-\U0001f6ff"
    "\U0001f900-\U0001faff"
    "\U00002700-\U000027bf"
    "\U0001f1e0-\U0001f1ff"
    "]"
)

SOURCE_FILES = (
    SANITIZED,
    CONCENTRATION,
    MIXTURE,
    BREAKS,
    MULTIPLICITY,
)


def _png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not a PNG"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def _svg_text() -> str:
    return SVG.read_text()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_chart_source_files_exist():
    for path in SOURCE_FILES:
        assert path.exists(), path


def test_all_three_visual_files_exist():
    for path in (SVG, PNG, SQUARE):
        assert path.exists(), path
        assert path.stat().st_size > 0, path


def test_readme_references_diagram_with_resolving_path_and_alt():
    text = README.read_text()
    match = re.search(
        r"!\[(?P<alt>[^\]]*)\]\((?P<path>docs/assets/feedtrace-research-overview\.svg)\)",
        text,
    )
    assert match, "README does not embed the research-overview SVG"
    assert (ROOT / match.group("path")).exists()
    alt = match.group("alt")
    assert len(alt) >= 100, "alt text should meaningfully describe the dashboard"
    for token in ("1,174", "Unresolved", "Lorenz", "Gini", "q = 0.078", "28-post"):
        assert token in alt, f"alt text missing {token!r}"


def test_svg_has_no_local_absolute_paths():
    text = _svg_text()
    assert "/Users/" not in text
    assert "C:\\Users\\" not in text
    assert "Users-thor" not in text


def test_svg_has_no_private_or_tool_metadata():
    lowered = _svg_text().lower()
    for token in ("cursor", "prompt", "@gmail.com", "co-authored", "tool_call"):
        assert token not in lowered, f"SVG contains {token!r}"


def test_svg_has_no_emojis_or_fancy_dashes():
    text = _svg_text()
    assert not EMOJI_RE.search(text), "SVG contains an emoji"
    assert "\u2014" not in text, "SVG contains an em dash"
    assert "\u2013" not in text, "SVG contains an en dash"


def test_svg_states_unresolved_verdict():
    assert "UNRESOLVED" in _svg_text()


def test_svg_includes_preliminary_label_limitation():
    assert "Preliminary automated labels" in _svg_text()


def test_svg_does_not_conflate_race_groups():
    text = _svg_text()
    assert "n = 61" in text
    assert "n = 83" in text
    assert "Composite Black-visibility group" in text
    assert "Direct Black-centered content" in text


def test_race_result_shows_q_with_raw_p():
    text = _svg_text()
    assert "0.0098" in text
    assert "q = 0.078" in text
    mult = pd.read_csv(MULTIPLICITY)
    row = mult[mult["test"] == "black_centered_content"].iloc[0]
    assert round(float(row["frozen_primary_raw_p"]), 4) == 0.0098
    assert round(float(row["bh_q_value"]), 3) == 0.078


def test_audience_expansion_labeled_exploratory_n28():
    text = _svg_text()
    assert "n = 28" in text
    assert "purposefully selected" in text
    assert "causal ranking mechanism" in text
    # Coefficient labels name each estimate directly.
    assert "Out-of-network share:" in text
    assert "Repeat-exposure ratio:" in text
    assert "rho = 0.71" in text
    assert "rho = -0.62" in text


def test_may_2026_change_point_labeled_upward():
    text = _svg_text()
    assert "May 2026" in text
    assert "upward" in text
    assert "2.74" in text
    assert "does not identify its cause" in text
    breaks = pd.read_csv(BREAKS)
    weekly = breaks[breaks["series"] == "weekly_median"].iloc[0]
    assert weekly["pelt_breaks"] == "2026-05-17"


def test_no_chart_claims_causation():
    text = _svg_text().lower()
    for forbidden in (
        "proves suppression",
        "algorithm change",
        "causal suppression confirmed",
        "platform intent",
    ):
        # "platform intent" appears only in the disclaimer about what is NOT established.
        if forbidden == "platform intent":
            assert "do not independently establish platform intent" in text
            continue
        assert forbidden not in text, forbidden


def test_svg_statistics_match_tracked_data():
    text = _svg_text()
    df = pd.read_csv(SANITIZED)
    originals = df[df["is_original_post"].astype(bool)]
    impressions = originals["feed_impressions"].dropna()

    assert f"{len(originals):,}" in text
    assert "impressions" in text.lower()
    assert str(int(impressions.median())) in text
    assert f"{int(impressions.max()):,}" in text
    assert round(float(np.percentile(impressions, 99)), 1) == 1518.5
    assert "1,518" in text
    assert round(float(np.percentile(impressions, 95)), 1) == 254.4
    assert "254" in text

    row = pd.read_csv(CONCENTRATION).iloc[0]
    assert f"{round(float(row['gini']), 3)}" in text
    assert f"{round(float(row['top1']) * 100, 1)}" in text

    mix = pd.read_csv(MIXTURE)
    one = mix[mix["components"] == 1].iloc[0]
    mu = float(one["log_means"])
    sd = float(one["log_sds"])
    assert (round(mu, 3), round(sd, 3)) == (4.096, 0.941)
    fitted_p99 = math.exp(mu + 2.3263478740408408 * sd)
    assert round(fitted_p99) == 537
    assert "537" in text


def test_race_statistics_present():
    text = _svg_text()
    for token in ("82", "52", "-23.7%", "-37.8%", "-6.3%"):
        assert token in text, f"SVG missing {token!r}"


def test_png_dimensions_match_documented():
    assert _png_dimensions(PNG) == DOCUMENTED_FEED
    assert _png_dimensions(SQUARE) == DOCUMENTED_SQUARE
    doc = DOC.read_text()
    assert "1200 x 1350" in doc
    assert "1080 x 1080" in doc


def test_documentation_checksums_match_files():
    doc = DOC.read_text()
    for path in (SVG, PNG, SQUARE):
        assert _sha256(path) in doc, f"checksum for {path.name} not in documentation"


def test_visual_files_in_public_manifest():
    manifest = json.loads((ROOT / "release" / "PUBLIC_MANIFEST.json").read_text())
    listed = {entry["path"]: entry for entry in manifest["files"]}
    for path in (SVG, PNG, SQUARE):
        rel = path.relative_to(ROOT).as_posix()
        assert rel in listed, f"{rel} not in PUBLIC_MANIFEST.json"
        assert listed[rel]["sha256"] == _sha256(path), rel


def test_documentation_lists_chart_sources():
    doc = DOC.read_text()
    for name in (
        "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv",
        "CONCENTRATION_BY_STRATUM.csv",
        "MIXTURE_DIAGNOSTICS.csv",
        "STRUCTURAL_BREAK_SENSITIVITY.csv",
        "R9_MULTIPLICITY_REPORTING_AUDIT.csv",
    ):
        assert name in doc, name
