---
name: du-meeting-follow-up
description: Turns a meeting transcript or notes into a customer follow-up email, internal summary and proposed Salesforce updates (call log, tasks, opportunity changes) via du MCP actions. Use when the user pastes or uploads meeting notes or a transcript and wants a recap, follow-up or CRM update.
---

# du Meeting Follow-up

Nothing is saved to Salesforce or sent until the user approves each item.

## Tools

- Salesforce connector: `du_find_records`, `du_renewal_baseline` or `du_account_360` for context, `du_activity`, `du_opportunity_update`.
- Mail connector, only to create a draft and only after approval. Never send.

## Steps

1. **Read the input**: pasted text, an uploaded file, or a transcript.
   - Pull out attendees, date, decisions, customer needs and pains, objections, commitments made by each side, risks, competitors and budget or timeline signals.
   - Quote only short phrases. Mark anything uncertain.
2. **Resolve records.**
   - Use `du_find_records` for the account, opportunity and contacts named in the notes.
   - If several records match, ask the user to choose.
   - Optionally call `du_renewal_baseline` to compare with the current stage, next step and close date.
3. **Draft outputs.**
   - **Customer email:** short; thank them, recap agreed points, list next steps with owners and dates, attach nothing unsupported. No internal opinions.
   - **Internal summary:** 5–8 bullets with decisions, risks and asks of the team.
   - **Action list:** Action | Owner | Due date | Source line in the notes.
4. **Propose Salesforce updates as previews:**
   - `du_activity` with `mode="log"` for the meeting (`isCall=true` if it was a call), the summary as the description, linked to the opportunity or account and the main contact.
   - `du_activity` (task mode) for each du-side follow-up action.
   - `du_opportunity_update` only for changes the notes support (next step, close date, stage, amount, description note).
   - Always use `dryRun=true`. Show each preview with Current → Proposed and the line in the notes that justifies it.
5. **Apply** only the items the user approves. Call the same tools again with `dryRun=false` and report what was saved, with links. If a save fails, show the error and leave the record unchanged.
