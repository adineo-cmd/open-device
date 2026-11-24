# Open questions

A single entry point for the `[OPEN]` markers scattered through the evidence.
This is an index of *pointers*, not a replacement for the question's own section
— the detailed statement and evidence stay where they belong.

When you resolve one, update its home document **and** remove the pointer here.
If a question is refuted, move it to `research/CORRECTIONS.md` instead.

## Highest impact

| Question | Home document | Why it matters |
| --- | --- | --- |
| `qdsp6sw.mbn` payload undecoded (issue #606) | `docs/REPO-STATE-MAP.md` (Deep RE) | ~84 MB, ~48% of SM8250 modem volume |
| CDSP: no spec and no parser | `docs/REPO-STATE-MAP.md` (Blob spec / Fleet) | Entire firmware family undocumented |
| Signature and attestation rules per family | `docs/REPO-STATE-MAP.md`, each family's `## [OPEN]` | Blocks complete boot-chain claims |
| `tz.img` `seg[10]` entropy 6.64 | `research/fleet/dsp-tz-map.md` | Unexplained high-entropy segment |

## Per-family pointers

| Family | Canonical open-question section |
| --- | --- |
| Qualcomm ADSP / bm2n | `research/laptop/qualcomm-adsp-bm2n-container-header.md` (words 11-15, tail) |
| Qualcomm Bluetooth / QCA | `research/fleet/qca-bt-format.md`, `research/laptop/qualcomm-qca-bt-fleet-content.md` |
| Qualcomm GPU / Adreno | `research/laptop/qualcomm-adreno-gmu-content.md` §8, `implementations/adreno650-fleet/a650-fleet-analysis.md` |
| Qualcomm modem / PIL | `research/fleet/pil-metadata-sweep.md`, `research/laptop/qualcomm-pil-manifest-family.md` |
| Qualcomm WiFi / bdwlan | `research/fleet/bdwlan-format.md` (tags 1..30) |
| Qualcomm TrustZone | `research/fleet/qsee-crossgen.md`, `research/fleet/dsp-tz-map.md` |
| Patch streams | `research/fleet/patch-stream-structure.md` (section boundary, 256-byte tail) |
| MediaTek interfaces | `research/mediatek/docs/`, `implementations/mediatek/*/README.md` |
| Camera assets | `research/laptop/xiaomi-camera-effect-assets.md` (channel order) |

## Clean-room component gaps

| Component | Status |
| --- | --- |
| `implementations/htt` | documented gap; no committed implementation |
| `implementations/root` | documented gap (`REPO-STATE-MAP.md`) |
| `implementations/big-clusters` | analysis only, no self-test suite |

## Rule for adding entries

Use a relative path and a section anchor where possible. Add a one-line reason.
Do not copy the whole open question here — duplication causes drift.
