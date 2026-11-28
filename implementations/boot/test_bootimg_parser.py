#!/usr/bin/env python3
"""test_bootimg_parser.py — unittest suite for the clean-room boot-family parser.

CLEAN-ROOM STATEMENT
Written from the public AOSP specifications named in bootimg_parser.py
(bootimg.h, avbtool.py, mkdtimg), all fetched 2026-11-26; no proprietary
material was read. Every fixture is self-made by make_fixture.py from those
documented field layouts. No device payload is committed.

Two fixture classes are exercised:

  * synthetic fixtures from make_fixture.py, which cover every grammar and
    every error path deterministically, and
  * an optional real payload directory pointed at by the BOOT_FIXTURE_REAL
    environment variable. When set, the same parser is run against real
    boot/dtbo payloads held in scratch space, so the laws are checked on
    vendor bytes as well as on constructed ones. The suite skips those
    checks when the variable is absent, so the suite always passes in a
    clean checkout with no device files present.

Covers: format detection for all five grammars plus the unrecognised case,
the v0/v1/v2 and v3/v4 page arithmetic including the computed-end and
trailing-byte accounting, the DER-tail classification, the vendor_boot v3
and v4 layouts with the ramdisk table, the dt_table field order (the one
place a naive big-endian read silently swaps entry_size and entry_count),
the FDT magic at every dtb_offset, both AVB verification laws, the ELF
multi-header walk, and the truncation and garbage error paths.
"""

import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bootimg_parser as parser
import make_fixture

FIX = os.path.join(HERE, "fixtures")
REAL = os.environ.get("BOOT_FIXTURE_REAL")


def setUpModule():
    """Regenerate fixtures before the suite runs.

    The fixtures are synthetic and deterministic, and every extension they use
    (``.img``, ``.bin``) is gitignored, so they are generated here rather than
    committed. Nothing device-derived is written: see make_fixture.py.
    """
    make_fixture.write_all()


def load(name):
    with open(os.path.join(FIX, name), "rb") as handle:
        return handle.read()


class TestFixtureDeterminism(unittest.TestCase):
    def test_regeneration_is_byte_exact(self):
        first = dict((n, d) for n, _s, d in make_fixture.write_all())
        second = dict((n, d) for n, _s, d in make_fixture.write_all())
        self.assertEqual(first, second)
        self.assertEqual(len(first), 15)


class TestDetection(unittest.TestCase):
    def test_boot_image(self):
        self.assertEqual(parser.detect_format(load("boot_v0.img")), "boot_image")

    def test_vendor_boot_image(self):
        self.assertEqual(parser.detect_format(load("vendor_boot_v4.img")),
                         "vendor_boot_image")

    def test_dt_table(self):
        self.assertEqual(parser.detect_format(load("dt_table_multi.img")), "dt_table")

    def test_vbmeta(self):
        self.assertEqual(parser.detect_format(load("vbmeta_rsa4096.img")), "avb_vbmeta")

    def test_elf(self):
        self.assertEqual(parser.detect_format(load("elf64.bin")), "elf")

    def test_garbage_is_none(self):
        self.assertIsNone(parser.detect_format(load("garbage.bin")))

    def test_parse_garbage_raises(self):
        with self.assertRaises(parser.ParseError):
            parser.parse(load("garbage.bin"))

    def test_truncated_boot_raises(self):
        with self.assertRaises(parser.ParseError):
            parser.parse(load("truncated_boot.img"))


class TestBootV0(unittest.TestCase):
    def setUp(self):
        self.data = load("boot_v0.img")
        self.result = parser.parse_boot_image(self.data)

    def test_header_version(self):
        self.assertEqual(self.result["header_version"], 0)

    def test_page_size_from_header(self):
        self.assertEqual(self.result["page_size"], 2048)

    def test_sizes(self):
        self.assertEqual(self.result["kernel_size"], 5000)
        self.assertEqual(self.result["ramdisk_size"], 3000)
        self.assertEqual(self.result["second_size"], 1000)

    def test_name_and_cmdline(self):
        self.assertEqual(self.result["name"], "synth")
        self.assertEqual(self.result["cmdline"], "console=ttyS0")

    def test_page_arithmetic_closes(self):
        page = self.result["page_size"]
        expected = page
        expected += parser._round_up(5000, page)
        expected += parser._round_up(3000, page)
        expected += parser._round_up(1000, page)
        self.assertEqual(self.result["computed_end"], expected)
        self.assertEqual(self.result["computed_end"], len(self.data))
        self.assertEqual(self.result["trailing_bytes"], 0)

    def test_section_offsets(self):
        names = [s[0] for s in self.result["sections"]]
        self.assertEqual(names, ["kernel", "ramdisk", "second"])
        self.assertEqual(self.result["sections"][0][1], 2048)

    def test_os_version_zero_is_none(self):
        self.assertIsNone(self.result["os_version"])

    def test_id_is_32_bytes(self):
        self.assertEqual(len(self.result["id"]), 64)


class TestBootV2(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse_boot_image(load("boot_v2.img"))

    def test_header_version(self):
        self.assertEqual(self.result["header_version"], 2)

    def test_dtb_section_present(self):
        names = [s[0] for s in self.result["sections"]]
        self.assertIn("dtb", names)
        self.assertEqual(self.result["dtb_size"], 2048)

    def test_recovery_dtbo_absent(self):
        self.assertEqual(self.result["recovery_dtbo_size"], 0)
        names = [s[0] for s in self.result["sections"]]
        self.assertNotIn("recovery_dtbo", names)

    def test_arithmetic_closes(self):
        self.assertEqual(self.result["computed_end"], len(load("boot_v2.img")))


class TestBootV3V4(unittest.TestCase):
    def test_v3_header_size_and_page(self):
        result = parser.parse_boot_image(load("boot_v3.img"))
        self.assertEqual(result["header_version"], 3)
        self.assertEqual(result["header_size"], 1580)
        self.assertEqual(result["page_size"], 4096)

    def test_v3_os_version_decodes(self):
        result = parser.parse_boot_image(load("boot_v3.img"))
        self.assertEqual(result["os_version"], {
            "major": 14, "minor": 0, "patch": 0, "year": 2024, "month": 3,
        })

    def test_v4_has_signature_section(self):
        result = parser.parse_boot_image(load("boot_v4.img"))
        self.assertEqual(result["header_version"], 4)
        self.assertEqual(result["header_size"], 1584)
        self.assertEqual(result["signature_size"], 4096)
        names = [s[0] for s in result["sections"]]
        self.assertIn("boot_signature", names)

    def test_v4_arithmetic_closes(self):
        data = load("boot_v4.img")
        result = parser.parse_boot_image(data)
        self.assertEqual(result["computed_end"], len(data))
        self.assertEqual(result["trailing_bytes"], 0)

    def test_der_tail_is_classified(self):
        data = load("boot_v4_der_tail.img")
        result = parser.parse_boot_image(data)
        self.assertEqual(result["trailing_bytes"], 254)
        self.assertEqual(result["trailing"]["kind"], "der_sequence")
        self.assertTrue(result["trailing"]["der_covers_tail"])


class TestVendorBoot(unittest.TestCase):
    def test_v3_layout(self):
        result = parser.parse_vendor_boot_image(load("vendor_boot_v3.img"))
        self.assertEqual(result["header_version"], 3)
        self.assertEqual(result["header_size"], 2112)
        self.assertEqual(result["vendor_ramdisk_size"], 3000)
        self.assertEqual(result["dtb_size"], 1024)
        self.assertEqual(result["vendor_ramdisk_table"], [])
        self.assertEqual(result["computed_end"], len(load("vendor_boot_v3.img")))

    def test_v4_layout(self):
        result = parser.parse_vendor_boot_image(load("vendor_boot_v4.img"))
        self.assertEqual(result["header_version"], 4)
        self.assertEqual(result["header_size"], 2128)
        self.assertEqual(result["vendor_ramdisk_table_entry_num"], 2)
        self.assertEqual(result["vendor_ramdisk_table_entry_size"], 108)
        self.assertEqual(result["vendor_ramdisk_table_size"], 216)

    def test_v4_ramdisk_table_entries(self):
        result = parser.parse_vendor_boot_image(load("vendor_boot_v4.img"))
        table = result["vendor_ramdisk_table"]
        self.assertEqual(len(table), 2)
        self.assertEqual(table[0]["ramdisk_name"], "platform")
        self.assertEqual(table[0]["ramdisk_type"], 1)
        self.assertEqual(table[0]["ramdisk_size"], 1000)
        self.assertEqual(table[1]["ramdisk_name"], "dlkm")
        self.assertEqual(table[1]["ramdisk_type"], 3)
        self.assertEqual(table[1]["ramdisk_offset"], 1000)

    def test_v4_bootconfig_present(self):
        result = parser.parse_vendor_boot_image(load("vendor_boot_v4.img"))
        self.assertEqual(result["bootconfig_size"], 300)
        names = [s[0] for s in result["sections"]]
        self.assertIn("bootconfig", names)


class TestDtTable(unittest.TestCase):
    def test_field_order_is_not_the_naive_read(self):
        data = load("dt_table_multi.img")
        result = parser.parse_dt_table(data)
        self.assertEqual(result["entry_size"], 32)
        self.assertEqual(result["entry_count"], 3)
        naive = struct_unpack_naive(data)
        self.assertNotEqual(naive[3], result["entry_size"])

    def test_multi_entries(self):
        result = parser.parse_dt_table(load("dt_table_multi.img"))
        self.assertEqual(len(result["entries"]), 3)
        self.assertEqual([e["dtb_size"] for e in result["entries"]],
                         [1024, 2048, 512])
        self.assertEqual([e["id"] for e in result["entries"]], [0, 1, 2])

    def test_fdt_magic_at_every_offset(self):
        result = parser.parse_dt_table(load("dt_table_multi.img"))
        self.assertTrue(all(e["fdt_magic_ok"] for e in result["entries"]))

    def test_bounds_ok(self):
        result = parser.parse_dt_table(load("dt_table_multi.img"))
        self.assertTrue(all(e["bounds_ok"] for e in result["entries"]))

    def test_total_size_matches_file(self):
        result = parser.parse_dt_table(load("dt_table_single.img"))
        self.assertTrue(result["total_size_matches_file"])

    def test_header_and_page(self):
        result = parser.parse_dt_table(load("dt_table_single.img"))
        self.assertEqual(result["header_size"], 32)
        self.assertEqual(result["page_size"], 2048)
        self.assertEqual(result["version"], 0)

    def test_bad_magic_raises(self):
        with self.assertRaises(parser.ParseError):
            parser.parse_dt_table(load("garbage.bin"))


def struct_unpack_naive(data):
    import struct
    return struct.unpack_from(">7I", data, 4)


class TestAvbVbmeta(unittest.TestCase):
    def setUp(self):
        self.data = load("vbmeta_rsa4096.img")
        self.result = parser.parse_avb_vbmeta(self.data)

    def test_header_fields(self):
        self.assertEqual(self.result["version_major"], 1)
        self.assertEqual(self.result["version_minor"], 0)
        self.assertEqual(self.result["algorithm_type"], 2)
        self.assertEqual(self.result["algorithm_name"], "SHA256_RSA4096")

    def test_total_size(self):
        self.assertEqual(self.result["total_size"], len(self.data))

    def test_release_string(self):
        self.assertEqual(self.result["release_string"], "avbtool 1.2.0")

    def test_one_hash_descriptor(self):
        self.assertEqual(len(self.result["descriptors"]), 1)
        descriptor = self.result["descriptors"][0]
        self.assertEqual(descriptor["tag_name"], "HASH")
        self.assertEqual(descriptor["partition_name"], "boot")
        self.assertEqual(descriptor["hash_algorithm"], "sha256")

    def test_descriptor_length_self_consistent(self):
        descriptor = self.result["descriptors"][0]
        self.assertEqual(descriptor["descriptor_payload"],
                         descriptor["num_bytes_following"])

    def test_vbmeta_digest_law(self):
        ok, computed, stored = parser.avb_verify_vbmeta_digest(self.data, self.result)
        self.assertTrue(ok)
        self.assertEqual(computed, stored)

    def test_hash_descriptor_law(self):
        descriptor = self.result["descriptors"][0]
        payload = make_fixture.stream(b"vbmeta-payload", 8192)
        ok, computed, stored = parser.avb_verify_hash_descriptor(payload, descriptor)
        self.assertTrue(ok)
        self.assertEqual(computed, stored)

    def test_hash_descriptor_law_detects_corruption(self):
        descriptor = self.result["descriptors"][0]
        payload = bytearray(make_fixture.stream(b"vbmeta-payload", 8192))
        payload[0] ^= 0xFF
        ok, _computed, _stored = parser.avb_verify_hash_descriptor(bytes(payload),
                                                                   descriptor)
        self.assertFalse(ok)


class TestDtboWithAvb(unittest.TestCase):
    def setUp(self):
        self.data = load("dtbo_with_avb.img")
        self.result = parser.parse(self.data)

    def test_detected_as_dt_table(self):
        self.assertEqual(self.result["format"], "dt_table")

    def test_footer_found(self):
        self.assertIn("avb_footer", self.result)
        self.assertEqual(self.result["avb_footer"]["version_major"], 1)

    def test_vbmeta_followed(self):
        self.assertIn("avb_vbmeta", self.result)
        self.assertEqual(self.result["avb_vbmeta"]["algorithm_name"],
                         "SHA256_RSA4096")

    def test_footer_offsets_agree(self):
        footer = self.result["avb_footer"]
        self.assertEqual(footer["vbmeta_offset"] + footer["vbmeta_size"],
                         footer["footer_offset"])

    def test_descriptor_names_the_partition(self):
        descriptors = self.result["avb_vbmeta"]["descriptors"]
        self.assertEqual(descriptors[0]["partition_name"], "dtbo")

    def test_hash_descriptor_law_on_padded_image(self):
        descriptor = self.result["avb_vbmeta"]["descriptors"][0]
        ok, computed, stored = parser.avb_verify_hash_descriptor(self.data, descriptor)
        self.assertTrue(ok)
        self.assertEqual(computed, stored)

    def test_vbmeta_digest_law(self):
        footer = self.result["avb_footer"]
        blob = self.data[footer["vbmeta_offset"]:footer["vbmeta_offset"] + footer["vbmeta_size"]]
        ok, computed, stored = parser.avb_verify_vbmeta_digest(blob,
                                                               self.result["avb_vbmeta"])
        self.assertTrue(ok)
        self.assertEqual(computed, stored)


class TestElf(unittest.TestCase):
    def test_elf64_single(self):
        result = parser.parse_elf_headers(load("elf64.bin"))
        self.assertEqual(result["class"], 64)
        self.assertEqual(result["e_machine"], 183)
        self.assertEqual(result["elf_count"], 1)
        self.assertTrue(result["entry_in_load"])

    def test_elf32_multi_counts_both(self):
        result = parser.parse_elf_headers(load("elf32_multi.bin"))
        self.assertEqual(result["class"], 32)
        self.assertEqual(result["elf_count"], 2)
        self.assertEqual(result["elf_magic_offsets"][0], 0)

    def test_multi_outer_machine_differs_from_inner(self):
        result = parser.parse_elf_headers(load("elf32_multi.bin"))
        self.assertEqual(result["e_machine"], 1)
        inner = result["elf_magic_offsets"][1]
        self.assertGreater(inner, 0)

    def test_entry_in_load_false_when_outside(self):
        data = bytearray(load("elf64.bin"))
        data[0x18:0x20] = (0x900000).to_bytes(8, "little")
        result = parser.parse_elf_headers(bytes(data))
        self.assertFalse(result["entry_in_load"])


class TestOsVersionDecode(unittest.TestCase):
    def test_zero_is_none(self):
        self.assertIsNone(parser.decode_os_version(0))

    def test_documented_bit_layout(self):
        raw = (14 << 25) | (0 << 18) | (0 << 11) | ((2024 - 2000) << 4) | 3
        decoded = parser.decode_os_version(raw)
        self.assertEqual(decoded["major"], 14)
        self.assertEqual(decoded["year"], 2024)
        self.assertEqual(decoded["month"], 3)


class TestRoundUp(unittest.TestCase):
    def test_exact_multiple(self):
        self.assertEqual(parser._round_up(4096, 4096), 4096)

    def test_partial(self):
        self.assertEqual(parser._round_up(4097, 4096), 8192)

    def test_zero(self):
        self.assertEqual(parser._round_up(0, 4096), 0)

    def test_bad_page(self):
        with self.assertRaises(parser.ParseError):
            parser._round_up(10, 0)


class TestCli(unittest.TestCase):
    def test_cli_json(self):
        script = os.path.join(HERE, "bootimg_parser.py")
        proc = subprocess.run(
            [sys.executable, "-I", script, "--json",
             os.path.join(FIX, "boot_v2.img")],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["parsed"]["format"], "boot_image")
        self.assertEqual(payload["parsed"]["header_version"], 2)

    def test_cli_unrecognised_exits_nonzero(self):
        script = os.path.join(HERE, "bootimg_parser.py")
        proc = subprocess.run(
            [sys.executable, "-I", script, "--json",
             os.path.join(FIX, "garbage.bin")],
            capture_output=True, text=True,
        )
        self.assertNotEqual(proc.returncode, 0)


@unittest.skipUnless(REAL, "BOOT_FIXTURE_REAL not set")
class TestRealPayloads(unittest.TestCase):
    """The same laws on real vendor bytes held in scratch space."""

    def test_real_boot_image(self):
        path = os.path.join(REAL, "real_boot.img")
        if not os.path.exists(path):
            self.skipTest("real_boot.img absent")
        with open(path, "rb") as handle:
            data = handle.read()
        result = parser.parse(data)
        self.assertEqual(result["format"], "boot_image")
        self.assertEqual(result["header_version"], 0)
        self.assertEqual(result["page_size"], 4096)
        self.assertEqual(result["kernel_size"], 10456559)
        self.assertEqual(result["ramdisk_size"], 1280946)
        self.assertEqual(result["computed_end"], 11743232)
        self.assertEqual(result["trailing_bytes"], 1254)
        self.assertEqual(result["trailing"]["kind"], "der_sequence")
        self.assertTrue(result["trailing"]["der_covers_tail"])

    def test_real_dtbo_with_avb(self):
        path = os.path.join(REAL, "a21s_dtbo.img")
        if not os.path.exists(path):
            self.skipTest("a21s_dtbo.img absent")
        with open(path, "rb") as handle:
            data = handle.read()
        result = parser.parse(data)
        self.assertEqual(result["format"], "dt_table")
        self.assertEqual(result["entry_size"], 32)
        self.assertEqual(result["entry_count"], 5)
        self.assertTrue(all(e["fdt_magic_ok"] for e in result["entries"]))
        self.assertEqual(result["avb_footer"]["original_image_size"], 748480)
        descriptor = result["avb_vbmeta"]["descriptors"][0]
        self.assertEqual(descriptor["partition_name"], "dtbo")
        self.assertEqual(descriptor["image_size"], 748480)
        ok, computed, stored = parser.avb_verify_hash_descriptor(data, descriptor)
        self.assertTrue(ok)
        self.assertEqual(computed, stored)

    def test_real_dtb_single(self):
        path = os.path.join(REAL, "a21s_twrp_dtb.img")
        if not os.path.exists(path):
            self.skipTest("a21s_twrp_dtb.img absent")
        with open(path, "rb") as handle:
            data = handle.read()
        result = parser.parse(data)
        self.assertEqual(result["format"], "dt_table")
        self.assertEqual(result["entry_count"], 1)
        self.assertTrue(result["total_size_matches_file"])
        self.assertTrue(result["entries"][0]["fdt_magic_ok"])
        self.assertNotIn("avb_footer", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
