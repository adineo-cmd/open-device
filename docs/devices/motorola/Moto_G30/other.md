# motorola Moto_G30 (caprip) - `other` family status (57 rows - PRESENT as the residual catch-all across 5 locations; 9 clusters, 39,210,797 B, 54 distinct md5s; 22 corpus-unique rows; the venus b11-b18 gap is STRUCTURAL per the public venus-6.0/qcm2290 build witness; fngap64 is the QSEE fingerprint TrustZone app; tbase is a complete Trustonic TEE split set shipped alongside the Qualcomm TEE stack; the WCN3950 cm* set carries both the 1.2.0 and 1.3.0 branches and NONE byte-matches the public linux-firmware builds)

Analysis date: 2026-11-21. Analyst: ZC-1 (issue [#1282](https://github.com/adineo-cmd/open-device/issues/1282)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, feat/open-device-site 7c0f9e3), `upstream-contribution/blob-database/device-inventory.csv`, the sibling doc docs/devices/motorola/Moto_G10/other.md (#1264, the capri twin - cited not re-deriving), docs/devices/motorola/Moto_G30/adsp.md (#1276, same device), LineageOS `android_device_motorola_caprip` `proprietary-files.txt` (lineage-22.2 branch, raw.githubusercontent, fetched 2026-11-21, header "All unpinned blobs below are extracted from caprip_retail S0RC32.41-10-19-25"), linux-firmware WHENCE (git.kernel.org, fetched 2026-11-21; WCN3950 section lines 5343-5356) plus the six mainlined public builds `qca/{cmbtfw12,cmbtfw13}.tlv` and `qca/{cmnv12,cmnv13,cmnv13s,cmnv13t}.bin` (git.kernel.org plain, fetched and md5-recorded 2026-11-21), the LineageOS `android_device_samsung_msm8916-common` `Android.mk` tbase packaging fragment (GitHub code search, fetched 2026-11-21), the public Kinibi/t-base identity page Azeria-Labs "Trustonic's Kinibi TEE implementation" (web, 2026-11-21), the pnangn touch-reflash script and FP4 fngap64 public prior art as recorded in #1264 (fetched there 2026-11-21), and the fleet docs research/fleet/other-media.md (#2058) and research/fleet/other-audio.md (#2052) as recorded in #1264. No device payload was fetched or committed; the only binaries inspected are the six public linux-firmware qca files, and only their sizes and md5s. Every number is command output or a recorded fetch; sums re-verified with python3 -I this session.

**Verdict: the `other` family is PRESENT on Moto_G30 and the census is COMPLETE for what the matrix grammar captures - 57 rows, 39,210,797 B, 54 distinct md5s, 22 corpus-unique rows, all P3, spread over 5 locations.** The family is the census remainder (research/soc/per-soc-method-plans.md:417: "other (rest - the upstream UNKNOWN tail)"): it decomposes into 9 clusters - the radio partition image trio (3 rows, 86.56% of family bytes), the `fngap64` QSEE fingerprint TrustZone app as a complete 9-row 64-bit split-PIL set with the same size skeleton as capri's (8.07%), the `venus` video firmware as a complete 13-row split set whose b11-b18 absence is STRUCTURAL - the public `qcom/venus-6.0/venus.mbn` program-header witness parsed in #1264 matches caprip's seven smallest segment sizes exactly (1.94%), `Data.msc` + the orphaned `scuba_ipa_fws.mdt` (2 rows, 1.67%), a complete 9-row `tbase` Trustonic TEE split set that capri lacks (0.93%), the `djn1_nt36525c` touchscreen pair (2 rows, 0.61%), a 12-row WCN3950-branch `cm*` Bluetooth set carrying BOTH the 1.2.0 and 1.3.0 build branches - none byte-identical to the public linux-firmware builds (0.22%), the Awinic AW882XX speaker-amp pair (2 rows, 0.01%) and 5 camera calibration rows (542 B). Two recorded census divergences: the LineageOS caprip manifest lists `dual_golden_{depth,ov8856_wide,wide}.bin`, `vidhance_calibration`, `ILITEK_FW_TIANMA_9882N`, `ILITEK_FW_TXD_9882N` and two `NT36xxx_MP_Setting_Criteria_*.csv` files with zero rows anywhere in the 33,917-row corpus.

## Device identity

| fact | value | source |
|---|---|---|
| model | Motorola Moto G30, XT2129 | sibling doc #1276 identity table [F]; public spec pages (via #1276) [F] |
| codename | `caprip` (db_path `motorola/caprip/...` and inventory `build_codename` agree) | coverage-matrix.csv + device-inventory.csv [F]; #1276 [F] |
| SoC | Qualcomm **SM6115 Snapdragon 662** (11 nm), Adreno 610 GPU, Snapdragon X11 LTE modem | inventory cell [F]; public spec pages (via #1276) [F]. **The inventory SoC cell is CORRECT for this device** - unlike the known-wrong dubai/tundra cells flagged in #1270 |
| stock build | `caprip_retail S0RC32.41-10-19-25` | LineageOS caprip proprietary-files.txt header (lineage-22.2, fetched 2026-11-21) [F] |
| census scope | 232 rows in 9 families (other 57, modem 43, wifi 45, adsp 37, gpu 14, cdsp 12, bt 11, boot 8, tz 5); total 457,752,331 B | coverage-matrix.csv + device-inventory.csv [F]; family row counts and byte sums re-verified with python3 this session and equal the inventory totals exactly |
| priority | P3 on all 57 `other` rows | coverage-matrix.csv [F] |

Inventory flags for the lead: (a) the caprip accounting cells are internally consistent (232 = sizes_rows = matrix rows; 457,752,331 = family-byte sum) [F]; (b) `extract_status_22.2` = "fails" while the matrix carries the complete 232-row census - same data-hygiene question #1276 raised, unresolved; (c) the inventory SoC cells of the tbase/venus sharing cohorts named below are EMPTY for cebu/guamp/denver and carry `Qualcomm SM6115 Snapdragon 662` for bathena where public spec pages put the Defy 2021 on the QM215/SM4250 class - not adjudicated here, flagged [I].

## Where the family lives and the census grammar [F]

| db_path | rows | bytes |
|---|---|---|
| `motorola/caprip/radio` (partition images) | 3 | 33,939,456 |
| `motorola/caprip/modem/image` (firmware mount) | 33 | 4,944,556 |
| `motorola/caprip/bluetooth/image` | 12 | 86,495 |
| `motorola/caprip/vendor/firmware` | 4 | 239,748 |
| `motorola/caprip/vendor/etc/camera` | 5 | 542 |
| total | 57 | 39,210,797 |

Subfamily split: misc 37 rows / 38,446,135 B; media 13 / 761,940; camera 5 / 542; audio 2 / 2,180 (python-verified, this session). Cluster sums equal the subfamily sums and the total exactly. All 57 rows have `isa_identified` EMPTY, `interface_documented=n`, `sha256_if_listed` EMPTY. Recorded db_type pattern: mdt/monolith rows carry `ELF64` (9 rows), the Awinic pair carries `CODEC` (2), segments carry `UNKNOWN` (46) - including `tbase.mdt`/`tbase.b00` = `ELF64`, which the exact size arithmetic below contradicts (the tbase container is ELF32); flagged for the lead, the same tension #1264 recorded for capri's `venus.mdt`.

Grammar note: the matrix files every `venus.*` row corpus-wide under `other`/`media` (per #1264's 371-row sweep) while the method-plan sketch would place it under a dsp family - the matrix implementation is what the corpus shows [F, per #1264].

## Cluster A - radio partition image trio (3 rows, 33,939,456 B, 86.56%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| dsp.img | 33,554,432 | `ae19750b739aa98d8a69cac66d0ea289` | 1 (corpus-unique) |
| prov.img | 258,048 | `94a3b2113d86dd8c95a326b16c099e0e` | 1 (corpus-unique) |
| storsec.img | 126,976 | `aa2b17999fdbdc3584dcae56d1e75dda` | 1 (corpus-unique) |

- Same three files, same three sizes, same same-size-different-bytes per-device pattern as capri's trio (#1264 cluster A) [F]. The three sizes are the SM4250/SM6115-generation constants: `dsp.img` exists on 61 corpus devices - exactly 32 MiB (33,554,432) on 23 devices of the SD425/SM6115/SM6225/SM6375 class and 64 MiB (67,108,864) on 38; `prov.img` on 21 (10 at 258,048, 11 at 262,144); `storsec.img` on 28 (10 at 126,976, 11 at 131,072, 6 at 24,576, 1 at 20,480) - all re-swept on the current matrix this session, matching #1264's numbers [F].
- Flash flow (cited from #1264): CalyxOS/scripts `factory/hawao/flash-base.sh` (fetched there 2026-11-21) runs `fastboot flash storsec_a/b storsec.img`, `flash prov_a/b prov.img`, `flash dsp_a/b dsp.img` - Motorola radio-package partition images flashed to A/B partitions [F].
- Content: not verifiable from the census (one opaque 32 MiB image, no payload fetched). The Qualcomm `dsp` partition is the DSP system object slot in public packaging conventions [I]; caprip's own adsp image ships in the modem firmware mount per #1276, so which subsystems caprip's dsp.img carries is [OPEN].

## Cluster B - `fngap64`, the QSEE fingerprint TrustZone app (9 rows, 3,165,489 B, 8.07%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| fngap64.mdt | 7,464 | `9af5a4abfb2ef9ac9e8300dbb863153d` | 1 (corpus-unique) |
| fngap64.b00 | 512 | `8ee479d04b64f5910e1ffa934a41c7da` | 3 (Moto_G10, Moto_G30, Moto_G9_Power) |
| fngap64.b01 | 6,952 | `45d4065297b089855d6f5abb4449209f` | 1 (corpus-unique) |
| fngap64.b02 | 2,621,656 | `cc956d079c849a136d2fe65dbb13514d` | 1 (corpus-unique) |
| fngap64.b03 | 264 | `3ceb3cbd48cfcb5f5582a4300ceb98da` | 3 (same trio) |
| fngap64.b04 | 403,112 | `f637670d6acb979c5bb14b72aa2f0f08` | 3 (same trio) |
| fngap64.b05 | 1,728 | `eeede038681661c4ecc57c6fe0749591` | 3 (same trio) |
| fngap64.b06 | 304 | `897fb22825e714f3cf55a6e454e8e0f9` | 3 (same trio) |
| fngap64.b07 | 123,497 | `cdea27f6b0ab98b8c21a9337ec43529c` | 3 (same trio) |

- Identity (public prior art, cited from #1264, not re-derived): `fngap64` is the QSEE fingerprint TrustZone application - nyl/linux-qseecom-mobile `tz-qsee-fingerprintd/plugins/fp4_icnf7312/README.md` documents the FP4 instance (`TCL_T2MFP4_qsee5.10_SM7225_android12_ca64bit_icnf7312`, loaded as `"fingerprint"`, TCI command IDs 0x00-0x23, 16-byte transport header, 64 KiB shared buffer, Pangu R60C matching algorithm); nyl/device-firmware-blobs readme names the Chipone ICNF7312 TA; LineageOS `android_device_vsmart_casuarina` ships `fngap64.b00-b06` + mdt. The name spans SDM660-era vsmart through SM7225 FP4 to the Moto SM4250/SM6115/SM6225 fleet [F].
- **Container layout [F arithmetic, re-verified on caprip's own rows this session]:** complete 9-row split image - mdt = b00 + b01 exactly (512 + 6,952 = 7,464), and `fngap64.b00` 512 = 64 + 8 x 56 - the exact size of an ELF64 header (64 B) plus 8 program header entries (56 B each); the ELF32 reading has no integral solution ((512-52)/32 = 14.375). So **caprip's fngap64 is an ELF64 image with e_phnum = 8**, matching the census db_type=ELF64 on the mdt/b00 rows and the `ca64bit` marker in the public FP4 TA build string [I for the generational tie].
- **Size skeleton identical to capri's [F]:** all nine caprip sizes equal capri's (7,464 / 512 / 6,952 / 2,621,656 / 264 / 403,112 / 1,728 / 304 / 123,497 - python comparison this session); six of nine files (b00, b03-b07) are byte-identical across the Moto_G10/Moto_G30/Moto_G9_Power trio, the mdt, b01 and the 2.6 MB b02 body are build-local [F, md5 sweeps this session].
- Metadata-segment algebra [I, applying the #2058/pil-metadata-sweep decomposition recorded in #1264]: caprip b01 6,952 = 168 + 48x8 + 256 + 6,144 (48x8 = 384 hash table over 8 phdrs, RSA-2048 signature, one 6,144 B cert chain) - identical to capri's decomposition, consistent with per-device signatures over the same skeleton.
- Interface [F, caprip manifest lines 186-193, fetched 2026-11-21]: the caprip LineageOS manifest ships two fingerprint HAL services - `android.hardware.biometrics.fingerprint@2.1-service-chipone` (+ `chipone.fingerprint.default.so`) and `@2.1-service-fpc` (+ `fpc_ident`, uinput-fpc idc/keylayout) - so the trustlet serves Chipone- and FPC-sensor SKUs; which sensor the census build pairs with is not resolvable from the corpus [OPEN], the same dual-HAL situation #1264 found on capri.

## Cluster C - `venus` video-firmware split set (13 rows, 761,940 B, 1.94%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| venus.mdt | 8,220 | `07d9b01885dbd0283d13b9174d966da3` | 1 (corpus-unique) |
| venus.b00 | 692 | `34e021dd71229b15e20aab2cba716e9b` | 5 (Moto_G30, Moto_G82_5G, Moto_G_Stylus_5G, Phone_1, Pro_1X) |
| venus.b01 | 7,528 | `ab1c8b52202b006d90e8b1d8d6d1a3ae` | 1 (corpus-unique) |
| venus.b02 | 292 | `00072978914e571061fa6047647df379` | 3 (Moto_G30, Phone_1, Pro_1X) |
| venus.b03 | 20 | `4344e840708282eccd554f7d244c7e63` | 23 |
| venus.b04 | 20 | `8d357ccaade40bc6e930189209d7ebe5` | 3 (Moto_G30, Phone_1, Pro_1X) |
| venus.b05 | 20 | `f05c4f03a9283589091c31be065c6fed` | 30 |
| venus.b06 | 20 | `d81a5c71adbe6aae61e4b4a8e121e446` | 30 |
| venus.b07 | 24 | `eb667b725e1602ba8b9300293a4a2272` | 30 |
| venus.b08 | 16 | `ec2d6ced2030acafa2b680b83eb3ab63` | 30 |
| venus.b09 | 689,040 | `90913174277d95edd0e48b893e8ae3ff` | 3 (Moto_G30, Phone_1, Pro_1X) |
| venus.b10 | 56,016 | `37be6c6795a227dc75e96c99bc24d65c` | 3 (Moto_G30, Phone_1, Pro_1X) |
| venus.b19 | 32 | `0d68af0904dd698b16ffc9cd28b9b0c8` | 34 |

- **The b11-b18 absence is STRUCTURAL, not a census gap** (established in #1264 for capri; caprip's set has the identical shape and the identical public anchors). Four lines of evidence: (1) size laws [F arithmetic, caprip's own rows, python this session]: mdt = b00 + b01 exactly (692 + 7,528 = 8,220) and b00 = 52 + 20 x 32 - an ELF32 header plus 20 program header entries (the ELF64 reading has no integral solution, (692-64)/56 = 11.21), so **e_phnum = 20**; the shipped set is exactly {mdt, b00..b10, b19} = 13 rows, i.e. phdrs 0-19 minus phdrs 11-18. (2) Public generational witness [F, parsed in #1264]: linux-firmware `qcom/venus-6.0/venus.mbn` (1,794,924 B, md5 `b7f437a33adbb851e75099293d0b35e1`) parses as ELF32 LE, e_machine **94 (EM_XTENSA)**, e_phnum 20, phdr 0 = 692 B header table (= caprip's b00 size exactly), phdrs 2-8 p_filesz = 292/20/20/20/20/24/16 - **caprip's b02-b08 sizes exactly, all seven** (re-verified from the census this session) - phdr 9 = code, phdr 10 = data, **phdrs 11-18 all p_filesz 0**, phdr 19 p_filesz 32 (= caprip's b19 size). A p_filesz-0 PT_LOAD produces no `.bNN` file under the split convention (torvalds/linux `drivers/soc/qcom/mdt_loader.c` requests segments only when p_filesz > 0, lines 413-423, per #1264) - so no venus.b11..b18 files exist to census. (3) Corpus sweep [F, per #1264 + re-swept this session]: zero `venus.b11`..`venus.b18` rows exist anywhere in the 33,917-row corpus; the tiny segments are fleet constants (b05/b06/b07/b08 on 30 devices, b03 on 23, b19 on 34). (4) In-repo prior measurement [F, #2058 sec 4.5 via #1264]: on actual venus files the metadata hash table has zero entries exactly at indices {1, 11..18}, the hash-zero rule hash[i] = 0 iff i = 1 or phdr[i].p_filesz = 0.
- ISA [F, cited from #1264]: the venus container is e_machine 94 = EM_XTENSA (public build parsed there; #2058 measured the same on SM8250 venus/cvpss); the mainline driver binds this generation as `qcom,qcm2290-venus` (sm6115.dtsi lines 1856-1858) with `.fwname = "qcom/venus-6.0/venus.mbn"`, HFI 4XX, min_fw 6.0.55 (venus-core.c lines 1200-1233), and the AR50_LITE reset path groups it with IRIS2/IRIS2_1 (venus-core.c line 260). No disassembly was performed; the ISA verdict rests on the e_machine byte and the kernel's reset path [I on the generational extension to caprip's own bytes].
- Metadata algebra [I]: caprip b01 7,528 = 168 + 48x20 + 256 + 6,144 (RSA-2048-signed metadata over 20 phdrs) - identical decomposition to capri's (per #1264).
- **The caprip-specific sharing cohort [F, new this session]:** caprip's b00 is byte-identical with Moto_G82_5G (SM6375/SD695), Moto_G_Stylus_5G (denver, inventory SoC cell EMPTY), Phone_1 (SM7325) and Pro_1X (SM6115) - and b02/b04/b09/b10 with Phone_1 + Pro_1X. capri's corresponding files were corpus-unique. So caprip rides the newer venus-6.0 build cohort: its code segment `venus.b09` is 689,040 B vs capri's 686,672 (delta 2,368) and its mdt/b01 are its own signed build, while Phone_1 (SM7325) and Pro_1X (SM6115) carry byte-identical venus payloads [F md5s; I on what the cohort implies about build generations].

## Cluster D - modem/image misc singles (2 rows, 653,192 B, 1.67%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| Data.msc | 646,172 | `18f7f57b9bd9bc601fc543bf1e1a74c0` | 1 (corpus-unique) |
| scuba_ipa_fws.mdt | 7,020 | `8eacc6f0b646adf5d38b774a573ff316` | 1 (corpus-unique) |

- `Data.msc` sits in the modem firmware mount across 54 corpus devices (627,835-1,769,820 B range re-swept this session; caprip 646,172, its own build). Its role is not publicly documented; the sibling doc #1228 carries an EFS/NV-container hypothesis [I] and public device trees place it in `/vendor/firmware_mnt/image` [I, per #1264]. Honest status: hypothesis only, no format facts.
- `scuba_ipa_fws.mdt` is a **classification orphan**, exactly as on capri (#1264 cluster D): its five segment files sit in the `modem` family with db_type=CELL (`scuba_ipa_fws.b00` 212, `b01` 6,808, `b02` 12,040, `b03` 128, `b04` 320) while the mdt alone fell into `other` with db_type=ELF64 [F]. Inside caprip the scuba set is byte-comparable to the `ipa_fws` set (modem family): b00/b02/b03/b04 md5-identical between the two names (`c1b22203dd726a44d792d193806a362b`, `1c57082a52206086968252972b98f5e4`, `f012db03ebbde9ce8650993112ee430b`, `94e6dae207e61c724ebc61078bad87fa`), b01 and mdt differ at identical sizes 6,808/7,020 (`3652b22e0545426304b6b1c5559676d7` vs `708c2ffbc303b8151827da57d793b590`; `1f75e079ca490304be53afd7d9c93876` vs `8eacc6f0b646adf5d38b774a573ff316`) - a re-metadata'd build of the same IPA firmware under the scuba name [F md5s, swept this session]. Corpus: 11 Moto devices carry the full 6-row scuba set (bengal fleet + Moto_G_Stylus_5G) and the two Galaxy_Tab_A7 variants carry mdt-only rows (#1120, established) [F]. `scuba` is the SM6115 platform codename (#1120) - the scuba-named build shipping on caprip, a native SM6115 device, is consistent with that identification [I].

## Cluster E - `tbase`, the Trustonic TEE split set (9 rows, 363,935 B, 0.93%) - capri lacks it entirely

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| tbase.mdt | 7,260 | `7634cbe71ef7f8526321f28d29731850` | 1 (corpus-unique) |
| tbase.b00 | 308 | `488944514e5f6729b116e86692867158` | 5 (Defy_2021, Moto_G30, Moto_G9, Moto_G9_Power, Moto_G_Power) |
| tbase.b01 | 6,952 | `d60b7df1950f3170dfa4ef92b276161d` | 1 (corpus-unique) |
| tbase.b02 | 348,285 | `a387372127f39f37ab57ff726cf3e012` | 5 (same cohort) |
| tbase.b03 | 68 | `a73bfb92de07d10d401f1812532c9d50` | 8 |
| tbase.b04 | 52 | `469aa816010c9c8639a9176f625189af` | 8 |
| tbase.b05 | 52 | `55c3305e02c3f7fa2db0be81ad4556bb` | 5 (cohort; = tbase.b07 within each device) |
| tbase.b06 | 906 | `90f26852eb706e986fd7c615feb48240` | 8 |
| tbase.b07 | 52 | `55c3305e02c3f7fa2db0be81ad4556bb` | 5 (cohort; = tbase.b05 within each device) |

- **Identity [I, public witnesses]:** `tbase` is the Trustonic t-base (Kinibi, also MobiCore) TEE OS image. Public sources: Azeria-Labs "Trustonic's Kinibi TEE implementation" (fetched 2026-11-21) documents Kinibi = t-base = MobiCore as Trustonic's TEE product; LineageOS `android_device_samsung_msm8916-common` `Android.mk` (code search, fetched 2026-11-21) packages `tbase.b00 tbase.b01 tbase.b02 tbase.b03 tbase.mdt` to `$(TARGET_OUT_ETC)/firmware` - a public packaging witness that the `tbase.*` split set is a firmware image installed alongside other TEE/PIL firmware on a Qualcomm (msm8916) device. No Moto-specific public document names the trustlet; the mapping rests on the exact name match, the split-ELF container, and the modem/image placement [I].
- **Container layout [F arithmetic, caprip's own rows]:** complete 9-row split image, no gaps - mdt = b00 + b01 exactly (308 + 6,952 = 7,260), and `tbase.b00` 308 = 52 + 8 x 32 - an ELF32 header plus 8 program header entries; the ELF64 reading has no integral solution ((308-64)/56 = 4.36). So **caprip's tbase is an ELF32 image with e_phnum = 8**, all 8 phdrs file-backed (phdr 0 = 308 B header table, phdr 1 = 6,952 B hash/metadata segment, six payload phdrs). The census db_type=ELF64 on the mdt/b00 rows contradicts this arithmetic - census detection error or a non-ELF-class meaning of the field; flagged for the lead (second instance of the tension #1264 recorded for venus.mdt) [F tension].
- **Within-device duplication [F]:** `tbase.b05` and `tbase.b07` are byte-identical on caprip (and on every other tbase-carrying device) - the same 52 B payload packaged under two segment names.
- **Two corpus cohorts [F, swept this session]:** exactly 8 devices carry tbase sets, all Motorola: the 2021-generation cohort (caprip, guamp/Moto_G9, borneo/Moto_G_Power, cebu/Moto_G9_Power, bathena/Defy_2021) shares b00/b02/b05+b07 (348,285 B b02 = the TEE payload, byte-identical on all five) with per-device mdt/b01; the 2022-generation cohort (G_Stylus_5G-2-2022, Moto_G_5G_2024, Moto_G_Stylus_5G) carries a different build (b00 `79dc42ca09a451372e7b80876e3a9ed8`, b02 `188e9535a493a7388420ffc93edccacd`, b05/b07 = 152 B `f9360100fb60ea22c0345ac1a3197ee1`, again b05==b07 within each device) - and b03/b04/b06 (68/52/906 B) are byte-identical across ALL eight devices spanning both cohorts [F]. Every device's 9-row set is complete (mdt + b00-b07, no interior gap; python check on all 8 sets this session).
- **Dual-TEE device [I]:** caprip's `tz` family carries the full Qualcomm secure-OS stack as partition images (`tz.img` 4,190,208, `hyp.img` 520,192, `keymaster.img` 520,192, `uefisecapp.img` 2,093,056, `devcfg.img` 126,976 [F, 5 rows]) while `tbase.*` rides in the modem firmware mount in `other`. The census therefore shows a device shipping BOTH a Qualcomm TEE stack and a Trustonic t-base image; which one owns which runtime service is not resolvable from the corpus [OPEN].

## Cluster F - `djn1_nt36525c` touchscreen firmware (2 rows, 237,568 B, 0.61%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| djn1_nt36525c_novatek_ts_fw.bin | 118,784 | `d743e67b8934a4411bf987ddf30773c8` | 1 (corpus-unique) |
| djn1_nt36525c_novatek_ts_mp.bin | 118,784 | `fdceebb1812482d84f79423355167c2b` | 1 (corpus-unique) |

- Interface [F, cited from #1264]: moto-sm4350/android_device_motorola_pnangn `recovery/bin/load_touch.sh` (fetched there 2026-11-21) reads `/sys/class/touchscreen/*/panel_supplier` and reflashes the Novatek firmware via sysfs (`forcereflash`/`doreflash`) - the djn/djn1 files are Novatek touch-controller firmware for the Tianma-panel SKUs of Moto's bengal generation.
- The caprip census names the controller in the filename: **NT36525C** [F from the filename]. The caprip manifest lists both files at vendor/firmware plus recovery copies (lines 277-284, fetched 2026-11-21) [F] - one-to-one with the census rows. The ts_fw/ts_mp pair is same-size with different bytes [F]; mp reads as the mass-production variant [I, per #1264].
- **Corpus divergence [F]:** the manifest also lists `ILITEK_FW_TIANMA_9882N` and `ILITEK_FW_TXD_9882N` (lines 273-274, Ilitek firmware for alternate touch-panel SKUs) and `NT36xxx_MP_Setting_Criteria_601D.csv`/`602A.csv` (lines 275-276) with **zero rows anywhere in the 33,917-row corpus** (awk sweep, this session). Same divergence class as #1264's dual_golden finding; unresolved, [OPEN].

## Cluster G - `cm*` WCN3950-branch Bluetooth firmware (12 rows, 86,495 B, 0.22%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| cmbtfw10.tlv | 4,803 | `505051a52545bffe76082c82adda3147` | 14 |
| cmbtfw11.tlv | 14,247 | `8ec02ba2343140c0d155ea251ef416ac` | 14 |
| cmbtfw12.tlv | 47,755 | `134686ca6a1f3ad7aa5a99319ce4c8fd` | 1 (corpus-unique) |
| cmbtfw12.ver | 33 | `4363c53aef85ad22862847756061be51` | 1 (corpus-unique) |
| cmbtfw13.tlv | 7,583 | `4956c43e396eaead47cc62757ceefe16` | 1 (corpus-unique) |
| cmbtfw13.ver | 33 | `9f85e049b371229835e896a20b43ba46` | 1 (corpus-unique) |
| cmnv10.bin | 2,034 | `2dceb768ace4075997b5ebfcccd14bc8` | 14 |
| cmnv11.bin | 2,676 | `c22408ff6a58959d28a3a2ec4b35b024` | 14 |
| cmnv12.bin | 2,690 | `55d4fc9aff4108b07b9c42b5f3661c62` | 3 (Moto_G30, Phone_1, Pro_1X) |
| cmnv13.bin | 1,547 | `8a726c98324a0a4051512e44729d8fb1` | 1 (G30-only identity, 3 rows) |
| cmnv13s.bin | 1,547 | `8a726c98324a0a4051512e44729d8fb1` | (same identity) |
| cmnv13t.bin | 1,547 | `8a726c98324a0a4051512e44729d8fb1` | (same identity) |

- Chip identity [F, established per-soc-method-plans and #1264, verified against mainline btqca case labels]: `cmbtfw*`/`cmnv*` = WCN3950. linux-firmware WHENCE section "Driver: qca - Qualcomm Atheros Bluetooth support for WCN3950 chips" (lines 5343-5356, fetched 2026-11-21) lists `qca/cmbtfw12.tlv` (Version BTFM.CMC.1.2.0-00218-QCACHROMZ-2, line 5346), `qca/cmbtfw13.tlv` (BTFM.CMC.1.3.0-00184-QCACHROM-1, line 5348) and `qca/cmnv12.bin`/`cmnv13.bin`/`cmnv13s.bin`/`cmnv13t.bin` (lines 5349-5352). The WCN3950 support was mainlined into the kernel in early 2025 (Bluetooth: qca add WCN3950 support, per web search 2026-11-21).
- **caprip carries BOTH build branches [F]:** the 1.2.0 branch (cmbtfw12.tlv 47,755 + cmbtfw12.ver + cmnv12 2,690) and the 1.3.0 branch (cmbtfw13.tlv 7,583 + cmbtfw13.ver + cmnv13/13s/13t 1,547 each) - all six 12/13-branch files are corpus-unique to caprip, while the older 10/11 builds are fleet constants on 14 devices spanning 9 vendors and 5 SoC generations (Defy_2021, Mi_A3, Moto_E7_Plus, Moto_G10, Moto_G30, Moto_G32, Moto_G42, Moto_G52, Moto_G9, Moto_G9_Power, Moto_G_Power, Moto_G_Stylus_5G, Phone_1, Pro_1X - python roster re-verified at 7c0f9e3; #1246's earlier roster recorded in #1264 adds Moto_G_5G_2024). caprip's `cmnv12.bin` (2,690 B) is shared with Phone_1 and Pro_1X, not with the SM4250 twins - capri's cmnv12 shares with Moto_E7_Plus instead [F].
- **Within-device identity [F]:** `cmnv13.bin` = `cmnv13s.bin` = `cmnv13t.bin` (1,547 B, identical md5) - three filenames, one content. The public build shows the same naming convention with a split: `qca/cmnv13.bin` = `qca/cmnv13t.bin` (both 1,658 B, md5 `029955b1c2b4e368d3e4be870897ebf7`) while `cmnv13s.bin` differs (md5 `2267640532cac27c95507ecbe072565f`) - the s/t suffixes are a real packaging distinction, collapsed to one payload on caprip's build [F; I on what the suffixes denote].
- **Public byte-check [F, honest negative]:** all six mainlined qca files fetched 2026-11-21 and md5-recorded: cmbtfw12.tlv 47,307 B / `5b28485f3fb1088cc1029d938f99a4d7`; cmbtfw13.tlv 36,927 B / `b8911425138debcfadc1187d7daef269`; cmnv12.bin 2,690 B / `33ef067bc3b13647b4f451814ca4c9da`; cmnv13/13s/13t 1,658 B each (md5s above). **None matches caprip's census bytes** - cmbtfw12.tlv differs in size (47,755 vs 47,307; the 47,307 size class is what #1264 recorded for G32/G42/G52), cmbtfw13.tlv differs enormously (7,583 vs 36,927 - caprip's 1.3.0-branch firmware is a 4.9x smaller file than the mainlined one), cmnv12 matches size but not bytes, cmnv13* differ in size (1,547 vs 1,658). The adsp family's jsn-trio byte-identity (#1276) has no cm* counterpart here: caprip's WCN3950 builds predate or diverge from the mainlined drops, and the 7,583 B tlv suggests a materially different patch level [I]. Build dating from public byte identity is not possible for this cluster.
- Why they are in `other`: the bt family grammar captured the `cr*` (WCN3990/3991/3998) and `ap*` (WCN3988) prefixes plus `bluetooth.img` (caprip's bt family, 11 rows: apbtfw10/11, apnv10/11, crbtfw11/20/21, crnv11/20/21, bluetooth.img 1,048,576 [F]) while `cm*` fell through to the residual family [F, same grammar artifact #1264 flagged]. caprip therefore ships **three** Qualcomm combo-BT chip firmware branches at once - ap, cr and cm [F].

## Cluster H - Awinic AW882XX speaker-amp firmware (2 rows, 2,180 B, 0.01%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| aw882xx_mono.bin | 2,036 | `b88e5ba238ebcea95a0959b92a97a3b0` | 1 (corpus-unique) |
| aw882xx_spk_reg.bin | 144 | `4c4315f5fd6cb18898a382d26de677e0` | 15 |

- The caprip manifest lists both at vendor/firmware (lines 17-18, fetched 2026-11-21) [F], matching the census one-to-one. Awinic AW882XX smart-amp configuration/calibration per #2052 (the fleet audio doc, via #1264: mainline parses Awinic ACF files via aw88395_lib.c; the Moto mono/spk_reg naming is the downstream Awinic-SDK driver's file set) [F + I].
- `aw882xx_spk_reg.bin` (144 B) is the fleet-wide byte-constant on 15 devices, all Moto-family (roster identical to #1264's: Defy_2021, Edge_2021, Edge_30, Edge_30_Fusion, Moto_E7_Plus, Moto_G10, Moto_G200, Moto_G30, Moto_G32, Moto_G42, Moto_G52, Moto_G9, Moto_G9_Power, Moto_G_Power, Moto_G_Stylus_5G) [F]. The 2,036 B mono file is caprip-local; capri carries a same-size mono with different bytes, and capri's third file `aw882xx_mono_power.bin` is absent from caprip's census and manifest - the G10-only corpus singleton per #1264 [F].

## Cluster I - camera calibration (5 rows, 542 B, 0.00%)

| file | bytes | md5 | devices sharing |
|---|---|---|---|
| dc_mot_ov8856.bin | 256 | `b87551bcb34928fcb3dabbf823997675` | 2 (Moto_G10, Moto_G30) |
| arcsoft_calibration_u_dc.bin | 256 | `3a510b98a69ff9391d5d1bd223eacbf0` | 7 (Edge_2021, Edge_30, Moto_G10, Moto_G30, Moto_G42, Moto_G52, Moto_G_Stylus_5G) |
| aec_golden_wide.bin | 10 | `822e276da683e95ac7bb6a668a2e32f6` | 1 (corpus-unique) |
| aec_golden_depth.bin | 10 | `c1cf5cfea406e273ef922cc928e30109` | 1 (corpus-unique) |
| aec_golden_ov8856_wide.bin | 10 | `d624d872cc337bca0a78716080f82459` | 1 (corpus-unique) |

- The five census rows match the caprip manifest's vendor/etc/camera entries lines 167-171 one-to-one (fetched 2026-11-21) [F]. Sensor context [F from the manifest + #1264's capri analysis]: the `aec_golden_*` naming marks the wide (`ov8856`) and depth golden-reference calibration bins; `dc_mot_ov8856.bin` is byte-identical between capri and caprip (the only G30-camera byte shared with another device); `arcsoft_calibration_u_dc.bin` is the Arcsoft-partner calibration, byte-identical across 7 Moto devices.
- **Recorded census divergence [F]:** the manifest also lists `dual_golden_depth.bin`, `dual_golden_ov8856_wide.bin`, `dual_golden_wide.bin` (lines 172-174) and `vidhance_calibration` (line 175) with **zero rows anywhere in the 33,917-row corpus** (awk sweep, this session) - exactly the four-file divergence #1264 recorded for capri. Either the corpus harvest predates/excludes these files or the matrix filters them out; unresolved, [OPEN].

## Cross-corpus facts

- The family is a residual catch-all, not a coherent firmware family: its 9 clusters span seven unrelated subsystems (radio partitions, QSEE TA, video PIL, Trustonic TEE, BT, touch, amp, camera calibration, modem misc) and 5 locations [F].
- 22 of 57 rows are corpus-unique; the cmnv13 trio is a G30-exclusive identity with 3 rows; the remaining 32 rows share identities with other devices (python-verified this session) [F].
- caprip's `other` is the largest family on the device by rows (57 vs modem 43) [F]. The capri/caprip row delta is exactly 13: +9 tbase rows, +5 cm* rows (12 vs 7), -1 vendor/firmware row (capri's G10-only `aw882xx_mono_power.bin`) (python, this session) [F].
- Fleet-constant concentration: the 32 shared rows split into fleet-wide constants (venus tiny segments on 23-34 devices, cmbtfw10/11 + cmnv10/11 on 14, aw882xx_spk_reg on 15), the Moto trios (fngap64 6 segments on G10/G30/G9_Power; tbase b03/b04/b06 on 8 devices), the 5-device bengal tbase cohort, the Phone_1/Pro_1X venus cohort, and single-partner pairs (dc_mot_ov8856 with G10, cmnv12 with Phone_1/Pro_1X) [F].
- The three complete split-ELF sets in this family (fngap64 phnum 8 ELF64, tbase phnum 8 ELF32, venus phnum 20 ELF32) each satisfy mdt = b00 + b01 exactly, and every set is complete - no interior gaps anywhere in this family [F, python model checks this session].
- Family grammar contrast [F]: `tz` (5 rows: devcfg/hyp/keymaster/tz/uefisecapp images), `bt` (11 rows: ap*/cr* + bluetooth.img) and `modem` (43 rows: 29 modem*, 6 ipa_fws, 5 scuba_ipa_fws segments, fsg, modemr, modemuw) absorb their grammatical namesakes; everything else lands here. The modem family's ipa_fws/scuba_ipa_fws twin-build structure is documented in cluster D.

## ISA and interface facts

- venus: Xtensa (EM_XTENSA 94) per the parsed public build and #2058, cited via #1264; kernel reset path XTSS/AR50_LITE for this generation [F]; no disassembly performed [N].
- fngap64: 64-bit TrustZone application (ELF64 arithmetic on caprip's own b00; `ca64bit` in the public FP4 TA build string). The FP4 public instance runs on the applications processor under QSEE with a documented TCI command surface (0x00-0x23) and the Pangu R60C matching algorithm [F public prior art via #1264]; caprip's own TA bytes were not inspected - the target ISA of its executable segment is AArch64 per the TA class [I], no disassembly performed.
- tbase: ELF32 split image (arithmetic above), Trustonic t-base/Kinibi TEE OS per the public identity and packaging witnesses [I]; the executable ISA of the t-base core is not publicly documented for this build and was not inspected [N].
- cm* TLVs: Qualcomm combo-chip firmware in the TLV format the mainline btqca driver downloads to WCN3950 controllers (driver interface [F]; the TLV container format itself is un-RE'd [N]). The .ver files are 33 B version records only Moto devices carry [F per #1264].
- djn1/aw882xx/camera bins: controller firmware and calibration/configuration data for the Novatek touch IC, the Awinic amp DSP and the camera HAL (Arcsoft/CamX stack); not executable firmware for the applications processor [I].
- prov.img/storsec.img/dsp.img: recorded db_type ELF64 [F cell]; the ELF class of the device files was not verified (no payload fetched) [N].
- The census records `isa_identified` EMPTY and `interface_documented=n` on all 57 rows - honestly un-RE'd at row level; this doc's interface facts come from public trees, not from the blobs [F].

## Honest negatives ([OPEN])

- No payload of this device was fetched or analyzed (metadata-only; all 57 files exist in the corpus as hashes only). The only binaries touched were the six public linux-firmware qca files, and only their sizes and md5s.
- caprip's phdr-level facts (fngap64 ELF64/phnum 8, tbase ELF32/phnum 8, venus ELF32/phnum 20 with phdrs 11-18 file-data-less) are derived from exact size laws plus the public generational witness - not from caprip's own mdt bytes. Program-header dumps of the real `venus.mdt` (8,220 B), `fngap64.mdt` (7,464 B) and `tbase.mdt` (7,260 B) remain the direct proof and are [OPEN].
- No ISA proof from the blobs: nothing was disassembled; Xtensa/AArch64 verdicts rest on public parses and kernel trees; `isa_identified` stays EMPTY on all 57 rows.
- tbase: no Moto-specific public document names the trustlet; the Trustonic identity rests on naming, container grammar and the Samsung msm8916 packaging witness [I]. The dual-TEE service split (what runs under QTEE/tz.img vs tbase) is unknown.
- dsp.img content is unverified; its relationship to the modem-partition adsp image (#1276) and cdsp family is [OPEN].
- Data.msc's role is a hypothesis (EFS/NV container per #1228 [I]); no public format documentation exists.
- None of caprip's six 12/13-branch cm* files byte-matches the mainlined linux-firmware builds; the 7,583 B cmbtfw13.tlv vs 36,927 B public size gap is unexplained (different patch level, chip stepping, or a partially-populated TLV) [OPEN].
- The `djn1` prefix, `dc_mot_` prefix, and the s/t suffix semantics of cmnv13s/cmnv13t are unexpanded; the NT36525C-to-panel pairing (tianma vs txd) is not resolvable from the corpus.
- The ILITEK pair, NT36xxx criteria CSVs, dual_golden_* and vidhance_calibration corpus absences are unexplained (harvest scope vs matrix filter) [OPEN].
- The `tbase.mdt`/`tbase.b00` db_type=ELF64 cells conflict with the exact 52+8x32 ELF32 arithmetic - census detection error or a non-ELF-class meaning of the field; flagged for the lead [F tension].
- Which fingerprint sensor SKU (Chipone vs FPC) the census build pairs with is unknown; both HALs ship [F manifest].
- The 2022-generation tbase cohort SoCs (G_Stylus_5G-2-2022, Moto_G_5G_2024, Moto_G_Stylus_5G) and the bengal siblings' inventory SoC cells are not adjudicated here (empty/wrong cells flagged above) [I].

## What would upgrade this finding

1. Extract the stock radio partitions (dsp/prov/storsec) and modem partition, byte-verify all 57 census md5s, and dump the ELF header tables of `venus.mdt`, `fngap64.mdt` and `tbase.mdt` - expect venus ELF32 e_phnum 20 with phdrs 11-18 p_filesz 0, fngap64 ELF64 e_phnum 8, tbase ELF32 e_phnum 8 - converting all three structural derivations from [I] to direct [F].
2. Dump the 32 MiB `dsp.img` filesystem to settle what the radio `dsp` partition carries on caprip.
3. Locate a caprip touch-init script (pnangn-style `load_touch.sh` in a caprip device tree or Moto kernel source) to confirm the NT36525C panel pairing and the ILITEK alternate-SKU handling.
4. RE the `cm*` TLV container against the mainline btqca download flow (WCN3950 patch series) and record the WCN3950 command grammar; fetch linux-firmware release history to date caprip's 1.2.0/1.3.0 builds against public drops.
5. RE the tbase image format (Trustonic Kinibi/MobiCore public research) and dump the 348,285 B b02 payload structure - the only device-class Trustonic TEE payload the corpus holds byte-identical across 5 devices.
6. Trace the harvest exclusion of the manifest-listed but census-absent files (ILITEK pair, NT36xxx CSVs, dual_golden_*, vidhance_calibration) in the census builder.

## RULE 0 record

- CLAIM posted 2026-11-21T11:58:21Z as the first comment (confirmed first by re-read at 11:58:27Z; no competing claim).
- SEARCH (Gate -1) posted 2026-11-21; DELTA (Gate 0) posted 2026-11-21; work started only after both.
- All census numbers are awk/python3 -I outputs on `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) and `device-inventory.csv` at feat/open-device-site 7c0f9e3, this session; every cluster sum, subfamily sum, size law, expected-set model check and share-roster re-verified with python3 before writing. Web fetches dated 2026-11-21: LineageOS/android_device_motorola_caprip proprietary-files.txt (lineage-22.2, lines 17-18, 167-175, 186-193, 273-284 cited), linux-firmware WHENCE (git.kernel.org; WCN3950 section lines 5343-5356 with version strings BTFM.CMC.1.2.0-00218-QCACHROMZ-2 and BTFM.CMC.1.3.0-00184-QCACHROM-1), public builds `qca/cmbtfw12.tlv`, `qca/cmbtfw13.tlv`, `qca/cmnv12.bin`, `qca/cmnv13.bin`, `qca/cmnv13s.bin`, `qca/cmnv13t.bin` (git.kernel.org plain; sizes and md5s recorded above), the Samsung msm8916-common Android.mk tbase fragment (GitHub code search), the Azeria-Labs Kinibi identity page (web search). Web searches dated 2026-11-21 with exact queries recorded in the SEARCH comment. The venus-6.0 public-build parse and the flash-base.sh, load_touch.sh, FP4 fngap64 and #2058/#2052 citations are taken from #1264 (fetched there 2026-11-21), cited not re-derived.

Nothing in this document is legal advice; no proprietary payload bytes were fetched, stored or committed - only sizes, md5s, ELF-header arithmetic, public-build metadata and public-source quotations.
