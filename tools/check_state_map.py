#!/usr/bin/env python3
"""Check that REPO-STATE-MAP.md does not point at artifacts that vanished.

The state map is a dated human snapshot; this check cannot regenerate it, but
it does catch the expensive failure mode: a path quoted as an existing
deliverable that no longer resolves in the checkout. Lines that explicitly say
the path is absent, or that the verdict is NEW / none, are skipped.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "docs", "REPO-STATE-MAP.md")
ROOTS = ("research/", "implementations/", "docs/", "tools/", "upstream/", "data/", "site/")
BACKTICK = re.compile(r"`([^`]+)`")
ABSENT = ("does not exist", "none dedicated", "none ", "no dedicated", "| NEW |")


def main():
    with open(MAP, encoding="utf-8") as handle:
        lines = handle.readlines()
    missing = []
    checked = 0
    for number, line in enumerate(lines, 1):
        if any(marker in line for marker in ABSENT):
            continue
        for token in BACKTICK.findall(line):
            path = token.strip().rstrip("/")
            if not path.startswith(ROOTS) or " " in path or "*" in path:
                continue
            if "<" in path or ">" in path or "http" in path:
                continue
            checked += 1
            if not os.path.exists(os.path.join(ROOT, path)):
                missing.append((number, path))
    if missing:
        print("REPO-STATE-MAP.md references %d missing paths:" % len(missing))
        for number, path in missing:
            print("  line %d: %s" % (number, path))
        return 1
    print("REPO-STATE-MAP.md: %d referenced artifact paths resolve" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
