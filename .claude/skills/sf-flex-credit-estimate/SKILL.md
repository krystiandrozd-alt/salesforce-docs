---
name: sf-flex-credit-estimate
description: Produce source-versioned Agentforce and Data 360 Flex Credit estimates using the repository's deterministic Python engine. Do not use for Conversations-only billing, technical license grants, unsupported Headless rates, or customer billing invoices.
---

# Flex Credit Estimation (SPQ pilot)

Read pricing-intelligence/AGENTS.md and docs/agent-io-contract.md. Calculation is deterministic software; the LLM chooses assumptions, not arithmetic.

1. Check availability of actual repository checkout, Python runtime and applicable rate-card version. Do not claim the local tool is exposed through ChatGPT or an Agentforce org.
2. Execute `python pricing-intelligence/credit_calculator.py --list-meters` to discover valid meter IDs/native units. If not executable, return a JSON scenario with `execution_status: NOT_RUN`.
3. Capture `month`, `meter`, `environment`, `quantity` (decimal string in native units), assumed actions per interaction, and any included allowance with its source. Reject unsupported purchase models and missing assumptions.
4. Validate against pricing-intelligence/schema/scenario.schema.json then execute `python pricing-intelligence/credit_calculator.py --scenario <scenario.json>` when authorized runtime is available. Preserve stdout result/error and version.
5. Data 360 production tiers reset per meter/calendar month. Headless Platform Interaction TBA or unknown sandbox rates → `INCOMPLETE_UNPRICEABLE_USAGE`, never zero or full TCO.

**Output:** input JSON or artifact path, exact command and execution_status, rate version/source, per-line credits, partial list-price equivalent, unpriced usage, assumptions and ESTIMATE_NOT_QUOTE. Do not equate usage-equivalent rate with invoice/pack purchasing.
