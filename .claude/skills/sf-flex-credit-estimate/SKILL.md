---
name: sf-flex-credit-estimate
description: Calculate reproducible Agentforce and Data 360 Flex Credit usage estimates from versioned rate data; use for Salesforce AI consumption forecasts and scenarios.
---

# Salesforce Flex Credit Estimate

Use deterministic calculation software rather than doing rate-card arithmetic in free text.

1. Read pricing-intelligence/data/rate-card-2026-11-03.json and pricing-intelligence/calculator/README.md. Official rate-card PDF: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-11.3.2026.pdf . Rates require contract applicability and visual-table review before commercial use.
2. Record the org, relevant rate-card contract generation, use case, period, monthly volumes, environment, metering unit, actions per interaction, included allowance, and price currency; label unavailable details UNKNOWN.
3. Build a JSON scenario with pricing_model FLEX_CREDITS and usage array. Each entry needs month YYYY-MM, meter ID from the rate JSON, environment production or sandbox, and quantity as a decimal string in the meter's native units. Nonzero included_credits requires allowance_source.
4. Execute from repository root:

    python pricing-intelligence/credit_calculator.py --scenario pricing-intelligence/examples/agentforce-example.json

5. For tests:

    python -m unittest discover -s pricing-intelligence/tests -v

6. Inspect machine-readable response: priced_lines, unpriceable_usage, monthly tier breakdown, priced_credits_only, allowance_assumption, net_priced_credits_only and partial_list_price_equivalent.
7. Headless Platform Interaction is TBA; return UNPRICEABLE, not zero. Slackbot sandbox multiplier is unspecified in the cited table. Conversation pricing is not compatible with this Flex Credit calculator. Data 360 tiers reset by meter and calendar month. Do not add license costs automatically.

Return scenario assumptions, exact volume per meter, source/version, credits, partial list equivalent, all unpriced usage, and explicit ESTIMATE — NOT A SALESFORCE QUOTE. Never call a partial amount the full solution TCO.
