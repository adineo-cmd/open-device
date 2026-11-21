# motorola Moto_G200 (xpeng) - `cdsp` family status (18 rows - PRESENT, census-complete; SM8350-generation split-PIL compute-DSP image with a complete b00-b15 segment run at e_phnum 17; two-generation servreg manifest split pinned to public linux-firmware bytes)

Analysis date: 2026-11-21. Analyst: ZC-1 (issue [#1270](https://github.com/adineo-cmd/open-device/issues/1270)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, feat/open-device-site 086491d), `upstream-contribution/blob-database/device-inventory.csv`, LineageOS `android_device_motorola_xpeng` `proprietary-files.txt` (lineage-24.0 branch, fetched 2026-11-21), LineageOS wiki pages xpeng + xpeng/variant1 + dubai (fetched 2026-11-21), Motorola support spec page and /e/OS device page xpeng (fetched 2026-11-21), torvalds/linux master `arch/arm64/boot/dts/qcom/sm8350.dtsi` and `drivers/remoteproc/qcom_q6v5_pas.c` (fetched 2026-11-21), linux-firmware WHENCE (git.kernel.org, fetched 2026-11-21; line numbers recorded per fetch) plus the downloaded public builds `qcom/sm8250/{cdsp.mbn,cdspr.jsn}` and `qcom/qrb4210/{cdsp.mbn,cdspr.jsn}` (fetched, md5-recorded and parsed 2026-11-21), public Hexagon RE survey (web search, 2026-11-21), sibling in-repo docs docs/devices/motorola/Moto_G10/adsp.md (#1258) and docs/devices/xiaomi/Mi_A3/adsp.md (#1240). No device payload was fetched or committed; the only binaries inspected are the public linux-firmware CDSP builds (ELF header tables) and the public 403-byte JSON manifest. Every number is command output or a recorded fetch; sums re-verified with python3 this session.

**Verdict: the `cdsp` family is PRESENT on Moto_G200 and the census is COMPLETE - 18 rows, 5,993,435 B, 18 distinct md5s, 17 db_type=COMPUTE + 1 db_type=UNKNOWN, all at `motorola/xpeng/modem/image`, priority P3.** The family is the signed split-PIL compute-DSP (CDSP) firmware image in Qualcomm's split-ELF convention: `cdsp.mdt` 7,980 B + a COMPLETE segment run `cdsp.b00`-`cdsp.b15` (16 files, 5,984,942 B) + the servreg manifest `cdspr.jsn` (513 B). The two exact size laws established in #1258 give **e_phnum = 17** (`cdsp.b00` = 596 = 52 + 32 x 17) and **mdt = b00 + b01** (596 + 7,384 = 7,980). Because the b00-b15 run is complete with no interior gap, no interior program header is file-less: the only file-less program header is the trailing one (phdr 16) [I - derived, see layout section]. There is no missing file to census; the 18-row census is the complete shipped set.

## Device identity

| fact | value | source |
|---|---|---|
| model | Motorola moto g200 5G, XT2175-1; sold in China as Edge S30 (same hardware) | LineageOS wiki xpeng/variant1 (fetched 2026-11-21) [F]; Motorola support spec page (fetched 2026-11-21) [F] |
| codename | `xpeng` (db_path `motorola/xpeng/...`, LineageOS wiki, /e/OS device page - all agree) | db_path [F]; LOS wiki + /e/OS (2026-11-21) [F] |
| SoC | Qualcomm **SM8350-AC Snapdragon 888+** (5 nm), Kryo 680 CPU, Adreno 660 GPU | LineageOS wiki variant1 "Qualcomm SM8350-AC Snapdragon 888+" (fetched 2026-11-21) [F]; inventory cell agrees - **CORRECT for this device**, unlike the known-wrong dubai/tundra cells re-flagged below |
| DSP | Hexagon 780 (Qualcomm 6th-gen AI Engine marketing name for SM8350); Hexagon toolchain arch v68 for this generation | public spec pages (fetched 2026-11-21) [F] |
| released | announced November 2021; launched on Android 11 | LOS wiki variant1 [F]; Motorola support page [F] |
| stock build | `xpeng_g-user 12 S1RXS32.50-13-25 5fb68-c44485 release-keys` (RETEU variant) | LineageOS xpeng proprietary-files.txt header (fetched 2026-11-21) [F] |
| mainline LOS | official LineageOS device, currently 24.0, kernel 5.4 | LOS wiki variant1 (fetched 2026-11-21) [F] |
| census scope | 651 rows in 9 families (other 238, wifi 188, tz 95, modem 38, adsp 35, gpu 28, cdsp 18, boot 10, bt 1); total 833,798,522 B | coverage-matrix.csv + device-inventory.csv [F] |
| priority | P3 on all 18 cdsp rows | coverage-matrix.csv [F] |

Inventory flags for the lead: (a) Moto_G200's own cells are internally consistent (count_csv_total 651 = matrix row count, sizes_bytes 833,798,522, extract_status_22.2 "fails") [F]; (b) re-flagging the sibling cells used in the md5 cohorts below: Edge_30/dubai is listed "Qualcomm SM7250 Snapdragon 765G" but the LOS wiki (XT2203-1) says **SM7325-AE Snapdragon 778G+ 5G** [F], Edge_30_Fusion/tundra carries the same wrong SM7250 cell but is SM8350-AC per the established loop correction, and OnePlus_9, OnePlus_12, OnePlus_13, FP6, Mi_13, Nord_4 and Redmi_K60_Pro have EMPTY SoC cells [F].

## Census evidence [F]

All 18 rows: `blob_subfamily` empty, `sha256_if_listed` empty, `isa_identified` empty, `interface_documented=n`, priority P3; 18 distinct md5s (no internal duplication); db_type COMPUTE on the 17 ELF files and UNKNOWN on the JSON manifest.

| container | rows | bytes | db_path |
|---|---|---|---|
| split-PIL firmware (`cdsp.mdt` + 16 `cdsp.bNN`, b00-b15 complete) | 17 | 5,992,922 | `motorola/xpeng/modem/image` |
| servreg manifest (`cdspr.jsn`) | 1 | 513 | `motorola/xpeng/modem/image` |
| total | 18 | 5,993,435 | - |

Verified decomposition: 7,980 (mdt) + 5,984,942 (16 bNN) + 513 (jsn) = 5,993,435 (python, this session). Min segment 596 B (`cdsp.b00`), max 2,739,464 B (`cdsp.b10`, 45.71% of family bytes).

### Shell files (2)

| file | bytes | md5 | distinct devices sharing md5 |
|---|---|---|---|
| cdsp.mdt | 7,980 | `fe3d9df0bf47eca1dc6d905be23d8bf1` | 1 (Moto_G200 only) |
| cdspr.jsn | 513 | `49003ffcd10ec16dee11caad22b11b42` | 30 (see cross-corpus section) |

### Segment files (16; b00-b15, no gaps)

`devices` = distinct corpus devices carrying that byte identity (md5 sweep over all 33,917 rows):

| file | bytes | md5 | devices |
|---|---|---|---|
| cdsp.b00 | 596 | `1173b670f0d11f59dc9e0276f6ce72aa` | 1 |
| cdsp.b01 | 7,384 | `3c8fa0473658334b55e2946d07eb4f45` | 1 |
| cdsp.b02 | 8,584 | `26ff37a2b3eb47d783abf391b1df932d` | 5 (Moto_G200, Edge_30_Fusion, OnePlus_9, OnePlus_9_Pro, OnePlus_9RT) |
| cdsp.b03 | 1,070,949 | `e48791ce55177cb5e2ad62a29e7fc3ca` | 1 |
| cdsp.b04 | 1,172 | `8e6e0a93ca7899a8c2c9d8e01f63a856` | 5 (same cohort as b02) |
| cdsp.b05 | 1,096 | `b8d1ab1b557fc1b98f9110e8880cfede` | 5 (same cohort as b02) |
| cdsp.b06 | 1,819,812 | `a3609791e8ef804d6514e86084703123` | 1 |
| cdsp.b07 | 106,288 | `515f673edcffd026359ba2cb3ab6dca4` | 1 |
| cdsp.b08 | 840 | `d29b65ae5edc28a3d043ad1c1430d929` | 1 |
| cdsp.b09 | 91,073 | `2670f6c0bde7155840fff3ea37346741` | 1 |
| cdsp.b10 | 2,739,464 | `274c615bcb48313bc7d101d2ef7860ab` | 1 |
| cdsp.b11 | 60,488 | `de206d1a6a5b0446dae5b2eb06413c77` | 1 |
| cdsp.b12 | 3,648 | `75e5db87cf81ef4b4b7425bca69695e4` | 1 |
| cdsp.b13 | 63,792 | `e07854a9078f5c3c9eaf273da979bd82` | 1 |
| cdsp.b14 | 1,564 | `7d54d10fe4b371f7a35b08b2657cafbc` | 1 |
| cdsp.b15 | 8,192 | `135c3335c214ec46534e1e15af410e10` | 1 |

14 of 17 ELF files (mdt + b00, b01, b03, b06-b15) are Moto_G200-exclusive corpus-wide - device-signed firmware is not shared; only three small low-index segments and the generic manifest cross device lines [F].

## Container layout - two exact size laws plus public generational witnesses

- **Law 1: `cdsp.b00` = 596 = 52 + 32 x 17.** A little-endian ELF32 header is 52 B and each program header entry 32 B; program header 0 in Qualcomm split-ELF images is a self-referential segment holding the header table itself. So **xpeng's CDSP ELF has e_phnum = 17** [F arithmetic; law established on the adsp family in #1258 and re-anchored below on public CDSP builds].
- **Law 2: mdt = b00 + b01 exactly: 596 + 7,384 = 7,980.** The mdt retains the header table (phdr 0) plus the hash/metadata segment (phdr 1); the kernel mdt loader reads the header size from phdrs[0].p_filesz and the hash table from the mdt itself (torvalds/linux `drivers/soc/qcom/mdt_loader.c`, lines 183-210, cited via #1258) [F].
- The loader names split segments `b%02d` by program-header index, requests them only for PT_LOAD headers that are not the hash segment and only when `p_filesz > 0` (mdt_loader.c, lines 84, 55-64, 413-423, cited via #1258) [F].

**Public generational witnesses (both parsed this session, stdlib python3 -I, ELF header table only):**

- `qcom/sm8250/cdsp.mbn` (WHENCE lines 7521-7523, Version CDSP.HT.2.3.c1-00076-SM8250-1; 5,826,324 B; md5 `b60a1a6bfab3bc8c995b0aa5080c9b71`): ELF32 LE, e_type 2 (EXEC), **e_machine 164 (EM_QUALCOMM_DSP6 / Hexagon QDSP6)**, e_entry 0x87800000, e_flags 0x66, **e_phnum 13**: phdr 0 = 468 B header-table self-reference (type 0, = 52 + 32 x 13), phdr 1 = 7,192 B hash/metadata (type 0), 8 file-backed PT_LOADs, and **BSS-only PT_LOADs (p_filesz 0, p_memsz > 0) at phdr 7 (p_memsz 425,984), phdr 10 (925,696) and phdr 12 (10,211,328 - huge trailing BSS)** [F, parsed 2026-11-21].
- `qcom/qrb4210/cdsp.mbn` (WHENCE lines 7492-7494, Version CDSP.VT.2.4.1-00269-KAMORTA-1; 3,008,020 B; md5 `6535ffeadeb1d4b9519762df56804594`): same skeleton - ELF32 LE, e_machine 164, e_entry 0x53500000, e_flags 0x66, e_phnum 13, phdr 0 = 468 B, phdr 1 = 7,192 B, BSS-only at phdr 7 (851,968), 10 (696,320), 12 (23,842,816 trailing) [F, parsed 2026-11-21].
- WHENCE (lines 7597-7598, the block covering the qrb4210/sdm845/sm8250-era files) records that `cdsp.mbn` was **converted from split firmware `21-cdsp_split/firmware/cdsp.*` using github.com/andersson/pil-squasher** - public confirmation that the CDSP image ships and travels as a split mdt+bNN set [F].

**Corpus-public correspondence (end-to-end validation of the bookkeeping, no xpeng bytes needed):** OnePlus_8 and OnePlus_8_Pro (SM8250) census 12 cdsp rows each: `cdspr.jsn` 403 B whose md5 `f2bd80d5f0b19b5b0d36d28383948149` is **byte-identical to BOTH downloaded public manifests** (`qcom/sm8250/cdspr.jsn` and `qcom/qrb4210/cdspr.jsn`), `cdsp.mdt` 7,660 B (= 468 + 7,192 by Law 2), and the segment set {b00, b01, b02, b03, b04, b05, b06, b08, b09, b11} = b00-b11 minus {b07, b10} - **exactly the public build's BSS-only phdrs {7, 10} with trailing phdr 12**; b00 468, b01 7,192, b02 235,420, b03 105,980, b04 1,076, b06 83,426 and b11 59,156 match the public build's phdr filesz values exactly, while b05 (2,803,308 vs 2,532,972), b08 (830,592 vs 2,779,840) and b09 (2,800 vs 3,576) differ in size - a different drop of the same skeleton [F rows + F public parse].

**xpeng derivation [I]:** e_phnum 17 spans phdrs 0-16; the census contains b00-b15 with no interior gap, so every interior phdr is file-backed in this build; phdr 1 is the hash segment (its 7,384 B ride in the mdt) and phdr 16 is the trailing file-less (BSS-only) segment - no `cdsp.b16` exists to census. Applying the loader rules, the kernel at boot requests only `cdsp.b02`-`cdsp.b15` (14 files); b00/b01 exist on the filesystem because the packaging tool dumps every phdr, but are not fetched at boot [I - same reasoning as #1258].

**Platform fit [I]:** the 5,993,435 B image fits the sm8350.dtsi `pil_cdsp_mem` carve-out of 0x1e00000 = 31,457,280 B (30 MiB) with ample headroom.

## Why the "absent / census gap" alternative is ruled out

- The Task's 18 rows are confirmed, and the family is a complete, internally consistent image: phdr count fixed at 17 by the b00 size law, so `b16`+ cannot exist; b00-b15 present with zero interior gaps; exactly one manifest (`cdspr.jsn`) - the corpus-wide cdsp convention (no device anywhere in the corpus carries `cdspua.jsn`/`cdsps.jsn`; the only other cdsp-family filenames are the 13-device newer-generation `cdsp_dtb` quartet) [F].
- Packaging hides the family by construction, not by absence: the LineageOS xpeng manifest (lineage-24.0, blobs from the S1RXS32.50-13-25 RETEU build) contains **no cdsp lines at all** - the image ships in the modem partition, and the census db_path `motorola/xpeng/modem/image` records exactly that. The census is the only completeness witness for this family, and it is internally complete [F + I].
- Contrast that motivates the check: 3 corpus devices DO show a cdsp census gap - Pixel_4A_5G/Pixel_5/Pixel_5A carry a single 1-row cdsp family (Pixel_5/redfin: only `cdsp.mdt` 7,660 B at `google/redfin/vendor/firmware`, no segments, no manifest) [F]. Moto_G200 is not in that state: all 17 ELF members are present.

## Cross-corpus facts

- **Corpus-wide presence:** 940 cdsp rows across 63 devices. Row-count distribution: 21 rows on 13 devices (the newer generation that adds a separate `cdsp_dtb` ELF quartet: OnePlus_11_5G shape = 17 ELF files + jsn + `cdsp_dtb.mdt` + `cdsp_dtb.b00-b02`, with a b14 gap and b00 564 = 52 + 32 x 16, i.e. phnum 16 [I on the phnum reading]; linux-firmware already ships matching `cdsp_dtb.mbn` files for x1e80100/glymur/hawi/kaanapali, WHENCE lines 7551-7563, 7607-7636), 19 rows on 9 devices, **18 rows on exactly 8 devices: Edge_30, Edge_30_Fusion, FP5, Moto_G200, OnePlus_9, OnePlus_9_Pro, OnePlus_9RT, Phone_1** - all carry b00 = 596 (phnum 17), with FP5/Phone_1 on a smaller-hash variant (mdt 7,828 = 596 + 7,232) and Edge_30 on xpeng's exact shell sizes (7,980 = 596 + 7,384) but different payloads [F], 12 rows on 19 mid-range devices, 11 rows on 11 devices (bengal Moto fleet + OnePlus_7 generation), 1 row on 3 Pixel devices (census gaps) [F].
- **SM8350 cohort sharing [F]:** `cdsp.b02` (8,584 B), `cdsp.b04` (1,172 B) and `cdsp.b05` (1,096 B) are byte-identical across exactly 5 devices - Moto_G200 (xpeng), Edge_30_Fusion (tundra) and the OnePlus_9/9_Pro/9RT lemonade family, all SM8350-generation. Everything payload-bearing is device-signed: b03 (1,070,949 B) has the same size on all 5 but 3 distinct md5s (G200 unique; the OnePlus trio share `e27708ba...`; tundra unique), b07 (106,288 B) repeats the same 3-way pattern, b11 (60,488 B) spans 4 devices with 3 distinct md5s, b10 differs in size outright (G200 2,739,464; OnePlus 9/9_Pro 2,739,368 shared; 9RT 2,739,368 with different bytes; tundra 2,739,496). Same skeleton, per-OEM builds [F rows, I on the conclusion].
- **Two-generation servreg manifest split [F]:** the corpus carries exactly two cdsp manifest generations, both 30-device fleets with zero overlap: the 403 B `cdspr.jsn` (md5 `f2bd80d5f0b19b5b0d36d28383948149`) on the bengal-through-SM8250 fleet (Moto_G10/G30/G32/G34/G42/G52/G82/G84/G_5G_2024/G9/G9_Power/G_Power/G_Stylus_5G/G_Stylus_5G-2-2022, Moto_E7_Plus, Defy_2021, Mi_A3, OnePlus_7/7_Pro/7T/7T_Pro/8/8_Pro, Nord_CE2/CE3, Pro_1X, FP4, Edge_30_Neo, Realme_9_Pro/10_Pro) - **byte-identical to both downloaded public manifests** - and the 513 B `cdspr.jsn` (md5 `49003ffc...`) on the 5 nm-generation fleet (Moto_G200, Edge_30, Edge_30_Fusion, Edge_40_Pro, FP5, FP6, Mi_12/12_Pro/12S/12S_Pro/12S_Ultra/12T_Pro/13/13_Pro, OnePlus_9/9_Pro/9RT/11_5G/12/13, Pad_Pro/Pad_2_Pro, Phone_1/Phone_2, Poco_F5/F5_Pro/F6_PRo, Nord_4, Nord_CE4, Redmi_K60_Pro). Delta 513 - 403 = 110 B. The 513 B file's bytes were not read (device payload); its schema is by convention the same servreg JSON [I].
- **servreg schema [F, public]:** the downloaded 403 B `qcom/sm8250/cdspr.jsn` parses as JSON: `sr_version` {major 1, minor 1, patch 1}; `sr_domain` {soc "msm", domain "cdsp", subdomain "root_pd", qmi_instance_id 76}; `sr_service` [{provider "tms", service "servreg", service_data_valid 0, service_data 0}]. This matches #1240's byte-verified adsp servreg schema with domain "cdsp" and qmi_instance_id 76. Three independent public code sources corroborate the mapping "cdspr.jsn = msm/cdsp/root_pd, instance 76": a pd-locator table (blu-sharky/debian-piano `initramfs/pd-locator/piano-pd-locator.c`), a leaked QTI build recipe installing `cdspr.jsn` as the cdsp_root image's SERVICE REGISTRY output (Rivko/android-firmware-qti-sdm670 `cdsp_proc/build/bsp/cdsp_root/build/cdsp_root.scons`), and a DSP-prep tool mapping `'cdspr.jsn': ('cdsp', 'root_pd', 76)` (Producdevity/reframed-vr `tools/prepare-pico-dsp.py`) - all located via GitHub code search, 2026-11-21 [F].
- **Contrast with the adsp family (#1258):** capri's adsp ships a THREE-file servreg trio (adspr/adsps/adspua = root_pd/sensor_pd/audio_pd); the cdsp domain corpus-wide ships exactly ONE manifest, consistent with the schema declaring only root_pd [F rows + F public schema].
- **The db_type=COMPUTE labels are corpus-accurate here** (17 rows): this family genuinely is the compute-DSP image - unlike the a660_gmu AUDIO mislabels (#946) [F].

## Interface and ISA facts

- **Mainline device tree [F, torvalds master fetched 2026-11-21]:** `sm8350.dtsi` declares `cdsp: remoteproc@a300000` with `compatible = "qcom,sm8350-cdsp-pas"`, reg 0x0a300000 + 0x10000, `memory-region = <&pil_cdsp_mem>` where `pil_cdsp_mem` = memory@89700000, size 0x1e00000 = 31,457,280 B (30 MiB, no-map); glink edge "cdsp" (IPCC_CLIENT_CDSP, remote-pid 5); a fastrpc node with compute-cb 1-8 (`/* note: secure cb9 in downstream */`). For contrast the same file's adsp node is `qcom,sm8350-adsp-pas` at remoteproc@3000000.
- **Driver [F]:** `drivers/remoteproc/qcom_q6v5_pas.c` registers `"qcom,sm8350-cdsp-pas"` with `sm8350_cdsp_resource`: `firmware_name = "cdsp.mdt"`, **pas_id 18**, crash_reason_smem 601, minidump_id 7, `auto_boot = true`, proxy powerdomains {cx, mxc}, load_state/ssr_name/sysmon_name "cdsp", ssctl_id 0x17. The PAS loader requests `cdsp.mdt` and the mdt loader pulls the bNN segments - the census names map 1:1 onto the boot chain.
- **Packaging [F]:** the LineageOS xpeng manifest packages no cdsp files; with modem-partition shipping, a booted stock device exposes the image under the firmware mount of the modem partition (`image/cdsp.mdt` + `image/cdsp.bNN` + `image/cdspr.jsn`), which is what the extraction corpus recorded as `motorola/xpeng/modem/image` [I on the mount-point string]. Contrast: Pixel_5's lone `cdsp.mdt` is recorded at `google/redfin/vendor/firmware` - a vendor-partition placement [F].
- **ISA [F + honest negative]:** the SM8350 compute DSP is Hexagon 780 (marketing name; toolchain arch hexagon-v68) per public spec pages (2026-11-21); the executable format is Hexagon QDSP6 ELF (e_machine 164 confirmed on both public CDSP witnesses parsed this session). The corpus records `isa_identified` EMPTY and `interface_documented=n` on all 18 rows - the segments are honestly un-RE'd here. By size the likely code/resource-bearing segments are b10 (2,739,464 B, 45.71%), b06 (1,819,812 B, 30.36%) and b03 (1,070,949 B, 17.87%) - together 93.94% of family bytes [I - no disassembly performed].
- **Prior RE art survey [F]:** web search (2026-11-21) finds generic Hexagon/QDSP6 RE resources (QDSP6 microarchitecture talks, Hexagon firmware emulation/fuzzing toolchains, Hexagon security tool collections) but nothing targeting the Moto G200 / xpeng cdsp image; GitHub code search for `"cdsp.mdt" xpeng` returns zero hits outside this repo.

## Honest negatives ([OPEN])

- No payload of this device was fetched or analyzed (metadata-only; the 17 device-signed files exist in the corpus as hashes only). The only binaries touched were the public linux-firmware sm8250/qrb4210 CDSP builds (ELF header tables) and the public 403-byte JSON manifest.
- The e_phnum 17 / phdr-role assignment for xpeng's own image is derived from two exact size laws plus public generational witnesses - not from xpeng's mdt bytes. A program-header dump of the real `cdsp.mdt` (7,980 B) remains the direct proof and is [OPEN].
- The 513 B `cdspr.jsn` bytes were not read; the G200 copy's domain/qmi_instance_id values are inferred from the public 403 B sibling schema and three independent public code references [I].
- No Hexagon ISA proof from the blobs: no segment was disassembled; Hexagon 780 is from the SoC spec, e_machine 164 from the public builds.
- Whether phdr 16 (trailing) is BSS-only rather than some other file-less form is rule-based [I], the same caveat #1258 records for its trailing phdr.
- The 93.94% three-segment byte concentration is a size-based ranking, not evidence of which segment contains which functionality [I].
- Reconciling the public sm8250 monolith against its own header table leaves a 17,218 B residue beyond phdr0 + phdr1 + the file-backed filesz sum (5,826,324 vs 5,809,106) - presumably inter-segment alignment from pil-squasher; noted, not explained further [I].

## What would upgrade this finding

1. Extract the stock modem partition (fastboot image or OTA payload), byte-verify all 18 census md5s, and dump the ELF program headers of `cdsp.mdt` (7,980 B): expect e_phnum 17, phdr 0 = 596 B header-table self-reference, phdr 1 = 7,384 B hash/metadata, phdr 16 with p_filesz 0 - converting the structural derivations from [I] to direct [F].
2. Read the 513 B `cdspr.jsn` (plain JSON): confirm sr_domain {soc, domain, subdomain, qmi_instance_id} for the 5 nm generation and diff against the 403 B public schema.
3. Disassemble b10/b06/b03 with a public Hexagon toolchain (Ghidra Hexagon module, a Capstone fork, or the LLVM Hexagon backend) and record the ISA revision - fills `isa_identified` on all 17 ELF rows.
4. linux-firmware ships no sm8350 CDSP drop; if one lands (or a public xpeng/Edge S30 OTA surfaces), diff its segment table against xpeng's sizes to test the phnum-17 skeleton hypothesis (b00 596 / mdt 7,980 vs sm8250's 468 / 7,660).

## RULE 0 record

- CLAIM posted 2026-11-21T11:23:33Z as the first comment (confirmed first by re-read at 11:23:38Z; no competing claim).
- SEARCH (Gate -1) posted 2026-11-21; DELTA (Gate 0) posted 2026-11-21; work started only after both.
- All census numbers are awk/python outputs on `upstream-contribution/blob-database/coverage-matrix.csv` at feat/open-device-site 086491d, this session; every sum re-verified with python3 before writing. Web fetches dated 2026-11-21: LineageOS wiki (xpeng, xpeng/variant1, dubai), LineageOS/android_device_motorola_xpeng proprietary-files.txt (lineage-24.0), Motorola support spec page, /e/OS device page, torvalds/linux master `sm8350.dtsi` + `qcom_q6v5_pas.c`, linux-firmware WHENCE (line numbers recorded per fetch), public builds `qcom/sm8250/{cdsp.mbn,cdspr.jsn}` (md5 `b60a1a6b...` / `f2bd80d5...`) and `qcom/qrb4210/{cdsp.mbn,cdspr.jsn}` (md5 `6535ffea...` / `f2bd80d5...`); ELF parsing and JSON schema read performed with stdlib `python3 -I` on the downloaded public files, header metadata and manifest fields only.

Nothing in this document is legal advice; no proprietary payload bytes were fetched, stored or committed - only sizes, md5s, ELF header metadata and JSON schema of public builds, public-source quotations and arithmetic derivations.
