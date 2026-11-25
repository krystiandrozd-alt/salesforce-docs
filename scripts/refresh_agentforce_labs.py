#!/usr/bin/env python3
"""Refresh the agentforce-labs folder from the Agentforce Labs capability manifest.

Usage (plain HTTPS, no browser needed):
  python3 scripts/refresh_agentforce_labs.py [--date YYYY-MM-DD]

What it does:
- reads https://labs.agentforce.com/api/capabilities (the site's own JSON list of
  every page, tool and experiment);
- rewrites agentforce-labs/index.md: every entry, grouped by the manifest's
  category, with canonical page, Markdown source, interaction type and description;
- rewrites only the "Section breakdown" block of agentforce-labs/content.md;
  the hand-written prose there and in org-configuration.md is kept.

This folder is outside developer.salesforce.com, so scripts/refresh_from_llms.py
skips it (EXTRA_SOURCES).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "agentforce-labs"
MANIFEST = "https://labs.agentforce.com/api/capabilities"
ENTRY_POINTS = [
    ("llms.txt", "https://labs.agentforce.com/llms.txt", "Getting-started instructions for coding agents and a short reference list"),
    ("llms.html", "https://labs.agentforce.com/llms.html", "The same instructions as HTML"),
    ("llms-full.txt", "https://labs.agentforce.com/llms-full.txt", "All documentation in one file"),
    ("Capability manifest", MANIFEST, "JSON list of every page, tool and experiment; the source of this index"),
]


def pages(n: int) -> str:
    return f"{n} page" if n == 1 else f"{n} pages"


def cell(value: str | None) -> str:
    text = " ".join((value or "").split()).replace("|", "\\|")
    return text or "—"


def fetch() -> dict:
    req = urllib.request.Request(MANIFEST, headers={"User-Agent": "docs-catalog-refresh/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def group(caps: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for c in caps:  # keep the manifest's own order of first appearance
        groups.setdefault(c.get("category") or "Uncategorised", []).append(c)
    return groups


def write_index(caps: list[dict], groups: dict[str, list[dict]], today: str) -> None:
    status = ", ".join(f"{k} {v}" for k, v in Counter(c.get("status", "?") for c in caps).items())
    audience = ", ".join(f"{k} {v}" for k, v in Counter(c.get("audience", "?") for c in caps).items())
    out = [
        "# Agentforce Labs -- Index",
        "",
        f"Source: [capability manifest]({MANIFEST}) published by Agentforce Labs (`labs.agentforce.com`). "
        "This folder is outside `developer.salesforce.com`, so `scripts/refresh_from_llms.py` skips it.",
        "",
        f"Full list extracted programmatically from the live manifest ({len(caps)} entries in {len(groups)} categories; "
        f"status: {status}; audience: {audience}). Last refreshed {today} by `scripts/refresh_agentforce_labs.py`. "
        "Categories are the manifest's own labels, in its order.",
        "",
        "## Machine-readable entry points",
        "",
        "| Entry point | URL | What it is |",
        "|---|---|---|",
        *[f"| {n} | {u} | {d} |" for n, u, d in ENTRY_POINTS],
        "",
    ]
    for name, items in groups.items():
        out += [f"## {name} ({pages(len(items))})", "", "| Page | Canonical page | Markdown | Type | Description |", "|---|---|---|---|---|"]
        out += [
            f"| {cell(c.get('title'))} | {c.get('canonicalUrl') or '—'} | {c.get('markdownUrl') or '—'} | "
            f"{cell(c.get('interaction'))} | {cell(c.get('description'))} |"
            for c in items
        ]
        out.append("")
    (FOLDER / "index.md").write_text("\n".join(out), encoding="utf-8")


def update_breakdown(groups: dict[str, list[dict]]) -> bool:
    path = FOLDER / "content.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    block = "Section breakdown:\n" + "\n".join(f"- **{n}** — {pages(len(i))}" for n, i in groups.items()) + "\n"
    new, count = re.subn(r"Section breakdown:\n(?:- .*\n?)+", block, text, count=1)
    if count:
        path.write_text(new, encoding="utf-8")
    return bool(count)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args()
    caps = fetch()["capabilities"]
    groups = group(caps)
    write_index(caps, groups, args.date)
    updated = update_breakdown(groups)
    print(f"entries: {len(caps)}; categories: {len(groups)}; content.md breakdown updated: {updated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
