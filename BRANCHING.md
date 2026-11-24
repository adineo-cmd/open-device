# Branching and integration

Short version: **do not push to `main`**. Work on a branch and open a PR against
`feat/open-device-site`.

| Branch | Role |
| --- | --- |
| `main` | Published snapshot. The website is built from here and it is the default branch. Do not push directly. |
| `feat/open-device-site` | Integration branch. All PRs target this. `AGENTS.md` Rule 3 requires agent pushes here. |
| `improvements/*`, `doc/*`, `impl/*` | Short-lived topic branches. Delete after merge. |

## Flow

1. `git fetch origin && git switch -c topic/name origin/feat/open-device-site`
2. Make the change; run `python3 tools/run_all_tests.py` and the repository
   checks listed in `CONTRIBUTING.md`.
3. Commit with an issue reference in the message when one exists, e.g.
   `docs: fix stale repo name (#1234)`.
4. Open a PR against `feat/open-device-site`, not `main`. Use the PR template.
5. After review, the integrator merges into `feat/open-device-site`; `main` is
   updated deliberately as a release/snapshot step.

## Agent-specific rules

`AGENTS.md` adds a claim protocol (Rule 2), a search gate (Rules 2a/2b) and
explicit push instructions (Rule 3). Agents must follow it: claim an issue in
their shard, post `SEARCH` and prior-art comments before editing, and report
the final remote SHA in a `DONE` comment. Humans contributing docs, tests or
small fixes may use the quick path in `CONTRIBUTING.md`, but must never take an
issue that already carries an agent `CLAIM`.

## Releases

Research milestones are tagged as releases (for example, a new corpus census).
A release records a state of the evidence, not a binary artifact; no firmware
is ever attached.
