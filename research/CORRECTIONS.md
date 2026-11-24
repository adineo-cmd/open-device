# Corrections

Claims this project got wrong, or that the wider ecosystem got wrong and we
corrected. Corrections are made **in place** in the original document; this file
is the changelog so a reader can see the history and so we do not repeat the
mistake. Dates are the dates recorded in the cited source; where no date was
recorded, the source is linked instead of invented.

| Date | Original claim | Correction | Source |
| --- | --- | --- | --- |
| 2026-11-16 | `cpp_firmware_*.fw` is WiFi firmware (upstream DB `blob_family=wifi`) | It is **MSM Camera Post-Processing microcode**. The upstream database label for 12 identities was corrected to camera. | `implementations/wifi-cpp-fleet/README.md`, `research/laptop/wifi-cpp-firmware-family.md` |
| 2026-11-16 | `*.jsn` files are split-MDT manifests | Premise refuted: mainline has zero `.jsn` handling; they are **JSON PDR service registries** consumed by userspace `pd-mapper`. | `implementations/README.md` (RULE 0 record), `implementations/pil-manifests/` |
| 2026-11-19 | ADSP `bm2nXX` files are DSP firmware | They are **serialized C++ tensor graphs** (QNN), not DSP firmware. The container is specified; the DSP code is not in the file. | `implementations/adsp-fleet/README.md` |
| 2026-11-19 | Adreno a650 GMU is a raw-ITCM class image like a619 | It is a **16-block container** class; 9 live devices of 14 carried, not 26. | `implementations/adreno650-fleet/README.md` |
| 2026-11-19 | `pdx215` / `Xperia_1_II` carries a650 | Mislabel corrected; SoC is `\N` in the DB and a650 co-residency is the current working attribution. | `implementations/adreno650-fleet/README.md` |
| — | MediaTek tinysys/scp is RISC-V | It is **ARM Cortex-M4F running FreeRTOS**. | `README.md` ("Two findings worth the trip") |
| — | MediaTek camera CCU core unidentified | It is **Synopsys ARCv2** (two ARC EM4-FPU cores). | `README.md` |
| — | MediaTek modem entry uses nanoMIPS | It is **MIPS32 LE with MIPS16e islands**; nanoMIPS belongs to later Dimensity silicon. | `README.md` |
| — | Qualcomm WCN6750 WiFi core is an 8-bit AVR (upstream Linux) | It is **32-bit RISC-V**. | `README.md` |
| 2026-11-19 | Repository scope is phone-specific | Renamed the repository (old and new names in `RENAME.md`); scope is now every device class. | `RENAME.md` |
| 2026-11-24 | Kryo 2XX MIDRs are `0x51008000` (gold) / `0x51008010` (silver) | They are **`0x510F8000` / `0x510F8010`**. `MIDR_CPU_MODEL` puts `0xf` in the architecture field (`cputype.h:43`), so the `0x0` nibble was wrong. A booted MSM8998 reports `0x51AF8001` / `0x51AF8014`, which mask down to the corrected pair. Fixed in place in the MSM8998 note, the SM4375 note and `docs/REPO-STATE-MAP.md`. | `research/soc/Qualcomm-MSM8998-Snapdragon-835-cpu.md` §4 (#841); `arch/arm64/include/asm/cputype.h:43` |

## Contributing a correction

Use the `Correction` issue template. Edit the claim in place, add a row here with
the date and source, grep for the same error elsewhere, and list the before/after
in the PR description (`AGENTS.md`, Rule 1). Do not leave the wrong version
beside the corrected one "for context" — that is how stale numbers survive.
