# Device census — Banana Pi M5 tablet image (`M5_Tablet`, `m5_tab`, Amlogic S905X3)

Issue adineo-cmd/open-device#515. Claimed `CLAIM ZC-2 zcode 2026-11-21T10:32:39Z`.
Work dates: 2026-11-21/22 (all searches and fetches recorded with dates below).
Gate -1 verdict: **NEW**. Gate 0 verdict: **DELTA** (Amlogic image tooling is cited
methodology prior art; no published census of this image exists).
Deliverables: this note plus `data/fleet/M5_Tablet-census.csv`
(sha256 `85de1f7f08b97d75daead0d725ddfa54585ef28edc94b1704a834fdb2fb786e1`, 2,749 rows).

## Device chosen and why

Non-phone SBC required for the site's every-device-class scope. Package state
was `inventory_only`: the upstream database records the identity but publishes
**zero** blob records for it (blobs column NULL), so the per-file census below
is a first-party recovery from the official public image.

## Identity, hardware and SoC (issue checklist items 2 and 3)

- Codename confirmation from the inventory:
  `upstream-contribution/blob-database/device-inventory.csv:18` —
  `bananaPI,M5_Tablet,m5_tab,Amlogic S905X3,builds.csv,...` with
  `build_codename=m5_tab`, `soc=Amlogic S905X3` (soc_source=builds.csv).
  Cross-checked against upstream itself: LibrePhone `builds.csv` lines 3-4
  (fetched from codeberg rsavoye/librephone main, 2026-11-21) —
  `BananaPI,M5_TV,m5,fails,,Amlogic S905X3,2020` and
  `BananaPI,M5_Tablet,m5_tab,fails,,Amlogic S905X3,2020`; `devices.sql`
  rows 428-429 carry both devices with the **blobs column NULL** and
  released-year 2020; `count.csv` has no bananaPI rows (grep, 0 hits) —
  consistent with `in_count_csv=n`.
- `type=sbc` — hardware fact: the Banana Pi M5 is a credit-card SBC board —
  wiki.banana-pi.org (fetched 2026-11-21): "single-board computer from
  Banana Pi in 2020"; Amlogic S905X3 64-bit quad-core Cortex-A55, Mali-G31
  GPU, 4GB LPDDR4, 16GB eMMC, 4x USB 3.0, 1 GbE, HDMI. CONFIRMED.
- `build_variant=mobile` — image fact: the official download table lists a
  **tablet** Android image (`2024-04-29-bpi-m5-m2pro-tablet-android9.img`,
  1,384,558,948 B) separate from the box/ATV variant — the wiki records
  "2023-03-01 release, box variant image" and "tablet variant image" as
  distinct downloads and publishes per-variant md5 files
  (`md5_2023tab.txt` = `b92fc473…`, `md5_2024tab.txt` = `05336d8f…`,
  `md5_2023box.txt` = `893c184b…`, fetched from the official Drive folder,
  2026-11-21). The mobile variant is the standard-Android tablet build, as
  opposed to the ATV (`m5`/M5_TV) build. CONFIRMED — the downloaded zip's
  md5 equals the published `md5_2024tab.txt` value exactly.
- SoC second sources (2026-11-22): S905X3 = quad Cortex-A55, **12 nm**,
  Mali-G31 MP2 (Odroid C4 hardware page + CNX articles + SDMC Tech
  solution-provider page); stock frequency 1908 MHz per CoreELEC's vendor
  dts (`stock_freq = <1908>;`) with the advertised "2.0xxGHz" and a 2016 MHz
  OPP as the tuning range.
- Radio correction (adversarial audit finding, 2026-11-22): the M5 has **no
  onboard WiFi/BT** — official docs list "Optional WiFi USB dongle" and an
  RTL8822CS 2T2R WiFi/BT expansion board, the official forum states the M5
  ships without embedded WiFi, and CoreELEC's vendor dts
  (`sm1_s905x3_bananapi_m5.dts`) `/delete-node/`s the aml_wifi and aml_bt
  nodes. Notes implying an AMPAK AP6256 module are wrong for this board.

## What the repo already knew (Gate -1)

- coverage-matrix.csv: 0 rows for M5_Tablet and M5_TV ("0 matrix rows" exact).
- `data/fleet/devices-001-222.csv`: `M5_Tablet,bananaPI,Amlogic
  S905X3,none,,0,,listed-not-populated,P3; extract22.2=fails` (M5_TV same).
- `site/data/device-types.csv:58` — `M5_Tablet,sbc,mobile,"m5_tab, same
  Banana Pi M5 SBC board as M5_TV (m5), tablet image, mobile variant"`.
- `site/tests/test_data_files.py:25-26` assert M5_TV/M5_Tablet are NOT in
  upstream-counts.csv — consistent with `state=inventory_only`
  (derived in `src/lib/data.ts:81`).
- `research/devices/M5_Tablet.md` never existed in checkout or history
  (`docs/REPO-STATE-MAP.md:15` — Device package family NEW).

## Support status (public software stacks, 2026-11-22)

| stack | status | evidence |
|---|---|---|
| Mainline Linux | SUPPORTED | torvalds `arch/arm64/boot/dts/amlogic/meson-sm1-bananapi-m5.dts` (`model = "Banana Pi BPI-M5"`, HTTP 200) + `meson-sm1.dtsi` |
| Armbian | OFFICIAL (mainline only) | `armbian/build config/boards/bananapim5.conf`: `BOARDFAMILY="meson-sm1"`, `KERNEL_TARGET="current,edge"` — no legacy vendor target |
| CoreELEC | OFFICIAL (vendor kernel) | `bl301.conf` line 19 `bananapi_m5=Bananapi_M5`; vendor dts `sm1_s905x3_bananapi_m5.dts` (`model = "Sinovoip Bananapi-M5"`, `coreelec-dt-id`) in `CoreELEC/common_drivers` |
| LineageOS | none | wiki devices list has no bpi-m5 page (404 probes 2026-11-21) |
| postmarketOS | none | pmOS wiki (moved to wiki.nura.eco) has no Banana Pi M5 page (`missing: true` via API); pmaports tree has 0 banana device packages (tree API, 2026-11-22) |
| Android 9 (vendor) | OFFICIAL images | wiki download table: tablet image (this census) + box variant + Ubuntu/Debian 2023-08-30 aarch64 images |

## The image census (issue checklist item 1)

Source: the official wiki-linked Google Drive zip
`2024-04-29-bpi-m5-m2pro-tablet-android9.img` package — 680,609,611 B zip,
**md5 `05336d8fcc805f6003de4f471f847ce0` = the published `md5_2024tab.txt`
value exactly** (the wiki's md5 covers the zip; the inner image's own
md5 is `90cdb638e606bdab91057204f4055ec7`, sha256
`201aee4c02c732871da1672e65355a7d67ea4c3f751bcc3fc742159b36939b2a`).
Extraction integrity is additionally proven by the zip's central-directory
CRC32 (`0775aca4`) matching the extracted stream.

The inner `.img` is **not** a raw disk — it is an Amlogic update container
(aml_image v2: magic `0x8d6aae68`-family header, then a 0x240-byte-stride
table of records `[payload offset u64][payload size u64][item type @+0x10]
[item name @+0x110]`, closed by 48-byte VERIFY blocks). Decoded contents:

| item | payload bytes | magic / type | census |
|---|---:|---|---|
| `bootloader` / `DDR` / `UBOOT` | 1,538,928 each | custom (`4017996c…`) | **byte-identical payload shipped three times** (sha256 `8119d898…` each) |
| `aml_sdc_burn` (UBOOT-type) | 1,539,440 | custom | sd-card burn u-boot variant |
| `aml_sdc_burn` (ini-type) | 602 | text (`3b0a3b41…`) | burn config |
| `_aml_dtb` / `meson1` | 153,600 each | `AML_` wrapper + DTB | **byte-identical** (sha256 `9196302a…` each) |
| `boot` | 10,086,400 | `ANDROID!` | kernel/ramdisk header fields do not fit the partition (Amlogic-custom boot container) — magic and page_size 2048 only [N] |
| `recovery` | 16,783,360 | `ANDROID!` | same header form [N] |
| `dtbo` | 4,819 | dt_table `d7b7ab1e` | Samsung/Amlogic dt_table variant |
| `logo` | 1,324,848 | custom (`a473bcae…`) | boot-logo blob |
| `odm` | 540,748 | android-sparse → raw ext4 134,217,728 B | **4 files** (etc/fs_config_{dirs,files}, selinux precompiled_sepolicy + sha256 file) |
| `product` | 4,218,956 | android-sparse → raw ext4 134,217,728 B | **11 files** (DLNA.apk 1,327,119 B, Miracast.apk 251,611 B, …) |
| `system` | 1,136,357,596 | android-sparse → raw ext4 1,342,177,280 B | **2,150 files** / 1,129,652,940 B (app/, priv-app/, framework/, lib64/, etc/) |
| `vendor` | 211,988,652 | android-sparse → raw ext4 469,762,048 B | **567 files** / 207,153,247 B |
| `vbmeta` | 4,096 | `AVB0` | AVB metadata |
| `platform` (conf) | 155 | text ("Platform") | platform config |

Method: stdlib-only `python3 -I` (chunked download, zip extraction, sparse
chunk walk, magic probes) + `debugfs 1.47.0` (`ls -l` per directory over the
converted raw ext4 partitions, recursive walk, symlinks skipped). The CSV
carries one row per container item (with sha256 for payloads ≤64 MB) plus
one row per ext4 file (sizes only; per-file sha256 out of scope for ~2,700
files — recorded as `hash_note=size-only ext4 listing`). Every number above
comes from a command output in the census session; the CSV is the durable
per-file layer the upstream DB lacks (its blobs column is NULL for this
device).

The recovery item ships a separate 16,783,360 B `ANDROID!` image while
`boot` ships 10,086,400 B — and no `data`/userdata item exists in the
container (shipped empty), consistent with a flashable factory image.

## Prior art (RULE 0, with adversarial audit)

Recorded queries (2026-11-21/22): GitHub repo search `m5_tab` → only
M5Stack Tab5 (ESP32-P4) products — a name confounder with the Banana Pi
codename, documented; `banana pi m5 firmware`, `S905X3 image census`,
`bpi-m5 android9 img census`, `"bpi-m5" "android9"` → no per-file census of
any BPI-M5 Android image; freaktab/ATVTW/web → no enumerating thread.
Methodology prior art that exists and is cited, not claimed as novel: the
Amlogic image-partition tooling family (ampart and the aml_image/aml_autoscript
unpack ecosystem) and CoreELEC's Amlogic device trees. Aggregate context:
arXiv:2410.11075 covers vendor blobs at aggregate level only. The adversarial
audit (2026-11-22) re-attacked identity, hardware-type, prior-art, kernel and
repo-number claims; the identity claim survived on the DB rows themselves
(`m5_tab` codename + bananaPI vendor in builds.csv/devices.sql), with one
correction adopted: the onboard-radio premise was broken (no AP6256 on M5).

## Honest negatives

1. The upstream LibrePhone DB records the device but publishes no blob rows
   (devices.sql blobs NULL; sizes.csv/sizes-22.2.csv/binfiles_devices.csv
   have no bananaPI rows) — the DB-side gap is what this census fills.
2. `extract 22.2 = fails` upstream: no 22.2-era extraction exists for this
   device; the Android 9 tablet image is the only public artifact set.
3. The `boot`/`recovery` `ANDROID!` headers carry size fields that do not
   fit their partitions (17,301,504 B "kernel" in a 10,086,400 B partition)
   — Amlogic-custom boot containers, not decoded here [N].
4. The wiki's published md5 files cover the zip packages, not the inner
   images; per-image md5s would need publishing upstream [N].
5. No mainline-basis note in the inventory (`mainline_basis_or_note` empty)
   despite mature mainline SM1 support — reported for the lead
   (`device-inventory.csv:18` could carry `meson-sm1 mainline dts`).
6. Google Drive throttling: the official image download required resumable
   chunked fetching across quota windows; three subagent attempts died to
   infrastructure timeouts and an initial assembly was corrupted by two
   concurrent downloader instances appending to the same chunk files — the
   final census came from a clean single-instance segment download verified
   by the published zip md5.
7. Per-file sha256 inside the ext4 partitions is out of scope for this
   session (~2,700 files); the CSV carries exact sizes and paths, and the
   container items carry full sha256.

## RULE 1 findings

- No dangling references or contradictory counts found for this device: 0
  matrix rows, no count row, inventory_only state and the fleet placeholder
  all agree across the in-repo occurrences.
- `data/fleet/M5_Tablet-census.csv` is NEW — the per-file layer the DB lacks.
- Reported for the lead: `device-inventory.csv:18` could record the mainline
  dts basis (`meson-sm1-bananapi-m5.dts` in torvalds) in
  `mainline_basis_or_note`, matching how P2 devices are annotated.

## Reproduction

```
curl -sL https://wiki.banana-pi.org/Banana_Pi_BPI-M5            # download table + specs
cat dl/md5_2024tab.txt                                           # 05336d8fcc805f6003de4f471f847ce0 (zip)
md5sum <downloaded zip>                                          # must equal the above
python3 -I -c "import zipfile; print(zipfile.ZipFile('<zip>').infolist())"
python3 -I scripts/parse_image.py <img> out.json                 # container probe
python3 -I scripts/build_census515.py                            # TOC decode + sparse->raw + debugfs walk
sha256sum data/fleet/M5_Tablet-census.csv                        # 85de1f7f08b97d75daead0d725ddfa54585ef28edc94b1704a834fdb2fb786e1
```
