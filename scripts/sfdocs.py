#!/usr/bin/env python3
"""Search this Salesforce docs catalog and fetch the official pages it points to.

Standard library only. Works offline for `search`, `areas` and `sections`;
`fetch` needs HTTPS access to developer.salesforce.com.

  python3 scripts/sfdocs.py search "place order api" [--area revenue-cloud] [--limit 10] [--json]
  python3 scripts/sfdocs.py areas
  python3 scripts/sfdocs.py sections industries-integrations
  python3 scripts/sfdocs.py fetch <url> [--max-chars 20000] [--refresh]

Search ranks the ~58k page links in every <area>/index.md by how many query words
appear in the page title, its section name, the URL path and the area name
(title hits weigh most). Use quotes for a multi-word query; `--area` takes a folder
name or a prefix of one (e.g. `industries` matches all five industries-* folders).

Fetched pages are cached under .cache/pages/ (git-ignored).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "pages"
LIST_FILE = ROOT / "salesforce-platform-docs-content-list.md"
ALLOWED_HOSTS = {"developer.salesforce.com"}
# Salesforce's bot protection answers 403 to a spoofed browser User-Agent sent without a
# real browser, but accepts plain tool agents. Try the stdlib default first, then curl's.
USER_AGENTS = (None, "curl/8.5.0")

ROW = re.compile(r"^\| (.+) \| (https?://\S+) \|$")
SECTION = re.compile(r"^## (.+?)(?: \(\d+ pages\))?$")
TOKEN = re.compile(r"[a-z0-9]+")
STOP = {"the", "a", "an", "of", "and", "or", "to", "for", "in", "on", "with", "how", "what", "is", "api"}


def tokens(text: str) -> list[str]:
    # split camelCase / PascalCase so "ProductCatalog" matches "product catalog"
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return TOKEN.findall(text.lower())


def load_entries(area_filter: str | None = None) -> list[dict]:
    entries = []
    for index in sorted(ROOT.glob("*/index.md")):
        area = index.parent.name
        if area_filter and not area.startswith(area_filter):
            continue
        section = ""
        for line in index.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                m = SECTION.match(line)
                section = m.group(1) if m else line[3:]
                continue
            m = ROW.match(line)
            if m and m.group(1) != "Page":
                entries.append({"area": area, "section": section,
                                "title": m.group(1).replace("\\|", "|").strip(), "url": m.group(2)})
    return entries


def score(entry: dict, qtokens: list[str], phrase: str) -> tuple[int, float]:
    title = set(tokens(entry["title"]))
    section = set(tokens(entry["section"]))
    path = set(tokens(urllib.parse.urlparse(entry["url"]).path))
    area = set(tokens(entry["area"]))
    matched, s = 0, 0.0
    for t in qtokens:
        w = 3.0 if t in title else 2.0 if t in section else 1.0 if t in path else 0.5 if t in area else 0.0
        if w:
            matched += 1
            s += w
    tl = entry["title"].lower()
    if phrase and phrase in tl:
        s += 4.0
        if tl == phrase:
            s += 4.0
    # prefer shorter, more specific titles on ties
    s -= len(title) * 0.01
    return matched, s


def cmd_search(a) -> int:
    q = [t for t in tokens(a.query) if t not in STOP] or tokens(a.query)
    if not q:
        print("empty query", file=sys.stderr)
        return 2
    phrase = " ".join(tokens(a.query))
    entries = load_entries(a.area)
    if not entries:
        print(f"no area matches '{a.area}' (see: sfdocs.py areas)", file=sys.stderr)
        return 2
    need = len(q) if a.all else max(1, (len(q) + 1) // 2)
    ranked = []
    for e in entries:
        m, s = score(e, q, phrase)
        if m >= need:
            ranked.append((m, s, e))
    ranked.sort(key=lambda r: (-r[0], -r[1], r[2]["url"]))
    top = ranked[: a.limit]
    if a.json:
        print(json.dumps([{**e, "matched": m, "score": round(s, 2)} for m, s, e in top], indent=2))
        return 0
    if not top:
        print(f"no results for '{a.query}'" + (f" in area '{a.area}'" if a.area else ""))
        return 1
    print(f"{len(ranked)} matches for '{a.query}' (showing {len(top)}; query words used: {' '.join(q)})\n")
    for i, (m, s, e) in enumerate(top, 1):
        print(f"{i:>2}. {e['title']}  [{e['area']} / {e['section']}]  ({m}/{len(q)} words)")
        print(f"    {e['url']}")
    return 0


def area_rows() -> list[tuple[str, str, str]]:
    rows = []
    for line in LIST_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| \d+ \| [^|]+ \| ([^|]+) \| \[folder\]\(([a-z0-9-]+)/\) \| (.*) \|$", line)
        if m:
            rows.append((m.group(2), m.group(1).strip(), m.group(3).strip()))
    return rows


def cmd_areas(a) -> int:
    counts = {}
    for e in load_entries():
        counts[e["area"]] = counts.get(e["area"], 0) + 1
    for slug, title, desc in area_rows():
        desc = re.sub(r"\s*\*\*[\d,]+ links\.\*\*", "", desc)
        print(f"{slug:<34} {counts.get(slug, 0):>6} pages  {title} — {desc}")
    return 0


def cmd_sections(a) -> int:
    path = ROOT / a.area / "index.md"
    if not path.exists():
        print(f"no folder '{a.area}' (see: sfdocs.py areas)", file=sys.stderr)
        return 2
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            print(line[3:])
    return 0


def http_get(url: str) -> tuple[str, str]:
    """Return (text, final_url) after redirects."""
    last = None
    for ua in USER_AGENTS:
        headers = {"Accept": "text/markdown, text/plain, */*"}
        if ua:
            headers["User-Agent"] = ua
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                return r.read().decode("utf-8", errors="replace"), r.geturl()
        except Exception as e:  # 403 or network error: try the next agent
            last = e
    try:  # last resort: a real headless browser, if Playwright is installed
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError(f"{last} (Playwright not installed for a browser fallback)")
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox"])
        r = b.new_page().goto(url, wait_until="domcontentloaded", timeout=120000)
        text = r.text() if r and r.status == 200 else None
        final = r.url if r else url
        b.close()
    if text is None:
        raise RuntimeError(f"{url}: browser fallback failed too ({last})")
    return text, final


def looks_html(text: str) -> bool:
    head = text.lstrip()[:200].lower()
    return head.startswith(("<!doctype", "<html")) or "<head" in head


def cmd_fetch(a) -> int:
    url = a.url.strip()
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or u.hostname not in ALLOWED_HOSTS:
        print(f"refusing {url}: only https://developer.salesforce.com pages are fetched", file=sys.stderr)
        return 2
    if u.path.endswith(".html"):  # the .md twin is clean Markdown
        url = url[: -len(".html")] + ".md"
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".md")
    if cached.exists() and not a.refresh:
        text, source = cached.read_text(encoding="utf-8"), "cache"
    else:
        try:
            text, final = http_get(url)
            # legacy atlas .htm links redirect to new .html pages; their .md twin is clean Markdown
            if looks_html(text) and urllib.parse.urlparse(final).path.endswith(".html"):
                url = final[: -len(".html")] + ".md"
                text, final = http_get(url)
        except Exception as e:
            print(f"FETCH FAILED for {url}: {e}\nDo not answer from this page; say the content was not verified.",
                  file=sys.stderr)
            return 1
        if len(text.strip()) < 40 or looks_html(text):
            print(f"FETCH RETURNED NO MARKDOWN for {url} (shell page or soft 404). Treat as unverified.",
                  file=sys.stderr)
            return 1
        cached.write_text(text, encoding="utf-8")
        source = "live"
    print(f"<!-- source: {url} ({source}) -->")
    if a.max_chars and len(text) > a.max_chars:
        print(text[: a.max_chars])
        print(f"\n<!-- truncated at {a.max_chars} of {len(text)} chars; rerun with --max-chars 0 for all -->")
    else:
        print(text)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="rank catalog pages for a query")
    s.add_argument("query")
    s.add_argument("--area", help="folder name or prefix, e.g. revenue-cloud, industries")
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--all", action="store_true", help="require every query word to match")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_search)
    sub.add_parser("areas", help="list the 54 areas with page counts").set_defaults(fn=cmd_areas)
    c = sub.add_parser("sections", help="list the sections of one area")
    c.add_argument("area")
    c.set_defaults(fn=cmd_sections)
    f = sub.add_parser("fetch", help="download one official page as Markdown (cached)")
    f.add_argument("url")
    f.add_argument("--max-chars", type=int, default=20000)
    f.add_argument("--refresh", action="store_true", help="ignore the cache")
    f.set_defaults(fn=cmd_fetch)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    import signal

    if hasattr(signal, "SIGPIPE"):  # quiet exit when piped into head
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
