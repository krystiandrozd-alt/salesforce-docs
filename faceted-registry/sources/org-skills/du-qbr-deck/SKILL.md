---
name: du-qbr-deck
description: Drafts a Quarterly Business Review slide deck for one customer from Salesforce data (du MCP actions). Use when the user asks for a QBR, business review, quarterly review deck, or customer review presentation.
---

# du QBR Deck

## Tools

- Salesforce connector: `du_find_records`, `du_account_360`, `du_OrderSummaryMcp`, `du_renewal_baseline` (only for the contract and stakeholder context).
- Mail and calendar connectors, when enabled: past commitments and the next meeting date.

## Steps

1. **Resolve the account.**
   - Call `du_find_records`. If several records match, ask the user to choose.
   - Period: use the user's period, or the last completed quarter by default. State which period you used.
2. **Pull data.**
   - Call `du_account_360` for the period; it also returns the previous period.
   - Use its `json` output for numbers and charts. Never type numbers in by hand.
   - If more context is needed, call `du_renewal_baseline` for contract dates and stakeholders.
3. **Check gaps.**
   - Usage, adoption, SLA and billing data are not in standard Salesforce.
   - Do not invent them. Mark them "to be provided" in the deck and list them for the user.
4. **Build the deck** with the Slides artifact type, or as a .pptx if the user asks for PowerPoint. About 10 slides:
   1. Title: customer, period, du account team.
   2. Executive summary: 3 headline outcomes taken from the data.
   3. Partnership at a glance: orders, value, change vs previous period (chart).
   4. Services delivered: top products and share of value (chart).
   5. Service experience: cases opened and closed, average resolution, escalations.
   6. Wins and progress: opportunities won in the period.
   7. Open initiatives: open pipeline relevant to the customer, without internal stages or probabilities.
   8. Customer priorities for next quarter: placeholders, plus the questions to ask.
   9. Proposed roadmap and next steps, with owners and dates.
   10. Appendix: data sources and definitions (order value is not ARR).
5. **Audience rules.**
   - The deck is customer-facing.
   - Never show internal forecast categories, risk ratings, probabilities, discount ideas or quota.
6. **Finish.** Give one line on what the deck shows, the list of data gaps, and an offer to add speaker notes.
