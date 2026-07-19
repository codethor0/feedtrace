# README visuals manifest

This manifest records every figure featured in the root `README.md`. All featured
figures link directly to the tracked rendered files under `figures/rendered/`.
No optimized README copies were required: every featured file is already small
(under 140 KB), uses a legible aspect ratio, and carries no embedded local paths,
so a separate `docs/assets/readme/` copy would only duplicate bytes. If a future
figure needs resizing, place the optimized copy under `docs/assets/readme/` and
record both source and optimized checksums here.

Figure plotting code is not part of the public package. The "reproduction" column
gives the public command that checks the figure's underlying values against a
tracked aggregate table where that is possible; figures marked not-public depend
on withheld inputs and cannot be checked from public row-level data.

## Featured figure 1: Reach concentration

- README placement: Key findings, section 1
- Display title: Recorded impressions are extremely concentrated
- Source figure: `figures/rendered/fig01_lorenz_curve.png`
- Optimized figure: none (source used directly)
- Paper figure number: 4
- Alt text: Lorenz curve of recorded impressions across 1,174 original posts. The
  cumulative-share curve bows far below the diagonal line of equality, showing
  that a small fraction of posts holds most impressions.
- Caption: Lorenz curve (paper Figure 4). Cumulative share of posts on the
  horizontal axis, cumulative share of recorded impressions on the vertical axis,
  with the dashed diagonal marking perfect equality.
- Source data: `data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv`
- Reproduction: `python -c "import pandas as pd; r=pd.read_csv('data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv').iloc[0]; print(round(r.gini,3), round(r.top1,3), round(r.effective_n,1))"`
- Source checksum (SHA-256): `35819757e07dfdf51ae7353f1d9907f22483ee2e504d2b24481bf2f033d77915`
- README-copy checksum: not applicable

## Featured figure 2: Heavy upper tail and model fit

- README placement: Key findings, section 2
- Display title: A heavy upper tail that no single distribution fits
- Source figure: `figures/rendered/fig05_qq_lognormal.png`
- Optimized figure: none (source used directly)
- Paper figure number: 6
- Alt text: Quantile-quantile plot of empirical log recorded impressions against
  theoretical lognormal quantiles. Body points track the reference line, while
  the highlighted upper 5 percent of posts rise well above it, marking a
  heavy-tail departure.
- Caption: Lognormal Q-Q plot (paper Figure 6). Points on the dashed line would
  indicate a lognormal fit; the highlighted upper-tail points depart upward.
- Source data: `data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproduction: `python -c "import pandas as pd, numpy as np; s=pd.read_csv('data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv'); print(round(np.log(s['feed_impressions'].dropna()+1).skew(),3))"`
- Source checksum (SHA-256): `6de0ad799446d9c97943a18776d6410d68a6b5fa391eeca4dcc8afa1ec291094`
- README-copy checksum: not applicable

## Featured figure 3: Time pattern

- README placement: Key findings, section 3
- Display title: A descriptive upward shift in mid-2026
- Source figure: `figures/rendered/fig13_changepoint_series.png`
- Optimized figure: none (source used directly)
- Paper figure number: 15
- Alt text: Two stacked time series of log recorded impressions from September 2025
  to mid-2026. Both the weekly median and the monthly mean rise sharply after a
  marked change point in mid-May 2026.
- Caption: Change-point series (paper Figure 15). Weekly median (top) and monthly
  mean (bottom) of log impressions, with the detected break and selected split
  marked. The shift is upward and descriptive; the analysis does not identify a
  cause.
- Source data: `data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv`
- Reproduction: `python -c "import pandas as pd; print(pd.read_csv('data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv').head())"`
- Source checksum (SHA-256): `4576519754956aa4bf7e4c62476017e40aba31d87950931792e6927b59d4640a`
- README-copy checksum: not applicable

## Featured figure 4: Audience expansion pilot

- README placement: Key findings, section 4
- Display title: Audience-expansion pilot (exploratory)
- Source figure: `figures/rendered/fig18_oon_vs_impressions.png`
- Optimized figure: none (source used directly)
- Paper figure number: 20
- Alt text: Scatter plot of out-of-network share of impressions versus analytics
  impressions on a log scale for 28 pilot posts. Higher-impression posts tend to
  sit higher on the out-of-network axis, a positive but scattered association.
- Caption: Out-of-network share versus impressions (paper Figure 20). Analytics
  impressions on a log scale (n = 28) against the out-of-network impression
  share. Associational, purposefully selected pilot; not causal.
- Source data: private detailed-analytics pilot (Level B, withheld); public
  coverage summary in `data/aggregate/detailed_analytics/DETAILED_ANALYTICS_FIELD_COVERAGE.csv`
- Reproduction: not-public (depends on withheld Level B per-post analytics)
- Source checksum (SHA-256): `d9c1966b8fff85e06deed96bd0c2ccfdce3d7d167401db61ec531a676cd47e8e`
- README-copy checksum: not applicable

## Featured visual 5: Research overview dashboard

Unlike figures 1 through 4, this visual is a chart-driven project summary
generated by the repository itself rather than a manuscript figure. Its full
documentation, chart list, value sources, dimensions, and checksums are in
[RESEARCH_OVERVIEW_DIAGRAM.md](RESEARCH_OVERVIEW_DIAGRAM.md).

- README placement: Research overview, before Key findings
- Display title: FeedTrace research overview
- Source figure: `docs/assets/feedtrace-research-overview.svg`
- Optimized figure: none (vector source used directly)
- Companion rasters: `docs/assets/feedtrace-research-overview.png` (1200 x 1350,
  LinkedIn feed / portrait) and `docs/assets/feedtrace-research-overview-square.png`
  (1080 x 1080, LinkedIn square)
- Generator: `scripts/build_research_overview.py` (deterministic; run
  `pip install -e ".[viz]"` then `python scripts/build_research_overview.py`)
- Charts: Lorenz concentration; heavy-tail CCDF versus frozen lognormal; monthly
  change-point series; exploratory pilot correlations (n = 28; omitted from the
  square version); racial-visibility raw medians plus adjusted estimate with
  UNRESOLVED verdict
- Alt text: FeedTrace research overview dashboard. Five charts summarize 1,174
  creator-owned LinkedIn original posts. A Lorenz curve shows extreme reach
  concentration, with a Gini coefficient of 0.799, the top 1 percent of posts
  holding 63.5 percent of impressions, and the bottom half holding 7.3 percent.
  A log-log distribution plot shows an upper tail far heavier than a fitted
  lognormal predicts, with a median of 53 and a maximum of 67,349 recorded
  impressions. A monthly time series shows an upward descriptive change point in
  May 2026 of about 2.74 times the earlier level. A correlation chart shows
  exploratory audience-expansion associations from a 28-post analytics pilot. A
  raw-median and adjusted-estimate comparison for Direct Black-centered content
  (n = 61) is marked Unresolved, with q = 0.078. Public materials include the
  paper, code, aggregate data, reproduction scripts, and checksums.
- Caption: FeedTrace research overview. The dashboard plots the study's
  strongest distribution findings, the descriptive time shift, the exploratory
  audience-expansion pilot, and the unresolved racial-visibility result directly
  from tracked public data and frozen aggregate tables.
- Source data: `data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`,
  `data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv`,
  `data/aggregate/mixture_models/MIXTURE_DIAGNOSTICS.csv`,
  `data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv`,
  `data/aggregate/multiplicity/R9_MULTIPLICITY_REPORTING_AUDIT.csv`, and frozen
  race and pilot values in the paper sources
- Reproduction: `python scripts/build_research_overview.py` (rebuilds the SVG and
  both PNG files deterministically)
- Source checksum (SHA-256): `3b98b8cb521c61c9a59d0fadf686bc4cee5302238029641f4025395180627cd8`
- Feed PNG checksum (SHA-256): `a324a869fef261373ebc0d221435cce0a7c32de2464b949fefdc077278576616`
- Square PNG checksum (SHA-256): `dc182ad3d853d84da1bd9aae72823792f4052f197c471f8ff3c599c4f821e270`
- README-copy checksum: not applicable
