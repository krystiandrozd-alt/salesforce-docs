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
| [product-docs](product-docs/) | 12,977 | 1.87 MB |
| [commerce-cloud](commerce-cloud/) | 6,864 | 900 KB |
| [data-cloud](data-cloud/) | 4,322 | 615 KB |
| [industries](industries/) | 4,021 | 592 KB |
| [platform-field-ref](platform-field-ref/) | 2,712 | 444 KB |
| [platform-apex](platform-apex/) | 2,881 | 442 KB |
| [platform](platform/) | 2,882 | 399 KB |
| [service-cloud](service-cloud/) | 2,586 | 373 KB |
| [platform-obj-meta-tool](platform-obj-meta-tool/) | 2,498 | 351 KB |
| [marketing-cloud](marketing-cloud/) | 2,177 | 303 KB |

These are reproduced **in full**, not condensed, per explicit instruction — including `product-docs`, the largest single index.

## Roadmap

The link catalog covers every section currently listed in `llms.txt`. Later work stays inside that shape:

1. **Stay current with the live index.** Re-run [`scripts/refresh_from_llms.py`](scripts/refresh_from_llms.py) when Salesforce adds or retires a product section. A new section gets its own folder. A section that leaves `llms.txt` stays in the tree as an archived snapshot.
2. **Deepen the ten largest syntheses.** Each `content.md` is a short overview taken from that index's own overview text. The next writing pass is a cited synthesis of the ten largest indexes: `product-docs`, `commerce-cloud`, `data-cloud`, `industries`, `platform-field-ref`, `platform-apex`, `platform`, `service-cloud`, `platform-obj-meta-tool`, and `marketing-cloud`. Page text stays on the official docs.
3. **Fill empty product descriptions.** Connect REST, Data Loader, GraphQL API, Platform, and Platform Package Exchange have no overview text in the source index. Those rows pick up the official description when Salesforce publishes one.
4. **Keep the headless areas as link catalogs.** Deeper writing for `headless-experience-layer`, `headless-three-sixty`, `hosted-mcp-servers`, and `multi-framework` lives in [headless-toolkit](https://github.com/krystiandrozd-alt/headless-toolkit).

## Source

All entries trace back to `developer.salesforce.com/docs/llms-*.txt` and the pages they link to. Captured starting 2026-10-24. Last refreshed 2026-11-06 with [`scripts/refresh_from_llms.py`](scripts/refresh_from_llms.py).
