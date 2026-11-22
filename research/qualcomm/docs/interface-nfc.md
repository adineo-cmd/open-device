# NFC driver ↔ blob interface (Fairphone FP6) — for upstream issue #17

One-page interface note, built **from public data only** (issue bodies,
mainline kernel sources, public kernel trees). Written 2026-11-16 for
[upstream issue #17](https://codeberg.org/rsavoye/librephone/issues/17)
("Document the interface between the NFC driver and the blob", in an
API-doc style so it can later become a test suite).

**Legend:** [PUBLIC] = public-kernel/standard fact with source; [LAB] =
lab-derived fact with committed doc; [OPEN] = not establishable from
data available here.

## 1. What the "blob" is on this device

- [PUBLIC] The FP6 public kernel tree
  (`github.com/LineageOS/android_kernel_fairphone_SM7635`, accessed
  2026-11-16) carries only the standard mainline `drivers/nfc/` set
  (`nxp-nci`, `pn533`, `st-nci`, `st21nfca`, `s3fwrn5`, ...), and the
  vendor module tree
  (`android_kernel_fairphone_sm7635-modules`, `qcom/opensource/`,
  accessed 2026-11-16) has **no** NFC module directory — the NFC stack
  is in-kernel driver + Android userspace HAL (`libnfc-nci`).
- [LAB] The lab's committed FP6 census (modem/vendor/dsp trees, 665
  files) **does** contain an NFC firmware image file:
  `vendor-firmware/sec_s3nrn4v_firmware.bin`, 184,620 B, sha256
  `407a4d07e712397d…` (`qualcomm-fp6/results/census.md` line 697,
  2026-11-15). *(Corrected 2026-11-22, issue #2060: this bullet
  previously read "contains **no NFC firmware image file**" and
  inferred the firmware was OTP-only. That was false against the
  census row it cited. See `research/fleet/other-nfc.md` §8 for the
  decode of the file and the hash reconciliation.)* The image is an
  `s3fwrn5`-format container: 44-byte header + two 128-byte signature
  blobs + the image in 4096-byte sectors
  (`44 + 128 + 128 + 45×4096 = 184,620` exactly). The LWN series
  *"nfc: s3fwrn5: support the S3NRN4V variant"* records that this
  chip **also** ships with working firmware and that mainline skips
  the download step on it, so the file is an update/recovery artifact
  rather than a must-load-at-boot blob.
- [LAB] The NFC controller on FP6 is a **Samsung S3NRN4V**, not an NXP
  part. *(Corrected 2026-11-22, issue #2060: this bullet was `[OPEN]`,
  reading "the exact NFC controller part on FP6 (NXP SN100 family vs
  other) is not stated in any data available to this box". The
  filename `sec_s3nrn4v_firmware.bin` states it, Samsung's part page
  lists `S3NRN4V (192K)`, and the LWN series names the Fairphone 6
  (SM7635) as a board using it.)* Consequence: the `nxp-nci` protocol
  table in §2 below is **accurate but describes a different vendor's
  part**. The matching driver family for this device is
  `drivers/nfc/s3fwrn5/`, whose command set and container are
  documented in `research/fleet/other-nfc.md` §3 and §5.3.

## 2. The driver ↔ controller interface, layer by layer

`[LAB]` **Scope note (added 2026-11-22, issue #2060).** The table below documents
the **NXP `nxp-nci`** path, which is *not* the part on this device (§1). It is
retained because the transport/framing/runtime layers are generic NCI and hold
for the Samsung part too; only the `boot mode` and `firmware download` rows are
NXP-specific. For the actual FP6 controller (`s3fwrn5` family) the download
protocol is `0x00 RESET`, `0x01 GET_BOOTINFO`, `0x02 ENTER_UPDATE_MODE`
(with `SHA1(image)` + signature), `0x04 UPDATE_SECTOR` (one whole sector per
command), `0x05 COMPLETE_UPDATE_MODE`, 1000 ms per-message timeout — see
`research/fleet/other-nfc.md` §5.3.

All anchorable in mainline (`torvalds/linux`, accessed 2026-11-16):

| layer | what crosses it | mainline anchor |
|---|---|---|
| transport | I2C/SPI byte stream to the NFC controller | `drivers/nfc/nxp-nci/i2c.c` (phy `set_mode` cold/NCI) |
| framing | **NCI** packets: 3-byte control header (MT/PBF/GID-OID) + payload; NXP variant uses a 4-byte header (`NXP_NCI_HDR_LEN = 4`) | `include/net/nfc/nci.h`, `net/nfc/nci/` core; `drivers/nfc/nxp-nci/core.c` |
| boot mode | controller cold start → FW-download mode → NCI mode (`NXP_NCI_MODE_COLD` → `NXP_NCI_MODE_NCI`) | `drivers/nfc/nxp-nci/core.c` (`nxp_nci_reset`, mode switching) |
| firmware download | the driver↔blob protocol itself — command set `0xF0 RESET`, `0xF1 GETVERSION`, `0xE0 CHECKINTEGRITY`, `0xC0 WRITE` (chunked, `NXP_NCI_FW_CHUNK_FLAG 0x0400`), `0xA2 READ`, `0xF2 GETSESSIONSTATE`, `0xA7 LOG`, `0xD0 FORCE`, `0xF4 GET_DIE_ID`; result codes (`NXP_NCI_FW_RESULT_OK = 0x00` ...); 30 s answer timeout | `drivers/nfc/nxp-nci/firmware.c` |
| runtime ops | NCI core: CORE_RESET/CORE_INIT/CORE_SET_CONFIG, RF discovery, NFCEE management — NFC Forum NCI specification (public standard) | `net/nfc/nci/`, NFC Forum NCI spec |
| userspace | generic NFC netlink/family API to the HAL | `include/uapi/linux/nfc.h`, `net/nfc/netlink.c` |

## 3. What a free re-implementation must provide (test-suite hooks)

1. Bring-up: probe → cold/NCI mode switch → `0xF1 GETVERSION` answer
   parse → NCI `CORE_RESET`/`CORE_INIT` round trip.
2. Firmware path: `0xF0` → `0xC0` WRITE chunk loop with integrity
   check → session-state query; must tolerate the 30 s timeout window.
   *(NXP path. For the FP6's actual `s3fwrn5` part the equivalent is
   `0x02 ENTER_UPDATE_MODE` → `0x04 UPDATE_SECTOR` loop →
   `0x05 COMPLETE_UPDATE_MODE`, one 4096-byte sector per command — and
   per the LWN series the download is skipped entirely on this chip
   because it reports a hardware version mainline has no base address
   for. Corrected 2026-11-22, issue #2060.)*
3. Data plane: NCI data-connection open, RF interface activation,
   ISO-DEP exchange — assertable with a virtual NCI device
   (`drivers/nfc/virtual_ncidev.c` exists in mainline for exactly this
   kind of testing).
4. Config surface: `WCNSS_qcom_cfg.ini`-style runtime knobs do not
   apply to NFC (that is WLAN); NFC config is NCI SET_CONFIG + HAL
   params. [OPEN] FP6-specific HAL parameters not extractable here.

## Sources consulted (accessed 2026-11-16; network flaky, all fetched OK)

- https://raw.githubusercontent.com/torvalds/linux/master/drivers/nfc/nxp-nci/core.c and `firmware.c` (fetched; command IDs quoted above)
- https://api.github.com/repos/torvalds/linux/contents/drivers/nfc (directory listing)
- https://api.github.com/repos/LineageOS/android_kernel_fairphone_sm7635-modules/contents/qcom/opensource (no NFC module)
- https://api.github.com/repos/LineageOS/android_kernel_fairphone_SM7635/contents/drivers/nfc (mainline-equivalent set present)
- Lab: `qualcomm-fp6/results/census.md` — ~~no NFC firmware file in the
  censused trees~~ **contains `vendor-firmware/sec_s3nrn4v_firmware.bin`,
  184,620 B, sha256 `407a4d07e712397d…`** (line 697; corrected 2026-11-22,
  issue #2060)
- Added 2026-11-22 (issue #2060): `torvalds/linux` `drivers/nfc/s3fwrn5/`
  `{firmware.c,firmware.h,core.c,nci.c}`; `lwn.net/Articles/1087764/`
  (`[PATCH v4 0/6] nfc: s3fwrn5: support the S3NRN4V variant`);
  `semiconductor.samsung.com/…/s3nrn4v/`; `research/fleet/other-nfc.md`

**Clean-room statement:** everything above is public-kernel/standard
material plus lab census facts; no proprietary content, no decompiled
code. The FP6 controller identity is **Samsung S3NRN4V** (§1, corrected
2026-11-22) and its firmware file is `sec_s3nrn4v_firmware.bin` in
`vendor/firmware`; no other FP6-specific firmware path is claimed.
