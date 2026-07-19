# GitHub Settings Checklist

Owner-only checklist. The agent does not change repository settings.

## Before the first push

- [ ] Confirm repository is private and empty or has clean history
- [ ] Enable two-factor authentication on the owner account
- [ ] Confirm the correct Git author email
- [ ] Review all local files
- [ ] Run tests, secret scans, privacy scans, and the public-boundary audit
- [ ] Review the complete first-commit diff
- [ ] Replace the comment-only CODEOWNERS placeholder with the owner username

## While private

- [ ] Enable dependency graph
- [ ] Enable Dependabot alerts and security updates
- [ ] Enable secret scanning and push protection where available
- [ ] Set Actions default workflow permissions to read-only
- [ ] Prevent Actions from creating or approving pull requests
- [ ] Keep GitHub Pages disabled
- [ ] Keep Discussions disabled unless moderated

## Before making public

- [ ] Review every commit, branch, tag, and Actions history
- [ ] Delete obsolete workflow runs and artifacts
- [ ] Rerun secret, privacy, and identifier scans
- [ ] Confirm licenses, CITATION.cff, security policy, templates, README language
- [ ] Confirm preliminary-status language and non-affiliation disclaimer
- [ ] Confirm no prompt artifacts, emojis, absolute local paths, or private ZIP files

## Immediately after making public

- [ ] Recheck rulesets, push protection, secret scanning, and Actions permissions
- [ ] Enable private vulnerability reporting
- [ ] Configure main-branch ruleset (PR required, CI required, no force push, no deletion)
- [ ] Configure squash merging and automatic deletion of merged branches
- [ ] Review the public community profile
