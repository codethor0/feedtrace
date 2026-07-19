# Contribution and branch workflow

FeedTrace is a solo, open-source research project. It uses a single permanent
branch and short-lived review branches.

## Branch model

- One permanent branch: `main`.
- No permanent `develop`, `development`, `staging`, `production`, `release`,
  `research`, or `gh-pages` branch.
- Short-lived branches for isolated units of work, named by prefix:
  - `docs/<short-description>`
  - `research/<short-description>`
  - `fix/<short-description>`
  - `test/<short-description>`
  - `data/<short-description>`

## Lifecycle of a change

1. Start from an up-to-date `main`.
2. Create a short-lived branch that addresses one related unit of work.
3. Open a pull request.
4. Pass CI (the required `ci` status check).
5. Squash merge into `main`.
6. Delete the branch after merge.

Dependabot branches are temporary and disappear after their pull request is
merged or closed.

## Releases

Use signed version tags for frozen research checkpoints instead of release
branches. Recommended tag pattern:

- `v0.1.0-preprint`
- `v0.2.0`
- `v1.0.0`

Tags are created manually by the owner. See `docs/INITIAL_RELEASE_PLAN.md`.

## History and privacy rules

- Keep a single clean root history.
- Author commits with the GitHub no-reply email.
- Sign commits where signing is required.
- Do not add co-author trailers that reveal private editor or tooling.
- Never include private LinkedIn records, raw exports, full post text, direct
  identifiers, cookies, tokens, authentication material, private review records,
  or editor and prompt artifacts in any commit, issue, or pull request.

## Local checks before opening a pull request

```sh
.venv/bin/pytest
.venv/bin/python scripts/verify_numeric.py --reproduced reproduced
.venv/bin/python scripts/audit_public_tree.py
.venv/bin/python scripts/verify_checksums.py
```

Describe local runs as "local validation passed", not "CI passed". Only a
successful GitHub-hosted `ci` run on `main` counts as green CI.
