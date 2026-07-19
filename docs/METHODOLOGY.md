# Methodology

## Design

FeedTrace is an outcome-based black-box audit of one creator account. The analysis uses creator-owned recorded impressions and, for a purposefully selected pilot, detailed creator analytics. Internals such as candidate pools, ranking scores, and eligibility decisions are not observed.

## Sample construction

1. Keep `is_original_post` records for inference.
2. Keep parseable timestamps for chronological analyses.
3. Keep strictly positive `feed_impressions` for the predictive benchmark.

Inventory: 1,192 records = 1,174 originals + 18 reposts. Cross-sectional analyses use n = 1,174. The predictive benchmark uses 1,173 posts after excluding the one original without a parseable timestamp.

## Predictive benchmark

The public package reproduces a chronological three-way split:

- training: first 60 percent (n = 703)
- calibration: next 20 percent (n = 235)
- test: final 20 percent (n = 235)

Models fit only on training data. Absolute residual nonconformity scores are computed only on calibration data. Coverage and width are evaluated only on the untouched test set. The finite-sample conformal order statistic uses ceil((n_calibration + 1) * (1 - alpha)) with alpha = 0.10. Seed = 20260719.

## Race-related labels

Racial-visibility labels were produced by a transparent, deterministic keyword taxonomy. The Direct Black-centered category has n = 61. The frozen race results remain Unresolved and are not re-estimated by the public package.

## Measurement definitions

- Recorded impressions: feed-level display count; primary outcome
- Members reached: unique-member estimate from detailed analytics (pilot only)
- Out-of-network share: analytics-reported share outside the follower network
- Repeat-exposure ratio: analytics impressions divided by members reached
