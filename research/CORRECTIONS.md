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
| 2026-11-26 | SM7325 / Kryo 670 Prime is `MIDR_CORTEX_X1`, MIDR `0x410fd440` | It is **Cortex-A78**, MIDR **`0x411fd411`** at the device's r1p1 — the *same* value as the Gold cluster, so the SoC has two distinct MIDRs, not three. `cputype.h`'s "Kryo 6XX Prime IDs itself as MIDR_CORTEX_X1" is a **family** note covering Kryo 680; Kryo 670 drops the X1. Three `sm7325` deviceinfohw captures report `FAMILY Cortex-A78 Cortex-A78 Cortex-A55`, and the same field reports `Cortex-X1` for `sm8350`, so it discriminates. Fixed in place in the SM7325 SoC note and `docs/REPO-STATE-MAP.md`. | `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-cpu.md` §3 (#853); `deviceinfohw.ru` items 103878/103829/103714 vs 103708 |
| 2026-11-26 | `CORTEX_A78` "appears in no erratum or mitigation list at all" because `cpufeature.c` has 0 hits | The count is right, the conclusion is not. A78 is listed in **`cpu_errata.c:402`** (`CONFIG_ARM64_ERRATUM_4118414`, TLBI completion), **`cpu_errata.c:669`** (`CONFIG_ARM64_ERRATUM_3194386`, SSBS) and **`proton-pack.c:882`** (`spectre_bhb_k32_list`); the Kconfig help names "ARM Cortex-A78 erratum 4193791" and "3324344". `cpufeature.c` holds capability/DBM tables, not errata. Fixed in place in the SM7325 SoC note. | `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-cpu.md` §4 (#853); `arch/arm64/kernel/{cpu_errata,proton-pack}.c` |
| 2026-11-26 | The `freq-domain` second phandle cell is a core count, giving three independent encodings of the cluster split | It is the vendor driver's **`max_cores` boost threshold**, compared against `LUT_CORE_COUNT` (`GENMASK(18,16)`) to flag `CPUFREQ_BOOST_FREQ` entries. It equals cluster size only on 6+2 parts (`blair`, `holi` → `6`,`2`); on 4+3+1 parts (`yupik`, `lahaina`, `shima`) it is `4`,`4`,`4`. Mainline dropped the cell: `#freq-domain-cells` is `const: 1` in the binding. Fixed in place in the SM4375 note. | `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-cpu.md` §3.1 (#847); `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-cpu.md` §2.2 (#853) |
| 2026-11-26 | The SM7325 CPU note's Rule 1 table said this file went "13 rows → 15 rows" | It went **11 → 14**: 11 data rows at `5790936` and 14 at `809e2f1`, three rows for three corrections. The `13` and `15` were both incremented by the wrong amount, and the same error was copied into the SM8350 CPU note's Rule 1 table as "16 rows". Both tables now measure the file instead of estimating it. | `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-cpu.md` §8 (#853); `git show 5790936:research/CORRECTIONS.md`, `git show 809e2f1:research/CORRECTIONS.md` |

## Contributing a correction

Use the `Correction` issue template. Edit the claim in place, add a row here with
the date and source, grep for the same error elsewhere, and list the before/after
in the PR description (`AGENTS.md`, Rule 1). Do not leave the wrong version
beside the corrected one "for context" — that is how stale numbers survive.
