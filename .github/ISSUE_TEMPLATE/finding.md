---
name: New research finding
about: Propose a documented, evidence-backed finding
title: 'research: '
labels: area:docs, type:re
---

## Claim

One sentence. State what the firmware actually is, not what it might be.

## Prior art (RULE 0)

Record exact queries and access dates. If prior art already covers this, say so
and propose closing as a duplicate.

- GitHub code search (excluding `adineo-cmd/*`):
- Web / XDA / LWN / HN / Reddit:
- arXiv / Scholar:
- Kernel + linux-firmware trees:

Verdict: `NEW` | `DELTA <what is new>` | `PRIOR-ART <urls>`

## Evidence

- Device / SoC / partition:
- Command or script used (must be reproducible):
- Measured values (addresses, hashes, versions, constants):
- Falsification chain — what would disprove this?:

## Deliverable path

`research/<track>/<name>.md`, written with `research/_template/finding.md`.

## Scope check

- [ ] No proprietary bytes, decompiled output or device-private data
- [ ] No CVE / exploit content (`SCOPE.md`)
- [ ] Negative results recorded too
