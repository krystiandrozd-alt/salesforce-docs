# Salesforce Developer Documentation — Content Catalog

A per-product content catalog built from Salesforce's aggregated [`llms.txt`](https://developer.salesforce.com/docs/llms.txt) index (the `llmstxt.org`-standard list of all 49 product-specific documentation sections under `developer.salesforce.com`).

Designed to be read by an AI assistant (Claude or otherwise) as grounding material: each finished product gets its own folder with an `index.md` (complete page-by-page link list, extracted programmatically from the live source) and a `content.md` (a short synthesis written independently from the source, with citations — not copied prose).

## Status: 17 of 49 products done

See [`salesforce-platform-docs-content-list.md`](salesforce-platform-docs-content-list.md) for the full 49-row table with ✅/⬜ status and folder links — that file is the authoritative index. Quick summary:

**Done (17):** [agentforce-conversation-client](agentforce-conversation-client/), [agentforce-operations](agentforce-operations/), [agentforce-partners](agentforce-partners/), [analytics](analytics/), [api-catalog](api-catalog/), [backup-recover-api](backup-recover-api/), [bot-api](bot-api/), [cms](cms/), [code-analyzer](code-analyzer/), [commerce-cloud](commerce-cloud/), [connect-rest](connect-rest/), [data-ae](data-ae/), [data-cloud](data-cloud/), [dataloader](dataloader/), [diagrams](diagrams/), [einstein-personalization](einstein-personalization/), [lwc](lwc/)

**Pending (32):** einstein-vision-language, event-bus, genai, graphql-api, headless-experience-layer, headless-three-sixty, hosted-mcp-servers, industries-core, industries-integrations, industries, lightning-base-components, lightning-type-systems, lwr-node, marketing-cloud-mobilepush, marketing-cloud, metadata-coverage, mobile-sdk, multi-framework, my-trust-center, pardot, personalization, platform-field-ref, platform-pkg-exchange, platform, revenue-cloud, sales-cloud, salesforce-functions, salesforce-slack-sdk, salesforcedx, security, service-cloud, product-docs

> Note: `headless-experience-layer`, `headless-three-sixty`, `hosted-mcp-servers`, and `multi-framework` are already covered in depth in the companion repo [headless-toolkit](https://github.com/krystiandrozd-alt/headless-toolkit) (restructured per-area with grounded content, plus launch-announcement blogs and the AIforce/Claudeforce brand hierarchy). When those four get their turn here, treat `headless-toolkit` as the primary source and keep this repo's version as a lighter per-`llms.txt` link catalog rather than duplicating that deeper work.

## Format per product folder

- `index.md` — every page link from that product's `llms-{product}.txt`, extracted programmatically (not hand-copied) to make even the largest indexes (several have 1,000+ links) tractable and accurate.
- `content.md` — a short synthesis from the index file's own overview text, with a section breakdown and a link back to `index.md` for the full list. Citations given per claim; no large verbatim copying (copyright).

Some products are enormous: Commerce Cloud alone has **6,844** page links, Data Cloud **4,282**, Analytics **1,003**, LWC **829**. These are reproduced in full per explicit instruction, not condensed.

## Source

All entries trace back to `developer.salesforce.com/docs/llms-*.txt` and the pages they link to. Captured starting 2026-10-24.
