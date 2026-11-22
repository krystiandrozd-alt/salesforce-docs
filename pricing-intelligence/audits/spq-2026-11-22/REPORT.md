# Skill & Prompt Quality v1.0 — Salesforce Pricing Skills Audit

Date: 2026-11-22
Baseline: feature/pricing-licensing-knowledge-graph-20261122 (draft PR #8).
Proposals: audit/spq-pricing-skills-20261122, under pricing-intelligence/audits/spq-2026-11-22/candidates.
Scope: six Claude SKILL.md files, CLAUDE.md, AGENTS.md, build-graph prompt, agent I/O contract, and private ChatGPT plugin.
Method: SPQ v1.0 AUDIT-LIBRARY / AUDIT-SKILL / AUDIT-PROMPT / OPTIMIZE / BENCHMARK DESIGN.
**Decision: REVIEW / PILOT ONLY. Never overwrite the originals without user approval.**

## Findings

| ID | Priority | Evidence | Improvement |
|---|---|---|---|
| F01 | HIGH | Repo and ChatGPT plugin maintain separate orchestrator instructions without synchronized version/release. | Define a versioned shared policy source; embed a policy snapshot in the independently deployed plugin; diff revisions at release. |
| F02 | HIGH | Five of six original skills lack an explicit negative activation phrase in a simple static check. | Add narrow positive and negative skill triggers and a priority router (public pricing is not native Agentforce development). |
| F03 | HIGH | Existing 18 code/metadata tests do not execute Claude skill selection or answer behavior. | Add 16 paired scenarios (12 development, 4 independent holdout); compare the exact same runner/model/tools with external graders and captured traces. |
| F04 | HIGH | Private plugin cannot independently invoke the local Python rate engine. | Capability gate; EXECUTED vs NOT_RUN status; require an actually connected adapter before claiming live calculations. |
| F05 | MEDIUM | Pricing/credential prohibitions and output rules repeat across the router, specialists, AGENTS, docs and plugin references. | One AGENTS contract plus short specialist instructions; plugin embeds self-contained policy because repo may be unavailable. |
| F06 | MEDIUM | Existing 1,624-word build prompt combines discovery, schema, graph, ingestion, testing and integrations into one run. | Stage A evidence/schema → B graph/query → C integrations, each with an exit gate; preserve original detailed acceptance list. |
| F07 | MEDIUM | Estimate specialist mixes public calculator workflow with org details and points to example scenario, not necessarily user inputs. | Require actual scenario JSON, native meter discovery, rate applicability and explicit execution outcomes; no org login for public research. |
| F08 | MEDIUM | Agent I/O example reports source_status "VERIFIED_OR_UNKNOWN", not a supported atomic evidence status. | Canonical statuses: SOURCE_VERIFIED, INFERRED, UNKNOWN, CONFLICTED. Distinguish source, code execution and commercial readiness. |
| F09 | MEDIUM | Audit skill requires Python tests for every audit, including one public pricing claim. | Run code tests only for calculation/code changes; use source corroboration for pricing assertions. |
| F10 | REVIEW | Agentforce bridge holds important CLI/org auth safety procedures; aggressive shortening may omit some detail. | Retain verified org/credential/approval invariants in shared AGENTS and official ADLC reference; do adversarial deployment tests before acceptance. |

## Static original versus candidate comparison

Method: words split by whitespace, file readback, and explicit negative-boundary phrase detection. **These measurements are NOT agent behavior, latency, token usage, accuracy, or a live Claude benchmark.**

| Skill | Original words | Proposed words | Negative trigger in baseline | Negative trigger in proposed |
|---|---:|---:|---|---|
| sf-pricing-intelligence | 601 | 257 | No | Yes |
| sf-pricing-research | 235 | 206 | No | Yes |
| sf-license-compare | 239 | 189 | No | Yes |
| sf-flex-credit-estimate | 242 | 206 | No | Yes |
| sf-pricing-audit | 241 | 221 | No | Yes |
| sf-pricing-agentforce-bridge | 697 | 235 | Yes | Yes |
| **Total** | **2,255** | **1,314** | **1/6** | **6/6** |

Proposed skill text is shorter by 941 words (41.7%). All six candidate skill frontmatter name/description fields were present in direct readback.
Baseline build-graph prompt: 1,624 words. Initial proposed staged prompt: 572 words before its final reminder preserving the baseline's full acceptance requirements.

**Warning:** shorter text is not evidence of a better response. This only measures instruction brevity and negative-trigger syntax.

## Benchmark protocol — NOT YET RUN

See paired-eval-suite.json: 16 cases covering exact routing, cross-cloud license semantics, native-rate units, Headless TBA, missing CLI, denied org access, public-vs-technical Agentforce, currency conflicts, malicious source instructions and unrelated requests. The four holdout cases are separate from revision-time cases.

Both original and candidate runner statuses remain NOT_RUN.
For genuine attribution: fix same Claude Code version/model/config, official source snapshots, available GitHub access and tool permissions. Capture prompts, tool traces, stdout/stderr, source citations, critical safety failures, independent grade, elapsed time and tokens only if observed.

A candidate is not promotable if it regresses on any critical confidentiality/org-action/false-quote case. If correctness is not better and any measured overhead gain is insignificant, keep originals.

## Proposals preserved separately

- candidates/skills/{six skill names}/SKILL.md
- candidates/AGENTS.md and candidates/CLAUDE.md
- candidates/prompts/build-graph.md
- candidates/plugin/SKILL.md and candidates/plugin/default-prompts.md
- paired-eval-suite.json
- pricing-intelligence/tests/test_spq_static.py for structural checks, not model behavior

These are **not** installed, merged, or substituted for .claude/skills, the existing PR #8 prompts, or the private ChatGPT plugin. The user must approve promotion of particular changes.

## Recommendation

1. Pilot the concise router and shared AGENTS policy first.
2. Resolve the runtime truth boundary: the installed ChatGPT plugin cannot call the repo calculator unless an actual adapter is available.
3. Run paired Claude Code evals and separately benchmark the ChatGPT plugin; do not combine the results.
4. Only then consider adopting shorter specialist skills, staged build prompt and new plugin release. Keep original Agentforce bridge steps as reference until adverse security tests pass.

Evidence: inspected GitHub PR #8 files, Plugin Creator read-only initial release 0.1.0, Skill & Prompt Quality v1.0 saved library SKILL.md. Code fixture CI from PR #8 is unrelated to this skill behavioral comparison.
