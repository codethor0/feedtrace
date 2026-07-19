"""Inventory and coverage classification for rendered figures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

EXPECTED_BASENAMES = {
    "cover_system_diagram.png",
    "fig01_lorenz_curve.png",
    "fig02_top_share_curve.png",
    "fig03_distribution_linear.png",
    "fig04_distribution_log.png",
    "fig05_qq_lognormal.png",
    "fig06_quantile_bootstrap.png",
    "fig07_distribution_comparison.png",
    "fig08_mixture_posterior.png",
    "fig09_regime_by_format.png",
    "fig10_regime_by_month.png",
    "fig11_age_vs_impressions.png",
    "fig12_sequence_semantic_effects.png",
    "fig13_changepoint_series.png",
    "fig14_public_chronology.png",
    "fig15_feed_vs_analytics.png",
    "fig16_impressions_vs_reached.png",
    "fig17_repeat_exposure.png",
    "fig18_oon_vs_impressions.png",
    "fig19_influence.png",
    "fig20_alias_map.png",
    "fig21_frozen_race_models.png",
    "fig22_claimB_uncertainty.png",
    "fig23_mechanism_dag.png",
}

NOT_PUBLICLY_REPRODUCIBLE = {
    "fig21_frozen_race_models.png",
    "fig22_claimB_uncertainty.png",
}

PARTIAL_FROM_AGGREGATES = EXPECTED_BASENAMES - NOT_PUBLICLY_REPRODUCIBLE


@dataclass(frozen=True)
class FigureInventory:
    present: tuple[str, ...]
    missing: tuple[str, ...]
    unexpected: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.missing and not self.unexpected


def inventory_rendered_figures(root: Path) -> FigureInventory:
    rendered = Path(root) / "figures" / "rendered"
    present = sorted(p.name for p in rendered.glob("*.png"))
    present_set = set(present)
    missing = sorted(EXPECTED_BASENAMES - present_set)
    unexpected = sorted(present_set - EXPECTED_BASENAMES)
    return FigureInventory(
        present=tuple(present),
        missing=tuple(missing),
        unexpected=tuple(unexpected),
    )


def coverage_for(name: str) -> str:
    if name in NOT_PUBLICLY_REPRODUCIBLE:
        return "not_publicly_reproducible"
    if name in PARTIAL_FROM_AGGREGATES:
        return "partially_reproducible"
    return "unknown"
