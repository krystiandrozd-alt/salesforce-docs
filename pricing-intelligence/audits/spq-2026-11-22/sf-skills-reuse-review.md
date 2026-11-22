# Salesforce Skills reuse assessment for SPQ audit
As checked: 2026-11-22 | Source: https://github.com/forcedotcom/sf-skills (main)
Status: RECOMMENDATION ONLY — no Salesforce skills installed, no target org contacted, no original skill or prompt overwritten.

## Decision
Keep `skill-prompt-quality` as the offline lint and benchmark coordinator. Reuse Salesforce-maintained skills **only in their narrow native Salesforce scope**, not as a substitute for testing local Claude pricing skills. Prefer composition over copying upstream instructions; upstream names/versions may change.

| Upstream skill | Verified focus | Use with pricing intelligence |
|---|---|---|
| `agentforce-generate` (v0.11) | Agent Script / AiAuthoringBundle review, repair, local syntax validation, org-bound authoring and baseline/candidate repair | Use ONLY for native .agent implementation or review. Not for public pricing or `SKILL.md` quality. |
| `agentforce-test` (v0.8) | Agentforce preview, suites, tests, and optional OWASP adversarial cases | Use when native agent exists and an org/test environment is authorized; adapt the test-case taxonomy for offline Claude skill benchmarks, **not** the org test commands. |
| `platform-docs-get` (v1.2) | Authoritative Salesforce developer/help/architect documentation extraction | Use to confirm actual technical license, metadata and feature prerequisites. Published pricing/rate-card PDFs require their own source capture; this skill excludes PDF fallback and is not a quoting engine. |
| `agentforce-architecture-analyze` (v1.0) | Design-time inventory of topics, tools and Apex/Flows for an agent in a specific org | Optional later, when a pricing Agentforce agent is genuinely deployed. |
| `agentforce-observe` (v0.9) | Runtime session trace diagnosis and alert monitoring | Optional after agent deployment and telemetry availability. |
| `dx-code-analyzer-run` (v1.0) | Salesforce code scanning using specialized analyzers | Not a `SKILL.md`/prompt benchmark; use only for supported code/metadata as needed. |

## Instruction collision to gate explicitly
The upstream `agentforce-generate` skill instructs checking `sf config get target-org --json` and, if missing, `sf config set target-org <alias>`. The project's `sf-pricing-agentforce-bridge` requires preserving the default org and explicit `--target-org`. **Project safety rule wins; never silently change global/default org as a side effect of a quality audit.**

The upstream `agentforce-generate` says “ALWAYS --json” on *every* sf CLI command, while platform capability varies by command; check installed CLI help rather than repeating unsupported flags. Its guidance to read full JSON must NOT override project requirements to keep authentication secrets out of model responses/logs.

`agentforce-test` provides a REST action example extracting an access token via `sf org display`; that is outside a pure skill audit and must not be copied into ordinary testing instructions. Never handle live org access tokens to benchmark public pricing skills.

The project's historical pricing-rates contract remains independent from the upstream Agentforce development library. Upstream `platform-docs-get` verifies technical platform semantics, **not** quote/SKU prices.

## Benchmarks to run — distinct evidence types

### Offline SPQ checks (can run with no org)
- SKILL.md frontmatter, trigger/negative-trigger specificity, file/reference validity.
- Cross-skill duplicated policy blocks and incompatible output vocabularies.
- Candidate compared to original on static rubric, clearly labeled proxy metrics.
- Evaluate six pricing scenarios + four negative cases (no data, unpriceable Headless, conflict, forbidden org change). A text-only check does NOT prove activation.

### Live Claude Code A/B (not yet run)
- Equal Claude version, tool settings, repository state and rate-card snapshots.
- Blind holdout tasks for price retrieval, user license vs edition, included bundles, credit calculation, Headless unknown, and org-negative-trigger.
- Capture chosen skill, actual tool trace, grounded citations, result validity, refusals, time and tokens if measured. Compare paired run artifacts; no improvement claim without real results.

### Optional native Agentforce tests (not yet run)
- Only if a concrete Agent Script agent has been built and a nonproduction org is authorized.
- Use `agentforce-test` smoke/batch functional tests, then expressly approved security cases.
- Use `agentforce-architecture-analyze` for architecture differences, `agentforce-observe` for actual traces.
- These assess *the deployed Salesforce agent*, not a local Claude skill's routing quality.

## Recommended next action
Do not install the entire SF library for a pricing-prompt audit. Use `platform-docs-get` for technical evidence where needed, and borrow the *test design principles* from `agentforce-test`. Keep official lifecycle skills referenced by the Agentforce bridge, install only when an authorized Salesforce-native development workflow begins.

Sources (current main; check actual changes before deployment):
- https://github.com/forcedotcom/sf-skills/blob/main/skills/agentforce-generate/SKILL.md
- https://github.com/forcedotcom/sf-skills/blob/main/skills/agentforce-test/SKILL.md
- https://github.com/forcedotcom/sf-skills/blob/main/skills/platform-docs-get/SKILL.md
- https://github.com/forcedotcom/sf-skills/blob/main/skills/agentforce-architecture-analyze/SKILL.md
- https://github.com/forcedotcom/sf-skills/blob/main/skills/agentforce-observe/SKILL.md
- https://github.com/forcedotcom/sf-skills/blob/main/skills/dx-code-analyzer-run/SKILL.md
