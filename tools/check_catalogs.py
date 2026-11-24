#!/usr/bin/env python3
"""Validate the machine-readable issue catalogs.

Each file in docs/issue-catalog/*.jsonl must contain one JSON object per line
with the keys id, key, title, body and labels. Keys and ids must be unique
within a file. Counts are printed so a drifting catalog is visible in CI logs.
"""

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "docs", "issue-catalog")
REQUIRED = {"id", "key", "title", "body", "labels"}


def main():
    failures = []
    total = 0
    for path in sorted(glob.glob(os.path.join(CATALOG, "*.jsonl"))):
        name = os.path.basename(path)
        keys, ids = set(), set()
        count = 0
        with open(path, encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as exc:
                    failures.append("%s:%d invalid JSON: %s" % (name, number, exc))
                    continue
                missing = REQUIRED - set(obj)
                if missing:
                    failures.append("%s:%d missing %s" % (name, number, sorted(missing)))
                if obj.get("key") in keys:
                    failures.append("%s:%d duplicate key %r" % (name, number, obj.get("key")))
                if obj.get("id") in ids:
                    failures.append("%s:%d duplicate id %r" % (name, number, obj.get("id")))
                keys.add(obj.get("key"))
                ids.add(obj.get("id"))
                count += 1
        total += count
        print("%-28s %5d records" % (name, count))
    if failures:
        for failure in failures[:30]:
            print("FAIL " + failure)
        if len(failures) > 30:
            print("... and %d more" % (len(failures) - 30))
        return 1
    print("catalogs valid: %d records total" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
