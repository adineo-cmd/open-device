## What changed

One paragraph. Link the issue if there is one (`Closes #1234`).

## Verification

Commands run and their result. Include the full list if the change touches code.

- [ ] `python3 tools/run_all_tests.py`
- [ ] `python3 tools/check_stale_names.py`
- [ ] `python3 tools/check_catalogs.py`
- [ ] `python3 tools/check_state_map.py`
- [ ] `npm ci && npm run check` (website changes only)

## Research rules (delete if not a research change)

- [ ] Prior-art queries and access dates recorded in the finding
- [ ] Claim is falsifiable; evidence and reproduction script included
- [ ] Negative results recorded
- [ ] Corrections logged in `research/CORRECTIONS.md`

## Boundaries

- [ ] No proprietary binary, decompiled output or device-private data committed
- [ ] No CVE / exploit work (`SCOPE.md`)
- [ ] Synthetic fixtures regenerate with `make_fixture.py`
- [ ] Clean-room statement present in new implementation code

## Before/after improvements (AGENTS.md Rule 1)

List any stale number, broken link or dangling reference fixed in this PR:

- before → after
