#!/usr/bin/env python3
"""Refresh sf-pi/index.md from a local clone of github.com/salesforce/sf-pi.

Usage (no network access in the script itself; clone first):
  git clone --depth 1 https://github.com/salesforce/sf-pi /tmp/sf-pi
  python3 scripts/refresh_sf_pi.py /tmp/sf-pi [--date YYYY-MM-DD]

What it does:
- reads the clone's generated extension catalog (catalog/index.json), the
  optional companion list (catalog/recommendations.json), package.json and the
  top-level docs/*.md titles;
- rewrites sf-pi/index.md: published docs pages, every extension grouped by the
  catalog's intent group, and the optional companion packages;
- rewrites only the "Section breakdown" block of sf-pi/content.md; the
  hand-written prose is kept.

Only JSON and Markdown files are read; nothing from the clone is executed.
This folder is outside developer.salesforce.com, so scripts/refresh_from_llms.py
skips it (EXTRA_SOURCES).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "sf-pi"
REPO = "https://github.com/salesforce/sf-pi"
SITE = "https://opensource.salesforce.com/sf-pi"


def cell(value) -> str:
    text = " ".join(str(value or "").split()).replace("|", "\\|")
    return text or "—"


def title_of(md: Path) -> str:
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md.stem


def head_commit(clone: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(clone), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clone", type=Path, help="path to a local clone of salesforce/sf-pi")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args()
    clone = args.clone.resolve()
    exts = json.loads((clone / "catalog" / "index.json").read_text(encoding="utf-8"))
    recs = json.loads((clone / "catalog" / "recommendations.json").read_text(encoding="utf-8"))
    pkg = json.loads((clone / "package.json").read_text(encoding="utf-8"))
    docs = sorted(p for p in (clone / "docs").glob("*.md"))
    adrs = len(list((clone / "docs" / "adr").glob("*.md"))) if (clone / "docs" / "adr").is_dir() else 0

    groups: dict[str, list[dict]] = {}
    for e in exts:  # keep the catalog's own order of first appearance
        groups.setdefault((e.get("docs") or {}).get("intentGroup") or "Other", []).append(e)
    maturity = ", ".join(f"{k} {v}" for k, v in Counter(e.get("maturity", "?") for e in exts).items())
    default_on = sum(1 for e in exts if e.get("defaultEnabled"))

    out = [
        "# SF Pi -- Index",
        "",
        f"Source: [salesforce/sf-pi]({REPO}) (Apache-2.0) and its documentation site [{SITE.split('//')[1]}]({SITE}/). "
        "This folder is outside `developer.salesforce.com`, so `scripts/refresh_from_llms.py` skips it.",
        "",
        f"Extracted programmatically from the repository's generated catalog files at version {pkg.get('version', '?')} "
        f"(commit `{head_commit(clone)}`): {len(exts)} extensions ({maturity}; {default_on} enabled by default), "
        f"{len(recs.get('items', {}))} optional companion packages, {len(docs)} top-level docs pages. "
        f"Last refreshed {args.date} by `scripts/refresh_sf_pi.py`.",
        "",
        f"## Documentation pages ({len(docs)})",
        "",
        "| Page | URL | Source file |",
        "|---|---|---|",
    ]
    for p in docs:
        url = f"{SITE}/" if p.stem == "index" else f"{SITE}/{p.stem}"
        out.append(f"| {cell(title_of(p))} | {url} | `docs/{p.name}` |")
    out += [
        "",
        f"Architecture decision records: {adrs} files in [`docs/adr`]({REPO}/tree/main/docs/adr) "
        "(in the repository only; the docs site excludes them).",
        "",
    ]
    for name, items in groups.items():
        out += [f"## Extensions: {name} ({len(items)})", "",
                "| Extension | ID | Category | Maturity | Commands | Tools | Description |", "|---|---|---|---|---|---|---|"]
        for e in items:
            cmds = ", ".join(f"`{c}`" for c in e.get("commands") or []) or "—"
            out.append(
                f"| [{cell(e.get('name'))}]({SITE}/extensions/{e['id']}) | `{e['id']}` | {cell(e.get('category'))} | "
                f"{cell(e.get('maturity'))} | {cmds} | {len(e.get('tools') or [])} | {cell(e.get('description'))} |")
        out.append("")
    items = recs.get("items", {})
    out += [f"## Optional companion packages ({len(items)})", "",
            "Third-party Pi packages that SF Pi recommends. They are installed only on explicit request (`/sf-pi recommended`).", "",
            "| Package | Source | License | Description |", "|---|---|---|---|"]
    for it in items.values():
        out.append(f"| [{cell(it.get('name'))}]({it.get('homepage') or REPO}) | `{cell(it.get('source'))}` | "
                   f"{cell(it.get('license'))} | {cell(it.get('description'))} |")
    out.append("")
    FOLDER.mkdir(exist_ok=True)
    (FOLDER / "index.md").write_text("\n".join(out), encoding="utf-8")

    content = FOLDER / "content.md"
    updated = False
    if content.exists():
        block = "Section breakdown:\n" + "\n".join(
            f"- **{n}** — {len(i)} extension{'' if len(i) == 1 else 's'}" for n, i in groups.items()) + "\n"
        text, updated = re.subn(r"Section breakdown:\n(?:- .*\n?)+", block, content.read_text(encoding="utf-8"), count=1)
        if updated:
            content.write_text(text, encoding="utf-8")
    print(f"version {pkg.get('version')}: {len(exts)} extensions, {len(items)} companions, {len(docs)} docs pages; "
          f"content.md breakdown updated: {bool(updated)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
