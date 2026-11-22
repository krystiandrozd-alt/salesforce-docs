---
name: sf-license-compare
description: Compare Salesforce editions, licensing and cross-cloud bundles with entitlements, prerequisites, optional add-ons, and separate consumption meters.
---

# Salesforce License and Bundle Comparison

1. Inspect pricing-intelligence/README.md, the YAML seed, and source audit. Use sf-pricing-research when fresh commercial facts need external verification.
2. Keep product, commercial offer, orderable SKU, technical UserLicense, Permission Set License, feature entitlement, capability, price, and buying model as SEPARATE types.
3. Gather user personas/seat counts, existing licenses, orgs, market, customer industry, required capabilities, external access and usage quantities. Identify gaps as assumptions.
4. Evaluate sourced relations: INCLUDES, OFFERS_OPTIONALLY, REQUIRES, ELIGIBLE_WITH, INCOMPATIBLE_WITH and SUPERSEDES. A marketing feature table is not proof of a technical entitlement.
5. Capture scope of included rights (eligible users, quantity, region, period, contractual conditions). Prevent double-counting of bundled Slack, Tableau, Agentforce, Data 360 and support allowances.
6. Keep seat/org/license lines separate from per-action, conversation, Flex Credit, Data 360 profile, Platform login/dev, and MuleSoft credit lines. Do not aggregate distinct units.
7. For consumption figures invoke sf-flex-credit-estimate if appropriate. Exclude unresolved pricing conflicts and unknown commercial dependencies from firm totals.
8. Customer-specific Order Forms override public assumptions only for the authorized customer; do not commit private terms.

Output: Requirement/persona | Proposed offer | Access license/entitlement | Included | Separate purchase | Price meter | Evidence and unknowns.

End with bounded options, trade-offs and non-quote caveats. If a prerequisite or billing denominator is unverified, mark UNKNOWN rather than inventing a configuration.
