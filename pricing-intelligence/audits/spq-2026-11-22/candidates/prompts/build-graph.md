# Salesforce Pricing Graph — Stage-Gated Build Prompt (SPQ candidate)

**Use in Claude Code on `krystiandrozd-alt/salesforce-docs` when the user requests to implement or extend the pricing graph.** This is a **build workflow**, not a public-price question. Do not execute every stage automatically.

The original `pricing-intelligence/prompts/build-graph.md` remains the detailed acceptance checklist. Do **not** delete its required source cases, negative tests, coverage tracking or safety gates when splitting work into stages. Each stage must cite the matching original acceptance criteria before passing its gate.

## Context and hard constraints

Read `pricing-intelligence/README.md`, `pricing-intelligence/AGENTS.md`, source registry, seeded facts and prior audit. Reuse the existing calculator, CI, and six specialist skills; preserve unrelated files. Official source of public prices: https://www.salesforce.com/eu/pricing/ and each specific Salesforce product pricing/rate-card page.

Preserve separately product, edition, confirmed SKU, technical license, entitlement, inclusion/dependency, price observation, unit, purchase model, billing schedule, source snapshot and contract override. Unknown ≠ false or zero. Do not invent commercial rates, orderable SKUs, org permissions or bundle inclusions. Retain original currency, denominator, region and observed/effective dates. No private customer contract in public Git. Do not deploy or merge without approval.

## Stage A — Evidence and schema (default first execution)

1. Inspect existing repository and select a bounded set of source-backed gaps, not an imagined greenfield project.
2. Enumerate all links on the EU pricing hub into a source registry; label each VERIFIED / NEEDS_REVIEW / CONTACT_SALES / INACCESSIBLE / NOT_VISITED. Do not claim complete coverage if traversal is partial.
3. Implement or validate versioned JSON Schema for observations, entities, relations, entitlement scope, allowances, rate cards and conflicts. Preserve raw source anchor and evidence timestamp.
4. Validate existing YAML/JSON and references without rewriting curated evidence. Write **proposed diffs** for conflicts.
5. Run schema/seed validation and output exact commands, passing/failing counts, provenance and remaining uncertainty.

**Gate A:** all selected observations have exact unit/currency/source, validation passes, and unverified claims are not promoted. **STOP** if source access or evidence is unreliable.

## Stage B — Graph and query engine (only after Gate A)

1. Implement a deterministic normalized graph exporter (file-backed JSON/YAML first; no mandatory Neo4j).
2. Support: family/edition lookup, sourced price observation, included vs optional/pre-required rights, product relationship paths, current vs historical snapshots and unresolved conflicts.
3. Add tests for double-counting, marketing edition vs PSL, mixed currencies, annually-billed monthly display, missing source, historical overwrite and conflicting marketing denominators.
4. Generate comparison tables from graph facts only.

**Gate B:** query outputs cite source sections and UNKNOWN when necessary; tests run and documented. Do not claim an official SKU catalog.

## Stage C — Consumer integrations (explicit follow-up scope only)

1. Reuse the existing credit_calculator.py and versioned rate data; do not rebuild arithmetic inside LLM prompts.
2. Expose a read-only adapter when actually implemented (never imply that a CLI is a live Agentforce action/MCP service).
3. Scenario inputs must match schema; preserve Data 360 meter units, production/sandbox and monthly tier reset.
4. Test usage scenarios against official sources and, if accessible, the official calculator; record discrepancies.
5. Offer optional org-bound Agentforce integration ONLY with explicitly authorized org, read-only verification first, and official ADLC skills.

**Gate C:** actual invocation logs and external comparison evidence. No customer-ready quote without applicable contract and commercial review.

## Required report after EACH stage

- Files changed (path/commit) and why; unaffected originals.
- Source links and evidence statuses, including inaccessible gaps.
- Node/edge/price counts **actually validated**, not estimated.
- Commands/tests actually run and exact failures.
- High-impact unresolved conflicts, claim-level dates and material exclusions.
- Decision: PROCEED / REVIEW / STOP; next single stage.
- If no runtime or official source access, say so and provide an executable handoff; never claim a build or benchmark that did not run.
