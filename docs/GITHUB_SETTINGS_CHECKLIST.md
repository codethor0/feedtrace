# GitHub Settings Checklist

Owner-only checklist. The agent does not change repository settings, and does not
commit, push, merge, tag, release, or change repository visibility.

## Before the first push

- [ ] Confirm repository is private with clean history
- [ ] Enable two-factor authentication on the owner account
- [ ] Confirm the correct Git author email (the GitHub no-reply address)
- [ ] Review all local files
- [ ] Run tests, secret scans, privacy scans, and the public-boundary audit
- [ ] Review the complete diff
- [ ] Confirm CODEOWNERS assigns the owner handle

## While private

- [ ] Enable dependency graph
- [ ] Enable Dependabot alerts and security updates
- [ ] Set Actions default workflow permissions to read-only
- [ ] Prevent Actions from creating or approving pull requests
- [ ] Keep GitHub Pages disabled
- [ ] Keep Discussions disabled unless moderated

## Public-launch gates (all must pass before making public)

- [ ] GitHub billing is corrected and Actions can run
- [ ] GitHub-hosted CI (`ci` job) is green on `main`
- [ ] Every open Dependabot pull request is reviewed, merged, deferred, or closed with a reason
- [ ] Only `main` remains as a persistent branch
- [ ] No stale topic branches remain
- [ ] No stale workflow artifacts remain
- [ ] No sensitive workflow logs remain
- [ ] Actions permissions remain read-only
- [ ] All commit identities use the no-reply address
- [ ] Every required commit signature is verified
- [ ] No co-author trailers reveal private editor or assistant tooling
- [ ] README renders correctly on desktop and mobile widths
- [ ] All featured visuals render
- [ ] Paper and supplement links work
- [ ] Public data files match their dictionaries
- [ ] Reproduction steps pass in a clean environment
- [ ] Public checksums pass
- [ ] Community files are complete
- [ ] Citation metadata is valid
- [ ] License mapping is valid
- [ ] Level B data is absent
- [ ] Secret scan is clean
- [ ] Privacy scan is clean
- [ ] Prompt-artifact scan is clean
- [ ] Actions history is reviewed before the visibility change
- [ ] Public-visibility consequences are understood (Actions history and logs become public)

## At the public transition (manual owner actions)

1. [ ] Make the repository public
2. [ ] Recheck the `main` ruleset
3. [ ] Verify secret scanning is enabled
4. [ ] Enable push protection where available
5. [ ] Enable private vulnerability reporting
6. [ ] Review the public community profile
7. [ ] Verify Actions permissions remain read-only
8. [ ] Rerun CI on the public repository
9. [ ] Confirm the README CI badge is green (add the badge only after this)
10. [ ] Confirm no repository setting was disabled or changed unexpectedly

## Main-branch ruleset

Configure the `main` ruleset only after CI succeeds. See
`docs/GITHUB_MAIN_RULESET_RECOMMENDATION.md`. Configure squash merging and
automatic deletion of merged branches.
