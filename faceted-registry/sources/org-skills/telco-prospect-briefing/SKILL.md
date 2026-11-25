---
name: telco-prospect-briefing
description: Per-prospect intelligence briefing for an Enxoo sales or BDR pursuit of a named telecom operator, wholesale carrier, data centre operator, internet exchange, digital infrastructure company, or FTTH operator. Output covers corporate disambiguation, KB-1 v1.13 segment classification, reference-status check, signal scoring, stakeholder map with Miller Heiman buying-role tags, recommended sales motions in north-star outcome-led format, agentic companion variants, outreach angle, and scope flags. Uses Salesforce account history when provided; falls back to public research when not. Trigger when an Enxoo user asks to research, profile, qualify, prep for, prospect, or brief any named telecom or digital-infrastructure company — even informally ("tell me about X", "what's the angle on Y", "who do we know at Z"). For segment-level play work (ICP, discovery questions, objection handling) without a named prospect, use `telco-sales-play-template` instead.
---

# Telco Prospect Briefing

Produces a prospect briefing for the Enxoo sales and BDR team. Output is structured markdown the user can paste into Slack, email, a deck, or meeting prep. HTML/dashboard format on explicit request only.

This skill is the per-prospect half of Enxoo's telecom sales motion. Pair with `telco-sales-play-template` for segment-level reusable play structure.

## Inputs

Required: **company name**. Strongly recommended: **company URL** and **Salesforce account history**. If the company name is ambiguous (e.g. "Telia" could be Telia Company, Arelion, or a subsidiary), ask once for the specific entity before proceeding.

## Workflow — seven stages, progressive disclosure enforced

The reference set exceeds 5,000 lines and would consume the context window if loaded eagerly. Each stage loads only what it needs.

### Stage 0 — Reference-status check + Salesforce account history

Per KB-1 v1.13 Rules R-23 (account-history canonical) and R-27 (reference-status check overrides cold-prospect signals).

**Step 0a — Reference-status lookup.** Before asking about SFDC history, check whether the prospect (or its parent / operating entity) appears in KB-1 v1.13 Section 13.5 Reference-Status Lookup. The table covers DT (T Wholesale), du ICT, DE-CIX, AMS-IX, Bayobab, Telia Carrier (now Arelion), Arelion, HGC Global Communications, Expereo, Tele2 Latvia, Upp, Nexera, plus delivery proof points like MASORANGE.

If the prospect matches:
- Set `reference_status = confirmed` with KB or anchor source
- Suppress cold-prospect signals at Stage 4 ("Salesforce footprint unclear", "platform fit must be qualified", "no Salesforce hiring visible", "BSS/OSS vendor invisible") — these flags are nonsense for a known reference and produce internal contradictions
- Reframe qualifying questions from classification to enrichment: deployment scope, live use cases, expansion or renewal opportunity, open issues
- Adjust motion recommendation logic toward expansion / renewal / cross-sell
- Emit a 🟢 line in the briefing header: *"Confirmed Enxoo reference per [KB-1 v1.13 Section X.X / credibility-anchors 5.1] — [segment] segment, [confidence]"*

If no match: set `reference_status = unknown` and proceed normally.

**Step 0b — SFDC history request.** Regardless of reference-status outcome, ask:

> *Is this an existing Salesforce account? If yes, paste:*
> - *Account status (active, dormant, cold)*
> - *Opportunity history — name, stage, close date, close reason, close notes*
> - *Active contacts — name, title, last touch*
> - *Any warm path — internal advocate, event invitation, trade-show meeting*
>
> *For known references, public-only mode is insufficient — please prioritise pasting SFDC history. If you can't, I'll produce a delta enrichment from public sources only and flag the SFDC gap explicitly.*

Set `mode = SFDC-enriched` if data provided, otherwise `mode = public-only`. Both `mode` and `reference_status` appear in the briefing header.

**References to load at this stage:** KB-1 v1.13 Section 13.5 (lookup table only — small subset).

### Stage 1 — Corporate-structure disambiguation

Identify operating entity vs holding company vs brand. Identify parent, subsidiaries, rebrands, ticker changes, ownership transitions in last 5 years. Output as a "Corporate context" block at the briefing top.

Re-run Stage 0a with parent and any sister entities discovered. Group rebrands (e.g. Batelco → Beyon 2022) frequently mask reference-status matches that exist at parent or sister-entity level.

**References to load:** none additional at this stage; web research only.

### Stage 2 — Public research

Run web search across the prospect's website, recent press (last 12 months), trade press, financials, LinkedIn (named stakeholders), regulator filings, and standards-body activity (TM Forum, MEF, Mplify Alliance, GSMA).

**Inline citation discipline:** every factual claim in the briefing must carry an inline citation back to the source. Numeric claims without sources are suppressed — mark `[NEEDS CONFIRM]` rather than estimate. Marketing language is never paraphrased into claims; quote and source it instead.

**References to load:** none — external research only.

### Stage 3 — Segment classification

Apply KB-1 v1.13 qualification matrix Q1–Q11 to the gathered evidence. The matrix output is the primary segment with confidence; secondary overlays where commercial reality straddles segments.

Apply Section 11 External Signal Set as confidence-adjuster, not as a substitute for Q1–Q11.

Apply anti-pattern checks before finalising: AP-S1/R-05 (Government is overlay tag, not segment), AP-S2 (portal signal not driving classification), AP-S3/AP-S4 (size not a classification driver), AP-S6 (ICT classification only when vCIO / managed-outcome model is present), AP-S21 (NaaS marketing language verified against commercial reality).

Output: primary segment ID + confidence (High / Medium-High / Medium / Low); secondary overlays where applicable; compliance overlay tags; anti-pattern audit ☑.

**References to load:** KB-1 v1.13 segment rows for candidate segments only + Q1–Q11 matrix (lines 345–355) + Section 11 signal set + anti-pattern table.

### Stage 4 — Signal scoring

For each candidate segment confirmed at Stage 3, score the External Signal Set (KB-1 Section 11) against gathered evidence. Each matched signal adjusts confidence; absent signals flag cold-prospect risk areas.

Apply NaaS maturity profile per KB-1 Section 11.3 (six-characteristic check). Apply governance & distress signal check per Section 11.5 (restructuring, ownership type, procurement-scale flag).

If `reference_status = confirmed` from Stage 0, suppress generic cold-prospect platform-fit signals — they're nonsense for known references.

**References to load:** KB-1 v1.13 Section 11 (signal sets, NaaS maturity, governance signals).

### Stage 5 — Stakeholder map

Load segment-specific persona table from `stakeholders-and-triggers.md`. Apply Miller Heiman buying-role tags (DM, BH, CH, INF, GK, USR) per the file's six-role extension. Identify Mobiliser per Challenger framework — typically Transformation, Digital, or specific commercial-leadership roles depending on segment; named per-segment in the file.

Apply 3-tier naming priority: (1) named and verified from research; (2) role known, person unknown — use title and search string template; (3) role inferred but unverified — flag as such.

For warm paths flagged in Stage 0 SFDC data, prioritise their personas at the top of the stakeholder map.

Procurement-scale flag (⚠) — surface early in qualification, not at RFP stage.

**References to load:** `stakeholders-and-triggers.md` segment-specific section only.

### Stage 6 — Motion matching

Match confirmed segment to motions in `sales-motions.md` v0.2. Lead with motion outcome (North Star), not accelerator IDs (per AP-S25). Accelerators support, never lead.

**Selection rules:**
- Primary motion = best-fit motion for primary segment
- Secondary motion = considered when secondary segment overlay is material (e.g. SEG-1b + SEG-5 hybrid → W-1 + I-2 dual-motion architecture)
- Agentic companion = R-26 + AP-S26: Agentforce never standalone, always companion to core-cloud motion

Per AP-S25, External block of motion narrative leads with operator outcome. Internal block carries accelerator IDs, confidence, boundaries, references.

Per R-22, Network Layer (SDN, optical activation, OTN device-level orchestration, GIS) is never Enxoo scope — exclude explicitly in motion boundaries.

**Confidence rating logic:** High = multiple delivered references + productised accelerator; Medium-High = one strong reference + productised pattern; Medium = pattern documented, reference adjacent; Low = pattern proposed, no direct reference.

**This is the largest context-load stage.** If approaching context limits, prioritise the matched motion and skim others — see references list for which files to pull.

**Skip, and explicitly:** name the motions / variants that do NOT apply to this prospect (with reason). Stops scope creep into Network Layer, standalone Agentforce, wrong-segment retail Marketing Cloud, etc.

**References to load:** `sales-motions.md` matched-motion section + `accelerator-catalogue.md` matched ACCs + `agentforce-catalogue.md` matched companions + `enxoo-customer-facing-profile.md` Section 4–7 (claims, references, boundaries).

### Stage 7 — Compose the briefing

Read `references/briefing-output-template.md` and follow it. The template is the canonical output schema with section-by-section guidance, External/Internal block separation, and customer-facing cleanliness rules.

Apply all anti-pattern audits before output (R-22, R-25, R-26, R-27, AP-S25, AP-S26, plus permanent named-entity exclusions per skill memory).

**References to load:** `references/briefing-output-template.md`.

## Output discipline

- Inline citations on every factual claim. Unsourced numbers → `[NEEDS CONFIRM]`, never estimated.
- External / Internal block separation in the motion section never relaxes — guidance language leaks if Internal is back-filled after External.
- Customer-facing cleanliness — never paste verbatim into customer materials; the briefing is internal enablement, not a leave-behind.
- No invented stakeholder names. 3-tier naming priority enforced.
- No fabricated reference customers.
- Permanent named-entity exclusions per skill memory honoured throughout.

## Output format

Default: structured markdown, paste-ready for Slack / email / deck / meeting prep.

HTML / dashboard format: only on explicit user request. When requested, write to `/mnt/user-data/outputs/[company-slug]-briefing.html` and surface via `present_files`. The HTML render is the same content with inline navigation; it is not a separate deliverable.

## Reference loading by stage

| Stage | Load |
|---|---|
| 0 | KB-1 Section 13.5 lookup table only |
| 1 | none (web only) |
| 2 | none (web only) |
| 3 | KB-1 candidate segment rows + Q1–Q11 + Section 11 signals + anti-pattern table |
| 4 | KB-1 Section 11 (signals, NaaS maturity, governance) |
| 5 | `stakeholders-and-triggers.md` segment section |
| 6 | `sales-motions.md` matched motion + `accelerator-catalogue.md` matched ACCs + `agentforce-catalogue.md` matched companions + `enxoo-customer-facing-profile.md` Sections 4–7 |
| 7 | `references/briefing-output-template.md` |

## References

- `references/briefing-output-template.md` — canonical output schema with section-by-section guidance and External/Internal block separation rules
- `references/KB1_Customer_Segmentation_Reference_v1_13.md` — segment definitions, Q1–Q11 qualification matrix, signal sets, anti-patterns, reference-status lookup
- `references/sales-motions.md` v0.2 — motion catalogue (W-1 to W-4, E-1 to E-4, I-1 to I-4, C-1 to C-3, X-1, X-2)
- `references/accelerator-catalogue.md` — productised accelerator catalogue (ACC-001 onwards)
- `references/agentforce-catalogue.md` — Agentforce companion catalogue with motion-pairing
- `references/stakeholders-and-triggers.md` — per-segment persona tables with MH buying-role tags
- `references/enxoo-customer-facing-profile.md` — claim-evidence pairs, boundaries, customer-facing language
- `references/enxoo-credibility-anchors.md` — cleared reference customers per segment
- `references/sales-motions-extensions.md` — Customer 360 / Data Cloud motion (X-1) and event-revenue motion (X-2)
- `references/salesforce-platform-trust.md` — Hyperforce regional residency, Shield, Privacy Center facts for compliance posture statements

## What this skill does not do

- Does not generate segment-level sales play (ICP, discovery questions, objection handling, exit criteria) — use `telco-sales-play-template`.
- Does not produce numeric ROI, pricing, or specific customer stories without source.
- Does not invent reference customers.
- Does not classify outside KB-1's 8-segment scope.
- Does not name entities under permanent exclusion per skill memory.
- Does not overclaim Network Layer scope (R-22).
- Does not position Agentforce standalone (AP-S26).
