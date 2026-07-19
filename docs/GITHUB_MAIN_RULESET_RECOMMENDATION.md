# Recommended ruleset for `main`

This is a recommendation only. The agent does not apply rulesets. The owner
configures this manually after the prerequisites below are met.

## Prerequisites before applying

1. GitHub billing is corrected so Actions can run.
2. The final CI workflow completes successfully on `main`.
3. The exact required status-check name is confirmed as `ci`.
4. The README visuals pull request is merged.

## Recommended rules (target: default branch `main`)

- Require a pull request before merging.
- Require the `ci` status check to pass.
- Require conversation resolution before merging.
- Require linear history.
- Block force pushes.
- Block branch deletion.
- Require signed commits.
- Allow squash merging (and prefer it).

## Solo-maintainer notes

- Do not require an outside approval, because there is a single maintainer.
- Do not grant routine bypass permission to anyone.
- Protect workflow files and `CODEOWNERS` changes behind owner review.

## After configuring

- Recheck the ruleset immediately after any repository visibility change, because
  visibility changes can affect protections.
- Confirm the required status-check name still matches the job name `ci`.
- Do not rename the `ci` job after the ruleset is configured, or the required
  check will not match.
