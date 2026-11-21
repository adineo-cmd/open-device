# motorola Moto_G30 (caprip) - `adsp` family status (37 rows - PRESENT, census-complete; SM6115-generation split-PIL audio-DSP image with the complete b00-b33 run minus structural b11 at e_phnum 35; fleet-wide servreg trio byte-identical to public linux-firmware manifests)

Analysis date: 2026-11-21. Analyst: ZC-1 (issue [#1276](https://github.com/adineo-cmd/open-device/issues/1276)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, feat/open-device-site d15a776), `upstream-contribution/blob-database/device-inventory.csv`, LineageOS `android_device_motorola_caprip` `proprietary-files.txt` (lineage-22.2 branch, fetched 2026-11-21), LineageOS wiki caprip page (fetched 2026-11-21), public spec pages (Qualcomm Snapdragon 662 product brief, 2026-11-21), linux-firmware WHENCE and the public builds `qcom/qcm2290/{adsp.mbn,adspr.jsn,adsps.jsn,adspua.jsn}` (git.kernel.org, fetched, md5-recorded and parsed 2026-11-21), sibling in-repo docs docs/devices/motorola/Moto_G10/adsp.md (#1258), docs/devices/xiaomi/Mi_A3/adsp.md (#1240) and docs/devices/motorola/Moto_G200/cdsp.md (#1270); torvalds/linux `sm6115.dtsi` / `qcom_q6v5_pas.c` line references cited from the #1258 fetch (2026-11-21). No device payload was fetched or committed; the only binaries inspected are the public linux-firmware QCM2290 builds (ELF header table) and the public JSON manifests. Every number is command output or a recorded fetch; sums re-verified with python3 this session.

**Verdict: the `adsp` family is PRESENT on Moto_G30 and the census is COMPLETE - 37 rows, 13,962,835 B, 37 distinct md5s, all db_type=MODEM, all at `motorola/caprip/modem/image`, priority P3.** The family is the signed split-PIL audio-DSP (ADSP) firmware image in Qualcomm's split-ELF convention, under the plain **`adsp`** name on this SM6115 (Snapdragon 662) device: `adsp.mdt` 9,420 B + 33 segment files `adsp.b00`-`adsp.b33` (13,952,052 B) + the 3-file servreg manifest trio (`adspr.jsn`, `adsps.jsn`, `adspua.jsn`, 1,363 B together). The b00-b33 range has exactly one gap, `adsp.b11`, and that gap is **structural, not a census gap**: the bengal-generation ADSP ELF declares program header 11 as a file-data-less (BSS-only) PT_LOAD - proven against the public linux-firmware QCM2290 build (re-parsed this session), established corpus-wide for all 10 bengal Moto devices in #1258 with Moto_G30 explicitly named - so no `adsp.b11` file exists to census. Two exact size laws fix the ELF skeleton: **e_phnum = 35** (`adsp.b00` = 1,172 = 52 + 32 x 35) and **mdt = b00 + b01** (1,172 + 8,248 = 9,420). The 37-row census is the complete shipped set.

## Device identity

| fact | value | source |
|---|---|---|
| model | Motorola Moto G30, XT2129 (family includes the K13 Pro variant; one shared LineageOS build) | LineageOS wiki caprip page (fetched 2026-11-21) [F]; public spec pages (2026-11-21) [F] |
| codename | `caprip` (db_path `motorola/caprip/...` and inventory `build_codename` agree) | db_path + device-inventory.csv [F]; LOS wiki caprip (2026-11-21) [F] |
| SoC | Qualcomm **SM6115 Snapdragon 662** (11 nm), Kryo 260 CPU, Adreno 610 GPU, Snapdragon X11 LTE modem | inventory cell [F]; public spec pages (2026-11-21) [F]. **The inventory SoC cell is CORRECT for this device** - unlike the known-wrong dubai/tundra cells flagged in #1270 |
| DSP | Hexagon 683 with Hexagon Vector eXtensions (HVX) and scalar accelerator; same DSP block as Snapdragon 460 | Qualcomm Snapdragon 662 product brief (fetched 2026-11-21) [F] |
| released | March 2021, shipped on Android 11 | public spec pages (fetched 2026-11-21) [F] |
| stock build | `caprip_retail S0RC32.41-10-19-25` | LineageOS caprip proprietary-files.txt header (lineage-22.2, fetched 2026-11-21) [F] |
| census scope | 232 rows in 9 families (other 57, modem 43, adsp 37, wifi 45, gpu 14, boot 8, cdsp 12, bt 11, tz 5); total 457,752,331 B | coverage-matrix.csv + device-inventory.csv [F]; family bytes and row counts sum to the inventory totals exactly (python, this session) |
| priority | P3 on all 37 adsp rows | coverage-matrix.csv [F] |

Inventory flags for the lead: (a) Moto_G30's accounting cells are internally consistent (count_csv_total 232 = sizes_rows = matrix rows; sizes_bytes 457,752,331 = family-byte sum) [F]; (b) `extract_status_22.2` = "fails" for caprip while the matrix carries a complete 232-row census - worth a data-hygiene look [F]; (c) the adspr.jsn share-fleet below again contains the two cells flagged in #1240/#1258 - OnePlus_7 is labeled "MSM8998 Snapdragon 835" but is SM8150 Snapdragon 855 per public specs, and Nord_CE3's cell carries a leading mojibake byte (re-citing, not re-deriving).

## Census evidence [F]

All 37 rows: `blob_subfamily` empty, `sha256_if_listed` empty, `isa_identified` empty, `interface_documented=n`, db_type `MODEM`, priority P3; 37 distinct md5s (no internal duplication). db_type=MODEM is genuinely accurate here (as in #1258) - the whole image ships in the modem partition (see packaging below).

| container | rows | bytes | db_path |
|---|---|---|---|
| split-PIL firmware (`adsp.mdt` + 33 `adsp.bNN`, b00-b33 minus b11) | 34 | 13,961,472 | `motorola/caprip/modem/image` |
| servreg manifest trio (`adspr.jsn`, `adsps.jsn`, `adspua.jsn`) | 3 | 1,363 | `motorola/caprip/modem/image` |
| total | 37 | 13,962,835 | - |

Verified decomposition: 9,420 (mdt) + 13,952,052 (33 bNN) + 1,363 (3 jsn: 403+405+555) = 13,962,835 (python, this session). Min segment 156 B (`adsp.b33`), max 6,488,516 B (`adsp.b24`, 46.47% of family bytes).

### Shell files (4)

| file | bytes | md5 | distinct devices sharing md5 |
|---|---|---|---|
| adsp.mdt | 9,420 | `7aa7254699272af1a40335e971cc9b34` | 1 (Moto_G30 only) |
| adspr.jsn | 403 | `40d6edf129dec063ca3fe6cb6837488f` | 30 |
| adsps.jsn | 405 | `c7253d84bff46e4cf5cb0585e9a851c5` | 24 |
| adspua.jsn | 555 | `d0bd5030a03f631c9af5060a5645d02e` | 30 |

### Segment files (33; b00-b33 minus b11)

`devices` = distinct corpus devices carrying that byte identity (md5 sweep over all 33,917 rows):

| file | bytes | md5 | devices |
|---|---|---|---|
| adsp.b00 | 1,172 | `b61c9daf37b916be5162f6c37e428276` | 1 |
| adsp.b01 | 8,248 | `5327854e892e6d4556f56c9da8e8b9a6` | 1 |
| adsp.b02 | 85,748 | `fc8fe209fc5c3d70de2d2fb4b1aa7f04` | 1 |
| adsp.b03 | 387,520 | `5f1c73010c9ae0170972276f4f2180fd` | 1 |
| adsp.b04 | 1,801,500 | `35296cb89fea72871a2bdbfab6ef1bee` | 1 |
| adsp.b05 | 1,696,204 | `a84a5e6f3bc9f1a84c134ea68fb2fd2f` | 1 |
| adsp.b06 | 2,896 | `afa6b60c3f5c0e92eec833cb369e3da7` | 1 |
| adsp.b07 | 17,352 | `ed4ce34d027e4fe6f62ad14079a46b42` | 3 (Moto_G30, Phone_1, Pro_1X) |
| adsp.b08 | 28,524 | `94a228a42bf7c67ef79b5d7eaea8dab2` | 1 |
| adsp.b09 | 4,828 | `e0c4328ed884fdc618c5c87ff810b691` | 1 |
| adsp.b10 | 260 | `481e6336d21dc05c578a65f3f4ed49d7` | 1 |
| adsp.b12 | 62,080 | `6b53ed89c11b2b46daba74f13dd4277e` | 1 |
| adsp.b13 | 72,968 | `ece89cceb379f9b3501959c501536f9c` | 1 |
| adsp.b14 | 364,544 | `0fc5a07c07fa1b2d7ee501808c856868` | 1 |
| adsp.b15 | 1,497,188 | `cfbcff5c6ae49ada89d975c2b573a866` | 1 |
| adsp.b16 | 28,676 | `54084a201ee8e914f91c8cc9c92874da` | 1 |
| adsp.b17 | 11,771 | `cd5437663d720d325105c667faf96210` | 8 (Defy_2021, Moto_G10, Moto_G30, Moto_G9, Moto_G9_Power, Moto_G_Power, Phone_1, Pro_1X) |
| adsp.b18 | 7,008 | `35c11334a6ffd806fe04c581db4e5a12` | 11 (9 Moto bengal devices + Phone_1 (SM7325) + Pro_1X (SM6115)) |
| adsp.b19 | 732 | `9619ba7401a98e5e8b5b8b1f687bcf42` | 3 (Defy_2021, Moto_G30, Moto_G9) |
| adsp.b20 | 7,776 | `317d4fd295409a80555c2cacf67f0319` | 1 |
| adsp.b21 | 28,444 | `3d914cc452231b32da8c076852c7da9f` | 1 |
| adsp.b22 | 272,012 | `aa8088b8000b9fb715053c508033935b` | 1 |
| adsp.b23 | 233,472 | `3ba61580ca6c62e034b0cc58e3e114e1` | 1 |
| adsp.b24 | 6,488,516 | `0ce9b2400fb2d01434f764ec035768b3` | 1 |
| adsp.b25 | 290,144 | `9e932e4d0febc4f8d12770456b344a70` | 1 |
| adsp.b26 | 2,960 | `0bafd0d1216fce4990bdaafb69aa03dc` | 1 |
| adsp.b27 | 97,800 | `693042e118624f1aadf8fb9ddcf0f8e7` | 1 |
| adsp.b28 | 283,156 | `e8b67963846fc90076b9ff37d257d412` | 9 (Defy_2021, Moto_G30, Moto_G32, Moto_G42, Moto_G52, Moto_G9, Moto_G9_Power, Moto_G_Power, Pro_1X) |
| adsp.b29 | 659 | `0117b62aa15a96d48dd21191c08c63e9` | 6 (Defy_2021, Moto_G30, Moto_G9, Moto_G9_Power, Moto_G_Power, Pro_1X) |
| adsp.b30 | 17,982 | `218aa9c22c24e6b81027ebbf886dc0d6` | 1 |
| adsp.b31 | 91,644 | `d2640eabb03febb1883685f6e62e3479` | 1 |
| adsp.b32 | 58,112 | `c30162eaf3c37334fa16dd458762fa44` | 1 |
| adsp.b33 | 156 | `24e1589311340ef5000591d0abf1f35d` | 1 |

28 of 34 ELF files (mdt + 27 segments) are Moto_G30-exclusive corpus-wide - device-signed firmware is not shared; only six small segments and the generic manifests cross device lines [F].

## Container layout - derived from two exact arithmetic laws plus a public generational witness

- **Law 1: `adsp.b00` = 1,172 = 52 + 32 x 35.** A little-endian ELF32 header is 52 B and each program header entry 32 B; program header 0 in Qualcomm split-ELF images is a self-referential segment holding the header table itself. So **caprip's ADSP ELF has e_phnum = 35** [F arithmetic; law established on the adsp family in #1258 and re-anchored below on the public QCM2290 build, whose phdr 0 = 1,012 B = 52 + 32 x 30 matches its parsed e_phnum of 30].
- **Law 2: mdt = b00 + b01 exactly: 1,172 + 8,248 = 9,420.** The mdt retains the header table (phdr 0) plus the hash/metadata segment (phdr 1); the kernel mdt loader reads the header size from phdrs[0].p_filesz and the hash table from the mdt itself (torvalds/linux `drivers/soc/qcom/mdt_loader.c` lines 183-210, cited via #1258). Note: this exact G30 arithmetic already appears as one of #1258's ten verified model checks; it is re-verified here directly from the caprip census rows.
- The kernel loader names split segments `b%02d` by **program-header index**, requests them only for PT_LOAD headers that are not the hash segment and only when `p_filesz > 0` (mdt_loader.c lines 84, 55-64, 413-423, cited via #1258) [F].
- **Public generational witness [F, parsed this session]:** linux-firmware `qcom/qcm2290/adsp.mbn` (WHENCE lines 7433-7434, Version ADSP.VT.5.4.1.c4-00013-KAMORTA-1; fetched 2026-11-21, md5 `4bd1f8342a7e5071295abf86b319dc28`, 12,826,756 B) parses as ELF32 LE, e_type 2 (EXEC), **e_machine 164 (EM_QUALCOMM_DSP6 / Hexagon QDSP6)**, e_entry 0x91a00000, e_flags 0x66, e_phnum 30: phdr 0 = 1,012 B header-table self-reference (type 0), phdr 1 = 7,856 B hash/metadata (type 0, flags 0x2200000), 28 file-backed PT_LOADs, **phdr 11 = PT_LOAD with p_filesz 0 and p_memsz 15,520 (BSS-only)**, and phdr 29 (last) = PT_LOAD p_filesz 0, p_memsz 3,575,808 (second, huge trailing BSS).
- **Five same-index size anchors [F rows + F public parse]:** the public build's file-backed phdr filesz values match caprip's census segment sizes exactly at the same program-header index for phdr 2 = `adsp.b02` (85,748), phdr 3 = `adsp.b03` (387,520), phdr 8 = `adsp.b08` (28,524), phdr 9 = `adsp.b09` (4,828) and phdr 10 = `adsp.b10` (260) - five exact anchors (python model comparison, this session). Per #1258, capri (Moto_G10) matched the same public build only at phdr 9/10, so caprip's drop is structurally closer to the public KAMORTA build at the low indices. Byte identities are NOT compared (the public build is a pil-squashed monolith, the census is a split set); sizes only [I on what the match implies].
- One cross-index size coincidence: the public build's phdr 20 = 11,771 B = the size of caprip's `adsp.b17`, whose bytes form the 8-device cohort that includes Phone_1 and Pro_1X (#1258 lists the same 8). Noted, not claimed as byte identity [I].
- **Boot-time request set [I]:** applying the loader rules to the derived roles, the kernel at boot would fetch only `adsp.b02`-`adsp.b33` minus b11 (31 files) - phdr 0's content rides in the mdt and phdr 1 is the hash segment; b00/b01 exist on the device filesystem because the packaging tool dumps every phdr, but are not fetched at boot.
- **Trailing phdr [I]:** e_phnum 35 spans phdrs 0-34; the census contains b00-b33 (phdrs 0-33) with no interior gap besides b11, so phdr 34 is the trailing file-less (BSS-only) segment - no `adsp.b34` exists to census (confirmed absent from the census, this session). Same rule as #1270's phdr 16 and #1258's phdr 32.
- **Platform fit [I]:** the 13,962,835 B image fits the sm6115.dtsi `pil_adsp_mem` carve-out of 0x2800000 = 41,943,040 B (40 MiB) with ample headroom.

## Why the "absent / census gap" alternative is ruled out

1. **The Task's 37 rows are confirmed** and form a complete, internally consistent image: e_phnum fixed at 35 by the b00 size law, so the segment range is b00-b33 (phnum-2); the only gap in that range is b11; exactly one file per remaining phdr; the expected set {b00..b33} minus {b11} matches the census **exactly, file for file** (python model check, this session).
2. **b11 is structural, not missing:** the public bengal-generation (SM4250/SM6115 family, KAMORTA) ADSP build has phdr 11 with p_filesz 0 (BSS-only), parsed this session; a filesz-0 PT_LOAD produces no `.bNN` file under the split convention (mdt_loader.c line 423) [F witness + I on caprip's own phdr 11]. #1258 establishes the corpus sweep: all 10 bengal Moto devices skip exactly b11 while spanning different phnum maxima, with **Moto_G30 b00-b33** explicitly named; 37 non-bengal corpus devices DO census `adsp.b11`/`adsp2.b11`.
3. **No packaging loss:** the LineageOS caprip manifest (lineage-22.2, blobs from the S0RC32.41-10-19-25 retail build) contains no adsp image files at all - the image ships in the modem partition and the census db_path `motorola/caprip/modem/image` records exactly that. The census is the only completeness witness for this family, and it is internally complete [F + I].

## Cross-corpus facts

- **The servreg trio is fleet-wide and byte-identical to the public manifests:** caprip's adspr.jsn/adspua.jsn md5s appear on 30 corpus devices each, adsps.jsn on 24 - and all three md5s **byte-match the public linux-firmware `qcom/qcm2290/{adspr,adsps,adspua}.jsn`** (fetched 2026-11-21, md5s `40d6edf129dec063ca3fe6cb6837488f` / `c7253d84bff46e4cf5cb0585e9a851c5` / `d0bd5030a03f631c9af5060a5645d02e`; WHENCE RawFile entries lines 7435-7437). Schema read this session from the public files (stdlib python3 -I): `sr_version` {major 1, minor 1, patch 1}; `sr_domain` {soc "msm", domain "adsp", qmi_instance_id 74}; subdomains adspr = "root_pd", adsps = "sensor_pd", adspua = "audio_pd"; `adspua.jsn` additionally declares the service pair {provider "avs", service "audio"}. This matches #1240's byte-verified schema exactly; the share-fleet lists in #1240/#1258 (30/24/30) are reproduced exactly from the caprip view [F].
- **Bengal row-count law [F + I]:** #1258 records the 10 bengal Moto adsp families at 35 (G10, Moto_E7_Plus), 36 (G32, G42, G52), 37 (G30) or 39 rows (G9, G9_Power, G_Power, Defy_2021). The caprip census adds the clean derivation: rows = phnum + 2 (phnum-2 segments after the structural b11 skip, + mdt, + 3 manifests): 35 + 2 = 37 for caprip (phnum 35), 33 + 2 = 35 for capri (phnum 33) - a pure phdr-count difference, not a census difference.
- **Sharing cohorts from the caprip view [F]:** `adsp.b18` (7,008 B) spans 11 devices = 9 Moto bengal devices + Phone_1 (SM7325) + Pro_1X (SM6115); `adsp.b17` (11,771 B) spans 8; `adsp.b28` (283,156 B) spans 9 devices **across three different segment indices** - b28 on caprip, b29 on Moto_G32/G42/G52 and Pro_1X, b30 on Moto_G9/G9_Power/G_Power and Defy_2021; `adsp.b29` (659 B) spans 6 across b29 (caprip) / b30 (Pro_1X) / b31 (G9 family, Defy_2021). The index shift tracks each build's phdr count - same payload, different phdr index [I on the mechanism].
- **Contrast cohorts within the fleet [F]:** caprip's `adsp.b07` (17,352 B) is shared only with Phone_1 and Pro_1X - capri's b07 (17,036 B) belongs to a different 5-device Moto cohort (#1258); caprip's `adsp.b19` (732 B) is shared with Defy_2021 and Moto_G9, while capri's b19 (732 B, different bytes) is shared with Phone_1 and Pro_1X. Same size anchors, per-build bytes.
- **G30-G10 byte sharing is exactly two segments plus the trio [F]:** b17 and b18 are byte-identical between caprip (`adsp.*`) and capri (`adsp2.*`), plus the three manifests. Everything else payload-bearing is device-unique.
- **adsp/adsp2 naming is a per-build packaging choice, not a SoC property [F rows, I on the conclusion, per #1258]:** caprip (SM6115) ships plain `adsp.*`; capri (SM4250) ships `adsp2.*`; Pro_1X (also SM6115) carries the shared bytes under BOTH names in the corpus.
- **Packaging [F]:** the LineageOS caprip manifest packages no adsp image files; the only adsp-related vendor file is `vendor/etc/acdbdata/adsp_avs_config.acdb` (audio calibration) - mirroring capri in #1258. With modem-partition shipping, a booted stock device exposes the image under the firmware mount of the modem partition (`image/adsp.*`), which is what the extraction corpus recorded as `motorola/caprip/modem/image` [I on the mount-point string].

## Interface and ISA facts

- **Mainline device tree [F, cited from the #1258 fetch of 2026-11-21]:** torvalds/linux `arch/arm64/boot/dts/qcom/sm6115.dtsi` declares `remoteproc_adsp: remoteproc@a400000` with compatible `qcom,sm6115-adsp-pas` (lines 2772-2800), memory-region `pil_adsp_mem` at 0x53800000 size 0x2800000 = 41,943,040 B (40 MiB), glink edge "lpass" with the apr audio service and a fastrpc node with compute-cb 3-7 (lines 2877-2912); `drivers/remoteproc/qcom_q6v5_pas.c` registers `qcom,sm6115-adsp-pas` (lines 2045-2047). For caprip this dtsi is the device's OWN SoC tree - Moto_G30 is a native SM6115 device, not an include-override like capri's sm4250.dtsi (which merely re-includes sm6115.dtsi and renames CPU compatibles, per #1258). No Motorola caprip board file exists upstream.
- **Downstream load chain [F, cited from #1258]:** Qualcomm's downstream `dsp/adsp-loader.c` (GPL-2.0) selects the firmware name from `adsp-fw-names` via the `adsp_variant` nvmem cell and calls `subsystem_get_with_fwname`; Motorola's bengal audio overlay on capri sets `adsp-fw-names = "adsp2"`. Caprip's build ships plain `adsp.*`, so its audio overlay/DT names the audio ADSP "adsp" - consistent with the census filenames, but the caprip DT string itself is unverified ([OPEN]; see negatives).
- **Firmware location [I]:** with modem-partition shipping, the extraction corpus records `motorola/caprip/modem/image`; the exact firmware mount-point string is inferred from the db_path, same caveat as #1258.
- **ISA [F + honest negative]:** the ADSP on SM6115 is Hexagon 683 with HVX (Qualcomm Snapdragon 662 product brief, fetched 2026-11-21); the executable format is Hexagon QDSP6 ELF - e_machine 164 confirmed on the public same-generation QCM2290 build parsed this session. The corpus records `isa_identified` EMPTY and `interface_documented=n` on all 37 rows - the segments are honestly un-RE'd here. By size the likely code/resource-bearing segments are b24 (6,488,516 B, 46.47%), b04 (1,801,500 B, 12.90%), b05 (1,696,204 B, 12.15%), b15 (1,497,188 B, 10.72%) and b03 (387,520 B, 2.78%) - together 85.02% of family bytes [I - no disassembly performed].
- **Prior RE art survey [F]:** web search (2026-11-21) finds generic Hexagon/QDSP6 RE resources (bkerler's QDSP reversing guide, programa-stic/hexag00n, Checkpoint DSP security research) but nothing targeting the Moto G30 / caprip adsp image; GitHub code search `caprip adsp` (excluding this repo) returns only device-tree/packaging manifests.

## Honest negatives ([OPEN])

- No payload of this device was fetched or analyzed (metadata-only; the 34 device-signed files exist in the corpus as hashes only). The only binaries touched are the four public linux-firmware QCM2290 files, and only the ELF header table and JSON manifest fields.
- The caprip phdr-level facts (e_phnum 35; phdr 11 BSS-only; phdr 34 trailing file-less) are derived from two exact size laws plus the public generational witness - not from caprip's own mdt bytes. A program-header dump of the real `adsp.mdt` remains the direct proof and is [OPEN].
- No Hexagon ISA proof from the blobs: no segment was disassembled; Hexagon 683 is from the SoC spec, e_machine 164 from the public build.
- The firmware-name string in caprip's downstream audio DT ("adsp" vs "adsp2") is inferred from the census filenames; MotorolaMobilityLLC's audio devicetree coverage for caprip was not located (code search surfaces only parrot/diwali overlays on the default branch) [OPEN].
- Which functionality lives in which segment is unknown; the 85.02% five-segment concentration is a size ranking, not a functional mapping [I].
- The 11,771 B cross-index size coincidence between the public build's phdr 20 and caprip's b17 is noted, not established as byte identity [I].
- `extract_status_22.2` = "fails" for caprip while a complete 232-row census exists - an accounting question for the lead, not resolved here.

## What would upgrade this finding

1. Extract the stock modem partition (fastboot image or OTA payload), byte-verify all 37 census md5s, and dump the ELF program headers of `adsp.mdt` (9,420 B): expect e_phnum 35, phdr 0 = 1,172 B header-table self-reference, phdr 1 = 8,248 B hash/metadata, phdr 11 with p_filesz 0/p_memsz near 15,520, phdr 34 trailing with p_filesz 0 - converting the structural derivations from [I] to direct [F].
2. Disassemble b24/b04/b05/b15 with a public Hexagon toolchain (Ghidra Hexagon module, a Capstone fork, or the LLVM Hexagon backend) and record the ISA revision - fills `isa_identified` on all 33 ELF segment rows.
3. Locate the caprip audio overlay in MotorolaMobilityLLC's public kernel-audio-devicetree branches (sm6115/RRCS31 line) to confirm `adsp-fw-names` for this build.
4. linux-firmware ships no SM6115/scuba ADSP drop (WHENCE grep, this session); if one lands, diff its segment table against caprip's sizes - the five same-index anchors (85,748 / 387,520 / 28,524 / 4,828 / 260) would sharpen into a full skeleton test.

## RULE 0 record

- CLAIM posted 2026-11-21T11:45:16Z as the first comment (confirmed first by re-read at 11:45:21Z; no competing claim).
- SEARCH (Gate -1) posted 2026-11-21; NO-PRIOR-ART (Gate 0) posted 2026-11-21; work started only after both.
- All census numbers are awk/python outputs on `upstream-contribution/blob-database/coverage-matrix.csv` at feat/open-device-site d15a776, this session; every sum and the expected-set model check re-verified with python3 before writing. Web fetches dated 2026-11-21: LineageOS wiki caprip page, LineageOS/android_device_motorola_caprip proprietary-files.txt (lineage-22.2), Qualcomm Snapdragon 662 product brief, linux-firmware WHENCE (line numbers 7432-7441 recorded per fetch), public builds `qcom/qcm2290/adsp.mbn` (md5 `4bd1f8342a7e5071295abf86b319dc28`) and `qcom/qcm2290/{adspr,adsps,adspua}.jsn` (md5s recorded above); ELF header parsing and JSON schema reads performed with stdlib `python3 -I` on the downloaded public files, header metadata and manifest fields only.

Nothing in this document is legal advice; no proprietary payload bytes were fetched, stored or committed - only sizes, md5s, ELF header metadata and JSON schema fields of public builds, public-source quotations and arithmetic derivations.
