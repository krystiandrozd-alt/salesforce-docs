# Process, capability, license and billing contract

Version: 0.2.1 · 2026-11-22 · **Design contract; a synthetic-only structural pilot exists, but the full commercial resolver is not implemented.**

The runnable [structural pilot](../RESOLVER-QUICKSTART.md) tests a strict subset of this contract. It supports explicit functional-skill queries, preliminary offer dependency inspection and claim/source impact; however it does not ingest the registries, verify actual licensing, establish customer eligibility or calculate prices. Its `evidence_verified` flag is intentionally false until trusted independent source attestation exists.

## Contents

1. [Purpose and ownership](#purpose-and-ownership)
2. [Entities](#entities)
3. [Typed relationships](#typed-relationships)
4. [References and evidence](#references-and-evidence)
5. [Resolution algorithm](#resolution-algorithm)
6. [Commercial handoff and billing](#commercial-handoff-and-billing)
7. [Query contract](#query-contract)
8. [Acceptance cases](#acceptance-cases)

## Purpose and ownership

Answer: **For this designed business process, function or functional skill, which implementation can deliver it, which rights/licenses are required, in which offer/package are they available, and how is each part billed?**

Preserve three source owners: SF Docs for technical discovery; Headless Toolkit for implementation patterns and the catalog of functional skills; Pricing Intelligence for commercial offers, entitlements, dependencies, allowances and rates. The solution layer owns requirements and joins these sources using stable IDs and evidence-backed claims. It does not duplicate their catalogs or calculators.

Resolve source locations through [the reference registry](../reference-registry.yaml) and [source manifest](../source-manifest.yaml). Use [the resolver prompt](../prompts/resolve-process-commercial.md) for agent execution and [the pricing build prompt](../../pricing-intelligence/prompts/build-graph.md) for implementation. A reference ID locates a source; it is not evidence that the source proves a claim.

The shared UI-surfaces project material can seed requirements such as account preparation, quotation and follow-up across Claude, Teams or a portal. Treat those scenarios as design input, not as verified product availability or license evidence.

## Entities

Use immutable IDs; aliases and display names are searchable attributes, never join keys. Preserve upstream IDs and namespace them by provider, product and version. Retain the existing Pricing Intelligence IDs instead of minting duplicate commercial records.

| Entity | Required information and distinction |
| --- | --- |
| `process` / `process_step` | Business outcome, sequence/branch, persona and requirement IDs; optional cited eTOM/TMF mapping. |
| `capability` | Atomic business function and acceptance criteria, independent of its UI or implementation. |
| `functional_skill` | Runtime business behavior, native skill ID, provider, inputs/outputs, actions, supported surfaces, effects and version. Multiple capabilities and multiple actions are possible. |
| `delivery_skill` | Instructions used by Claude/developers to design, build or validate software. Its availability does not establish a customer's runtime entitlement. |
| `implementation_option` | A concrete alternative: native configuration, vendor skill, custom API/MCP, Flow/Apex, HXL or another supported route; components and dependencies. |
| `technical_feature` / `product_variant` | Exact product/subproduct, generation, release and API/component identity. Preserve Communications managed-package versus core implementations; do not equate similarly named CPQ or ordering features. |
| `surface` / `integration_component` | Claude, Teams, portal, SDK, API or MCP endpoint; execution context, acting identity and read/write behavior. A surface is not the underlying business capability. |
| `access_entitlement` | Commercially permitted use, actor/access class, environment, restrictions and scope. |
| `technical_license` / `permission_requirement` | User license, permission-set license, package entitlement or org entitlement as evidenced; permissions/configuration are tracked separately from purchased rights. |
| `commercial_offer` | Edition, bundle, add-on or credit pack. An orderable SKU is a separate optional entity and is populated only with evidence. A commercial package is not a Salesforce managed package. |
| `requirement_group` | `group_id`, `operator` (`ALL_OF` / `ANY_OF`), nonempty `member_ids`, structured conditions and claim IDs; members may be nested groups, entitlements or prerequisites. E.g. a base entitlement AND one eligible add-on route. |
| `pricing_metric` / `price_observation` | Charged activity/unit and a dated price with geography, currency, unit denominator, qualifier, display period and billing cadence. |
| `entitlement_allowance` / `credit_pool` | Amount/unit, owner and scope, eligible meters, validity/reset period, environment, pooling and overage rules. Missing reset or pool rules remain unknown. |
| `source_snapshot` / `sourced_claim` | Exact source version and the claim it supports; technical and commercial evidence may be different. |

Treat a designed/custom functional skill as `design_state: PROPOSED` until implemented and verified. Treat catalog skill entries as candidates until their exact feature, support conditions and current commercial prerequisites have been checked. A custom skill may have no separately marketed license while its components still require paid rights or metered usage.

## Typed relationships

The following relationship names and directions are the bridge contract. Reuse an existing pricing relation when its meaning is identical; otherwise define an explicit adapter. Do not silently reinterpret a similarly named edge.

| From | Relation | To | Meaning |
| --- | --- | --- | --- |
| Process | `HAS_STEP` | Process step | Process decomposition. |
| Process step | `REQUIRES_CAPABILITY` | Capability | Required outcome at this step. |
| Functional skill | `DELIVERS` | Capability | Runtime behavior satisfies the stated acceptance criteria, wholly or partially. |
| Delivery skill | `SUPPORTS_BUILD_OF` | Implementation option | Authoring/validation support, not a runtime licensing link. |
| Capability | `REALIZED_BY` | Implementation option | Candidate or selected realization of the capability. |
| Implementation option | `USES_SKILL` | Functional skill | Selected runtime skill where applicable. |
| Implementation option | `USES_FEATURE` | Technical feature | All relevant underlying components must be enumerated. |
| Implementation option | `EXPOSED_ON` | Surface | Validated surface and execution context. |
| Technical feature | `PART_OF` | Product variant | Exact product/generation owning the feature. |
| Technical feature / implementation option | `REQUIRES` | Requirement group / entitlement / technical license / permission requirement | Typed target preserves commercial versus technical requirements. |
| Requirement group | `HAS_MEMBER` | Requirement group / entitlement / technical license / permission requirement / offer | Membership interpreted by the group's `ALL_OF` / `ANY_OF` operator. |
| Access entitlement | `PROVISIONED_AS` | Technical license | Optional evidenced mapping from purchased rights to technical license provisioning; never assume one-to-one equivalence. |
| Commercial offer | `INCLUDES` | Entitlement / allowance / other offer | Included only for the proven scope, amount and conditions. |
| Commercial offer | `AVAILABLE_FOR_PURCHASE` | Add-on offer | Purchasable separately; does not mean included. |
| Commercial offer / entitlement | `REQUIRES` / `ELIGIBLE_WITH` | Other offer / entitlement | Required prerequisite versus eligibility, respectively. |
| Commercial offer | `BILLED_BY` | Pricing metric | How the commercial offer is charged. |
| Implementation option / technical feature | `GENERATES_USAGE` | Pricing metric | Conditional billable activity; requires its own metering evidence. |
| Pricing metric | `USES_CREDIT_POOL` | Credit pool | Consumption draws from this pool when conditions match. |
| Price observation | `PRICES` | Pricing metric | Metric alone does not identify a price; observation also identifies the offer/purchasing model and applicability. |
| Entitlement allowance | `OFFSETS` | Pricing metric / credit pool | Deduct only the allowance proven applicable to that scope. |

These are many-to-many relations. One process can need several offers, and several processes can reuse the same entitlement. The resolver must follow required dependencies recursively, detect cycles and preserve alternative `ANY_OF` routes. Never combine alternatives into a single mandatory purchase list.

## References and evidence

Every material relationship and price observation needs an independent claim record. A single citation attached to the product node cannot prove all incident edges.

Minimum claim envelope:

```yaml
claim_id: CLAIM-EXAMPLE-001
subject_id: FEATURE-EXAMPLE
predicate: REQUIRES
object_id: ENTITLEMENT-EXAMPLE
evidence_status: UNKNOWN
lifecycle_status: ACTIVE
applicability:
  product_variant_id: null
  release: null
  region: null
  currency: null
  actor_type: null
  access_mode: null
  environment: null
  purchasing_model: null
  conditions: []
evidence_refs: []
derived_from_claim_ids: []
observed_at: null
effective_from: null
effective_to: null
freshness_status: NOT_CHECKED
gap: "Illustrative structure only; no product or licensing assertion."
```

For an evidenced claim, each `evidence_ref` resolves to `reference_id`, `snapshot_id`, original official URL, section/table/row or other precise locator, retrieval timestamp, and supported fact. For repository-derived evidence also capture repository, resolved commit SHA, path and content hash. Record publication/effective dates only when the source states them; retrieval time is not an effective date. A URL alone is insufficient.

Use `VERIFIED`, `INFERRED`, `UNKNOWN`, `CONFLICTED` for evidence. Adapt pricing's `SOURCE_VERIFIED` to `VERIFIED` only for the exact assertion, preserving the original status and provenance. Keep `RETIRED` as a lifecycle state, not a confidence level. Freshness, source availability and customer applicability remain separate fields. A public offer can be verified while the customer's eligibility remains unknown.

If a required condition is missing, return unresolved applicability rather than treating null as a wildcard. Explicit source statements of unrestricted applicability are different from missing conditions. Semantic similarity may suggest a candidate edge but can never promote it to `VERIFIED`.

Store applicability conditions as data predicates (`field`, allowlisted `operator`, `value`, supporting claim IDs), with nested `ALL_OF` / `ANY_OF` groups. Preserve explanatory source text alongside them. Do not execute arbitrary expressions from sources. If a condition cannot be normalized safely, retain it as unresolved and block unconditional eligibility. Aliases may include Polish/English search terms; aliases do not merge product generations or license identities.

Resolve conflicts by subject, predicate, version, region, actor and validity window. Evidence for different variants may coexist. An unresolved conflict for the same scope blocks a firm conclusion; preserve both claims. Do not automatically prefer a newer marketing page over governing terms. Authorized customer contracts apply only inside their private scope and must never be committed to this public-source catalog.

Reference integrity requirements:

- Local document links resolve relative to the linking file; registry paths resolve from their declared repository root.
- Resolve a branch to an immutable commit for every run and save that SHA in the run manifest. A moving branch is a discovery pointer, not a replayable citation.
- Validate reference IDs, node IDs, endpoints and allowed relation types; report orphan references explicitly.
- Use the original vendor source to substantiate current technical/commercial facts. A catalog summary, implementation prompt or source index is discovery/context evidence.
- Keep a reverse index from source/claim to capability, skill, process and BOM line so a source change marks affected results for revalidation.
- Unknown commercial information stays `null` with a gap reason; absence of evidence does not mean excluded, free or unnecessary.

## Resolution algorithm

1. Normalize the request into process steps, required capabilities and acceptance criteria. Preserve the original user wording. Capture region/as-of date, product generation, actor, surface, access mode and environment; separate supplied facts from assumptions.
2. Retrieve candidate functional skills and technical features with IDs, aliases and semantic search. Also find custom implementation alternatives. Name matches are candidates only.
3. Resolve each candidate against SF Docs and Headless Toolkit. Confirm feature variant, surface support, permissions, identity and side effects. Do not assume a Sales Cloud skill implements a Communications Cloud CPQ or MACD process.
4. Traverse typed `REQUIRES` groups to collect entitlements and technical prerequisites. Select only applicable `ALL_OF` / `ANY_OF` paths. Keep unresolved conditions, cycles and contradictory claims visible.
5. Find the commercial offers that include the required rights. Distinguish included, separately purchasable, eligible, explicitly excluded and unknown. Verify dependencies and alternative buying models.
6. Join each selected offer and each evidenced usage event to its metric, price observations and allowance rules for the same region, date and model. Check underlying multi-action usage and dependent services; one skill/tool invocation is not necessarily one billed action.
7. Compare against supplied existing entitlements in a separate customer overlay. Deduplicate by entitlement, owner/scope, environment and period, not just display name. Report required, already owned, incremental purchase and unknown separately. Unknown ownership is not zero ownership.
8. Produce traceable alternatives and a commercial BOM. Calculate only supported, applicable lines through the existing calculator. Retain incomplete routes rather than hiding them from search.
9. Return coverage for every requested step/capability and reverse impact links. Replaying the same source snapshots and assumptions must reproduce the same structural result.

Search must work forward (process → licenses and billing) and backward (offer/license/price change → affected capabilities, skills and processes). Rank implementation fit and evidence coverage separately from commercial cost. Never rank an unpriced route as cheapest.

## Commercial handoff and billing

Keep the bridge envelope separate from the existing [calculator contract](../../pricing-intelligence/docs/agent-io-contract.md). Its input schema is not a general license resolver.

The handoff contains `request_id`, `capability_ids`, `implementation_option_id`, entitlement/offer candidate IDs, requirement groups, billable-event-to-metric claims, existing-entitlement evidence, quantities/periods, region/currency, resolved reference snapshots and blockers. Pricing returns sourced offer/entitlement/allowance/rate IDs and qualified results. Join on IDs, never generated names.

Maintain a BOM as distinct lines: base subscriptions, add-ons, prepaid capacity/credit packs, estimated usage consumption, external workspace/runtime licenses, implementation and operations. Consumption estimates are not automatically extra invoice lines on top of purchased packs. Identify alternative buying models explicitly. Do not sum per-user fees and credits unless the applicable model requires both.

For each charge retain: `offer_id`, `pricing_metric_id`, `quantity`, native unit and unit size, original currency, price qualifier, displayed period, billing cadence, commitment period, minimum purchase, environment, allowance/pool/reset rules, overage and effective dates. Unknown fields stay unknown. A monthly display price does not establish a monthly contract or invoice cadence. A published "from" price does not establish the payable total.

Use `--list-meters` to discover supported estimator IDs; store an explicit adapter from graph metric IDs to returned meter IDs. Keep the current scenario schema unchanged. Block the dependent calculation when quantities, model compatibility or allowance applicability cannot be established; an explicitly requested gross scenario may use a clearly declared zero-allowance assumption. Report supported subtotals alongside unpriced lines; do not call the subtotal total cost. The current single-allowance interface cannot establish multi-pool/period allocation or full solution TCO.

## Query contract

Proposed operation: `resolve_process_commercial_requirements` (design name only; no tool registration exists yet).

Input: text or known process/capability/functional-skill IDs; context and as-of date; desired detail; optional existing-entitlement references and scenario volumes. Missing context permits candidate discovery, but blocks unconditional eligibility/price conclusions where relevant.

Output envelope:

- `contract_version`, `request_id`, `as_of`, `resolved_source_refs`, input facts and assumptions.
- `route_status`: `RESOLVED` / `PARTIAL` / `AMBIGUOUS` / `NO_VERIFIED_ROUTE` / `BLOCKED_BY_CONFLICT`. This describes mapping coverage, not purchasability or quote approval.
- `coverage`: requested, mapped, partial and unmapped step/capability IDs with reasons; no omitted requirements.
- `alternatives`: candidate and selected implementation IDs with required dependency groups and fit rationale.
- `rows`: process/step, capability, functional skill (nullable), product variant/feature, implementation, required entitlement/license, commercial offer, inclusion state, charge model, unit, cadence, allowance scope, evidence status and gaps.
- `trace_paths`: ordered node/claim IDs from each requirement through feature and entitlement to offer and billing evidence. A table row links to its own path.
- `commercial_bom`, optional unchanged calculator scenario/output, `calculation_status` (`NOT_RUN`, `BLOCKED`, `PARTIAL`, `CALCULATED_SUPPORTED_SCOPE`), assumptions, unpriced lines and customer-applicability status.
- `conflicts`, `gaps`, `refresh_required`, and evidence registry containing original URLs and exact locators.

When no verified route is found, state the searched sources and missing link. This is not proof that Salesforce cannot deliver the capability or that no suitable license exists.

## Acceptance cases

The implementation prompt must turn these into executable tests with synthetic fixtures, followed by separately evidenced vendor examples. They are future acceptance requirements, not tests already run.

| Case | Expected behavior |
| --- | --- |
| Designed telco quote-to-order with vendor skill and custom MCP alternatives | Preserve alternatives; enumerate underlying features, rights and meters separately. |
| Functional `account-context` candidate versus a developer authoring skill | Runtime skill and delivery skill remain different types; neither name establishes a license. |
| Same feature name in managed-package and core variants | No implicit equivalence; return separate scoped candidates. |
| Feature available as an add-on | Never show it as included in the base edition. |
| Base entitlement AND one of two add-ons | Enforce `ALL_OF` and `ANY_OF`; do not require both alternatives. |
| Included credits with unknown reset period | Preserve published quantity; block annual/monthly allowance derivation. |
| Several capabilities use one shared allowance | No duplicate deduction; evaluate owner, pool, environment and period. |
| One skill invokes several actions/services | Meter each supported billable event; never multiply by a guessed action rate. |
| Missing org entitlement evidence | Distinguish public requirements from unknown customer readiness. |
| Unknown price or meter | Return unpriced line and partial result; do not use zero or cheapest ranking. |
| Stale, retired or conflicting commercial claim | Exclude from unconditional current eligibility; expose history/conflict. |
| Changed package inclusion or billing metric | Reverse lookup identifies affected skills, process steps and BOM lines. |
| Missing reference, dangling edge, wrong endpoint type or cycle | Fail reference/graph validation or return an explicit blocker. |
| Same snapshots and input repeated | Deterministic paths, coverage and supported arithmetic. |

First implementation slice: one telco process with at least two functional capabilities, two implementation alternatives, a verified included/add-on distinction and one deliberately unresolved commercial dependency. Expand only after source-to-answer paths can be reproduced. Validate factual claims live; synthetic tests establish behavior, not vendor truth.
