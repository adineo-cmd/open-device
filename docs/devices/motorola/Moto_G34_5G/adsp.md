# motorola Moto_G34_5G (fogos) - `adsp` family status (44 rows - PRESENT, census-complete; split-PIL audio-DSP image at modem/image plus the six-file bm2n QNN/HTP graph set at vendor/lib/rfsa/adsp; the missing `adsp.b11` is STRUCTURAL on the 2022-2024 mid-tier fleet, not a census gap)

Analysis date: 2026-11-21. Analyst: ZC-1 (issue [#1294](https://github.com/adineo-cmd/open-device/issues/1294)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, feat/open-device-site 1edfc16), `upstream-contribution/blob-database/device-inventory.csv`, LineageOS `android_device_motorola_fogos` and `android_device_motorola_sm6375-common` `proprietary-files.txt` (lineage-22.2 branch, fetched 2026-11-21), torvalds/linux master `arch/arm64/boot/dts/qcom/sm6375.dtsi`, `drivers/remoteproc/qcom_q6v5_pas.c`, `drivers/soc/qcom/mdt_loader.c` (fetched 2026-11-21), linux-firmware WHENCE (git.kernel.org, fetched and grepped 2026-11-21), public spec pages (GSMArena, PhoneDB, Motorola support, 2026-11-21), in-repo family research `research/laptop/qualcomm-adsp-bm2n-container-header.md`, `-fleet.md`, `-fleet-content.md`, `-variant-matrix.md` (2026-11-18) and sibling device docs docs/devices/motorola/Moto_G10/adsp.md (#1258), docs/devices/xiaomi/Mi_A3/adsp.md (#1240), docs/devices/xiaomi/Mi_12T_Pro/adsp.md. No device payload was fetched or committed; no binary was parsed beyond what the cited in-repo research already measured. Every number is command output or a recorded fetch; sums re-verified with python3 this session.

**Verdict: the `adsp` family is PRESENT on Moto_G34_5G and the census is COMPLETE - 44 rows, 24,262,536 B, 44 distinct md5s, all db_type=MODEM, priority P3, in two containers.** Container (a), 38 rows at `motorola/fogos/modem/image`, is the signed split-PIL audio-DSP (ADSP) firmware image in Qualcomm's split-ELF convention: `adsp.mdt` 9,500 B + 34 segment files `adsp.b00`-`adsp.b34` (15,378,457 B together) + the 3-file servreg manifest trio (`adspr.jsn`, `adsps.jsn`, `adspua.jsn`, 1,363 B together). The b00-b34 range has exactly one gap, `adsp.b11`, and that gap is **structural, not a census gap**: the derived ELF has e_phnum 36 (b00 = 52 + 36 x 32 exactly), and the shipped set {b00..b34} minus exactly one index requires a file-less program header 11 - the same two-BSS-only-phdr pattern proven against the public linux-firmware QCM2290 build in #1258, reproduced here by an 11-device mid-tier fleet in which every member with census segments shows the identical shape. Container (b), 6 rows at `motorola/fogos/vendor/lib/rfsa/adsp` (`bm2n06/08/12/13/14/15.bin`, 8,873,216 B), is the SM6375-tree six-file set of the corpus-wide `bm2nXX` fleet: serialized QNN/HTP neural-network graph payloads delivered over FastRPC, **not modem code** despite the MODEM db_type (in-repo content research, cited below). The rfsa half is proven 6/6 complete against the public LineageOS packaging manifest, whose sm6375-common blob list states it was extracted from this device's own stock build.

## Device identity

| fact | value | source |
|---|---|---|
| model | Motorola Moto G34 5G, XT2363 (XT2363-1/-2/-3) | public spec pages (GSMArena, PhoneDB, Motorola support; fetched 2026-11-21) [F] |
| codename | `fogos` (db_path, LineageOS device tree, PhoneDB agree) | `device-inventory.csv` [F]; LineageOS `android_device_motorola_fogos` (fetched 2026-11-21) [F] |
| SoC | Qualcomm **SM6375 Snapdragon 695 5G** (6 nm), Kryo 660, Adreno 619 | inventory cell [F]; public spec pages (2026-11-21) [F]. **The inventory SoC cell is CORRECT for this device** - unlike the known-wrong dubai/tundra cells |
| DSP | Hexagon 686 (spec listings for SM6375); architecture v68/v69 SDK target generation | public spec listings (2026-11-21) [F, secondary]; QAIRT SDK target mapping [I] |
| released | inventory `released_year` cell EMPTY (data hygiene); public pages: announced December 2023 | device-inventory.csv [F]; public spec pages (2026-11-21) [F] |
| stock build | `fogos_g V1UGS35H.75-14-13-1` | LineageOS fogos and sm6375-common proprietary-files.txt headers "All unpinned blobs are extracted from fogos_g V1UGS35H.75-14-13-1" (fetched 2026-11-21) [F] |
| census scope | 358 rows in 9 families (wifi 99, other 65, tz 50, modem 47, adsp 44, gpu 19, bt 14, cdsp 12, boot 8; sum 358 = inventory count) | coverage-matrix.csv + device-inventory.csv [F] |
| priority | P3 | coverage-matrix.csv, all 44 adsp rows [F] |

Inventory flags for the lead: (a) `released_year` EMPTY for fogos [F]; (b) `extract_status_22.2` = "fails" [F]; (c) `count_csv_total` = 37 while the coverage-matrix holds 44 adsp rows - the same artifact accounting drift flagged for capri in #1258 [F cells]; (d) the `adspr.jsn`/`bm2n` share-fleets below again include the matrix cells already flagged in #1240 - OnePlus_7 is labeled "MSM8998 Snapdragon 835" but is SM8150 per public specs, and Nord_CE3's cell carries a leading mojibake byte - re-citing those flags, not re-deriving them; (e) new flag: corpus device `Nord_CE2` carries cell "SM6375 Snapdragon 695" but the retail OnePlus Nord CE 2 5G is MediaTek Dimensity 900 - the SM6375 device is the Nord CE 2 **Lite**; census shape (below) is SM6375-fleet-consistent, so the name or the cell is off by one product [OPEN].

## Census evidence [F]

All 44 adsp rows: `blob_subfamily` empty, `sha256_if_listed` empty, `isa_identified` empty, `interface_documented=n`, db_type `MODEM`, priority P3 (single `uniq -c` line `44 |||n|P3`, this session); 44 distinct md5s (no internal duplication). db_type=MODEM is genuinely accurate for the image half - it ships in the modem partition (below) - and is a path artifact for the rfsa half (see the bm2n section).

| container | rows | bytes | db_path |
|---|---|---|---|
| split-PIL firmware (`adsp.mdt` + 34 `adsp.bNN`, b00-b34 minus b11) | 35 | 15,387,957 | `motorola/fogos/modem/image` |
| servreg manifest trio (`adspr.jsn`, `adsps.jsn`, `adspua.jsn`) | 3 | 1,363 | `motorola/fogos/modem/image` |
| bm2n QNN/HTP graph set (`bm2n06/08/12/13/14/15.bin`) | 6 | 8,873,216 | `motorola/fogos/vendor/lib/rfsa/adsp` |
| total | 44 | 24,262,536 | - |

Verified decomposition: 9,500 (mdt) + 15,378,457 (34 bNN) + 1,363 (3 jsn: 403+405+555) = 15,389,320; 15,389,320 + 8,873,216 (6 bm2n) = 24,262,536 (python, this session). The image half is 63.43% of family bytes, the rfsa half 36.57%. The rfsa path carries NO other census family for fogos - exactly 6 rows, all adsp (awk, this session). Min segment 140 B (`adsp.b24`), max 6,774,696 B (`adsp.b25`, 27.92% of family bytes).

### Shell and manifest files (4)

| file | bytes | md5 | distinct devices sharing md5 |
|---|---|---|---|
| adsp.mdt | 9,500 | `1ab26984b849c32979d81e09e1b71587` | 1 (Moto_G34_5G only) |
| adspr.jsn | 403 | `40d6edf129dec063ca3fe6cb6837488f` | 29 |
| adsps.jsn | 405 | `c7253d84bff46e4cf5cb0585e9a851c5` | 23 |
| adspua.jsn | 555 | `d0bd5030a03f631c9af5060a5645d02e` | 29 |

The jsn trio bytes are the exact identities #1258 (#1240) byte-verified against the public linux-firmware files `qcom/qcm2290/{adspr,adsps,adspua}.jsn` (WHENCE lines 7435-7437; line numbers re-confirmed by fetch 2026-11-21) and schema-verified: sr_version 1.1.1, sr_domain {soc "msm", domain "adsp", qmi_instance_id 74}, subdomains adspr = root_pd, adsps = sensor_pd, adspua = audio_pd; adspua additionally declares the avs/audio service. Stock Android's proprietary `pd-mapper-svc` parses these files at boot (public boot logs; recorded at Gate 0) - the schema is public-adjacent prior art, the files themselves are fleet-generic, not device RE targets.

### Segment files (34; b00-b34 minus b11)

`devices` = distinct corpus devices carrying that byte identity (md5 sweep over all 33,917 rows, python this session):

| file | bytes | md5 | devices |
|---|---|---|---|
| adsp.b00 | 1,204 | `b2e9fd0280eae783bc3a244238f00a0b` | 1 |
| adsp.b01 | 8,296 | `d1a1a30a95cc2fb5e62778d124619ecb` | 1 |
| adsp.b02 | 85,800 | `223ff3fe7ba1e657be18985c480e26cb` | 1 |
| adsp.b03 | 387,456 | `ffe67676c09c9fe84eaa7bf6b45e3954` | 1 |
| adsp.b04 | 1,821,388 | `eb2106701c33af486eb89bb62b782f12` | 1 |
| adsp.b05 | 2,230,204 | `4bc0bffcfbc9336d976871e503e1ca12` | 1 |
| adsp.b06 | 3,000 | `b26980013da673b62dbecb34aa3840c2` | 2 (Moto_G34_5G, Moto_G84_5G) |
| adsp.b07 | 17,512 | `94ff7f4ee78b886f895853b693282f95` | 7 (G34, Edge_30_Neo, G_Stylus_5G-2-2022, G82, G84, G_5G_2024, G_Stylus_5G) |
| adsp.b08 | 28,620 | `3dad7dfa25fefaa22a20d3962e6a7348` | 6 (G34, Edge_30_Neo, G_Stylus_5G-2-2022, G82, G84, G_5G_2024) |
| adsp.b09 | 4,868 | `70fd518a2cf079eaab03785965cee344` | 3 (G34, G84, G_5G_2024) |
| adsp.b10 | 260 | `1fba82ad4830c8c9752ce6d26eadf424` | 11 (the entire shape fleet below) |
| adsp.b12 | 61,760 | `52d6924fd016d44899fa01e0c6a94693` | 1 |
| adsp.b13 | 72,456 | `982ddcdfe96a156fb3a81d62425c1c58` | 1 |
| adsp.b14 | 757,760 | `028b777a5eb7293d66bcfe0576e34934` | 1 |
| adsp.b15 | 1,386,972 | `c5c87a1eda8556d936169b27d1a2de53` | 1 |
| adsp.b16 | 24,580 | `f1f407f5b55bb4aecdc2fd47bf3e5bee` | 1 |
| adsp.b17 | 10,367 | `dc3754aee42e76c2c3f88b3213b730e9` | 1 |
| adsp.b18 | 10,616 | `44f441823cb8cae5058006f94fffcb92` | 7 (G34, Edge_30_Neo, G_Stylus_5G-2-2022, G82, G84, G_5G_2024, G_Stylus_5G) |
| adsp.b19 | 3,863 | `ed959a83891320116804f690332fe671` | 2 (G34, G_5G_2024) |
| adsp.b20 | 18,216 | `013c4669366f8348efccd29745e177bc` | 1 |
| adsp.b21 | 50,148 | `cf735ae9ef470337202495c7fc3de78e` | 1 |
| adsp.b22 | 256,272 | `2d6170d41db25c47cbca4fe6e65912a4` | 1 |
| adsp.b23 | 186,920 | `277373f65e3bc7133356fddc3bcb7c94` | 1 |
| adsp.b24 | 140 | `ea7631285e9bad0acd363b573cb00f94` | 1 |
| adsp.b25 | 6,774,696 | `2fbf7f3c67926ce171e800d60d8dd03b` | 1 |
| adsp.b26 | 288,520 | `98d5755df840550f34eee1a44ccaf5fa` | 1 |
| adsp.b27 | 2,680 | `7f609825bb6b02a43157de18feb6c5a8` | 1 |
| adsp.b28 | 17,544 | `8ce835965a5028cbf900142cdab3e6c3` | 4 (G34, Edge_30_Neo, G84, G_5G_2024) |
| adsp.b29 | 491,520 | `dfc9e8c7bd3d50f404d6f0b6ada20b0c` | 6 (G34, Edge_30_Neo, G82, G84, G_5G_2024, G_Stylus_5G) |
| adsp.b30 | 17,913 | `0f05f67796f4023c1e23cdea20d85659` | 4 (G34, Edge_30_Neo, G84, G_5G_2024) |
| adsp.b31 | 4,628 | `a74525490cfb1ab04ff9ae8869a36a34` | 6 (G34, Edge_30_Neo, G82, G84, G_5G_2024, G_Stylus_5G) |
| adsp.b32 | 659 | `79cf6aa1363e4c489d6e9ee88ae23410` | 4 (G34, Edge_30_Neo, G84, G_5G_2024) |
| adsp.b33 | 62,279 | `8fcdca2290336e2dd3dea5f94c573e36` | 1 |
| adsp.b34 | 289,340 | `2dd744878e485927e9d7466487eadf5d` | 1 |

22 of 34 segments (and the mdt) are Moto_G34_5G-exclusive corpus-wide - device-signed firmware is not shared, only the generic manifests and 12 small low/high-index segments of the mid-tier fleet (b06/b07/b08/b09/b10/b18/b19/b28/b29/b30/b31/b32) [F].

### bm2n rfsa files (6)

| file | bytes | md5 | distinct devices carrying identity |
|---|---|---|---|
| bm2n06.bin | 864,824 | `9010bb1a7c08222a058aaef7edd938c6` | 25 (24 others + G34) |
| bm2n08.bin | 3,091,896 | `1275a2d212e5bccce734d3055ff10156` | 25 |
| bm2n12.bin | 2,623,528 | `5c86c8fcc7451f51e11d38276253aac8` | 26 |
| bm2n13.bin | 1,106,944 | `bf635d9084b54633526f9ad8a84d299b` | 25 |
| bm2n14.bin | 103,168 | `805176afaae27821520b79647fa5d498` | 26 |
| bm2n15.bin | 1,082,856 | `2ce8163cda60f33cbf2b50f03a3d0ea1` | 26 |

These are exactly the six canonical identities of the in-repo bm2n primary fleet table (`qualcomm-adsp-bm2n-container-header.md` section 1, "DB devices 25/25/26/25/26/26" - consistent with the sweep above; python, this session). Sharers' SoC cells span SM4350/SM4375/SM6375/SM7250/SM7325(-AE)/SM8250/SM8350(-AC)/QCM6490 (awk/python, this session) across Motorola, OnePlus, Sony, Realme, Fairphone, Nothing - the established 25-device leverage set of the variant matrix, which explicitly lists Moto G34 5G.

## Container layout - derived from two exact arithmetic laws

All arithmetic python-verified this session; the split-ELF convention is public (torvalds/linux `drivers/soc/qcom/mdt_loader.c`).

- **Law 1: `adsp.b00` = 1,204 = 52 + 36 x 32.** A little-endian ELF32 header is 52 B and each program header entry 32 B; program header 0 in Qualcomm split-ELF images is a self-referential segment holding the header table itself (public anchor: the linux-firmware QCM2290 build parsed in #1258 has phdr 0 = 52 + 30 x 32 with e_phnum 30). So **fogos' ADSP ELF has e_phnum = 36** [F arithmetic + public anchor].
- **Law 2: mdt = b00 + b01 exactly: 1,204 + 8,296 = 9,500.** The mdt retains the header table (phdr 0) plus the hash/metadata segment (phdr 1); the kernel mdt loader reads the header from the mdt and the hash table from the mdt itself (`mdt_loader.c`, fetched 2026-11-21) [F].
- The loader names split segments `b%02d` by **program-header index** (`mdt_loader.c` line 84) and requests them only for PT_LOAD headers with `p_filesz > 0` [F].
- **Shipped-set model [I]:** with e_phnum 36, indices 0..35; phdr 35 (last) is the generational trailing BSS (QCM2290 witness: phdr 29 = p_filesz 0, p_memsz 3,575,808) so no b35 file; the shipped set is {b00..b34} (35 slots) and the census holds 34 - exactly one interior file-less phdr, index 11. **Boot-time request set [I]:** applying the loader rules, the kernel at boot would fetch `adsp.b02`-`adsp.b34` minus b11 (32 files) - phdr 0 rides in the mdt and phdr 1 is the hash segment; b00/b01 exist on the device filesystem because Motorola's packaging tool dumps every file-backed segment, but are not fetched at boot.

## The b11 absence is STRUCTURAL, not a census gap

Four independent lines of evidence, all command-verified:

1. **Public generational witness [F, from #1258]:** the public QCM2290 (SM4250-generation) ADSP build `qcom/qcm2290/adsp.mbn` has program header 11 with p_filesz 0 (BSS-only) AND a file-less trailing phdr - exactly the two-BSS pattern the fogos size laws require. A filesz-0 PT_LOAD produces no `.bNN` file (loader rule, `mdt_loader.c`). [I] the fogos build follows the same generational layout (its own mdt bytes are not in the corpus; linux-firmware ships NO SM6375/holi adsp build - WHENCE grep for sm6375/holi returned zero entries, fetched 2026-11-21).
2. **Corpus fleet sweep [F]:** every corpus device with the mid-tier 2022-2024 shape skips **exactly** b11 with identical spans - 11 devices hold 44 adsp rows, 34 segments spanning b00..b34 (python, this session): Moto_G34_5G, Moto_G82_5G, Moto_G84_5G, Edge_30_Neo, G_Stylus_5G-2-2022, Moto_G_5G_2024, Moto_G_Stylus_5G, Nord_CE2, Nord_CE3, Realme_9_Pro, Realme_10_Pro. Public identities on the Moto members: G34 = SM6375 [F], G84 = SM6375 (GSMArena primary; SM6450/SM7435-AB regional variants documented) [F], G Stylus 5G (2022) = SM6375 [F], G 5G (2024) = **SM4375** [F - the corpus cell, initially suspected wrong, is CORRECT], G Stylus 5G (2023) = **SM6450** [F - the corpus device `Moto_G_Stylus_5G` is generation-ambiguous; shape matches either way]. The fleet therefore spans SM4375/SM6375/SM6450-class Moto builds and SM6375 OnePlus/Realme builds - one generation of Qualcomm mid-tier packaging, not one SoC.
3. **Contrast cohort [F]:** 37 corpus devices DO census `adsp.b11`/`adsp2.b11` (python, this session) - 16 with flagship-class cells (SM8150/SM8250/SM8350/SM8475/SM8550, SM7250, SM7325-AE, MSM8998, QCM6490) plus 21 devices carrying the known-EMPTY soc cells (Mi_A3, Mi_12/13 series, OnePlus_9/12/13, FP6, Nord_4/CE4, Pad_Pro/Pad_2_Pro, Poco_F5 family, Redmi_K60_Pro - publicly 8xxx/7xxx-class SoCs [I]). Mi_A3 (SD665-class, 2019 build) also censuses b11 - so the skip is a firmware-generation property, not strictly a SoC one. Inside the mid-tier cohort there is no counter-example: 0 of 11 shape-fleet devices have b11, FP4 (SM7225 cell) also skips b11 with a 33-segment b00..b33 image, and #1258 already proved 10/10 bengal Moto devices skip b11 with a different phnum - the cross-OEM uniformity (Motorola + OnePlus + Realme) rules out a Moto-extractor artifact.
4. **Shell-size clusters [F]:** all 11 fleet devices carry b00 = 1,204 B (e_phnum 36 for all), b10 = 260 B, and byte-identical jsn trio md5s; two shell clusters exist - Moto mdt 9,500 / b01 8,296 (G34, G82, G84, Edge_30_Neo, G_5G_2024) vs OnePlus+Realme mdt 9,348 / b01 8,144 (Nord_CE2, Nord_CE3, Realme_9_Pro, Realme_10_Pro) (python, this session). The 260-B `adsp.b10` is byte-identical across all 11 - a fleet marker segment.

Conclusion: the 34-segment census is the complete shipped file set; there is no missing b11 to find. This extends the #1258 bengal proof one generation up (bengal phnum 33-37; this fleet phnum 36 across three SoC families).

## Cross-corpus facts

- **Shape-fleet payload sharing:** fogos' b07/b08/b18 (17,512 / 28,620 / 10,616 B) are byte-identical across 6-7 Moto members of the fleet (incl. G_5G_2024 on SM4375 - cross-SoC code sharing within one Motorola packaging generation [I]); b29/b31 across 6; b06/b09/b19/b28/b30/b32 across 2-4. No fogos image-half byte is shared with any non-fleet device [F].
- **Sony contrast [I]:** the SM6375 Sony devices in the corpus (Xperia_10_IV, Xperia_10_V, Xperia_5_V, Xperia_1_V) census bm2n rows ONLY (the 6-file rfsa set) with zero modem/image rows - a census-scope difference (their modem partitions are not in the extraction corpus), not a structural absence; the same 6 bm2n identities on both OEMs show the rfsa payloads are platform-common while the signed image is per-device.
- **Packaging [F]:** the LineageOS `android_device_motorola_sm6375-common` manifest (fetched 2026-11-21) packages, under "# ADSP", exactly `vendor/lib/rfsa/adsp/bm2n06/08/12/13/14/15.bin` - 6 of 23 rfsa/adsp entries, the other 17 being `.so` DSP shared objects (not census adsp family); the fogos device-tree manifest packages NO adsp files at all (only `vendor/etc/acdbdata/adsp_avs_config.acdb`). The split-PIL image ships in the modem partition and is extracted from there, matching the census db_path 1:1 and making the census the only completeness witness for the image half - while the rfsa half is independently witnessed 6/6 by the public manifest.
- **Public byte witness [F, from variant matrix attempt #9, fetched 2026-11-18]:** `TheMuppets/proprietary_vendor_motorola_sm6375-common` (lineage-22.2 through 24.0) carries `bm2n13.bin` = 1,106,944 B, md5 `bf635d9084b54633526f9ad8a84d299b` - fogos' exact identity, in a public tree, under a manifest whose header names fogos' own stock build.

## The bm2n half - what the six files are

The in-repo fleet research (all [F], MEASURED PAYLOADS, 2026-11-18) applies to fogos' six files because their md5s are the canonical fleet identities:

- **Container [F]:** little-endian load-header + segment table, validated 48/48 - magic `0xfa0000fa` at 0x14, build-id 7 ASCII chars + NUL at 0x0c with length prefix at 0x08, load base at 0x00/0x1c (one of 0x200000/0x400000/0x800000), segment count at 0x20, segment table at 0x24, terminator `((~n & 0xffff) << 16) | n`; addresses are LOAD addresses, not file offsets. fogos' `bm2n13.bin` (build-id `5371806`, 3 segments, terminator `0xfffc0003`) is the section-1 worked example of that document.
- **Content [F]:** serialized QNN/HTP neural-network graph payloads - record tag `TENSOR_MAGIC 0x1337beef` from public `QNN/HTP/core/tensor.h:100`, prologue RTTI name `14ConcreteTensorIN5Tdefs10QuantUint8EE`, `hnnx`-namespaced operator classes, one fleet member a standard HTP pickle (`0x7309F72B`); entropy 3.5-7.6 bits/byte (structured, not encrypted). Per-file facts for fogos' six: bm2n06 build-id `4bd22b0`, N=2, 781 records; bm2n08 `32da3bd`, N=3, 1,227; bm2n12 `2c855d1`, N=3, 17,241; bm2n13 `5371806`, N=3; bm2n14 `2a8527c`, N=2, 885; bm2n15 `5371806`, N=3, 4,348.
- **Delivery [F]:** runtime FastRPC, not boot PIL - `vendor/lib/rfsa/adsp` is the FastRPC ADSP-domain path (`ADSP_DOMAIN_ID (0)` in `drivers/misc/fastrpc.c:31`); the MODEM db_type is a corpus labeling artifact of the adsp family, established for diting in the Mi_12T_Pro doc and holding here by identity.
- Parser and 86-test suite: `implementations/adsp-fleet/` (in-repo).

## Interface and ISA facts

- **Mainline support state [F]:** torvalds/linux `sm6375.dtsi` (fetched 2026-11-21) declares `remoteproc_adsp: remoteproc@a400000`, compatible `qcom,sm6375-adsp-pas`, memory-region `pil_adsp_mem` at 0x86700000 size 0x2000000 = 33,554,432 B (32 MiB) (lines 1567-1612, 580-582), glink edge "lpass", power-domains SM6375_VDD_LPI_CX/MX; `qcom_q6v5_pas.c` line 2051 registers `{ .compatible = "qcom,sm6375-adsp-pas", .data = &sm6350_adsp_resource }`. Mainline sm6375.dtsi has NO fastrpc node; 32 MiB carve-out fits the 14.68 MiB image half with headroom [I].
- **Firmware location [I]:** with modem-partition shipping, a booted stock device exposes the image under the firmware mount of the modem partition (`image/adsp.*`), which is what the extraction corpus recorded as `motorola/fogos/modem/image`; the exact firmware-name string in fogos' non-public vendor DT is unconfirmed. The plain `adsp` naming (vs bengal's `adsp2`) matches the per-build packaging choice documented in #1258, and matches mainline's default `adsp` fw name for the PAS driver [I].
- **ISA [F + honest negative]:** SM6375's DSP is Hexagon 686 per public spec listings (2026-11-21); Hexagon QDSP6 as the ELF machine type is attested by the public QCM2290 sibling build's e_machine 164 (#1258 parse). The corpus records `isa_identified` EMPTY and `interface_documented=n` on all 44 rows - the segments are honestly un-RE'd here; no disassembly was performed. By size alone the likely code/resource-bearing segments are b25 (6,774,696 B, 27.92% of family), b05 (2,230,204), b04 (1,821,388), b15 (1,386,972) and b14 (757,760) - together 12,971,020 B = 53.46% of family bytes [I - no disassembly performed].

## Honest negatives ([OPEN])

- No payload of this device was fetched or analyzed (metadata-only; the 38 device-signed image files exist in the corpus as hashes only; the 6 bm2n identities are covered by the in-repo fleet research's own payload work, not re-fetched here).
- The fogos phdr-level facts (e_phnum 36; phdr 11 BSS-only; phdr 35 trailing BSS) are derived from two exact size laws plus fleet uniformity plus the public generational witness - not from fogos' own mdt bytes. A program-header dump of the real `adsp.mdt` (9,500 B) remains the direct proof and is [OPEN].
- No Hexagon ISA proof: no segment was disassembled; Hexagon 686 / v68-v69 generation is from spec pages and SDK targets, not from the blobs.
- Record-level semantics of the bm2n graphs (record payload semantics, segment `kind` values, window field, prologue scalars) remain [OPEN] per the in-repo fleet research.
- Which Moto board DT string boots this image on fogos (mainline PAS default is `adsp`; fogos' vendor DT unverified) is [OPEN].
- `Nord_CE2` corpus identity (retail Nord CE 2 is Dimensity 900; SM6375 device is CE 2 Lite) and `Moto_G_Stylus_5G` generation (2022 = SM6375 vs 2023 = SM6450) are unresolved [OPEN] - shape analysis is unaffected.
- The exact relationship of the Moto shell cluster (mdt 9,500 / b01 8,296) to the OnePlus+Realme cluster (mdt 9,348 / b01 8,144) - same e_phnum, different hash-segment size - is unexplained beyond "different signing payloads" [OPEN].

## What would upgrade this finding

1. Extract the stock modem partition (fastboot image or OTA payload), byte-verify all 38 image-row md5s, and dump the ELF program headers of `adsp.mdt` (9,500 B): expect e_phnum 36, phdr 11 with p_filesz 0, phdr 35 with p_filesz 0, phdr 1 as the hash segment - that would convert the structural-b11 [I] into a direct [F].
2. Disassemble b25/b05/b04/b15 with a public Hexagon toolchain (Ghidra Hexagon module or a Capstone fork) and record the Hexagon ISA revision - fills `isa_identified` for the image half.
3. Diff fogos' b25/b05 segments against the G82/G84/Edge_30_Neo builds (sizes differ? bytes differ?) to map which ADSP code is shared across the Moto mid-tier generation vs per-device.
4. Trace the bm2n graph set's runtime consumer on SM6375 (which vendor service loads `bm2nXX.bin` via FastRPC - QNN runtime session cache) and diff against the SM8475 diting set documented in the Mi_12T_Pro doc.

## RULE 0 record

- CLAIM posted 2026-11-21T12:37:32Z as the first comment (confirmed first by re-read at 12:37:37Z; no other agent claimed).
- SEARCH (Gate -1) and GATE 0/DELTA posted 2026-11-21; work started only after both.
- All census numbers are awk/python outputs on coverage-matrix.csv at feat/open-device-site 1edfc16, this session; all web fetches and web searches dated 2026-11-21 with queries recorded in the SEARCH/GATE 0 comments; the LineageOS manifests, torvalds sources and WHENCE were fetched as public text only. No proprietary payload was fetched, stored or committed - sizes, md5s, public-source quotations and arithmetic derivations only.

Nothing in this document is legal advice; no proprietary payload bytes were fetched, stored or committed.
