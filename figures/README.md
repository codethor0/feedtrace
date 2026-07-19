# Figure inventory

This directory holds the rendered manuscript figures under `rendered/` and figure
source-data maps under `source_data/`.

Notes that apply to every figure:

- Figure plotting code is not part of the public package. The rendered PNG files
  are tracked; the private generation scripts are withheld with the raw data.
- Study window: September 6, 2025 through July 18, 2026, unless a narrower sample
  is stated below.
- Reproducibility levels: "partial" means the underlying values can be checked
  against public aggregate tables or the sanitized impressions table, but the
  figure cannot be regenerated end to end from public row-level inputs.
  "not-public" means the figure depends on withheld inputs (the private
  detailed-analytics pilot or the private race-label review).
- Paper figure numbers follow `source_data/R9_FIGURE_RENUMBERING_MAP.csv`.
- Do not use screenshots of PDF pages, and do not recreate any chart by eye.

## Featured in the root README

| File | Paper Fig | Title | Sample | Reproducibility |
|---|---|---|---|---|
| `rendered/fig01_lorenz_curve.png` | 4 | Lorenz curve of recorded impressions | n = 1,174 originals | partial |
| `rendered/fig05_qq_lognormal.png` | 6 | Lognormal Q-Q plot with heavy-tail departure | n = 1,174 originals | partial |
| `rendered/fig13_changepoint_series.png` | 15 | Change-point series (weekly and monthly) | n = 1,174 originals | partial |
| `rendered/fig18_oon_vs_impressions.png` | 20 | Out-of-network share versus impressions | n = 28 pilot posts | not-public |

## Full inventory

Each entry lists: paper figure, title, research question, measurement, sample,
source data, reproducibility, key limitation, and SHA-256.

### fig03_distribution_linear.png

- Paper figure: 1
- Title: Recorded-impression distribution (linear scale)
- Research question: What is the shape of the impression distribution?
- Measurement: Feed-level recorded impressions per original post
- Sample: n = 1,174 originals
- Source data: `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: Linear scale compresses the body; see the log-scale companion
- SHA-256: `5fd4046d1d9c4d21a91ae3702387c00bad8987b957dc57ed940e28c9b08d7db2`

### fig04_distribution_log.png

- Paper figure: 2
- Title: Recorded-impression distribution (log scale)
- Research question: How heavy is the right tail on a log scale?
- Measurement: Feed-level recorded impressions per original post
- Sample: n = 1,174 originals
- Source data: `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: Descriptive only; no distributional claim by itself
- SHA-256: `c77fdc6f6c2c24ca9c9252e11636b3189c3077588b69e0c19e8b9adad70b5ce9`

### fig06_quantile_bootstrap.png

- Paper figure: 3
- Title: Bootstrap confidence intervals for key quantiles
- Research question: How stable are the sample quantiles?
- Measurement: Bootstrap intervals for selected impression quantiles
- Sample: n = 1,174 originals
- Source data: `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: Intervals reflect sampling variation for one account only
- SHA-256: `a1d3d7d7cd24d128a63437e6fa23702b57b8037032eb3bbbb480d439bce42706`

### fig01_lorenz_curve.png

- Paper figure: 4
- Title: Lorenz curve of recorded impressions
- Research question: How concentrated are recorded impressions across posts?
- Measurement: Cumulative share of impressions versus cumulative share of posts
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv`,
  `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: Concentration is descriptive and account-specific
- SHA-256: `35819757e07dfdf51ae7353f1d9907f22483ee2e504d2b24481bf2f033d77915`

### fig02_top_share_curve.png

- Paper figure: 5
- Title: Top-share concentration curve
- Research question: What share of impressions do the top posts capture?
- Measurement: Cumulative impression share held by the top k percent of posts
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv`
- Reproducibility: partial
- Limitation: Sensitive to a few extreme posts
- SHA-256: `110785096d095a827864b6ea71fb8b118f9e266cee1f18430379362c598815f8`

### fig05_qq_lognormal.png

- Paper figure: 6
- Title: Lognormal Q-Q plot with heavy-tail departure
- Research question: Does a lognormal describe the impression distribution?
- Measurement: Empirical log impressions versus theoretical lognormal quantiles
- Sample: n = 1,174 originals (upper 5 percent highlighted)
- Source data: `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: The body tracks lognormal, but the upper tail departs upward
- SHA-256: `6de0ad799446d9c97943a18776d6410d68a6b5fa391eeca4dcc8afa1ec291094`

### fig07_distribution_comparison.png

- Paper figure: 7
- Title: Candidate distribution comparison by corrected AIC
- Research question: Which continuous family fits best by information criterion?
- Measurement: Delta corrected AIC relative to the best-ranked family
- Sample: n = 1,174 originals
- Source data: `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: Lower AIC is a relative ranking, not proof of tail fit
- SHA-256: `e5474b73579f0930b8b91b64d190e8320426b610027af063d4fcb918fd4f0d9c`

### fig08_mixture_posterior.png

- Paper figure: 8
- Title: Two-component lognormal mixture posterior
- Research question: Can a two-regime mixture summarize the distribution?
- Measurement: Posterior mixture components over log impressions
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/mixture_models/MIXTURE_DIAGNOSTICS.csv`
- Reproducibility: partial
- Limitation: Components are descriptive, not identified production stages
- SHA-256: `bd61f305ec565162f2a8152e3dee2ea163514e3ba814e30323c2f4e2da3a18a6`

### fig09_regime_by_format.png

- Paper figure: 9
- Title: High-impression regime membership by post format
- Research question: Does high-regime membership vary by post format?
- Measurement: Share of posts in the high component by format
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/mixture_models/MIXTURE_DIAGNOSTICS.csv`
- Reproducibility: partial
- Limitation: Format categories are unbalanced
- SHA-256: `3ebf4a51f742a396fa82e0d901374558d8e3e487e36ee3c697f2a28cc8ea4125`

### fig10_regime_by_month.png

- Paper figure: 10
- Title: High-impression regime membership by month
- Research question: Does high-regime membership vary over time?
- Measurement: Share of posts in the high component by month
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv`
- Reproducibility: partial
- Limitation: Monthly counts vary; descriptive only
- SHA-256: `c89d181762e7fa547e4aa09d0b7ff2cd2b9e75160dce26d7d5483748a36e6048`

### fig23_mechanism_dag.png

- Paper figure: 11
- Title: Mechanism directed acyclic graph
- Research question: What causal structure is assumed for interpretation?
- Measurement: Conceptual DAG of assumed relationships
- Sample: Not applicable (conceptual diagram)
- Source data: None (diagram)
- Reproducibility: partial
- Limitation: Encodes assumptions, not verified platform mechanics
- SHA-256: `f94399c2410527a7f28b5e7831d43098e213d3cc1ef5d12b0a56161ea50575a7`

### fig11_age_vs_impressions.png

- Paper figure: 12
- Title: Post age versus recorded impressions
- Research question: How do impressions relate to observation age?
- Measurement: Impressions against post age at observation
- Sample: n = 1,174 originals
- Source data: `../data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`
- Reproducibility: partial
- Limitation: Cross-sectional ages, not a fixed-age snapshot
- SHA-256: `468dc79bb8c1b09e55482e80927184fe86c27a72aaf36b5fdc012312005e4661`

### fig12_sequence_semantic_effects.png

- Paper figure: 13
- Title: Sequence and semantic effects on impressions
- Research question: Do posting sequence and content features associate with reach?
- Measurement: Estimated effects for sequence and text-derived features
- Sample: n = 1,174 originals (text features from verified subset)
- Source data: Derived from withheld post-text features; not publicly released
- Reproducibility: not-public
- Limitation: Text-derived features rely on withheld full text
- SHA-256: `948c3f73d15c83175f188002147d6af2432a56aee10f4a7cbc70639f120ba7e7`

### fig20_alias_map.png

- Paper figure: 14
- Title: Variable alias map
- Research question: How do public variable names map to paper terms?
- Measurement: Reference crosswalk of variable aliases
- Sample: Not applicable (reference diagram)
- Source data: None (diagram)
- Reproducibility: partial
- Limitation: Documentation aid, not an analytic result
- SHA-256: `5c56cf9f220ad70b385b8f072bd759149ddf0aed4273a415859cbb6dda953529`

### fig13_changepoint_series.png

- Paper figure: 15
- Title: Change-point series (weekly and monthly)
- Research question: Is there a shift in reach over time?
- Measurement: Weekly median and monthly mean log impressions with detected breaks
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv`
- Reproducibility: partial
- Limitation: Break detection is descriptive; it does not identify a cause
- SHA-256: `4576519754956aa4bf7e4c62476017e40aba31d87950931792e6927b59d4640a`

### fig14_public_chronology.png

- Paper figure: 16
- Title: Public collection chronology
- Research question: When were observations collected?
- Measurement: Timeline of public data-collection events
- Sample: Collection metadata
- Source data: Collection metadata (dates only)
- Reproducibility: partial
- Limitation: Records collection timing, not platform behavior
- SHA-256: `2bd62d58f7f81c5b0d2eaf74d0cd38495cd94aca1481f4b0bb20c6a0abc5c986`

### fig15_feed_vs_analytics.png

- Paper figure: 17
- Title: Feed-level versus analytics impressions agreement
- Research question: Do feed-level and analytics impressions agree?
- Measurement: Feed-level impressions against analytics impressions
- Sample: n = 29 pilot posts
- Source data: `../data/aggregate/detailed_analytics/FEED_ANALYTICS_AGREEMENT.csv`
  (raw per-post analytics are withheld, Level B)
- Reproducibility: not-public
- Limitation: Small purposefully selected pilot
- SHA-256: `bf49285b5874c9af5e64b18baca2e49a5772a20842ed8b832e22656801900702`

### fig16_impressions_vs_reached.png

- Paper figure: 18
- Title: Impressions versus members reached
- Research question: How do impressions relate to unique members reached?
- Measurement: Impressions against members reached
- Sample: n = 28 pilot posts
- Source data: Private detailed-analytics pilot (Level B, withheld)
- Reproducibility: not-public
- Limitation: Repeat exposure inflates impressions above members reached
- SHA-256: `b194ab85f3de02998db2073df8d17530f7a1467561d6a7fe98b470f8fe42e22d`

### fig17_repeat_exposure.png

- Paper figure: 19
- Title: Repeat-exposure ratio versus impressions
- Research question: Does repeat exposure change with reach?
- Measurement: Impressions-to-members-reached ratio against impressions
- Sample: n = 28 pilot posts
- Source data: Private detailed-analytics pilot (Level B, withheld)
- Reproducibility: not-public
- Limitation: Exploratory; small non-representative pilot
- SHA-256: `e8d9d3e21dd0badf5c91a44a9d2dde725e5b801c7bd0029ddfa35bf87a796f37`

### fig18_oon_vs_impressions.png

- Paper figure: 20
- Title: Out-of-network share versus impressions
- Research question: Do higher-reach posts expand beyond the follower network?
- Measurement: Out-of-network impression share against analytics impressions
- Sample: n = 28 pilot posts
- Source data: Private detailed-analytics pilot (Level B, withheld)
- Reproducibility: not-public
- Limitation: Associational, purposefully selected, not causal
- SHA-256: `d9c1966b8fff85e06deed96bd0c2ccfdce3d7d167401db61ec531a676cd47e8e`

### fig19_influence.png

- Paper figure: 21
- Title: Regression influence diagnostics
- Research question: Do individual posts unduly influence the model?
- Measurement: Influence and leverage diagnostics for the account-level model
- Sample: n = 1,174 originals
- Source data: `../data/aggregate/residual_dependence/RESIDUAL_DEPENDENCE.csv`
- Reproducibility: partial
- Limitation: Diagnostic aid for the fitted model
- SHA-256: `de4b2f529daaf6b4d1be27fac8f4d46c10a9a5088d67f3f3af6b6d490fcaa92d`

### fig21_frozen_race_models.png

- Paper figure: 22
- Title: Frozen race models (preliminary labels)
- Research question: Do adjusted models show a racial-visibility difference?
- Measurement: Adjusted estimates across frozen model specifications
- Sample: Direct Black-centered content n = 61
- Source data: `../data/aggregate/multiplicity/R9_MULTIPLICITY_REPORTING_AUDIT.csv`
  (label review is withheld)
- Reproducibility: not-public
- Limitation: Preliminary automated labels; result is Unresolved; not human-validated
- SHA-256: `ea39eb99c122bb28c99af42a03981717e1325779bac65dfe69b078301ea756e9`

### fig22_claimB_uncertainty.png

- Paper figure: 23
- Title: Claim B uncertainty (preliminary labels)
- Research question: How uncertain is the adjusted racial-visibility estimate?
- Measurement: Estimate with uncertainty interval and multiplicity context
- Sample: Direct Black-centered content n = 61
- Source data: `../data/aggregate/multiplicity/R9_MULTIPLICITY_REPORTING_AUDIT.csv`
- Reproducibility: not-public
- Limitation: Did not survive multiple-testing correction; Unresolved
- SHA-256: `f88ec178b5bf9ecf2d802d29a074de39c4a4c82db7b6be2edd0642b1615a735b`

### cover_system_diagram.png

- Paper figure: cover
- Title: System and data-flow cover diagram
- Research question: How does the collection and analysis pipeline fit together?
- Measurement: Conceptual overview diagram
- Sample: Not applicable (diagram)
- Source data: None (diagram)
- Reproducibility: partial
- Limitation: Illustrative overview, not an analytic result
- SHA-256: `622766495118b8a294cb3376cd437b532ce8a6a39a9109bb65280e977af69cf6`
