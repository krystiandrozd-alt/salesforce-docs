---
name: "du-weekly-team-review"
description: "Builds the du SMB weekly team review slide deck from live Salesforce order data in one go. Use when asked for the weekly team review, Monday sales review, team weekly or 'weekly review deck'."
---

# du Weekly Team Review

One command, one finished deck. Run every step without stopping to ask, unless the Salesforce connector is down.

## Tools

- Salesforce connector: `du_OrderSummaryMcp` (order number, account, status, effective date, amount AED).
- If they exist on the connector, also use: `du_PendingApprovalsMcp` (approvals slide), a tool or field returning order Owner (per-seller slide), SObject Reads on Opportunity (won / slipped / new deals slide).
- Output: the Slides artifact type (downloads as PPTX or PDF).

## 1. Define the weeks

- Review week = the last complete Monday–Sunday week before today. Name it by ISO week number ("Week 41").
- Prior week = the Monday–Sunday week before that.
- This week to date = Monday of the current week until today.
- Bucket every order by its effective date. State the dates on the cover.

## 2. Pull every order

`du_OrderSummaryMcp` shows only the latest 10 orders per call.

1. Call it with `status` Draft, Activated and Completed to get the true total per status.
2. For any status whose total is above 10, call it again with that status plus `accountName` set to single letters (a, e, i, o, u, y, then the rest of the alphabet if needed) and merge by order number until the count matches the total.
3. Never estimate a number. Every figure on a slide comes from the merged order list.

## 3. Compute

- Review week: order count, value, mix by status; same for prior week.
- Book today: count and value per status, share of value still Activated.
- Top accounts in the review week by value (exclude test accounts), and their share of customer value.
- Needs attention (age = days since effective date):
  - Activated 7+ days: chase fulfilment; 14+ days: escalate.
  - Activated under 7 days: give the date they cross 7 days.
  - Drafts with AED 0: complete or delete.
- Data hygiene:
  - Test accounts: names containing test, dry run, probe, zz, rules test (case-insensitive). Report their value separately and exclude them from "real customer" figures.
  - Possible duplicates: same account, status, effective date and non-zero amount.
- This week to date: new orders, and whether any are from real customers.

## 4. Build the deck (9 slides)

Style: navy #14233A, warm light #F7F6F2, magenta accent #B0164F, teal #1F6F7A; Rubik headings, IBM Plex Sans text; footer "du SMB · Weekly team review · Week N · page".

1. Cover: Week N, review dates, generated date.
2. Last week in numbers: orders, value, real-customer value, each vs prior week; status mix line.
3. Order book today: bar per status, headline = share of value still in fulfilment.
4. Top accounts last week: table, headline = how many accounts brought what share.
5. Needs attention: three cards (overdue, watch, stalled), each with a one-line next step.
6. Data hygiene: table of test accounts and possible duplicates with next steps.
7. This week so far: accent statement slide (magenta background).
8. Not in this review yet: missing views (per seller, deals, approvals, signatures) and what turns each on. Drop a row once its tool exists, and add a real slide for it instead.
9. Actions for this week: table with Owner as [name] placeholders and due dates in the current week.

Headlines state the finding ("91% of value is still in fulfilment"), not the topic. Speaker notes explain definitions and caveats.

## 5. Hand over

One line on what the week showed, the list of caveats (bulk-loaded dates, test data, missing views), and that the deck is private until shared. Offer to schedule it for Monday mornings.