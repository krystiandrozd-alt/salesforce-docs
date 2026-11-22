---
name: du-pipeline-coverage
description: Compares Salesforce pipeline with the required coverage against quota and flags deals that need attention (du MCP actions). Use when the user asks about pipeline coverage, coverage ratio, whether the pipeline is enough to hit the number, or which deals need attention.
---

# du Pipeline Coverage

## Tools

- Salesforce connector: `du_pipeline_coverage`. Use `du_find_records` when the user names a specific deal or owner.
- For approved fixes only: `du_opportunity_update` and `du_activity` (always `dryRun=true` first).

## Steps

1. **Inputs.**
   - Period: default is the current quarter. State it.
   - Quota: required for coverage. If missing, ask once. If the user has none, run without it and report pipeline only.
   - Coverage target: default 3x.
   - Owner: optional. Stale days: default 21.
2. **Run** `du_pipeline_coverage`. If the user wants a team view, run it once per owner.
3. **Explain the math** in one line: coverage = open pipeline closing in the period ÷ (quota − closed won).
   - Show the remaining amount to quota, the required pipeline at target, and the gap.
   - Weighted pipeline is a sanity check, not a forecast.
4. **Deals needing attention.** Group by reason, largest amount first:
   - Close date passed
   - Stale, no activity
   - Stuck in stage
   - No next step or no amount
   - Closing soon at low probability
   For each deal, give one concrete action (update the close date, book a call, confirm budget). Never invent facts about the deal.
5. **Output.**
   - Short summary in chat: status, coverage, gap, top 5 deals.
   - If the user wants something to share, build a Dashboard artifact from the tool's JSON.
6. **Hygiene fixes.** Propose them with `du_opportunity_update` or `du_activity` using `dryRun=true`. Apply only the items the user explicitly approves.
