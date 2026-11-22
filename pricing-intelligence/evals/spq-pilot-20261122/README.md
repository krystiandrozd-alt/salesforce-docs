# SPQ Salesforce Pricing Skills — Pilot Release (2026-11-22)

**Scope:** Six active Claude pricing skills, AGENTS.md, CLAUDE.md and build-graph.md on a dedicated pilot branch. No merge to main or Salesforce org change.

## Implemented

- Replaced six .claude/skills/sf-*/SKILL.md files only on this pilot branch, with explicit triggers, capability gates and shared source/permissions contract.
- Centralized evidence, licensing, credentials and calculation safeguards in pricing-intelligence/AGENTS.md.
- Reduced project Claude instructions and staged build prompt.
- Archived exact original complete build acceptance checklist at pricing-intelligence/prompts/reference/build-graph-acceptance-v1.md.
- Added six static SPQ checks validating original Git revisions, policy invariants and 16 prepared paired eval cases (12 development / 4 holdouts).

## Original and rollback

Original Git commit: 6da8886c2cf2f1aecceb9270398dd98b0673b6e7, from draft PR #8.
Audit proposal: draft PR #9 (audit/spq-pricing-skills-20261122).
Pilot branch: feature/spq-pricing-skills-pilot-20261122.

Rollback: revert the pilot PR, or restore the six active skills and AGENTS.md/CLAUDE.md/build-graph.md directly from the original commit. The canonical source history is untouched.

## Benchmarks and constraints

Preliminary candidate text measured 2,255 → 1,314 whitespace words (-41.7%) and negative skill trigger coverage of 1/6 → 6/6. Active pilot safety clarifications change final word count; CI prints actual current counts.
Those numbers measure text only, not Claude correctness, latency, tokens or real behavior. All sixteen actual original-vs-pilot Claude evaluations remain NOT_RUN.

Run from repo root (full Git history required for baseline assertions):

    python -m unittest discover -s pricing-intelligence/tests -v
    python pricing-intelligence/credit_calculator.py --scenario pricing-intelligence/examples/agentforce-example.json

Tests check local pricing fixtures and static safety contracts; they do not prove Salesforce quoting or billing parity.

## Promotion gate

Run the same 16 prompts on original and pilot under identical Claude Code model, settings, tools, rate card, public-source snapshots and repository access. Capture routing, outputs, source citations, executed command logs, missing tools, external independent grades, and measured time/tokens when available.

Block release on any credential exposure, unauthorized org change, invented binding quote, TBA-as-zero, or holdout regression. If the paired runs are missing, label behavioral improvement INCONCLUSIVE.

The original private ChatGPT pricing plugin remains unchanged: https://chatgpt.com/plugins/plugins_6b02de2e09948191b22c8a38645cc902 .
A **separate private pilot plugin** was created for a clean A/B comparison without overwriting it: https://chatgpt.com/plugins/plugins_6b0310056314819187b100d9b96317a8 .
The pilot's source is the independently packaged SPQ-reviewed skill and policy snapshot. Neither plugin contains a live GitHub connector or hosted rate calculator; compare only under the same actual tool and source availability.

## Side-by-side ChatGPT plugin benchmark

1. Open the baseline plugin and the pilot plugin separately, with the same model and tool permissions where supported.
2. Use the same prompts from paired-eval-suite.json, including R01-R12 development cases and H01-H04 holdouts. Keep default prompt wording unchanged between the two plugins.
3. Capture actual response, source URLs/sections, tool-execution evidence, unpriced items and any unintended Salesforce org behavior for each run.
4. Grade independently against expected_skill and must_observe. Missing execution or untrusted quote = failure; do not award points merely for repeating safety text.
5. Record observed cost/latency only if the platform exposes them. Promotion stays blocked while baseline/candidate statuses are NOT_RUN.

**Release state: PILOT BRANCH — CI can pass, but live Claude behavior benchmark and commercial contract validation remain required.**
