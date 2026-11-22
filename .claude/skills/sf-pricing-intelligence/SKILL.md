---
name: sf-pricing-intelligence
description: Route requests about Salesforce public prices, licensing, Flex Credit estimates, pricing verification, or explicitly authorized native Agentforce pricing agents. Do not use for unrelated Salesforce development or general sales strategy.
---

# Salesforce Pricing — Router (candidate)

**Outcome:** choose the smallest appropriate skill and make source, execution and uncertainty visible. Shared invariants live in pricing-intelligence/AGENTS.md; do not duplicate them here.

## Dispatch (apply in order)

1. **Native Agentforce build, deployment or org-backed integration explicitly requested** → sf-pricing-agentforce-bridge. A public pricing question mentioning Agentforce is NOT an org task.
2. **Audit, challenge, or validate a claim, artifact or calculation** → sf-pricing-audit.
3. **Usage-based Flex Credit scenario** → sf-flex-credit-estimate; never calculate as narrative when executable engine is available.
4. **Editions, entitlements, bundles, or license architecture** → sf-license-compare; call pricing research only for price claims needing external verification.
5. **Published amount / edition lookup** → sf-pricing-research.
6. **Mixed request** → compose only the necessary steps; show which step was skipped and why when material.

## Capability gate

Check the actual access to official pages, private repo, Python calculator, and Salesforce org independently. Do not infer that a plugin, file path, CLI or Salesforce org is connected merely because it is named in a prompt.

Report `task_mode`, `source_status` (SOURCE_VERIFIED/INFERRED/UNKNOWN/CONFLICTED), `execution_status` (EXECUTED/NOT_RUN/NOT_APPLICABLE), relevant sources and source section, original pricing unit, result, and material commercial gaps.

**Stop:** no source for a current price → UNKNOWN; no executable calculator → output runnable scenario with NOT_RUN; unpriced rate → do not assert a complete total; no explicit org authorization → read-only.
