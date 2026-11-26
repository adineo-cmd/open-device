# `gpu-compute` — one filename, `fastrpc_shell_0`, the Hexagon user-PD shell (3 rows, 3 devices)

Analysis date: 2026-11-26. Analyst: OC-1 (`100milionseek`), issue
[#2057](https://github.com/adineo-cmd/open-device/issues/2057).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; **thirteen real `fastrpc_shell_*` payloads**, which is what makes this
note byte-level rather than size-only — seven extracted from two on-disk
LineageOS dumps (`lineage-fp6` `dsp-adsp`/`dsp-cdsp`, fetched 2026-11-09;
`instantnoodle/dsp-ext4` `adsp`/`cdsp`/`sdsp`, fetched 2026-11-18) and six
fetched today from `linux-msm/hexagon-dsp-binaries` branch `trunk`
(2026-11-26), plus one payload recovered **from inside** an on-disk
`dsp.img`; `torvalds/linux` `drivers/misc/fastrpc.c` (69,506 B, 2,831 lines,
fetched 2026-11-26) for the interface contract;
`qualcomm/fastrpc` and `linux-msm/hexagon-dsp-binaries` `README.md` (3,355 B,
fetched 2026-11-26) for the naming convention; `linux-firmware` `WHENCE`
(542,288 B, 11,954 lines, fetched 2026-11-26) as the upstream negative;
Check Point Research's Pwn2Own DSP write-up (2021-05-06, fetched 2026-11-26)
for third-party corroboration; and
`research/qualcomm/results/census.md`, `research/fleet/dsp-tz-map.md` and
`research/fleet/qsee-crossgen.md` as cited prior art.

Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `gpu-compute` bucket is 3 rows, 3 devices, 2,523,240 B,
**one filename** (`fastrpc_shell_0`), and **three builds** — and it is not a
compute workload bucket at all. It is one artifact: the Hexagon DSP's FastRPC
**user-PD shell image**, the generic program frame the DSP loads to run a user
process's skeleton libraries. The token `gpu` and the token `compute` are both
wrong, and the name is a misnomer of exactly the same class as `sensors` for
`snsc.bin` (`research/fleet/other-sensors.md`, §2 and §6.1): a bucket named
after a guess about what the file is, when the file is one file.

Two independent decodes make the artifact legible without any census payload.
First, the `_N` suffix **is the driver's domain id**: `drivers/misc/fastrpc.c`
defines `ADSP_DOMAIN_ID (0)`, `MDSP_DOMAIN_ID (1)`, `SDSP_DOMAIN_ID (2)`,
`CDSP_DOMAIN_ID (3)`, `GDSP_DOMAIN_ID (4)`, and every on-disk directory agrees
with every filename — `adsp/`↔`_0`, `sdsp/`↔`_2`, `cdsp/`↔`_3`, 3 of 3. So
`fastrpc_shell_<N>` names the user-PD shell for DSP domain `N`. Second, the
container is a **plain ELF32 `ET_DYN` shared object**, `e_machine=164`
(`EM_QDSP6`), on **13 of 13** builds measured — a family-level fact, not a
sample of two.

The bucket is therefore not a compute class but a **filename class**, and the
corpus's actual compute label is somewhere else entirely: `db_type=COMPUTE` is
carried by **880 rows that are all `blob_family=cdsp`** and 828 of them are
named `cdsp.*` — the CDSP PIL image set. The three `gpu-compute` rows carry
`db_type=ELF64`, `blob_family=other`, and share **zero** rows with the
`COMPUTE` label. The matrix has a compute bucket and it is not this one.

There is one defect to report and one to correct. The defect: `db_type=ELF64`
on all 3 rows, against ELF**32** on 13 of 13 same-family builds — the same
wrong-label pattern already recorded for 28/28 rows in
`research/fleet/other-camera.md` §6 and 757 `.mdt` rows in
`research/fleet/other-misc.md` §7.3. The correction: a prior note in this
session treated `census.md`'s `e50a473fb4edcee4` as a truncated **md5** and
inferred a mismatch; it is the **sha256** column, and the fp6 copy matches it
exactly (§4.2). That build *is* the census payload.

---

## 0. Headline

1. **`[F]` The bucket is 3 rows / 3 devices / 1 basename / 3 payloads /
   2,523,240 B.** 0.0088% of corpus rows and 0.0036% of corpus bytes;
   0.0200% of `other` rows and 0.0178% of `other` bytes. It is **#13 of 13**
   `other` subfamilies on both axes — the last bucket in the family by rows
   *and* by bytes.

2. **`[F]` `gpu-compute` is one filename.** All 3 rows are
   `filename=fastrpc_shell_0`; across the whole 33,917-row corpus only **3
   rows** contain `fastrpc` in the filename, and they are these three. There
   is no second name in the bucket.

3. **`[F]` The artifact is the Hexagon FastRPC user-PD shell, not a GPU
   workload.** It is an ELF32 `ET_DYN` shared object, `e_machine=164`
   (`EM_QDSP6`), on **13 of 13** measured builds. Per `qualcomm/fastrpc`'s
   README it is "a shell executable to run in the user protection domain (PD)
   on the DSP"; per Check Point it is "the special shell process
   (`/vendor/dsp/fastrpc_shell_0` for aDSP and `/vendor/dsp/fastrpc_shell_3`
   for cDSP) … loaded on the DSP when a user process is spawned".

4. **`[F]` The `_N` suffix decodes to the driver's DSP domain id, 3 of 3.**
   `adsp/fastrpc_shell_0`↔0, `sdsp/fastrpc_shell_2`↔2,
   `cdsp/fastrpc_shell_3`↔3. The driver defines five ids (0–4); two of them
   (MDSP 1, GDSP 4) are absent from both trees, so their numbering rests on
   the constants alone.

5. **`[F]` The ELF grammar is uniform across 13 builds.** Class 1 (ELF32),
   `EI_DATA` 1, `e_type` 3 (`ET_DYN`), `e_machine` 164, `e_ehsize` 52,
   `e_phentsize` 32, `e_shentsize` 40, and `e_phoff == e_ehsize == 52` on
   **13 of 13**. Section headers end exactly at EOF (`slack 0`, 13 of 13).
   `e_flags` bits[11:0] is the Hexagon ISA version: **V66** (`0x66`) on 10
   builds, **V73** (`0x73`) on 3.

6. **`[F]` Size does not determine build — demonstrated three ways.** Edge_30
   and Phone_1 are both **841,072 B** with different md5s. The public tree has
   three files at **845,584 B** in **2** md5s and five at **845,632 B** in
   **3** md5s. And the single public 841,072 B file does not match either
   census 841,072 B row.

7. **`[F]` `_unsigned` is an independent build, not a stripped copy.**
   `fastrpc_shell_unsigned_3` diverges from `fastrpc_shell_3` at **offset 32**
   (inside the ELF header) on both devices, is not a prefix or a suffix of it,
   and differs in **9 of 28** (fp6) and **12 of 25** (instantnoodle) sections
   by size — including `.bss` growing by **+1,310,744 B** / **+1,043,592 B**.
   Both halves are ELF32/164; the relationship between them is `[N]`.

8. **`[F]` `db_type=ELF64` on 3 of 3 rows is wrong, or at minimum unverified.**
   Every same-family build is ELF32. `ELF64` is set on 3,284 corpus rows of
   which 3,248 have a blank `isa_identified`, and `mdt` files alone are 1,572
   of them — the label is applied by habit, not by parse.

9. **`[N]` No census payload obtainable; `filename:fastrpc_shell_0` returns 8
   GitHub hits, all SDM660 build-tree intermediates.** linux-firmware's
   `WHENCE` has **0** `fastrpc` hits. The three census md5s appear in none of
   the 13 payloads measured.

---

## 1. The bucket in numbers `[F]`

| quantity | value |
|---|---|
| rows | **3** |
| devices | **3** |
| distinct basenames | **1** (`fastrpc_shell_0`) |
| distinct sizes | **2** |
| distinct md5 | **3** |
| total bytes | **2,523,240** |
| % of corpus rows | 0.0088% |
| % of corpus bytes | 0.0036% |
| % of `other` rows | 0.0200% |
| % of `other` bytes | 0.0178% |
| `db_type` | `ELF64` on 3/3 |
| `priority` | `P2` on 1, `P3` on 2 |
| `vendor` | `motorola`, `fairphone`, `nothing` — 1 each |
| `soc` | populated 3/3, 3 distinct |
| `isa_identified` | blank on 3/3 |
| `interface_documented` | `n` on 3/3 |
| `sha256_if_listed` | blank on 3/3 |
| `db_path` | `…/modem/image` on 3/3 |

`python3` assertion passed: `841072×2 + 841096 = 2523240`, and the two sizes are
**24 B apart**.

### 1.1 Rank inside `other` `[F]`

| rank | by rows | rows | by bytes | bytes |
|---:|---|---:|---:|---:|
| 9 | `nfc` | 75 | `nfc` | 9,677,922 |
| 10 | `esim` | 41 | `esim` | 8,407,085 |
| 11 | `sensors` | 5 | `audio` | 5,418,315 |
| 12 | `tinysys` | 4 | `tinysys` | 4,132,864 |
| **13** | **`gpu-compute`** | **3** | **`gpu-compute`** | **2,523,240** |

`other` as a whole is 14,987 rows / 14,152,121,440 B across 13 subfamilies,
with a median of **284 rows** and **29,190,348 B**. `gpu-compute` is below both
medians by two orders of magnitude on rows and one on bytes — the smallest
bucket in the family, and the only one that is a single filename.

### 1.2 One filename, three payloads `[F]`

| device | vendor | soc | size | md5 |
|---|---|---|---:|---|
| Edge_30 | motorola | Qualcomm SM7325-AE Snapdragon 778G 5G | 841,072 | `eb1b256c5a76ce2c3acf8507a27964a4` |
| FP5 | fairphone | Qualcomm QCM6490 | 841,096 | `b6e6dbb529def8281f74e2c8e10d6af1` |
| Phone_1 | nothing | Qualcomm SM7325-AE Snapdragon 778G+ 5G | 841,072 | `a69cf7d50862b3155d315472adc83423` |

Three distinct md5s over two distinct sizes, so the map is **not** a bijection —
the first of three independent size↔build failures in this family (§4).

`[F]` The three devices are three vendors on two SoC parts: two
`SM7325-AE` (Snapdragon 778G / 778G+, the same die binned twice) and one
`QCM6490`. So the row set spans a vendor axis and almost no SoC axis.

### 1.3 Where the file actually sits `[F]`

| device | census path | codename |
|---|---|---|
| Edge_30 | `motorola/dubai/modem/image` | `dubai` |
| FP5 | `fairphone/FP5/modem/image` | `FP5` |
| Phone_1 | `nothing/Spacewar/modem/image` | `Spacewar` |

`[F]` All three are filed under **`modem/image`**, a directory that carries
**22,285 rows across 74 devices** in the corpus. But the artifact is an **ADSP
domain** object (§2), and the corpus has **zero** rows whose `db_path` contains
`/dsp/` or `dsp-adsp` — the directory that every real device tree uses for
these files. So the path is a compression artifact, not a location: the shell
lives inside `modem.img`, which is why the census finds it there (§2.3).

`[F]` The label is also not `gpu`. Inside `modem/image` the corpus carries
**276 rows** of `blob_family=gpu`, and they are all `fpctzapp.bNN` — the
trust-zone applications, nothing to do with FastRPC. `gpu-compute` is a third
thing filed in the same directory as both.

---

## 2. The `_N` suffix is the domain id `[F]`

### 2.1 The driver's constants

`[F]` `drivers/misc/fastrpc.c` lines 31–35, verbatim:

```c
#define ADSP_DOMAIN_ID (0)
#define MDSP_DOMAIN_ID (1)
#define SDSP_DOMAIN_ID (2)
#define CDSP_DOMAIN_ID (3)
#define GDSP_DOMAIN_ID (4)
```

`[F]` `fastrpc_get_domain_id()` (line 2454) maps a device-tree domain string to
that id by prefix — `adsp`, `cdsp`, `mdsp`, `sdsp`, `gdsp` — and returns
`-EINVAL` for anything else.

`[F]` The same file also defines the protection-domain classes the shell runs
in: `ROOT_PD (0)` (line 124), `USER_PD (1)` (line 125), `SENSORS_PD (2)`
(line 126). And it caps a loaded module at `INIT_FILELEN_MAX (2 * 1024 * 1024)`
(line 65) = 2 MiB, checked at line 1597 (`if (init.filelen > INIT_FILELEN_MAX)`).

### 2.2 The on-disk directories agree, 3 of 3

The seven `fastrpc_shell_*` files on disk sit in directories named for the same
domains:

| directory | filename | domain id | agrees |
|---|---|---:|---|
| `dsp-adsp/` | `fastrpc_shell_0` | 0 | **yes** |
| `sdsp/` | `fastrpc_shell_2` | 2 | **yes** |
| `cdsp/` | `fastrpc_shell_3` | 3 | **yes** |
| `dsp-cdsp/` | `fastrpc_shell_3` | 3 | **yes** |
| `dsp-cdsp/` | `fastrpc_shell_unsigned_3` | 3 | **yes** |

`[F]` Five files, three domains, zero mismatches. This is a decode, not a
guess: the directory name and the filename suffix are two independent
witnesses, and they never disagree.

`[F]` The public tree confirms the convention and extends it. Across
`linux-msm/hexagon-dsp-binaries` `trunk` (2,501 entries, 208 `fastrpc` basenames)
the suffixes present are **0–6**:

| artifact | suffixes present | entries |
|---|---|---:|
| `fastrpc_shell_N` | 0, 2, 3, 4, 5, 6 | 133 |
| `fastrpc_shell_unsigned_N` | 3, 4, 5, 6 | 67 |
| `fastrpc_shell` (un-suffixed) | — | 5 |
| **total** | | **205** |

`[U]` Suffixes **5 and 6** exist publicly but the mainline driver defines only
0–4. Either the driver has not caught up with newer parts, or 5/6 are
Qualcomm-internal numbering outside the upstream id set. Not resolvable from
bytes.

`[I]` The unsigned variants appear **only** at 3, 4, 5 and 6, and the driver
says why: at line 2606, `case ADSP_DOMAIN_ID: case MDSP_DOMAIN_ID: case
SDSP_DOMAIN_ID:` sets `data->unsigned_support = false` with the comment
*"Unsigned PD offloading is only supported on CDSP and GDSP"*, while
`case CDSP_DOMAIN_ID: case GDSP_DOMAIN_ID:` sets it `true` (lines 2612–2614).
So the presence of `_unsigned` at 3 and 4 and its absence at 0 and 2 is exactly
the driver's rule, and the on-disk pair `cdsp/fastrpc_shell_unsigned_3` is the
predicted artifact. `[U]` 5 and 6 sit outside the rule's stated scope.

### 2.3 The path oddity, and why it exists `[F]`

`[F]` In the on-disk `instantnoodle` `modem.img` (192,278,528 B, FAT16,
`bps` 4096, `spc` 4, `fatsz` 13, root at `0x1b000`, data at `0x1f000)`, the
shell names appear **inside** the DSP firmware blobs, not as files:

| image | size | md5 | `fastrpc_shell_N` names inside | `/statichashes/` entries |
|---|---:|---|---:|---:|
| `adsp.b04` | 1,961,932 | `052ce311e3a0c79f` | **0** only | 8 |
| `slpi.b04` | 2,077,548 | `64d4aac91296cfaf` | **2** only | 6 |
| `cdsp.b05` | 2,803,308 | `525d9c4ed934658c` | **3** only | 79 |

`[F]` The suffix set inside each image matches that image's own domain, 3 of 3.
`adsp.b04` contains `fastrpc_shell_0` and no other number; `cdsp.b05` contains
`fastrpc_shell_3` and no other; `slpi.b04` (the SDSP image) contains
`fastrpc_shell_2` and no other. That is a third independent witness to §2.2.

`[F]` `slpi.b04` also carries the compressed payload: at `0x196e02` the string
`fs:/fastrpc_shell/fastrpc_shell_2.z`, then a zlib stream at `0x196e28`
consuming **370,290** bytes and inflating to **706,960** B (md5
`4b08466ec6a3bcfee81bfe86a628578f`), which begins `7f454c46 01010100` — an
ELF32 header. Parsed: class 1, `e_type` 3, `e_machine` 164, `e_flags` `0x66`
(V66), `e_entry` `0x94`, `e_phoff` 52, `e_shoff` 706,080, `phnum` 3, `shnum` 22,
`shstrndx` 21, slack 0. Its `.comment` is `QuIC LLVM Hexagon Clang version
8.2.05 (based on LLVM 5.0.0git-c7d6f70)` with `hexagon-clang-82-326`.

`[I]` So there are **three** delivery shapes for the same artifact: a
standalone file in a `dsp.img` ext4 tree, a deflate stream embedded in an SDSP
PIL image, and a name referenced from `/statichashes/` in the ADSP and CDSP
images. Whichever shape a device dump yields, the census's `modem/image` path is
a statement about which partition the extraction came from, not about where the
loader looks.

`[F]` The standalone copies in `dsp.img` are 4 KiB-aligned and byte-identical to
the ext4 tree's files:

| file | size | in `dsp.img` at | aligned | identical |
|---|---:|---|---|---|
| `adsp/fastrpc_shell_0` | 908,340 | `0x6c1000` | yes | yes |
| `cdsp/fastrpc_shell_3` | 930,932 | `0xbed000` | yes | yes |
| `cdsp/fastrpc_shell_unsigned_3` | 925,352 | `0xcd1000` | yes | yes |
| `sdsp/fastrpc_shell_2` | 893,772 | `0x1b9a000` | yes | yes |

---

## 3. The ELF container, on 13 builds `[F]`

### 3.1 Header fields

| build | size | `e_flags` | ISA | `e_entry` | `phoff` | `shoff` | `phnum` | `shnum` | `shstrndx` | slack |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| fp6 `dsp-adsp/shell_0` | 1,219,384 | `0x73` | V73 | `0xb4` | 52 | 1,218,224 | 4 | 29 | 26 | 0 |
| fp6 `dsp-cdsp/shell_3` | 1,303,040 | `0x73` | V73 | `0xb4` | 52 | 1,301,920 | 4 | 28 | 25 | 0 |
| fp6 `dsp-cdsp/shell_unsigned_3` | 1,298,776 | `0x73` | V73 | `0xb4` | 52 | 1,297,656 | 4 | 28 | 25 | 0 |
| inst `adsp/shell_0` | 908,340 | `0x66` | V66 | `0x94` | 52 | 907,340 | 3 | 25 | 22 | 0 |
| inst `sdsp/shell_2` | 893,772 | `0x66` | V66 | `0x94` | 52 | 892,772 | 3 | 25 | 22 | 0 |
| inst `cdsp/shell_3` | 930,932 | `0x66` | V66 | `0x94` | 52 | 929,932 | 3 | 25 | 22 | 0 |
| inst `cdsp/shell_unsigned_3` | 925,352 | `0x66` | V66 | `0x94` | 52 | 924,352 | 3 | 25 | 22 | 0 |
| dragon-q6a `shell_0` | 841,072 | `0x66` | V66 | `0x94` | 52 | 840,112 | 3 | 24 | 21 | 0 |
| rb3 `…c8-00149` | 845,584 | `0x66` | V66 | `0x94` | 52 | 844,624 | 3 | 24 | 21 | 0 |
| rb3 `…c8-00217` | 845,584 | `0x66` | V66 | `0x94` | 52 | 844,624 | 3 | 24 | 21 | 0 |
| rb3 `…c8-00246` | 845,632 | `0x66` | V66 | `0x94` | 52 | 844,672 | 3 | 24 | 21 | 0 |
| rb3 `…c8-00249.1` | 845,632 | `0x66` | V66 | `0x94` | 52 | 844,672 | 3 | 24 | 21 | 0 |
| rb3 `…c8-00256.2` | 845,632 | `0x66` | V66 | `0x94` | 52 | 844,672 | 3 | 24 | 21 | 0 |

`[F]` Thirteen of thirteen: `EI_CLASS` 1 (ELF32), `EI_DATA` 1 (LE), `e_type` 3
(`ET_DYN`), `e_machine` 164 (`EM_QDSP6`), `e_ehsize` 52, `e_phentsize` 32,
`e_shentsize` 40. That is a **family-level** result, not a two-sample one.

`[F]` `e_phoff` is **52** on 13 of 13 — identical to `e_ehsize`, i.e. the
program header table starts immediately after the 52-byte ELF32 header. It is
**not** `e_ehsize + e_phnum × e_phentsize` (148 with 3 phdrs, 180 with 4).
The `b00 == e_ehsize + e_phnum × e_phentsize` law documented in
`research/fleet/other-misc.md` §1 for `.mdt` containers has **no meaning
here** — that law describes a split container whose first part holds the header
*and* the phdr table, whereas this is one monolithic ELF. It is not applied
and not claimed.

`[F]` `e_shoff + e_shnum × e_shentsize == filesize` exactly on 13 of 13 — the
section header table is the last thing in the file, with zero trailing slack.
That matches the same statement in `research/fleet/dsp-tz-map.md` §2 ("file
size == e_shoff + e_shnum*40 on every blob") for the 57 SDM845 DSP ELFs.

`[F]` `e_flags` decodes as a Hexagon ISA version. LLVM's `BinaryFormat/ELF.h`
defines `EF_HEXAGON_ISA_V66 = 0x00000066`, `EF_HEXAGON_ISA_V73 = 0x00000073`,
and `EF_HEXAGON_ISA` as bits[11:0]. So `0x66` = **V66** on 10 builds and `0x73`
= **V73** on 3, and the tiny-core flag (bit 15) is clear on all 13.

`[F]` `phnum` is 3 on the nine V66 builds and 4 on the three V73 builds. The
fourth, on the V73 set, is `PT_TLS` (type 4, `filesz` 0, `memsz` 8, flags 4).
So program-header count is a **generation** marker: V66 → 3, V73 → 4.

`[F]` `shnum` is **build-dependent, not domain-dependent**: 25 on all four
instantnoodle builds regardless of domain, 28 on both fp6 CDSP builds, 29 on
the fp6 ADSP build, 24 on all five KODIAK builds. Any claim that section count
tracks the domain is false.

### 3.2 Program headers

`[F]` The V66 three-phdr shape, on `dragon-q6a` (841,072 B):

| # | type | `p_offset` | `p_vaddr` | `p_filesz` | `p_memsz` | flags | align |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | `PT_LOAD` | 0 | 0 | 694,844 | 694,844 | 5 (R+X) | `0x1000` |
| 1 | `PT_LOAD` | `0xaa000` | `0xaa000` | 22,504 | 246,248 | 6 (R+W) | `0x1000` |
| 2 | `PT_DYNAMIC` | `0xaa000` | `0xaa000` | 152 | 152 | 6 | 4 |

`[F]` Two `PT_LOAD`s: read+execute from offset 0, read+write from `0xaa000`,
plus a 152-byte `PT_DYNAMIC` inside the second — the ordinary shape of a
position-independent shared object at 4 KiB page granularity. `p_memsz` >
`p_filesz` on the RW segment (246,248 vs 22,504) is the `.bss` the loader zero
fills.

`[F]` The V73 four-phdr shape, on fp6 (1,219,384 B): `PT_LOAD` 0–926,524
(R+X), `PT_LOAD` `0xe3000` filesz 33,108 / memsz 478,376 (R+W), `PT_DYNAMIC`
`0xe3000` 152 B, `PT_TLS` `0xe3000` `filesz` 0 / `memsz` 8 — thread-local
storage, which the V66 builds do not have.

### 3.3 Section table

`[F]` The 24 sections of `dragon-q6a`, in order, with the offsets a downstream
parser needs:

| # | name | type | `sh_addr` | `sh_offset` | `sh_size` |
|---:|---|---|---:|---:|---:|
| 0 | — | NULL | 0 | 0 | 0 |
| 1 | `.start` | PROGBITS | `0x94` | 148 | 248 |
| 2 | `.dynsym` | DYNSYM | `0x18c` | 396 | 26,960 |
| 3 | `.dynstr` | STRTAB | `0x6adc` | 27,356 | 22,403 |
| 4 | `.hash` | 5 | `0xc260` | 49,760 | 13,488 |
| 5 | `.rela.dyn` | RELA | `0xf710` | 63,248 | 32,748 |
| 6 | `.init` | PROGBITS | `0x17700` | 96,000 | 128 |
| 7 | `.text` | PROGBITS | `0x17780` | 96,128 | **509,384** |
| 8 | `.fini` | PROGBITS | `0x93d60` | 605,536 | 68 |
| 9 | `.rodata` | PROGBITS | `0x93da8` | 605,608 | 88,975 |
| 10 | `.eh_frame` | PROGBITS | `0xa9940` | 694,592 | 252 |
| 11 | `.dynamic` | DYNAMIC | `0xaa000` | 696,320 | 152 |
| 12 | `.sdata` | PROGBITS | `0xaa098` | 696,472 | 4 |
| 13 | `.data.rel.ro` | PROGBITS | `0xaa0a0` | 696,480 | 8,572 |
| 14 | `.data` | PROGBITS | `0xac220` | 705,056 | 7,092 |
| 15 | `.ctors` | PROGBITS | `0xaddd4` | 712,148 | 8 |
| 16 | `.dtors` | PROGBITS | `0xadddc` | 712,156 | 12 |
| 17 | `.got` | PROGBITS | `0xadde8` | 712,168 | 6,640 |
| 18 | `.got.plt` | PROGBITS | `0xaf7d8` | 718,808 | 16 |
| 19 | `.bss` | NOBITS | `0xaf7e8` | 718,824 | 223,744 |
| 20 | `.comment` | PROGBITS | 0 | 718,824 | 225 |
| 21 | `.shstrtab` | STRTAB | 0 | 719,049 | 179 |
| 22 | `.symtab` | SYMTAB | 0 | 719,228 | 64,288 |
| 23 | `.strtab` | STRTAB | 0 | 783,516 | 56,596 |

`[F]` Read as bytes: `.text` is the largest section at **509,384 B = 60.56%** of
the file; `.rodata` 88,975; `.bss` 223,744 (not present in the file). The
largest *stored* data structures after `.text` are `.symtab` (64,288) and
`.strtab` (56,596), so roughly 14% of the artifact is symbol and string
metadata — a debug-friendly build, not a stripped one.

`[F]` On fp6 the same read gives `.text` 703,000 = **57.65%**, and three extra
sections appear: `.rela.plt` (12), `.plt` (64), `.tbss` (4), plus two
annotations — `.note.llvm.cgmdinfo` (90,126 B) and `.note.qc.cov` (8,017 B).
`[I]` Code-coverage and call-graph metadata shipped inside the image, which is
a development-build signature.

### 3.4 What the bytes say about themselves

`[F]` Every build carries a `.comment` with the toolchain that produced it:

| build | first `.comment` string | `.comment` size |
|---|---|---:|
| dragon-q6a | `QuIC LLVM Hexagon Clang version 8.4.07 (based on LLVM 10.0.0)` | 225 |
| rb3 `…c8-00149` | same 8.4.07 / LLVM 10.0.0 | 225 |
| rb3 `…c8-00246` | same 8.4.07 / LLVM 10.0.0 | 225 |
| inst `adsp`/`sdsp`/`cdsp` | `QuIC LLVM Hexagon Clang version 8.3.06 (based on LLVM 7.0.0)` | 209 |
| fp6 `adsp` | `QuIC LLVM Hexagon Clang version 8.7.05 Engineering Release: hexagon-clang-87-6198` | 8,817 |
| fp6 `cdsp` | `QuIC LLVM Hexagon Clang version 8.6.04 Engineering Release: hexagon-clang-86-7585` | 9,110 |

`[F]` The engineering-release line gives the exact compiler build:
`hexagon-clang-84-5479` for the KODIAK builds, `hexagon-clang-83-4733` for
instantnoodle. The fp6 `.comment` is 40× larger because it is a release build
with the full annotation block, including link command lines
(`/pkg/qct/software/hexagon/releases/tools/8.6.04/Tools/bin/hexagon-link
-mv73 -g -E -nostdlib …`). `[F]` That `-mv73` independently corroborates the
`e_flags` V73 decode from a different field of the same file.

`[F]` Each build also carries a `CRMBuilds` path tag naming its firmware
release: `ADSP.HT.5.5.c9-00028-KODIAK-2_20250819_030546` (dragon),
`ADSP.HT.5.5.c8-00149-KODIAK-1_20240603_025047` (rb3-00149),
`ADSP.HT.5.5.c8-00246-KODIAK-1_20251211_183427` (rb3-00246),
`ADSP.HT.5.3-00614-SM8250-1_20210822_233012` (instantnoodle adsp),
`CDSP.HT.2.3-00602-SM8250-1.551792.1.5` (instantnoodle cdsp),
`CDSP.HT.3.0-00953-LANAI-1_20250603_02…` (fp6 cdsp),
`LPAIDSP.HT.1.0-01111-LANAI-1_20250717_022841` (fp6 adsp).

`[F]` That last one is worth a line: **fp6's ADSP shell is tagged `LPAIDSP`**,
not `ADSP` — the low-power-AI DSP naming — while its directory says `dsp-adsp`
and its filename says `_0`. Three naming schemes for one domain, and only the
`_0` suffix and the directory agree with the driver.

`[F]` String census, whole-file byte counts:

| build | `fastrpc` | `hexagon` | `qurt` | `_skel` | `shell` | `QDSP6` |
|---|---:|---:|---:|---:|---:|---:|
| dragon-q6a | 297 | 217 | 789 | 29 | 2 | **0** |
| rb3-00149 | 301 | 217 | 792 | 29 | 2 | **0** |
| inst adsp | 388 | 218 | 1,036 | 48 | 3 | **0** |
| fp6 adsp | 529 | 427 | 1,201 | 109 | 96 | **0** |

`[F]` `QDSP6` never appears as a string (0 of 4) even though `e_machine` is 164
(`EM_QDSP6`) — the identifier lives only in the header field. `[F]` The exact
literal `fastrpc_shell_0` occurs **once** in dragon-q6a, at offset `0xa0371`,
preceded by `Kernel received an floating point error` and followed by
`Unknown` / `exception_killer` / `fastrpc_exception` / `listener` /
`listener_hexagon.c` — i.e. it is a *runtime label* the shell prints in its
listener diagnostics, not a path it is loaded from.

`[F]` No build contains a `FASTRPC_SHELL_UNSIGNED_NAME` macro expansion
(0 of 5 checked) — that token exists in the modem firmware's loader strings
(§2.3) but not in the shell ELF.

### 3.5 Entropy and repetition

`[F]` The artifact is ordinary compiled code, not packed:

| build | size | entropy | zlib-9 | ratio | 16 B blocks | distinct | extra dups | max count |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dragon-q6a | 841,072 | 6.6649 | 417,598 | 49.65% | 52,567 | 49,008 | 3,559 | 376 |
| rb3-00149 | 845,584 | 6.6682 | 420,503 | 49.73% | 52,848 | 49,270 | 3,578 | 376 |
| inst adsp | 908,340 | 6.5459 | 432,101 | 47.57% | 56,771 | 53,212 | 3,559 | 376 |

`[F]` ~6.6 bits/byte and a 50% deflate ratio is what `.text` looks like. The
3,559 duplicate 16-byte blocks with a max count of 376 are the all-zero block
(the `.bss`/padding region), not a cipher signature — contrast
`research/fleet/other-sensors.md` §3.1, where 46,718–55,362 duplicates against
a ~1.7×10⁻²⁷ birthday expectation proved ECB. Here the count is ordinary
zero-fill.

`[F]` Each build contains exactly **two** `\x7fELF` occurrences: the real header
at 0, and one at a mid-file offset that is the loader's compare constant
followed immediately by its own error string — `7f454c46 00` then
`bad elf magic in %s`. Positions: `0xa1d5a` (dragon), `0xa2dbd` (rb3-00149),
`0xb215a` (inst adsp), `0xd5a5e` (fp6 adsp), `0xea07a` (fp6 cdsp).
`research/fleet/qsee-crossgen.md` §4 already established this as a false
positive for the SDM845 shells; it holds for all five builds here, 5 of 5.

---

## 4. Size does not determine build `[F]`

This is the reusable finding, and it appears **three** times in this family
across two sources and two size classes.

### 4.1 Three cases in one table `[F]`

| # | size | build A (md5) | build B (md5) | source | verdict |
|---:|---:|---|---|---|---|
| 1 | **841,072** | Edge_30 `eb1b256c…` | Phone_1 `a69cf7d5…` | census | **different** |
| 2 | **845,584** | rb3 `…c8-00149` `1afb6774…` | rb3 `…c8-00217` `9272f230…` | public tree | **different** |
| 3 | **845,632** | `…c8-00246` `f42a7cba…` | `…c8-00249.1` `275a12a3…`, `…c8-00256.2` `145ac290…` | public tree | **three builds** |

`[F]` Case 1 is the census's own data: two rows, one size, two md5s. Case 2 and
case 3 are measured on bytes: the public tree has **3 files at 845,584 B in 2
md5s** and **5 files at 845,632 B in 3 md5s**. So "same size ⇒ same payload"
fails at 2 of the 3 sizes this family exhibits in public.

`[F]` Case 2 is the sharpest because both files are in hand: 845,584 B each,
md5 `1afb6774c8caba405aa158cc943904be` vs `9272f230966161b36597bde3ee0a7da1`,
and **280,727 bytes differ (33.20%)**, first at offset `0x44`. Two builds a
third of a megabyte apart in content, identical in length, differing from
inside the ELF header onward. Section-level: `.text` (513,464 B) is **not**
identical, `.rodata` is **not** identical, `.dynstr` **is** identical
(22,423 B), `.strtab` **is** identical (56,825 B) — so the symbol and string
names are shared while the code is not. `[I]` Same source tree, same symbol
namespace, different compile — consistent with two builds of one release train
four revisions apart.

`[F]` Case 3 splits into two very different distances, which is itself
informative:

| pair | size | differing bytes | share |
|---|---:|---:|---:|
| `…c8-00246` vs `…c8-00249.1` | 845,632 | 83,495 | 9.87% |
| `…c8-00246` vs `…c8-00256.2` | 845,632 | 83,506 | 9.87% |
| `…c8-00249.1` vs `…c8-00256.2` | 845,632 | **739** | **0.09%** |

`[F]` `…c8-00249.1` and `…c8-00256.2` are 99.91% byte-identical at the same
size and still carry different md5s — a 739-byte delta. That is the finest
same-size difference in the set and the clearest demonstration that md5, not
size, is the build identity.

`[F]` Across a size *change*, the distance is also small: 845,584 → 845,632 is
+48 B, and only **four** sections change size — `.text` +320, `.rodata` +184,
`.symtab` +16, `.strtab` +33. Everything else shifts by exactly the inserted
bytes and keeps its length. `[I]` One function and its strings grew; the rest
of the image is the same build.

### 4.2 The prior-art case, and a correction `[F]`

`research/qualcomm/results/census.md` line 61 reads:

```
| `dsp-adsp/fastrpc_shell_0` | 1,219,384 | ELF | QDSP6 / Hexagon | `e50a473fb4edcee4` |
```

`[F]` The column header at line 43 is **`sha256 (16)`**, not md5. Measured on
the fp6 copy: size 1,219,384, `md5[:16]` = `720ba571938cd932`,
**`sha256[:16]` = `e50a473fb4edcee4`** — an exact match.

`[F]` Verified on five rows, not one, to establish the column semantics rather
than fit a single value:

| row | size | claimed | `md5[:16]` | `sha256[:16]` | match |
|---|---:|---|---|---|---|
| `dsp-adsp/fastrpc_shell_0` | 1,219,384 | `e50a473fb4edcee4` | `720ba571938cd932` | `e50a473fb4edcee4` | **sha256** |
| `dsp-cdsp/fastrpc_shell_3` | 1,303,040 | `7521badd4e1a95a4` | `d7b6f47c52e3ad39` | `7521badd4e1a95a4` | **sha256** |
| `dsp-cdsp/fastrpc_shell_unsigned_3` | 1,298,776 | `8090fab798ae465c` | `6b1168025f8343cf` | `8090fab798ae465c` | **sha256** |
| `dsp-adsp/cps_module.so.1` | 293,112 | `0ac7ef9f5b237fc4` | `cefb7ad688212f4a` | `0ac7ef9f5b237fc4` | **sha256** |
| `dsp-adsp/flac_dec_module.so.1` | 41,688 | `126adca960f9a3f3` | `2b83d12f21693566` | `126adca960f9a3f3` | **sha256** |

`[F]` So the fp6 on-disk copy **is** the payload `census.md` describes — same
size, and the 16-byte value matches the column exactly, 3 of 3 for this
filename. A working note earlier in this session compared that value against a
computed **md5**, found no match, and inferred a mismatch; that inference is
**withdrawn**. It was a column-semantics error, not a data discrepancy.

`[F]` What survives from that line is weaker but still true and still worth
recording: `census.md` prints only **16 hex characters (8 bytes)** of the
sha256, both for the fp6 tree and throughout. Two distinct payloads collide in
8 bytes with probability ~2⁻⁶⁴ per pair, so a prefix match is strong evidence
but not proof, and no row in that table can be *disproved* by prefix
comparison. That limit is a property of the table, not of this artifact.

`[F]` The genuine same-size trap from `census.md` is therefore case 1 alone —
Edge_30 and Phone_1, both 841,072, both md5s full-length in `md5_db`. Cases 2
and 3 come from measured bytes.

### 4.3 The census sizes are absent from the public tree `[F]`

`[F]` `linux-msm/hexagon-dsp-binaries` has **57** `fastrpc_shell_0` entries in
**36** distinct sizes, ranging **685,320** to **1,479,200 B**. Neither census
size is represented meaningfully:

| size | entries in public tree |
|---|---:|
| 841,072 (Edge_30, Phone_1) | **1** — `qcs6490/radxa/dragon-q6a/…c9-00028-KODIAK-2` |
| 841,096 (FP5) | **0** |
| 845,584 | 3 |
| 845,632 | 5 |
| 908,340 (instantnoodle) | 0 |
| 1,219,384 (fp6) | 0 |

`[F]` The single public 841,072 B file is md5 `09e699f721f38533ea2453a8189e95b7`,
which matches **neither** census 841,072 B row. So even the one size the public
tree shares with the census resolves to a third build.

`[F]` 841,096 B — the FP5 row — occurs **nowhere** in the tree: 0 entries at
that size for `fastrpc_shell_0`, and 0 entries at that size for any basename.
Its nearest neighbours are 841,072 and 845,584. `[U]` Whether FP5's 24-byte
excess over Edge_30 is one extra section, one extra function, or a different
link is unknowable without the payload.

`[F]` For scale, the whole public corpus of shell builds spans 685,320 →
1,479,200 B, a factor of 2.16. The three census sizes sit at 841,072–841,096 —
within 24 B of each other, near the low end. `[U]` That clustering suggests the
three devices ship near-identical firmware generations, but three points cannot
establish it.

---

## 5. `_unsigned` is an independent build, not a stripped copy `[N]`

The obvious hypothesis — `fastrpc_shell_unsigned_3` is `fastrpc_shell_3` with a
signature removed — is **false**, and it is testable three ways on two devices.

| test | fp6 | instantnoodle |
|---|---|---|
| sizes | 1,303,040 vs 1,298,776 | 930,932 vs 925,352 |
| size delta | **4,264 B** | **5,580 B** |
| `unsigned == signed[:len(u)]` | **no** | **no** |
| `unsigned == signed[-len(u):]` | **no** | **no** |
| first differing byte | **32** (`0x20`) | **32** (`0x20`) |
| sections differing in size or type | **9 of 28** | **12 of 25** |

`[F]` Offset 32 is `e_shoff` inside the ELF header — the two files disagree
before any section exists. A truncation, a suffix, or a signature append would
agree through the header by construction.

`[F]` Section-level, fp6:

| section | type | signed | unsigned | delta |
|---|---|---:|---:|---:|
| `.rela.dyn` | RELA | 45,696 | 46,092 | +396 |
| `.text` | PROGBITS | 763,628 | 761,056 | −2,572 |
| `.rodata` | PROGBITS | 134,807 | 134,496 | −311 |
| `.data.rel.ro` | PROGBITS | 14,460 | 14,628 | +168 |
| **`.bss`** | **NOBITS** | **514,828** | **1,825,572** | **+1,310,744** |
| `.comment` | PROGBITS | 9,110 | 9,749 | +639 |
| `.note.llvm.cgmdinfo` | NOTE | 91,571 | 91,196 | −375 |
| `.symtab` | SYMTAB | 82,528 | 82,288 | −240 |
| `.strtab` | STRTAB | 72,585 | 72,204 | −381 |

`[F]` On instantnoodle the same test gives 12 of 25 sections differing,
`.text` −1,832, `.bss` **+1,043,592**, `.rodata` −1,344, `.data` −1,032.

`[F]` A `.bss` that **grows** by 1.25 MiB while `.text` **shrinks** is not a
signature removal in either direction. `[F]` The section-name lists are
identical (28 of 28 names match on fp6) and `e_entry` is unchanged (`0xb4` on
both), so the two are the same program linked twice.

`[F]` The evidence of *why* is in the strings. The `_unsigned` build's
`.comment` carries the link command line and the object paths that produced it,
and they name a **different build directory**: `unsigned_img/qdsp6/milos.cdsp.prod/`
and `unsigned_img/build/milos.cdsp.prod/fastrpc_shell_unsigned_3.elf.map`, with
61 occurrences of `unsigned_img`. The signed build names `signed_img/…`, also 61
occurrences. Two link invocations from two trees, one per variant.

`[F]` And the arithmetic corroborates: the extra `.bss` in the unsigned build
is the heap the unsigned PD is given, and `adsp_proc/platform/fastrpc_heap/` is
in the unsigned build's own source list. `[I]` The unsigned variant is linked
with a larger static heap because it cannot allocate the same way inside the
signed PD's memory envelope. That is a plausible reading of the numbers; the
numbers themselves do not name it.

**Verdict `[N]`:** `_unsigned` is not `signed` minus a signature — the two
differ from ELF-header offset 32 onward and 9 of 28 (fp6) / 12 of 25
(instantnoodle) sections change size, including a NOBITS section by
+1,310,744 B / +1,043,592 B. Both are ELF32, `e_machine=164`, `e_type=3`. The
relationship between the pair is **not** a truncation and **not** a suffix;
**why two variants ship** is `[U]`.

---

## 6. `gpu-compute` is a misnomer, and the corpus has a real compute bucket `[F]`

### 6.1 The name is wrong on both tokens `[F]`

`[F]` **Not `gpu`.** The corpus has a `gpu` family. In `modem/image` it is
**276 rows**, and all of them are `fpctzapp.bNN` — trust-zone applications. No
row in the corpus has a `gpu`-family filename anywhere near `fastrpc`. The
shell is not a GPU artifact; it is the Hexagon DSP's user-PD loader image.

`[F]` **Not `compute`.** The corpus has a compute label, `db_type=COMPUTE`, on
**880 rows across 63 devices / 280,601,355 B**. Every one of those 880 rows is
`blob_family=cdsp`, 828 are named `cdsp.*`, and the remaining 52 are
`cdsp_dtb.*`. So the corpus's own definition of "compute" is the **CDSP PIL
image set** — `cdsp.mdt` and its `cdsp.bNN` segments. The three `gpu-compute`
rows carry `db_type=ELF64`, `blob_family=other`, and share **zero** rows with
the `COMPUTE` label.

`[F]` So the matrix contains two unrelated things whose names both suggest
compute, and the smaller one is the FastRPC shell. A reader who trusts the
subfamily name will conclude the bucket is a GPU workload class; it is one file.

### 6.2 The precedent, and what it establishes `[F]`

`[F]` `research/fleet/other-sensors.md` §6.1 records the same defect shape: a
bucket named `sensors` holding one file, `snsc.bin`, which is not a sensor
artifact but a camera capture trigger — the label assigned from a substring
(`sns` read as "sensor") rather than from evidence. That note's framing applies
verbatim here.

`[I]` The mechanism is the same: a single-file bucket gets a name by guessing at
the file's role. `gpu-compute` is the guess "this is acceleration code", which
is half right — the shell *is* the frame that runs accelerated DSP code — but
the bucket is not the workload, it is the loader.

`[F]` One structural difference from `sensors`, and it matters for triage: the
`sensors` bucket had 5 rows across 5 devices and 3 payloads, whereas
`gpu-compute` has 3 rows across 3 devices and 3 payloads — one build per
device, no sharing at all. There is no platform cluster here to reason from,
which is why §4 is built on public same-family builds instead.

`[N]` No rename is proposed. Changing a corpus label is a `blob-database`
change, not a `research/` change, and this issue's scope is documentation.

---

## 7. Defects in the record `[F]`

### 7.1 `db_type=ELF64` on 3 of 3 rows `[F]`

`[F]` Every one of the 13 same-family builds is **ELF32** (`EI_CLASS=1`),
`e_machine=164`, `e_type=3`. The matrix types all 3 rows `ELF64`.

`[F]` The honest framing: the two available `gpu-compute`-filename builds (and
eleven more of the same family) are ELF32 `e_machine=164`; the matrix types all
3 rows `ELF64`; **whether the three census builds are ELF32 is `[U]`** because no
census payload was obtainable — but the `ELF64` label is at minimum unverified
and inconsistent with **13 of 13** same-family builds measured.

`[F]` This is the third instance of the same labelling defect in this repo, and
the pattern is now well established:

| note | finding |
|---|---|
| `research/fleet/other-misc.md` §7.3 | `db_type=ELF64` on **757 of 757** `.mdt` rows, against 43 ELF32 + 35 ELF64 on disk |
| `research/fleet/other-camera.md` §6 | `db_type=ELF64` wrong on **28 of 28** rows, all ELF32 |
| **this note** | `db_type=ELF64` on **3 of 3** rows, against 13 of 13 ELF32 |

`[F]` The label's prevalence explains the defect. `ELF64` is set on **3,284**
corpus rows; **3,248** of those have a blank `isa_identified` — 98.9% carry no
checked ISA claim at all. The single largest contributor is `.mdt` at **1,572
rows (47.9%)**, with `ipa_fws.mdt` alone at 77. So `ELF64` is applied as a
default for "some kind of ELF container", not as a parsed value, and a row that
is genuinely ELF32 inherits it silently.

`[F]` For context, `ELF64` is *not* wrong everywhere: 36 rows do carry an ISA
string, including 25 `AArch64`, 4 `QDSP6 / Hexagon`, and RV32 entries. The
label is correct where it was checked and a default where it was not.

### 7.2 `isa_identified` is blank on 3 of 3 rows `[F]`

`[F]` The ISA is not merely inferable, it is **in the header**: `e_machine=164`
(`EM_QDSP6`, glibc `elf.h` line 298 `#define EM_QDSP6 164 /* QUALCOMM DSP6 */`)
plus `e_flags` bits[11:0] giving the Hexagon generation. On the measured
builds that resolves to V66 or V73. Three rows carry a blank where a
two-field read would fill it.

`[U]` The census builds' `e_flags` cannot be read without their payloads, so
their ISA *version* is unknown — but their `e_machine` almost certainly 164,
since no other machine value appears in 13 same-family builds.

### 7.3 `interface_documented=n` is right for this file, and misleading `[F]`

`[F]` `interface_documented` is `n` on 3 of 3. That is **correct as a statement
about the file**: no driver in the tree names or loads it. `grep -c
fastrpc_shell` in `drivers/misc/fastrpc.c` → **0**; `grep -c request_firmware`
→ **0**. The driver is a runtime RPC driver (ioctl, mmap, dmabuf, PD
create/attach, `FASTRPC_INIT_HANDLE`), not a firmware loader.

`[F]` But the *interface the file participates in* is documented in that same
driver, at length: `FASTRPC_INIT_HANDLE (1)` (line 42),
`FASTRPC_DSP_UTILITIES_HANDLE (2)` (line 43), the PD classes, and a comment
block drawing the invoke payload layout as "Arguments → Invoke Buffer list →
Page info list → Optional info → Inline ARGS". So `n` is accurate and also
unhelpful — the reader concludes nothing is known, when the contract is in
mainline.

`[F]` One more negative worth recording, because it is the natural next
question: `linux-firmware`'s `WHENCE` (542,288 B, 11,954 lines) has **0**
`fastrpc` hits and **0** `shell` hits, while `adsp` appears **133** times. The
shell is not a linux-firmware blob; it ships in the vendor's `hexagon-dsp-binaries`
side repository instead, whose README says exactly that: linux-firmware carries
the DSP firmware, and the FastRPC shell and skeletons are "additional set of
binaries to be executed on the DSP side".

---

## 8. What this adds to the existing record `[F]`

Cites, not re-derivations — the ISA and the SDM845 container shape were already
established:

- `research/fleet/dsp-tz-map.md` §2 lists `adsp/fastrpc_shell_0` at **873,128 B**,
  md5 `b9ffea38e0f6787ee2f28337e6756c6d`, plus `cdsp/fastrpc_shell_3`
  (878,584 B, `2d7756f3c676a4bc178035fa8494302b`) and `sdsp/fastrpc_shell_2`
  (857,208 B, `053fca51499728c69d8479439134c724`), and states the shared shape
  as "ELF32 LE, `e_machine` 164, `e_type` 3, section headers present at file
  end".
- `research/fleet/qsee-crossgen.md` §4 settles the embedded-ELF question: the
  mid-file `\x7fELF` in each SDM845 shell is the loader's compare constant plus
  its `bad elf magic in %s` string, not an appended image.
- `research/qualcomm/results/census.md` line 61 gives
  `dsp-adsp/fastrpc_shell_0` at **1,219,384 B**, "ELF / QDSP6 / Hexagon", with
  the sha256 prefix `e50a473fb4edcee4` (§4.2).

What is genuinely new here:

- the `_N` suffix is decoded to the driver's domain id and confirmed 3 of 3 by
  directory name + 3 of 3 again by in-image `fastrpc_shell_N` strings (§2);
- the ELF grammar is raised from a 57-blob SDM845 observation to a **13-build**
  family statement, and `e_phoff == e_ehsize == 52` is measured on all 13 (§3.1);
- `e_flags` is decoded as the Hexagon ISA version, independently corroborated by
  the `-mv73` in a link command line (§3.4);
- `_unsigned` is shown **not** to be a stripped copy, with section-level deltas,
  and the two variants are traced to two separate `signed_img/`/`unsigned_img/`
  link trees (§5);
- the size↔build failure is demonstrated three ways, two of them on bytes (§4);
- the `gpu-compute` label is shown to collide with the corpus's real `COMPUTE`
  bucket, which is the CDSP PIL image set on 880 rows (§6.1);
- three delivery shapes for one artifact are measured — standalone ext4 file,
  deflate stream inside an SDSP PIL image, `/statichashes/` name reference in
  ADSP and CDSP images (§2.3).

---

## 9. Honest negatives `[N]`

- **No census payload.** None of the three md5s — `eb1b256c5a76ce2c3acf8507a27964a4`,
  `b6e6dbb529def8281f74e2c8e10d6af1`, `a69cf7d50862b3155d315472adc83423` —
  matches any of the 13 payloads measured. Edge_30, FP5 and Phone_1's own builds
  are unobtained, so §7.1's census-class question stays `[U]`.
- **No public payload for the three devices.** GitHub `/search/code`
  `filename:fastrpc_shell_0` → **8** hits, and every one is under
  `adsp_proc/build/bsp/core_libs/build/core_libs/qdsp6/660.adsp.prod/660_xml/660.adsp.prod/`
  in two SDM660 firmware repos (`David112x/android-firmware-qti-sdm660`,
  `me-cafebabe-backyard/android-firmware-qti-sdm660`) — build-tree intermediates
  for a different SoC. `fastrpc_shell_0 dubai` → 0; `fastrpc_shell_0 Spacewar` → 0.
- **The vendor trees carry the partition, not the file.** All three
  `proprietary-files.txt`-equivalent manifests
  (`dubai`/`Spacewar`/`FP5` `*-vendor.mk`) reference only
  `vendor/lib{,64}/libsns_fastRPC_util.so`; `radio/modem.img` is a **Git LFS
  pointer** in all three (sizes 136,769,708 / 180,908,032 / 190,541,824 B), and
  the LFS object is not retrievable — the batch API returns
  `404 Object does not exist on the server` for FP5's
  `a4b947bcbc0ad843b68f2b5040b1722a4554a0e3ff5eb089dc2a141505da120c`.
- **`fastrpc_shell_0` is not a filesystem path in any of them.** In the FAT16
  `instantnoodle` `modem.img` there is no `fastrpc`-named file entry in `/image/`
  at all; the name exists only as a **string inside** `adsp.b04` / `cdsp.b05` /
  `slpi.b04` and as a `/statichashes/` reference. Where the shell lives on a
  shipped device — `/vendor/dsp/` per Check Point — is a runtime path the census
  does not see.
- **No `.mdt` relation.** The shell is not a PIL image and does not participate
  in the `b00`/`mdt` container at all (§3.1). Nothing here re-derives
  `other-misc.md`'s `b00` law.
- **`_unsigned` vs `signed`: relationship `[N]`, purpose `[U]`.** Not a
  truncation, not a suffix — proven. *Why* two variants ship, and what the
  extra 1.25 MiB of `.bss` is for, is not established from bytes.
- **The 3 census builds' `e_flags`, `phnum`, `shnum` and ISA version are `[U]`.**
  13 builds give a strong prior (V66 or V73, 3 or 4 phdrs, 24–29 sections) but
  the three rows themselves were never opened.
- **Suffixes 5 and 6 exist publicly but are not driver-defined.** The constants
  stop at `GDSP_DOMAIN_ID (4)`; the public tree ships `fastrpc_shell_5`,
  `_6`, `_unsigned_5`, `_unsigned_6`. Unresolved.
- **FP5's 841,096 B does not exist publicly.** 0 entries at that size for
  `fastrpc_shell_0` and 0 for any basename in the 2,501-entry tree. Its 24-byte
  excess over Edge_30 is unexplained.

---

## 10. Gate 0 — prior art search `[N]`

Recorded as required by the issue template. All queries run 2026-11-26.

**GitHub code search** (REST `/search/code`, exact query strings):

| query | hits | result |
|---|---:|---|
| `fastrpc_shell_0` | 1,220 | overwhelmingly build-tree references and device dumps; no analysis |
| `fastrpc_shell` | 4,176 | same, broader |
| `filename:fastrpc_shell_0` | **8** | all `*.xml.i` / `*.xml.pp` intermediates under `660.adsp.prod/660_xml/` in two SDM660 repos |
| `modem/image/fastrpc_shell_0` | 1 | `Klozz/qti_missi_dump:all_files.txt` — a filesystem listing, no analysis |
| `fastrpc_shell_0 dubai` | **0** | — |
| `fastrpc_shell_0 Spacewar` | **0** | — |

**Web** (searxng, aggregating Google/Bing/Brave/DDG):

- `fastrpc_shell_0 Qualcomm`
- `FastRPC shell firmware Hexagon user PD`
- `fastrpc_shell_0 shell_3 domain id naming adsp cdsp sdsp`
- `linux-msm hexagon-dsp-binaries fastrpc_shell_0 adsp cdsp naming`

`[F]` The substantive hits are worth recording because they *are* the prior art
that made §2 possible:

- **`qualcomm/fastrpc` README** — "FastRPC user driver on DSP | User mode code
  that includes a shell executable to run in the user protection domain (PD) on
  the DSP and complete the remote invocations to the skel library". That is the
  definition this note uses.
- **`linux-msm/hexagon-dsp-binaries` README** — "These binaries include
  `fastrpc_shell_N` (where N is 0, 1, 2, 3), `fastrpc_shell_unsigned_N` (N = 3,
  special version of shell for CDSP only)". The `N`-is-a-number statement plus
  the unsigned-only-on-CDSP statement, both confirmed against the driver.
- **Check Point Research, "Pwn2Own Qualcomm DSP" (2021-05-06)** — "The special
  shell process (`/vendor/dsp/fastrpc_shell_0` for aDSP and
  `/vendor/dsp/fastrpc_shell_3` for cDSP) is loaded on the DSP when a user
  process is spawned. The shell is responsible for invocation of the skeleton
  and object libraries." And on the unsigned case: "Signature-free dynamic
  shared objects are run inside an Unsigned PD … limited in its access to
  underlying DSP drivers and thread priorities."
- **ctfiot.com (Chinese)** — "在ADSP中，它的名字是`fastrpc_shell_0`，而在CDSP中，有两个不同的shell：`fastrpc_shell_3`和…" — the same 0/3 split, independently.
- **LLVM `BinaryFormat/ELF.h`** — `EF_HEXAGON_ISA_V66 = 0x00000066`,
  `EF_HEXAGON_ISA_V73 = 0x00000073`, `EF_HEXAGON_ISA = 0x000003ff` (bits[11:0]).
  That is the source for the §3.1 ISA decode.

`[N]` **No page describes the container's internal layout, the section set, the
size distribution, or the `unsigned`/`signed` divergence.** Every source
describes *what the shell is for*; none describes *what is in it*. That gap is
what §3 and §5 fill.

**Kernel / linux-firmware** `[N]`: `WHENCE`, fetched 2026-11-26, 542,288 B,
11,954 lines — `grep -ci fastrpc` → **0**, `grep -ci shell` → **0**,
`grep -ci adsp` → **133**. The shell is not a linux-firmware blob and no
upstream loader names it: `drivers/misc/fastrpc.c`, 69,506 B / 2,831 lines,
`grep -c fastrpc_shell` → **0**, `grep -c request_firmware` → **0**.

**Decision**: prior art exists for the artifact's *role* and its *naming*, and
none for its *contents*. Not a duplicate; this DELTA adds the byte-level
characterisation and the label defect.

---

## 11. Open items `[U]`

1. **Obtain the three census payloads** — Edge_30 `eb1b256c…`, FP5
   `b6e6dbb5…`, Phone_1 `a69cf7d5…`. This settles their ELF class (§7.1), their
   `e_flags` ISA version, and whether FP5's 24 extra bytes are structural. The
   viable route is the LFS `modem.img` objects, three of which are currently
   `404` at the batch endpoint.
2. **Resolve suffixes 5 and 6.** The driver defines 0–4; the public tree ships
   5 and 6 including unsigned variants. Newer SoCs, or non-upstream numbering?
3. **Explain the `.bss` growth in `_unsigned`** (+1,310,744 B / +1,043,592 B) —
   plausible as a static heap for the unsigned PD, unproven from bytes.
4. **Decode the `.note.llvm.cgmdinfo` / `.note.qc.cov` sections** (90,126 /
   8,017 B on fp6). They are named for call-graph and coverage data; their
   schema is unexamined.
5. **Establish whether `LPAIDSP` is a distinct domain.** fp6's ADSP shell is
   tagged `LPAIDSP.HT.1.0` while its directory says `adsp` and its suffix says
   `_0`. Does the driver's 5-domain map cover it, or is it a sixth?
6. **Confirm the three delivery shapes are exhaustive.** Standalone ext4 file,
   deflate inside `slpi.b04`, name-only in `adsp.b04`/`cdsp.b05`. Whether every
   device uses one of these, or some use an un-deflated in-image copy, is
   unchecked beyond the two dumps here.
7. **Resolve the `gpu-compute` label** with the `blob-database` owner — it
   collides with the real `COMPUTE` (CDSP) bucket and shares no row with it.

---

## 12. Method `[F]`

All commands `python3 -I`, stdlib only. No payload committed; the 13 builds
were either already on disk or fetched to a scratch directory outside the repo,
and only hashes, sizes, offsets, counts and ≤16-byte hex samples appear above.

```python
# census
rows = list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g = [r for r in rows if r['blob_subfamily'] == 'gpu-compute']        # -> 3 rows
sum(int(r['size_bytes']) for r in g)                                 # -> 2523240
len({r['md5_db'] for r in g})                                        # -> 3

# the real COMPUTE bucket, for §6.1
c = [r for r in rows if r['db_type'] == 'COMPUTE']                   # -> 880 rows, all blob_family=cdsp

# ELF header, 13 of 13
cls, dat = d[4], d[5]                                                # -> 1, 1
e_type, e_mach = struct.unpack_from('<HH', d, 16)                    # -> 3, 164
e_flags = struct.unpack_from('<I', d, 36)[0]                         # -> 0x66 / 0x73
eh, pe, pn, se, sn, si = struct.unpack_from('<HHHHHH', d, 40)        # -> 52, 32, 3|4, 40, 24..29
struct.unpack_from('<I', d, 28)[0] == eh                             # phoff == ehsize == 52, 13/13

# ISA decode
ISA = {0x66: 'V66', 0x73: 'V73'}                                     # LLVM EF_HEXAGON_ISA_V*
ISA[e_flags & 0xfff]                                                 # -> V66 on 10, V73 on 3

# section headers end at EOF
len(d) - (shoff + sn * se)                                           # -> 0 on 13/13

# size-vs-build trap, measured on bytes
sum(1 for i in range(n) if a[i] != b[i])                              # 845,584 pair -> 280727 (33.20%)
                                                                     # 845,632 pair -> 83506 / 739

# _unsigned is not a stripped copy
next(i for i in range(n) if s[i] != u[i])                            # -> 32 on both devices
u == s[:len(u)]; u == s[len(s)-len(u):]                              # -> False, False

# domain id agreement (directory vs suffix vs in-image string)
# adsp/shell_0 -> 0, sdsp/shell_2 -> 2, cdsp/shell_3 -> 3            # 3/3

# embedded payload in slpi.b04
zlib.decompressobj().decompress(d[k:k+3000000])                      # 370290 -> 706960 B, head 7f454c46
```

Scratch fetch of the six public builds (2026-11-26) from
`raw.githubusercontent.com/linux-msm/hexagon-dsp-binaries/trunk/qcm6490/…` and
`…/qcs6490/…`; the one duplicate md5 (`…c8-00217` shipped identically under both
`RB3gen2` and `RubikPi3`) is recorded as 2 files / 1 md5, not as 2 builds.
