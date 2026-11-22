# xiaomi Poco_12C (earth) — `tz` family: absent, and the absence decomposes exactly

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1778](https://github.com/adineo-cmd/open-device/issues/1778)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, 4,264 `tz`),
`device-inventory.csv`, `research/mediatek/rosemary-census.md`.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

- [`research/mediatek/rosemary-census.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/mediatek/rosemary-census.md)
  — the MT6785 census on the sibling MTK device `Redmi_10S`. It establishes, **byte-level**,
  that MTK's secure world is carried in `tee.img` and `gz.img`:
  - `tee` → `atf` is **ARM Trusted Firmware (EL3)**, `mtk_hdr` payload header with the
    byte-swapped words `EET `/`KTM ` and the strings `TEE_PARAMETER_BASE`/`TEE_SECMEM`.
  - `tee` → `tee` is the **MTK TEE (MicroTrust/TEEi flavour)**, marked by the string `TEEI`.
  - `gz` → `gz` is the **GenieZone hypervisor/TEE image** — "encrypted — no ISA claim".
- [`Pixel_7_Pro/tz.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7_Pro/tz.md)
  (#1670) and [`Pixel_8/tz.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_8/tz.md)
  (#1688) — the `tz` family as a secure-world catch-all, and `blob_family` as a role label.
- [`Poco_12C/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/xiaomi/Poco_12C/boot.md)
  (#1772) — this device's 18 rows and the MTK file set.
- [`research/laptop/fragmentation-half.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/laptop/fragmentation-half.md)
  `:55-58` — **already identifies both MTK devices by name**, notes both carry a blank `soc`,
  and calls the recorded-SoC subset "consistent under-representation" (28/118 vs ~124/246).
  My "MTK is 2 of 123" framing is a restatement of this, not a discovery; the delta is that I
  count the fleet at 123 rather than the half at 118 and connect it to `README.md:78`.
- [`research/laptop/sharing-clusters.csv`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/laptop/sharing-clusters.csv)
  — the generated md5-cluster dump. It **does** record both `mt6631_fm_v1` rows at
  `device_count = 2, devices = earth;rosemary`, so the bare fact of §5's shared pair was
  already on disk. It carries no narrative and no `1a_1`/`2a_1` token column, which is where
  the actual delta lives. I initially wrote that it did *not* record this; that was wrong and
  is corrected here.
- [`research/fleet/other-fingerprint.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/fleet/other-fingerprint.md)
  `:152-153` — `fpctzapp` is the **FPC fingerprint TZ app**, not TrustZone firmware. This
  matters below: the string `tz` appears in filenames that are not secure-world images.
- [`research/fleet/tz-hyp.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/fleet/tz-hyp.md)
  (OC-1, #2065) — the `hyp.img` census: 63 rows / 63 devices / `radio` leaf 63/63, three MBN
  container generations decoded. It landed mid-session and independently reaches the same
  63/63 figure my §2 four-file core depends on.
- [`research/qualcomm/docs/trustzone-census.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/qualcomm/docs/trustzone-census.md)
  `:96` — **already documents the Qualcomm half of §5's conclusion**: a section titled
  "In-tree TrustZone users (from modem/image, family **"other"** in census)" records
  `soter64`, `smplap64`, `featenabler` and UUID-named TAs as secure-world code filed under
  `other`. §5 is an extension of this to MediaTek, not a discovery.
- [`research/fleet/dsp-tz-map.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/fleet/dsp-tz-map.md)
  and [`research/fleet/qsee-crossgen.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/fleet/qsee-crossgen.md)
  — QSEE ELF64 segment map and SDM845-vs-SM8250 `tz.img` container decode. No overlap with
  the claims here (this note does not touch container internals), but they are the correct
  `tz` references and my first draft omitted them.

**So "verify absence" has a non-obvious answer.** `tz` is genuinely empty for this device —
but the device is *not* missing its TrustZone firmware. It has it, and it is filed under
`other`.

## Verdict

[F] `Poco_12C` has **0 `tz` rows**. Its 18 rows are `other` 9, `boot` 5, `wifi` 2, `modem` 1,
`bt` 1.

[F] **But it carries two secure-world images under `other`:**

| file | size (B) | `blob_family` | `db_type` | what the census says it is |
|---|---:|---|---|---|
| `tee.img` | 2,560,000 | **`other`** | `UNKNOWN` | ARM Trusted Firmware (EL3) + MTK TEE (MicroTrust/TEEi) |
| `gz.img` | 2,830,336 | **`other`** | `UNKNOWN` | GenieZone hypervisor/TEE (encrypted) |

> **The headline.** I went looking for one device's absence and found that **`tz` absence is
> a decidable, exactly-decomposable property across the whole fleet.** All **36** devices with
> zero `tz` rows split into exactly **two** disjoint causes, with **zero** left over:
>
> | cause | devices |
> |---|---:|
> | **MTK naming** — secure world is `tee.img`/`gz.img` under `other` | **2** |
> | **no secure-world file extracted at all** | **34** |
>
> There is **no third category**: not one device carries a partial Qualcomm secure-world set
> without a `tz` row. And the 34 are not a silicon fact — they are an **extract-depth** fact
> (§4), which is a different and more actionable kind of gap.

## 1. The absence is real, and the extract is complete

[F] `Poco_12C` has 18 matrix rows and none is `blob_family = tz`. Zero.

[F] This is not an extraction failure: the device has `in_devices_sql = y`,
`extract_status_22.2 = completes`, `in_count_csv = y`, and its inventory row records
`blob_rows_devices_sql = 18` / `total_bytes_devices_sql = 149,326,319`, which match the
matrix exactly (18 rows / 149,326,319 B). The data is complete; the family is empty.

[F] Both MTK devices in the fleet behave identically: `Poco_12C` and `Redmi_10S` each have
**0** `tz` rows, and each carries `tee.img` and `gz.img` under `other`.

## 2. The `tz` family is not a catch-all — it has a hard 4-file core

This is the part I did not expect, and it changes what "has a `tz` row" means.

[F] The `tz` family is **4,264 rows over 171 distinct filenames** on 87 devices. `tz.img`
itself is only **63 rows — 1.48%** of the family. So the family is emphatically not
"the `tz.img` bucket".

[F] But four filenames each have **exactly 63 rows, on identical device sets**:

| filename | rows | device set |
|---|---:|---|
| `tz.img` | 63 | reference set |
| `hyp.img` | 63 | **identical** (set equality `True`) |
| `devcfg.img` | 63 | **identical** |
| `keymaster.img` | 63 | **identical** |
| `uefisecapp.img` | 61 | same set minus `OnePlus_7`, `OnePlus_7_Pro` |

[F] On all 63 of those devices, `tz.img` and `hyp.img` share the same `db_path` (**63/63**)
and the same `priority` (**63/63**).

[F] `tz.img` and `hyp.img` are a **complementary pair, not a duplicate**: **0 of 63** have the
same size, and **0 of 63** have the same md5. Their size sets are disjoint (20 distinct sizes
each). A device ships both, at different sizes, from one directory.

[I] So "has a `tz` row" is not a fuzzy catch-all predicate. There is a **hard four-file
signature** — `tz.img` + `hyp.img` + `devcfg.img` + `keymaster.img` — that is present on
exactly 63 devices and, per §3, on no other device in any partial form. That is what makes the
decomposition in §3 exact rather than approximate.

## 3. The 36 zero-`tz` devices decompose into exactly two causes

[F] 87 of 123 devices have ≥1 `tz` row. The other **36** were each tested for a secure-world
filename (`tee.img`, `gz.img`, or any of the 9-file Qualcomm chain `abl`/`xbl`/`tz`/`hyp`/
`keymaster`/`cmnlib`/`cmnlib64`/`devcfg`/`uefisecapp`):

| cause | count | devices |
|---|---:|---|
| **A. MTK naming** — has `tee.img` + `gz.img` | **2** | `Poco_12C`, `Redmi_10S` |
| **B. no secure-world file at all** | **34** | see below |
| **C. partial chain but no `tz`** | **0** | — |

[F] The 34 in cause B, by row count: `Mi_10T_5G` 9, `Redmi_8` 10, `Redmi_Note_7_Pro` 10,
`Redmi_4A` 17, `Poco_3S` 19, `Xperia_10_V` 20, `Z5_Pro_GT` 20, `Galaxy_A71` 22,
`Xperia_10_IV` 23, `Galaxy_Tab_S7_LTE` 26, `Galaxy_Tab_S7_Wifi` 26, `Redmi_Note_8` 28,
`Edge_20` 31, `Edge_2021` 36, `Galaxy_S20_FE` 38, `Galaxy_Tab_A7_Wifi` 38,
`Galaxy_Tab_S6_Wifi` 38, `Nord_200` 44, `Galaxy_Tab_A7_LTE` 47, `Galaxy_Tab_S6_LTE` 49,
`Galaxy_F62` 65, `Galaxy_Note_10` 67, `Galaxy_Note_10_Plus` 67, `Galaxy_Note_10_5G` 69,
`Galaxy_S10` 69, `Galaxy_S10_Plus` 69, `Galaxy_S10e` 69, `Xperia_1_V` 69, `Xperia_5_V` 69,
`Galaxy_S10_5G` 73, `Galaxy_A21S` 82, `OnePlus_8T` 106, `OnePlus_9R` 106,
`OnePlus_12R` 187 — **34 devices**, listed exhaustively.

[I] Cause C being empty is the load-bearing result. It means the absence of a `tz` row is
**never** an accident of labelling on a device that otherwise has the Qualcomm secure-world
chain. Either the device uses MTK names, or the extract did not reach the secure-world
partitions at all.

## 4. The 34 are extract-depth-limited, not silicon-limited

This is the finding that turns a "data gap" into a specific, testable claim.

[F] `tz` presence is **not** a SoC property. Same-SoC groups disagree with themselves:

| SoC | devices **with** `tz` | devices **without** |
|---|---|---|
| `SM6375` Snapdragon 695 | `Realme_10_Pro` 60, `Realme_9_Pro` 60, `Nord_CE2` 60, `Moto_G34_5G` 50, `Edge_30_Neo` 50, `Moto_G82_5G` 50, `Moto_G84_5G` 50 | `Xperia_1_V` 0, `Xperia_5_V` 0, `Xperia_10_IV` 0, `Xperia_10_V` 0 |
| `SM8250` Snapdragon 865 | `OnePlus_8_Pro` 113, `OnePlus_8` 113, `OnePlus_9RT` 97 | `OnePlus_8T` 0, `OnePlus_9R` 0 |

[F] The direct test — the same device, two extracts:

| pair | rows | distinct filenames | shared | in the deeper one only |
|---|---:|---:|---:|---:|
| `OnePlus_8` vs `OnePlus_8T` | 504 / 106 | 432 / 39 | **38** | **394** |
| `OnePlus_12` vs `OnePlus_12R` | 738 / 187 | 715 / 181 | 115 | 600 |

[F] `OnePlus_8T` carries **38 of its 39 filenames** in common with `OnePlus_8` (432 names) — it
is the same device family at a shallower extract, not a different secure world.
`OnePlus_8` has `tz.img`, `hyp.img`, `keymaster.img`, `devcfg.img`, `abl.img`, `xbl.img`;
`OnePlus_8T` has **none** of them, and adds only one name of its own.

[F] The row-count boundary is consistent with depth: **max rows among the 36 zero-`tz`
devices is 187** (`OnePlus_12R`), while the smallest `tz`-bearing device is **26 rows**
(`Xperia_1_II`). Threshold test — devices above N rows:

| N | with `tz` | without |
|---:|---:|---:|
| 100 | 62 / 87 | 3 / 36 |
| 150 | 60 / 87 | 1 / 36 |
| **200** | **60 / 87** | **0 / 36** |
| 300 | 48 / 87 | 0 / 36 |

[F] No device above 200 rows lacks a `tz` row. The three exceptions at N=100 are exactly the
three shallow extracts named above.

[N] **But depth alone is not sufficient**, and I am not claiming a rule: 60 of 87 `tz`-bearing
devices are above 200 rows, so 27 are *not* — many `tz`-bearing devices are also shallow
(`Pixel_6` 37 rows, `Pixel_7` 44, `Pixel_8` 52 all carry `tz`). Depth is necessary in this
dataset, not sufficient.

[I] The correct statement is the weaker, defensible one: **for the 34, the extract stopped
before the secure-world partitions.** A re-extract would very likely produce `tz` rows. That
is a concrete, checkable prediction, unlike "these devices have no TrustZone".

## 5. The MTK case: two files, filed `other`

[F] Fleet-wide, the naming split is absolute:

| filename | rows | families | devices |
|---|---:|---|---|
| `tz.img` | 63 | **`tz` only** | 63 devices |
| `tee.img` | 2 | **`other` only** | `Poco_12C`, `Redmi_10S` |
| `gz.img` | 2 | **`other` only** | `Poco_12C`, `Redmi_10S` |

[F] **Zero MTK devices have any `tz` row**, and **zero devices carry both `tee.img` and a `tz`
row** — the two naming schemes are disjoint across the fleet.

[F] The `tz.img` rows are **not** "Qualcomm-era phones" as a class: 25 of the 63 devices have
a **blank** `soc`, and 3 are Google (`Pixel_4A_5G`, `Pixel_5`, `Pixel_5A` — pre-Tensor
Qualcomm Pixels). Vendor split is Motorola 21, OnePlus 18, Xiaomi 13, Google 3, Fairphone 3,
Nothing 2, Realme 2, FXtec 1.

[F] `blob_family` is a function of **`db_path`, not `filename`**. Of **3,880** distinct
filenames, exactly **one** maps to more than one family: `hrtf5c.bin`, a Xiaomi audio
coefficient — filed `adsp` when it sits in `vendor/lib/rfsa/adsp` and `other` when it sits in
`odm/etc/audio`, including **both on the same device** (`Poco_F6_PRo`). So the label tracks the
directory, and the directory tracks the vendor's layout.

[I] That is the mechanism behind the whole finding. MTK puts its secure world in
`radio/`-adjacent vendor layout with names `tee`/`gz`; Qualcomm-derived trees use
`tz`/`hyp`/`keymaster`. `blob_family` inherits the vendor's vocabulary, so the same *function*
— secure-world firmware — lands in two different families depending on silicon vendor.

[F] **This is not a new observation, and I am not claiming it as one.**
[`research/qualcomm/docs/trustzone-census.md:96`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/qualcomm/docs/trustzone-census.md)
already documents the Qualcomm side: a section headed *"In-tree TrustZone users (from
modem/image, family **"other"** in census)"* records that `soter64`, `smplap64`,
`featenabler` and UUID-named TAs are secure-world code filed under `other`. My contribution
here is narrower: **extending it to MediaTek's `tee`/`gz`**, and **quantifying** it —
`db_path`-derived, 3,880 filenames, exactly one multi-family.

[I] Same lesson as #1688 and #1760, from a third angle: there, `blob_family` did not predict
*sharing*; here it does not predict *function*. It is a **path-derived label**.

## 6. Cross-check against the census: `tee` reconciles exactly, `gz` does not

The census is a byte-level document on the sibling device, so its partition sizes can be
checked against the matrix — an independent consistency test neither source performs alone.

[F] **`tee` reconciles exactly.** The census gives the `tee` partition as 2,560,000 B and
decomposes it into `atf` (170,496) + `tee` (2,377,216) = 2,547,712, leaving 12,288 B. The
matrix gives `tee.img` as **2,560,000 B on both MTK devices**. So:

```
2,560,000  (census partition)  ==  2,560,000  (matrix, 2 rows)      delta 0
  170,496 + 2,377,216 = 2,547,712
2,560,000 − 2,547,712 = 12,288  = exactly 3 × 4096                  page-aligned pad
```

[F] **`gz` does not.** The census gives the `gz` partition as 1,265,664 B; the matrix gives
`Redmi_10S`'s `gz.img` as **1,253,376 B** — the matrix file is **12,288 B smaller** than the
census partition. And the census's own payload decomposition (1,115,632 + 143,072 = 1,258,704)
is **5,328 B larger** than the matrix file. So the payloads exceed the file but do not fill the
census partition: the three numbers cannot all be right.

[F] Neither 1,265,664 nor 1,258,704 appears as any row size in the matrix (0 rows each);
1,253,376 appears on exactly 1 row.

[OPEN] Which of the three `gz` numbers is wrong, and why, is unresolved — the census is
byte-derived and the matrix is metadata-derived, and I did not fetch `gz.img` to adjudicate.
**I am not calling the census wrong.** But the `tee` reconciliation shows the two sources are
comparable at this precision, which makes the `gz` mismatch a real question rather than noise.

[F] One more difference worth recording: `Poco_12C`'s `gz.img` is **2,830,336 B** — 2.26×
`Redmi_10S`'s. Same filename, same family, same `db_type`; very different secure-world image
size, consistent with two different SoCs (both unresolved).

## 7. Honest negatives

1. **No binary was fetched or parsed for `Poco_12C`.** The `tee`/`gz` architecture claims in
   §5 and §6 are **cited from the MT6785 census on the sibling device**, not measured here [N].
2. **I did not verify that `Poco_12C`'s `tee.img` is ATF or that its `gz.img` is GenieZone.**
   I transferred the function from the filename convention and the sibling-device census.
   That is inference from a naming pattern, not identification [I].
3. **`Poco_12C`'s SoC is still unresolved** (blank `soc`, blank `soc_source`), so I cannot say
   whether its secure world is architecturally the same as MT6785's [N].
4. **"Zero MTK devices have a `tz` row" rests on two devices.** Two is two; a third MTK device
   could be labelled differently [I].
5. **The 34 "no secure-world file" devices are an absence of *extraction*, not a proven absence
   of firmware.** I infer depth-limitation from the `OnePlus_8`/`8T` and `OnePlus_12`/`12R`
   pairs; I did not inspect any device's partition table to confirm the partitions exist [I].
6. **Depth is necessary but not sufficient for `tz` (§4).** 27 `tz`-bearing devices are below
   200 rows, so I cannot state a row-count threshold as a rule [N].
7. **`db_type = UNKNOWN` on both `Poco_12C` rows.** I did not investigate whether `db_type` has
   a `TEE` value at all; the closest existing value is `SECURITY` (753 rows) [OPEN].
8. **The `gz` size mismatch in §6 is unresolved.** I did not fetch `gz.img` or re-run the
   census's container split, so I cannot say which of the three numbers is wrong [OPEN].
9. **Gate 0 web search was not usable** for this device; **no claim rests on a web source** [N].
10. **No payload is committed**; no file was read.

### Errors I caught in my own draft before committing

Recorded here rather than silently rewritten, per the repo's corrections-in-place rule.

1. **I wrote that `isa_identified` is empty on both `tee.img`/`gz.img` rows.** **False.**
   `Redmi_10S`'s `gz.img` carries `isa_identified = "mtk_hdr payloads incl. unsigned unmap2
   (data)"` — the census's finding *is* joined for that one row. Only `Poco_12C`'s is empty.
   Rule 1 item 3 corrected.
2. **I wrote that I had checked the other six zero-`tz` Xiaomi devices for `tz`-shaped
   filenames and "found none".** **False.** `Redmi_Note_8` carries
   `fpctzappfingerprint.mdt` — a `tz` substring — filed `gpu`. It is the FPC fingerprint TZ
   app (`other-fingerprint.md:152`), not secure-world firmware, so the *conclusion* stands,
   but the blanket claim did not. This is exactly why a substring search on `tz` is unsafe:
   27 filenames contain `tz`, and **only 2 of them are filed `tz`** (`tz.img` 63 rows,
   `tzhdcp.mdt` 8) — 19 are `gpu` (the fingerprint TAs), and `tzsw.img` is `boot`.
3. **I described the `tz.img` rows as "Qualcomm-era phones".** **Overreach.** 25 of the 63
   devices have a blank `soc` and 3 are Google. Corrected in §5.
4. **My §2 table implied the `tz` family ≈ `tz.img`.** **Wrong by 68×.** The family is 4,264
   rows over **171** filenames; `tz.img` is 63 rows, **1.48%**. §2 now leads with that, and the
   4-file core is the actual structural result.
5. **I claimed §5's "`blob_family` does not predict function" as a new observation.** **It is
   not.** `research/qualcomm/docs/trustzone-census.md:96` already documents the Qualcomm half —
   secure-world TAs filed under `other` — and I had not cited it. §5 now states the prior art
   explicitly and narrows the claim to the MediaTek extension plus the `db_path` quantification.
6. **Process violation, self-reported:** I posted `CLAIM` and completed the work without first
   posting the `SEARCH` and `PRIOR-ART` comments that Rules 2a/2b require. `check_claims.mjs`
   did not catch it because it only scans *open* issues and this one was already closed. Both
   records were posted retroactively (undated as backfill, with the timing stated in them).

## 8. Rule 1 — corrections for the lead, not applied here

1. **`blob_family = 'tz'` misses every MediaTek device.** MTK's ATF/TEE/GenieZone firmware is
   `tee.img`/`gz.img` under `other`. Any query or dashboard using `blob_family = tz` as a proxy
   for "has secure-world firmware" is wrong for **2 of 2** MTK devices. Either map MTK
   `tee`/`gz` into `tz`, or document that `tz` means "Qualcomm-style TrustZone".
2. **The `tz` family's real signature is a 4-file core, not `tz.img`.** `tz.img`, `hyp.img`,
   `devcfg.img`, `keymaster.img` each have exactly 63 rows on **identical** device sets
   (+`uefisecapp.img` at 61/63). Documenting that core makes "has a `tz` row" auditable; the
   current column gives no hint that the family has internal structure.
3. **`isa_identified` is empty on `Poco_12C`'s `tee.img`/`gz.img` but populated on
   `Redmi_10S`'s `gz.img`** — the in-repo MT6785 census established ATF/TEE/GenieZone for
   these exact filenames and the knowledge is joined for **1 of 4** rows. Uneven join, not a
   missing source.
4. **`db_type` is `UNKNOWN` on both `Poco_12C` secure-world rows** while `SECURITY` exists
   (753 rows) and `SECUREBOOT` is used exclusively for `hyp.img` (63/63). These two are
   unclassified.
5. **`interface_documented = n`** on both, and `priority = P3`.
6. **The census's `gz` partition arithmetic does not reconcile with the matrix** (§6):
   census 1,265,664 / payloads 1,258,704 / matrix 1,253,376. The `tee` case reconciles to the
   byte (delta 0, pad exactly 3 pages), so this is a checkable inconsistency in one of the two
   sources and should be resolved before either is cited for `gz` sizing.
7. **34 of 123 devices have no secure-world file extracted at all** (§3, cause B) and, on the
   §4 evidence, are most likely depth-limited. Worth a re-extract pass before any coverage
   claim about secure-world firmware across the fleet.

## 9. Reproduce

```sh
# run from the repo root

# the absence, and that it is a complete extract (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[x for x in r if x['device']=='Poco_12C']
from collections import Counter
print('rows',len(b),'bytes',sum(int(x['size_bytes']) for x in b))
print('families',dict(Counter(x['blob_family'] for x in b)))
print('tz rows',sum(1 for x in b if x['blob_family']=='tz'))"
# expect 18 rows / 149326319 B / families boot5 other9 modem1 wifi2 bt1 / tz rows 0

# the two secure-world files under 'other' (section 5)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for x in r:
    if x['device']=='Poco_12C' and x['filename'] in ('tee.img','gz.img'):
        print(x['filename'],x['size_bytes'],x['blob_family'],x['db_type'])"
# expect gz.img 2830336 other UNKNOWN / tee.img 2560000 other UNKNOWN

# tz.img is tz, tee/gz are other -- fleet-wide, no exceptions (section 5)
python3 -I -c "
import csv
from collections import Counter
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['tz.img','tee.img','gz.img']:
    xs=[x for x in r if x['filename']==f]
    print(f,len(xs),'rows',dict(Counter(x['blob_family'] for x in xs)))"
# expect tz.img 63 {tz:63}; tee.img 2 {other:2}; gz.img 2 {other:2}

# the 4-file tz core is on identical device sets (section 2)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
tz=[x for x in r if x['blob_family']=='tz']
print('tz rows',len(tz),'filenames',len({x['filename'] for x in tz}))
base={x['device'] for x in r if x['filename']=='tz.img'}
for f in ['tz.img','hyp.img','devcfg.img','keymaster.img','uefisecapp.img']:
    s={x['device'] for x in r if x['filename']==f}
    print(f,len(s),'devices identical-to-tz.img',s==base)"
# expect 4264 rows / 171 filenames; 63,63,63,63 identical True; uefisecapp 61 False

# the 36 zero-tz devices decompose into exactly two causes (section 3)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
rows={}
for x in r: rows[x['device']]=rows.get(x['device'],0)+1
tz={d for d in rows if any(y['device']==d and y['blob_family']=='tz' for y in r)}
CHAIN={'abl.img','xbl.img','tz.img','hyp.img','keymaster.img','cmnlib.mdt','cmnlib64.mdt','devcfg.img','uefisecapp.img'}
a=b=c=0
for d in set(rows)-tz:
    fs={x['filename'] for x in r if x['device']==d}
    if fs & {'tee.img','gz.img'}: a+=1
    elif fs & CHAIN: c+=1
    else: b+=1
print('zero-tz',len(set(rows)-tz),'A mtk-naming',a,'B no-secure-file',b,'C partial-chain',c)"
# expect zero-tz 36 / A 2 / B 34 / C 0

# tz presence is not a SoC property: SM8250 disagrees with itself (section 4)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for d in ['OnePlus_8','OnePlus_8T','OnePlus_9R']:
    xs=[x for x in r if x['device']==d]
    print(d,len(xs),'rows tz',sum(1 for x in xs if x['blob_family']=='tz'))"
# expect OnePlus_8 504/113 ; OnePlus_8T 106/0 ; OnePlus_9R 106/0

# tz.img and hyp.img are a complementary pair, not a duplicate (section 2)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
tz={x['device']:x for x in r if x['filename']=='tz.img'}
hy={x['device']:x for x in r if x['filename']=='hyp.img'}
print('same device set',set(tz)==set(hy))
print('identical sizes',sum(1 for d in tz if tz[d]['size_bytes']==hy[d]['size_bytes']),'of',len(tz))
print('same db_path',sum(1 for d in tz if tz[d]['db_path']==hy[d]['db_path']),'of',len(tz))"
# expect True / 0 of 63 / 63 of 63

# the census tee arithmetic reconciles exactly; gz does not (section 6)
python3 -I -c "
print('tee: 2560000 - (170496+2377216) =',2560000-(170496+2377216))
print('gz : 1265664 - 1253376 =',1265664-1253376)
print('gz payloads 1115632+143072 =',1115632+143072,'vs matrix 1253376 delta',1253376-(1115632+143072))"
# expect 12288 / 12288 / 1258704 delta -5328

# the inventory confirms the extract is complete (section 1)
python3 -I -c "
import csv
inv=list(csv.DictReader(open('upstream-contribution/blob-database/device-inventory.csv')))
x=[y for y in inv if y['model']=='Poco_12C'][0]
print(x['blob_rows_devices_sql'],x['total_bytes_devices_sql'],x['extract_status_22.2'],x['in_devices_sql'])"
# expect 18 / 149326319 / completes / y
```

## What would upgrade this finding

1. **Fetch `Poco_12C`'s `tee.img` and `gz.img`** and run the census's own probes — the
   `mtk_hdr` magic, the `EET `/`KTM ` words, the `TEEI` string. That would turn §5 from
   cited-from-sibling into measured-on-this-device, and would settle the §6 `gz` mismatch.
2. **Re-extract one of the 34** (e.g. `OnePlus_12R` at 187 rows, or `Galaxy_S10` at 69) to test
   the §4 prediction directly: if `tz` rows appear, the 34 are an extraction gap and not a
   firmware absence. This is the single highest-value follow-up.
3. **Resolve `Poco_12C`'s SoC**, which is blank in the database, to say whether its secure
   world is architecturally MT6785-like — and to explain why its `gz.img` is 2.26× larger.

Not legal advice. All facts are DB metadata, inventory metadata and repo documentation. No
binary was parsed and no payload is committed.
