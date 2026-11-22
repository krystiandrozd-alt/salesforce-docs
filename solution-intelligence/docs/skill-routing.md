# Salesforce Solution Intelligence — skill ownership and routing

Version: 0.3.0 · 2026-11-22 · **Routing policy, not an installation claim**

This document routes work; it neither installs skills nor grants org access.
For pricing and licensing, use an actual connected GitHub tool and the exact
resolved ref/commit. The historical pricing seed is **not** a live price book.

## Deterministic ownership

| User intent | Owner / entry point | Supporting skill or source | Runtime and access gate |
| --- | --- | --- | --- |
| End-to-end business process → design → licenses, packages, billing | \`sf-solution-architect\` (Claude project skill) | Salesforce Docs, Headless Toolkit, pricing owner | Read-only discovery by default; no org or CLI required for public-source reasoning |
| Public Salesforce price, license, current edition, bundle | **Canonical** \`sf-pricing-intelligence\` (ChatGPT GitHub-first v0.2 where available; Claude project equivalent otherwise) | \`sf-pricing-research\`, \`sf-license-compare\`, \`sf-pricing-audit\` | GitHub read must actually succeed at a resolved ref; official product pricing page verified live |
| Explicit A/B or skill quality benchmark | **Experimental** \`sf-pricing-intelligence-spq-pilot\` | Shared controlled fixture set, held-out cases | Opt-in only; no default commercial routing or silent fallback |
| Credit scenario with explicit quantities | \`sf-flex-credit-estimate\` via pricing owner | \`pricing-intelligence/credit_calculator.py\` | Run CLI only if actual interpreter, source rate card and supported meter are available; otherwise NOT_RUN |
| Salesforce org metadata inventory / capability existence | Upstream \`platform-metadata-discovery-get\` if installed | Salesforce CLI or authorized Metadata Grounding/H360 MCP | Real, selected org required; do not infer entitlement from metadata |
| Inspect design-time architecture of **one named Agentforce agent** | Upstream \`agentforce-architecture-analyze\` if installed | Agentforce metadata via \`sf\` | Named or discovered agent and authorized target org; not runtime audit or pricing |
| Find potential Salesforce plugin/capability when **no matching leaf skill exists** | Upstream \`platform-capability-search\` **only with full Salesforce Development plugin installed** | Plugin's \`sf-context\` scripts | It is an internal discovery tool, **not** a general orchestrator; standalone skill install is insufficient |
| Agentforce native build / test / deploy | Official relevant Agentforce ADLC/skill, only on explicit request | Salesforce Development plugin and org | Verify CLI version, project and target org; separate consent for mutating actions |
| Prompt/skill quality review | Dedicated quality skill **only if actually discoverable**; otherwise documented manual rubric | Independent holdout rubric | \`skill-prompt-quality\` not present in PR's \`.claude/skills\`; local installation unknown |

**Precedence:** project architect > specialist discovery > one canonical pricing skill. If a pricing request is already specific, skip the architect stage. When the host exposes both ChatGPT pricing skills, prefer the GitHub-first skill for real commercial work; select SPQ pilot **only** for a named controlled A/B run, never because its description also matches.

The ChatGPT plugin is not automatically active in Claude Code. Project skills are not proof that connected GitHub, Salesforce, installed CLI, an MCP server or the Python runtime exists. A GitHub path or tool list is not proof that a file was read.

## Evidence and execution contracts

- **Source selection:** Salesforce Docs indexes find technical candidates. Headless Toolkit finds patterns. Live official technical docs verify technical claims. Pricing Intelligence and applicable official pricing/rate card/contract evidence verify billing claims. Customer contracts remain private.
- **No fabricated rights:** marketing offer ≠ SKU ≠ technical license ≠ permission ≠ runtime skill. A vendor skill existing in a registry does not establish that a customer can run it or that it is included in a package.
- **No silent duplicate engines:** ChatGPT GitHub-first and Claude project pricing skills share policy but are distinct runtimes. Do not execute both for the same question unless an explicit paired benchmark is requested. The SPQ pilot is not a pricing source.
- **Run truth:** SOURCE_VERIFIED requires inspecting exact source/section and applicable scope. A source reference, cache, model recollection or a synthetic graph cannot promote a claim. Arithmetic only through a calculator that actually ran; otherwise NOT_RUN.
- **No surprise installs/org operations:** never install packages, authenticate, deploy, mutate Salesforce org, invoke write-capable MCP actions or access customer contracts without the needed authorization.
- **Readiness test before use:** verify skill file **and** plugin manifest/required scripts, runtime version, connected tools and permissions. If a prerequisite is absent, report capability as unavailable and route to bounded manual investigation.
- **Skills upstream are versioned:** verify actual \`forcedotcom/sf-skills\` ref and release; skill availability may change. A forked listing is not proof of current upstream version.

## A/B quality assurance

Keep the baseline skills/prompt unchanged. Use [holdout cases](../examples/skills-holdout-cases.json) as inputs and [the benchmark runbook](../benchmarks/README.md) for independent grading; run baseline and optimized **on the same pinned sources, model and tools**, then independently grade outcomes. Record:
- routing precision (did the correct owner run?);
- source/ref and claim/edge trace completeness;
- license/edition/consumption semantic correctness;
- hallucinated SKU/price/license or unsupported availability (critical failure);
- execution truth (\`EXECUTED\` vs \`NOT_RUN\`);
- source and product generation applicability;
- prompt cost, latency and tool calls as secondary metrics.

An unexecuted benchmark plan is **NOT** an A/B result. Structural unit-test pass rates are separate from quality benchmark and live commercial correctness.
