---
name: salesforce-docs
description: "Ground answers in official Salesforce developer documentation using this repo's catalog of ~58k page links (54 areas from developer.salesforce.com/docs/llms.txt). Search the local index for the exact page, fetch it as Markdown, answer with the URL. TRIGGER when: a question needs facts about Salesforce APIs, objects, fields, Apex classes, Metadata API, LWC, Agentforce, Data 360, Revenue Cloud / CPQ / Billing, Industries / Communications Cloud (EPC, CPQ, Digital Commerce, Advanced Orders, TM Forum Open APIs), Service/Sales/Marketing/Commerce Cloud, or any 'what is the exact name / endpoint / field' check before something goes to a client. DO NOT TRIGGER when: the task is editing this repo's catalog itself, or the question is only about help.salesforce.com setup articles (use platform-docs-get for those)."
---

# salesforce-docs

Find the exact official page in the local catalog, read it, then answer. The catalog
holds links, not page text, so a search result alone is never evidence.

All commands run from the repo root:

```bash
python3 scripts/sfdocs.py search "<query>" [--area <folder or prefix>] [--limit 10] [--all]
python3 scripts/sfdocs.py fetch <url> [--max-chars 20000]
python3 scripts/sfdocs.py areas
python3 scripts/sfdocs.py sections <area>
```

## Workflow

1. **Name the target.** Pull the exact identifier out of the question: object, field,
   class, endpoint, TMF API number, feature name.
2. **Search the catalog.** Use 2–4 distinctive words. Narrow with `--area` when the
   product is known (table below). If nothing fits, try synonyms, drop a word, or run
   `sections <area>` to browse.
3. **Pick 1–3 URLs** whose title matches the concept, not a broad landing page.
   Prefer the newer `/docs/<product>/...md` page over a legacy `atlas.en-us` duplicate.
4. **Fetch each page** with `fetch`. It returns Markdown, follows legacy atlas
   redirects, and caches under `.cache/pages/`. Raise `--max-chars` (0 = all) when
   the answer is further down the page.
5. **Check the page.** It counts as evidence only if the exact identifier or concept
   appears in the fetched text. If not, follow 1–3 links inside the page (they are
   relative, prefix `https://developer.salesforce.com`) or search again.
6. **Answer with citations.** For each claim: page title and full URL. Say plainly if
   a fetch failed or the page did not confirm the point.

## Hard rules

- Never state an object, field, API, endpoint, TMF API number, release name or
  licence detail that is not on a fetched page. If unconfirmed, say "not verified".
- `FETCH FAILED` or `NO MARKDOWN` means no evidence: report the URL found, mark the
  content unverified, do not fill the gap from memory.
- Default to the latest API version unless the user names one (Salesforce's own
  instruction to LLM agents in `llms.txt`).
- Separate what the page says from your inference, and label the inference.
- Only `https://developer.salesforce.com` is fetched. For help.salesforce.com articles
  use the `platform-docs-get` skill.

## Where to look (`--area`)

| Topic | Area folder(s) |
|---|---|
| Comms Cloud TM Forum Open APIs (TMF620, TMF622, TMF641...) | `industries-integrations` |
| Industries CPQ, EPC, Digital Commerce (CME), Advanced Orders | `industries` |
| Other Industries clouds | `industries-core`, `industries-fsc-ins`, `industries-health`, `industries-mfg-auto` (or `--area industries` for all) |
| Revenue Cloud / Revenue Management, Salesforce CPQ, Billing, Contracts, Place Order | `revenue-cloud` |
| Standard objects and fields | `platform-obj-meta-tool`, `platform-field-ref`, `product-docs` |
| Apex classes and methods | `platform-apex`, `product-docs` |
| REST, SOAP, Metadata, Tooling, Bulk APIs; platform guides | `platform`, `product-docs` |
| Connect REST, GraphQL, Pub/Sub, platform events, CDC | `connect-rest`, `graphql-api`, `event-bus` |
| Agentforce, Agent API, Models API, Agent Script, Testing API | `genai`, `agentforce-*` |
| Hosted MCP servers, API Catalog | `hosted-mcp-servers`, `api-catalog` |
| Data 360 (Data Cloud) | `data-cloud`, `data-ae` |
| LWC, base components, Lightning Types | `lwc`, `lightning-base-components`, `lightning-type-systems` |
| Service / Sales / Marketing / Commerce Cloud | `service-cloud`, `sales-cloud`, `marketing-cloud`, `commerce-cloud` |
| CLI, VS Code, DX | `salesforcedx`, `metadata-coverage` |

Run `python3 scripts/sfdocs.py areas` for all 54 areas with descriptions.

## Example

Question: "Does Communications Cloud support TMF622 Product Ordering, and which version?"

```bash
python3 scripts/sfdocs.py search "TMF622 product ordering" --area industries-integrations --limit 5
python3 scripts/sfdocs.py fetch https://developer.salesforce.com/docs/industries/communications/guide/<page>.md
```

Answer from the fetched text, quote the version exactly as the page states it, and
cite the URL.

## Keeping the catalog fresh

`python3 scripts/refresh_from_llms.py` regenerates every `index.md` from the live
`llms.txt` (standard library; Playwright only as a fallback if HTTPS is refused).
