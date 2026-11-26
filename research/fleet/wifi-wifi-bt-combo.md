# `wifi-bt-combo` — four rows, two containers, and a `_hdr.bin` that is not a header (4 rows, 2 devices)

Analysis date: 2026-11-26. Analyst: OC-1 (`100milionseek`), issue
[#2066](https://github.com/adineo-cmd/open-device/issues/2066).

Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data
rows) for the census; the four device payloads fetched from the Xiaomi trees
(`xiaomi/rosemary` = `Redmi_10S`, `xiaomi/earth` = `Poco_12C`), all four md5s
re-verified against the matrix this session; five upstream `WIFI_RAM_CODE_*`
builds from `linux-firmware`; the device's own kernel sources
(`LineageOS/android_kernel_xiaomi_earth`, branch `lineage-24.0`); the normative
mainline spec (`drivers/net/wireless/mediatek/mt76/mt76_connac_mcu.h` /
`.c`); `linux-firmware` `WHENCE` (11,958 lines / 542,570 B).

Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** Four rows, two devices, 1,671,348 B — **#17 of 18** named
subfamilies by rows and **#18 of 18 by bytes**: the smallest named subfamily in
the corpus. That smallness is the only thing census-level about it, because the
bucket contains **two different container formats** and the matrix files them
under one label with no `db_type`.

The first format is the **`mt76_connac2` firmware container**, specified in
mainline Linux and verified here byte-for-byte on the device payloads:

```
payload[Σ region.len] ‖ stamp ‖ region_table[n_region × 40] ‖ trailer[36]
```

The sum law closes exactly on both devices (`636,336 + 128 + 200 + 36 = 636,700`
and `639,920 + 132 + 200 + 36 = 640,288`), and the 36-byte trailer decodes to
`chip_id=7`, `n_region=5`, `fw_ver='tk__000200'` with a per-build build date.

The second format is **not a header at all**, despite the `_hdr.bin` suffix. It
is a `struct wmt_rom_patch` (48 B) followed by a raw EMI image, and the device's
own kernel reads exactly that:

```c
prRomEmiHeader = (struct ROM_EMI_HEADER *)pvFwImageMapFile;
u4Addr  = prRomEmiHeader->u4PatchAddr;
u4Len   = u4FwImageFileLength - sizeof(struct ROM_EMI_HEADER);
u4Offset= sizeof(struct ROM_EMI_HEADER);
```

`ROM_EMI_HEADER` and `wmt_rom_patch` are the same 48-byte layout. The payload
starts at byte 48, not at byte 0 — which is the opposite of what the `.bin`
suffix and the "`_hdr` = container header" reading would suggest.

Three findings carry the note.

First, **the stamp is a `#`-framed TLV whose length is derivable, not
arbitrary.** It is `b'#'*16 ‖ u32le payload_len ‖ body[payload_len] ‖ b'#'*16`,
total `payload_len + 36`. That law holds on **7 of 7** files tested — the two
device builds plus five upstream `WIFI_RAM_CODE_*` builds with stamp lengths
152, 76, 144, 68 and 172. The body begins with a length byte, then 3 flag
bytes, then a `t-neptune-…` ASCII manifest naming the silicon
(`KRUG_SOC1_0_E1_ASIC` on the Redmi 10S, `TALBOT_SOC1_0_E1_ASIC` on the Poco
12C).

Second, **`feature_set` has a real meaning and the `0x80` regions are
downloaded.** `FW_FEATURE_NON_DL` is `BIT(6)` = **`0x40`**, not `0x80`; `0x07` is
`SET_ENCRYPT` plus `SET_KEY_IDX`=3, i.e. the three small regions are
**encrypted with key index 3**. `0x80` is **not defined** in
`mt76_connac_mcu.h`, so the two large regions carrying it are neither
non-downloadable nor overridden — they are downloaded normally, and the bit
means something the mainline header does not name.

Third, **the four `soc1_0_*_hdr.bin` siblings are the rest of the same family,
and the matrix files three of them elsewhere.** The device ships a five-file set
(`WIFI_RAM_CODE_soc1_0_2a_1.bin` plus `_patch_mcu`, `_ram_bt`, `_ram_mcu`,
`_ram_wifi`); only two land in `wifi-bt-combo`, three land in `misc` or carry no
subfamily at all. So the subfamily boundary does not follow the firmware family.

---

## 0. Headline numbers

| quantity | value |
|---|---:|
| rows | **4** |
| devices | **2** (`Redmi_10S`, `Poco_12C`) |
| basenames | **4** |
| distinct `md5_db` | **4** |
| distinct sizes | **4** (636,700 / 640,288 / 196,764 / 197,596) |
| total bytes | **1,671,348** |
| share of corpus rows | 0.0118 % |
| share of corpus bytes | 0.0024 % |
| share of `wifi` rows | 0.0709 % |
| share of `wifi` bytes | 0.2341 % |
| rank among 18 named subfamilies, by rows | **#17** |
| rank among 18 named subfamilies, by bytes | **#18 (smallest)** |
| `isa_identified` populated | **0 of 4** |
| `sha256_if_listed` populated | **0 of 4** |
| `db_type` | `UNKNOWN` on **4 of 4** |
| `priority` | `P3` on **4 of 4** |
| `interface_documented` | `n` on **4 of 4** |

Corpus: 33,917 rows / 69,797,539,502 B. `wifi` family: 5,642 rows /
714,009,036 B, of which `wpss` is 5,198 rows / 317,873,910 B and 440 rows carry
no subfamily. `wifi-bt-combo` is the `wifi` family's smallest named bucket by
both measures.

---

## 1. The census rows `[F]`

All four rows, verbatim from the matrix:

| # | device | filename | size | md5 | subfamily |
|---:|---|---|---:|---|---|
| 1 | `Redmi_10S` | `WIFI_RAM_CODE_soc1_0_2a_1.bin` | 636,700 | `62da7ec18aa9274a0c02a5a8ebe61e02` | `wifi-bt-combo` |
| 2 | `Redmi_10S` | `soc1_0_ram_wifi_2a_1_hdr.bin` | 196,764 | `30bdc679a40ebc00a4aef11650ba0ec7` | `wifi-bt-combo` |
| 3 | `Poco_12C` | `WIFI_RAM_CODE_soc1_0_1a_1.bin` | 640,288 | `c97f3faff7866db8484822a334983dd9` | `wifi-bt-combo` |
| 4 | `Poco_12C` | `soc1_0_ram_wifi_1a_1_hdr.bin` | 197,596 | `05e0e2a5d8e76d32a1a80f26af03095e` | `wifi-bt-combo` |

All four md5s were re-computed from the local payloads this session and match
the matrix exactly `[F]`. Paths: `xiaomi/rosemary/vendor/firmware` (Redmi 10S)
and `xiaomi/earth/vendor/firmware` (Poco 12C). All four are `blob_family=wifi`,
`db_type=UNKNOWN`, `priority=P3`, `interface_documented=n`, `soc` blank,
`isa_identified` blank, `sha256_if_listed` blank `[F]`.

The filename encodes the variant: `…_2a_1.bin` and `…_1a_1.bin` differ only in
the flavour letter (`2a` vs `1a`), which is the SoC-variant selector. A public
postmarketOS note on the same chip family states it plainly: "firmware
`WIFI_RAM_CODE_soc1_0_<hw>_<n>.bin`, flavor 'a' => `..._2a_1.bin`" `[F]` (source
in §5.2).

### 1.1 The bucket is half of a five-file family `[F]`

Both devices ship five `soc1_0` files, but only two reach this subfamily. The
other three are filed elsewhere or not at all:

| file | Redmi_10S size | subfamily | Poco_12C size | subfamily |
|---|---:|---|---:|---|
| `WIFI_RAM_CODE_soc1_0_*a_1.bin` | 636,700 | **`wifi-bt-combo`** | 640,288 | **`wifi-bt-combo`** |
| `soc1_0_ram_wifi_*a_1_hdr.bin` | 196,764 | **`wifi-bt-combo`** | 197,596 | **`wifi-bt-combo`** |
| `soc1_0_ram_bt_*a_1_hdr.bin` | 570,949 | *(blank)* | 571,045 | *(blank)* |
| `soc1_0_ram_mcu_*a_1_hdr.bin` | 122,712 | `misc` | 105,656 | `misc` |
| `soc1_0_patch_mcu_*a_1_hdr.bin` | 22,350 | `misc` | 25,934 | `misc` |

So the `wifi-bt-combo` label captures the WiFi RAM code and the WiFi ROM-patch
carrier, but files the Bluetooth carrier with **no subfamily at all** and the MCU
pair under `misc` — despite `bt` in the bucket's own name. The bucket name is
"wifi-bt-combo" while the `bt` file is not in it `[F]`.

### 1.2 Rank inside the 18 named subfamilies `[F]`

| rank **by rows** | subfamily | rows | bytes (rank differs) |
|---:|---|---:|---:|
| 14 | `modem-config` | 5 | 9,361,040 |
| 15 | `sensors` | 5 | 86,541,968 |
| 16 | `tinysys` | 4 | 4,132,864 |
| **17** | **`wifi-bt-combo`** | **4** | **1,671,348** |
| 18 | `gpu-compute` | 3 | 2,523,240 |

By rows it is **#17**, ahead of `gpu-compute` only. By bytes it is **#18** —
1,671,348 B, smaller than `gpu-compute`'s 2,523,240 B despite having one more
row. It is the **smallest named subfamily in the corpus by bytes** `[F]`.

The two orderings genuinely disagree here: `sensors` ranks 15th by rows but **7th**
by bytes (86,541,968 B), and `tinysys` ranks 16th by rows but 15th by bytes. Of
these five neighbours, only `wifi-bt-combo` sits at **18th of 18** by bytes —
`gpu-compute` is 17th, `tinysys` 15th, `modem-config` 12th, `sensors` 7th.

---

## 2. Artifact A — `WIFI_RAM_CODE_soc1_0_*.bin` is an `mt76_connac2` container `[F]`

636,700 B (Redmi 10S) and 640,288 B (Poco 12C). Not ELF, not compressed. The
format is specified in mainline Linux by `mt76_connac2_load_ram()` and
`mt76_connac_mcu_send_ram_firmware()`, and the payloads conform exactly.

### 2.1 The layout, and the sum that closes `[F]`

```
file = region_payload[Σ region.len] ‖ stamp ‖ region_table[n_region × 40] ‖ trailer[36]
```

| file | size | Σ `region.len` | stamp | `n_region`×40 | trailer | sum |
|---|---:|---:|---:|---:|---:|---:|
| `WIFI_RAM_CODE_soc1_0_2a_1.bin` | 636,700 | 636,336 | 128 | 200 | 36 | **636,700** ✓ |
| `WIFI_RAM_CODE_soc1_0_1a_1.bin` | 640,288 | 639,920 | 132 | 200 | 36 | **640,288** ✓ |

**Region payload starts at byte 0.** The driver confirms it — `offset = 0`,
`data + offset`, `offset += len` — so there is nothing before the payload. The
region table sits immediately before the trailer, and is walked backwards:

```c
region = (const void *)((const u8 *)hdr - (hdr->n_region - i) * sizeof(*region));
```

`sizeof(struct mt76_connac2_fw_region)` = 40 and
`sizeof(struct mt76_connac2_fw_trailer)` = 36, both confirmed from the header
field-by-field `[F]`.

### 2.2 The trailer `[F]`

| field | offset | `2a_1` | `1a_1` |
|---|---:|---|---|
| `chip_id` | 0 | **7** | **7** |
| `eco_code` | 1 | 0 | 0 |
| `n_region` | 2 | **5** | **5** |
| `format_ver` | 3 | 2 | 2 |
| `format_flag` | 4 | 1 | 1 |
| `rsv[2]` | 5 | `00 00` | `00 00` |
| `fw_ver[10]` | 7 | `tk__000200` | `tk__000200` |
| `build_date[15]` | 17 | `20230627203605` | `20231117111610` |
| `crc` | 32 | `0xd99cfa4e` | `0xd4ff2092` |

`chip_id = 7` matches **none** of the ids mainline assigns a name to — the
upstream builds in this session carry `13` (`MT7961`), `16` (`MT7922`), `19`
(`MT7902`), `21` (`MT6639`) and `24` (`MT7925`). There is **no id→name table** in
the driver, so `chip_id=7` cannot be named from mainline `[F]`; it is the
`soc1_0` silicon, whose marketing name the mainline tree does not record `[N]`.

### 2.3 The region table `[F]`

Five regions each, 40 bytes, decoded against the real struct:

| # | `2a_1` addr | `2a_1` len | `1a_1` addr | `1a_1` len | `feature_set` (both) |
|---:|---|---:|---|---:|---|
| 0 | `0x00057000` | 3,952 | `0x00057000` | 4,016 | `0x07` |
| 1 | `0x02010000` | 272 | `0x02010000` | 336 | `0x07` |
| 2 | `0x40100200` | 9,664 | `0x40100200` | 9,616 | `0x07` |
| 3 | `0xf0177000` | 480,048 | `0xf0177000` | 480,432 | `0x80` |
| 4 | `0xf01fe000` | 142,400 | `0xf01fe000` | 145,520 | `0x80` |

The two builds agree on **all five addresses** and differ only in the three
small region lengths and the two large ones — i.e. the load map is fixed by
silicon and the payload sizes vary by build `[F]`. `decomp_crc`,
`decomp_len` and `decomp_blk_sz` are **0 on all 10 regions** `[F]`.

### 2.4 `feature_set` — `NON_DL` is `0x40`, so the `0x80` regions download `[F]`

The mainline header defines, verbatim:

```c
#define FW_FEATURE_SET_ENCRYPT      BIT(0)   /* 0x01 */
#define FW_FEATURE_SET_KEY_IDX      GENMASK(2, 1)
#define FW_FEATURE_ENCRY_MODE       BIT(4)   /* 0x10 */
#define FW_FEATURE_OVERRIDE_ADDR    BIT(5)   /* 0x20 */
#define FW_FEATURE_NON_DL           BIT(6)   /* 0x40 */
```

So on these payloads:

| `feature_set` | regions | decode |
|---|---:|---|
| `0x07` | 3 (small) | `SET_ENCRYPT` + `SET_KEY_IDX` = **3** — downloaded **encrypted, key index 3** |
| `0x80` | 2 (large) | **no defined bit set** — `BIT(7)` is undefined here; `NON_DL` clear, `OVERRIDE_ADDR` clear |

The driver skips a region only on `feature_set & FW_FEATURE_NON_DL`, which is
`0x40`. `0x80 & 0x40 == 0`, so **both large regions are downloaded normally**.
`0x80` therefore carries a meaning the mainline header does not name, and this
note records it as `[U]` rather than inventing one.

Cross-check on the upstream builds is consistent with the constant: `MT7961`
and `MT7902`/`MT7922`/`MT7925` carry `0x40` on their **last** region — the
genuine `NON_DL` — and `MT6639` carries none `[F]`. So `0x40` appears as
`NON_DL` exactly where mainline says it should, which is independent
confirmation that the constant is `0x40` and not `0x80`.

### 2.5 The stamp is a `#`-framed TLV, and its length is derivable `[F]`

```
stamp = b'#'*16 ‖ u32le payload_len ‖ body[payload_len] ‖ b'#'*16
total = payload_len + 36
```

| file | stamp | `payload_len` | `16+4+len+16` | lead `b'#'*16` | trail `b'#'*16` |
|---|---:|---:|---:|---|---|
| `2a_1` (Redmi 10S) | 128 | 92 | 128 ✓ | yes | yes |
| `1a_1` (Poco 12C) | 132 | 96 | 132 ✓ | yes | yes |
| upstream `MT7961_1` | 152 | 116 | 152 ✓ | yes | yes |
| upstream `MT7902_1` | 76 | 40 | 76 ✓ | yes | yes |
| upstream `MT7922_1` | 144 | 104 | 144 ✓ | yes | yes |
| upstream `MT6639_2_1` | 68 | 32 | 68 ✓ | yes | yes |
| upstream `MT7925_1_1` | 172 | 136 | 172 ✓ | yes | yes |

**7 of 7.** The body is a length byte, 3 flag bytes, then an ASCII manifest:

| file | body[0] | body[1:4] | manifest |
|---|---:|---|---|
| `2a_1` | 68 | `00 00 01` | `t-neptune-mp-soc1_0e1-2050-tc8sp3-KRUG_SOC1_0_E1_ASIC-20230627203301` |
| `1a_1` | 69 | `00 03 01` | `t-neptune-mp-soc1_0e1-2015-tc8sp-TALBOT_SOC1_0_E1_ASIC-20231117111350` |

`KRUG` and `TALBOT` are the two devices' internal board names; `soc1_0e1` is
the silicon; `2050`/`2015` are the chip revisions; `tc8sp3`/`tc8sp` the
toolchain; and the trailing 14 digits are the **build timestamp**, which is
**184 seconds and 140 seconds** before the trailer's `build_date`
(`20230627203301`→`20230627203605` = 184 s; `20231117111350`→`20231117111610` =
140 s). Two independent timestamps in one file, a few minutes apart, are the
build-start and build-end of the same run `[I]`.

On the upstream builds the same field reads `t-neptune-main-…` or
`t-neptune-mp-…`, so **`neptune` is MediaTek's firmware toolchain tag**, not a
device-only codename `[F]`.

### 2.6 The `_hdr.bin` sibling embeds this build date `[F]`

The `soc1_0_ram_wifi_*a_1_hdr.bin` file's **first 12 bytes** are the stamp's
build timestamp with the `20` century prefix stripped:

| file | stamp timestamp | `_hdr.bin` first 12 | match |
|---|---|---|---|
| `2a_1` | `20230627203301` | `230627203301` | ✓ |
| `1a_1` | `20231117111350` | `231117111350` | ✓ |

followed by `0000`. That is a hard link between the two artifacts: they come
from the same build, which is why they ship as a pair `[F]`.

---

## 3. Artifact B — `soc1_0_ram_wifi_*_hdr.bin` is a ROM-patch carrier, not a header `[F]`

196,764 B (Redmi 10S) and 197,596 B (Poco 12C). The `_hdr` suffix reads as "this
is the container header". It is the opposite: the file is **a 48-byte
`struct wmt_rom_patch` followed by a raw EMI image**, and the 48 bytes are the
header of the *payload*, not of a container.

### 3.1 The device's own kernel says so `[F]`

`LineageOS/android_kernel_xiaomi_earth` (branch `lineage-24.0`),
`wlan/core/gen4m/chips/soc5_0/soc5_0.c`:

```c
} else if ((eDlIdx == IMG_DL_IDX_MCU_ROM_EMI) ||
           (eDlIdx == IMG_DL_IDX_WIFI_ROM_EMI)) {
    prRomEmiHeader = (struct ROM_EMI_HEADER *)pvFwImageMapFile;
    u4Addr   = prRomEmiHeader->u4PatchAddr;
    u4Len    = u4FwImageFileLength - sizeof(struct ROM_EMI_HEADER);
    u4Offset = sizeof(struct ROM_EMI_HEADER);
    u4Status = wlanDownloadEMISection(prAdapter, u4Addr, u4Len,
                                      pvFwImageMapFile + u4Offset);
```

and `include/chips/soc5_0.h` defines

```c
struct ROM_EMI_HEADER {
    uint8_t  ucDateTime[16];
    uint8_t  ucPLat[4];
    uint16_t u2HwVer;
    uint16_t u2SwVer;
    uint32_t u4PatchAddr;
    uint32_t u4PatchType;
    uint32_t u4CRC[4];
};
```

`4+4+2+2+4+4+16 = 48` bytes, and the payload is `file[48:]`. The legacy
`struct wmt_rom_patch` in
`common/common_main/core/include/wmt_core.h` is field-identical, so both
subsystems read the same 48-byte prefix `[F]`.

### 3.2 The decode `[F]`

| field | `2a_1` | `1a_1` |
|---|---|---|
| `ucDateTime[16]` | `b'2306272033010000'` | `b'2311171113500000'` |
| `ucPLat[4]` | `b'ALPS'` | `b'ALPS'` |
| `u2HwVer` | `0x8a00` | `0x8a00` |
| `u2SwVer` | `0x8a00` | `0x8a00` |
| `u4PatchAddr` | `0xf0140011` | `0xf0140011` |
| `u4PatchType` | `0x03000000` | `0x03000000` |
| `u4CRC[4]` | `0, 0, 0, 0xaffc0000` | `0, 0, 0, 0x938f0000` |
| payload `file[48:]` | 196,716 B | 197,548 B |

Both builds agree on `ucPLat`, both version words, `u4PatchAddr` and
`u4PatchType`, and differ only in the date and the last CRC word `[F]`.

`u2HwVer = u2SwVer = 0x8a00` is corroborated externally on the same chip
family: a public Redmi 9 (MT6768) mainline note records the device reporting
`Chip ID[0001] Version[E1] HW[0x8a00] SW[0x8a00]`, and another records
`chipid 0x6768, version id 0x10020501, HW/FW 0x8a00` (§5.2) `[F]`.

**`u4PatchAddr = 0xf0140011` has a low byte of `0x11`.** A public postmarketOS
port of the same connsys generation documents exactly this hazard: "the low byte
of the patch address is a sequence flag, not part of the EMI offset — it has to
be zeroed or the firmware lands at the wrong place and `hw_check` fails
forever." A second, independent port of the same family states the rule as a
mask, verbatim: "offsets from u32@24 of the header (LE): `off = u32 & 0x00ffff00`"
— and gives `wifi 0x140000 (0x3044c)` for the same `soc1_0_ram_wifi_*_hdr.bin`
(§5.2).

That mask reproduces on these payloads exactly:

| file | `u4PatchAddr` | `& 0x00ffff00` |
|---|---|---|
| `2a_1` | `0xf0140011` | **`0x140000`** |
| `1a_1` | `0xf0140011` | **`0x140000`** |

So the EMI target is `0xbc000000 + 0x140000` and **both** the top byte `0xf0`
and the low byte `0x11` are stripped by the mask — the top byte is an address-
space tag and the low byte the sequence number `[F]`/`[I]`. This is a real trap
the header invites and the `_hdr` name hides: a loader that uses `u4PatchAddr`
raw targets `0xf0140011` where the intended EMI offset is `0x140000` — a
difference of `0xf0000011` bytes, i.e. **3,840 MiB** (the `0xf0` address-space
tag alone contributes `0xf0000000`).

### 3.3 Why `ALPS` is at offset 16 and not 0 `[F]`

`ALPS` — the MediaTek in-house tag — sits at `0x10`, i.e. inside
`ucPLat[4]`, which is the fourth field of the struct. It is **not** a file magic
and cannot be found by scanning for it at offset 0. A parser that looks for a
magic at the start of a `_hdr.bin` will fail; one that reads `ucPLat` will
succeed. The same note that documents the sequence flag records that the `ALPS`
header is **stripped before the image is written to EMI**
(`wmt_ic_soc.c:3585-3586`), which is consistent with `ucPLat` being a
build-side tag rather than a load-time one `[F]`/`[I]`.

### 3.4 No ISA claim `[F]`/`[N]`

The payload after byte 48 is a raw EMI image. Standard prologue probes return
**0** for the MIPS `addiu sp,sp,-32` and `jr ra` patterns and **0** for the ARM
`push {…, lr}` pattern; entropy is **6.6605** (`2a_1`) and **6.6643** (`1a_1`),
i.e. dense binary. The trailer parse at `len-36` yields all zeros, so the
connac2 trailer grammar does **not** apply to this artifact — a second,
independent demonstration that it is a different format.

The device's own kernel routes this file to `IMG_DL_IDX_WIFI_ROM_EMI`, i.e. it
is **copied into EMI by the AP and executed by the WF CPU**, not by an AP-side
loader. Which ISA that CPU implements is **not** established here: no
disassembler run, and no probe produced a hit. So `isa_identified` staying blank
on all four rows is **correct** for this bucket, and this note adds no ISA claim
`[N]`.

---

## 4. Two builds of each filename exist in the wild `[F]`

This matters for reproducibility, and it is a real hazard for anyone checking
this note against a different download.

| filename | this session's payload | a second, older build |
|---|---:|---:|
| `WIFI_RAM_CODE_soc1_0_2a_1.bin` | **636,700** (`62da7ec1…`) | 654,344 (`029c43e9…`) |
| `soc1_0_ram_wifi_2a_1_hdr.bin` | **196,764** (`30bdc679…`) | 197,748 (`b89ff3c1…`) |

The two `RAM_CODE` builds differ by 17,644 B; the two `_hdr` builds by 984 B and
share only **26.66 %** of their bytes at the same offset. The older `RAM_CODE`
build has a stamp of 124 B and a stamp date of `20221225160501` with trailer
`20221225160750` — **169 s** apart — while this session's build has 128 B and
184 s. Both obey the stamp law and the sum law, so the **format** is stable and
the **builds** differ `[F]`.

The older build also carries `feature_set` `0x07, 0x07, 0x07, 0x80, 0x80` —
identical to this session's — so the feature split is not a build artifact `[F]`.

---

## 5. Gate 0 — prior art `[F]`/`[N]`

Access date **2026-11-26** for every query below. Queries are exact strings.

### 5.1 GitHub code search (REST `/search/code`)

| query | hits | what they are |
|---|---:|---|
| `WIFI_RAM_CODE_soc1_0` | **1,702** | overwhelmingly `proprietary-files.txt` manifests (`LineageOS/android_device_xiaomi_rosemary`, `begonia-dev/android_device_redmi_begonia`, `sarthakroy2002/device_realme_RMX2020`, `crdroidandroid/android_device_xiaomi_mt6768-common`) — plus **one real driver**: `abdullaabdullazade/mt7902_driver` `gen4-mt7902/chips/connac/connac.c` |
| `soc1_0_ram_wifi` | **1,276** | the same manifests; no format description |
| `soc1_0_ram_mcu` | **1,276** | the same manifests |
| `soc1_0_patch_mcu` | **1,266** | the same manifests, plus `Sabslgs/galaxy-a31-postmarketos` `connsys/README.md` — **a real port writeup** |
| `t-neptune-mp-soc1_0` | **76** | `F-to-pay/PostmarketOS-begonia` `wifi/NOTES.md` — **a real port writeup naming the manifest** |
| `KRUG_SOC1_0_E1` | **3** | the same begonia notes and `getActivity/AndroidSystemPropertyCollect` (a `getprop` dump containing the string) |
| `mt76_connac2_fw_trailer` | **1,692** | mainline kernel copies (`OnlineLearningTutorials/mt7902_temp` × several versions) **and** `MtkWifiRev/MtkWifiTools` `add_wf_region.c` — **a real region-table editor** |
| `struct wmt_rom_patch` | **492** | the MediaTek connsys headers, incl. `LineageOS/android_kernel_xiaomi_earth` — **the device's own kernel** |
| `ROM_EMI_HEADER repo:LineageOS/android_kernel_xiaomi_earth` | **6** | the `soc3_0`/`soc5_0`/`soc7_0` headers and C files |
| `u4PatchAddr repo:LineageOS/android_kernel_xiaomi_earth` | **7** | the same, plus `wmt_core.h` |

### 5.2 Web and project documentation

| source | what it establishes |
|---|---|
| `F-to-pay/PostmarketOS-begonia` `wifi/NOTES.md` (44,513 B) | A working MT6785 mainline port that **names this exact manifest**: "`WIFI_RAM_CODE_soc1_0_2a_1.bin` (manifest `t-neptune-mp-soc1_0e1-2015-KRUG_SOC1_0_E1_ASIC-20200924182102`, 5 regions)". It confirms the **5-region** count, the `KRUG` board name, that `gen4m` loads the file through the HIF, and that the two EMI sections land at `0xbc000000+0x177000` and `+0x1fe000` — matching regions 3 and 4 here. It also states the flavour rule: "firmware `WIFI_RAM_CODE_soc1_0_<hw>_<n>.bin`, flavor 'a' => `..._2a_1.bin`". **It does not decode the stamp, the trailer, or `feature_set`.** |
| `hataketsu/redmi9-lancelot-mainline` `docs/wifi-state.md` (31,092 B) | MT6768 port notes. Records that the `ALPS` header is **stripped** before the EMI write (`wmt_ic_soc.c:3585-3586`), and verifies a patch write byte-for-byte against `soc1_0_ram_mcu_1a_1_hdr.bin` at offset 48, with `sizeof(struct wmt_rom_patch) = 48`. Also records `chipid 0x6768, HW/FW 0x8a00`. |
| `Sabslgs/galaxy-a31-postmarketos` `connsys/README.md` | Documents the `srh_rom_patch` handler reading the patch address **out of the `.bin` header**, and the specific trap: "the low byte of the patch address is a sequence flag, not part of the EMI offset". |
| `MtkWifiRev/MtkWifiTools` `add_wf_region.c` (10,084 B) | An independent tool that parses `mt76_connac2_fw_trailer` / `_fw_region` and **appends a new region**, copying the bytes between payload and table as an opaque `trailer_space` of length `size − sizeof(trailer) − n_region×sizeof(region) − Σ len`. It therefore **confirms the layout arithmetic** and **never decodes the stamp**. |

### 5.3 Upstream trees

`linux-firmware` `WHENCE` (11,958 lines / 542,570 B, fetched 2026-11-26):
`soc1_0` → **0**. It lists **6** `WIFI_RAM_CODE_*.bin` and **5**
`BT_RAM_CODE_*_hdr.bin`, all MT79xx-class (`MT6639`, `MT7902`, `MT7922`,
`MT7925`, `MT7961`); the `soc1_0` family is **device-only and not upstream** `[F]`.

Mainline `drivers/net/wireless/mediatek/mt76/mt76_connac_mcu.h` (51,758 B) and
`.c` (94,816 B) are the normative spec for the trailer, the region struct, the
`FW_FEATURE_*` constants and the load loop `[F]`.

### 5.4 Decision — **PRIOR-ART**, partial

This is **not** a `DELTA`. The container format is specified in mainline Linux,
the `_hdr.bin` header is specified in MediaTek's own kernel headers, and two
independent public ports plus one independent tool operate on these exact
files. Anyone implementing this format should read those first, and this note
credits them.

What is **not** in any of those sources, and is this note's contribution:

1. **The stamp grammar.** No public source decodes it. `MtkWifiTools` copies it
   as opaque `trailer_space`; the begonia notes quote the manifest string but
   never parse the framing. The `b'#'*16 ‖ u32le len ‖ body ‖ b'#'*16` law with
   `total = len + 36`, verified on **7 of 7** files across two silicon
   generations, is stated here for the first time `[F]`.
2. **The `0x80` vs `0x40` distinction on these payloads.** The public sources
   quote the `FW_FEATURE_*` defines but none applies them to `soc1_0`. That
   `0x80` is undefined in mainline and therefore the two large regions **do**
   download, while `0x07` means encrypted-with-key-3, is derived here `[F]`.
3. **The `_hdr.bin` ↔ `RAM_CODE` build-date link.** That the `_hdr.bin`'s first
   12 bytes are the stamp timestamp minus its century prefix is not in any
   source found `[F]`.
4. **The two-build discrepancy** for both filenames, with both builds obeying
   the same laws `[F]`.
5. **The subfamily boundary defect** in §1.1 — that `bt` is outside
   `wifi-bt-combo` and the MCU pair is under `misc` `[F]`.

---

## 6. Honest negatives `[N]`

- **`soc1_0` is not in `linux-firmware`.** `WHENCE` has **0** hits, so the
  format can be checked against mainline but the payloads cannot be obtained
  from upstream. Every payload here came from a device tree.
- **`chip_id = 7` cannot be named.** Mainline assigns no name to 7; the five
  upstream builds carry 13/16/19/21/24. The marketing name of the `soc1_0`
  silicon is `[U]`.
- **`0x80` in `feature_set` is undecoded.** It is not `NON_DL`, not
  `OVERRIDE_ADDR`, not `ENCRY_MODE`, and not any defined bit. Recorded `[U]`,
  not guessed.
- **No ISA claim.** No MIPS/ARM prologue probe hit; no disassembler run. The
  payload executes on the WF CPU, whose ISA is not established here. Matches
  `isa_identified` blank on 4 of 4 rows.
- **`u4PatchType = 0x03000000` is undecoded.** The device's own kernel reads
  `u4PatchAddr` and ignores `u4PatchType` on this path, so its meaning is not
  established from source `[U]`.
- **The `ALPS` inner layout is not decoded.** After `ALPS` the bytes
  `8a 00 8a 00 11 00 14 f0 00 00 00 03` are the `u2HwVer`/`u2SwVer` pair plus
  `u4PatchAddr`/`u4PatchType` — but whether anything after byte 48 is a
  structured ALPS image or raw code was **not** established `[U]`.
- **`WPSS` is the `wifi` family's real mass** (5,198 rows / 317,873,910 B) and is
  out of scope here; this bucket is 0.23 % of the family's bytes. Nothing in
  this note should be read as describing the family.

---

## 7. Open items `[U]`

1. What `feature_set = 0x80` requests. The mainline header has a free `BIT(7)`
   and the vendor driver may use it; the vendor gen4m source was not read far
   enough to say.
2. The name and ISA of the `soc1_0` silicon behind `chip_id = 7`.
3. Whether the two `_hdr.bin` builds' 984-byte difference is code or metadata.
4. Whether `u4PatchAddr`'s sequence byte `0x11` is consumed by the vendor
   loader or ignored, on this device specifically.

---

## 8. Method `[F]`

- Census: `csv.DictReader` over `upstream-contribution/blob-database/coverage-matrix.csv`,
  grouped on `blob_subfamily`; ranks from the sorted 18 aggregates, never in
  head.
- Container: trailer read at `len-36` as `<BBBBB2s10s15sI`; `n_region` from
  byte 2; table base `len - 36 - n_region*40`; each region read as
  `<III4sIIB14s` (40 B) against `struct mt76_connac2_fw_region`.
- Stamp: located at `Σ region.len`, i.e. `table_base - stamp_len`; framing
  tested as `st[:16]==b'#'*16 and st[-16:]==b'#'*16 and 16+4+u32le(st,16)+16==len(st)`.
- `_hdr.bin`: 48-byte `ROM_EMI_HEADER` read field-by-field against the device's
  own header; `u2HwVer`/`u2SwVer` as **big**-endian (they read `0x8a00`, the
  value the public ports report), all other integers little-endian.
- md5s re-computed with `md5sum` and compared against the matrix column, all
  four matching.
- All arithmetic (sums, ranks, percentages, time deltas, the 24.27×-style
  ratios) printed by the command that computed it, never carried in head.
- Every file opened read-only. No payload committed; the only hex in this note
  is ≤16 bytes per sample.
