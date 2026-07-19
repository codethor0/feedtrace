# FeedTrace

Independent research. Not affiliated with, endorsed by, or conducted on behalf of LinkedIn or any employer.

**Status.** This repository publishes a preliminary single-account audit. Race-related topic labels were produced by a deterministic keyword taxonomy and remain preliminary. The main racial-visibility signal is **Unresolved**. The repository does not prove or disprove suppression.

## Summary

FeedTrace is an ongoing longitudinal research project that examines observable LinkedIn recorded impressions, ranking-relevant outputs, audience expansion, impression concentration, and racial-visibility patterns using creator-owned data. The current release checkpoint analyzes 1,174 original posts from one account between September 6, 2025, and July 18, 2026.

## Research question

What do creator-owned recorded impressions and related analytics reveal about concentration, audience expansion, Feed mechanism boundaries, and account-level racial-visibility patterns, under the limits of an external observational audit?

## Current study scope

- 1,192 inventoried records; 1,174 creator-owned originals; 18 reposts
- Feed-level recorded impressions for all 1,174 originals
- Detailed creator analytics for a purposefully selected 29-post pilot (members reached and out-of-network share available for 28)
- 29 verified full-text originals; 1,145 records classified from possibly truncated previews
- 459 race-review candidates; 0 human-approved at the frozen checkpoint
- 0 confirmed structured moderation records
- Direct Black-centered preliminary category n = 61

## Key findings (with uncertainty)

1. **Concentration.** Recorded impressions are extremely concentrated (Gini 0.799). The top 1 percent of posts account for 63.5 percent of impressions; the bottom half account for 7.3 percent.
2. **Distribution structure.** No single continuous family fits body and upper tail. A two-component lognormal mixture is a useful descriptive summary of body and high-impression regimes; mixture components are not identified production stages.
3. **Audience expansion (pilot).** In the 29-post pilot, higher impressions associate with higher out-of-network share and lower repeat exposure. These associations are exploratory and non-causal.
4. **Racial-visibility signal (Unresolved).** Direct Black-centered posts (n = 61) have higher unadjusted median recorded impressions (82 versus 52), while adjusted models estimate approximately 24 percent fewer conditional recorded impressions (95 percent CI -37.8 to -6.3; raw p = 0.0098; BH q = 0.078; Holm and Bonferroni adjusted p = 0.078). Stratified checks do not reproduce the reduction. The signal remains Unresolved.

## What this research does not establish

- Platform-wide effects
- Causal topic penalties
- Platform intent
- Fairness from nonsignificance
- Suppression as proven fact
- Clearance as proven fact

## Repository contents

| Path | Contents |
|---|---|
| `paper/` | Public research report and technical supplement PDFs, plus Markdown sources |
| `src/feedtrace/` | Sanitized predictive benchmark, validation, checksums, public-boundary audit |
| `scripts/` | Reproduction and verification entry points |
| `data/sanitized/` | Text-free, identifier-free non-race analytic table |
| `data/aggregate/` | Aggregate result tables used by the paper |
| `figures/rendered/` | Final manuscript figures |
| `results/model_outputs/` | Frozen predictive baselines |
| `docs/` | Integrity, methodology, privacy, reproducibility, and policy documentation |
| `release/` | Preliminary status, privacy notes, publication checklist, checksums |
| `tests/` | Schema, numeric, boundary, and artifact tests |

## Quick start

```sh
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python scripts/reproduce_benchmark.py \
  --data data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv \
  --output-dir reproduced
.venv/bin/python scripts/verify_numeric.py --reproduced reproduced
.venv/bin/pytest
.venv/bin/python scripts/audit_public_tree.py
```

If a `pylock.toml` is present, prefer installing from that lock file for a deterministic environment.

## Reproducibility coverage

| Coverage | What is included |
|---|---|
| Fully reproducible | Sanitized non-race predictive benchmark; numerical-tolerance verification; file-integrity checksums; public aggregate tables |
| Partially reproducible | Manuscript calculations that can be checked against aggregate tables but not fully rerun from withheld row-level inputs; static figures |
| Not publicly reproducible | Raw LinkedIn collection; browser navigation; authenticated analytics collection; full post text analysis; direct identifiers; race-label candidate review; private reviewer records |

The repository does not claim that the entire paper is independently reproducible from the public package.

## Data availability and privacy

Public row-level data contain only sanitized numeric and structural fields needed for the predictive benchmark. Post text, URLs, activity identifiers, viewer identities, race-label candidate records, raw exports, cookies, tokens, and authentication material are withheld. See `docs/DATA_AVAILABILITY.md`, `docs/ETHICS_AND_PRIVACY.md`, and `data/DATA_DICTIONARY.md`.

## Citation

See [CITATION.cff](CITATION.cff). Preferred citation:

Thor, Isaac (2026). *FeedTrace: Reach, Ranking, and Black Visibility in 1,174 LinkedIn Posts*. Independent research report.

## License

- Code under `src/`, `scripts/`, and `tests/`: MIT
- Paper, documentation, figures, and released data: CC BY 4.0

See [LICENSE.md](LICENSE.md).

## Contributing and security

Contribution guidance is in [CONTRIBUTING.md](CONTRIBUTING.md). Never attach private LinkedIn data, tokens, cookies, or authentication material to issues or pull requests. Security reports should use GitHub private vulnerability reporting once enabled; see [SECURITY.md](SECURITY.md).

## Roadmap

See [ROADMAP.md](ROADMAP.md) and `docs/RESEARCH_CYCLE.md`. Near-term priorities include human validation of race-related labels as a separate result set, repeated fixed-age snapshots, broader analytics coverage, and multi-account designs.
