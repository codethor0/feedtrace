# Research overview diagram

## Purpose

The research overview is a chart-driven visual dashboard for first-time visitors
to the repository. It is not a replacement for the research report or the
technical supplement. Numbers sit across the top, charts occupy the middle, and
the unresolved conclusion with limitations sits at the bottom.

The viewer should understand within seconds that:

1. Reach is extremely concentrated.
2. The distribution has a heavy upper tail.
3. Reach changed over time.
4. Audience expansion is associated with higher impressions in a limited pilot.
5. The primary racial-visibility result remains unresolved.

## Files

| File | Role |
|---|---|
| `scripts/build_research_overview.py` | Deterministic source that builds every output |
| `docs/assets/feedtrace-research-overview.svg` | Authoritative landscape vector for the README |
| `docs/assets/feedtrace-research-overview.png` | LinkedIn feed (portrait) raster, 1200 x 1350 |
| `docs/assets/feedtrace-research-overview-square.png` | LinkedIn square raster (1080 x 1080) |

The SVG is the authoritative artifact. Both PNG files are produced from the same
build script and the same tracked inputs.

## Generation command

```sh
python3 -m venv .venv
.venv/bin/pip install -e ".[viz]"
.venv/bin/python scripts/build_research_overview.py
```

The `viz` optional dependency (matplotlib) is required only to rebuild the
dashboard. It is not needed for tests, reproduction, or verification, and it is
intentionally excluded from the CI `dev` install. Rendering uses the
matplotlib-bundled DejaVu Sans font, keeps SVG text as real text elements, uses a
fixed SVG hash salt, and strips variable file metadata, so repeated builds on the
same library versions produce identical bytes.

## Output dimensions

| File | Dimensions | Notes |
|---|---|---|
| SVG | 1152 x 1008 pt (16 x 14 in) | Vector landscape, five charts |
| Feed PNG | 1200 x 1350 px | LinkedIn feed (portrait), five charts |
| Square PNG | 1080 x 1080 px | LinkedIn square, four charts (pilot omitted) |

## Chart list and data sources

Every plotted value comes from tracked public aggregate data or frozen model
outputs. No decorative data points are invented.

### Top metrics strip

| Value | Source |
|---|---|
| 1,174 original posts | `data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv` |
| Median impressions: 53 | same table, median of `feed_impressions` |
| Gini coefficient: 0.799 | `data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv` |
| Top 1 percent share: 63.5 percent | same concentration table |
| Maximum impressions: 67,349 | sanitized table maximum |

### Chart 1: Reach Is Extremely Concentrated

- Type: Lorenz curve of all 1,174 original posts
- Displays: equality line, observed curve, Gini 0.799, bottom-50% share 7.3
  percent, top-1% share 63.5 percent
- Sources: sanitized analytic table (curve); concentration table (Gini and top
  share)

### Chart 2: The Upper Tail Is Much Heavier Than a Simple Lognormal Predicts

- Type: complementary cumulative distribution on log-log axes
- Displays: observed CCDF; frozen one-component lognormal fit; median 53;
  empirical 95th percentile about 254; empirical 99th percentile about 1,518;
  maximum 67,349; fitted lognormal 99th percentile about 537
- Sources: sanitized analytic table (empirical curve); frozen one-component fit
  in `data/aggregate/mixture_models/MIXTURE_DIAGNOSTICS.csv` (log mean 4.096,
  log sd 0.941)
- Caption: no single tested continuous distribution fully fits both the body and
  upper tail

### Chart 3: Recorded Reach Changed Over Time

- Type: monthly mean of ln(impressions)
- Displays: monthly series; descriptive May 2026 change point (weekly PELT break
  2026-05-17); pre level 3.76; post level 4.77; post-split factor about 2.74
- Sources: sanitized analytic table (monthly series); break dates in
  `data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv`
- Caption: the shift was upward and descriptive; the analysis does not identify
  its cause
- Note: the 2.74 factor is the published unadjusted descriptive estimand
  exp(4.77 - 3.76), reproduced from the tracked monthly means with May 2026
  onward treated as post-split. It is not labeled an algorithm change.

### Chart 4: Higher Reach Was Associated With Broader Audience Expansion

- Type: Spearman correlation plot (n = 28)
- Displays: out-of-network audience share rho = 0.71 (p = 2.6e-05);
  repeat-exposure ratio rho = -0.62 (p = 4.4e-04). Each coefficient is labeled
  directly with its measure name ("Out-of-network share:" and
  "Repeat-exposure ratio:") so the two estimates remain unambiguous.
- Source: frozen pilot statistics in the paper sources
- Important privacy substitution: the per-post detailed-analytics pilot rows
  (Level B) are withheld from the public repository, so a per-post scatter cannot
  be drawn from tracked data. The dashboard therefore plots the frozen pilot
  correlations rather than inventing observations. The chart is explicitly
  labeled as a purposefully selected exploratory pilot, not representative of
  the full 1,174-post population, and not evidence of a causal ranking
  mechanism.
- Omitted from the square version for space; retained in the landscape SVG and
  the LinkedIn feed PNG.

### Chart 5: The Main Race-Related Result Remains Unresolved

- Type: raw median comparison plus adjusted effect with confidence interval
- Displays: Direct Black-centered content n = 61, raw medians 82 versus 52;
  adjusted estimate -23.7 percent (95 percent CI -37.8 to -6.3); raw p = 0.0098;
  BH-FDR q = 0.078; prominent UNRESOLVED badge
- Sources: frozen race results in the paper sources for the effect and
  confidence interval; `data/aggregate/multiplicity/R9_MULTIPLICITY_REPORTING_AUDIT.csv`
  for the raw p-value and BH-FDR q-value
- Notes shown on the chart: within-month and within-format comparisons did not
  reproduce the reduction; preliminary automated labels, not human validated;
  most source text from possibly truncated previews; Direct Black-centered
  content (n = 61) is distinct from the Composite Black-visibility group
  (n = 83); not proof of suppression and not proof of fairness

## Accessibility decisions

- Light background with high-contrast dark text and lines.
- Chart titles and direct annotations carry the findings; color is never the
  only cue (labels, markers, and line styles are distinct).
- The unresolved section uses an amber badge and the word UNRESOLVED as text.
- SVG text is kept as real text (not converted to paths).
- The README image includes descriptive alt text and a short caption.

## Alt text used in the README

FeedTrace research overview dashboard. Five charts summarize 1,174
creator-owned LinkedIn original posts. A Lorenz curve shows extreme reach
concentration, with a Gini coefficient of 0.799, the top 1 percent of posts
holding 63.5 percent of impressions, and the bottom half holding 7.3 percent. A
log-log distribution plot shows an upper tail far heavier than a fitted
lognormal predicts, with a median of 53 and a maximum of 67,349 recorded
impressions. A monthly time series shows an upward descriptive change point in
May 2026 of about 2.74 times the earlier level. A correlation chart shows
exploratory audience-expansion associations from a 28-post analytics pilot. A
raw-median and adjusted-estimate comparison for Direct Black-centered content
(n = 61) is marked Unresolved, with q = 0.078. Public materials include the
paper, code, aggregate data, reproduction scripts, and checksums.

## Scientific limitations

- The dashboard is a summary. Confidence intervals, model details, sensitivity
  analyses, and full methodology live in the report and technical supplement.
- The racial-visibility result is preliminary and Unresolved. It is a hypothesis
  for human-validated, preregistered follow-up. It is not proof of suppression
  and not proof of fairness.
- Race-related topic labels are preliminary automated labels and are not
  human-validated.
- The audience-expansion chart uses frozen pilot correlations because per-post
  Level B rows are withheld; it is exploratory and not causal.
- The May 2026 time shift is descriptive; the analysis does not identify a
  cause and does not label the shift as an algorithm change.
- All findings are from a single account and are observational. They do not
  establish platform intent, causal suppression, or platform-wide effects.

## Privacy confirmation

The dashboard contains no private data, no direct identifiers, no post text, no
URLs to individual posts, and no personal contact information. It contains no
absolute local paths and no editor, prompt, or tool metadata. The SVG embeds no
private metadata and no external image dependencies. The withheld Level B
per-post pilot rows are not reconstructed.

## SHA-256 checksums

| File | SHA-256 |
|---|---|
| `docs/assets/feedtrace-research-overview.svg` | `3b98b8cb521c61c9a59d0fadf686bc4cee5302238029641f4025395180627cd8` |
| `docs/assets/feedtrace-research-overview.png` | `a324a869fef261373ebc0d221435cce0a7c32de2464b949fefdc077278576616` |
| `docs/assets/feedtrace-research-overview-square.png` | `dc182ad3d853d84da1bd9aae72823792f4052f197c471f8ff3c599c4f821e270` |

The authoritative integrity list remains `release/SHA256SUMS.txt`, and every file
above is also recorded in `release/PUBLIC_MANIFEST.json`.
