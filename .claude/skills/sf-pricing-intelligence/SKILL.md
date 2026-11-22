---
name: sf-pricing-intelligence
description: Entry point for Salesforce public pricing, licensing comparisons, Agentforce or Data 360 credit estimation, and evidence audits; route each question to the correct skill and deterministic tool.
---

# Salesforce Pricing Intelligence — Claude agent entry point

This skill is the **single entry point** for using the pricing-intelligence project. It dispatches to existing specialist skills rather than copying their instructions. Read `pricing-intelligence/AGENTS.md` and `pricing-intelligence/docs/agent-io-contract.md` before running calculations.

## Route by requested outcome

| Intent | Delegate to skill | Result |
|---|---|---|
| Current public Salesforce prices, editions, billing | `sf-pricing-research` | Product / offer / amount / original currency / unit / source section |
| Licensing structure, prerequisites, bundles, included access | `sf-license-compare` | Product / commercial offer / technical license / entitlement / optional vs included |
| Agentforce or Data 360 Flex Credit scenario | `sf-flex-credit-estimate` | Reproducible JSON scenario, executed CLI result and unknown meters |
| Commercial claim, source or calculator validation | `sf-pricing-audit` | Evidence-backed pass/review/block audit |
| Salesforce-native Agentforce agent build or deployment | `sf-pricing-agentforce-bridge` | Explicit authorized org validation + official Agentforce ADLC workflow |

Use only relevant stages. For a combined customer proposal: research → license map → deterministic cost estimate → independent audit.

## Data and runtime contract

- Current public facts: https://www.salesforce.com/eu/pricing/ → exact official product-specific pricing page and relevant official rate card. The pricing hub alone is not a complete SKU catalog.
- Historical project seed: `pricing-intelligence/data/seed-eu-2026-11-22.yaml`; it is NOT a live/current price book.
- Rate card snapshot: `pricing-intelligence/data/rate-card-2026-11-03.json` (visual reconciliation and applicable contract validation still required).
- Strict scenario contract: `pricing-intelligence/schema/scenario.schema.json`. Amounts are decimal strings in native meter units.
- Discover meters: `python pricing-intelligence/credit_calculator.py --list-meters`.
- Execute: `python pricing-intelligence/credit_calculator.py --scenario pricing-intelligence/examples/agentforce-example.json`.
- Test: `python -m unittest discover -s pricing-intelligence/tests -v`.
- Never claim that a command ran without actual execution. If no runtime is available, produce a JSON scenario and mark NOT_RUN.

## Non-negotiable distinctions

1. Edition ≠ SKU ≠ UserLicense ≠ Permission Set License ≠ included entitlement ≠ capability.
2. Public list price ≠ signed contract price. Original currency and denominator must be preserved. Monthly display with annual billing is not a monthly contract.
3. A bundled capability is not an unrestricted separate user license. Do not double-count included Slack, Tableau or Agentforce entitlements.
4. Flex Credits, Conversations, profiles, Platform Login & Dev Credits, and MuleSoft credits are different metrics. Do not combine them as one pool without source evidence.
5. UNKNOWN, TBA and CONFLICTED never mean zero. Headless Platform Interaction must remain unpriceable while the applicable multiplier is TBA.
6. A deterministic estimate is NOT a binding quote; `partial_list_price_equivalent` may omit additional licenses, unpriceable meters, credits, taxes and negotiated terms.
7. No Salesforce org credentials or setup are needed to research public prices. Salesforce CLI, ADLC and org access apply only to explicitly requested native Agentforce build workflows. Connecting an org does not authorize changes.

## Standard output

Return **scope; requested facts; verified official page and section; edition/region/unit/billing period; input scenario and exact command if a calculation; resulting status; assumptions; conflicts and remaining commercial unknowns**.

If sources conflict, flag CONFLICTED. If a source is inaccessible, mark UNKNOWN rather than guessing. Never invent an orderable SKU, customer discount or rate multiplier.

## ChatGPT plugin relationship

The separately created private ChatGPT plugin `salesforce-pricing-intelligence` supplies the same orchestration principles when invoked in ChatGPT, but is a **skills-only plugin**. It does not automatically connect GitHub, install a Python runtime, execute this repository's CLI, access a Salesforce org, or deploy a live MCP service. Use actual connected tools to establish those capabilities before claiming execution.
