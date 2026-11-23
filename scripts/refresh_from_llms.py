#!/usr/bin/env python3
"""Refresh this catalog from the official Salesforce llms.txt files.

Usage (needs Playwright + Chromium; plain HTTP to developer.salesforce.com returns 403):
  pip install playwright && python -m playwright install chromium
  python3 scripts/refresh_from_llms.py [--date YYYY-MM-DD]

What it does:
- reads https://developer.salesforce.com/docs/llms.txt and every llms-<area>.txt it lists;
- regenerates <area>/index.md (full link list, grouped by section) for every area.
  Some source files list the same URL many times (llms-product-docs.txt did on
  2026-11-23); each URL is kept once, with the title of its first occurrence, and
  the header reports the unique links and the removed duplicates;
- creates <area>/content.md for new areas; for existing areas it keeps the
  hand-written text, rewrites the "Section breakdown" block and the
  "Last refreshed" line, and updates every count wrapped in a count marker
  (see COUNT_MARK). Unmarked counts in known phrasings are wrapped on the first run;
- regenerates salesforce-platform-docs-content-list.md (keeps existing row
  descriptions without their link-count mentions, uses MANUAL_DESCRIPTIONS for areas
  whose source has no description, the official description for new rows) and the
  status, count, top-ten and largest-index parts of README.md;
- reports areas that disappeared from llms.txt (folders are left untouched).
Running it twice against an unchanged source leaves every file unchanged.
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

# One-sentence descriptions for areas whose llms.txt entry has no usable description,
# written from the section headings in each index.md. Kept here so a refresh cannot erase them.
MANUAL_DESCRIPTIONS = {
    "connect-rest": "REST API developer guides for Connect REST API, CRM Analytics, Einstein Discovery and Data Prep recipes.",
    "dataloader": "Dataloader from MuleSoft guide: importing, exporting and deleting Salesforce data, including connections to Box, Dropbox, FTP and SFTP.",
    "graphql-api": "Salesforce GraphQL API guide, including query examples for aggregation, grouping and ordering.",
    "headless-experience-layer": "Headless Experience Layer (HXL) developer guide (beta): building widgets and rich UI for Agentforce and external agents, and setting up MCP access.",
    "multi-framework": "Guides for Salesforce Multi-Framework and for embedding UI with Salesforce Microfrontend.",
    "platform-pkg-exchange": "ISV packaging and distribution guides: ISVforce, first- and second-generation managed packaging, and application installation.",
    "platform": "Core platform developer guides: REST, SOAP, Bulk and Streaming APIs, Platform Events and Change Data Capture, SOQL and SOSL, Aura components, Visualforce, Experience Cloud, mobile and offline, and developer limits.",
}

# Any link-count mention in a content-list description, such as "**6,844 links — 2nd largest.**",
# "**2,872 links across 25 sections.**" or "**829 links**, plus ...", together with the
# " (...)" or ", ..." clause that continues it.
COUNT_MENTION = re.compile(r"\s*\*\*[\d,]+\s+links?\b[^*]*\*\*(?:\s*\([^)]*\)|,[^.|]*)?\.?")
NO_DESCRIPTION = re.compile(r"\(no description provided[^)]*\)\.?", re.I)

# Counts inside content.md text are wrapped in markers so that every refresh finds and updates them:
#   <!--pages-->N<!--/pages-->               unique links in index.md
#   <!--pages:Section name-->N<!--/pages-->  links in one section
#   <!--sections-->N<!--/sections-->         number of sections
COUNT_MARK = re.compile(r"<!--(pages|sections)(?::([^>]*?))?-->(\d[\d,]*)<!--/\1-->")
STAMP = re.compile(r"\n*^\*Last refreshed [^\n]*\*$\n*", re.M)


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


def dedupe(sections):
    """Keep each URL once (its first occurrence and title); drop sections left empty."""
    seen, kept, removed = set(), [], 0
    for name, links in sections:
        unique = []
        for t, u in links:
            if u in seen:
                removed += 1
                continue
            seen.add(u)
            unique.append((t, u))
        if unique:
            kept.append((name, unique))
    return kept, removed


def write_index(slug: str, title: str, sections, today: str):
    """Write index.md with every URL once; return (unique links, deduplicated sections, removed entries)."""
    sections, removed = dedupe(sections)
    n = sum(len(s[1]) for s in sections)
    out = [
        f"# {title} -- Index",
        "",
        f"Source: [llms-{slug}.txt](https://developer.salesforce.com/docs/llms-{slug}.txt).",
        "",
        f"Full link list extracted programmatically from the live source file ({n} unique page links across "
        f"{len(sections)} sections; duplicate URLs removed: {removed}). "
        f"Last refreshed {today} by `scripts/refresh_from_llms.py`.",
        "",
    ]
    for name, links in sections:
        out += [f"## {name} ({len(links)} pages)", "", "| Page | URL |", "|---|---|"]
        out += [f"| {t} | {u} |" for t, u in links]
        out.append("")
    (ROOT / slug).mkdir(exist_ok=True)
    (ROOT / slug / "index.md").write_text("\n".join(out), encoding="utf-8")
    return n, sections, removed


def breakdown(sections) -> str:
    return "Section breakdown:\n" + "\n".join(f"- **{n}** — {len(l)} pages" for n, l in sections) + "\n"


def resolve_section(name: str, sections) -> str | None:
    """The section called `name`, or the only section whose heading contains all of its words."""
    names = [s for s, _ in sections]
    if name in names:
        return name
    words = set(re.findall(r"[\w.+/-]+", name.lower()))
    hits = [s for s in names if words <= set(re.findall(r"[\w.+/-]+", s.lower()))]
    return hits[0] if len(hits) == 1 else None


def mark_counts(text: str, sections, slug: str) -> str:
    """Wrap still-unmarked counts in known phrasings in count markers (needed once per file)."""
    free = r"(?<![\d,>])"  # a number that is not already inside a marker
    text = re.sub(free + r"(\d[\d,]*)(\s+(?:page\s+links|pages|links)\s+across\s+)(\d+)(\s+sections)",
                  lambda m: f"<!--pages-->{m[1]}<!--/pages-->{m[2]}<!--sections-->{m[3]}<!--/sections-->{m[4]}", text)
    text = re.sub(free + r"(\d[\d,]*)(?=-(?:page )?link list)", lambda m: f"<!--pages-->{m[1]}<!--/pages-->", text)

    def section(m: re.Match) -> str:
        name = resolve_section(m["name"].strip(), sections)
        if name is None:
            print(f"warning: {slug}/content.md: no section matches '{m['name'].strip()}' "
                  f"({m['num']} pages); count left unmarked", file=sys.stderr)
            return m[0]
        return f"{m['pre']}<!--pages:{name}-->{m['num']}<!--/pages-->"

    # "**Section name** (N pages" and "(Section name N pages" / ", Section name N pages"
    text = re.sub(r"(?P<pre>\*\*(?P<name>[^*\n]+)\*\*\s*\(\s*)(?P<num>\d[\d,]*)(?= pages)", section, text)
    text = re.sub(r"(?P<pre>[(,]\s*(?P<name>[A-Za-z][^(),;:*<>\n]*?)\s+)(?P<num>\d[\d,]*)(?= pages)", section, text)
    return text


def update_counts(text: str, n: int, sections, slug: str) -> str:
    """Set every marked count to its current value, keeping the thousands-separator style."""
    per_section = {name: len(links) for name, links in sections}

    def current(m: re.Match) -> str:
        kind, name, old = m[1], m[2], m[3]
        if kind == "sections":
            value = len(sections)
        elif name is None:
            value = n
        elif name in per_section:
            value = per_section[name]
        else:
            print(f"warning: {slug}/content.md: section '{name}' is no longer in the source; count kept", file=sys.stderr)
            return m[0]
        shown = f"{value:,}" if "," in old else str(value)
        return f"<!--{kind}{'' if name is None else ':' + name}-->{shown}<!--/{kind}-->"

    return COUNT_MARK.sub(current, text)


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
            f"Built programmatically from the index file's own \"Overview\" text and section listing; no deep page-by-page review. See [index.md](index.md) for the full <!--pages-->{n}<!--/pages-->-page link list.",
            "",
        ]
        path.write_text("\n".join(body), encoding="utf-8")
        return True
    text = path.read_text(encoding="utf-8")
    text = update_counts(mark_counts(text, sections, slug), n, sections, slug)
    text = re.sub(r"Section breakdown:\n(?:- .*\n?)+", lambda m: breakdown(sections), text, count=1)
    # One blank line on each side of the stamp, however many earlier runs left behind.
    text = STAMP.sub("\n\n", text)
    if "\n## Extraction notes" in text:
        text = re.sub(r"\n+## Extraction notes", lambda m: "\n\n" + stamp + "\n\n## Extraction notes", text, count=1)
    else:
        text = text.rstrip() + "\n\n" + stamp + "\n"
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


def describe(slug: str, old: str, official: str, overview: str, n: int) -> str:
    """Content-list description: no link-count mentions or placeholders, then the current count."""
    def tidy(s: str) -> str:
        s = NO_DESCRIPTION.sub("", COUNT_MENTION.sub("", clean(s)))
        return re.sub(r"\s{2,}", " ", s).strip()

    d = tidy(old)
    manual = MANUAL_DESCRIPTIONS.get(slug)
    if manual:
        rest = (d[len(manual):] if d.startswith(manual) else d).strip()
        d = f"{manual} {rest}".strip()
    else:
        d = d or tidy(official) or tidy(overview) or "No overview text in source."
    if n >= 1000:
        d += f" **{n:,} links.**"
    return d


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=date.today().isoformat())
    a = ap.parse_args()
    today = a.date
    descs = old_descriptions()
    areas, texts = fetch_all()
    rows, sizes, created, removed_total = [], [], [], 0
    for i, (slug, title, desc) in enumerate(areas, 1):
        overview, sections = parse(texts[slug])
        n, sections, removed = write_index(slug, title, sections, today)
        if removed:
            print(f"{slug}: {removed} duplicate URL entries in the source removed", file=sys.stderr)
        removed_total += removed
        if write_content(slug, title, overview, sections, today, n):
            created.append(slug)
        rows.append(f"| {i} | ✅ | {title} | [folder]({slug}/) | {describe(slug, descs.get(slug, ''), desc, overview, n)} |")
        sizes.append((slug, n, (ROOT / slug / "index.md").stat().st_size))
    gone = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "index.md").exists()
                  and p.name not in {s for s, _, _ in areas})
    total = len(areas)
    lst = [
        "# Salesforce Developer Documentation — Content List (Index)",
        "",
        f"Source: [`{LLMS}`]({LLMS}) (aggregated index, llmstxt.org standard)",
        f"Captured: 2026-10-24. Last refreshed: {today} with `scripts/refresh_from_llms.py` (all folders regenerated from the live source).",
        "",
        f"This is the authoritative index of all {total} product-specific `llms.txt` sections published under the Developer Documentation Portal. "
        "Each product has its own folder (`index.md` + `content.md`, full link list + short description) — see [README.md](README.md) for the folder format.",
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
    readme = re.sub(r"(?:even|including) `[^`]+`, (?:which alone is larger than the previous \d+ folders combined|the largest single index)\.",
                    f"including `{top[0][0]}`, the largest single index.", readme)
    if "scripts/refresh_from_llms.py" not in readme.split("## Format per product folder")[1].split("##")[0]:
        readme = readme.replace(
            "- `content.md` —",
            "- `scripts/refresh_from_llms.py` (repo root) — regenerates every `index.md`, the content list and README counts from the live `llms.txt`; keeps hand-written `content.md` prose.\n- `content.md` —", 1)
    readme = re.sub(r"Captured starting 2026-10-24\.[^\n]*", f"Captured starting 2026-10-24. Last refreshed {today} with [`scripts/refresh_from_llms.py`](scripts/refresh_from_llms.py).", readme)
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"areas: {total}; new folders: {', '.join(created) or 'none'}; no longer listed: {', '.join(gone) or 'none'}")
    print(f"pages: {sum(s[1] for s in sizes):,} unique links; duplicate URL entries removed: {removed_total:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
