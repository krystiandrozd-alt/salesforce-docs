---
name: sf-pricing-research
description: Research and verify current public Salesforce prices, editions, add-ons, billing units and evidence from official Salesforce sources; use for product pricing lookups.
---

# Salesforce Pricing Research

Use to answer what Salesforce publishes, NOT to generate a customer quote.

1. Read pricing-intelligence/README.md and pricing-intelligence/data/seed-eu-2026-11-22.yaml. This seed is an incomplete historical sample.
2. Establish region, currency, product, edition, and relevant date. Go from https://www.salesforce.com/eu/pricing/ to the specific product pricing page and any official detailed page or rate card. Cite the precise edition/section.
3. Record offer, amount, original currency, pricing qualifier (starting-from/contact-sales/fixed), unit denominator, display period, payment cadence, region, bundle contents, allowances, purchase model and source date separately. UNKNOWN is not zero.
4. Recheck high-impact amounts on the live page rather than relying exclusively on the seed. When public sources disagree, preserve competing observations as CONFLICTED; do not silently select one.
5. Do not turn marketing editions into technical licenses or invent orderable SKUs. Do not convert USD on EU pages to EUR unless a sourced FX conversion is explicitly requested.
6. Remain read-only unless the user explicitly asks to update data. When updating, add a timestamped sourced observation without destroying history.

Return: Offer | Published price | Unit and term | Included vs optional | Source/section | Checked date | Evidence status.

Keep negotiated customer terms outside the public Git repository. Mark all public pricing as indicative rather than a binding quote.
