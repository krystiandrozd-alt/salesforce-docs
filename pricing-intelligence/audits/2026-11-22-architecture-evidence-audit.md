# KD DecisionOps — Architecture Audit #1 (2026-11-22)

**Target:** Salesforce EU Pricing & Licensing Knowledge Graph, draft PR #8.
**Method:** WER-02 deliverable audit + WER-01 claim verification + ARC-02 architecture options.
**Gate:** REVIEW for blueprint; BLOCK for quote-ready use or claims of tested implementation.

## Actual inspection

- Read all 3 committed artifacts on feature branch: README (211 lines), YAML seed (290 lines), build prompt (164 lines).
- Bounded static identifier/reference check of the seed: 7 sources, 5 families, 10 offers, 3 capabilities, 11 prices, 3 relations, 1 conflict; zero duplicate IDs and zero unresolved offer/family/source/edge references detected.
- This was a text-level static scan, NOT full YAML parser, JSON Schema, executable graph, source snapshot archive or automated test suite.
- Official public product pages and combined Flex Credit Rate Card updated November 3, 2026 reviewed as external evidence. PDF screenshot retrieval failed; do not claim pixel-perfect table verification.

## Prioritized issues

| ID | Gate | Evidence / risk | Required change |
|---|---|---|---|
| A01 | BLOCK | No executable schema, graph loader, query API or tests; only blueprint and seed. | Build schema and tests before release. |
| A02 | BLOCK | None of 11 price observations has its own observed_at or historical effective dates. | Per-claim capture time, immutable provenance and temporal selectors. |
| A03 | REVIEW | Agentforce Conversations uses billing_cadence PRE_PURCHASE; this is purchasing model, not invoice cadence. Flex pack uses ONE_TIME_PACKAGE as period. | Separate purchase_model, unit, packaging, display_period, billing_schedule, contract_term. |
| A04 | BLOCK | No rate-card multiplier entities or sandbox/prod/volume tier rules. | Versioned consumption engine and rate-card reference. |
| A05 | REVIEW | Marketing Intelligence EUR 10,000 per USER in overview vs per ORG in detailed page; correctly marked CONFLICTED. | Do not quote until clarified. |
| A06 | REVIEW | INCLUDES edges lack eligibility, allowance, term and scope. | First-class entitlement grants. |
| A07 | REVIEW | No immutable excerpt/page hash for source observations. | Provenance snapshot identifiers and hashes where permitted. |
| A08 | REVIEW | Missing shared credit pool, allowances, eligibility and exclusive billing modes. | Distinct meters, pools, license gating and buying models. |
| A09 | REVIEW | Only 7 public URLs registered, not full EU hub. | Exhaustive navigational link inventory and explicit coverage states. |
| A10 | BLOCK for Headless pricing | November 2026 Flex Credit Rate Card lists Headless Platform Interaction multiplier as TBA. | Mark UNCOSTABLE / TBA until an applicable official multiplier exists. |

## New source evidence

- EU pricing hub: https://www.salesforce.com/eu/pricing/
- Agentforce EU: https://www.salesforce.com/eu/agentforce/pricing/ (EUR 500 per 100,000 Flex Credits; 20/action, 30/Voice action, EUR 2/conversation).
- Updated 2026-11-03 rate card: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-11.3.2026.pdf (production vs sandbox, Data 360 volume tiers, Slackbot, prompts, Headless TBA).
- Public combined calculator: https://www.salesforce.com/eu/agentforce/pricing/calculator/ (Agentforce + Data 360, templates, scenarios, one-year estimates; exact backend defaults not audited).
- Marketing conflicting units: https://www.salesforce.com/eu/marketing/pricing/ vs https://www.salesforce.com/eu/marketing/analytics/pricing/
- Data 360 public pricing: https://www.salesforce.com/eu/data/pricing/; legacy Data Services Credits contract conditions may differ.

## ARC-02 alternatives

| Option | Benefit | Risk / change cost |
|---|---|---|
| Static catalog | Quick source index | Cannot explain temporal or bundled rights |
| **Versioned claim graph + deterministic rate engine** | Independently testable rules, priced consumption, explainable provenance | Requires careful rate validation |
| Remote graph database + automated collector | Rich traversal | Operational complexity, source errors and unwarranted authority |

**Recommendation:** versioned claim graph + deterministic calculation engine in Git; export graph to a database only if verified query requirements justify it. No accepted ADR yet; architecture change remains proposed.

## Gates

1. P0: full YAML parser + JSON Schema + unique keys + referential integrity + historical observations. UNEXECUTED.
2. P1: versioned rate engine with production/sandbox, per-type monthly Data 360 tiers, rate-card fixtures, allowance, currency and credit-pool separation. UNEXECUTED.
3. P2: all hub URLs enumerated, classified and cited. UNEXECUTED.
4. P3: 20 material claims independently reviewed before commercial use. UNEXECUTED.

**Result:** initial static audit complete; fixes and execution still outstanding.