# Data Dictionary

## `data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`

Row-level, text-free, race-free analytic table used by the corrected R9 predictive benchmark. One row per snapshotted post. No post text, identifiers, race or topic labels, or viewer data are present.

| Column | Type | Definition |
|---|---|---|
| `created_at` | ISO 8601 UTC timestamp | Capture time of the post impression snapshot. Used for chronological ordering and the train/calibration/test split. |
| `is_original_post` | boolean | True for original posts authored by the account. Reposts are excluded from modeling. |
| `feed_impressions` | integer | Recorded feed impressions for the post. Primary outcome (analyzed on the natural-log scale for strictly positive counts). |
| `feed_impressions_post_age_hours` | float | Age of the post in hours at snapshot time. |
| `word_count` | integer | Number of words in the post text. The text itself is withheld. |
| `hashtag_count` | integer | Number of hashtags in the post. |
| `has_image` | boolean | Post contains an image. |
| `has_video` | boolean | Post contains a video. |
| `has_document` | boolean | Post contains a document or carousel. Text is the reference format when all media flags are false. |

Notes:

- Inventory: 1,192 rows = 1,174 originals + 18 reposts.
- One original without a parseable timestamp is excluded from the date-anchored benchmark (1,173 modeled rows).
- The benchmark derives `log_age_h` and `posts_prev_24h` internally from these fields.
- No `members_reached`, out-of-network, or race fields are included; those analyses rely on privacy-restricted inputs reported in the paper only.

## Aggregate tables

Aggregate CSVs and JSON under `data/aggregate/` contain frozen summary statistics used by the manuscript. They do not contain full post text or direct identifiers.
