# Salesforce Solution Intelligence — architecture + headless + commercial

**Status:** draft cross-repository contract with a runnable **synthetic-only structural resolver pilot**. This is NOT a connected Salesforce org, MCP server, executable Headless Toolkit, verified product/license database or quote-ready pricing system.

## Goal

Enable an architect/consultant/AI agent to move from a designed business process, capability or functional skill to a justified implementation, required licenses/entitlements, eligible packages and an appropriately qualified billing/TCO view.

Three independent, source-owned layers:

| Layer | Canonical repository | What it contributes | Not authoritative for |
| --- | --- | --- | --- |
| TECHNICAL | [salesforce-docs](https://github.com/krystiandrozd-alt/salesforce-docs) (master, 54 product sections; `index.md` and `content.md`) | Salesforce product documentation and direct official source references | Customer's actual org configuration, licensing contracts |
| SOLUTION | [headless-toolkit](https://github.com/krystiandrozd-alt/headless-toolkit) (master) | HXL (Beta), Hosted MCP Servers, Multi-Framework, Microfrontend, headless patterns | Production-ready runtime or guaranteed suitability for every surface |
| COMMERCIAL | [pricing-intelligence](https://github.com/krystiandrozd-alt/salesforce-docs/tree/feature/pricing-licensing-knowledge-graph-20261122/pricing-intelligence) (feature branch) | Public-price research, entitlements research, deterministic limited Flex Credit estimation, independent audit | Complete SKU catalog, contract price, complete implementation TCO |

Do not replicate source files or create unmaintained price lists. Store resolvable pointers, dated evidence and explicit assumptions. The headless catalog is already designated as the primary deeper source for headless/HXL/MCP by salesforce-docs README.

## Agent entry point

Use `/sf-solution-architect` (project skill at `../.claude/skills/sf-solution-architect/SKILL.md`).

The skill coordinates documentation lookup, solution-pattern selection and the existing `/sf-pricing-intelligence` skill. It does **not** reimplement the existing six pricing skills or the Python estimator.

## Required process-to-commercial references

Before mapping a process, function or functional skill to commercial requirements, read the following in order:

| Reference | Purpose |
| --- | --- |
| [Skill routing and prerequisites](docs/skill-routing.md) | Ownership, GitHub-first production pricing versus SPQ pilot, upstream Salesforce Skills access gates. |
| [Source manifest](source-manifest.yaml) and [reference registry](reference-registry.yaml) | Canonical ownership, exact repository paths and per-run commit resolution. |
| [Capability and commercial contract](docs/capability-commercial-contract.md) | Typed many-to-many relations, prerequisites, evidence, billing and output definitions. |
| [Process resolver prompt](prompts/resolve-process-commercial.md) | Reusable Claude/agent workflow from process or skill to entitlement, package and billing. |
| [Pricing build prompt](../pricing-intelligence/prompts/build-graph.md) | Implementation work including the process/capability bridge and acceptance cases. |
| [Resolver pilot quickstart](RESOLVER-QUICKSTART.md) | Run the deliberately synthetic relationship graph; distinguish prototype coverage from real licensing verification. |

The required trace is process/step → capability → implementation/functional skill → exact technical feature → required entitlement/license → providing offer/package → applicable billing metric, rate and allowance. Each relation has its own evidence and applicability. Keep authoring/delivery skills distinct from runtime functional skills, commercial offers distinct from managed packages, and permissions distinct from purchased rights.

The target production resolver must support forward search and reverse impact lookup, explicit `ALL_OF` / `ANY_OF` prerequisites, existing-entitlement comparison and an evidence path for every output row. The current pilot now accepts process, step, capability **and functional-skill IDs**, but returns candidate offers, not verified customer orderability. Semantic search finds candidates; typed, scoped relationships establish supported conclusions. Unknown licensing, inclusion or billing remains unknown.

**Implementation status:** the contract, source routing and prompts are present. A **synthetic-data structural resolver with 24 automated synthetic contract tests** is now available at [resolver.py](resolver.py); see [quickstart](RESOLVER-QUICKSTART.md). A verified/ingested commercial graph, complete licensing/allowance logic, cross-repository runtime adapters and an MCP/API endpoint are **not** implemented. The existing limited Flex Credit CLI is a separate working component.

## Typical workflow

1. **Scope:** current process, personas, channels, existing Salesforce clouds/org, volumes, NFRs, region, constraints.
2. **Source:** decompose process steps into capabilities; find functional-skill candidates in Headless Toolkit and exact product/feature/API docs in salesforce-docs; verify critical/recent claims in live official vendor pages; identify missing org evidence.
3. **Design:** compare native Lightning/LWC vs Multi-Framework vs Microfrontend vs HXL Beta vs API/MCP integration. Do not force headless if native is better.
4. **Validate:** auth, identity, permission checks, state changes, governance, eventing, latency, failure/retry, release and beta support.
5. **Price:** resolve required rights/licenses, offer/package inclusion versus add-on purchase, conditional dependencies and usage metrics for each implementation. Create a distinct bill of materials, deduplicate shared entitlements/allowances and delegate commercial evidence/calculation to existing pricing skills.
6. **Audit:** trace every material claim to an evidence URL, source repo/ref and timestamp. Record conflicts, unpriced meters and missing contract data separately.

## Deliverables

- Architecture Decision Record: alternatives, constraints, selected pattern, rationale and rejected options.
- Source/evidence register: fact, URL/section, repo/ref, observed date, VERIFIED/INFERRED/UNKNOWN/CONFLICTED.
- Capability-to-component map and integration contracts: clouds, APIs/events/MCP tools, data, ownership and governance.
- Bill of Materials and TCO: clearly partition licenses, usage/credits, implementation and ongoing operations. Give numeric estimates only for supported inputs.
- Risk/readiness matrix: beta/GA evidence, security, environments, required access, gaps, tests and owners.
- Executive-facing option comparison: native-first, hybrid/headless, and headless-first where feasible; separate product facts from recommended design.

See [source-manifest.yaml](source-manifest.yaml) for ownership and update discipline and [reference-registry.yaml](reference-registry.yaml) for resolvable pointers. Trace source changes back to affected skills, capabilities, process steps and BOM lines.

## Example request

> Assess a B2B wholesale telco sales workflow spanning Salesforce Communications Cloud, pricing/quoting, Microsoft Teams and a custom portal. Compare native Salesforce, hosted MCP, HXL and Multi-Framework; provide cited design alternatives, permission model, migration risks, and a price/usage scenario distinguishing known rates from UNKNOWN items.

## Known limitations

- Salesforce technical documents are a curated catalog, not a live org discovery service; last refreshed in that repo on 2026-11-06.
- Headless repo documents capabilities; deployment tooling, sandbox validation and actual target-surface behavior need separate proofs.
- HXL is Beta in captured docs; confirm current support and release status.
- Pricing feature branch is draft. Flex Credit CLI covers a limited set of meter scenarios; Headless Platform Interaction pricing may be TBA. A rate-card unit test is not proof of live billing parity.
- No GitHub/Claude/ChatGPT installation or MCP runtime connection is provided by this repository file alone.

