#!/usr/bin/env python3
"""Check that every developer.salesforce.com link in views/*.md exists in a generated index.md.

Usage: python3 scripts/check_views.py
Exits 1 and lists missing URLs if a curated view links to a page that is no longer in the catalog.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = re.compile(r"https://developer\.salesforce\.com/[^\s|)>\]]+")


def main() -> int:
    known: set[str] = set()
    for idx in ROOT.glob("*/index.md"):
        known.update(URL.findall(idx.read_text(encoding="utf-8")))
    failed = 0
    for view in sorted((ROOT / "views").glob("*.md")):
        urls = sorted(set(URL.findall(view.read_text(encoding="utf-8"))))
        missing = [u for u in urls if u not in known]
        print(f"{view.relative_to(ROOT)}: {len(urls)} links, {len(missing)} missing")
        for u in missing:
            print(f"  MISSING {u}")
        failed += len(missing)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
