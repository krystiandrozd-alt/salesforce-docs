# Salesforce Developer Documentation — Content Catalog

A per-product content catalog built from Salesforce's aggregated [`llms.txt`](https://developer.salesforce.com/docs/llms.txt) index (the `llmstxt.org`-standard list of all 49 product-specific documentation sections under `developer.salesforce.com`).

Designed to be read by an AI assistant (Claude or otherwise) as grounding material: each finished product gets its own folder with an `index.md` (complete page-by-page link list, extracted programmatically from the live source) and a `content.md` (a short synthesis written independently from the source, with citations — not copied prose).

## Status: 49 of 49 products done

Every product-specific `llms-*.txt` section now has its own folder here. See [`salesforce-platform-docs-content-list.md`](salesforce-platform-docs-content-list.md) for the full 49-row table with links — that file is the authoritative index.

> Note: `headless-experience-layer`, `headless-three-sixty`, `hosted-mcp-servers`, and `multi-framework` are also covered in much greater depth in the companion repo [headless-toolkit](https://github.com/krystiandrozd-alt/headless-toolkit) (restructured per-area with grounded content, launch-announcement blogs, and the AIforce/Claudeforce brand hierarchy). Treat `headless-toolkit` as the primary source for those four; the folders here are the lighter per-`llms.txt` link catalog, kept for completeness rather than duplicating that deeper work.

## Format per product folder

- `index.md` — every page link from that product's `llms-{product}.txt`, extracted programmatically (not hand-copied) to make even the largest indexes tractable and accurate.
- `content.md` — a short synthesis from the index file's own overview text, with a section breakdown and a link back to `index.md` for the full list. Citations given per claim; no large verbatim copying (copyright).

## The ten largest indexes (verified via GitHub API, by file size)

| Product | Links | `index.md` size |
|---|---|---|
| [product-docs](product-docs/) | 23,053 | 3.79 MB |
| [commerce-cloud](commerce-cloud/) | 6,844 | 919 KB |
| [data-cloud](data-cloud/) | 4,282 | 624 KB |
| [industries](industries/) | 4,010 | 604 KB |
| [platform-field-ref](platform-field-ref/) | 2,712 | 455 KB |
| [platform](platform/) | 2,872 | 407 KB |
| [service-cloud](service-cloud/) | 2,585 | 382 KB |
| [marketing-cloud](marketing-cloud/) | 2,174 | 310 KB |
| [revenue-cloud](revenue-cloud/) | 1,870 | 278 KB |
| [analytics](analytics/) | 1,003 | 135 KB |

These are reproduced **in full**, not condensed, per explicit instruction — even `product-docs`, which alone is larger than the previous 48 folders combined.

## Source

All entries trace back to `developer.salesforce.com/docs/llms-*.txt` and the pages they link to. Captured starting 2026-10-24.
