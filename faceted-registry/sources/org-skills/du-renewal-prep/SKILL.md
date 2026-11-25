---
name: du-renewal-prep
description: Evidence-based renewal assessment and execution plan for a customer contract, from Salesforce (du MCP actions), mail and calendar. Use when the user asks to prepare a renewal, find contracts close to renewal, assess renewal risk, or build a renewal plan for an account or contract.
---

# du Renewal Prep

Read-only assessment first. Nothing is written to Salesforce, sent or scheduled without the user's explicit approval of the exact change.

## Tools

- Salesforce connector: `du_find_records`, `du_contract_renewals`, `du_renewal_baseline`, `du_OrderSummaryMcp`; for approved changes only `du_opportunity_update` and `du_activity` (always `dryRun=true` first).
- Mail: Gmail or Microsoft 365 connector, when enabled.
- Calendar: Google Calendar or Microsoft 365 connector, when enabled.
If a source is not connected, say so once and mark its facts as unknown. Never assume billing, usage or support data exists.

## Steps

1. **Scope.**
   - No account or contract given: call `du_contract_renewals` (default 120 days) and show the list sorted by urgency, then ask which one to prepare.
   - Name given: call `du_find_records`. If several records match, ask the user to choose. Never pick for them.
2. **Baseline.** Call `du_renewal_baseline` with the contract Id (or account). If it returns `needsSelection=true`, show the candidates and stop until the user picks.
3. **Mail and calendar.**
   - Search the last 90 days for the account name, its email domain and the key contacts' addresses.
   - Look for dissatisfaction, escalations, pricing or budget talk, competitor names, promises made, and procurement contacts.
   - List upcoming meetings with those contacts.
4. **Assess.**
   - For every material finding, cite the source (record, email or meeting) and its date.
   - Label each finding as Verified fact, Inference or Unknown, and say how it affects the renewal.
   - Rate the risk Low, Medium or High, with a confidence level and the reason. Never invent a probability or health score.
5. **Money.**
   - Keep the metric the source uses: order value is not ARR, MRR, ACV or TCV.
   - Show any calculation you make and flag missing inputs.
   - Never invent pricing, discount authority, contractual rights or approval thresholds.
6. **Deliver**, as a Docs artifact unless the user asks otherwise:
   - A. Executive summary of at most 200 words.
   - B. Fact sheet table: Field | Value | Source and date | Confidence or missing.
   - C. Risk and action register: Risk | Evidence | Impact | Mitigation | Owner | Due date.
   - D. Stakeholder plan: Stakeholder | Role in renewal | Priorities | Next engagement | Owner.
   - E. Execution plan, worked backwards from the end date and the notice deadline. If either date is unknown, flag it instead of inventing a timeline.
   - F. Customer meeting brief: objective, 5 discovery questions, proof points, likely objections, desired commitment.
   - G. Draft customer email. Consultative, with no internal risk ratings or negotiation limits.
   - H. Proposed Salesforce updates: run `du_opportunity_update` and `du_activity` with `dryRun=true` and show the previews.
   - Keep expansion opportunities separate from the base renewal.
7. **Close** with the 5 most important information gaps or decisions blocking a reliable plan. Then ask whether to apply any of the step H previews. Only after a clear yes, call the same tools again with `dryRun=false`, one approved change at a time.
