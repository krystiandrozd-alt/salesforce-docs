# Ambition Engine — Pricing Intelligence Architecture Review

**Date:** 2026-11-22  
**Repository:** krystiandrozd-alt/salesforce-docs, draft PR #8  
**Current decision:** proceed with versioned claim graph + deterministic rate engine + project-scoped Claude skills; do not claim full pricing book or Salesforce quote parity.

## Reframe

Original task: create a Salesforce pricing artifact and let Claude use it.

Better outcome: let Claude **answer verifiable licensing questions and reproduce bounded commercial estimates**, with source evidence, contract awareness, explicit unknowns, and automated numeric checks.

## Three alternatives

| Option | Mechanism | Benefit | Biggest weakness | Reversible test |
|---|---|---|---|---|
| A. Markdown price collection + Claude instructions | Manual extraction and prompt-based answers | Low setup | Stale information and inconsistent arithmetic | Ask five cross-cloud pricing questions twice, check discrepancies |
| **B. Skills + versioned claims + deterministic calculator** | Claude interprets questions, a rules engine calculates, Git records provenance | Reproducible numbers and auditable assumptions | Still vulnerable to wrong source extraction or contract applicability | Run thirteen fixtures and independently reconcile five Salesforce scenarios |
| C. Continuous crawler + remote knowledge graph + autonomous recommender | Ingest and compare entire Salesforce portfolio | Wide coverage and timely changes | Excessive operational scope; can spread source errors across reports | Do not build until B passes source and user-value checks |

**Decision:** B with narrow P0 focus. Defer autonomous crawling and graph database.

## Fragile assumptions and falsifiers

| Claim | Challenge | Minimum check |
|---|---|---|
| Public Salesforce rates are usable for every customer | Editions, rate cards, contract cohorts and Order Forms can change eligibility | Compare with authorized customer contract/usage record |
| Price page alone describes licensing | Commercial edition is not a technical user license, and inclusion may have scope restrictions | Review five edition-PSL/entitlement pairs with official documentation |
| AI can safely compute costs | Language models can invent or combine incompatible units | Independent deterministic calculator + test fixtures |
| Catalog coverage equals procurement coverage | Public pricing pages omit negotiated and SKU-specific terms | Report public coverage separately from quote completeness |
| A graph database is required to have a knowledge graph | Most first-party questions may be answered from typed files | Track queries; migrate only after measurable traversal need |

## Observed implementation

- Existing documentation repo originally had a blueprint, curated seed, build prompt, source conflict register and calculator specification.
- Added four project-scoped Claude skills (pricing research, license comparison, Flex Credit estimate, pricing audit).
- Added data/rate-card-2026-11-03.json with 29 official-rate-card usage meters and original-unit denoms.
- Added credit_calculator.py, example scenario, 13 unittest fixtures and GitHub Actions CI.
- Official Salesforce Flex Credit Rate Card updated November 3, 2026: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-11.3.2026.pdf
- EU Agentforce published rate: https://www.salesforce.com/eu/agentforce/pricing/
- Claude Code skills reference: https://code.claude.com/docs/en/skills

**Verified execution:** GitHub Actions run https://github.com/krystiandrozd-alt/salesforce-docs/actions/runs/45020898343 completed successfully on the feature PR; 13/13 Python unit fixtures passed; sample output = 100,040 Flex Credits. This validates calculations against the committed rate fixture, not external billing parity.

**Known evidence limitation:** PDF text tables were accessible but the web screenshot request returned a cache miss, so the rate card JSON is flagged TRANSCRIBED_OFFICIAL_PDF_PENDING_VISUAL_TABLE_CHECK. The published rate card also says Headless Platform Interaction rate TBA. Never quote Headless usage as free or as zero.

## P0/P1 gates and backlog

| Priority | Improvement | Proof required |
|---|---|---|
| P0 | Full visual and semantic cross-check of all 29 multipliers | Every number/unit reconciled to the exact versioned official rate card |
| P0 | Compare 5 manual cases with Salesforce public calculator using documented inputs | Differences explained or reproduced, no unexplained rate mismatch |
| P1 | JSON Schema for product, offer, license entitlement, rate observation, allowance, snapshot and conflict | Schema and referential tests pass |
| P1 | Bounded source registry spanning full EU pricing hub | Every product/industry link classified, with review status and capture date |
| P1 | Versioned product dependency edges with eligibility and bundle allowances | Inclusion/prerequisite queries pass source-backed review |
| P1 | Skill behavioral tests in Claude Code (manual prompts with observed answers) | No invented SKU or ungrounded price in ten adversarial scenarios |
| P2 | Commercial input layer: licenses, negotiated terms, credit pools | Secure storage controls + correct isolation and contract applicability |
| P2 | Calculator UI and scenario comparisons | Independent user acceptance, scenarios reproducible from JSON |
| Defer | Neo4j / autonomous price recommender | Evidence a file-backed graph cannot support real needed queries |

## Acceptance and anti-hallucination gates

- All pricing numbers must identify rate version, original currency, source URL, specific unit, region and period.
- Product, commercial edition, technical access license, price, purchase model and entitlement remain separate classes.
- Included or optional add-ons are not double-counted.
- Data 360 production tiers reset per usage type and calendar month; sandbox rates handled separately.
- UNKNOWN, TBA and CONFLICTED data never become numeric zero.
- Financial output differentiates *consumption equivalent*, *commercial purchase*, *subscription cost* and *whole-solution TCO*.
- Actual customer quotations need applicable contract evidence and human commercial review.

**Outside judge:** technical tests are necessary but insufficient; require independent comparison with Salesforce official calculator and authorized contract samples.

## First Claude task sequence

1. /sf-pricing-research Check two current EU pricing pages and record exact source sections and denominators.
2. /sf-license-compare Model the difference between a commercial edition, an included entitlement and an optional add-on.
3. /sf-flex-credit-estimate Run the supplied 5,000-action plus 1M-row example and identify list equivalent vs actual purchasing cost.
4. /sf-pricing-audit Challenge it with the Headless TBA and Marketing Intelligence conflicting-unit examples.

**Go/no-go:** Go for internal research and bounded estimates with caveats. No-go for binding quotes, unattended procurement decisions or claims of exhaustive Salesforce SKU coverage.
