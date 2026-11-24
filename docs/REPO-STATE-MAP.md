# Repo-state map — what already exists, by issue family

Generated 2026-11-20 from `git rev-parse HEAD` and the committed tree. This is
the reference for Gate -1: before any issue is worked, its family row says what
already exists and what is actually missing.

> **Maintenance note:** this is a dated human snapshot, not a generated report.
> `tools/check_state_map.py` verifies that the artifact paths quoted below still
> resolve in the checkout and runs in CI; it cannot regenerate the verdicts.
> Refresh the table after material coverage changes, and update `ROADMAP.md` and
> `research/OPEN-QUESTIONS.md` at the same time.

Verdicts: **DONE** = deliverable present and tested; **PARTIAL** = substantial
work committed, a named delta remains; **NEW** = no committed deliverable.

## Summary

| issue family | count | verdict | existing artifact |
|---|---:|---|---|
| Firmware family doc | 1,107 | NEW | only stubs (`docs/devices/*/leverage-families.md`, "Deep-RE status: none yet") |
| Device package | 245 | NEW | `research/devices/` does not exist |
| SoC package | 27 | PARTIAL | 8 per-SoC GPU result docs under `research/soc/` plus 4 SoC-package notes (`Qualcomm-SM8350-Snapdragon-888-soc.md`, `Qualcomm-MSM8998-Snapdragon-835-soc.md`, `Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md`, `Qualcomm-SM7325-Snapdragon-778G-soc.md`: CPU/DSP/boot-chain/TZ/firmware census); `per-soc-method-plans.md` is the plan they derive from |
| CPU/SoC core ID | 27 | PARTIAL | 5 per-SoC CPU core-ID sections in `research/soc/`: SM8350 (4×A55 + 3×A78 + 1×X1, one `cpu-map` cluster, three `freq-domain`s), MSM8998 (4+4 Kryo 280, two clusters, `capacity-dmips-mhz` 1024/1536, MIDR `0x510F8000`/`0x510F8010` from `cputype.h` — no MIDR in the DT; `Qualcomm-MSM8998-Snapdragon-835-cpu.md` adds the observed device MIDRs `0x51AF8001`/`0x51AF8014`, the 8-vs-16 ISA flag split, and the fact that MSM8998 has no CPU DVFS node while SM8150 has 17 `cpufreq_hw` refs), SM4375 (2×A78 + 6×A55 from public spec, two `freq-domain`s in the sibling DT; **no** SM4375 DT exists, so the MIDRs `0x410fd410`/`0x410fd050` are `cputype.h` arithmetic and instruction-level proof is recorded as absent) and SM7325 (4+3+1 from `kodiak.dtsi`, one `cpu-map` cluster, three `freq-domain`s, capacities 1024/1946/1985; Kryo 670 reports stock A78/A55 MIDRs per `cputype.h:241-246`, so no vendor part number exists); 22 SoCs remain |
| GPU core ID | 27 | PARTIAL | 8 per-SoC GPU docs under `research/soc/`: MSM8998, SM4375, SM4350, SM7250, SM7325, SM8250, SM8350 (Adreno) + Google Tensor GS201 (Mali-G710, the first non-Adreno part); 19 SoCs remain |
| Driver interface | 42 | PARTIAL | 10 FP6 interface docs under `research/qualcomm/docs/` |
| Proprietary blob spec | 9 | PARTIAL | 6 families have committed format work |
| Firmware fleet | 9 | PARTIAL | 3 families have committed fleet notes |
| Deep RE | 15 | MIXED | see per-issue rows below |
| Device part | 18 | PARTIAL | `research/fleet/` covers boot/dtb and some partitions |
| Open-source implementation | 9 | PARTIAL | `implementations/` has 19 tested components |
| Clean-room implementation | 21 | DONE/PARTIAL | 19 components with code; 2 gaps (`root`, `htt`) |
| Site | 7 | DONE | deployed, closed |

## Blob spec — per family

| family | existing artifact | verdict | delta |
|---|---|---|---|
| adsp | `research/laptop/qualcomm-adsp-bm2n-container-header.md` (48/48 files, five invariants, segment table), `-fleet-content.md`, `-variant-matrix.md`; parser `implementations/adsp-fleet/` (86 tests) | PARTIAL | signature/attestation rules absent; fleet is bm2n only |
| boot | `research/qualcomm/docs/bootchain-census.md` (FP6 inventory, AVB, RISC-V cores) | PARTIAL | no byte-level cross-device container spec, no parser |
| bt | `research/fleet/qca-bt-format.md` (field-level spec, 29 devices), `research/fleet/patch-stream-structure.md`; parser `implementations/qca-bt/` (30 tests) | PARTIAL | signature/manifest semantics marked open; 24-byte vs vendor-extended header |
| cdsp | `research/cdsp-fleet/container.md` (split-MDT container, `p_flags` decode, sibling-size invariant, 2 devices / V65+V66), `research/cdsp-fleet/census.md` (23 files, 64 devices, 586 md5); parser `implementations/cdsp-fleet/` (140 tests) | PARTIAL | certificate/hash-record semantics `[OPEN]`; `cdsp_dtb.*` series unverified by bytes; no disassembly |
| gpu | `research/laptop/qualcomm-adreno-gmu.md`, `-gmu-content.md`, `-a650-fleet.md`, `research/fleet/gpu-bdwlan.md`, `research/soc/Qualcomm-*-gpu.md` (7 per-SoC Adreno: MSM8998, SM4375, SM4350, SM7250, SM7325, SM8250, SM8350), `research/soc/Google-Tensor-GS201-gpu.md` (1 per-SoC Mali: G710, 5 revisions × 5 devices, linux-firmware name-space collision); parsers `implementations/adreno650/` (4 tests), `adreno-fleet/` (62 tests) | PARTIAL | signature rules absent; no bdwlan GPU parser; no Mali parser; 19 of 27 SoCs have no per-SoC GPU doc |
| hyp | `research/fleet/tz-hyp.md` (63 rows / 63 devices / 153,300,992 B; 3 payloads decoded: SDM845 MBNv5, SM8250 MBNv6, QCM6490 MBNv7) | PARTIAL | 1 of 63 rows ISA-verified, 0 of 63 interface-documented; 11-row 8 MiB cluster is partition-size unproven; `w[1]` identified as MBN version |
| modem | `research/laptop/qualcomm-pil-manifest-family.md`, `research/fleet/pil-metadata-sweep.md`, `research/fleet/qdsp6sw-container.md`; parsers `implementations/pil-manifests/` (41 tests), `implementations/hexagon-qdsp6/` (47 tests) | PARTIAL | `qdsp6sw.mbn` (84,123,868 B) container + metadata + embedded QuRT XML decoded; CLADE payload bytes, `.clade.dict`/`.clade.comp` offsets, per-segment instruction decode still open |
| other | `research/laptop/qualcomm-data-blob-fleet.md` (hrtf5c, dax_param); parser `implementations/data-blob-fleet/` (54 tests) | PARTIAL | rest of the "other" bucket |
| tz | `research/fleet/dsp-tz-map.md` (QSEE ELF64 segment map, enchilada), `research/qualcomm/docs/trustzone-census.md` (FP6) | PARTIAL | cross-device spec, signature, `seg[10]` entropy 6.64 question |
| wifi | `research/fleet/bdwlan-format.md` (container RESOLVED, 34-file IE map, record structure) | PARTIAL | no stdlib parser, single-device scope |

## Firmware fleet — per family

| family | existing artifact | verdict | delta |
|---|---|---|---|
| adsp | `research/laptop/qualcomm-adsp-bm2n-fleet.md` (metadata, 20 devices), `-fleet-content.md` (48/48), `-variant-matrix.md`; `implementations/adsp-fleet/` | PARTIAL | catalog cites 253 files / `adspua.jsn` 60 devices; docs cover 48 bm2n |
| boot | `research/qualcomm/docs/bootchain-census.md` | PARTIAL | FP6 only |
| bt | `research/laptop/qualcomm-qca-bt-fleet.md`, `-content.md` (gen-1/gen-2, SHA-256 invariant), `research/fleet/qca-bt-format.md`, `patch-stream-structure.md` | PARTIAL | cross-device beyond laptop/mobile half |
| cdsp | `research/cdsp-fleet/census.md` (23 files, 64 devices, 586 md5, 51.8% shared instances), `research/cdsp-fleet/container.md` | PARTIAL | cross-device beyond devices 001-222 slice; `cdsp_dtb` reach |
| gpu | `research/laptop/qualcomm-adreno-a650-fleet.md`, `qualcomm-adreno-gmu-content.md`, `research/fleet/gpu-bdwlan.md`, `research/soc/Qualcomm-*-gpu.md` (6 Adreno per-SoC slices), `research/soc/Google-Tensor-GS201-gpu.md` (Mali per-SoC slice: matrix-wide `mali*` is 65 rows / 13 devices / 5 filenames) | PARTIAL | bdwlan GPU fleet; per-SoC slices are ad-hoc, no fleet-wide GPU census; whole Mali corpus is 5 filenames on 13 Tensor devices |
| modem | `research/fleet/pil-metadata-sweep.md` (SDM845 + SM8250), `research/fleet/qdsp6sw-container.md` (SM8250/SDX55M), `research/laptop/qualcomm-pil-manifest-family.md`; parser `implementations/hexagon-qdsp6/` | PARTIAL | CLADE payload decode, cross-device `qdsp6sw.mbn` |
| other | `research/laptop/qualcomm-data-blob-fleet.md` (2 blobs) | PARTIAL | rest |
| tz | `research/fleet/dsp-tz-map.md`, `research/fleet/qsee-crossgen.md` (SDM845 vs SM8250) | PARTIAL | cross-device |
| wifi | `research/fleet/bdwlan-format.md` (enchilada) | PARTIAL | cross-device |

## Deep RE — per issue

| issue | existing artifact | verdict |
|---|---|---|
| Adreno A650 GMU/SQE continuation | `research/laptop/qualcomm-adreno-a650-fleet.md`; `implementations/adreno650-fleet/` (113 tests) | DONE — only manifest record semantics `[OPEN]` |
| bdwlan tag semantics 1..30 | `research/fleet/bdwlan-format.md` | NEW — genuinely open |
| bm2n header words 11-15 + `0x10400` TOC | `qualcomm-adsp-bm2n-container-header.md` §2 resolves `u32[10]==0x010400` = `segment[0].flags` and `u32[2]==7` = build-id length | PARTIAL — words 11-15 open |
| bm2n tail `[2794,7172)` | none | NEW |
| 256-byte QCA patch tail | `research/fleet/patch-stream-structure.md` §1: per-file-unique high-entropy, signature/attestation-like `[F]` | PARTIAL — role not proven |
| WiFi `cpp_firmware` continuation | `research/laptop/wifi-cpp-firmware-family.md`; `implementations/wifi-cpp-fleet/` (88 tests) | DONE — only `[OPEN]` register |
| historic-device queue | `research/historic/historic-devices-queue.md` | PARTIAL — pmaports/LineageOS/UT/eOS expansion |
| MediaTek interface claims vs AOSP kernel | `research/mediatek/docs/*`, `research/mediatek/rosemary-census.md` | PARTIAL |
| patch-stream section boundary | `research/fleet/patch-stream-structure.md` line 181: "section boundary semantics unknown" | NEW |
| PIL `B01[40+32*n]` signing | `research/fleet/pil-metadata-sweep.md`; `research/fleet/other-fingerprint.md` §5 | PARTIAL — `b01` layout and per-part SHA-256 slots decoded for the fingerprint TA (`40+7×32+256+6144` exact, 6/7 slots, self-slot zeroed); sig alg is `sha256WithRSA` there, not the PSS the sweep generalised `[F]`; whether the 40-B base scales with `phnum` is `[U]` |
| PIL `.jsn` manifest extension | `research/laptop/qualcomm-pil-manifest-family.md`; `implementations/pil-manifests/` (41 tests) | DONE — only `[OPEN]` list |
| `media` subfamily (Venus/VPU, 470 rows / 53 devices) | `research/fleet/other-media.md` | DONE — census, container identity 5/5, ISA corrected `EM_XTENSA` not RISC-V, PR-5 withdrawn; `_unsigned` SHA-256 scheme, `venus`≡`cvpss` template `[F]` |
| `audio` subfamily (speaker-amp DSP, 422 rows / 83 devices) | `research/fleet/other-audio.md` | DONE — census; rows are coefficient payloads not bootable `.wmfw` (zero size-band overlap `[F]`); 2.75× symlink inflation, 234-name fan-out; Cirrus 44 / Awinic 36 devices, 0 both; `audio_dsp.img` Xtensa `[F]`; 60-byte ACF prefix `[F]`; no ISA in `.wmfw`, no Xtensa backend `[N]` |
| `touch` subfamily (panel + fingerprint firmware, 880 rows / 71 devices) | `research/fleet/other-touch.md` | DONE — census; `aoc.bin` is 74.7% of bucket bytes and is not touch `[F]`; `_FAE` spans 6 container formats `[F]`; Goodix GT9886 container fully specified — `0x100`+11 descriptors closes 14/14, checksum `BE16(sum bytes[6:])` 14/14 `[F]`; 13 files → 7 payloads, `6885b0` self-IDs as GT9885 `[F]`; mainline `goodix_fwupload.c` is a different container (36,878 B) `[F]`; no ISA resolved 880/880 `[N]` |
| `fingerprint` subfamily (QSEE fingerprint TA, 284 rows / 33 devices) | `research/fleet/other-fingerprint.md` | DONE — census; the bucket is missing its own ELF header — `fingerpr.mdt` is filed `misc` on all 33 devices while its `b00`–`b08` are filed `fingerprint` `[F]`; `b00` size gives `e_phnum` exactly (`64+phnum×56`, 33/33) and predicts the part count (`b08` iff `phnum==9`, 20/20) `[F]`; sig alg is `sha256WithRSA` not RSASSA-PSS, 0 PSS OIDs in 4/4 `[F]`; `b01` = `40+7×32+256+6144` exact, all `pil-metadata-sweep.md` field roles reproduce `[F]`; `b00` is a verbatim `.mdt` prefix duplicate 4/4 `[F]`; bucket is 61.1% of the 54 devices carrying this firmware — 21 devices have sensor firmware and zero bucket rows `[F]`; no local payload, class split is size-only inference `[N]` |
| `nfc` subfamily (NFC controller firmware, 75 rows / 46 devices) | `research/fleet/other-nfc.md` | DONE — census; 8 filenames resolve to **3 silicon vendors** (Samsung `sec_s3nrn*` 17 devices, STMicro `st54*` 22, NXP `sn100u` 7) with **zero cross-vendor devices** `[F]`; Samsung container fully decoded — `44 + 128 + 128 + N×4096` closes on `s3nrn4v` (N=45, 184,620 B) **and** on `s3nrn82` (N=37, 151,852 B) and on 0 of 6 non-Samsung sizes `[F]`; kernel spec agrees 8/8 fields `[F]`; two 128-B sigs are standard+custom, chosen at runtime from `bootinfo.hw_version[2]`, and `SHA1(image)` is recomputed not stored `[F]`; `sn100u.bin` is `db_type=AUDIO` on 7/7 rows (defect, `audio.md` already said so) `[F]`; `Galaxy_A21S` 3 exact duplicate rows `[F]`; `sn100u` opaque at 7.9957 bits/byte, 0 repeated 16-B blocks `[N]`; no ISA on 75/75 `[N]` |
| `fastchg` subfamily (315 rows / 28 devices) | `research/fleet/other-fastchg.md` | DONE — census; **only 4.96% of bytes are fast-charge firmware** — 82 rows at `firmware/tp/` (33.02%) and 31 at `firmware/ufs/` (61.32%) are mislabelled, 123 rows carry 95.04% of bytes `[F]`; `FwUp` container closes `80 + u32@0x0C + 128 == len` on 80/80 files `[F]`; `_FAE` is the bare body (`Δ = 208 = 80+128`) on 36/37 pairs, 1 counter-example is a different build `[F]`; wrapper hides 6 body dialects (24 binary / 13 ASCII Intel HEX) and `LIMITIMG` is a second container, `41/41` structural checks / 449 records `[F]`; embedded path renames `oppo_vooc_fw.bin`→`oplus_vooc_fw.bin` 20/20 `[F]`; `S3910` spans 4 subfamilies, `S3706` 3, 0 filenames shared `[F]`; trailer is a bijection with (header,body) but matches no plain digest 0/80 `[N]`; no public `FwUp` spec, no ISA on 315/315 `[N]` |
| `oled` subfamily (157 rows / 19 devices) | `research/fleet/other-oled.md` | DONE — census; all 157 rows are `LIMIT_*` at `firmware/tp/`, and `db_type=OLED` is exactly co-extensive with the subfamily (157/157) `[F]`; the 371 `LIMIT_` rows split exactly two ways, `touch` 214 / `oled` 157, over 47 names with **zero** shared names `[F]`; subfamily tracks the controller IC, 18 of 19 pure — the one split (`NT36672C`, 46/8) is decided by token *order* (`LIMIT_NF_*`→touch, `*_NF_*`→oled, 54/54) `[F]`; **one byte-identical payload is filed under both labels**: `LIMIT_SY761_SAMSUNG.img` (oled) ≡ `LIMIT_S6SY761_SAMSUNG.img` (touch), same md5 / 15,628 B / same 4 devices, 16 oled + 12 touch rows sit on the 2 cross-filed md5s `[F]`; two `LIMIT_*.ini` plaintext touch-test configs exist on disk and **0** `.ini` rows exist in the matrix `[F]`; record-magic `OPPO`⇒oled hypothesis refuted 37/56 (23/41 in `larry`) `[N]`; no in-tree `LIMITIMG` consumer, no `PV5_4` spec `[N]`; no ISA on 157/157 `[N]` |
| `qdsp6sw.mbn` | `research/fleet/qdsp6sw-container.md`; `implementations/hexagon-qdsp6/` (47 tests) | DONE — container, metadata segment, embedded QuRT XML; CLADE byte layout still `[OPEN]` |
| `camera` subfamily (asset-heavy, 1,611 rows / 72 devices) | `research/fleet/other-camera.md` | DONE — census; 2nd of 13 `other` subfamilies on rows **and** bytes (4,563,019,282 B) yet **88.2% of bytes are AI models + tuning tables** and PIL firmware is 27 `.mdt` rows / 144,108 B / 0.0032% `[F]`; FP6 `CAMERA_ICP` ISA corroborated — `.elf`/`.mbn`/`.mdt`/`.b00` are `e_machine=94` `EM_XTENSA`, verified both from the header and from inside the unstripped build (`xthal` 47, `xos` 154, `UEXC`+`KEXC` 155 symbols; `tensilica-lx7` / `Xtensa Compiler Version 12.0.9` build paths), while `CAMERA_ICP_170.elf` and the `enchilada`/`instantnoodle` copies are `e_machine=40` ARM32 — **same filename, two ISAs**; the header-level label is prior art from `qualcomm/docs/fp6-architecture-census.md` L35–L36 + `qualcomm/results/census.md` L653–677 and is credited, the symbol/build-path corroboration is new `[F]`; `CAMERA_ICP.mdt == b00 + b20` byte-for-byte on 5,484 B, hash found by `p_flags & 7<<24 == 2<<24` not by position, and hash index 20 is a **family constant** across 4 independent builds / 3 vendors / 2 sizes, vs `wpss` where `wifi-wpss.md` §2.4 measures it moving `b01`↔`b12` `[F]`; the `b00 + b<hash>` law widened 6→38 conforming files of 39 testable across 35 stems, hash indices 1–47, lone failure a synthetic fixture `[F]`; `db_type=ELF64` wrong on 28/28 ELF32 `.mdt` rows `[F]`; 50 rows filed `camera` sit at `vendor/gpu/kbc` beside GPU kernel caches and 3 `.img` rows sit at `…/radio` (both report-only) `[F]`; 0-hit public queries incl. `linux-firmware` `WHENCE` (540,393 B) — no source documents the container's segment roles or any of the 410 filenames `[N]`; no Xtensa disassembler, so no instruction-level claim `[N]` |
| QSEE PSS blocks | `research/fleet/qsee-crossgen.md` | PARTIAL |
| Tensor radio-directory inventory | none | NEW |
| `tz.img` `seg[10]` entropy 6.64 | `research/fleet/dsp-tz-map.md` open item | NEW |

## Rule

An issue marked DONE here is closed with `ALREADY-DONE`. An issue marked PARTIAL
gets a `REPO-STATE` comment naming the existing path and the delta; the agent
does the delta only. An issue marked NEW proceeds to Gate 0 unchanged.
