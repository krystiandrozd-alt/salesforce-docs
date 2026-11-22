# Claude Code implementation prompt — Salesforce EU Pricing & Licensing Knowledge Graph

## Mission

Implement a **working, source-grounded and version-controlled licensing knowledge graph** in the existing repository:

Repository: https://github.com/krystiandrozd-alt/salesforce-docs  
Working namespaces: pricing-intelligence/ for canonical commercial data and calculations; solution-intelligence/ for process/capability relationships and adapters.  
Authoritative public index: https://www.salesforce.com/eu/pricing/  
Target region: EU; capture date: current run date.  
Starting artifacts:
- pricing-intelligence/README.md
- pricing-intelligence/data/seed-eu-2026-11-22.yaml
- solution-intelligence/source-manifest.yaml
- solution-intelligence/reference-registry.yaml
- solution-intelligence/docs/capability-commercial-contract.md
- solution-intelligence/prompts/resolve-process-commercial.md

Do **not** replace this with a long pricing report, decorative graph image, generic sales brochure, or unverified SKU database. Implement the schema, curated claims, source discovery, queries, tests, and coverage reporting.

## Non-negotiable rules

1. Inspect existing repo contents and read the blueprint and seed BEFORE changing anything. Preserve the current developer documentation catalog and unrelated files.
2. Use only public official Salesforce sources for public-price assertions. The pricing hub provides links, NOT a complete authoritative SKU book. Traverse product pricing pages and their directly linked detailed pricing pages, official rate cards and pricing guides. Stop when access is prohibited; report the gap.
3. A commercial offer/edition is not the same as a technical Salesforce UserLicense, permission set license, Salesforce feature, organization-level entitlement or orderable SKU. Create those as separate entity types.
4. Never fabricate price, SKU, entitlement, included feature, conversion rate, contract term, availability, required base license, or billing unit. Unknown != false.
5. Record exact source URL and page section for EVERY factual observation and relation. Preserve capture time, original currency, region, amount qualifier (FROM, STARTING_FROM, FIXED_PUBLIC, CONTACT_SALES), display unit, billing cadence and text ambiguity. Do not convert currencies without a sourced FX rate.
6. Treat the following relations as distinct: INCLUDES, AVAILABLE_FOR_PURCHASE, REQUIRES, OPTIONALLY_REQUIRES, ELIGIBLE_WITH, REPLACES, RENAMED_FROM, BILLED_BY, USES_CREDIT_POOL. A feature shown as “available for purchase” must not become an included entitlement.
7. Pricing is temporal. Append new observations, preserve older data, compute diffs, and flag conflicting sources; do not silently overwrite. Keep CONTROVERSIAL or CONFLICTED facts out of firm quotes.
8. Price shown per user/month but billed annually is NOT the same as a monthly cancelable subscription. Model the display unit and payment cadence separately.
9. Only verified data may be surfaced as verified. Derivations must expose their input facts and carry INFERRED status.
10. Never commit credentials, customer-specific Order Forms, negotiated discounts or proprietary private quote data. Add a secure separate data layer only if explicitly authorized.
11. Respect website terms, rate limits and copyrights. Summarize extracted facts with links; do not bulk redistribute protected material.
12. Do not claim complete coverage, functioning code, correct pricing or successful tests until objectively checked.

## Objectives

A. Answer **what can be purchased**: products, families, current/legacy editions, bundles, add-ons and availability.
B. Answer **how it is licensed**: technical license vs commercial offer, access class, required edition and included rights (ONLY when verified).
C. Answer **how it is billed**: per user, org, member, login, action, Flex Credit, profile, conversation, Mule Credit, percentage of qualifying spend or contract.
D. Answer **what is included vs separately purchased**: Slack, Tableau, Agentforce, Data 360, Marketing Cloud, support plans and industry BSS suites.
E. Answer **what changed**: new/renamed/removed products, updated price, metric, currency, included allowance, support level or dependency.
F. Return supporting evidence and uncertainty for every answer.
G. Resolve a designed process, capability or functional skill to implementation → exact technical feature → required entitlement/license → providing edition/package/add-on → billing metric, rate and allowance, with source-backed relationships.
H. Reverse this lookup to show which functional skills, capabilities and process steps are affected by an offer, entitlement, rate or source change.

## Process and functional-skill integration

Read the [capability and commercial contract](../../solution-intelligence/docs/capability-commercial-contract.md) and [reference registry](../../solution-intelligence/reference-registry.yaml) before defining the bridge. The contract owns bridge entity types, relation direction, applicability, query output and acceptance cases. Existing commercial entities retain their IDs and ownership here. Source references in the registry are navigation pointers; claim records must cite the exact supporting source content.

Distinguish runtime functional skills from delivery/authoring skills and commercial packages from managed packages. Use Headless Toolkit to discover functional skills and implementation patterns, SF Docs to resolve exact technical features/generations, and Pricing Intelligence to establish commercial requirements. Semantic matching finds candidates; it must not manufacture licensing edges. Preserve one-to-many/many-to-many mappings, `ALL_OF` / `ANY_OF` prerequisites and alternative buying models.

Implement forward process-to-commercial resolution and reverse impact queries over typed, evidenced relations. Return coverage for every requested capability, including unmapped ones. Required rights, already-owned entitlements and incremental purchases are separate views. Deduplicate shared entitlements and allowances by owner, environment, pool and period. A skill/tool invocation is not automatically a billed action.

Keep the bridge request/result envelope outside the existing calculator scenario. Discover valid calculator meter IDs and create explicit mappings; preserve its current input contract. Unknown eligibility, price, allowance scope or meter blocks the affected conclusion and is never zero. The goal is an executable resolver plus source evidence; this prompt's existence does not establish completion.

## Build stages

### Stage 0 — repo and evidence inventory

- Enumerate existing repo structure, read current blueprint and YAML seed, inspect relevant earlier Salesforce licensing artifacts if present; do not assume they are authoritative.
- Crawl/inspect the EU pricing hub and enumerate ALL product-by-role and industry links.
- Produce data/sources.yaml with source URL, family, title, discovery URL, HTTP/retrieval status, last checked, source type, applicability, and last known changes.
- Build docs/coverage.md with discovered, ingested, “Contact Sales”, blocked, needs review, and not yet inspected counts.
- Show a compact, grounded inventory with actual links before claiming scope completion.

### Stage 1 — executable schema

Implement schema/graph.schema.json (JSON Schema 2020-12 or equivalent Pydantic model) for:
- product_family
- product
- offer / edition / bundle / add-on / credit pack
- SKU (only when publicly confirmed)
- technical_license and access_entitlement
- capability
- purchasing_model
- pricing_metric
- price_observation
- entitlement_allowance
- graph_relationship / sourced_claim
- source_snapshot
- conflict
- customer_contract_override (schema only, not populated)

Add process, process_step, functional_skill, delivery_skill, implementation_option, product_variant, technical_feature, permission_requirement, surface and requirement_group bridge entities as defined in the solution contract. Reference existing capability, offer, entitlement, license, metric, allowance, claim and source IDs instead of copying commercial entities. Validate edge endpoint types and referential integrity across namespaces.

Include:
- stable IDs and aliases; different IDs for editions when names change meaning
- temporal fields observed_at, effective_from, effective_to when known
- availability and geography qualifiers
- facts status: SOURCE_VERIFIED, INFERRED, UNKNOWN, CONFLICTED, RETIRED
- source and section reference per assertion
- unit_quantity + denomination + currency + displayed period + billing cadence
- raw-to-normalized traceability and validation errors
- source observation hashes if implementable

**Storage decision:** start with YAML/JSON in Git and a simple query/index layer. Do not add Neo4j or a remote database merely to claim a “graph”; an export to a real graph database can be a later adapter.

### Stage 2 — discovery, normalization and change detection

Implement scripts/discover.py, scripts/ingest.py, scripts/validate.py, scripts/query.py (or equivalent clean CLI). Recommended dependencies: Python 3.12, PyYAML, jsonschema, requests + BeautifulSoup where legally permitted. Make reproducible and easy to run locally.

- Fetch the public hub; extract product/industry links and canonicalize URLs while preserving locale.
- Traverse linked official price pages and directly referenced detailed rate/pricing pages at bounded depth, with domain allowlist, timeouts, retries, respectful rate limiting and deduplication.
- A published price card is evidence of a price **observation**, not proof of an SKU. If parsing fields is unreliable, add the page to a manual-review queue rather than guessing.
- Parse a price only when amount, currency and unit can be confidently attributed to the SAME offer.
- Explicitly handle contact-sales/no-price entries, multiple currencies on same HTML page, edition comparison tables and package quantities.
- Parse relationship cues such as “included”, “available for purchase”, “requires”, “from”, “billed annually” and “per org” without overinterpreting marketing copy.
- Ingest with idempotent keys, keep older observations, and emit a reviewable diff before promotion to SOURCE_VERIFIED.
- Never parse missing checkmark/icons from plain-text empty cells as false. If feature table indicators are not machine-readable, tag UNKNOWN and request visual/manual validation.

### Stage 3 — first graph and query interface

Implement a deterministic normalized graph exporter with nodes and directed typed edges (JSON export plus Mermaid output). It must support these commands or equivalent:

- list offers grouped by family and role/industry
- show offer with price metric, source and valid-at date
- compare two edition inclusions with source evidence
- explain bundle/optional dependency paths
- flag products that require commercial confirmation
- show all unresolved price observations or unit conflicts
- diff two capture dates

Treat the provided historical partial YAML seed as candidate claims; validate their structure and current applicability before promoting individual assertions, then expand through source-backed discoveries.

Also support:
- resolve a process/capability/functional skill to applicable license and package alternatives with complete evidence paths
- show included versus separately purchased components and all required dependency groups
- show subscription and consumption metrics without treating unsupported charges as free
- find impacted skills, capabilities, processes and BOM lines when a source, offer or rate changes
- return partial/unmapped coverage, conflicts, stale claims and customer-applicability gaps

### Stage 4 — proof, tests, handoff

Create automated tests, fixture pages, a runbook and a sample query report. Include tests that deliberately fail for these cases:
- Slack “included” and “available for purchase” swapped
- two differently metered products treated as the same charge
- USD values re-labelled EUR
- monthly displayed price interpreted as monthly contract
- invented SKU or guessed missing feature checkmark
- price observation without source URL/section/time
- stale price overwrites a newer value without audit trail
- Marketing Intelligence overview per-user vs detailed per-org conflict silently resolved
- same Starter Suite counted twice when it appears on Sales, Service and Marketing pages
- B2B BSS Suite org/year treated as a user license
- functional runtime skill confused with a developer/delivery skill
- managed-package and core product variants joined by a similar feature name
- `ALL_OF` / `ANY_OF` license prerequisites flattened into a mandatory purchase list
- shared allowance deducted once per capability or applied across an unverified pool/reset period
- one skill invocation assumed to equal one metered action
- missing customer entitlement evidence treated as owned or unowned
- a dangling reference, wrong edge endpoint, dependency cycle or missing required condition silently accepted
- a changed commercial claim fails to identify affected process/capability rows

Cover all [bridge acceptance cases](../../solution-intelligence/docs/capability-commercial-contract.md#acceptance-cases), including deterministic replay. Use synthetic fixtures for resolver behavior and separately verified live sources for factual claims.

Do not equate a passed unit test with truth of an external price; document which claims received independent source review.

## Live evidence cases that MUST be tested

1. Sales Core has a public EU per-user price and lists Slack Business+ and Tableau Next as included. Source: https://www.salesforce.com/eu/sales/pricing/
2. Communications Cloud shows per-user Growth/Advanced and a separate B2B BSS Suite with starting org/year pricing. Source: https://www.salesforce.com/eu/communications/pricing/
3. Agentforce shows per-credit, per-conversation, and user-license options with different conditions. Source: https://www.salesforce.com/eu/agentforce/pricing/
4. Data 360 offers Flex Credit and Profiles/Enterprise Profiles paths, with other actions potentially consuming separate credits. Source: https://www.salesforce.com/eu/data/pricing/
5. Marketing Intelligence contains a source disagreement: marketing overview displays EUR 10,000/user/month while detailed marketing analytics page displays EUR 10,000/org/month. Preserve both as CONFLICTED and exclude from calculation. Sources:
   - https://www.salesforce.com/eu/marketing/pricing/
   - https://www.salesforce.com/eu/marketing/analytics/pricing/
6. Page changes and source retrieval timestamps may differ: do not claim the website “last updated” date without evidence.

## Deliverables required in this repository

1. An executable schema and validation with no invalid curated seed data.
2. Source registry covering every role/industry index entry on the current EU pricing hub.
3. Normalized nodes, edges and observational price records with evidence.
4. Scripts for discovery, validation, query and temporal diff; document exact invocations.
5. Markdown product/edition comparison views generated from structured facts, not separately maintained prose tables.
6. Conflict register, source-status coverage report, machine-readable validation output.
7. Automated tests for all guardrails above.
8. A clear README with example commands, limitations, and explicit remaining work.
9. A sample query output explaining at least five cross-product questions with traceable source URL/section.
10. A PR containing code, tests, data, and a factual completion summary. Do not merge without review.
11. A process/capability-to-commercial resolver and reverse impact query with stable IDs, source snapshots, per-edge evidence, explicit unknowns and a complete output row for every requested requirement.
12. Reference integrity checks and an end-to-end telco example satisfying the first implementation slice in the solution contract; report implemented behavior separately from remaining design requirements.

## Required response format after execution

Report:
- What actually changed (files, commits, PR link if any)
- Which hub entries were discovered, verified, inaccessible or pending
- Count of offers, price observations, relations, conflict cases, and verified SKUs (0 is valid)
- Sample successful graph queries with source URLs
- Exact tests run and output (including failures)
- Known data gaps and unknown commercial terms
- Next decisions, especially whether customer contract reconciliation is worth implementing

## Success / stop criterion

Proceed to full-scale collection ONLY if the curated graph passes all validation tests and a reviewer can reproduce five answers from the source evidence. If source access or parsing is unreliable, stop at a source registry + curated graph and do not claim complete price intelligence.

**Deliver a useful, smaller graph that is correct rather than an impressively large graph that is wrong.**

