---
name: sf-pricing-intelligence-github-first
description: Candidate router for Salesforce prices, editions, licensing, source conflicts and Flex Credit estimates; require verified GitHub branch discovery plus fresh official Salesforce evidence. Do not use for unrelated questions or Salesforce-native org deployment.
---

# Salesforce Pricing Intelligence — GitHub-first candidate (NOT INSTALLED)

This is a proposed replacement for the private ChatGPT pricing orchestrator and
companion to Claude's existing entry skill. The original skills and plugin remain unchanged.
Read `pricing-intelligence/workflows/github-first/WORKFLOW.md` before use.

## Preflight (mandatory for each relevant request)

1. Identify intent: PRICE, LICENSE, CREDIT, AUDIT or a relevant combination.
2. Probe the **actual** connected GitHub app for
   `krystiandrozd-alt/salesforce-docs` and read its `default_branch`.
   Search for `pricing-intelligence/` in default branch. If missing, inspect explicit
   feature/PR refs; known candidate `feature/pricing-licensing-knowledge-graph-20261122`.
   Log exact `repo`, `ref`, `head_sha` and whether each read succeeded.
3. Read historical seed and relevant `AGENTS.md` from the **resolved ref**.
   Never treat a path named in a prompt as accessed unless GitHub returned it.
4. If GitHub is unavailable, proceed with authoritative public research, mark
   `REPOSITORY_UNAVAILABLE` and disclose the missed data layer. Do not simulate
   the graph or pretend a file was fetched.
5. Independently verify current price and feature claims on exact official Salesforce
   regional pages and any applicable rate card. Preserve web snapshots, original
   currencies, pricing denominators, billing cadence and date of observation.
   Repo seed is NOT the authoritative live price book.
6. Reconcile disagreements across historical seed and distinct official page
   variants. Label `CONFLICTED` where the effective price or edition taxonomy
   is unresolved. Newer crawl timestamp is a clue, NOT a contract effective date.

7. Any missing or non-applicable public evidence is `UNKNOWN`, not FALSE or zero.
   Customer price applicability remains `UNKNOWN` until verified against an approved Order Form.

## Routing

- PRICE: return edition, original currency, unit, cadence, URL/section and conflict status.
- LICENSE: separate edition, orderable SKU, technical license, entitlement, optional
  add-on and purchasing model. Do not invent rights or presume included = optional.
- CREDIT: read versioned JSON rate card, use executable deterministic calculator with
  explicit JSON scenario and rate version only when actual runtime is available; report
  `NOT_RUN` otherwise. No Headless TBA->zero or cross-pool aggregation.
- AUDIT: verify evidence, recency, assumptions, conflicts, runtime claims and
  customer applicability; run code tests only for code/calculator changes.
- Salesforce-native Agentforce authoring requires separate explicit authorization;
  never activate it because a pricing question mentions "Agentforce".

## Required response envelope

`request`, `task_mode`, `repo`, `ref`, `sha`, `github_access_status`,
`read_files`, `source_observations[]`, `verified_facts[]`,
`conflicts[]`, `currency`, `price_unit`, `billing_cadence`,
`execution_status` (EXECUTED/NOT_RUN/NOT_APPLICABLE),
`commercial_status` (RESEARCH_ONLY/ESTIMATE_NOT_QUOTE/QUOTE_REVIEW_REQUIRED),
and `unknowns[]`.

Never call a historical price "current" without fresh evidence. A public price
is NOT an orderable Salesforce SKU or binding contract quote. Never disclose
customer Order Forms, org access tokens, or negotiated rates in a public repository.

## Regression gates

- Missing default-branch pricing directory triggers explicit branch discovery.
- GitHub is actually read, or the output explicitly reports unavailability.
- Historical 325/475 and newer indexed 300/450 Communications prices cause a
  conflict report, never silent replacement.
- Older "Agentforce 1" versus newer "Max" editions are NOT silently merged.
- Tests of local CLI fixtures do not establish Salesforce billing parity.
- The skill remains a candidate until the existing 16-case paired skill suite
  plus GitHub-branch/freshness scenarios are run on the same model/tool setup
  and pass critical safety gates.
