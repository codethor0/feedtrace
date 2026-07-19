# Initial release plan (proposed)

This is a proposal only. The agent does not create tags or releases. The owner
creates the tag and release manually after CI is green on `main` and the
repository is ready.

## Proposed tag

`v0.1.0-preprint` (signed, annotated)

## Release title

FeedTrace v0.1.0-preprint: Reach, ranking, and Black visibility in 1,174 LinkedIn posts

## Release description (draft)

FeedTrace is an independent, single-account observational study of observable
LinkedIn recorded impressions, ranking behavior, audience expansion, impression
concentration, and preliminary racial-visibility differences using creator-owned
data. This preprint checkpoint accompanies the research report and technical
supplement.

- Paper version: preprint checkpoint matching `paper/FeedTrace_Independent_Research_Report.pdf` and `paper/FeedTrace_Technical_Supplement.pdf`.
- Study period: September 6, 2025 through July 18, 2026.
- Dataset coverage: 1,192 inventoried records (1,174 originals, 18 reposts);
  feed-level recorded impressions for all originals; a purposefully selected
  29-post detailed-analytics pilot (members reached and out-of-network share for
  28); 29 verified full-text originals.
- Preliminary-label status: race-related topic labels are produced by a
  deterministic keyword taxonomy and are preliminary.
- Manual-review status: no race-review candidates were human-approved at the
  frozen checkpoint. The manual race review is not complete.

## Main findings

- Recorded impressions are extremely concentrated: median 53, top 1 percent
  holds 63.5 percent, bottom half holds 7.3 percent, Gini 0.799.
- No single tested continuous distribution fits both the body and the extreme
  upper tail.
- A descriptive upward change point appears around mid-May 2026; cause is not
  identified.
- An exploratory pilot associates higher impressions with higher out-of-network
  share (n = 28).
- The account-level racial-visibility signal for Direct Black-centered content
  (n = 61) is Unresolved.

## Important limitations

- Single-account observational design; not platform-wide.
- No confirmed structured moderation records.
- Preliminary automated race labels; most source text truncated.
- The paper is not fully reproducible from public row-level inputs.

## Reproduction commands

```sh
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python scripts/reproduce_benchmark.py \
  --data data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv \
  --output-dir reproduced
.venv/bin/python scripts/verify_numeric.py --reproduced reproduced
.venv/bin/pytest
.venv/bin/python scripts/audit_public_tree.py
.venv/bin/python scripts/verify_checksums.py
```

## Principal checksums

Full checksums are in `release/SHA256SUMS.txt`. Verify with
`scripts/verify_checksums.py`. Featured figure checksums are recorded in
`docs/README_VISUALS_MANIFEST.md` and `figures/README.md`.

## Included assets

- Source tree at the tagged commit.
- Research report and technical supplement PDFs under `paper/`.
- Sanitized non-race analytic table and public aggregate tables.
- Rendered manuscript figures.

## Public data boundary

The release contains only sanitized numeric and structural fields plus aggregate
tables. Raw exports, full post text, direct identifiers, viewer identities,
cookies, tokens, authentication material, and Level B detailed-analytics inputs
are withheld.

## License summary

- Code: MIT.
- Paper, documentation, figures, and released aggregate data: CC BY 4.0.
