# Reproducibility

## Fully reproducible from the public repository

- Sanitized non-race predictive benchmark
- Numerical-tolerance verification
- File-integrity checksums
- Included aggregate tables

## Partially reproducible

- Manuscript calculations that can be verified against aggregate tables
- Static figures whose source aggregates are public but whose private generation code is withheld

## Not publicly reproducible

- Raw collection and browser navigation
- Authenticated analytics collection
- Full post-text analyses
- Direct identifiers
- Race-label candidate review
- Private reviewer records

## Environment

Python 3.12 or later. Runtime dependencies are pinned in `pyproject.toml`. When present, `pylock.toml` provides a standardized lock generated with `python -m pip lock`. Exact byte hashes can vary across platforms even when numbers match; use `scripts/verify_numeric.py` as the version-robust gate (default rtol 1e-6, atol 1e-9).

## Commands

```sh
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python scripts/reproduce_benchmark.py \
  --data data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv \
  --output-dir reproduced
.venv/bin/python scripts/verify_numeric.py --reproduced reproduced
.venv/bin/python scripts/verify_checksums.py
.venv/bin/pytest
```
