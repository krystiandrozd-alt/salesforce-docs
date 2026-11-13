# Salesforce Developer Documentation — Content Catalog

A per-product content catalog built from Salesforce's aggregated [`llms.txt`](https://developer.salesforce.com/docs/llms.txt) index (the `llmstxt.org`-standard list of all 54 product-specific documentation sections under `developer.salesforce.com`).

Designed to be read by an AI assistant (Claude or otherwise) as grounding material: each finished product gets its own folder with an `index.md` (complete page-by-page link list, extracted programmatically from the live source) and a `content.md` (a short synthesis written independently from the source, with citations — not copied prose).

## Status: 54 of 54 products done

Every product-specific `llms-*.txt` section now has its own folder here. See [`salesforce-platform-docs-content-list.md`](salesforce-platform-docs-content-list.md) for the full 54-row table with links — that file is the authoritative index.

> Note: `headless-experience-layer`, `headless-three-sixty`, `hosted-mcp-servers`, and `multi-framework` are also covered in much greater depth in the companion repo [headless-toolkit](https://github.com/krystiandrozd-alt/headless-toolkit) (restructured per-area with grounded content, launch-announcement blogs, and the AIforce/Claudeforce brand hierarchy). Treat `headless-toolkit` as the primary source for those four; the folders here are the lighter per-`llms.txt` link catalog, kept for completeness rather than duplicating that deeper work.

## Format per product folder

- `index.md` — every page link from that product's `llms-{product}.txt`, extracted programmatically (not hand-copied) to make even the largest indexes tractable and accurate.
- `scripts/refresh_from_llms.py` (repo root) — regenerates every `index.md`, the content list and README counts from the live `llms.txt`; keeps hand-written `content.md` prose.
- `content.md` — a short synthesis from the index file's own overview text, with a section breakdown and a link back to `index.md` for the full list. Citations given per claim; no large verbatim copying (copyright).

## The ten largest indexes (by `index.md` size, from the refresh script)

| Product | Links | `index.md` size |
|---|---|---|
| [product-docs](product-docs/) | 12,979 | 1.87 MB |
| [commerce-cloud](commerce-cloud/) | 6,878 | 902 KB |
| [data-cloud](data-cloud/) | 4,329 | 616 KB |
| [industries](industries/) | 4,021 | 592 KB |
| [platform-field-ref](platform-field-ref/) | 2,712 | 444 KB |
| [platform-apex](platform-apex/) | 2,879 | 441 KB |
| [platform](platform/) | 2,882 | 399 KB |
| [service-cloud](service-cloud/) | 2,586 | 373 KB |
| [platform-obj-meta-tool](platform-obj-meta-tool/) | 2,576 | 365 KB |
| [marketing-cloud](marketing-cloud/) | 2,181 | 303 KB |

These are reproduced **in full**, not condensed, per explicit instruction — including `product-docs`, the largest single index.

## Using it with Claude (or any agent)

`scripts/sfdocs.py` turns the catalog into a working lookup tool (standard library only):

```bash
python3 scripts/sfdocs.py search "TMF622 product ordering" --area industries-integrations
python3 scripts/sfdocs.py fetch https://developer.salesforce.com/docs/industries/communications/guide/TMF622.md
python3 scripts/sfdocs.py areas
python3 scripts/sfdocs.py sections revenue-cloud
```

- `search` ranks all page links by title, section, URL path and area (offline, about 0.3 s).
- `fetch` downloads the official page as Markdown, follows legacy `atlas.en-us` redirects to the new `.md` page, and caches it in `.cache/pages/`.
- The Claude Code skill [`.claude/skills/salesforce-docs`](.claude/skills/salesforce-docs/SKILL.md) tells Claude when to use it and how to cite: search, fetch, answer only from fetched text. [`CLAUDE.md`](CLAUDE.md) points every session in this repo to it.

## MCP server

[`scripts/sfdocs_mcp.py`](scripts/sfdocs_mcp.py) serves the same functions over the Model Context Protocol (stdio transport, standard library only, so no `pip install`). Tools:

| Tool | What it does |
|---|---|
| `search_docs(query, area?, limit?, require_all?)` | Ranked page search over the catalog (offline) |
| `fetch_page(url, offset?, max_chars?, refresh?)` | Official page as Markdown; long pages come in windows, the text ends with the next `offset` |
| `list_areas()` | The 54 areas with page counts and descriptions |
| `list_sections(area)` | The guides inside one area |

The server also sends instructions to the client: search, then fetch, then answer only from fetched text with the URL.

**Claude Code, inside this repo:** [`.mcp.json`](.mcp.json) registers it automatically; approve it on the first prompt.

**Claude Code, in every project** (use the absolute path of your clone):

```bash
claude mcp add salesforce-docs --scope user -- python3 /ABSOLUTE/PATH/salesforce-docs/scripts/sfdocs_mcp.py
```

**Claude Desktop:** add this to `claude_desktop_config.json` (Settings, Developer, Edit Config) and restart. On Windows use `python` and a path such as `C:\\Users\\you\\salesforce-docs\\scripts\\sfdocs_mcp.py`.

```json
{
  "mcpServers": {
    "salesforce-docs": {
      "command": "python3",
      "args": ["/ABSOLUTE/PATH/salesforce-docs/scripts/sfdocs_mcp.py"]
    }
  }
}
```

Requirements: Python 3 (tested on 3.13) and HTTPS access to `developer.salesforce.com` for `fetch_page`. Search works offline. Fetched pages are cached in `.cache/pages/`. After `refresh_from_llms.py`, restart the server so it reloads the index.

## Source

All entries trace back to `developer.salesforce.com/docs/llms-*.txt` and the pages they link to. Captured starting 2026-10-24. Last refreshed 2026-11-12 with [`scripts/refresh_from_llms.py`](scripts/refresh_from_llms.py).
