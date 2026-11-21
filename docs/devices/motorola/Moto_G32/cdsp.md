# motorola Moto_G32 (devon) - `cdsp` family status (12 rows - PRESENT, census-complete; SM6225 split-PIL compute-DSP image at e_phnum 13 with BSS-only program headers 7 and 10 matching the public linux-firmware SM8250/QRB4210 skeleton file-for-file; `cdsp.b11` byte-identical across the 5-device SM6115/SM6225 cohort; 403 B servreg manifest byte-identical to the public build)

Analysis date: 2026-11-21. Analyst: ZC-1 (issue [#1288](https://github.com/adineo-cmd/open-device/issues/1288)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, feat/open-device-site e567696), `upstream-contribution/blob-database/device-inventory.csv`, LineageOS `android_device_motorola_devon` `proprietary-files.txt` (lineage-22.2 branch, fetched 2026-11-21), LineageOS wiki devon page (fetched 2026-11-21), public spec pages (Qualcomm Snapdragon 680 4G product brief; customrombay device page, 2026-11-21), TheMuppets `proprietary_vendor_motorola_sm6225-common` `sm6225-common-vendor.mk` (lineage-22.2, fetched 2026-11-21), LineageOS `android_kernel_motorola_sm6225` `drivers/soc/qcom/qdsp6v2/cdsp-loader.c` (lineage-22.2, fetched 2026-11-21), torvalds/linux master `arch/arm64/boot/dts/qcom/sm6115.dtsi`, `drivers/remoteproc/qcom_q6v5_pas.c`, `drivers/soc/qcom/mdt_loader.c` (fetched 2026-11-21; the qcom dtsi directory listing recorded - **no sm6225.dtsi exists upstream**), linux-firmware WHENCE (git.kernel.org, fetched 2026-11-21; line numbers recorded per fetch) plus the downloaded public builds `qcom/sm8250/{cdsp.mbn,cdspr.jsn}` (fetched, md5-recorded and ELF/JSON-parsed 2026-11-21), linux-msm/hexagon-dsp-binaries contents listing (2026-11-21), sibling in-repo docs docs/devices/motorola/Moto_G10/adsp.md (#1258), docs/devices/motorola/Moto_G30/adsp.md (#1276) and docs/devices/motorola/Moto_G200/cdsp.md (#1270). No device payload was fetched or committed; the only binaries inspected are the public linux-firmware CDSP build and manifest (ELF header table and JSON fields only). Every number is command output or a recorded fetch; sums re-verified with python3 this session.

**Verdict: the `cdsp` family is PRESENT on Moto_G32 and the census is COMPLETE - 12 rows, 3,208,499 B, 12 distinct md5s, 11 db_type=COMPUTE + 1 db_type=UNKNOWN, all at `motorola/devon/modem/image`, priority P3.** The family is the signed split-PIL compute-DSP (CDSP) firmware image in Qualcomm's split-ELF convention: `cdsp.mdt` 7,660 B + 10 segment files `cdsp.b00`-`cdsp.b11` minus `b07`/`b10` (3,200,436 B together) + the servreg manifest `cdspr.jsn` (403 B). Two exact size laws fix the ELF skeleton: **e_phnum = 13** (`cdsp.b00` = 468 = 52 + 32 x 13) and **mdt = b00 + b01** (468 + 7,192 = 7,660). The two interior gaps, `b07` and `b10`, are **structural, not census gaps**: the public linux-firmware SM8250 CDSP build, re-parsed this session, has e_phnum 13 with BSS-only (p_filesz 0) program headers at exactly {7, 10} plus a file-less trailing phdr 12 - devon's file set matches that skeleton file-for-file, and the shell sizes (phdr 0 = 468 B, phdr 1 = 7,192 B) match the public build exactly. There is no missing file to census; the 12-row census is the complete shipped set.

## Device identity

| fact | value | source |
|---|---|---|
| model | Motorola moto g32, XT2235-1/-2/-3 | LineageOS wiki devon page (fetched 2026-11-21) [F]; public spec pages (2026-11-21) [F] |
| codename | `devon` (db_path `motorola/devon/...`, inventory `build_codename`, LOS wiki agree) | db_path + device-inventory.csv [F]; LOS wiki (2026-11-21) [F] |
| SoC | Qualcomm **SM6225 Snapdragon 680 4G** (6 nm), Kryo 265 CPU (4x 2.4 GHz + 4x 1.9 GHz), Adreno 610 GPU | inventory cell [F]; LOS wiki (fetched 2026-11-21) [F]. **The inventory SoC cell is CORRECT for this device** - unlike the known-wrong dubai/tundra cells flagged in #1270 |
| Qualcomm platform name | `holi` per the customrombay devon page; Motorola's own tree is named `sm6225` (LineageOS kernel repo) | customrombay.org/motorola-devon (2026-11-21) [F]; LOS wiki [F] |
| DSP | Hexagon 686 DSP (SD680 4G product brief) | Qualcomm Snapdragon 680 4G product brief (fetched 2026-11-21) [F] |
| released | August 2022 | LOS wiki + public spec pages (fetched 2026-11-21) [F] |
| stock build | `devon_g T2SNS33.73-22-3-15` | LineageOS devon proprietary-files.txt header (lineage-22.2, fetched 2026-11-21) [F] |
| census scope | 232 rows in 9 families (other 52, modem 43, adsp 36, wifi 42, gpu 23, cdsp 12, boot 8, bt 11, tz 5); total 473,578,241 B | coverage-matrix.csv + device-inventory.csv [F]; family counts and byte total match the inventory cells exactly (python csv reader, this session) |
| priority | P3 on all 12 cdsp rows | coverage-matrix.csv [F] |

Inventory flags for the lead: (a) Moto_G32's accounting cells are internally consistent (count_csv_total 232 = matrix row count, sizes_bytes 473,578,241 = family-byte sum) [F]; (b) `extract_status_22.2` = "fails" for devon while the matrix carries a complete 232-row census - the same data-hygiene question already raised for capri/caprip/xpeng in #1258/#1276/#1270 [F].

## Census evidence [F]

All 12 rows: `blob_subfamily` empty, `sha256_if_listed` empty, `isa_identified` empty, `interface_documented=n`, priority P3; 12 distinct md5s (no internal duplication). db_type is COMPUTE on the 11 ELF files and UNKNOWN on the JSON manifest. The COMPUTE labels are corpus-accurate here - this family genuinely is the compute-DSP image, unlike the a660_gmu AUDIO mislabels (#946).

| container | rows | bytes | db_path |
|---|---|---|---|
| split-PIL firmware (`cdsp.mdt` + 10 `cdsp.bNN`, b00-b11 minus b07/b10) | 11 | 3,208,096 | `motorola/devon/modem/image` |
| servreg manifest (`cdspr.jsn`) | 1 | 403 | `motorola/devon/modem/image` |
| total | 12 | 3,208,499 | - |

Verified decomposition: 7,660 (mdt) + 3,200,436 (10 bNN) + 403 (jsn) = 3,208,499 (python, this session). Min segment 468 B (`cdsp.b00`), max 2,153,308 B (`cdsp.b05`, 67.11% of family bytes).

### Shell files (2)

| file | bytes | md5 | distinct devices sharing md5 |
|---|---|---|---|
| cdsp.mdt | 7,660 | `01c1fcaf860806abfb8a5a260e1a2720` | 1 (Moto_G32 only) |
| cdspr.jsn | 403 | `f2bd80d5f0b19b5b0d36d28383948149` | 30 (see cross-corpus section) |

### Segment files (10; b00-b11 minus b07/b10)

`devices` = distinct corpus devices carrying that byte identity (md5 sweep over all 33,917 rows):

| file | bytes | md5 | devices |
|---|---|---|---|
| cdsp.b00 | 468 | `b1a9ce0be2c3cac05890ee7119b93b31` | 3 (Moto_G32, Moto_G42, Moto_G52) |
| cdsp.b01 | 7,192 | `ac41f5b44213292418de6ebde1744202` | 1 |
| cdsp.b02 | 235,672 | `6f68425c3a32dc57b66986852144cb97` | 1 |
| cdsp.b03 | 106,620 | `0dedafaea7d83059735b71c4980746e3` | 1 |
| cdsp.b04 | 1,100 | `73d08353cdbecf61c195e7aecb0aafac` | 3 (Moto_G32, Moto_G42, Moto_G52) |
| cdsp.b05 | 2,153,308 | `ea4ea3f1735002b7f9f02fbe15c88409` | 1 |
| cdsp.b06 | 23,392 | `fc12d6cf4704812e90b0a5adaf874439` | 3 (Moto_G32, Moto_G42, Moto_G52) |
| cdsp.b08 | 611,192 | `dd3b4f5e20fd9a7d5e362817fda84084` | 1 |
| cdsp.b09 | 2,592 | `e539a392a553a10dca51fabf4b8a1932` | 1 |
| cdsp.b11 | 58,900 | `78fff93ab15fe4e4519cfe9c470d6463` | 5 (Moto_G30, Moto_G32, Moto_G42, Moto_G52, Pro_1X) |

7 of the 11 ELF files (mdt + b01, b02, b03, b05, b08, b09) are Moto_G32-exclusive corpus-wide - 3,124,236 B = 97.37% of family bytes. Device-signed firmware is not shared; only the three small SM6225-trio segments (b00/b04/b06, 24,960 B together), the cross-device b11 (58,900 B) and the generic manifest cross device lines [F].

## Container layout - two exact arithmetic laws plus a public generational witness

- **Law 1: `cdsp.b00` = 468 = 52 + 32 x 13.** A little-endian ELF32 header is 52 B and each program header entry 32 B; program header 0 in Qualcomm split-ELF images is a self-referential segment holding the header table itself. So **devon's CDSP ELF has e_phnum = 13** [F arithmetic; law established on the adsp family in #1258 and the cdsp family in #1270, re-anchored below on the public SM8250 build, whose phdr 0 = 468 B matches its parsed e_phnum of 13].
- **Law 2: mdt = b00 + b01 exactly: 468 + 7,192 = 7,660.** The mdt retains the header table (phdr 0) plus the hash/metadata segment (phdr 1); for split firmware the hash is found directly following the ELF header in the mdt (torvalds/linux `drivers/soc/qcom/mdt_loader.c` lines 150-154 and 183-210, fetched 2026-11-21) [F].
- The kernel loader names split segments `b%02d` by **program-header index** (mdt_loader.c line 84, `sprintf(... "b%02d", segment)`) and requests a split file only when the phdr's `p_filesz` is nonzero (caller lines 421-425; a filesz-0 phdr is zero-filled in place, lines 429-430) [F, fetched 2026-11-21]. A BSS-only phdr therefore produces **no** `.bNN` file.
- **Public generational witness [F, parsed this session with stdlib python3 -I]:** linux-firmware `qcom/sm8250/cdsp.mbn` (WHENCE lines 7521-7523, Version CDSP.HT.2.3.c1-00076-SM8250-1; fetched 2026-11-21, md5 `b60a1a6bfab3bc8c995b0aa5080c9b71`, 5,826,324 B) parses as ELF32 LE (`7f 45 4c 46`), e_type 2 (EXEC), **e_machine 164 (EM_QUALCOMM_DSP6 / Hexagon QDSP6)**, e_entry 0x87800000, e_flags 0x66, e_phentsize 32, e_ehsize 52, **e_phnum 13**. Full program-header table (all 13, parsed this session):

  | phdr | type | flags | p_filesz | p_memsz | role |
  |---|---|---|---|---|---|
  | 0 | 0 | 0x07000000 | 468 | 0 | header-table self-reference |
  | 1 | 0 | 0x02200000 | 7,192 | 8,192 | hash/metadata |
  | 2 | 1 | 0x08000005 | 235,420 | 720,896 | file-backed |
  | 3 | 1 | 0x08000005 | 105,980 | 106,496 | file-backed |
  | 4 | 1 | 0x08000005 | 1,076 | 4,096 | file-backed |
  | 5 | 1 | 0x08000007 | 2,532,972 | 4,947,968 | file-backed |
  | 6 | 1 | 0x08000006 | 83,426 | 86,016 | file-backed |
  | 7 | 1 | 0x08000004 | 0 | 425,984 | **BSS-only** |
  | 8 | 1 | 0x08000007 | 2,779,840 | 3,264,512 | file-backed |
  | 9 | 1 | 0x08000006 | 3,576 | 4,096 | file-backed |
  | 10 | 1 | 0x08000004 | 0 | 925,696 | **BSS-only** |
  | 11 | 1 | 0x08000007 | 59,156 | 274,432 | file-backed |
  | 12 | 1 | 0x08000007 | 0 | 10,211,328 | **BSS-only (trailing)** |

  This reproduces #1270's recorded parse exactly. The second witness, `qcom/qrb4210/cdsp.mbn` (WHENCE lines 7492-7494, Version CDSP.VT.2.4.1-00269-KAMORTA-1, md5 `6535ffeadeb1d4b9519762df56804594`), carries the same skeleton (e_phnum 13, phdr 0 = 468, phdr 1 = 7,192, BSS-only at {7, 10, trailing 12}) per #1270's parse [F cited].
- **Devon mapping [F rows + F public parse; I on the inference]:** devon's segment set {b00, b01, b02, b03, b04, b05, b06, b08, b09, b11} = the public build's file-backed phdrs {2, 3, 4, 5, 6, 8, 9, 11} plus the shell files - **exactly the public build's BSS-only phdrs {7, 10} with trailing phdr 12**. The shell sizes match the public drop exactly at phdr 0 (468) and phdr 1 (7,192), giving the identical 7,660 B mdt. Every file-backed payload size differs from the public drop (b02 235,672 vs 235,420; b03 106,620 vs 105,980; b04 1,100 vs 1,076; b05 2,153,308 vs 2,532,972; b06 23,392 vs 83,426; b08 611,192 vs 2,779,840; b09 2,592 vs 3,576; b11 58,900 vs 59,156) - a different drop of the same skeleton [I].
- **Boot-time request set [I]:** applying the loader rules, the kernel at boot fetches only `cdsp.b02`-`cdsp.b11` minus b07/b10 (8 files); phdr 0's content rides in the mdt and phdr 1 is the hash segment. b00/b01 exist on the device filesystem because the packaging tool dumps every phdr, but are not fetched at boot.
- **Platform fit [I]:** mainline has no sm6225.dtsi (see interface section), so devon's own carve-out is not documented upstream; the nearest mainline relative sm6115.dtsi reserves `pil_cdsp_mem` at 0x51a00000, size 0x1e00000 = 31,457,280 B (30 MiB) - the 3,208,096 B devon image fits with ample headroom.

## Why the "absent / census gap" alternative is ruled out

1. **The Task's 12 rows are confirmed** and form a complete, internally consistent image: phdr count fixed at 13 by the b00 size law, so the file range is b00-b11 (phdrs 0-11) with a file-less trailing phdr 12 (no `cdsp.b12` can exist); the interior gaps are {7, 10}; the expected shipped set {b00..b11} minus {b07, b10} matches the census **exactly, file for file** (python model check, this session).
2. **The gaps are structurally explained:** the public SM8250 CDSP build has BSS-only phdrs at exactly {7, 10} in a phnum-13 table (parsed this session; qrb4210 corroborates per #1270). A filesz-0 phdr produces no split file under the kernel loader rules [F witness + I on devon's own phdrs].
3. **No packaging loss:** the LineageOS devon manifest (lineage-22.2, blobs from the T2SNS33.73-22-3-15 retail build) contains no cdsp lines at all (grep, fetched 2026-11-21) - the image ships in the modem partition, and the census db_path `motorola/devon/modem/image` records exactly that. The sm6225-common vendor manifest likewise packages only userspace CDSP components (`vendor.qti.cdsprpc-service.rc`, `libcdsprpc`, `libcdsp_default_listener`, `cdsprpcd`) and no firmware files [F]. The census is the only completeness witness for this family, and it is internally complete [F + I].
4. **Contrast that motivates the check:** 3 corpus devices DO show a cdsp census gap - Pixel_4A_5G/Pixel_5/Pixel_5A carry a single 1-row cdsp family (Pixel_5/redfin: only `cdsp.mdt` 7,660 B at `google/redfin/vendor/firmware`, no segments, no manifest) [F, established in #1270]. Moto_G32 is not in that state: all 11 expected ELF members plus the manifest are present.

## Cross-corpus facts

- **The servreg manifest is fleet-wide and byte-identical to the public build:** devon's `cdspr.jsn` (403 B, `f2bd80d5f0b19b5b0d36d28383948149`) appears on 30 corpus devices (Defy_2021, Edge_30_Neo, FP4, G_Stylus_5G-2-2022, Mi_A3, Moto_E7_Plus, Moto_G10, Moto_G30, Moto_G32, Moto_G34_5G, Moto_G42, Moto_G52, Moto_G_5G_2024, Moto_G82_5G, Moto_G84_5G, Moto_G9, Moto_G9_Power, Moto_G_Power, Moto_G_Stylus_5G, Nord_CE2, Nord_CE3, OnePlus_7, OnePlus_7_Pro, OnePlus_7T, OnePlus_7T_Pro, OnePlus_8, OnePlus_8_Pro, Pro_1X, Realme_9_Pro, Realme_10_Pro) - and that md5 **byte-matches the public linux-firmware `qcom/sm8250/cdspr.jsn`** (fetched 2026-11-21, md5 re-verified this session; #1270 records the same bytes for `qcom/qrb4210/cdspr.jsn`). Schema read this session from the public file (stdlib python3 -I): `sr_version` {major 1, minor 1, patch 1}; `sr_domain` {soc "msm", domain "cdsp", subdomain "root_pd", qmi_instance_id 76}; `sr_service` [{provider "tms", service "servreg", service_data_valid 0, service_data 0}] - matching #1270's byte-verified schema exactly [F].
- **One manifest per cdsp image corpus-wide** - no device anywhere in the 33,917-row corpus carries `cdspua.jsn`/`cdsps.jsn`, consistent with the schema declaring only root_pd (contrast the adsp family's three-file trio) [F, established in #1270].
- **`cdsp.b11` is byte-identical across the 5-device SM6115/SM6225 cohort [F]:** Moto_G30 (caprip, SM6115), Moto_G32 (devon, SM6225), Moto_G42 (hawao, SM6225), Moto_G52 (rhode, SM6225) and Pro_1X (fxtec/pro1x, SM6115 per its mainline device tree `sm6115-fxtec-pro1x.dts`) all carry the same 58,900 B bytes at `modem/image` db paths. Size-identical across all five of those devices: b00 468, b01 7,192, b02 235,672, b03 106,620, b11 58,900 plus the 403 B manifest [F].
- **SM6225 trio byte cohort [F]:** devon, hawao and rhode (all SM6225, all shipped 2022) share b00 (468 B), b04 (1,100 B) and b06 (23,392 B) byte-identically; hawao+rhode additionally share b02 (235,672 B) and b03 (106,620 B) bytes. Devon's payload-bearing files (mdt, b01, b02, b03, b05, b08, b09) are corpus-exclusive to it.
- **Two payload generations under one skeleton [F rows, I on the generational reading]:** within the 5-device b11 cohort the remaining segment sizes split cleanly - the SM6115-generation builds (caprip, pro1x) carry b04 1,068 / b05 2,447,100-2,443,004 / b06 23,392-23,212 / b08 103,812 / b09 280, while the SM6225 builds (devon, hawao, rhode) carry b04 1,100 / b05 2,153,308 / b06 23,392 / b08 611,192 / b09 2,592. Cross-generation byte shares exist at the low indices: caprip and pro1x share b04 bytes (1,068 B, `c69dd780...`, also carried by Moto_G10's cdsp.b04) and b09 bytes (280 B, `7f6d0249...`) [F].
- **Index-shift contrast with the SM4250 generation [F rows + I on the mechanism]:** Moto_G10 (capri, SM4250) carries an 11-row cdsp set {b00-b06, b08, b10} at phnum 12 (b00 = 436 = 52 + 32 x 12; mdt = 436 + 7,144 = 7,580, python-verified) with gaps {7, 9}; its 58,900 B segment sits at index **b10** with different bytes (md5 `063e55ea48ffe7baaab4d35b829c7926`). The 12-row phnum-13 builds (devon, caprip, hawao, rhode, pro1x, OnePlus_8/8_Pro per #1270) have one more file-backed segment (b09) than the SM4250 build - same 58,900 B payload size, different phdr index and bytes.
- **Row-count distribution [F, established in #1270, 12-row list re-verified this session]:** 12 rows on 19 corpus devices (devon among them), 11 rows on 11 devices (SM4250 Moto fleet + OnePlus_7 generation), 1 row on the 3 Pixel devices (real census gaps).
- **adsp/cdsp contrast on this very device [F]:** devon's `adsp` family (36 rows) has **no** `adsp.b11` - the bengal/holi-generation ADSP ELF declares phdr 11 BSS-only (structural b11 skip, #1258/#1276, with G32's adsp.b00 1,140 = phnum 34). The CDSP image carries `cdsp.b11` - different program-header geometry per image, proving the b11 skip is per-ELF, not per-device or per-census.

## Interface and ISA facts

- **Downstream load chain [F]:** Motorola's sm6225 kernel (LineageOS `android_kernel_motorola_sm6225`, lineage-22.2, kernel 4.19 per LOS wiki) carries the downstream CDSP stack: `drivers/soc/qcom/qdsp6v2/cdsp-loader.c` line 81 calls `subsystem_get("cdsp")` (fetched 2026-11-21) - the downstream PIL resolves subsystem name "cdsp" to `cdsp.mdt` in the modem firmware directory, whose split segments are the census filenames. Code search over the same tree (2026-11-21) additionally shows `cdsprm.c` (CDSP resource manager), `governor_cdsp_l3.c` (CDSP L3 devfreq), `msm_isense_cdsp.c` (CDSP thermal) and `fastcvpd.c` (FastCV personalization driver - a fastrpc CDSP consumer).
- **Userspace fastrpc interface [F]:** the sm6225-common vendor manifest packages `libcdsprpc`, `libcdsp_default_listener`, `cdsprpcd` and `vendor.qti.cdsprpc-service.rc` (TheMuppets sm6225-common-vendor.mk, lineage-22.2, fetched 2026-11-21) - the standard QTI compute-DSP fastrpc userspace, confirming the CDSP is a live fastrpc compute target on this device.
- **Mainline support state [F + honest negative]:** torvalds/linux master has **no sm6225.dtsi at all** (qcom dtsi directory listing + 404 on the file, fetched 2026-11-21) - SM6225 has no upstream SoC tree, hence no mainline CDSP remoteproc node for devon. The nearest mainline relative `sm6115.dtsi` declares `remoteproc_cdsp: remoteproc@b300000` with compatible `qcom,sm6115-cdsp-pas` (lines 2914-2936), memory-region `pil_cdsp_mem` at 0x51a00000 size 0x1e00000 (30 MiB), glink edge "cdsp" (remote-pid 5) with a fastrpc node carrying compute-cb 1-6 (lines 2938-2984); `drivers/remoteproc/qcom_q6v5_pas.c` registers `qcom,sm6115-cdsp-pas` (line 2046) with `cdsp_resource_init` (lines 1228-1236): `firmware_name = "cdsp.mdt"`, **pas_id 18**, crash_reason_smem 601, `auto_boot = true`, ssr/sysmon name "cdsp", ssctl_id 0x17 [F, fetched 2026-11-21]. For caprip (G30, SM6115) this is the device's own SoC node; for devon it is the nearest-generation analogue only [I on the analogy].
- **Firmware location [I]:** with modem-partition shipping, a booted stock device exposes the image under the firmware mount of the modem partition (`image/cdsp.mdt` + `image/cdsp.bNN` + `image/cdspr.jsn`), which is what the extraction corpus recorded as `motorola/devon/modem/image`; the exact mount-point string is inferred from the db_path, same caveat as #1258/#1270.
- **ISA [F + honest negative]:** the compute DSP on SM6225 is Hexagon 686 (Qualcomm Snapdragon 680 4G product brief, fetched 2026-11-21); the executable format is Hexagon QDSP6 ELF - e_machine 164 confirmed on the public SM8250 build parsed this session. The corpus records `isa_identified` EMPTY and `interface_documented=n` on all 12 rows - the segments are honestly un-RE'd here. By size the likely code/resource-bearing segments are b05 (2,153,308 B, 67.11%) and b08 (611,192 B, 19.05%) - together 86.16% of family bytes [I - no disassembly performed].
- **Prior RE art survey [F]:** web search (2026-11-21) finds generic Hexagon/QDSP6 RE resources (programa-stic/hexag00n, bkerler's QDSP reversing guide, 2025 LibAFL/QEMU-Hexagon baseband fuzzing) but nothing targeting the Moto G32 / devon or any holi CDSP image; the public linux-msm/hexagon-dsp-binaries archive carries no holi/SM6225 directory at all (contents listing, 2026-11-21); GitHub code search for `SM6225 cdsp fastrpc` (excluding this repo) returns only vendor packaging manifests and device trees.

## Honest negatives ([OPEN])

- No payload of this device was fetched or analyzed (metadata-only; the 11 device-signed files exist in the corpus as hashes only). The only binaries touched are the public linux-firmware `qcom/sm8250/{cdsp.mbn,cdspr.jsn}`, and only the ELF header table and JSON manifest fields.
- The devon phdr-level facts (e_phnum 13; BSS-only phdrs 7 and 10; file-less trailing phdr 12) are derived from two exact size laws plus the public generational witness - not from devon's own mdt bytes. A program-header dump of the real `cdsp.mdt` (7,660 B) remains the direct proof and is [OPEN].
- The generational reading of the payload sizes (SM6115-gen vs SM6225-gen drops under one skeleton) is [I] - no functional evidence distinguishes the two clusters.
- No Hexagon ISA proof from the blobs: no segment was disassembled; Hexagon 686 is from the SoC spec, e_machine 164 from the public build.
- Whether the SM6225 CDSP build's BSS-only phdrs have the same p_memsz profile as the public SM8250 build (425,984 / 925,696 / 10,211,328) is unknowable without devon's mdt bytes [I].
- The downstream device-tree CDSP node for devon/hlt (memory-region carve-out size, fastrpc compute-cb count) was not extracted from the Motorola sm6225 kernel tree; only the loader's firmware-name string was cited [OPEN].
- Which functionality lives in which segment is unknown; the 86.16% two-segment concentration is a size ranking, not a functional mapping [I].
- `extract_status_22.2` = "fails" for devon while a complete 232-row census exists - an accounting question for the lead, not resolved here (re-citing the sibling flag from #1258/#1276/#1270).

## What would upgrade this finding

1. Extract the stock modem partition (fastboot image or OTA payload), byte-verify all 12 census md5s, and dump the ELF program headers of `cdsp.mdt` (7,660 B): expect e_phnum 13, phdr 0 = 468 B header-table self-reference, phdr 1 = 7,192 B hash/metadata, phdr 7 and phdr 10 with p_filesz 0, phdr 12 trailing with p_filesz 0 - converting the structural derivations from [I] to direct [F].
2. Disassemble b05/b08 with a public Hexagon toolchain (Ghidra Hexagon module, a Capstone fork, or the LLVM Hexagon backend) and record the ISA revision - fills `isa_identified` on all 11 ELF rows.
3. Fetch the devon/hlt downstream DT from `android_kernel_motorola_sm6225` and record the CDSP node's memory-region carve-out and fastrpc compute-cb range.
4. linux-firmware ships no holi/SM6225 CDSP drop today (WHENCE grep, 2026-11-21) and hexagon-dsp-binaries has no holi directory; if one lands, diff its segment table against devon's sizes (the shell anchors 468 / 7,192 / 7,660 and the gap set {7, 10} would sharpen the skeleton test).
5. The 58,900 B `cdsp.b11` is the single largest cross-device byte share in this family (5 devices across two SoC generations); a targeted RE pass on that one segment (public, from any device whose payload is accessible) would identify what payload is fleet-shared here.

## RULE 0 record

- CLAIM posted 2026-11-21T12:21:49Z as the first comment (confirmed first by re-read at 12:21:55Z; no competing claim).
- SEARCH (Gate -1) posted 2026-11-21; NO-PRIOR-ART (Gate 0) posted 2026-11-21; work started only after both.
- All census numbers are awk/python outputs on `upstream-contribution/blob-database/coverage-matrix.csv` at feat/open-device-site e567696, this session; every sum, the two size laws and the expected-set model check re-verified with python3 before writing. Web fetches dated 2026-11-21: LineageOS wiki devon page, LineageOS/android_device_motorola_devon proprietary-files.txt (lineage-22.2), TheMuppets sm6225-common-vendor.mk (lineage-22.2), LineageOS/android_kernel_motorola_sm6225 cdsp-loader.c (lineage-22.2), torvalds/linux master `sm6115.dtsi` + `qcom_q6v5_pas.c` + `mdt_loader.c` (line numbers recorded per fetch) and the qcom dtsi directory listing, linux-firmware WHENCE (qrb4210 lines 7492-7494, sm8250 lines 7521-7523 recorded per fetch), public builds `qcom/sm8250/cdsp.mbn` (md5 `b60a1a6bfab3bc8c995b0aa5080c9b71`) and `qcom/sm8250/cdspr.jsn` (md5 `f2bd80d5f0b19b5b0d36d28383948149`); ELF header parsing and JSON schema read performed with stdlib `python3 -I` on the downloaded public files, header metadata and manifest fields only.

Nothing in this document is legal advice; no proprietary payload bytes were fetched, stored or committed - only sizes, md5s, ELF header metadata and JSON schema fields of public builds, public-source quotations and arithmetic derivations.
