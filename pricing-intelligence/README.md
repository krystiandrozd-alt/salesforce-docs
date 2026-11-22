---
artifact_id: SF-PRICING-LICENSING-KNOWLEDGE-GRAPH
title: Salesforce EU Pricing & Licensing Knowledge Graph — Blueprint
version: 0.1.0
as_of: 2026-11-22
region: EU
status: blueprint_and_curated_seed
source_of_truth: official_salesforce_public_pages_plus_customer_contract_for_customer_specific_terms
implementation_prompt: prompts/build-graph.md
seed_data: data/seed-eu-2026-11-22.yaml
---

# Salesforce Pricing & Licensing Knowledge Graph

## 1. Purpose and decision

Build a **provenance-first, temporal licensing knowledge graph** across Salesforce products, editions, entitlements, bundles, purchasing models, and published prices. The graph should answer commercial and architecture questions without confusing commercial SKUs, technical licenses, product capabilities, and consumption metrics.

**Do not build another giant static Markdown price list.** Build canonical structured facts and generate views from them: edition matrix, licensing dependency diagram, comparison report, product card, and TCO inputs.

**The public pricing hub is a navigation index, not an authoritative SKU catalog or binding quote.** Source: https://www.salesforce.com/eu/pricing/ . Contract-specific and orderable SKU facts must remain UNKNOWN until supported by signed Order Forms, Salesforce quote data, or official SKU documentation.

## 2. Ambition Engine: the decision

- **Chosen approach — licensing knowledge graph:** treat prices as *observations*, and licensing rules as *evidence-backed claims*; store links and validity periods as first-class objects. This unlocks both product research and downstream agent queries.
- **Rejected alternative — simple catalog:** easier to fill but cannot explain whether a price is an addition, an included bundle, a prerequisite, or a historical quotation.
- **Deferred approach — automated pricing engine:** broad automated crawling and TCO simulation before source quality is established would institutionalize errors.
- **Most dangerous assumption:** published pricing tables expose complete license rights and SKU dependencies. They do not. The commercial contract and technical org entitlements may differ.
- **No-build test:** if the sole user need is occasional manual lookup of a small number of product prices, maintain a curated source index instead of deploying a graph database.
- **External validation:** use actual cross-cloud pricing pages plus a Salesforce commercial/solution architect review of 20 high-risk graph claims; compare separately against a real customer Order Form when authorized.

## 3. High-level graph

~~~mermaid
flowchart LR
  F[Product family] -->|HAS_PRODUCT| P[Product]
  P -->|HAS_OFFER| O[Edition / bundle / add-on / offer]
  O -->|INCLUDES or OFFERS_OPTIONALLY| C[Capability / entitlement]
  O -->|REQUIRES| R[Prerequisite offer or setup]
  O -->|LICENSES_WITH| L[Access license / eligibility]
  O -->|BILLED_BY| M[Pricing metric]
  O -->|HAS_PRICE_OBSERVATION| Q[Published price observation]
  Q -->|SUPPORTED_BY| S[Source snapshot]
  O -->|PURCHASED_UNDER| B[Buying model]
  O -->|PART_OF| X[Contract / order form - private layer]
  O -->|SUPERSEDES| H[Historical offer]
~~~

### Entity classes (separate identity from evidence)

| Class | Meaning | Minimum fields |
|---|---|---|
| product_family | Salesforce category | id, canonical_name |
| product | Named product capability group | id, canonical_name, family_id, aliases |
| offer | Commercially described edition, suite, add-on, credit pack, or program | id, canonical_name, product_id, offer_type, status |
| technical_license | Base user license, PSL, feature license, external access, org entitlement | id, kind, access_scope, verified_technical_name |
| capability | Purchasable or included capability/feature | id, canonical_name |
| pricing_metric | What quantity is charged | id, unit, denominator, measurement_window |
| price_observation | Public price, not inherently an orderable SKU price | id, offer_id, amount, currency, denominator, billing_cadence, qualifier, region, observed_at, source_id |
| buying_model | Subscription, prepaid, pay-as-you-go, pre-commit, enterprise agreement | id, commitment_and_payment_semantics |
| entitlement_allowance | Included capacity or credit quantity | id, quantity, unit, period, scope, offer_id |
| source_snapshot | URL and observation provenance | id, url, section, observed_at, retrieval_status, optional snapshot hash |
| claim | Evidence-backed fact or tentative interpretation | id, subject_id, predicate, object_or_value, evidence_ids, status, valid_from, valid_to |
| conflict | Contradictory source observations | id, involved_claim_ids_or_sources, category, disposition |
| contract_override | Signed customer terms (separately secured) | id, customer_scope, controlling_document, effective_dates |
| sku | Verified orderable SKU only | id, actual_sku, official_evidence, offer_id |

**SKU ≠ edition ≠ user license ≠ permission set ≠ permission-set license ≠ price.** Do not generate SKU identifiers or map marketing labels directly to technical Salesforce license names.

### Allowed relation vocabulary

- HAS_PRODUCT, HAS_OFFER, EDITION_OF, BUNDLE_OF, ADD_ON_TO
- INCLUDES, OFFERS_OPTIONALLY, REQUIRES, ELIGIBLE_WITH, INCOMPATIBLE_WITH
- BILLED_BY, USES_CREDIT_POOL, HAS_ALLOWANCE, PURCHASED_UNDER
- REPLACES, RENAMED_FROM, SUPERSEDES
- ASSERTED_BY, SUPPORTED_BY, CONTRADICTED_BY

**INCLUDES** is not **OFFERS_OPTIONALLY**. “Available for purchase” always maps to OFFERS_OPTIONALLY, not INCLUDES. “All features in previous tier” is an inheritance claim with provenance, not permission to invent every inherited SKU.

## 4. Minimum price observation schema

A price observation must preserve the page's raw presentation and its normalized fields. Do not convert USD figures shown on an EU page into EUR without a separately sourced FX observation, and do not silently reinterpret monthly *unit pricing* as monthly *billing*.

~~~yaml
id: price-sales-core-eu-2026-11-22
offer_id: offer-sales-core
amount: 195
currency: EUR
unit: USER
unit_quantity: 1
display_period: MONTH
billing_cadence: ANNUAL
minimum_commitment: UNKNOWN
qualifier: PUBLIC_LIST_PRICE
region: EU
observed_at: "2026-11-22"
source_id: source-sales-pricing
source_section: "Core"
verification: SOURCE_VERIFIED
~~~

Extend when evidence supports it: starting_from, tax_included, included_amount, rollover_policy, overage_formula, promotional_terms, eligibility, seat_floor, contract_term. Missing fields remain null/UNKNOWN. A value in a public price card is **not** proof that the corresponding edition is orderable on those terms for every customer.

## 5. Source hierarchy and evidence rules

1. **Customer-specific:** signed Order Form, applicable terms, official Salesforce quote and SKU details, then Salesforce org allocation (distinct commercial vs deployed truths).
2. **Public commercial:** official Salesforce product-specific pricing page and detailed rate card or pricing guide.
3. **Public overview:** https://www.salesforce.com/eu/pricing/ and flexible buying model pages.
4. **Technical documentation:** official license documentation, setup help, release notes.
5. **Derived reasoning:** clearly marked INFERRED with supporting claims; never presented as verified.

For each claim: preserve source URL, product/section, capture date, statement type, subject/predicate/object, evidence status and unresolved conflicts. A missing entry means UNKNOWN, never FALSE. Distinguish source verification from business/legal applicability.

**Observed public pages (2026-11-22 review; pages may have been crawled earlier):**

| Family | Official page | Structural signal |
|---|---|---|
| Salesforce hub | https://www.salesforce.com/eu/pricing/ | Role- and industry-indexed product navigation |
| Sales | https://www.salesforce.com/eu/sales/pricing/ | Per-user editions, bundled Slack/Tableau/credits |
| Communications | https://www.salesforce.com/eu/communications/pricing/ | Per-user editions plus multi-million-euro org/year BSS suites |
| Agentforce | https://www.salesforce.com/eu/agentforce/pricing/ | Per-user, action/credit, conversation, and add-ons |
| Data 360 | https://www.salesforce.com/eu/data/pricing/ | Credit-based and per-profile purchasing; non-profile work may need credits |
| Marketing | https://www.salesforce.com/eu/marketing/pricing/ | Org-based editions plus cross-product packages |
| Marketing Intelligence detailed | https://www.salesforce.com/eu/marketing/analytics/pricing/ | Clarifies detailed edition licensing unit |
| Platform app development | https://www.salesforce.com/eu/platform/enterprise-app-development/pricing/ | Named user vs login/credit licensing |
| Flexible buying | https://www.salesforce.com/eu/pricing/flexible-buying-models/ | Pre-purchase, pre-commit, pay-as-you-go |

All additional role/industry entries from the hub need discovery and validation; the table above is an initial registry, not exhaustive coverage.

## 6. Curated seed, deliberately limited

See [data/seed-eu-2026-11-22.yaml](data/seed-eu-2026-11-22.yaml). Its factual examples include:
- Sales Cloud Core: EUR 195/user/month, billed annually; published bundle contains Slack Business+ and Tableau Next.
- Communications Cloud Growth EUR 325/user/month; Advanced EUR 475/user/month; B2B BSS Suite starting at EUR 4,000,000/org/year.
- Agentforce Flex Credits EUR 500 per 100,000 credits; Conversations EUR 2/conversation.
- Marketing Cloud Next Growth EUR 1,500/org/month.
- Data 360 Profiles USD 240 per 1,000 profiles/year; currency deliberately preserved despite the EU URL.

**Conflict to preserve, not “fix” silently:** Marketing overview labels Marketing Intelligence EUR 10,000 **per user/month**, but the detailed page labels the same amount EUR 10,000 **per org/month**. Flag CONFLICTED until official clarification. Do not admit either into a quote-ready graph.

## 7. Repository architecture — graph first, database later

~~~text
pricing-intelligence/
  README.md                     # Blueprint and architecture
  prompts/build-graph.md        # Ready-to-run Claude implementation prompt
  data/seed-eu-2026-11-22.yaml  # Curated, source-linked observations
  [proposed build outputs]
  schema/graph.schema.json
  data/sources.yaml
  data/raw/                     # Page snapshots or references, copyright-safe
  data/normalized/              # Nodes, edges, claims, observations, conflicts
  scripts/discover.py
  scripts/ingest.py
  scripts/validate.py
  scripts/query.py
  tests/fixtures/
  tests/test_provenance.py
  tests/test_commercial_rules.py
  docs/coverage.md
  docs/conflicts.md
~~~

Use versioned structured files as the canonical source. Export to SQLite/Neo4j/NetworkX later if relational exploration or graph traversal warrants it; **do not require graph infrastructure to validate an MVP**.

## 8. Work plan and milestones

| Phase | Implementation | Concrete exit criterion |
|---|---|---|
| P0 — model and provenance | JSON Schema, source registry, identifier policy, field evidence, curated seed | Curated seed validates; all prices trace to URL and section; no fabricated SKU |
| P1 — bounded discovery | Traverse ALL product and industry pricing links from EU hub; discover directly linked detailed price/rate-card pages | Coverage report lists every hub entry as verified, blocked, contact-sales, or pending; no invisible omissions |
| P2 — licensing graph | Normalize offers, claims, bundle inclusion, dependencies, metrics, allowances; preserve names and aliases | Supported queries return traceable evidence and UNKNOWN where data missing |
| P3 — change intelligence | Time-stamped observations, diff review, conflict queue, human approval | New site change cannot silently overwrite prior verified fact |
| P4 — decision support | Cross-cloud license comparison, entitlement mapping and bounded TCO scenario templates | Calculations explicitly separate published assumptions from quoted terms |

**Priority:** P0 + P1, then review 20 highest-risk claims with independent evidence. Do not build a slick UI, autonomous purchase recommender, comprehensive calculator, or quotation engine until provenance and graph correctness pass.

### Acceptance tests (must pass)

1. Every published price has amount, original currency, metric denominator, billing cadence (or UNKNOWN), region, source, observation date.
2. Cannot classify “available for purchase” as “included”.
3. Cannot conflate technical UserLicense/PSL with commercial editions.
4. Cannot multiply an included Slack/Tableau/Agentforce allowance into extra standalone costs unless evidence indicates extra purchase.
5. Cannot equate Agentforce Flex Credits, Platform Login/Dev Credits, Mule Credits, Data 360 profiles, and conversation counts.
6. No unsourced conversion of USD↔EUR; no mislabelling of billed annually vs display per month.
7. Conflicted marketing intelligence units remain unresolved and excluded from firm calculations.
8. Historical observations remain accessible; current values are selected by valid time + retrieval date + conflict status.
9. Hub navigation completion is reported, including URLs not reachable or with “Contact Sales”.
10. Every answer returns supporting source references and clearly identifies UNKNOWN / INFERRED / CONFLICTED facts.

### Minimum supported queries

- What purchase models are available for Agentforce, and what meters do they apply to?
- Which Sales editions explicitly include Slack or Tableau, and where is only an optional purchase shown?
- What is the difference between Communications Cloud per-user editions and the B2B/B2C BSS Suite organization pricing?
- Which Marketing offers have org-based pricing, and which published metric conflicts block comparison?
- What licensing facts are still unknown for a given industry edition?
- What changed between two public pricing observations?

## 9. Implementation handoff

Use **[prompts/build-graph.md](prompts/build-graph.md)** in Claude Code or another coding agent. The prompt requires real repository inspection, source verification, graph schema implementation, tests, actual outputs, and a source-by-source completion report. The graph is a commercial-knowledge instrument, **not a definitive Salesforce quotation**.

## 10. Governance

- Require review before promotion of scraped observations to VERIFIED claims.
- Protect any customer-specific contract files and prices; never commit private Order Forms or account terms to a public repository.
- Track product rename/deprecation with identity-stable IDs and historical aliases.
- Respect crawling limits, site terms, and public-page copyright; retain factual extraction and citations rather than reproducing full proprietary tables verbatim.
- Escalate contested commercial and legal interpretations to Salesforce account team.
