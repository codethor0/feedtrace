#!/usr/bin/env python3
"""Build the FeedTrace research-overview dashboard (SVG and PNG).

A chart-driven visual summary of the project for repository visitors. Every
plotted value comes from tracked public data or frozen aggregate tables:

- data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv (impressions, dates)
- data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv (Gini, top shares)
- data/aggregate/mixture_models/MIXTURE_DIAGNOSTICS.csv (frozen lognormal fit)
- data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv (break dates)
- data/aggregate/multiplicity/R9_MULTIPLICITY_REPORTING_AUDIT.csv (raw p, BH q)
- frozen values transcribed in paper/source (race effect CI, pilot correlations)

The per-post detailed-analytics pilot rows (n = 28) are withheld (Level B), so
the audience-expansion chart plots the frozen pilot correlations rather than a
per-post scatter; no observation is invented.

Rendering is deterministic: matplotlib-bundled DejaVu Sans, fixed SVG hash salt,
stripped variable metadata. Rebuild with:

    pip install -e ".[viz]"
    python scripts/build_research_overview.py
"""

from __future__ import annotations

import math
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from scipy.stats import lognorm  # noqa: E402

matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["path.simplify"] = False
matplotlib.rcParams["axes.unicode_minus"] = False
# Fixed salt so SVG element ids (clip paths) are stable across runs.
matplotlib.rcParams["svg.hashsalt"] = "feedtrace-research-overview"

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
DPI = 100

INK = "#1b2430"
MUTED = "#4a5563"
GRID = "#d9e0e8"
PANEL = "#f6f8fb"
BLUE = "#1f4e79"
TEAL = "#217f78"
GREEN = "#2f6b3e"
SLATE = "#414b57"
AMBER = "#b26a00"
AMBER_BG = "#fff5e6"
AMBER_INK = "#7a4700"
RED = "#9b2226"

TITLE = "FeedTrace"
SUBTITLE = (
    "A longitudinal audit of LinkedIn reach, ranking, audience expansion, "
    "and racial visibility"
)
SCOPE_NOTE = (
    "Single-account observational study, September 6, 2025 through July 18, 2026."
)
URL = "github.com/codethor0/feedtrace"
MATERIALS = (
    "Public repository: paper, technical supplement, sanitized code, aggregate "
    "data, figures, reproduction scripts, checksums, and manual-review plan."
)
DISCLAIMER = (
    "Independent, preliminary, single-account observational research. The results "
    "do not independently establish platform intent, causal suppression, or "
    "platform-wide effects."
)

# Frozen values transcribed from the published paper sources (not re-estimated).
RACE_EFFECT_PCT = -23.7
RACE_CI_PCT = (-37.8, -6.3)
RACE_MEDIANS = {"Direct Black-centered\ncontent (n = 61)": 82, "All other originals\n(n = 1,113)": 52}
PILOT_CORRELATIONS = [
    (
        "Out-of-network\naudience share",
        0.71,
        "Out-of-network share:\nrho = 0.71, p = 2.6e-05",
    ),
    (
        "Repeat-exposure\nratio",
        -0.62,
        "Repeat-exposure ratio:\nrho = -0.62, p = 4.4e-04",
    ),
]
DESCRIPTIVE_PRE_LN = 3.76
DESCRIPTIVE_POST_LN = 4.77
DESCRIPTIVE_FACTOR = 2.74


def load_inputs() -> dict:
    """Load and cross-check every tracked input the dashboard plots."""
    df = pd.read_csv(
        ROOT / "data" / "sanitized" / "R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv",
        parse_dates=["created_at"],
    )
    orig = df[df["is_original_post"].astype(bool)].copy()
    imp = orig["feed_impressions"].dropna().astype(float)
    assert len(imp) == 1174, len(imp)
    assert int(imp.median()) == 53
    assert int(imp.max()) == 67349

    conc = pd.read_csv(
        ROOT / "data" / "aggregate" / "concentration" / "CONCENTRATION_BY_STRATUM.csv"
    ).iloc[0]
    gini = round(float(conc["gini"]), 3)
    top1 = round(float(conc["top1"]) * 100, 1)
    assert gini == 0.799 and top1 == 63.5, (gini, top1)

    mix = pd.read_csv(
        ROOT / "data" / "aggregate" / "mixture_models" / "MIXTURE_DIAGNOSTICS.csv"
    )
    one = mix[mix["components"] == 1].iloc[0]
    ln_mu = float(one["log_means"])
    ln_sd = float(one["log_sds"])
    assert (round(ln_mu, 3), round(ln_sd, 3)) == (4.096, 0.941)

    mult = pd.read_csv(
        ROOT / "data" / "aggregate" / "multiplicity" / "R9_MULTIPLICITY_REPORTING_AUDIT.csv"
    )
    row = mult[mult["test"] == "black_centered_content"].iloc[0]
    raw_p = float(row["frozen_primary_raw_p"])
    bh_q = float(row["bh_q_value"])
    assert round(raw_p, 4) == 0.0098 and round(bh_q, 3) == 0.078

    breaks = pd.read_csv(
        ROOT / "data" / "aggregate" / "structural_breaks" / "STRUCTURAL_BREAK_SENSITIVITY.csv"
    )
    weekly = breaks[breaks["series"] == "weekly_median"].iloc[0]
    assert weekly["pelt_breaks"] == "2026-05-17"

    monthly = (
        orig.dropna(subset=["feed_impressions"])
        .assign(month=lambda d: d["created_at"].dt.tz_localize(None).dt.to_period("M"))
        .groupby("month")["feed_impressions"]
        .apply(lambda s: float(np.log(s).mean()))
    )
    pre = monthly[monthly.index <= pd.Period("2026-04")]
    post = monthly[monthly.index >= pd.Period("2026-05")]
    assert round(pre.mean(), 2) == DESCRIPTIVE_PRE_LN
    assert round(post.mean(), 2) == DESCRIPTIVE_POST_LN

    return {
        "imp": np.sort(imp.values),
        "gini": gini,
        "top1": top1,
        "ln_mu": ln_mu,
        "ln_sd": ln_sd,
        "raw_p": raw_p,
        "bh_q": bh_q,
        "monthly": monthly,
    }


def _style_axes(ax, fs=9):
    ax.set_facecolor("white")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=fs)
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)


def _chart_title(ax, text, color=INK, fs=None):
    if fs is None:
        fs = 12
    ax.set_title(text, fontsize=fs, fontweight="bold", color=color, loc="left", pad=8)


def _caption(ax, text, fs=8.2, drop_in=0.55):
    """Wrap a caption to the axes width and place it below in figure coords.

    drop_in is the distance in inches below the axes bottom, leaving room for
    tick labels and the x-axis label.
    """
    fig = ax.figure
    fig_w, fig_h = fig.get_size_inches()
    pos = ax.get_position()
    axes_w_in = pos.width * fig_w
    chars = max(30, int(axes_w_in / (fs * 0.0074)))
    wrapped = "\n".join(textwrap.wrap(text, chars))
    fig.text(pos.x0, pos.y0 - drop_in / fig_h, wrapped, fontsize=fs, color=MUTED,
             ha="left", va="top", linespacing=1.35)


# ---------------------------------------------------------------- charts


def chart_lorenz(ax, d, fs=9, cap_drop=0.55):
    imp = d["imp"]
    n = len(imp)
    x = np.arange(0, n + 1) / n
    y = np.concatenate([[0.0], np.cumsum(imp) / imp.sum()])
    ax.plot([0, 1], [0, 1], color=MUTED, lw=1.1, ls="--", label="Perfect equality")
    ax.plot(x, y, color=BLUE, lw=2.4, label="Observed (Lorenz curve)")
    ax.fill_between(x, y, x, color=BLUE, alpha=0.10)
    _style_axes(ax, fs)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Cumulative share of posts", fontsize=fs, color=MUTED)
    ax.set_ylabel("Cumulative share of impressions", fontsize=fs, color=MUTED)

    y50 = float(np.interp(0.5, x, y))
    ax.plot([0.5], [y50], "o", color=RED, ms=5, zorder=5)
    ax.annotate(
        "Bottom 50% of posts:\n7.3% of impressions",
        xy=(0.5, y50), xytext=(0.53, 0.30), fontsize=fs, color=INK,
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0),
    )
    y99 = float(np.interp(0.99, x, y))
    ax.plot([0.99], [y99], "o", color=RED, ms=5, zorder=5)
    ax.annotate(
        "Top 1% of posts:\n63.5% of impressions",
        xy=(0.99, y99), xytext=(0.44, 0.72), fontsize=fs, color=INK,
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0),
    )
    ax.text(0.04, 0.90, f"Gini = {d['gini']}", transform=ax.transAxes,
            fontsize=fs + 3, fontweight="bold", color=BLUE)
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.86), fontsize=fs - 0.5,
              frameon=False)
    _chart_title(ax, "Reach Is Extremely Concentrated", BLUE, fs=fs + 3)
    _caption(ax,
             "Cumulative impression share across all 1,174 original posts, sorted "
             "by recorded impressions. Source: sanitized analytic table and "
             "CONCENTRATION_BY_STRATUM.csv.", drop_in=cap_drop)


def chart_ccdf(ax, d, fs=9, cap_drop=0.55, short_title=False, title=None):
    imp = d["imp"]
    n = len(imp)
    sf = 1.0 - np.arange(1, n + 1) / n
    sf[-1] = 1.0 / n
    ax.loglog(imp, sf, drawstyle="steps-post", color=GREEN, lw=2.0,
              label="Observed posts")
    grid_x = np.logspace(0, math.log10(80000), 300)
    fitted = lognorm(s=d["ln_sd"], scale=math.exp(d["ln_mu"]))
    ax.loglog(grid_x, fitted.sf(grid_x), color=MUTED, lw=1.4, ls="--",
              label="Fitted lognormal (frozen fit)")
    _style_axes(ax, fs)
    ax.set_xlim(1, 1e5)
    ax.set_ylim(5e-4, 1.05)
    ax.set_xlabel("Recorded impressions (log scale)", fontsize=fs, color=MUTED)
    ax.set_ylabel("Share of posts above x (log)", fontsize=fs, color=MUTED)

    marks = [(53, 0.5, "Median: 53", (95, 0.55)),
             (254, 0.05, "95th pct: 254", (430, 0.075)),
             (1518, 0.01, "99th pct: 1,518", (2500, 0.016))]
    for xv, yv, label, (tx, ty) in marks:
        ax.plot([xv], [yv], "o", color=RED, ms=4.5, zorder=5)
        ax.annotate(label, xy=(xv, yv), xytext=(tx, ty), fontsize=fs - 0.5,
                    color=INK)
    ax.plot([67349], [1.0 / n], "o", color=RED, ms=4.5, zorder=5)
    ax.annotate("Max: 67,349", xy=(67349, 1.0 / n), xytext=(2400, 5.6e-4),
                fontsize=fs - 0.5, color=INK)
    ax.annotate(
        "Lognormal 99th pct: about 537\nObserved 99th pct: about 1,518",
        xy=(537, 0.01), xytext=(1.6, 3.2e-3), fontsize=fs - 0.5, color=AMBER_INK,
        arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.0),
    )
    ax.legend(loc="upper right", fontsize=fs - 0.5, frameon=False)
    if title is None:
        title = (
            "A Heavier Upper Tail Than Lognormal Predicts"
            if short_title
            else "The Upper Tail Is Much Heavier Than a Simple Lognormal Predicts"
        )
    _chart_title(ax, title, GREEN, fs=fs + 3)
    _caption(ax,
             "No single tested continuous distribution fully fits both the body "
             "and upper tail. Sources: sanitized analytic table; frozen "
             "one-component fit in MIXTURE_DIAGNOSTICS.csv.", drop_in=cap_drop)


def chart_time(ax, d, fs=9, cap_drop=0.8):
    monthly = d["monthly"]
    labels = [p.strftime("%b %y") for p in monthly.index]
    xs = np.arange(len(monthly))
    ax.plot(xs, monthly.values, "-o", color=TEAL, lw=2.0, ms=4.5,
            label="Monthly mean of ln(impressions)")
    split = 7.5  # between Apr 2026 and May 2026
    ax.axvline(split, color=AMBER, lw=1.6, ls="--")
    ax.hlines(DESCRIPTIVE_PRE_LN, -0.3, split, color=MUTED, lw=1.2, ls=":")
    ax.hlines(DESCRIPTIVE_POST_LN, split, len(monthly) - 0.7, color=MUTED, lw=1.2,
              ls=":")
    _style_axes(ax, fs)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=fs - 1)
    ax.set_ylabel("Monthly mean of ln(impressions)", fontsize=fs, color=MUTED)
    ax.set_ylim(3.2, 5.75)
    ax.text(split + 0.12, 5.68, "Descriptive change point,\nMay 2026 (weekly break "
            "2026-05-17)", fontsize=fs - 0.8, color=AMBER_INK, va="top")
    ax.text(0.4, DESCRIPTIVE_PRE_LN - 0.14, "Pre level 3.76 (geo. mean about 43)",
            fontsize=fs - 0.8, color=MUTED, va="top")
    ax.text(len(monthly) - 0.7, DESCRIPTIVE_POST_LN - 0.12,
            "Post level 4.77\n(geo. mean about 118)", fontsize=fs - 0.8,
            color=MUTED, va="top", ha="right")
    ax.annotate(
        "Post-split monthly level about 2.74x\nthe earlier level (upward, descriptive)",
        xy=(8.6, 4.95), xytext=(1.2, 4.95), fontsize=fs, color=INK,
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0),
    )
    _chart_title(ax, "Recorded Reach Changed Over Time", TEAL, fs=fs + 3)
    _caption(ax,
             "The shift was upward and descriptive. The analysis does not identify "
             "its cause. Sources: sanitized analytic table; break dates in "
             "STRUCTURAL_BREAK_SENSITIVITY.csv.", drop_in=cap_drop)


def chart_pilot(ax, fs=9, cap_drop=0.55, short_title=False):
    ys = [1, 0]
    ax.axvline(0, color=MUTED, lw=1.2)
    for (label, rho, note), y in zip(PILOT_CORRELATIONS, ys):
        color = TEAL if rho > 0 else SLATE
        ax.plot([0, rho], [y, y], color=color, lw=3.0, solid_capstyle="round")
        ax.plot([rho], [y], "o", color=color, ms=9)
        # Place the coefficient label beside the marker with the measure name
        # included so the two estimates remain unambiguous without relying on
        # the y-axis alone.
        ax.text(
            rho - 0.04 if rho > 0 else rho + 0.04,
            y + 0.28,
            note,
            fontsize=fs - 0.5,
            color=INK,
            ha="right" if rho > 0 else "left",
            va="bottom",
        )
    _style_axes(ax, fs)
    ax.set_yticks(ys)
    ax.set_yticklabels([p[0] for p in PILOT_CORRELATIONS], fontsize=fs)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.7, 1.85)
    ax.set_xlabel("Spearman correlation with recorded impressions (n = 28)",
                  fontsize=fs, color=MUTED)
    _chart_title(
        ax,
        "Reach Rose With Audience Expansion (Pilot)"
        if short_title
        else "Higher Reach Was Associated With Broader Audience Expansion",
        TEAL,
        fs=fs + 3,
    )
    _caption(ax,
             "Exploratory associations in a purposefully selected analytics pilot "
             "(n = 28). Per-post pilot rows are withheld for privacy, so the frozen "
             "correlations are shown instead of a scatter. Not representative of "
             "the full 1,174-post population and not evidence of a causal ranking "
             "mechanism. Source: frozen pilot statistics in the paper sources.",
             drop_in=cap_drop)


def chart_race_medians(ax, fs=9):
    labels = list(RACE_MEDIANS)
    values = list(RACE_MEDIANS.values())
    bars = ax.barh([1, 0], values, height=0.55, color=[AMBER, SLATE])
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                str(val), fontsize=fs + 1, fontweight="bold", color=INK,
                va="center")
    _style_axes(ax, fs)
    ax.set_yticks([1, 0])
    ax.set_yticklabels(labels, fontsize=fs - 0.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Raw median recorded impressions", fontsize=fs, color=MUTED)
    ax.grid(axis="y", visible=False)


def chart_race_effect(ax, d, fs=9):
    lo, hi = RACE_CI_PCT
    ax.axvline(0, color=MUTED, lw=1.4)
    ax.text(0, 1.28, "No difference", fontsize=fs - 1, color=MUTED, ha="center")
    ax.plot([lo, hi], [0.6, 0.6], color=AMBER, lw=3.0, solid_capstyle="round")
    ax.plot([RACE_EFFECT_PCT], [0.6], "D", color=AMBER, ms=9)
    ax.text(RACE_EFFECT_PCT, 0.9, f"{RACE_EFFECT_PCT}%", fontsize=fs + 1,
            fontweight="bold", color=AMBER_INK, ha="center")
    ax.text((lo + hi) / 2, 0.24,
            f"95% CI {lo}% to {hi}%\nraw p = 0.0098, BH-FDR q = 0.078",
            fontsize=fs - 0.5, color=INK, ha="center", va="top")
    _style_axes(ax, fs)
    ax.set_yticks([])
    ax.set_xlim(-45, 15)
    ax.set_ylim(-0.7, 1.55)
    ax.set_xlabel("Adjusted change in recorded impressions (%)", fontsize=fs,
                  color=MUTED)
    ax.grid(axis="y", visible=False)


RACE_NOTES = (
    "Within-month and within-format comparisons did not reproduce the reduction. "
    "Preliminary automated labels, not human validated; most source text from "
    "possibly truncated previews. Direct Black-centered content (n = 61) is "
    "distinct from the Composite Black-visibility group (n = 83). Not proof of "
    "suppression and not proof of fairness."
)


def add_race_block(fig, rect, d, fs=9, notes_fs=8.2, stacked=False):
    """Add the race panel (title, two charts, verdict, notes) inside rect.

    rect is (x0, y0, width, height) in figure fractions; y0 is the bottom.
    When stacked is True, the two charts are placed one above the other.
    """
    x0, y0, w, h = rect
    fig_w, fig_h = fig.get_size_inches()

    title_y = y0 + h
    fig.text(x0, title_y, "The Main Race-Related Result Remains Unresolved",
             fontsize=fs + 3, fontweight="bold", color=AMBER_INK, va="top")

    badge_w_in, badge_h_in = 1.55, 0.34
    badge_w, badge_h = badge_w_in / fig_w, badge_h_in / fig_h
    bx = x0 + w - badge_w
    by = title_y - badge_h + 0.004
    fig.patches.append(
        FancyBboxPatch((bx, by), badge_w, badge_h,
                       boxstyle="round,pad=0.004,rounding_size=0.008",
                       transform=fig.transFigure, linewidth=0, facecolor=AMBER,
                       zorder=5)
    )
    fig.text(bx + badge_w / 2, by + badge_h / 2, "UNRESOLVED", fontsize=fs + 2,
             fontweight="bold", color="white", ha="center", va="center", zorder=6)

    title_gap = 0.45 / fig_h
    notes_lines = textwrap.wrap(RACE_NOTES, max(60, int(w * fig_w / (notes_fs * 0.0074))))
    notes_h = (len(notes_lines) * notes_fs * 1.5 / 72.0 + 0.12) / fig_h

    chart_top = title_y - title_gap
    chart_bottom = y0 + notes_h + 0.55 / fig_h  # room for x labels
    chart_h = chart_top - chart_bottom
    if stacked:
        half = (chart_h - 0.55 / fig_h) / 2
        ax1 = fig.add_axes([x0 + 0.13 * w, chart_bottom + half + 0.55 / fig_h,
                            w * 0.85, half])
        ax2 = fig.add_axes([x0 + 0.13 * w, chart_bottom, w * 0.85, half])
    else:
        ax1 = fig.add_axes([x0 + 0.09 * w, chart_bottom, w * 0.36, chart_h])
        ax2 = fig.add_axes([x0 + w * 0.56, chart_bottom, w * 0.42, chart_h])
    chart_race_medians(ax1, fs)
    chart_race_effect(ax2, d, fs)
    fig.text(x0, y0 + notes_h, "\n".join(notes_lines), fontsize=notes_fs,
             color=MUTED, va="top", linespacing=1.4)


# ---------------------------------------------------------- page furniture


METRICS = [
    ("1,174", "original posts"),
    ("53", "median impressions"),
    ("0.799", "Gini coefficient"),
    ("63.5%", "top 1 percent share"),
    ("67,349", "maximum impressions"),
]


def add_metric_cards(fig, y, height, fs_big=17, fs_small=8.8, x0=0.03, x1=0.97):
    n = len(METRICS)
    gap = 0.012
    card_w = (x1 - x0 - gap * (n - 1)) / n
    for i, (value, label) in enumerate(METRICS):
        cx = x0 + i * (card_w + gap)
        fig.patches.append(
            FancyBboxPatch((cx, y), card_w, height,
                           boxstyle="round,pad=0.003,rounding_size=0.008",
                           transform=fig.transFigure, linewidth=1.0,
                           edgecolor=GRID, facecolor=PANEL, zorder=2)
        )
        fig.text(cx + card_w / 2, y + height * 0.60, value, fontsize=fs_big,
                 fontweight="bold", color=BLUE, ha="center", va="center", zorder=3)
        fig.text(cx + card_w / 2, y + height * 0.22, label, fontsize=fs_small,
                 color=MUTED, ha="center", va="center", zorder=3)


def add_header(fig, title_fs=26, sub_fs=11.5, y_title=0.975, x=0.03):
    fig.text(x, y_title, TITLE, fontsize=title_fs, fontweight="bold", color=INK,
             va="top")
    fig.text(x, y_title - 0.033, SUBTITLE, fontsize=sub_fs, color=MUTED, va="top")


def add_footer(fig, y=0.012, fs=8.6, x=0.03):
    fig.text(x, y + 0.030, MATERIALS + "  " + URL, fontsize=fs, color=INK,
             va="bottom", fontweight="bold")
    fig.text(x, y, DISCLAIMER, fontsize=fs, color=MUTED, va="bottom")


def _new_fig(w, h):
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    fig.patch.set_facecolor("white")
    return fig


# ---------------------------------------------------------------- layouts


def render_landscape(d):
    """GitHub README version: 1600 x 1400 px, five charts."""
    fig = _new_fig(16.0, 14.0)
    add_header(fig, y_title=0.982)
    fig.text(0.97, 0.982, SCOPE_NOTE, fontsize=9.5, color=MUTED, ha="right",
             va="top")
    add_metric_cards(fig, y=0.878, height=0.052)

    # Row 1: Lorenz (prominent, left) and CCDF (right).
    ax_lorenz = fig.add_axes([0.055, 0.63, 0.40, 0.215])
    chart_lorenz(ax_lorenz, d, fs=9.5, cap_drop=0.62)
    ax_ccdf = fig.add_axes([0.565, 0.63, 0.40, 0.215])
    chart_ccdf(ax_ccdf, d, fs=9.5, cap_drop=0.62)

    # Row 2: time series (left) and pilot correlations (right).
    ax_time = fig.add_axes([0.055, 0.39, 0.40, 0.135])
    chart_time(ax_time, d, fs=9.5, cap_drop=0.95)
    ax_pilot = fig.add_axes([0.565, 0.39, 0.40, 0.135])
    chart_pilot(ax_pilot, fs=9.5, cap_drop=0.62)

    # Row 3: race block, full width.
    add_race_block(fig, (0.055, 0.06, 0.91, 0.215), d, fs=10, notes_fs=8.8)
    add_footer(fig, y=0.008)
    return fig


def render_feed(d):
    """LinkedIn feed (portrait) version: 1200 x 1350 px, five charts stacked."""
    fig = _new_fig(12.0, 13.5)
    add_header(fig, title_fs=23, sub_fs=10.5, y_title=0.982)
    fig.text(0.96, 0.982, SCOPE_NOTE, fontsize=8.2, color=MUTED, ha="right",
             va="top")
    add_metric_cards(fig, y=0.878, height=0.05, fs_big=15, fs_small=8,
                     x0=0.04, x1=0.96)

    ax_lorenz = fig.add_axes([0.085, 0.645, 0.385, 0.185])
    chart_lorenz(ax_lorenz, d, fs=8.5, cap_drop=0.6)
    ax_ccdf = fig.add_axes([0.60, 0.645, 0.375, 0.185])
    chart_ccdf(ax_ccdf, d, fs=8.5, cap_drop=0.6, short_title=True)

    ax_time = fig.add_axes([0.085, 0.395, 0.385, 0.14])
    chart_time(ax_time, d, fs=8.5, cap_drop=0.9)
    ax_pilot = fig.add_axes([0.60, 0.395, 0.375, 0.14])
    chart_pilot(ax_pilot, fs=8.5, cap_drop=0.6, short_title=True)

    add_race_block(fig, (0.055, 0.065, 0.9, 0.19), d, fs=9, notes_fs=8.0)
    add_footer(fig, y=0.010, fs=8.0, x=0.04)
    return fig


def render_square(d):
    """LinkedIn square version: 1080 x 1080 px, four charts."""
    fig = _new_fig(10.8, 10.8)
    add_header(fig, title_fs=21, sub_fs=9.0, y_title=0.982)
    fig.text(0.96, 0.982, SCOPE_NOTE, fontsize=7.4, color=MUTED, ha="right",
             va="top")
    add_metric_cards(fig, y=0.858, height=0.056, fs_big=14, fs_small=7.6,
                     x0=0.04, x1=0.96)

    ax_lorenz = fig.add_axes([0.09, 0.615, 0.375, 0.175])
    chart_lorenz(ax_lorenz, d, fs=7.8, cap_drop=0.5)
    ax_ccdf = fig.add_axes([0.60, 0.615, 0.375, 0.175])
    chart_ccdf(ax_ccdf, d, fs=7.8, cap_drop=0.5, short_title=True)

    ax_time = fig.add_axes([0.09, 0.385, 0.86, 0.10])
    chart_time(ax_time, d, fs=7.8, cap_drop=0.78)

    add_race_block(fig, (0.055, 0.05, 0.9, 0.225), d, fs=8, notes_fs=7.2)
    add_footer(fig, y=0.010, fs=7.4, x=0.04)
    return fig


def build(out_dir: Path | None = None) -> dict[str, Path]:
    out_dir = Path(out_dir) if out_dir else ASSETS
    out_dir.mkdir(parents=True, exist_ok=True)
    d = load_inputs()

    svg = out_dir / "feedtrace-research-overview.svg"
    png = out_dir / "feedtrace-research-overview.png"
    square = out_dir / "feedtrace-research-overview-square.png"

    fig = render_landscape(d)
    fig.savefig(svg, format="svg", metadata={"Date": None})
    plt.close(fig)
    # Matplotlib path dumps leave trailing spaces; strip them so git
    # whitespace checks stay clean.
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n"
    )

    fig_feed = render_feed(d)
    fig_feed.savefig(png, format="png", dpi=DPI, metadata={"Software": None})
    plt.close(fig_feed)

    fig_sq = render_square(d)
    fig_sq.savefig(square, format="png", dpi=DPI, metadata={"Software": None})
    plt.close(fig_sq)

    return {"svg": svg, "png": png, "square": square}


if __name__ == "__main__":
    import hashlib

    paths = build()
    for key, path in paths.items():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{key}: {path.name}  {path.stat().st_size} bytes  {digest}")
