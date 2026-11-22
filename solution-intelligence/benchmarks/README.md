# Controlled baseline vs optimized skill benchmark

**Status: PREPARED, NOT EXECUTED** for actual Claude/ChatGPT responses.

Inputs:
- Holdout cases: [six prompts](../examples/skills-holdout-cases.json).
- Baseline: skills/prompts at original PR #10 head \`0c6c921a7e53774a760983c4aad511dc3dece55b\`.
- Optimized: current PR head (resolve immutable SHA and record it for each run).
- Both cohorts must use the **same** model, settings, vendor source snapshots, tool permissions, customer/org access and independent evaluator.

For each of the six cases, obtain genuine agent responses under both configurations, save response artifacts and tool logs, and have an independent reviewer score **six Boolean checks**: \`routing_correct\`, \`source_trace_complete\`, \`license_semantics_correct\`, \`no_unsupported_claims\`, \`execution_truth\`, \`applicability_correct\`. False on \`no_unsupported_claims\` or \`execution_truth\` is a critical candidate failure.

Store results in separate, private JSON files (do not commit customer data); each must have:

```json
{
  "model": "exact-model-version",
  "source_snapshot_id": "same-immutable-source-bundle",
  "tool_profile": "same-connected-tools-and-permissions",
  "reviewed_by": "independent-reviewer-id",
  "responses": [
    {
      "case_id": "H01",
      "artifact_ref": "path-or-record-for-actual-response",
      "review": {
        "routing_correct": true,
        "source_trace_complete": true,
        "license_semantics_correct": true,
        "no_unsupported_claims": true,
        "execution_truth": true,
        "applicability_correct": true
      }
    }
  ]
}
```

Include **all six** case IDs H01–H06 in each cohort; snippet above is only a schema illustration, **not a recorded result**. Do not fabricate or self-grade the model responses.

From the repository root after running the two cohorts:

```bash
python solution-intelligence/benchmarks/compare.py \
  --cases solution-intelligence/examples/skills-holdout-cases.json \
  --baseline /private/review/baseline.json \
  --candidate /private/review/optimized.json

python -m unittest discover -s solution-intelligence/tests -v
```

The comparer refuses missing/duplicate cases, missing independent reviewer, inconsistent model/snapshot/tool profile or missing Boolean review scores. Exit code 3 means at least one critical candidate failure; exit code 2 means input blocked. Comparer output is a **graded skills benchmark**, not validation of Salesforce contract terms or invoicing. Track latency, token usage and tool calls in run logs separately; they are not scored as evidence correctness.

**Current objective facts:** synthetic resolver tests and synthetic comparator tests can execute in CI; actual Claude/Codex/ChatGPT paired runs have **not** been performed through this repository workflow.
