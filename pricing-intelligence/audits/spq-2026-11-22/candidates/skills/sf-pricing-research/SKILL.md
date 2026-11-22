---
name: sf-pricing-research
description: Find or verify current published Salesforce product and edition prices, region-specific billing terms and rate-card facts. Do not use for customer-specific signed quotes or org metadata changes.
---

# Salesforce Published Pricing — Research (candidate)

Read shared evidence and output rules from pricing-intelligence/AGENTS.md.

1. Scope named product, edition, region, date, and currency. If region absent, label any EU assumption rather than presenting it as the user's contract region.
2. Open the **exact** official product-specific Salesforce pricing page and linked detail/rate card, not just the EU pricing hub. Record URL, section, observed timestamp and product context.
3. Extract `offer`, `amount`, `original_currency`, `unit_quantity`, `unit`, `display_period`, `billing_cadence`, `buying_model`, `qualifier` (FROM/FIXED/CONTACT_SALES), and any verified included entitlements. Never infer a technical license or SKU.
4. Compare with stored observations for temporal or denominator conflict. A historical YAML entry is not current evidence. Preserve both conflicting observations; label CONFLICTED.
5. If access is blocked or rate absent, say UNKNOWN; if a source contains USD on an EU URL, retain USD. Do not silently convert or produce a customer quote.

**Output:** table of offer/price/unit/terms/source and status; then a short section for unresolved eligibility, conflict, or missing coverage. Only update data on explicit request, append evidence rather than overwriting history.
