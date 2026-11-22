---
name: sf-license-compare
description: Compare Salesforce editions, technical access licenses, entitlements, prerequisites and included-versus-optional bundles. Do not use for simple rate lookups or unverified customer quote commitments.
---

# Salesforce Licensing Comparison (candidate)

Read the shared commercial invariants in pricing-intelligence/AGENTS.md. Use official Salesforce documentation (optionally `platform-docs-get` when installed) for technical license semantics; pricing amounts require product-specific commercial sources.

1. Identify customer scenario: personas/seats, existing products, geography, requested capabilities, external users, deployment model and known contract constraints. State missing inputs instead of inventing them.
2. Keep distinct entities: product → commercial offer → technical license/entitlement → capability → purchase model → price observation. SKU is UNKNOWN without explicit commercial evidence.
3. For each relation record one of `INCLUDES`, `OPTIONAL`, `REQUIRES`, `ELIGIBLE_WITH`, `INCOMPATIBLE_WITH`, or `UNKNOWN` plus **specific source and applicability** (seats, org, quantity, term). Do not infer from marketing adjacency.
4. If current prices matter, invoke sf-pricing-research for the affected offers; if credit consumption matters, invoke sf-flex-credit-estimate. Neither is automatic.
5. Deduplicate included products before presenting extra lines. Track incompatible meters separately: user, org, conversation, Flex Credits, profiles, logins and other credit pools.

**Output:** Requirement | Offer | Access/entitlement | Included/optional | Prerequisite | Meter | Source/status | Gap. Provide bounded alternatives; no firm total if eligibility/denominator is unresolved.
