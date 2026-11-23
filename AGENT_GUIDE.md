# Agent Guide

How an AI agent should use this catalog to ground Salesforce answers.

Adapted from the evidence rules in Salesforce's [`sf-pi` SF Docs agent guide](https://github.com/salesforce/sf-pi/blob/39ea83d9a699b084c1a1397693b72363e2371dce/extensions/sf-docs/AGENT_GUIDE.md) (Apache-2.0). That guide targets the `sf_docs` tool in the Pi coding agent. This one targets this catalog plus the Salesforce Docs MCP connector (`salesforce_docs_search`, `salesforce_docs_fetch`). The collection map and URL rules were checked against the connector on 2026-11-23.

## What this repo is, and is not

- `<product>/index.md` is a link map extracted from the official `llms-*.txt` files. Use it to find the product area and the exact page URL.
- `<product>/content.md` is a short orientation summary. It is not evidence; do not cite it.
- Evidence is the official page you actually fetched. This repo tells you where to look, not what is true.

## Retrieval workflow

1. **Classify the question.**
   - Implementation-sensitive (exact API behaviour, field, limit, release availability): fetch the page and cite it.
   - Orientation or broad explanation: a search excerpt can be enough; say that it is an excerpt.
   - Architecture choice: see [Architecture Center](#architecture-center-which-source).
2. **Connector first, when it is available.**
   - Set `collection` (`{source}/{area}`, with a slash) from the [collection map](#collection-map).
   - Use `search_mode="hybrid"` for literal tokens: API, class or field names, error strings, permission names.
   - Keep `limit` at 3–5; each result is large.
   - Fetch the 1–3 strongest results with the `documentPath` or `url` that search returned. Never build an id yourself.
3. **Use the catalog** when you know a page title (grep `*/index.md`), when the connector has no or thin coverage for an area, or to confirm which product area owns a topic.
4. **Fetching a catalog link.** Catalog links end in `.md`, and the connector rejects that form with *Document not found*. Replace `.md` with `.html` and retry once. If it still fails, read the official page with web access; for JS-heavy pages follow the `platform-docs-get` playbook.
5. **No readable official page?** Mark the statement *unverified*, give the best official URL, and ask for a link or docs access. Do not install or enable tools silently.

## Collection map

49 of the 54 catalog folders have a `developer/*` collection with the same name. Exceptions and thin areas:

| Catalog folder (links) | Connector coverage | Use instead |
| --- | --- | --- |
| `platform-apex` (2,881) | `developer/platform-apex`: 2 docs | `legacydeveloper/apexref` (Apex Reference), `legacydeveloper/apexcode` (Apex Developer Guide) |
| `platform-obj-meta-tool` (2,498) | none | `legacydeveloper/object_reference`, `legacydeveloper/api_meta`, `legacydeveloper/api_tooling` |
| `platform-field-ref` (2,712) | none | Closest: `legacydeveloper/object_reference` (fields per object); else the catalog link via web access |
| `product-docs` (12,977, legacy `.htm` links) | none under `developer/*` | The matching `legacydeveloper/*` area where one exists; else web access |
| `personalization` (614) | `developer/personalization`: 95 docs | Connector first, then the catalog link via web access |
| `metadata-coverage` (42), `my-trust-center` (3) | none | Catalog link via web access |

Not in this catalog, connector only:

- `admin/*`: Salesforce Help (setup, configuration, release notes), 15 areas such as `admin/ind`, `admin/platform` and `admin/release-notes`.
- `architect/*`: Architecture Center (`decision-guides`, `well-architected`, `fundamentals`, `reference-diagrams`, `resources`).
- `mulesoft/*` and `tableau/*`.

The catalog's `diagrams/` folder holds data-model diagrams (`developer/diagrams`), not Architecture Center reference diagrams.

## Telco and Industries routing

| Need | Start with |
| --- | --- |
| TM Forum Open APIs on Communications Cloud: which APIs, versions, conformance, access method | `developer/industries-integrations`, page *Get Started with Industry API*; catalog `industries-integrations/` |
| Industries REST APIs: CPQ, EPC, Digital Commerce | `developer/industries`; catalog `industries/` |
| Revenue Cloud: Revenue Management, Billing, Contracts, Place Order, CPQ | `developer/revenue-cloud`; catalog `revenue-cloud/` |
| Industries setup and admin how-to | `admin/ind` (inferred from the name; confirm with the `collection` field of an unfiltered search) |
| Standard object and field facts | `legacydeveloper/object_reference` |
| When a feature became available | `admin/release-notes` |

Do not quote TMF API numbers, versions or endpoints from memory or from this table. Fetch the page and cite it; these pages change between releases.

## Evidence rules

- **Cite the fetched page**: the `url` the connector returned, or the official URL you read. Not a search snippet, a `content.md` summary or a remembered link.
- **List what you fetched** for implementation-sensitive answers: title and URL per source, and whether the content was partial.
- **Keep evidence types apart.** Docs establish documented product behaviour. Org metadata and SOQL establish what a specific org has. Repository source and ADRs establish an existing design. Architecture guidance informs a design; it proves nothing about a given org.
- **Documented availability is not entitlement.** Edition and permission metadata on a doc page says where a feature can exist, not what a customer has licensed.
- **Preserve constraints.** Keep the requested product, release, locale and document type. If results don't meet them, report an evidence gap instead of answering from a near miss.
- **Release questions need release-note evidence** from `admin/release-notes`. A current page that carries a release number is not a release note.
- **Help article URLs.** The connector indexes Help articles as `…/articleView?id=<article>&release=<n>&type=5`. A pasted Help URL without `release=` returns *Document not found*. Search `admin/*` with the article's title words and fetch the URL that search returns.
- **Route on intent, not keywords.** Use `architect/*` for explicit decision-guide, Well-Architected or reference-diagram questions, not whenever the word "architecture" appears.
- **Stop early.** Start with one primary source and stop when it settles the question. Avoid repeated near-identical searches; widen only for a distinct open gap. A long page returned truncated is not a failed fetch.
- **Absence is not evidence.** A page missing from this catalog or the connector does not prove a feature doesn't exist. Check snapshot dates: catalog in [README](README.md), connector in `last_indexed` of `collection://list`.

## Architecture Center: which source

Use `architect/*` for material solution design or an architecture review. Choose the smallest source that answers the question.

| Need | Start with |
| --- | --- |
| Choose between viable approaches | `architect/decision-guides` |
| Understand platform behaviour or constraints | `architect/fundamentals` |
| Weigh cross-cutting quality trade-offs | The relevant pillar in `architect/well-architected` |
| Review a concrete design for risks | Patterns and anti-patterns: search `architect/*` (the connector has no separate patterns area) |
| Communicate a solution or data model | `architect/reference-diagrams`; examples are not evidence of an org's actual architecture |
| Produce a policy, plan or review artifact | `architect/resources` (templates), only when that deliverable is needed |

Skip the lookup for routine edits or settled designs with no new architectural risk.

## Keeping this guide current

Re-check the collection map after `scripts/refresh_from_llms.py` adds or renames folders, or when the connector's `collection://list` changes: compare folder names with `developer/*` collection names and update the exceptions table.
