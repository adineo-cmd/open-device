# `gpu` / Mali CSF firmware — a portable grammar, and prior art whose file offsets are wrong on 5/5 payloads

Analysis date: 2026-11-28. Analyst: OC-1 (`100milionseek`), issue
[#832](https://github.com/adineo-cmd/open-device/issues/832).

Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data
rows) for the census; five real upstream `mali_csffw.bin` payloads from
`linux-firmware` for byte-level verification; the in-tree normative kernel
source `drivers/gpu/drm/panthor/panthor_fw.c`; and one public third-party
implementation, `leegao/panthor2kbase`, which I cite, credit and correct.

Every number below is command output. No payload is committed; samples are ≤16
bytes. Evidence classes: `[F]` fact measured by command, `[I]` inference from
measurements, `[H]` hypothesis, `[N]` honest negative, `[U]` unknown.

**Two corrections to this issue's own REPO-STATE note, stated first `[F]`.**

The 2026-11-20 note says the delta is *"Signature rules absent; no bdwlan GPU
parser."* Measured:

1. **`blob_family=gpu` carries 0 `bdwlan` rows.** All 5,120 `bdwlan` rows in
   the corpus are `blob_family=wifi`. "No bdwlan GPU parser" is a delta against
   an empty set, and building one would have been work on nothing.
2. **The real uncovered slice is Mali**: 65 rows / 13 devices / 5 basenames /
   18,759,680 B, and **zero** committed research in this repository. A `grep`
   for `mali` and `csffw` across `research/` returns no Mali format work. The
   state map's *"no Mali parser"* is the true delta, and it is what this note
   closes.

---

## 0. Headline numbers

| quantity | value |
|---|---:|
| `gpu` rows | **781** |
| `gpu` bytes | **88,036,049** |
| `gpu` devices | 105 |
| `gpu` distinct basenames | 86 |
| rank among 9 families, by bytes | **#9 of 9** (smallest) |
| rank among 9 families, by rows | #8 of 9 |
| share of corpus rows | 2.3027 % |
| share of corpus bytes | 0.1261 % |
| Mali rows | **65** (8.32 % of family rows) |
| Mali bytes | 18,759,680 (21.31 % of family bytes) |
| Mali devices | 13 |
| Mali distinct basenames | 5 |
| distinct Mali md5s in corpus | **10** (across 65 rows) |
| `bdwlan` rows in `blob_family=gpu` | **0** |
| upstream generations verified byte-level | **5** |
| generations where `max(data_end) == file size` | **5 / 5** |

Corpus: 33,917 rows / 69,797,539,502 B.

`gpu` is the **smallest** family by bytes in the whole corpus. That is worth
saying plainly: this is a narrow slice, and the note is correspondingly narrow.

---

## 1. The five verified payloads `[F]`

Nothing in this note is measured on a device from this repository's corpus.
The byte-level sections are measured on five files fetched from
`git.kernel.org/.../firmware/linux-firmware.git` on **2026-11-28**:

| path in `linux-firmware` | bytes | md5 |
|---|---:|---|
| `arm/mali/arch10.8/mali_csffw.bin` | 282,624 | `cd95e83312eec65ff523025b52badb4a` |
| `arm/mali/arch10.10/mali_csffw.bin` | 282,624 | `cd95e83312eec65ff523025b52badb4a` |
| `arm/mali/arch10.12/mali_csffw.bin` | 282,624 | `cd95e83312eec65ff523025b52badb4a` |
| `arm/mali/arch11.8/mali_csffw.bin` | 299,008 | `64fc3695e92756f111f6bc7287ff1569` |
| `arm/mali/arch12.8/mali_csffw.bin` | 307,200 | `15f238b54dbf8aadcbccab55c47c05ac` |
| `arm/mali/arch13.8/mali_csffw.bin` | 311,296 | `98bd8fc1e193f03917fb6e87a2b0529c` |
| `arm/mali/arch14.8/mali_csffw.bin` | 344,064 | `bc2ee99629e05c1c9e88d442680e11aa` |

`arch10.8`, `arch10.10` and `arch10.12` are **byte-identical** (same md5, same
sha1 `3d6bad6fec2efff4b702e36791a39f11c533036f`, `cmp` clean). Seven other
paths — `arch10.5`, `arch10.6`, `arch10.7`, `arch10.9`, `arch10.11`,
`arch11.0`, `arch9.0` — return a **3,265-byte HTML error page**, not a payload
(§8.3). So the distinct set is **five** generations, and the three 10.x copies
are one build republished under three architecture directory names `[F]`.

Twelve paths were requested in the first pass; two more (`arch10.8`, `arch10.10`)
were added to confirm the byte-identity claim. Of the **fourteen** paths, **seven
return 404 and seven return a payload**, and those seven payloads are **five
distinct files** by md5 `[F]`.

**What this does and does not prove `[N]`.** It proves the *grammar* against
real vendor bytes across five generations. It does **not** prove that any of
the 65 corpus rows has this exact content — see §6, where the sizes do not even
overlap.

---

## 2. The container grammar — read from the in-tree driver `[F]`

The grammar is **not new**. It is stated normatively in
`drivers/gpu/drm/panthor/panthor_fw.c` (45,236 B, GPL-2.0, read 2026-11-28):

```c
struct panthor_fw_binary_hdr {
        u32 magic;            /* CSF_FW_BINARY_HEADER_MAGIC 0xc3f13a6e */
        u8  minor;
        u8  major;            /* CSF_FW_BINARY_HEADER_MAJOR_MAX 0 */
        u16 padding1;
        u32 version_hash;
        u32 padding2;
        u32 size;             /* the DESCRIPTOR TABLE size, not the file size */
};

#define CSF_FW_BINARY_ENTRY_TYPE(ehdr)   ((ehdr) & 0xff)
#define CSF_FW_BINARY_ENTRY_SIZE(ehdr)   (((ehdr) >> 8) & 0xff)
#define CSF_FW_BINARY_ENTRY_UPDATE       BIT(30)
#define CSF_FW_BINARY_ENTRY_OPTIONAL     BIT(31)
```

and the walk in `panthor_fw_load()`:

```c
iter.size = hdr.size;
while (iter.offset < hdr.size) {
        ret = panthor_fw_load_entry(ptdev, fw, &iter);
        ...
}
```

So the container is:

```
0x00  20 bytes:  u32 magic | u8 minor | u8 major | u16 pad1
                 u32 version_hash | u32 pad2 | u32 hdr_size
0x14  entry:     u32 ehdr  (type = bits[7:0], size = bits[15:8],
                            bit30 UPDATE, bit31 OPTIONAL)
                 body[size - 4]
                 advance by size, repeat while offset < hdr_size
```

### 2.1 The single most important field `[F]`

**`hdr_size` is the length of the descriptor table, not of the file.** Every
payload's `hdr_size` is under 900 B while the file is a quarter of a megabyte:

| generation | file bytes | `hdr_size` | entries | walk ends at | == `hdr_size` |
|---|---:|---:|---:|---:|:--:|
| arch10.12 | 282,624 | **792** | 24 | 792 | yes |
| arch11.8 | 299,008 | **792** | 24 | 792 | yes |
| arch12.8 | 307,200 | **824** | 25 | 824 | yes |
| arch13.8 | 311,296 | **824** | 25 | 824 | yes |
| arch14.8 | 344,064 | **856** | 26 | 856 | yes |

Five files, five exact walks to `hdr_size`, zero slack. This is the reading
that makes the format portable, and it is the reading the prior art gets wrong
(§4).

### 2.2 Header field values `[F]`

| generation | `major` | `minor` | `version_hash` | `pad1` | `pad2` |
|---|---:|---:|---|---:|---:|
| arch10.12 | 0 | 3 | `0x01050000` | 0 | 0 |
| arch11.8 | 0 | 3 | `0x02080000` | 0 | 0 |
| arch12.8 | 0 | 3 | `0x030d0000` | 0 | 0 |
| arch13.8 | 0 | 3 | `0x030d0000` | 0 | 0 |
| arch14.8 | **0** | **4** | `0x04060000` | 0 | 0 |

`major` is **0 on all five** — which is exactly why the driver's
`hdr.major != CSF_FW_BINARY_HEADER_MAJOR_MAX` check has never fired. `minor`
tracks 3, 3, 3, 3, 4. `version_hash` is the field that actually distinguishes
builds: `0x030d0000` is shared by arch12.8 and arch13.8, so it is a firmware
version hash and **not** a per-file identifier `[I]`.

---

## 3. The section table and the invariant that validates a payload `[F]`

Entry `type 0` is `CSF_FW_BINARY_ENTRY_TYPE_IFACE`, the section descriptor:

```c
struct panthor_fw_binary_section_entry_hdr {
        u32 flags;
        struct { u32 start; u32 end; } va;     /* MCU virtual range */
        struct { u32 start; u32 end; } data;   /* file offsets */
};
```

That struct is 20 B, and the entry is 32 B, so **8 bytes follow it**. Those 8
bytes are a **section name buffer**, not padding: the driver reads
`name_len = iter->size - iter->offset` — that is, whatever is left after the
20-byte struct — and NUL-terminates it. Measured on all 44 type-0 entries
across the five payloads, **byte 0 of that buffer is `0x00` in 44/44 cases**,
so every real section has an **empty name**. The remaining 7 bytes hold stale
`va_start` bytes in 41/44 cases (all three exceptions are the `0x00c00000`
section in arch12.8–14.8, where the tail is all zero) — an artefact of the
build, not a field.

This is worth stating precisely because it is a trap: a parser that assumes
the body is exactly 20 B and then requires the entry to be 20+4 bytes will
still work, but a parser that reads the trailing 8 bytes as a second VA range
will read garbage. The honest grammar is `struct` (20 B) + `name[entry_size-24]`,
and the name is empty in every payload measured `[F]`.

### 3.1 The reference generation, in full `[F]`

`arch10.12`, all eight type-0 entries:

| # | entry off | flags | va range | data range | len |
|---:|---:|---|---|---|---:|
| 0 | 20 | `0x00000009` | `0x00400000`–`0x00410000` | 4892–5016 | 124 |
| 1 | 52 | `0x00000009` | `0x00410000`–`0x00420000` | 5024–9924 | 4,900 |
| 2 | 84 | `0x00000009` | `0x00000000`–`0x00010000` | 4892–5016 | 124 |
| 3 | 116 | `0x0000000d` | `0x00800000`–`0x00820000` | 9924–92872 | 82,948 |
| 4 | 148 | `0x8000000b` | `0x02000000`–`0x02040000` | 92872–271016 | 178,144 |
| 5 | 180 | `0x80000009` | `0x01000000`–`0x01040000` | 92872–271016 | 178,144 |
| 6 | 212 | `0x0000002b` | `0x03000000`–`0x03040000` | 0–0 | **0** |
| 7 | 244 | `0xc000001b` | `0x04000000`–`0x04010000` | 274432–282624 | 8,192 |

Entry 6 is a **zero-length section** — a BSS-style reservation with no file
backing. It is not corruption, and a validator that requires `data_end >
data_start` will wrongly reject the file `[F]`.

There are **two distinct kinds of zero-length section**, and only one of them
is the BSS case `[F]`:

| kind | VA range | flags | present in |
|---|---|---|---|
| BSS reservation | `0x03000000`–`0x03040000` (256 KiB of VA, 0 B of file) | `0x0000002b` | all 5 generations |
| degenerate | `0x00420000`–`0x00420000` (0 B of VA, 0 B of file) | `0x00000009` | **arch14.8 only** |

The second is a new empty code section in the newest generation. It is
zero-length in *both* address spaces, so it reserves nothing and backs nothing
— a slot the build emits but does not fill. A parser must tolerate it for the
same reason as the BSS case, but it is not the same phenomenon and should not
be described as one `[F]`.

### 3.2 The integrity invariant `[F]`

Not `hdr_size`, and not any checksum: the **maximum `data_end` across type-0
sections equals the file size exactly**, on all five generations.

| generation | max `data_end` | file bytes | match |
|---|---:|---:|:--:|
| arch10.12 | 282,624 | 282,624 | **yes** |
| arch11.8 | 299,008 | 299,008 | **yes** |
| arch12.8 | 307,200 | 307,200 | **yes** |
| arch13.8 | 311,296 | 311,296 | **yes** |
| arch14.8 | 344,064 | 344,064 | **yes** |

The section table therefore describes the whole file, and the payload region
begins at `hdr_size` (the first `data_start` is 4,892 > 792). This is a real,
build-independent integrity check and it is the one a parser should use.

### 3.3 Sections alias — naive accounting double-counts `[F]`

Two pairs of virtual ranges point at **the same** file bytes in every
generation:

| generation | aliased file range | VAs sharing it |
|---|---|---|
| arch10.12 | 4892–5016 | `0x00400000`, `0x00000000` |
| arch10.12 | 92872–271016 | `0x02000000`, `0x01000000` |
| arch11.8 | 4892–5020 | `0x00400000`, `0x00000000` |
| arch11.8 | 102456–287160 | `0x02000000`, `0x01000000` |
| arch12.8 | 4924–5052 | `0x00400000`, `0x00000000` |
| arch12.8 | 88288–282784 | `0x02000000`, `0x01000000` |
| arch13.8 | 4932–5092 | `0x00400000`, `0x00000000` |
| arch13.8 | 89352–286888 | `0x02000000`, `0x01000000` |
| arch14.8 | 5060–5220 | `0x00400000`, `0x00000000` |
| arch14.8 | 105968–316856 | `0x02000000`, `0x01000000` |

The consequence is concrete. Summing per-section lengths for `arch10.12` gives
**452,576 B of "covered" data in a 282,624 B file** — 169,952 B more than
exists. The **union** of distinct ranges is **274,308 B**, leaving 8,316 B
genuinely unclaimed:

| generation | distinct ranges | union | file | unclaimed |
|---|---:|---:|---:|---:|
| arch10.12 | 5 | 274,308 | 282,624 | 8,316 |
| arch11.8 | 5 | 290,456 | 299,008 | 8,552 |
| arch12.8 | 6 | 301,900 | 307,200 | 5,300 |
| arch13.8 | 6 | 305,976 | 311,296 | 5,320 |
| arch14.8 | 6 | 335,820 | 344,064 | 8,244 |

The unclaimed bytes are the header/descriptor table plus page padding. A parser
that reports "sections cover the file" is reporting an artefact of
double-counting; the honest statement is "union covers all but ~5–8 KiB" `[F]`.

### 3.4 The build-info section carries a git SHA in plaintext `[F]`

Entry `type 6` is `CSF_FW_BINARY_ENTRY_TYPE_BUILD_INFO_METADATA`, and its body
is `{ u32 meta_start, u32 meta_size }`. `meta_start` is always `hdr_size`
exactly, and the 51 bytes there are ASCII:

| generation | `meta_start` | `meta_size` | content |
|---|---:|---:|---|
| arch10.12 | 792 | 51 | `git_sha: 95a25d71030715381f33105394285e1dcc860a65 \0` |
| arch11.8 | 792 | 51 | same SHA |
| arch12.8 | 824 | 51 | same SHA |
| arch13.8 | 824 | 51 | same SHA |
| arch14.8 | 856 | 51 | `git_sha: 28a24f0ca8655a7e6344648f0bc7647af2d99db5 \0` |

So four of the five upstream payloads were built from the **same firmware git
commit** (`95a25d71…`) even though they ship different sizes and different
`version_hash` values — they are per-architecture *builds* of one source
revision `[I]`. `arch14.8` is the only one from a different revision
(`28a24f0c…`). This is a stronger provenance signal than `version_hash` and it
is not mentioned in the prior art.

The sample is a 40-hex-character commit id, which is public metadata about a
build, not payload content.

---

## 4. Gate 0 verdict: PRIOR-ART for the container; its file offsets fail on 5/5 `[F]`

The closest public implementation is **`leegao/panthor2kbase`**
(`src/emulator/lifted_csffw.c`, 21,354 B; `lifted_csffw.h`), a CSF firmware
lifter with an ARMv7-M Thumb-2 static lifter. It is the most serious prior art
on this format and I am **citing and crediting it, not competing with it**. Its
contribution is the opcode lift; this note's contribution is the container.

Its parser reads the header correctly and then applies constants from
`lifted_csffw.h`:

```
#define CSFFW_HEADER_SIZE_EXPECTED   968U
#define CSFFW_OPCODE_TABLE_FILE_OFF  0x0000125CU
#define CSFFW_OPCODE_TABLE_ENTRIES   129U
#define CSFFW_FUNC_LIST_PAIRS        167U
#define CSFFW_SHARED_IFACE_FILE_OFF  0x00042000U
```

and gates on `if (hdr_size != CSFFW_HEADER_SIZE_EXPECTED) return false;`.

Tested against the five payloads. Two of its constants turn out to be **right**
and I say so; the rest are wrong in ways I can show:

| prior-art constant | what it claims | what the bytes say | verdict |
|---|---|---|---|
| `hdr_size == 968` | the only valid header size | 792, 792, 824, 824, **856** | **rejects 5/5** |
| `OPCODE_TABLE_VA 0x004100BC` | opcode table VA | **correct** — maps inside section `0x00410000` on 5/5 | **right** |
| `OPCODE_TABLE_ENTRIES 129` | 129 × 4 B = 516 B | span is **516 B on 5/5** | **right** |
| `OPCODE_TABLE_FILE_OFF 0x125C` | the file offset of that VA | the VA-derived offset is `0x145C`/`0x145C`/`0x147C`/`0x14AC`/`0x152C`; `0x125C` is **unmapped** and reads ASCII | **0/5** |
| `FUNC_LIST_VA_START/END` | `0x00410de4`–`0x0041131c` | **correct**, and `(0x1131c-0x10de4)/8 = 167` exactly | **right** |
| `FUNC_LIST_PAIRS 167` | 167 pairs | **right for that VA range**, but its companion file offset is wrong | **right** |
| `SHARED_IFACE_VA 0x04000000` | shared iface VA | **correct** — real section at that VA on 5/5 | **right** |
| `SHARED_IFACE_FILE_OFF 0x42000` | the file offset of that VA | real offsets are `0x43000`/`0x47000`/`0x49000`/`0x4a000`/`0x52000`; `0x42000` maps to VA `0x0202b538`/`0x02028fc8`/`0x0202c720`/`0x0202c2f8`/`0x02028210` | **0/5** |
| vector table at file `0x001124` | `sp`, `reset_handler` | offset **unmapped** on 5/5; `sp` reads `0x000c0000`, `0x000c0000`, `0x17000000`, `0x6174735f`, `0x494c4241` | **0/5** |

**The pattern is precise and it is not "the prior art is bad".** Every *virtual
address* the prior art names is **correct**. Every *file offset* it derives from
those VAs by a fixed formula is **wrong**. It uses
`0x11A0 + (VA - 0x00410000)` for the function list, and `0x125C` for the opcode
table, and `0x42000` for the shared interface — three constants where the real
mapping is a per-build lookup. The correct file offset is
`data_start + (VA - va_start)` from the section that contains the VA, and that
is the whole correction.

The vector table is the same story with no VA given at all: the prior art
hardcodes `0x001124`, while the real vector table sits at `0x131C` (arch10.12)
through `0x13C4` (arch14.8) — 504 to 672 bytes further in, and the gap grows
with each generation. That is why `0x1124` reads ASCII: it is inside the
descriptor table's string data, not the vector table.

**The correction is: derive offsets from the section table, do not hardcode
them.** The correct vector table is the type-0 section whose `va_start == 0`,
and reading it that way works on 5/5:

| generation | `va==0` section data | initial SP | reset handler |
|---|---|---|---|
| arch10.12 | 4892–5016 | `0x02030000` | `0x00801fbd` |
| arch11.8 | 4892–5020 | `0x02033000` | `0x00801fb5` |
| arch12.8 | 4924–5052 | `0x02035000` | `0x00801f6d` |
| arch13.8 | 4932–5092 | `0x02037000` | `0x00801f55` |
| arch14.8 | 5060–5220 | `0x0203a000` | `0x00801f4d` |

Every SP is in `0x0203_xxxx` and every reset handler is in the `0x0080_xxxx`
MCU code window — internally consistent on all five, and obtained with no
hardcoded offset `[F]`.

### 4.1 GitHub code search — exact strings, access date 2026-11-28

| query | hits |
|---|---:|
| `CSF_FW_BINARY_HEADER_MAGIC 0xc3f13a6e` | **213** |
| `mali_csffw.bin parser` | **503** |
| `panthor_fw_binary_section_entry_hdr` | **211** |
| `0xc3f13a6e magic` | **489** |
| `mali_csffw format specification` | **268** |
| `mali csf firmware section parse python` | 5,904 |

Counts are a live index and drift between runs; the order of magnitude is the
finding, not the digit.

### 4.2 Web search `[N]`

SearXNG returned **0 results** on all three of these, on 2026-11-28:

- `mali_csffw.bin CSF firmware binary format header magic`
- `panthor CSF firmware section entry format documentation`
- `ARM Mali CSF firmware binary container parse`

Recorded as `[N]` — an empty result set from one engine is **not** evidence of
absence, and I am not treating it as such. The GitHub code search above is the
evidence that prior art exists.

### 4.3 Normative source

`drivers/gpu/drm/panthor/panthor_fw.c` (45,236 B, GPL-2.0, read 2026-11-28) is
the specification for the container. `Documentation/gpu/panthor.rst` (2,167 B)
documents only the DRM usage-stats interface and says nothing about the binary
format — an honest negative worth recording, since a reader might expect the
format to be documented there `[N]`.

This is GPL-2.0 source and is cited, not copied. No code from it appears in
`implementations/gpu-mali/`; the parser there is written from the *format*,
with a clean-room header naming these files as the specification.

---

## 5. The entry types, measured — and what I refuse to claim `[F]` / `[U]`

Type histogram across the five generations:

| type | arch10.12 | arch11.8 | arch12.8 | arch13.8 | arch14.8 | entry sizes |
|---|---:|---:|---:|---:|---:|---|
| 0 IFACE | 8 | 8 | 9 | 9 | 10 | 32 |
| 1 CONFIG | 2 | 2 | 2 | 2 | 2 | 24, 32 |
| 2 FUTF_TEST | **0** | **0** | **0** | **0** | **0** | — |
| 3 TRACE_BUFFER | 8 | 8 | 8 | 8 | 8 | 40, 44, 48, 52 |
| 4 TIMELINE_METADATA | 1 | 1 | 1 | 1 | 1 | 28 |
| 5 | 1 | 1 | 1 | 1 | 1 | 20 |
| 6 BUILD_INFO | 1 | 1 | 1 | 1 | 1 | 12 |
| 7 | 1 | 1 | 1 | 1 | 1 | 16 |
| 8 | 1 | 1 | 1 | 1 | 1 | 8 |
| 9 | 1 | 1 | 1 | 1 | 1 | 12 |
| **total** | 24 | 24 | 25 | 25 | 26 | |

**Type 2 (`FUTF_TEST`, the firmware unit tests) is absent from all five
upstream payloads** `[N]`. The driver has a `case` for it that returns 0; a
production build ships none. Anyone writing a parser against the enum alone
would expect it and not find it.

Entry sizes are **constant per type across all five generations** — the format
did not change shape in five architecture revisions, only the section count
grew (8 → 9 → 10 type-0 entries).

### 5.1 Type 3 is fully decoded `[F]`

`type 3` (`TRACE_BUFFER`) has 8 entries in every generation, and the body
grammar is:

```
u32 flags | u32 va[5] | u32 value | ASCII name, NUL-terminated, zero-padded to entry end
```

This parses **40/40** (8 entries × 5 generations) with no exceptions. The names
and the `flags` word are identical across all five generations:

| name | flags | `value` on arch10.12–13.8 | `value` on arch14.8 |
|---|---:|---:|---:|
| `fwutf` | `0x00000000` | 0 | 0 |
| `firmware trace` | `0x00000001` | 4 | 4 |
| `fwlog` | `0x00000001` | 17 | **18** |
| `benchmark` | `0x00000000` | 57 | **59** |
| `timeline` | `0x00000000` | 1 | 1 |
| `debug monitor in` | `0x00000001` | 2 | 2 |
| `debug monitor out` | `0x00000001` | 2 | 2 |
| `gpu_metrics` | `0x00000000` | 1 | 1 |

Six of the eight `value` fields are stable; `fwlog` and `benchmark` each gain
one on `arch14.8`, so `value` is **not** a fixed per-name constant — it is a
build-dependent count, consistent with a buffer-size or event-count field `[I]`.
That is exactly the kind of field a hardcoded table would get wrong on the
next generation, which is why it is not hardcoded here.

The five VAs in each entry are consecutive `0x0041_00xx` words — a five-word
register/descriptor block per trace buffer. The meaning of `flags` and `value`
beyond "one bit and a small count" is `[U]`; I am not inventing it.

### 5.2 Type 1 and type 4 carry ASCII too `[F]`

- `type 1` (`CONFIG`) bodies carry the strings `Log verbosity` and `WA_CFG0`,
  identical across all five generations.
- `type 4` (`TIMELINE_METADATA`) carries `timeline_header`.

### 5.3 What I refuse to claim `[U]`

Types **5, 7, 8, 9** appear exactly once each, at sizes 20, 16, 8 and 12, in
every generation. Their bodies are 1–3 u32 words. I report their sizes and
offsets and **do not** assign them semantics — they are not in the enum, the
driver's `switch` falls through to `default`, and the `OPTIONAL` bit is set on
all four, so the driver tolerates not understanding them. Guessing here would
be the exact failure mode this repository's evidence classes exist to prevent.

---

## 6. Census reconciliation — and why the corpus is not these files `[F]` / `[N]`

The corpus Mali slice is 65 rows / 13 devices / 5 basenames. Two size classes,
and the split is by SoC generation:

| size | rows | devices | SoC labels in the matrix |
|---|---:|---:|---|
| **278,528** | 25 | 5 | `Google Tensor GS201` ×25 |
| **294,912** | 40 | 8 | `Google Tensor G3` ×25, `Google Tensor G4` ×5, empty ×10 |

- **278,528 B**: `Pixel_7`, `Pixel_7_Pro`, `Pixel_7a`, `Pixel_Fold`,
  `Pixel_Tablet` — the five GS201 (Tensor G2) devices.
- **294,912 B**: `Pixel_8`, `Pixel_8A`, `Pixel_8_Pro`, `Pixel_9`, `Pixel_9A`,
  `Pixel_9_Pro`, `Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL` — eight devices.

### 6.1 The md5 structure: 65 rows, 10 distinct values `[F]`

Every device ships **all five revisions** (`r50p0` … `r54p0`), and within a
size class **all devices share the identical set of five md5s**:

| size class | devices | distinct md5-sets | all devices identical |
|---|---:|---:|---:|
| 278,528 | 5 | **1** | yes |
| 294,912 | 8 | **1** | yes |

So 5 basenames × 2 size classes = **10 distinct payloads** for 65 rows. The
`r50p0`…`r54p0` basenames are five *revisions* shipped together, not five
different firmwares — and the corpus's `md5_db` confirms it: each `(basename,
size)` pair has exactly one md5 across all 13 devices.

### 6.2 A corpus label defect `[N]`

The 294,912 B class spans **`Google Tensor G3`, `Google Tensor G4`, and empty**
SoC labels — yet all eight devices share **5 of 5** identical md5s. `Pixel_9`
is labelled `Google Tensor G4` and `Pixel_9_Pro` is labelled `Google Tensor G3`,
and they carry byte-identical firmware. At most one of those labels is right
for this file, and the file cannot distinguish them.

This is the same shape of defect as the `db_type=BOOT` mislabel in the `boot`
family and the `FW_NF_ILI7807S_*` rows in `wifi`: a per-row label that the
bytes do not support. Flagged here, **not** silently fixed, because resolving
it needs per-device build fingerprints this workspace does not hold.

### 6.3 The corpus payloads are not the upstream payloads `[N]`

| | sizes |
|---|---|
| corpus (65 rows) | **278,528**, **294,912** |
| upstream (5 generations) | 282,624, 299,008, 307,200, 311,296, 344,064 |
| overlap | **∅** |
| md5 overlap | **∅** (0 of 10 corpus md5s match any upstream md5) |

The sets are disjoint, and both are multiples of 4,096 — so this is **not**
truncation or page-padding of the same file. The corpus holds **different
builds** than any of the five upstream ones. The nearest pair is 278,528 vs
282,624, a 4,096 B difference, but both are page-aligned and the md5s differ,
so it is a different build that happens to be one page smaller `[I]`.

**This is the honest limit of the whole note.** The grammar is verified on five
real upstream payloads; the corpus connection is by **name and size class
only**, and the sizes do not even match. A corpus payload would be needed to
claim more, and none is held here (§8.2).

---

## 7. The rest of the `gpu` family, named `[F]`

The Mali slice is 21.31 % of the family's bytes. The other **716 rows /
69,276,369 B / 81 basenames / 92 devices** are Adreno and Mali-adjacent, and
`research/fleet/gpu-bdwlan.md` (248 lines) already covers the Adreno side:

| basename | rows | bytes | covered by |
|---|---:|---:|---|
| `a630_sqe.fw` | 51 | 1,649,936 | `gpu-bdwlan.md` §2.3 |
| `sequence_manifest.bin` | 50 | 192,976 | **not covered** |
| `a660_sqe.fw` | 30 | 1,238,028 | `gpu-bdwlan.md` §2.3 |
| `a615_zap.mdt` | 27 | 182,156 | `gpu-bdwlan.md` §1 |
| `a619_gmu.bin` | 24 | 786,432 | `gpu-bdwlan.md` §2.1 |
| `a660_gmu.bin` | 21 | 1,158,788 | `gpu-bdwlan.md` §2.2 |
| `fpctzapp.*` (10 files) | 112 | 34,916,316 | **not covered** |
| `egtzappf.*` (9 files) | 72 | 21,201,517 | **not covered** |
| `gmu_gen*.bin` (4 files) | 28 | 1,857,520 | **not covered** |

`fpctzapp.*` and `egtzappf.*` together are **56,117,833 B = 63.7 % of the
family's bytes**, in a 9–10 file split-MDT form (`mdt` + `b00`…`b07`) that is
the same shape as the Adreno ZAP containers already documented. They are the
largest genuinely uncovered item in this family and they are **not** what this
note specs — an honest remainder, not an omission.

---

## 8. Honest negatives `[N]`

### 8.1 What is not measured

- **No corpus payload was opened.** Every byte-level claim in §2–§5 is on five
  upstream `linux-firmware` files. The corpus connection is by name and size
  class only, and §6.3 shows the sizes do not overlap.
- **Entry types 5, 7, 8, 9 have no assigned meaning** (§5.3). Sizes and offsets
  only.
- **The type-0 `flags` field is decoded bit-for-bit against the driver, and
  every observed value is a legal combination.** The macros are `RD BIT(0)`,
  `WR BIT(1)`, `EX BIT(2)`, cache mode `GENMASK(4,3)`, `PROT BIT(5)`,
  `SHARED BIT(30)`, `ZERO BIT(31)`. Bits that are ever set across the 44
  type-0 entries: 0 (44), 1 (15), 2 (5), 3 (44), 4 (5), 5 (5), 30 (5), 31 (15)
  — and nothing outside `SUPPORTED_FLAGS`. Concretely: the code sections are
  `0x00000009` (RD, cache mode 1), `0x0000000d` (RD+EX), the two largest
  sections are `0x8000000b` (RD+WR+ZERO) and `0x80000009` (RD+ZERO) — both
  `0x02000000`/`0x01000000`, sized 174.0 KiB on arch10.12 growing to 205.9 KiB
  on arch14.8 — the BSS section is `0x0000002b` (RD+WR+PROT+cache 1), and the
  8 KiB `0x04000000` section is `0xc000001b` (RD+WR+ZERO+SHARED+cache 3) —
  exactly the `CSF_MCU_SHARED_REGION_START` section the driver requires to
  carry `SHARED`. The semantics of the *cache-mode* value are `[U]`; the bit
  positions are `[F]`.
- **The type-3 `flags` word is only partly decoded.** It is `0` or `1` across
  all 40 entries, with the `1` set on `firmware trace`, `fwlog`, `debug
  monitor in` and `debug monitor out`. What that bit means is `[U]`.
- **`version_hash` is not decoded.** The five values are `0x01050000`,
  `0x02080000`, `0x030d0000`, `0x030d0000`, `0x04060000`. The high byte runs
  1, 2, 3, 3, 4 — a monotonic counter, not the arch major (10–14) — and
  `arch12.8` and `arch13.8` share a value outright, so it is not a per-file
  identifier either. I am not asserting a packing `[U]`.
- **No signature verification was attempted.** The container carries no
  signature field in the header; integrity is structural (§3.2), not
  cryptographic. I did not test whether a modified payload is accepted.
- **The 8,316 B (arch10.12) of unclaimed file bytes are not decoded** (§3.3).
  They are header, descriptor table and page padding, but "padding" is an
  inference from position, not from content.

### 8.2 Why no corpus payload

`find` over the workspace for `mali_csffw*` returned nothing. `.gitignore`
blocks `*.bin`, so a corpus payload could not be committed even if obtained.
This is a structural limit on this issue, not an omission: the acceptance
criteria forbid committing payloads, and the byte-level work therefore runs
against upstream files fetched on the day.

### 8.3 The upstream set is five, not fourteen `[N]`

Twelve `arm/mali/arch*/mali_csffw.bin` paths were requested on 2026-11-28, then
two more (`arch10.8`, `arch10.10`) to test the byte-identity claim. **Seven of
the fourteen returned a 3,265-byte HTML error page**, not a payload:

| path | result |
|---|---|
| `arch10.5`, `arch10.6`, `arch10.7`, `arch10.9`, `arch10.11`, `arch11.0`, `arch9.0` | 404, 3,265 B HTML |

Each of those seven files begins `<!DOCTYPE` and has magic `0x4f44213c`
(`"<D O"`), which is a text file, not a firmware header. They were size- and
magic-checked before use; a fetch loop that only checked the HTTP status would
have silently "succeeded" on seven non-payloads.

The other seven resolve to **five distinct payloads** — `arch10.8`, `arch10.10`
and `arch10.12` are byte-identical (md5 `cd95e833…`, sha1 `3d6bad6f…`, `cmp`
clean), plus `arch11.8`, `arch12.8`, `arch13.8`, `arch14.8`. So the **five
distinct payloads** in §1 are exactly the distinct content, and anyone counting
fourteen generations from a path list is counting 404s and republished copies
`[F]`.

---

## 9. Method `[F]`

- Census: `csv.DictReader` over `upstream-contribution/blob-database/coverage-matrix.csv`,
  grouped on `blob_family`; every total, share and rank printed by the command
  that computed it.
- Header: `struct.unpack_from("<IBBHIII", data, 0)` — 20 B, magic `0xc3f13a6e`.
- Entries: `ehdr = u32 at off`; `type = ehdr & 0xFF`, `size = (ehdr >> 8) & 0xFF`,
  `UPDATE = bit30`, `OPTIONAL = bit31`; advance by `size` while `off < hdr_size`.
- Sections: `struct.unpack_from("<5I", data, off + 4)` = flags, va_start,
  va_end, data_start, data_end.
- Vector table: the type-0 section with `va_start == 0`; `sp = u32 at
  data_start`, `reset = u32 at data_start + 4`. **Not** a hardcoded offset.
- Integrity: `max(data_end over type-0) == len(file)`.
- Union coverage: sort distinct `(data_start, data_end)` ranges, merge, sum.
- Payloads opened read-only from scratch space; nothing committed; the only hex
  in this note is ≤16 bytes per sample plus public git SHAs and ASCII names.
- Implementation: `implementations/gpu-mali/mali_csffw_parser.py`, self-tests in
  `test_mali_csffw_parser.py`, fixtures generated deterministically by
  `make_fixture.py` because every fixture extension is gitignored, so the suite
  calls `make_fixture.write_all()` in `setUpModule`.

### 9.1 Rule-1 corrections applied in place

Two rows of `docs/REPO-STATE-MAP.md` are corrected rather than contradicted in
a new file:

1. The `gpu` blob-spec row claimed *"no bdwlan GPU parser"*. Measured:
   `blob_family=gpu` has **0** `bdwlan` rows. The phrase is replaced with the
   real open item.
2. The same row claimed *"no Mali parser"*. That was **true** at the time and
   is now false, so it is updated to cite this note and
   `implementations/gpu-mali/`.

---

## 10. Open items `[U]`

1. What are entry types 5, 7, 8, 9? Present once each in every generation, 8–20
   B, `OPTIONAL` set, absent from the enum.
2. What does `version_hash` encode? Four distinct values across five payloads,
   with `0x030d0000` shared by arch12.8 and arch13.8.
3. What are the 8,316 unclaimed file bytes in arch10.12?
4. Are the corpus's 278,528 / 294,912 B payloads the same *format* as these five
   upstream ones? Almost certainly `[H]`, but unproven without a corpus payload,
   and the md5 sets are disjoint.
5. Is the `Google Tensor G3` / `G4` SoC label on the 294,912 B class resolvable
   from bytes? All eight devices share identical firmware, so the file cannot
   distinguish them (§6.2).
6. `fpctzapp.*` and `egtzappf.*` — 56,117,833 B, 63.7 % of the family, in a
   split-MDT form that `gpu-bdwlan.md` does not cover.
7. Why does arch14.8 carry an extra empty code section at `0x00420000` with
   `va_start == va_end` (§3.1)? It reserves nothing and backs nothing, so it
   cannot be observed from the file beyond its existence.
