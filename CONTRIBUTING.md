# Contributing

Thank you for your interest in FeedTrace.

## Before you open an issue or pull request

1. Read `README.md`, `docs/RESEARCH_INTEGRITY.md`, and `docs/ETHICS_AND_PRIVACY.md`.
2. Do not upload private LinkedIn data, raw exports, cookies, tokens, or authentication material.
3. Do not request or propose collection code for authenticated scraping.
4. Keep discussion focused on the public package, documentation, and scientific clarity.

## Development setup

```sh
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## Pull requests

- Keep changes small and reviewable.
- Add or update tests for code changes.
- Do not invent DOI, ORCID, or repository URLs.
- Do not introduce emojis or Unicode dash characters in public prose.
- Do not change frozen scientific claims without explicit documentation and a version bump.
