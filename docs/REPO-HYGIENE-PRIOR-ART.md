# Prior-art record — repository hygiene work (2026-11-24)

Per `AGENTS.md` Rule 0, the searches below were run before the hygiene changes
were finalised. This is **not a research finding** and makes no uniqueness
claim: contribution guidelines, licenses and CI are established engineering
conventions. The record exists so the provenance of the decision is visible.

## Repo search (whole checkout)

Commands (abbreviated results):

```
git log --all --oneline -- LICENSE CONTRIBUTING.md .github/workflows/tests.yml
  -> no commit adding a license, contributing guide or test workflow
grep -rn "CONTRIBUTING\|CODE_OF_CONDUCT\|LICENSE" . --include='*.md' --include='*.yml'
  -> only README/SCOPE boundary prose; no governance files
find .github -type f
  -> .github/workflows/pages.yml only
docs/REPO-STATE-MAP.md
  -> no repo-hygiene family; the gap was identified in the audit, not an issue
```

Verdict: **NEW within this repository** (no committed artifact), **DELTA against
established practice** (we adopt documented conventions rather than invent
them).

## Web / project docs

| Query / source | Date | Result |
| --- | --- | --- |
| searxng: `GitHub repository LICENSE CONTRIBUTING CODE_OF_CONDUCT SECURITY CI workflow best practices open source research project` | 2026-11-24 | No results returned by the search backend |
| searxng: `open source firmware reverse engineering research repository license clean room documentation` | 2026-11-24 | No results returned |
| searxng: `Astro site npm run check @astrojs/check typescript @types/node CI github actions` | 2026-11-24 | No results returned |
| GitHub Docs, "Setting guidelines for repository contributors" (<https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors>) | 2026-11-24 | Recommends `CONTRIBUTING.md`, issue/PR templates and a code of conduct; confirms the chosen layout |
| GitHub Docs, "Adding a license to a repository" (linked from the same page) | 2026-11-24 | Confirms a root `LICENSE` is the discoverable location |
| GitHub Docs workflow configuration URL | 2026-11-24 | 404; workflow syntax taken from the existing `pages.yml` in-repo instead |

## What is actually new here

- The **two-part license split** (GPL-2.0-only for code derived from public GPL
  headers, CC BY-SA 4.0 for findings and data) is specific to this corpus.
- `tools/run_all_tests.py` unifies the three test conventions that coexist in
  `implementations/` (unittest, the `historic/fp2` `check()` harness, and C
  self-tests) plus `site/tests/`.
- `tools/check_stale_names.py`, `tools/check_catalogs.py` and
  `tools/check_state_map.py` automate invariants this repo already stated in
  prose (`RENAME.md`, `docs/issue-catalog/SCHEMA.md`, `REPO-STATE-MAP.md`).

## Adversarial audit note

No novelty claim is made for the conventions themselves, so there is no claim
to break. The falsifiable statements in this change set are the measured ones
(e.g. "770 committed files", "19+ tested components", "2,836 catalog issues"),
each of which is printed by a committed check script rather than asserted here.

## Protocol note (owner-directed work)

This change set was requested directly by the repository owner in conversation,
not through a GitHub work package. No `CLAIM`/`SEARCH` issue comments were
posted because no issue exists for it. Before merge, the owner may open an
issue, post the claim/search record there, and reference it in the PR; the
changes themselves are local and uncommitted to the integration branch at the
time of writing.
