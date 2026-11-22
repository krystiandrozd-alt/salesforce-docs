# Salesforce Flex Credit Calculator — functional specification (proposed)

**Status:** SPECIFICATION ONLY — not an implemented calculator or official Salesforce quote.
**As-of:** 2026-11-22. Pricing / multipliers must be versioned and reviewed for each calculation.

## Official references

- Public calculator: https://www.salesforce.com/eu/agentforce/pricing/calculator/
- Agentforce EU list price: https://www.salesforce.com/eu/agentforce/pricing/
- Official Flex Credits Rate Card updated November 3, 2026: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-11.3.2026.pdf
- Data 360 pricing: https://www.salesforce.com/eu/data/pricing/

## Functional reconstruction target

Reproduce user-facing scenario estimation rather than proprietary Salesforce quoting. The public calculator covers Agentforce and Data 360 use-case inputs, seat licensing, included credits, one-year summary, Flex / Profiles modes, detailed breakdown and generated reports. Recreating unverified backend template defaults, partner-only SKU selection or negotiated price waterfalls is **out of scope** pending source evidence.

## Credit formula

For non-tiered usage: credits = sum(quantity / metering_unit_size * applicable_multiplier).
Keep business event count, metered usage count and actions per business event separate.
Ex.: 5,000 production standard Agentforce actions × 20 credits/action = 100,000 credits.
At public EUR 500 / 100,000 credits, list-price usage equivalent = EUR 500. When procurement uses 100k packs, calculate ceiling-pack purchase separately from actual consumption. Contract inclusions or tiered commercial discounts can change net cost.

### Example rate-card meters (November 3, 2026)

| Meter | Unit | Production | Sandbox |
|---|---|---:|---:|
| Agentforce standard/custom action | Per action | 20 | 16 |
| Agentforce Voice standard/custom action | Per voice action | 30 | 24 |
| BYO LLM starter prompt | Per prompt | 2 | 2 |
| Salesforce LLM basic/standard/advanced prompt | Per prompt | 2 / 4 / 16 | 2 / 4 / 16 |
| Help/IT/HR Agent Resolutions | Per resolution | 400 | 0 |
| Sales leads worked | Per lead | 400 | 320 |
| Slackbot standard/advanced action | Per action | 40 / 200 | See rate card — do not infer sandbox |
| Headless Platform Interaction | Per interaction | **TBA** | **TBA** |

### Data 360 tiered volume model

The rate card defines **per-usage-type monthly tiers**, reset at calendar-month boundaries, and **non-tiered sandbox multipliers**. Store rate schedules with usage type, metering units, tier thresholds in credits, multiplier, environment, effective version and month. Avoid a global uniform 20-credits/action assumption.

| Data 360 usage type | Unit | Production base multiplier | Tier 2 | Tier 3 | Tier 4 | Sandbox |
|---|---|---:|---:|---:|---:|---:|
| Prep | 1M rows | 40 | 32 | 16 | 8 | 32 |
| Unification | 1M rows | 75,000 | 60,000 | 30,000 | 15,000 | 60,000 |
| Segmentation | 1M rows | 50 | 40 | 20 | 10 | 40 |
| Activation | 1M rows | 60 | 48 | 24 | 12 | 48 |
| Zero-Copy Sharing-Out | 1M shared rows | 60 | 48 | 24 | 12 | 48 |
| Queries | 1M rows | 3 | 2.4 | 1.2 | 0.6 | 2.4 |
| Unstructured Processing | MB | 150 | 120 | 60 | 30 | 120 |
| Intelligent Processing | MB | 600 | 480 | 240 | 120 | 480 |
| Streaming Pipeline | 1M rows | 3,500 | 2,800 | 1,400 | 700 | 2,800 |
| Real-Time Pipeline | 1M combined events/API/actions | 250,000 | 200,000 | 100,000 | 50,000 | 200,000 |
| Code Extension | Compute unit | 40 | 32 | 16 | 8 | 32 |

Production tier boundaries in rate-card cumulative credits: up to 300,000 (base); 300,000–1,500,000 (tier 2); 1,500,000–12,500,000 (tier 3); over 12,500,000 (tier 4). Check how tier transitions and fractional units are rounded against Salesforce actual usage before claiming financial equivalence.

## Mandatory inputs

- Rate card version / market / selected product / contract generation.
- Usage by scenario: audience, interactions, action mix, voice, prompt class, production versus sandbox and events per month.
- Data 360 monthly usage by distinct metered service, quantity and unit, profile tier option where applicable.
- Included credits, timing/expiry, pool eligibility and credit-purchase scheme.
- Seat-based Agentforce license count and product-specific eligibility (only when verified).
- Price currency, verified rate, packaging/rounding and contract discounts **explicitly supplied** rather than invented.

## Outputs

1. Monthly breakdown: meters × production/sandbox multipliers × credit tiers.
2. Credits consumed, credits covered by verified allowances, net credits to purchase.
3. Usage-equivalent list cost versus whole-pack purchase estimate (separate).
4. Scenario comparison; 12-month forecast with tier resets.
5. Source and multiplier version per line, plus unknown/unpriceable usages.
6. Summary of conditions not covered: CRM licenses, implementation, taxes, data storage, enterprise discounts, contract limits and other consumption types.

## Calculation quality gates

- Agentforce standard action 5,000 prod → 100,000 credits.
- Agentforce standard action 5,000 sandbox → 80,000 credits.
- Voice action 1,000 prod → 30,000 credits.
- Data 360 base Prep 1M processed rows → 40 credits before relevant tier/usage aggregation.
- Prohibited calculation: Headless Platform Interaction without an official numeric multiplier.
- Data 360 monthly reset is tested with a 2-month fixture; tiers do not carry over.
- A customer using Conversation pricing must not automatically be modeled as concurrently eligible for Flex Credits in the same org without contract-specific verification.
- Pricing and purchasing math must respect credits denomination, currency, available allowances, and unknown deal discounts.

## Architecture

Use a pure calculation library fed by versioned rate-card data and commercial-contract overrides, and a separate UI. The UI can resemble Salesforce's step flow (industry → use cases → configure → results), but must show transparent formulas and evidence links. Keep the input assumptions and calculation result reproducible in YAML/JSON.

**Release gate:** Source-verified rate data, passing offline fixtures, review of billing semantics, and comparison with at least five live Salesforce sample scenarios. Until then, label all calculations ESTIMATE.