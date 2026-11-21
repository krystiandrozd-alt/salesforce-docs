#!/usr/bin/env python3
"""Refresh this catalog from the official Salesforce llms.txt files.

Usage (needs Playwright + Chromium; plain HTTP to developer.salesforce.com returns 403):
  pip install playwright && python -m playwright install chromium
  python3 scripts/refresh_from_llms.py [--date YYYY-MM-DD]

What it does:
- reads https://developer.salesforce.com/docs/llms.txt and every llms-<area>.txt it lists;
- regenerates <area>/index.md (full link list, grouped by section) for every area;
- creates <area>/content.md for new areas; for existing areas it keeps the
  hand-written synthesis and only rewrites the "Section breakdown" block and the
  "Last refreshed" line;
- regenerates salesforce-platform-docs-content-list.md (keeps existing row
  descriptions, uses the official description for new rows) and the status,
  count and top-ten parts of README.md;
- reports areas that disappeared from llms.txt (folders are left untouched);
- skips the folders in EXTRA_SOURCES (built from other sources; see README).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LLMS = "https://developer.salesforce.com/docs/llms.txt"
LINK = re.compile(r"^\s*- \[(.+?)\]\((https?://[^)\s]+)\)(?::\s*(.*))?$")
LIST_FILE = ROOT / "salesforce-platform-docs-content-list.md"
# Folders built from sources outside developer.salesforce.com (README, "Additional sources"),
# each with its own refresh script. Not regenerated here and not reported as "no longer listed".
EXTRA_SOURCES = {"agentforce-labs", "sf-pi"}


def fetch_all() -> tuple[list[tuple[str, str, str]], dict[str, str]]:
    from playwright.sync_api import sync_playwright

    areas, texts = [], {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = b.new_page()

        def get(url: str) -> str:
            r = page.goto(url, wait_until="domcontentloaded", timeout=120000)
            if not r or r.status != 200:
                raise RuntimeError(f"{url}: HTTP {r.status if r else '?'}")
            return page.evaluate("document.body.innerText")

        for line in get(LLMS).splitlines():
            m = LINK.match(line)
            if not m or "/docs/llms-" not in m.group(2):
                continue
            slug = re.search(r"/llms-([a-z0-9-]+)\.txt", m.group(2)).group(1)
            areas.append((slug, m.group(1).strip(), clean(m.group(3) or "")))
            print(f"fetch {slug}", file=sys.stderr)
            texts[slug] = get(m.group(2))
        b.close()
    return areas, texts


PLACEHOLDER = re.compile(r"write a brief description of the repository", re.I)


def clean(desc: str) -> str:
    """Drop Salesforce's unfilled template description."""
    return "" if PLACEHOLDER.search(desc or "") else (desc or "").strip()


def parse(text: str) -> tuple[str, list[tuple[str, list[tuple[str, str]]]]]:
    overview, sections, cur, in_overview = [], [], None, False
    for line in text.splitlines():
        if line.startswith("## "):
            name = line[3:].strip()
            in_overview = name.lower() == "overview"
            cur = None if in_overview else (name, [])
            if cur:
                sections.append(cur)
            continue
        m = LINK.match(line)
        if m and cur is not None:
            cur[1].append((m.group(1).replace("|", "\\|").strip(), m.group(2)))
        elif in_overview and line.strip() and not line.startswith("#"):
            overview.append(line.strip())
    sections = [s for s in sections if s[1]]
    return clean(" ".join(overview)), sections


def write_index(slug: str, title: str, sections, today: str) -> int:
    n = sum(len(s[1]) for s in sections)
    out = [
        f"# {title} -- Index",
        "",
        f"Source: [llms-{slug}.txt](https://developer.salesforce.com/docs/llms-{slug}.txt).",
        "",
        f"Full link list extracted programmatically from the live source file ({n} page links across "
        f"{len(sections)} sections). Last refreshed {today} by `scripts/refresh_from_llms.py`.",
        "",
    ]
    for name, links in sections:
        out += [f"## {name} ({len(links)} pages)", "", "| Page | URL |", "|---|---|"]
        out += [f"| {t} | {u} |" for t, u in links]
        out.append("")
    (ROOT / slug).mkdir(exist_ok=True)
    (ROOT / slug / "index.md").write_text("\n".join(out), encoding="utf-8")
    return n


def breakdown(sections) -> str:
    return "Section breakdown:\n" + "\n".join(f"- **{n}** — {len(l)} pages" for n, l in sections) + "\n"


def write_content(slug: str, title: str, overview: str, sections, today: str, n: int) -> bool:
    path = ROOT / slug / "content.md"
    stamp = f"*Last refreshed {today}: {n} pages in {len(sections)} sections (counts from the live source).*"
    if not path.exists():
        body = [
            f"# {title} — Content",
            "",
            "Overview as published in the source index (short official description, not page text).",
            "",
            overview or "No overview text in source — title-only index.",
            "",
            breakdown(sections),
            f"*Source: [`llms-{slug}.txt`](https://developer.salesforce.com/docs/llms-{slug}.txt) — official aggregated index (developer doc page), overview section.*",
            "",
            stamp,
            "",
            "## Extraction notes",
            "",
            f"Built programmatically from the index file's own \"Overview\" text and section listing; no deep page-by-page review. See [index.md](index.md) for the full {n}-page link list.",
            "",
        ]
        path.write_text("\n".join(body), encoding="utf-8")
        return True
    text = path.read_text(encoding="utf-8")
    new_bd = breakdown(sections)
    if re.search(r"Section breakdown:\n(?:- .*\n?)+", text):
        text = re.sub(r"Section breakdown:\n(?:- .*\n?)+", new_bd, text, count=1)
    text = re.sub(r"\n\*Last refreshed [^\n]*\*\n", "\n", text)
    text = re.sub(r"(\n## Extraction notes)", "\n" + stamp + "\n\\1", text, count=1) if "## Extraction notes" in text \
        else text.rstrip() + "\n\n" + stamp + "\n"
    path.write_text(text, encoding="utf-8")
    return False


def old_descriptions() -> dict[str, str]:
    d = {}
    if LIST_FILE.exists():
        for line in LIST_FILE.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\| \d+ \| [^|]+ \| [^|]+ \| \[folder\]\(([a-z0-9-]+)/\) \| (.*) \|$", line)
            if m:
                d[m.group(1)] = m.group(2)
    return d


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=date.today().isoformat())
    a = ap.parse_args()
    today = a.date
    descs = old_descriptions()
    areas, texts = fetch_all()
    rows, sizes, created = [], [], []
    for i, (slug, title, desc) in enumerate(areas, 1):
        overview, sections = parse(texts[slug])
        n = write_index(slug, title, sections, today)
        if write_content(slug, title, overview, sections, today, n):
            created.append(slug)
        d = clean(descs.get(slug, "")) or desc or overview or "No overview text in source."
        d = re.sub(r"\s*\*\*[\d,]+ links\.\*\*", "", d).strip()
        if n >= 1000:
            d += f" **{n:,} links.**"
        rows.append(f"| {i} | ✅ | {title} | [folder]({slug}/) | {d} |")
        sizes.append((slug, n, (ROOT / slug / "index.md").stat().st_size))
    gone = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "index.md").exists()
                  and p.name not in {s for s, _, _ in areas} and p.name not in EXTRA_SOURCES)
    total = len(areas)
    lst = [
        "# Salesforce Developer Documentation — Content List (Index)",
        "",
        f"Source: [`{LLMS}`]({LLMS}) (aggregated index, llmstxt.org standard)",
        f"Captured: 2026-10-24. Last refreshed: {today} with `scripts/refresh_from_llms.py` (all folders regenerated from the live source).",
        "",
        f"This is the authoritative index of all {total} product-specific `llms.txt` sections published under the Developer Documentation Portal. "
        "Each product has its own folder (`index.md` + `content.md`, full link list + synthesis) — see [README.md](README.md) for the folder format.",
        "",
        f"**{total} of {total} done.**",
        "",
        "| # | Status | Product | Folder | Description |",
        "|---|---|---------|---------------|--------------|",
        *rows,
        "",
    ]
    if gone:
        lst += ["## No longer listed in llms.txt", "", *[f"- [{g}]({g}/) — kept as an archived snapshot" for g in gone], ""]
    LIST_FILE.write_text("\n".join(lst), encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = re.sub(r"all \d+ product-specific", f"all {total} product-specific", readme)
    readme = re.sub(r"## Status: \d+ of \d+ products done", f"## Status: {total} of {total} products done", readme)
    readme = re.sub(r"full \d+-row table", f"full {total}-row table", readme)
    top = sorted(sizes, key=lambda s: -s[2])[:10]
    table = "| Product | Links | `index.md` size |\n|---|---|---|\n" + "\n".join(
        f"| [{s}]({s}/) | {n:,} | {sz / 1048576:.2f} MB |" if sz >= 1048576 else f"| [{s}]({s}/) | {n:,} | {sz // 1024} KB |"
        for s, n, sz in top) + "\n"
    readme = re.sub(r"## The ten largest indexes \([^)]*\)\n\n(?:\|.*\n)+", "## The ten largest indexes (by `index.md` size, from the refresh script)\n\n" + table, readme)
    readme = re.sub(r"even `product-docs`, which alone is larger than the previous \d+ folders combined\.",
                    "including `product-docs`, the largest single index.", readme)
    if "scripts/refresh_from_llms.py" not in readme.split("## Format per product folder")[1].split("##")[0]:
        readme = readme.replace(
            "- `content.md` —",
            "- `scripts/refresh_from_llms.py` (repo root) — regenerates every `index.md`, the content list and README counts from the live `llms.txt`; keeps hand-written `content.md` prose.\n- `content.md` —", 1)
    readme = re.sub(r"Captured starting 2026-10-24\.[^\n]*", f"Captured starting 2026-10-24. Last refreshed {today} with [`scripts/refresh_from_llms.py`](scripts/refresh_from_llms.py).", readme)
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"areas: {total}; new folders: {', '.join(created) or 'none'}; no longer listed: {', '.join(gone) or 'none'}")
    print(f"pages: {sum(s[1] for s in sizes):,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
