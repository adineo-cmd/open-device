# `camera` — 1,611 rows where 88% of the bytes are not firmware

Analysis date: 2026-11-24. Analyst: OC-1 (`100milionseek`), issue
[#2053](https://github.com/adineo-cmd/open-device/issues/2053).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; the FP6 split PIL set at
`…/downloads/lineage-fp6/extracted/trees/vendor-firmware/CAMERA_ICP.{elf,mbn,mdt,b00–b20}`;
three further public `CAMERA_ICP.mdt` builds (Poco_F5/`marble`, Xiaomi Pad 6 Pro/`liuqin`,
Mi 12S Ultra/`thor`) fetched 2026-11-24, making four with the FP6 copy; and the 39 testable
`.mdt` files on disk, spanning 36 stems (`CAMERA_ICP`, four `*_zap`, `adsp`, `adsp_dtb`,
`cdsp`, `cdsp_dtb`, `cpusys_vm`, `evass`, `facereg`, `ipa_fws`, `ipa_uc`, `modem`,
`synth_modem`, `wpss`, nineteen `image_*`).
No payload is committed. No payload bytes are reproduced: the note carries sizes, offsets,
counts, `e_machine`/`e_type`/`e_flags` values, md5 prefixes, and symbol/string names only.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** `camera` is the **2nd-largest of thirteen `other` subfamilies by rows
(1,611) and by bytes (4,563,019,282)** — the only bucket besides `misc` that is 2nd or
better on both axes, and 32.24% of all `other` bytes. It is not a firmware bucket.
**88.2% of its bytes are AI models plus tuning tables; actual PIL firmware is 27 `.mdt`
rows and 0.0032% of bytes.**

The bucket nevertheless contains the one thing worth chasing: `CAMERA_ICP.mdt`, the
camera ICP remote-processor image. This report settles three things about it that the
repository had left open or stated too narrowly:

1. **The ISA question was closed by an earlier issue, and this report corroborates it from
   inside the image.** `other-media.md` §7 declined the question — *"the local copies are
   `EM_ARM` (40), not 94. I make **no** claim about the FP6 `CAMERA_ICP` ISA."* But
   `research/qualcomm/docs/fp6-architecture-census.md` and `results/census.md` already
   label `CAMERA_ICP.mbn/.elf/.mdt` `e_machine=94` `EM_XTENSA` and `CAMERA_ICP_170.elf`
   `ARM (40)`. So the ISA is **not new**, and the honest delta is narrower: the
   `other-media.md` disclaimer is stale, and the unstripped `.elf` lets the ISA be
   **corroborated from its own symbol table and build paths** rather than from header
   bytes alone. The database's `isa_identified = "RISC-V (old, bespoke)"` on the FP6 row
   is still wrong.
2. **`CAMERA_ICP.mdt` is exactly `b00 + b20`** — 5,484 B, zero slack, and
   `len(mdt) == phdr[0].p_filesz + phdr[20].p_filesz` = 724 + 4,760. That is mainline
   `qcom_mdt_read_metadata()`'s split-firmware case, verified against the kernel's own
   predicates.
3. **The hash segment sits at program-header index 20 on all four builds** — a family
   constant, unlike the `wpss` family where `wifi-wpss.md` §2.4 measures it moving per
   device.

It also records two defects and a large honest negative: `db_type` is `ELF64` on all 28
`.mdt` rows that are in fact ELF32; 50 rows filed `camera` live in `vendor/gpu/kbc`
alongside GPU kernel caches; and **no public source documents this container or any of the
410 filenames.**

---

## 0. Headline

1. **`[F]` `camera` is a content bucket, not a firmware bucket.** 1,611 rows /
   72 devices / 4,563,019,282 B, 2nd of 13 `other` subfamilies on both rows and bytes.
   But the functional split puts **60.5% of bytes in AI/ML models** and **27.7% in camera
   tuning/calibration**. PIL firmware — the 27 rows named `CAMERA_ICP.mdt` (25) or
   `CAMERA_ICP_1.mdt` (2), every one under a `firmware` directory (`vendor/firmware` 23,
   `odm/firmware` 4) — is **27 rows, 144,108 B, 0.0032%**. (The full `CAMERA_ICP.*` family
   including the 13 loose `Edge_40_Pro` segments and the extra `rtwo/modem/image` `.mdt`
   copy is 41 rows / 660,184 B, still 0.0145%.)
2. **`[F]` The FP6 `CAMERA_ICP` ISA is `EM_XTENSA` (94), and it is not one ISA across
   devices.** The FP6 set (`CAMERA_ICP.elf`, `.mbn`, `.mdt`, all 21 `.bNN`) is
   `e_machine=94`. But `CAMERA_ICP_170.elf` in the *same directory* is `e_machine=40`
   (ARM32), and so are the `enchilada` and `instantnoodle` copies. **Same filename, two
   ISAs.** This is **already recorded in this repository** —
   `research/qualcomm/docs/fp6-architecture-census.md` lists `CAMERA_ICP.mbn/.elf/.mdt`
   under `Xtensa (94)` and `CAMERA_ICP_170.elf` under `ARM (40)`, and
   `results/census.md` L653–677 carries the same per-file labels. What this note adds is
   the corroboration *from inside the image* (symbol prefixes and build strings, §3.3)
   and the explicit statement that one filename carries two ISAs. §3.
3. **`[F]` `CAMERA_ICP.mdt == b00 + b20`, byte-for-byte, 5,484 B, zero slack.** Both
   `len(mdt) == ph0.p_filesz + ph20.p_filesz` (724 + 4,760) and
   `phdr[20].p_flags & QCOM_MDT_TYPE_MASK == QCOM_MDT_TYPE_HASH`. This is the kernel's
   documented split case: the hash follows the ELF header rather than sitting at
   `p_offset`. §4.
4. **`[F]` The hash index is 20 on all four independent builds** — FP6, Poco_F5,
   Pad 6 Pro and Mi 12S Ultra, three vendors, two sizes (5,484 and 5,004 B). So for
   `CAMERA_ICP` the index is a **family constant**, where `wifi-wpss.md` §2.4 measured it
   moving between `b01` and `b12` across `wpss` devices. §4.3.
5. **`[F]` The three forms are one build in three stages.** `.elf` (3,306,937 B) is
   **unstripped** — 19 phdrs, 36 sections, a 3,420-entry symtab, 3,386 named symbols,
   1,525 functions, and DWARF from `-O2 -g3`. `.mbn` (516,760 B) is the same 11 segment
   bodies with the hash appended at `p_offset` 0x7d000. `.mdt` (5,484 B) is the header
   plus that hash. §5.
6. **`[F]` `db_type=ELF64` is wrong on all 28 `.mdt` rows.** Every one is ELF**32**
   (class byte 1, `e_phentsize` 32). §6.
7. **`[F]` 50 rows in this subfamily sit at `vendor/gpu/kbc`** — 50 devices carry a
   `unified_ksqs.bin` there, in the same directory as GPU kernel caches. §7.
8. **`[N]` No public document describes this container or its 410 filenames.** Four
   recorded 0-hit queries; `linux-firmware` does not ship `CAMERA_ICP`. §10.

---

## 1. The subfamily in numbers

All figures `[F]` from the matrix.

| metric | value |
|---|---:|
| rows | **1,611** |
| devices | **72** |
| filenames (basenames) | **410** |
| distinct `md5_db` | **622** |
| total declared bytes | **4,563,019,282** |
| `(device, filename)` pairs | **1,482** |
| rows per pair | **1.09** |
| distinct `db_path` values | **358** |
| duplicate full rows | **0** |
| rows with blank md5 | **0** |
| rows with `sha256_if_listed` | **1** |
| rows with blank `soc` | **1,179** |
| `interface_documented = n` | **1,611 / 1,611** |

Share of the corpus and of `other`:

| denominator | rows | bytes |
|---|---:|---:|
| all 33,917 rows / 69,797,539,502 B | 4.7498% | 6.5375% |
| `other` 14,987 rows / 14,152,121,440 B | 10.7493% | **32.2427%** |

### 1.1 Rank inside `other` `[F]`

| rank | subfamily | rows | bytes |
|---:|---|---:|---:|
| 1 | `misc` | 10,720 | 8,498,193,635 |
| **2** | **`camera`** | **1,611** | **4,563,019,282** |
| 3 | `touch` | 880 | 516,418,690 |
| 4 | `media` | 470 | 29,190,348 |
| 5 | `audio` | 422 | 5,418,315 |
| 6 | `fastchg` | 315 | 36,989,007 |
| 7 | `fingerprint` | 284 | 387,540,764 |
| 8 | `oled` | 157 | 4,068,320 |
| 9 | `nfc` | 75 | 9,677,922 |
| 10 | `esim` | 41 | 8,407,085 |
| 11 | `sensors` | 5 | 86,541,968 |
| 12 | `tinysys` | 4 | 4,132,864 |
| 13 | `gpu-compute` | 3 | 2,523,240 |

`camera` is 2nd on **both** axes. What makes that notable is how the small buckets behave:
`media` is 4th by rows but 7th by bytes, `audio` 5th by rows but 10th by bytes, and
`sensors` is 11th by rows yet 5th by bytes on only 5 rows. Only `misc` and `camera` are
large on both axes, and `camera` alone has 32.2% of `other` bytes on 10.7% of its rows.

### 1.2 Vendors and devices `[F]`

| vendor | rows | devices |
|---|---:|---:|
| oneplus | 984 | 22 |
| xiaomi | 437 | 14 |
| motorola | 78 | 18 |
| realme | 46 | 2 |
| fairphone | 26 | 3 |
| nothing | 14 | 2 |
| google | 12 | 3 |
| sony | 7 | 5 |
| samsung | 7 | 3 |

OnePlus alone is 61.1% of rows. Top devices by bytes:

| device | rows | bytes |
|---|---:|---:|
| OnePlus_12 | 128 | 583,957,535 |
| Nord_CE4 | 108 | 530,689,155 |
| OnePlus_12R | 104 | 524,459,190 |
| Nord_4 | 112 | 512,100,171 |
| OnePlus_13 | 140 | 483,765,328 |
| OnePlus_11_5G | 89 | 390,486,721 |
| Pad_2_Pro | 88 | 161,081,487 |
| Mi_13_Pro | 41 | 127,208,221 |
| Mi_13 | 36 | 123,545,455 |
| Mi_12S_Ultra | 38 | 97,543,482 |

### 1.3 Size distribution `[F]`

| bucket | rows |
|---|---:|
| 0 B | **8** |
| < 1 KiB | 177 |
| 1 KiB – 1 MiB | 948 |
| 1 – 16 MiB | 417 |
| ≥ 16 MiB | 61 |

min 0, median 131,072 (128 KiB), max 50,331,648 (48 MiB exactly). 446 rows exceed 1 MiB.

The eight zero-byte rows are real matrix entries, not parse errors:

| filename | device | path |
|---|---|---|
| `eye_retouch_chinese.bin` | oneplus/erhai | `odm/etc/camera/fb_model` |
| `eye_retouch_chinese.bin` | oneplus/dodge | `odm/etc/camera/fb_model` |
| `dgain_mask_rear_uw.bin` | FP6 | `vendor/etc/camera/AncRawAlgos` |
| `dgain_mask_raw_sr.bin` | FP6 | `vendor/etc/camera/AncRawAlgos` |
| `dgain_mask_rear_main.bin` | FP6 | `vendor/etc/camera/AncRawAlgos` |
| `dgain_mask_front_main.bin` | FP6 | `vendor/etc/camera/AncRawAlgos` |
| `dgain_mask_AncSuperNightLite.bin` | FP5 | `vendor/etc/camera` |
| `dgain_mask_AncSuperNight.bin` | FP5 | `vendor/etc/camera` |

A zero-size `dgain_mask_*` is a placeholder: the gain mask for an absent camera mode.
`[I]` These are declaration files whose content the tuning tool supplies at build time.
Measured: 8 rows, 0 bytes; cause `[U]`.

Row inflation is minimal: 1,482 pairs over 1,611 rows = **1.09 rows/pair**, histogram
`1×1366, 2×105, 3×9, 4×2`. 197 of the 410 names appear on exactly one row.

---

## 2. What the bucket actually contains `[F]`

Classified by path signature and filename, not by extension, because 1,567 of 1,611 rows
(97.3%) are `.bin` and the extension carries no information.

| functional class | rows | % rows | bytes | % bytes | devices |
|---|---:|---:|---:|---:|---:|
| AI / ML model | 439 | 27.3% | 2,761,528,454 | **60.5%** | 21 |
| camera tuning / calibration | 178 | 11.0% | 1,264,096,364 | **27.7%** | 53 |
| other / unclassified | 498 | 30.9% | 388,289,239 | 8.5% | 65 |
| LUT / colour filter | 273 | 16.9% | 117,899,621 | 2.6% | 19 |
| render effect asset | 85 | 5.3% | 30,653,500 | 0.7% | 11 |
| CFR snapshot / frame | 111 | 6.9% | 407,996 | 0.009% | 33 |
| **PIL firmware (`.mdt` under a `firmware` dir)** | **27** | **1.7%** | **144,108** | **0.0032%** | 25 |

**88.2% of bucket bytes are AI models plus tuning data.** Firmware is 0.0032%.

This matters for scoping: a reader who sees `camera` ranked 2nd of 13 would reasonably
expect a firmware-heavy bucket. It is instead the repository's largest concentration of
*numeric asset* data, which is why the extension census is uninformative and why the only
container-analysis target is the 27-row `.mdt` set (`CAMERA_ICP.mdt` 25 rows,
`CAMERA_ICP_1.mdt` 2 rows).

### 2.1 The largest files are not code `[F]`

| filename | rows | devices | bytes |
|---|---:|---:|---:|
| `night_align_lsc_tbl_40963072.bin` | 6 | 6 | 301,989,888 |
| `night_align_lsc_tbl_40962304.bin` | 6 | 6 | 226,492,416 |
| `selfbokehmodel.bin` | 11 | 11 | 224,509,827 |
| `awb_parameter_default.bin` | 7 | 7 | 156,014,392 |
| `beauty_body.bin` | 10 | 10 | 118,545,459 |
| `darksight_ultrawide.bin` | 13 | 13 | 103,114,725 |
| `darksight_main.bin` | 13 | 13 | 101,737,109 |
| `DREAM_4_5_354_654.bin` | 5 | 5 | 92,606,400 |
| `SEA_4_5_354_654.bin` | 5 | 5 | 92,606,400 |
| `film_grain_small.bin` | 19 | 15 | 79,691,776 |

`night_align_lsc_tbl_40963072.bin` is **exactly 50,331,648 B = 48 MiB** on all 6 devices;
its sibling `…_40962304.bin` is **exactly 37,748,736 B = 36 MiB** on the same 6. Both are
clean powers-of-two-multiple tables, consistent with a fixed-size LSC (lens-shading
correction) alignment table sized for a specific sensor resolution. The embedded numbers
`40963072` and `40962304` are `[U]` — they are not obviously `w*h*4` for any common
sensor, and no public source explains them.

Those two names alone are 528,482,304 B = **11.58% of the bucket**, on 12 rows.

### 2.2 md5 concentration `[F]`

622 distinct md5 over 1,611 rows. The most-shared single md5 spans **25 devices**
(`dae8b801cf…`), then 19, and **seven** at 15. That is genuine fleet-wide sharing of a small
number of tuning assets, and is why `camera` shows high byte volume on few distinct
payloads.

---

## 3. The ISA, measured and corroborated `[F]`

### 3.1 Prior position, and what was already established

`research/fleet/other-media.md` §7 said, before this issue corrected it in place:

> **`CAMERA_ICP` is out of local reach** — the local copies are `EM_ARM` (40), not 94. I
> make **no** claim about the FP6 `CAMERA_ICP` ISA; only about `vpu20/30/33`, which is
> what this issue's subfamily contains.

and again, in the same honest-negatives list:

> **`CAMERA_ICP` ISA not asserted.** The local copies are `EM_ARM`; the FP6 set the repo
> discusses is not in the local tree.

Both statements were **correctly scoped and are now stale**, because a *different* issue
already answered the question. Two committed notes carry the answer:

| note | what it already says |
|---|---|
| `research/qualcomm/docs/fp6-architecture-census.md` L35–L36, L51–L55 | `Xtensa (94, EM_XTENSA) — 12 files — **CAMERA_ICP.mbn/.elf/.mdt**, vpu20/30/33_*.mbn`; `ARM (40) — 31 files — …CAMERA_ICP_170.elf`; and the §"Camera ICP / VPU" bullet naming `e_machine=94` for both sets |
| `research/qualcomm/results/census.md` L653–677 | per-file labels: `.b00`, `.elf`, `.mbn`, `.mdt` = `Xtensa`; `CAMERA_ICP_170.elf` = `ARM` |

So the ISA is **prior art and is credited, not claimed**. What is genuinely new here is
(§3.2) the fresh measurement on the current tree against freshly fetched payloads, the
explicit "one filename, two ISAs" statement, which neither note makes, and the *internal*
corroboration in §3.3, which the header-byte censuses could not do because they never
opened the symbol table.

Both prior notes check out. `census.md`'s histogram reads `| QDSP6 / Hexagon | 94 |` under
a `| machine | count |` header — 94 *files* whose `e_machine` is 164 — and `Xtensa | 12`
alongside it. `fp6-architecture-census.md` L31–L38 says the same thing with the machine
values inline (`Hexagon (164) | 94`, `Xtensa (94, EM_XTENSA) | 12`). The two agree, and the
per-file labels agree with both.

### 3.2 Measured, all payloads

| file | size | class | `e_machine` | ISA | `e_type` |
|---|---:|---:|---:|---|---:|
| `CAMERA_ICP.elf` | 3,306,937 | 1 | **94** | **EM_XTENSA** | 2 |
| `CAMERA_ICP.mbn` | 516,760 | 1 | **94** | **EM_XTENSA** | 2 |
| `CAMERA_ICP.mdt` | 5,484 | 1 | **94** | **EM_XTENSA** | 2 |
| `CAMERA_ICP.b00` | 724 | 1 | **94** | **EM_XTENSA** | 2 |
| `CAMERA_ICP.b01` … `.b18` | see §4.1 | — | not ELF | — | — |
| `CAMERA_ICP.b20` | 4,760 | — | not ELF (hash blob) | — | — |
| `CAMERA_ICP_170.elf` | 4,179,544 | 1 | **40** | **ARM32** | 2 |
| `enchilada/…/CAMERA_ICP.elf` | 3,299,320 | 1 | **40** | **ARM32** | 2 |
| `instantnoodle/…/CAMERA_ICP.elf` | 3,922,232 | 1 | **40** | **ARM32** | 2 |

Only `b00` among the 21 segments is an ELF; the rest are raw segment bodies and the hash.
Confirmed: scanning all 21 `.bNN` for the ELF magic finds exactly one hit, `b00`.

**So "the `CAMERA_ICP` ISA" is not a single thing.** On FP6 the camera ICP firmware is
Xtensa. On `enchilada`, `instantnoodle` and (per `CAMERA_ICP_170.elf`) the FP6 tree's
alternate build, it is 32-bit ARM. The two sizes make the distinction concrete: the three
Xtensa forms are 3,306,937 / 516,760 / 5,484 B and the ARM builds are 4,179,544 /
3,299,320 / 3,922,232 B, so `_170.elf` is the *largest* file in the set and is not
Xtensa at all.

The database's single global label `isa_identified = "RISC-V (old, bespoke)"` — applied to
exactly one row, FP6's `.mdt` — is wrong in three ways: 94 is not a RISC-V value at all
(`EM_RISCV` is 243, established in `other-media.md` §2 from four independent sources),
FP6 is Xtensa, and the label is attached to a `.mdt` that is a header, not code.

### 3.3 Independent corroboration from inside the image `[F]`

The unstripped `.elf` (§5) makes the ISA verifiable a second way, without a disassembler —
something the header-only censuses in `census.md` and `fp6-architecture-census.md` could
not do. Its symbol table contains toolchain and RTOS symbols that only exist for one
architecture:

| symbol prefix | count | what it is |
|---|---:|---|
| `xthal` | 47 | Xtensa HAL |
| `xos` | 154 | Xtensa OS layer (`xtos`) |
| `UEXC`, `KEXC` | 155 | Xtensa user/kernel exception vectors |

and the embedded build-path strings name the toolchain directly:

```
#Xtensa Compiler Version 12.0.9 :  Z:/b/fw_core/ICP/ICP1/src/icpdomain.c compiled with : -O2 -g3
/build/tree/RG-2018.9_kuma/tools/swtools-MSWin32-x86/xtensa-elf/src/hal/not_certified/interrupts.c
Z:/b/external/corexos/kernel/xtos/build/camera_icp/tensilica-lx7/AAAAAA/Reset_mem.o
```

`tensilica-lx7`, `xtensa-elf`, `xtos`, `RG-2018.9` — the Xtensa LX7 core, Xtensa ELF
toolchain, Xtensa RTOS. This is **not** disassembly, but it is stronger than a header
field: it is the build system naming its own target. `[F]` for the strings; `[I]` that
LX7 is the exact core (the path says `lx7`; the register map is not decoded).

### 3.4 What is still not established `[N]`

No Xtensa disassembler exists in this environment (*no* backend in Capstone, `objdump`
lists x86 targets only — the same limitation `other-media.md` §2.4 records). So the ISA
verdict rests on `e_machine`, the toolchain symbol prefixes and the embedded build paths,
**not on decoded instructions**. The core model beyond "LX7 per its own build path" and
the ABI in use are `[U]`.

---

## 4. The `.mdt` container, and the hash index `[F]`

### 4.1 The 21 program headers

`CAMERA_ICP.mdt` is ELF32, `e_phnum` 21, `e_phentsize` 32, `e_shnum` 0, `e_entry` 0.
Every header's `p_filesz` equals the corresponding `.bNN` file size, **21/21**.

| idx | `p_type` | `p_offset` | filesz | memsz | `p_flags` | role |
|---:|---|---:|---:|---:|---|---|
| 0 | PT_NULL (0) | 0x000000 | 724 | 0 | `0x07000000` | ehdr + phdr table (`b00`) |
| 1 | PT_LOAD | 0x0002d4 | 460 | 460 | `0x08000005` | |
| 2 | PT_LOAD | 0x0004a0 | 16 | 16 | `0x08000005` | |
| 3 | PT_LOAD | 0x0004b0 | 16 | 16 | `0x08000005` | |
| 4 | PT_LOAD | 0x0004c0 | 16 | 16 | `0x08000005` | |
| 5 | PT_LOAD | 0x0004d0 | 20 | 20 | `0x08000005` | |
| 6 | PT_LOAD | 0x0004e4 | 24 | 24 | `0x08000005` | |
| 7 | PT_LOAD | 0x0004fc | 16 | 16 | `0x08000005` | |
| 8 | PT_LOAD | 0x001000 | 433,784 | 433,784 | `0x08000005` | main code body |
| 9 | PT_LOAD | 0x06b000 | 27,652 | 27,652 | `0x08000006` | |
| 10 | PT_LOAD | 0x071c04 | 0 | 0 | `0x08000000` | zero-length |
| 11 | PT_LOAD | 0x071c10 | 0 | 623,184 | `0x08000006` | BSS |
| 12 | PT_LOAD | 0x071c04 | 0 | 45,628 | `0x08000006` | BSS |
| 13 | PT_LOAD | 0x071c04 | 0 | 0 | `0x08000000` | zero-length |
| 14 | PT_LOAD | 0x071c08 | 0 | **4,194,304** | `0x08000006` | BSS (4 MiB) |
| 15 | PT_LOAD | 0x071c04 | 0 | 0 | `0x08000000` | zero-length |
| 16 | PT_LOAD | 0x071c08 | 0 | **1,048,576** | `0x08000006` | BSS (1 MiB) |
| 17 | PT_LOAD | 0x071c08 | 24,084 | 24,084 | `0x08000005` | |
| 18 | PT_LOAD | 0x077a20 | 21,476 | 21,476 | `0x08000006` | |
| 19 | PT_LOAD | 0x07ce04 | 0 | 0 | `0x08000000` | zero-length |
| 20 | PT_NULL (0) | 0x07d000 | 4,760 | 4,760 | **`0x02000000`** | **HASH** (`b20`) |

Decoded with the kernel's constants (§4.2): `(0x02000000 & (7<<24)) == (2<<24)` →
`QCOM_MDT_TYPE_HASH`. **All 19 PT_LOAD headers (indices 1–19) carry `BIT(27)` =
`QCOM_MDT_RELOCATABLE`** — including the eight with `p_filesz == 0`; only the two
`PT_NULL` headers (0 and 20) lack it.

Sums: `sum p_filesz` = 513,048; `sum p_memsz` = 6,424,016 — a **12.52×** ratio, with
5,910,968 B declared and not stored. Two of the BSS segments are exactly 4 MiB and 1 MiB.

Segment index 20 is the last, and it is a `PT_NULL` carrying the hash type in `p_flags`.
**Index 20 out of 21 is not where a naive reader expects the hash**; on most Qualcomm
PIL images it is index 1.

### 4.2 `mdt == b00 + b20`, against the kernel's own rule

Mainline `drivers/soc/qcom/mdt_loader.c` and
`include/linux/soc/qcom/mdt_loader.h` (fetched 2026-11-24) define:

```c
#define QCOM_MDT_TYPE_MASK   (7 << 24)
#define QCOM_MDT_TYPE_HASH   (2 << 24)
#define QCOM_MDT_RELOCATABLE BIT(27)
```

and `qcom_mdt_read_metadata()` locates the hash segment by that type field, not by
`p_type` and not by position:

```c
for (i = 1; i < ehdr->e_phnum; i++) {
    if ((phdrs[i].p_flags & QCOM_MDT_TYPE_MASK) == QCOM_MDT_TYPE_HASH) {
        hash_segment = i; break;
    }
}
```

The loader's split detection is: if the hash region falls *directly after the ELF header*
rather than at its declared `p_offset`, the file is the split `.mdt`; otherwise it is the
monolithic image. Both branches verified here:

| check | result |
|---|---|
| `mdt == b00 + b20` byte-for-byte | **True** |
| `len(mdt) == ph0.p_filesz + ph20.p_filesz` | **True** (5,484 = 724 + 4,760) |
| `mdt.find(b20)` | **0x2d4** (= 724, immediately after the header) |
| `mbn.find(b20)` | **0x7d000** (= `ph20.p_offset`, the declared position) |
| hash segment identified by type field, not `p_type` | idx 20, `p_type` = PT_NULL |
| every non-empty segment at declared `p_offset` inside `.mbn` | **13/13** |
| `len(mbn) == ph20.p_offset + ph20.p_filesz` | **True** (516,760) |

So `CAMERA_ICP.mdt` is the canonical split form: `b00` (the 724-byte header) followed
immediately by `b20` (the 4,760-byte hash/certificate block). `CAMERA_ICP.mbn` is the
monolithic form of the same build, hash at its declared offset. That the `.mdt` is *not* a
prefix of the `.mbn` (`mdt == mbn[:5484]` is **False**; they agree only up to 0x2d4) is
exactly the hash relocation the kernel documents.

**What is prior art and what is mine.** `mdt == b00 + bNN` is **already established in
this repository** — MSM8998 §7.1 (27/27), SM8350 (23/23), SM4350 (7/7 zap), SM4375
(17/17), `cdsp-fleet/audit.md`, and `other-fingerprint.md` §5.4 (`mdt[:len(b00)] == b00`,
4/4). `wifi-wpss.md` §2.4 further states `.mdt = b00 ‖ b<hash-index>` and notes the index
varies. I am **not** claiming the law. What is measured here for the first time is its
application to `CAMERA_ICP`: index **20**, and the 5,484-byte instance.

### 4.3 The hash index is 20 on all four independent builds `[F]`

Four separate public builds of `CAMERA_ICP.mdt`, three vendors, two sizes:

| build | size | md5 | `e_machine` | phnum | hash idx | `ph0 + hash == size` |
|---|---:|---|---:|---:|---:|---|
| FP6 (`larry`/`vendor-firmware`) | 5,484 | `0c284e23…` | 94 | 21 | **20** | ✔ 724 + 4,760 |
| Poco_F5 (`marble`) | 5,484 | `fc2604d0…` | 94 | 21 | **20** | ✔ 724 + 4,760 |
| Xiaomi Pad 6 Pro (`liuqin`) | 5,004 | `0b4fe307…` | 94 | 21 | **20** | ✔ 724 + 4,280 |
| Mi 12S Ultra (`thor`) | 5,004 | `ce6fc139…` | 94 | 21 | **20** | ✔ 724 + 4,280 |

All four: `e_ehsize` 52, `e_phnum` 21, `e_phentsize` 32, so **724 = 52 + 21×32** on all
four, and the ELF header size is invariant while the hash block size is not (4,760 vs
4,280). The three matrix size clusters follow directly:

| `.mdt` size | `− 724` | rows |
|---:|---:|---:|
| 5,484 | 4,760 | 21 |
| 5,004 | 4,280 | 5 |
| 4,704 | 3,980 | 2 |

**So `CAMERA_ICP` has a constant hash index (20) with a variable hash size**, the mirror
image of `wpss`, where `wifi-wpss.md` §2.4 measures a *variable* index (`b01` on Edge_30 /
FP5 / Phone_1 / Nord_CE4, `b12` on FP6 / Nord_4) at constant-ish size. A reassembler
written from the `wpss` result ("hash is `b01` or `b12`") fails on `CAMERA_ICP`; one
written from the kernel's rule passes both.

### 4.4 The same law across 39 testable `.mdt` files on disk `[F]`

To check whether index 20 is genuinely unusual, the law was measured on every ELF32
`.mdt` on this machine that has both a `.b00` and its hash segment:

```
ELF32 .mdt files:                     43
testable (b00 + hash segment present): 39
mdt == b00 + b<hash-index>:            38
```

Hash index distribution over those 38 conformers (the 1 non-conformer contributes no
valid index):

| index | files |
|---:|---:|
| 1 | 29 |
| 2 | 2 |
| 3 | 1 |
| 4 | 1 |
| 12 | 1 |
| 15 | 1 |
| **20** | **1** (this one) |
| 30 | 1 |
| 47 | 1 |

The nine non-1 cases all satisfy the law:

| file | hash idx | `b00` | hash | `.mdt` | equal |
|---|---:|---:|---:|---:|---|
| `adsp.mdt` | 47 | 1,588 | 6,056 | 7,644 | ✔ |
| `adsp_dtb.mdt` | 2 | 148 | 3,896 | 4,044 | ✔ |
| `cdsp.mdt` | 15 | 564 | 4,520 | 5,084 | ✔ |
| `cdsp_dtb.mdt` | 2 | 148 | 3,896 | 4,044 | ✔ |
| `cpusys_vm.mdt` | 3 | 180 | 10,992 | 11,172 | ✔ |
| `ipa_fws.mdt` | 4 | 212 | 3,992 | 4,204 | ✔ |
| `modem.mdt` | 30 | 1,044 | 5,240 | 6,284 | ✔ |
| `wpss.mdt` | 12 | 468 | 4,376 | 4,844 | ✔ |
| **`CAMERA_ICP.mdt`** | **20** | **724** | **4,760** | **5,484** | **✔** |

The single failure is `implementations/historic/fp2/fixtures/synth_modem.mdt`, which is a
**synthetic fixture** (`b00` 880 B, `b01` 904 B, `b02` 4,052 B, and `mdt` 880 B matches
none of them) — i.e. a test stub, not a real image. Recording it rather than silently
excluding it: 38/39, with the 1 non-conformer identified.

**This widens `wifi-wpss.md` §2.4 from 6 files to 38 conforming ones (of 39 testable).**
That note's general form is correct; what it could not show, and this measurement does, is
that the hash index ranges from 1 to 47 across families and that `b00 + b01` — the form
MSM8998/SM8350/SM4350/SM4375 state as *the* law — is a special case of it, holding on 29
of the 38.

---

## 5. The three forms are one build in three stages `[F]`

The FP6 tree ships `CAMERA_ICP` in three container forms plus 21 loose segments, all from
the same build:

| form | size | phdrs | sections | symtab | hash |
|---|---:|---:|---:|---:|---|
| `.elf` | **3,306,937** | 19 | **36** | **3,420 entries** | absent |
| `.mbn` | **516,760** | 21 | 0 | none | at `p_offset` 0x7d000 |
| `.mdt` | **5,484** | 21 | 0 | none | at 0x2d4 (after header) |

### 5.1 The `.elf` is unstripped `[F]`

`CAMERA_ICP.elf` carries a full symbol table and section headers:

| metric | value |
|---|---:|
| section headers | **36** |
| `SYMTAB` entries | **3,420** (`e_shentsize` 16) |
| named symbols | **3,386** |
| `STT_FUNC` symbols | **1,525** |
| `STT_OBJECT` symbols | 726 |
| symbols with non-zero size | 2,239 |
| total `STT_FUNC` bytes | **371,905** |
| `STRTAB` size | 54,037 B |
| source filenames referenced | 90 distinct |
| bytes after last phdr end (0x7ce04) | 2,795,445 = **84.5% of the file** |

Named functions, largest first:

| symbol | size |
|---|---:|
| `IpeCopySettings` | 10,260 |
| `IpeManageCache` | 8,485 |
| `ProcessAsyncCommand` | 7,023 |
| `CreateIcaPasses` | 6,935 |
| `IcaConfigurator_GeneratePassRegisters` | 5,273 |
| `BpsTopologyBuilderCreatePasses` | 5,177 |
| `ICPDomainCmdHandler` | 5,062 |
| `TopologyBuilderConfigScaleDimensions` | 4,681 |
| `IspConfigFrame` | 4,069 |
| `PopulateClcIQSettings` | 3,772 |
| `BLGenerator_GenerateBL_Core` | 3,446 |
| `DJManager_CreateDeferredJob` | 3,416 |
| `AddIpeFrameProcessToHangDump` | 3,059 |

and the symbol prefixes name the subsystem: `Ipe` 61, `Bps` 74, `ICA` 117, `Cdm` 28,
`ICPH` 30, `HFI` 13. The `ICP*` API surface is fully named — 42 distinct `ICP*` symbols,
among them `ICPHalSetInitRequest`, `ICPHalSetInitResponse`,
`ICPHostInterface_postMessage`, `ICPDomainCreate`, `ICPDomainResumeWarmBoot`,
`ICPHalGetSharedmemProps`, `ICPHalProgramInterruptEnableToHost`, `smem_image_version`.

**One distinction that matters.** The 90 source filenames above come from the **symbol
table** and are mostly the C library and Xtensa HAL (`xprintf.c`, `memmove.c`,
`mpu_set_attr.c`, `xtensa/tie/xt_core.h`) — only eight are ICP-specific (`CDMVirtualHal.c`,
`virtualhw.c`, `board_init.c`, `clibrary_init.c`, `camera_top.h`, `cdmpayload.h`,
`qc_version.c`, `oem_version.c`). The **DWARF path strings** are where the product sources
are, and there are far more of them: 729 distinct `.c`/`.h` names appear as NUL-terminated
strings, 232 of them ICP-related, including `b/fw_core/ICP/ICP1/src/cdmdomain.c`,
`…/icpdomain.c`, `…/icpebpsdomain.c`, `…/icphostinterface.c`, `…/ICP/hal/src/hfihal_lx7.c`,
`…/ICP/Common/src/hfiqueue.c`, and the full `HLD/Clc/` tuning-block set (`lsc_v42.c`,
`demosaic_v38.c`, `ltm_v20.c`, `bayer_ltm_v12.c`, `asf_v34.c`, … 90-odd `*_vNN.c` files).

**This is unusual and worth stating plainly: the vendor shipped an unstripped,
DWARF-bearing build of the camera ICP firmware in the vendor partition.** 84.5% of the
file is debug/symbol data. It is the reason §3.3 can corroborate the ISA without a
disassembler, and it means the function-level structure of this firmware is legible
without any RE tooling beyond an ELF parser.

`[N]` This does not mean instruction-level RE is possible here: no Xtensa disassembler is
available, so the *code* remains undecoded even though every function is named.

### 5.2 `.mbn` is the stripped, hash-bearing image `[F]`

The `.mbn`'s 21 phdrs are the `.mdt`'s 21 (`filesz` vectors identical), and its phdr list
equals the `.elf`'s 19 shifted by one, with the header (`b00`, 724 B) prepended and the
hash appended:

| check | result |
|---|---|
| `.mbn` phdr[1..19] `p_filesz` == `.elf` phdr[0..18] `p_filesz` | **True** |
| `.mbn` phdr[1..19] `p_vaddr` == `.elf` phdr[0..18] `p_vaddr` | **True** |
| `.mbn` segment *bodies* identical to `.elf` bodies (11 non-empty) | **11/11** |
| `.mbn` segment at declared `p_offset` | **13/13** |
| hash block (`b20`) present in `.mbn` | **True** |
| hash block (`b20`) present in `.elf` | **False** |
| section headers in `.mbn` | 0 |
| `len(mbn) == ph[20].p_offset + ph[20].p_filesz` | **True** |

The only `p_flags` difference between `.elf` and `.mbn` in the shifted range is uniform:
every `.mbn` phdr 1–19 carries `BIT(27)` (`0x08000000`) that its `.elf` counterpart does
not. So `.elf` → `.mbn` is "add the relocatable bit, prepend the header segment, append the
hash, drop the sections".

### 5.3 So the build pipeline is `[I]`

`[I]` The chain is: link to an unstripped ELF (`.elf`, 3.3 MB, DWARF `-g3`), strip and
attach the hash (`.mbn`, 517 KB), then emit the two PEP-format pieces for a split loader
(`.mdt` = header + hash, and the 21 `.bNN`). `[F]` for all sizes and byte identities;
the stage order is inference from the size relationship and the symbol/section presence.

`[N]` Why the vendor partition ships *all three* forms plus the loose segments is `[U]` —
that is 4.5 MB of redundancy for one firmware. No source explains it.

### 5.4 The `.elf` and `.mbn` are different builds from the matrix `[F]`

None of the four disk builds' md5s appears among the matrix's 26 distinct `.mdt` md5s:

| build | disk md5 | in matrix? |
|---|---|---|
| FP6 | `0c284e2351c29a5e6ac1a4641d3a0301` | **no** |
| Poco_F5 | `fc2604d0…` | **no** |
| Pad 6 Pro | `0b4fe307…` | **no** |
| Mi 12S Ultra | `ce6fc139…` | **no** |

The matrix records FP6's `.mdt` as `20016e3f00ec764406dfff1bd1138c4d`. So the payloads in
the database and the payloads on disk are **different builds of the same firmware**, which
is the standing reason a disk measurement cannot be assumed to describe a matrix row.
Every structural claim in §4 is invariant across all four builds and therefore safe; every
md5-level claim is build-specific.

---

## 6. `db_type` is wrong on all 28 `.mdt` rows `[F]`

| `db_type` | rows in `camera` |
|---|---:|
| UNKNOWN | 1,493 |
| FIRMWARE | 36 |
| **ELF64** | **29** |
| FIRMWARE6 | 25 |
| WIFI_BLUETOOTH | 9 |
| TOUCHSCREEN | 8 |
| FIRMWARE10 | 8 |
| FIRMWARE5 | 3 |

Two of those labels are the same family of files. All **11** `anc*` rows in the
camera bucket are camera userspace tuning models, and they are split across two
`db_type`s: the 3 `FIRMWARE5` rows are `anc.bin`, and the 8 `TOUCHSCREEN` rows are
its siblings (`anc_front.bin`, `anc_main.bin`, `anc_wide.bin`, `anc_1080p.bin`,
`anc_4k.bin`, `anc_cn.bin`, `anc_eu.bin`, `anc_ob_mask_1352_2400.bin`). On FP5
`anc.bin`, `anc_front.bin` and `anc_wide.bin` are one byte-identical payload under
three names with two different labels. Neither `FIRMWARE5` nor `TOUCHSCREEN` names
a loader: `anc.bin` sits at `vendor/etc/camera/`, which is not on the kernel's
`/lib/firmware` search path, and no mainline `camss` file calls
`request_firmware()`. Contract and evidence in `research/drivers/firmware5.md`
(#883).

28 of the 29 `ELF64` rows are `CAMERA_ICP.mdt` (the 29th is `CAMERA_ICP.b00`, also
ELF32). All 28 are ELF**32**:

| evidence | value |
|---|---|
| `e_ident[EI_CLASS]` at offset 4 | **1** (ELFCLASS32) on all four disk builds |
| `e_phentsize` | **32** on all four |
| `e_ehsize` | **52** on all four |
| `mdt_header_valid()` in `mdt_loader.c` requires `e_phentsize == sizeof(struct elf32_phdr)` | passes only because they are ELF32 |

So the label `ELF64` is wrong on 28/28 rows and on the accompanying `b00`. This is the
same defect class the SoC work found on other `.b00` files
(`research/fleet/qdsp6sw-container.md` §2.1 notes `mdt_header_valid()` "rejects ELF64
outright" — a row labelled `ELF64` in this database would be rejected by the very loader
the repository cites). Report-only: this note does not edit the CSV.

---

## 7. Two label defects `[F]`

### 7.1 50 `camera` rows live in `vendor/gpu/kbc` `[F]`

`unified_ksqs.bin` accounts for 50 rows across 50 devices, 26,037,918 B, and every one of
them sits at `…/vendor/gpu/kbc` — the directory that corpus-wide holds 50
`sequence_manifest.bin` files belonging to the **GPU** kernel-cache family:

| fact | value |
|---|---:|
| `camera` rows under `vendor/gpu/kbc` | **50** |
| distinct sizes of `unified_ksqs.bin` | 5 (209,153 / 211,997 / 318,222 / 390,660 / 796,357) |
| `db_type` split | `FIRMWARE6` 25, `UNKNOWN` 25 |
| vendors | oneplus 14, motorola 13, xiaomi 12, sony 5, fairphone 2, nothing 2, realme 2 |
| `sequence_manifest.bin` rows in the same dir, labelled blank | 50 |

`unified_ksqs.bin` is the only name in the subfamily with a `gpu/kbc` path. `[I]` "ksqs"
reads as a kernel-sequence queue/scheduler table feeding the same GPU kernel-cache
machinery as its directory neighbour, and `db_type=FIRMWARE6` on exactly half the rows
suggests the lab already suspected it was not camera. Whether it is GPU-side or a
shared GPU/camera table is `[U]`; what is `[F]` is that its directory says `gpu` and its
subfamily says `camera`.

### 7.2 Three `.img` rows are camera VPU firmware at `…/radio` `[F]`

| filename | size | device | path |
|---|---:|---|---|
| `cam_vpu1.img` | 1,150,976 | Redmi_10S | `xiaomi/rosemary/radio` |
| `cam_vpu2.img` | 12,165,120 | Redmi_10S | `xiaomi/rosemary/radio` |
| `cam_vpu3.img` | 143,360 | Redmi_10S | `xiaomi/rosemary/radio` |

These are labelled `camera` but sit in the device's **radio** partition directory. `[I]`
`cam_vpu*` is camera VPU firmware (the MediaTek camera coprocessor images that `other-media`
documents for `vpu*`), staged into `radio/` by that device's partition layout. This is a
path-vs-label mismatch of the same kind as §7.1, in the opposite direction: here the
*label* looks right and the *directory* looks wrong. 3 rows, 13,459,456 B. `[U]` which is
authoritative. Not resolved here.

---

## 8. `CAMERA_ICP` in the matrix: 41 rows, 25 devices `[F]`

| metric | value |
|---|---:|
| rows with `CAMERA_ICP` in the filename | **41** |
| devices | **25** |
| `.mdt` rows | **28** |
| `.bNN` rows | **13** (all `Edge_40_Pro`) |
| distinct `.mdt` md5 | **26** of 28 |
| priority | P3 40, P1 1 |
| `db_type` | `ELF64` 29, `UNKNOWN` 12 |

`.mdt` size clusters: **5,484 ×21, 5,004 ×5, 4,704 ×2**.

Two md5 collisions, both benign:

| md5 | rows | explanation |
|---|---|---|
| `6c6d8ef1…` | 2 | same device `Edge_40_Pro`, filed at both `vendor/firmware` and `modem/image` |
| `77b56183…` | 2 | `OnePlus_12R` (`aston`) and `OnePlus_11_5G` (`salami`) — one build, two devices |

`Edge_40_Pro` is the only device with loose `.bNN` rows — 13 of them, at `modem/image`,
in the same directory as one of its two `.mdt` copies. The matrix alone is enough to check
the container law on this device:

```
b00 724 + b20 4760 = 5484 = .mdt
```

which is §4.2's identity, confirmed from database fields with no disk access.

The 13 loose segments and their sizes match the FP6 layout in shape but **not** in size
(`b01` 372 vs 460, `b08` 439,992 vs 433,784, `b17` 14,236 vs 24,084) — different build,
same structure. `[I]` Consistent with §5.4: the matrix holds different builds.

### 8.1 The one P2/P1 concentration is a device artifact `[F]`

Priority is P3 on 1,574 rows, P2 on 20 and P1 on 17. **All 17 P1 rows are FP6**, and they
are FP6's entire `camera` contribution minus nothing — i.e. FP6's camera rows are
uniformly P1 regardless of what they contain. Priority here tracks *device* coverage
interest, not blob criticality; §2's functional split is the better guide to what matters.

---

## 9. Rule 1 corrections owed

### 9.1 To `research/fleet/other-media.md` §7 — applied in place `[F]`

Its statement that `CAMERA_ICP` is "out of local reach" with "no claim" about the FP6 ISA
is stale because a different issue had already answered it. The correction is applied in
place in that file, dated, and it names
`research/qualcomm/docs/fp6-architecture-census.md` / `results/census.md` as where the
answer already lived. Its (correct) `vpu20/30/33` conclusion is preserved untouched — this
note confirms it from a different file in the same tree.

### 9.2 To `research/fleet/wifi-wpss.md` §2.4 — nothing owed, widened `[F]`

That note states `.mdt = b00 ‖ b<hash-index>` from 6 `wpss` devices and is **correct**.
It is not contradicted; it is confirmed on **38 of the 39** testable files, spanning **35
distinct `.mdt` stems** (`CAMERA_ICP`, `a615_zap`, `a630_zap`, `a650_zap`, `a660_zap`,
`adsp`, `adsp_dtb`, `cdsp`, `cdsp_dtb`, `cpusys_vm`, `evass`, `facereg`, `ipa_fws`,
`ipa_uc`, `modem`, `wpss`, plus nineteen `image_*`), and the index range it could not
observe (1–47) is recorded here in §4.4. The 39th testable file is
`implementations/historic/fp2/fixtures/synth_modem.mdt`, a synthetic stub; it is the only
stem in the 36-file test set with no conforming instance. No edit to that file: it scoped
itself to `wpss`, and its rule survives.

### 9.3 To `research/qualcomm/results/census.md` — nothing owed `[F]`

The per-file labels are right: L653 `.b00`, L674 `.elf`, L675 `.mbn`, L676 `.mdt` are all
`Xtensa`, and L677 `CAMERA_ICP_170.elf` is `ARM`. That is the prior art §3.1 credits. Its
histogram row `| QDSP6 / Hexagon | 94 |` sits under a `| machine | count |` header and
means 94 *files* with `e_machine=164`, matching `fp6-architecture-census.md` L32; `Xtensa |
12` appears in the same table. No defect, no edit.

### 9.4 To `research/fleet/other-media.md` §0 — already correct, no edit `[F]`

§0's headline already says `e_machine=94` is `EM_XTENSA` and that `CAMERA_ICP.*` was
mislabelled RISC-V. That claim is right and is not touched.

---

## 10. Honest negatives

### 10.1 No public document describes this container or its filenames `[N]`

Recorded 0-hit queries (2026-11-24):

| query | result |
|---|---|
| `"CAMERA_ICP" xtensa oreo camera icp firmware "fw_name"` | **0 results** |
| `qcom_mdt_load "mdt" "b00"` | **0 results** |
| `"proprietary_vendor_xiaomi" cupid vendor firmware CAMERA_ICP` | **0 results** |
| `"CAMERA_ICP.mdt" cupid OR zeus xiaomi 4704` | **0 results** |

`linux-firmware`'s `WHENCE` (main, 540,393 B / 11,920 lines, fetched 2026-11-24) has **0**
case-insensitive hits for `CAMERA_ICP`, while it does carry the neighbouring `venus`
entries (`qcom/venus-1.8/venus.mbn`). The container *grammar* is
documented (mainline `mdt_loader.c`, the Qualcomm MBN/SIF documentation, `pil-splitter`,
the Rust `mbn` crate, IDA's MBN loader — all credited in `other-media.md` §9); what no
source describes is `CAMERA_ICP` specifically: the segment **role table** in §4.1, why the
hash sits at index 20 here and 1 or 12 elsewhere, and any of the 410 filenames.

So the segment roles below index 8 are **structural only**: index, size, flags. What
`b01` (460 B) or `b07` (16 B) *does* is `[U]`. Only indices 0 (header), 20 (hash) and the
4 MiB/1 MiB BSS segments have identified roles.

### 10.2 The 410 filenames are almost entirely undocumented `[N]`

No public source explains `night_align_lsc_tbl_40963072.bin`, `selfbokehmodel.bin`,
`DREAM_4_5_354_654.bin`, `awb_parameter_default.bin`, `unified_ksqs.bin`, or any of the
`MOD_HKRes*` model names. §2's classification is by **path and filename convention**, not
by parsed content — no AI model file was opened, and the claim "60.5% of bytes are AI/ML
models" is a claim about *directory placement and naming*, `[I]` for semantics, `[F]` for
the byte arithmetic.

### 10.3 88% of bytes were never opened `[N]`

**621 distinct non-empty payloads** (622 distinct `md5_db`, of which one is the empty-file
md5 `d41d8cd9…` behind all eight zero-byte rows) carry 4,563,019,282 B, and not one of
those payloads was opened. The functional split in §2 would be overturned by opening a
sample; the byte totals would not.

### 10.4 No ISA on 1,584 of 1,611 rows `[N]`

ISA was measured only on files named `CAMERA_ICP.mdt` (26 rows), `CAMERA_ICP.b00` (1 row),
and the disk-only names `CAMERA_ICP.elf` / `.mbn` / `_170.elf` that have no matrix row at
all. That covers **27 rows**; the remaining **1,584** have **no** ISA measurement, and the
database's one populated `isa_identified` value is the incorrect one (§3.2). Nothing here
infers an ISA from an extension, and `CAMERA_ICP_1.mdt` (2 rows, same firmware, different
filename) is *not* in the measured set.

### 10.5 The `.mdn`/`.elf` build provenance is `[U]`

Why the vendor tree ships `.elf`, `.mbn`, `.mdt` and 21 loose segments for one firmware
(4.5 MB for one image) is unexplained. §5.3's pipeline is inference.

### 10.6 The core model is `[I]`, not `[F]`

The build paths say `tensilica-lx7`; the register map, cycle behaviour and ABI are
unverified. §3.3 records this as `[I]`.

### 10.7 Report-only, nothing fixed `[N]`

Two label defects (§7.1 50 rows at `gpu/kbc`; §7.2 3 rows at `radio`) and one `db_type`
defect (§6, 28 rows `ELF64` on ELF32) are **reported, not repaired**. This note does not
edit the coverage matrix.

---

## 11. Method

Every number above is the output of a command run this session against
`upstream-contribution/blob-database/coverage-matrix.csv` and the payload files named in
the inputs. No payload byte is committed, and the note contains **no raw byte samples at
all** — only sizes, offsets, counts, `e_machine`/`e_type`/`e_flags` values, md5 prefixes,
and symbol and string names. Stdlib Python 3 only, run `python3 -I`, no third-party
libraries — `struct` for ELF parsing, `hashlib` for digests, `csv`/`collections` for the
census.

Derived quantities and the arithmetic that produces them:

| quantity | derivation |
|---|---|
| hash segment | `(p_flags & (7<<24)) == (2<<24)` over `e_phnum` headers at `e_phoff` |
| ELF class | `e_ident[4]`: 1 = ELF32, 2 = ELF64 |
| `b00` size | equals `e_ehsize + e_phnum × e_phentsize` (52 + 21×32 = 724) |
| split form | hash at `e_ehsize + e_phnum×e_phentsize` rather than at its `p_offset` |
| segment identity | `file[p_offset : p_offset+p_filesz]` compared to the matching `.bNN` |
| name/pairs census | basename of `filename`; pairs are `(device, basename)` |

The `CAMERA_ICP` on-disk assertions were checked on **four independent public builds** —
FP6 (`larry`), Poco_F5 (`marble`), Pad 6 Pro (`liuqin`), Mi 12S Ultra (`thor`) — of which
only FP6 ships the `.elf`/`.mbn`/`.mdt`/`.bNN` split tree; the `.mdt` law in §4.4 was
checked on **39** files. Where a claim rests on one build, §5.4 says so.

Reproduce the central check:

```python
import struct
TYPE_MASK, TYPE_HASH = 7 << 24, 2 << 24
mdt = open("CAMERA_ICP.mdt", "rb").read()
phoff, phentsize, phnum = (struct.unpack_from("<I", mdt, 28)[0],
                           struct.unpack_from("<H", mdt, 42)[0],
                           struct.unpack_from("<H", mdt, 44)[0])
ph = [struct.unpack_from("<8I", mdt, phoff + i * phentsize) for i in range(phnum)]
hidx = [i for i, p in enumerate(ph) if (p[6] & TYPE_MASK) == TYPE_HASH][0]
assert mdt == open("CAMERA_ICP.b00", "rb").read() + open(f"CAMERA_ICP.b{hidx:02d}", "rb").read()
assert len(mdt) == ph[0][4] + ph[hidx][4]
```

Both assertions pass on the FP6 build, and produce `hidx = 20`, `724 + 4760 = 5484`.
