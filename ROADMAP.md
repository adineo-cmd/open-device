# Roadmap and coverage

This file exists to keep the headline scope honest. The project's long-term
scope is every device class, but **current coverage is phone-concentrated**.
Nothing here is a promise of a dates-certain delivery; it is a statement of
where the gaps are and what "done" means.

## Current state (from `README.md` and `docs/REPO-STATE-MAP.md`)

| Measure | Value |
| --- | --- |
| Per-file blob rows committed | 33,917 |
| Devices with per-file rows | 123 |
| Devices inventoried | 245 |
| Devices with no per-file rows | 122 |
| Vendor fronts | Qualcomm (deep), MediaTek (starting) |
| SoCs with direct coverage | SDM845, SM6375, SM8250, QCM6490/FP6, selected MediaTek |
| Clean-room components with self-tests | 19+ |

The 122 uncovered devices are mainly tablets, TV boxes, single-board computers
and developer boards. They are **inventoried, not catalogued per file**.

## Near-term goals

1. **Close the undecoded high-impact families.** Highest priority is the
   `qdsp6sw.mbn` modem payload (issue #606, ~84 MB, ~48% of SM8250 modem
   volume) and the CDSP family, which currently has no spec or parser.
2. **Resolve signature/attestation semantics.** Marked `[OPEN]` across almost
   every blob family; this blocks any claim of a complete boot-chain story.
3. **Broaden past phones.** Use the existing `data/fleet/` inventory to pick
   first TV-box / SBC / devkit targets, then produce per-file rows for them.
4. **Finish the two clean-room gaps** named in `REPO-STATE-MAP.md`: `htt` and
   `root`. Keep `big-clusters` honest — analysis only, no self-test suite.
5. **Keep the corpus reproducible.** Every new dataset ships its generator;
   CI runs `tools/check_catalogs.py` and `tools/check_state_map.py`.

## What "done" means here

- A finding has a claim, evidence, a reproduction command, prior-art queries
  with dates, and a falsification chain (`research/_template/finding.md`).
- A format has a byte-level spec **and** a tested parser with synthetic
  fixtures.
- A device has per-file rows in the matrix, not just a model name in the
  inventory.
- Negative results are committed, not discarded.

## Explicitly out of scope

Per `SCOPE.md`: CVE hunting, classical-cipher cryptanalysis, and any commit of
proprietary payloads, decompiled output or device-private data.

## Status tracking

`docs/REPO-STATE-MAP.md` is a dated human snapshot (DONE / PARTIAL / NEW) used
by the agent fleet's Gate -1. `docs/issue-catalog/*.jsonl` is the machine-readable
work queue. This roadmap is the human-readable summary; update all three when
coverage changes materially.
