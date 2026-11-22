# SPQ pricing skills — pilot deployment record

Date: 2026-11-22
Approval: user message "Deploy" following the Skill & Prompt Quality audit and official Salesforce Skills reuse assessment.
Target: `feature/pricing-licensing-knowledge-graph-20261122` via review PR #14. This is NOT production `master`, a Salesforce org, or a customer quote pipeline.

## Applied in this release
- Deploy the shortened routing instructions from SPQ candidates for five pricing skills: orchestrator, public price research, license comparison, deterministic Flex Credit estimation, and pricing audit.
- Centralize shared restrictions in `pricing-intelligence/AGENTS.md`; `CLAUDE.md` routes without reprinting those rules.
- **Keep** the full original `sf-pricing-agentforce-bridge` steps. Add the documented upstream `agentforce-generate` compatibility guard: never run `sf config set target-org` implicitly; require an explicit `--target-org`; do not print authentication JSON/secrets.
- In research/licensing skills, refer to Salesforce `platform-docs-get` only if installed for technical license documentation. It does **not** establish published commercial price/contract applicability.
- Add `pricing-intelligence/prompts/build-graph-staged.md` to run evidence/schema → query graph → optional integrations behind gates; **preserve** original `prompts/build-graph.md` as the comprehensive acceptance matrix.
- Carry forward all six alternative candidates, original SPQ findings and the upstream reuse review for rollback and comparison.
- Add 14 additional mixed development/holdout scenario specifications; **NOT_RUN**, no fabricated Claude behavior.
- Update deterministic CI suite with regression guards for negative skill routing, output statuses, default-org protection, staged prompt preservation and official docs boundary.

## Verification / rollout gates
1. GitHub Actions tests must pass on PR #14's head.
2. Inspect changes: no source price data, engine mathematics, OAuth keys, private customer documents, default org, Salesforce deployments or procurement operations are touched.
3. Merge PR #14 only to the existing pricing feature branch; keep draft PR #8 unmerged pending independent review.
4. Pilot in Claude Code checkout of the pricing feature branch. Existing commands from repo root:
   - `python pricing-intelligence/credit_calculator.py --list-meters`
   - `python -m unittest discover -s pricing-intelligence/tests -v`
5. Before calling this a behavioral improvement, run paired baseline vs candidate Claude Code tasks (model, tools and source snapshots equal), retain traces, evaluate independent holdouts and stop on critical regression. `audits/spq-2026-11-22/paired-eval-suite.json` and `eval-suite.json` are designs, not run results.

## Separate private ChatGPT plugin
The `salesforce-pricing-intelligence` plugin is independently released and currently observed at **0.2.0**, with a newer GitHub-first workflow. This deployment intentionally **does not overwrite** that plugin from the older v0.1.0 ZIP. A plugin release needs a separate source reconciliation and real host behavior tests. No claim of synced plugin instructions or connected calculator is made.

## Known limitations
- CI only validates deterministic Python calculator fixtures and static instructions. It does not test actual Claude skill activation, citations or commercial source truth.
- No complete Salesforce licensing knowledge graph, real-time pricing collector, hosted MCP/API bridge or native Agentforce org deployment is provided by this release.
- The historical rate-card transcription remains subject to original PDF/contract validation.
- The existing source observations, seed and engine are unchanged; pricing eligibility is not automatically validated.

Rollback: restore the affected files from the pre-release commit on `feature/pricing-licensing-knowledge-graph-20261122`, or revert PR #14's merge commit. The candidate and audit directories are informational and not automatically activated as skills.
