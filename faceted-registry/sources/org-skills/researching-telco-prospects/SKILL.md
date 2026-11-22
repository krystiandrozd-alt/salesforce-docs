---
name: researching-telco-prospects
version: 0.3.2
description: Researches a telecom operator, wholesale carrier, data centre operator, internet exchange, digital infrastructure company, or FTTH operator as an Enxoo sales prospect. Produces a structured briefing with group structure mapping, full segment landscape, targeted deep dive on Enxoo target segments, stakeholder map, recommended sales motions, stakeholder-adapted outreach angles, and scope flags. Applies dual-layer segmentation (full landscape + target deep dive) using KB-1 v1.9 taxonomy. Outputs markdown by default; optional Enxoo-branded HTML briefing on request. Detects warm paths to Enxoo via LinkedIn connection overlap when profile data is available. Adapts outreach language per stakeholder archetype (CFO / Sales Leadership / CTO-CIO / Ops-Delivery). Uses Salesforce account history when provided; otherwise public research only. Use this skill when an Enxoo user asks to research, profile, qualify, prep for, prospect, or brief any named telecom or digital-infrastructure company.
---

# Researching Telco Prospects — v0.3.2

This skill produces a structured prospect briefing for the Enxoo sales and BDR team. Output is structured markdown the user can paste into Slack, email, a deck, or a meeting prep doc. HTML output mode is available on request, producing an Enxoo-branded static report.

v0.3.1 adds the dual-register Communication Style discipline: BDR-internal tone for briefing body, stakeholder-adapted tone for outreach (CFO / Sales Leadership / CTO-CIO / Operations archetypes). v0.3 foundations remain: warm-path detection via LinkedIn overlap, AP-S code inline citations in classification rationale, and optional Enxoo-branded HTML output alongside the default markdown.

## Inputs

Required: **company name**. Strongly recommended: **company URL**, and **Salesforce account history** if the prospect is already in Enxoo's CRM.

If the user provides only a company name and the name is ambiguous (e.g., "Vodafone" could mean Vodafone Group, Vodafone Business, individual OpCos, or Vantage Towers; "Beyond" could be the Polish data centre operator or another entity), the skill asks once for the specific entity before proceeding.

## Output modes

**Full briefing** (default) — all stages, ~100 lines markdown. For research, meeting prep, account planning.

**Mobile summary** — produced when user says "quick version," "short version," or uses `--mobile`. Contains banner (if distress), Layer 2 primary classification per entity, top 3 stakeholders, top 2 motions, 2-sentence outreach, critical flags only. Target: 25–30 lines.

**HTML briefing** — produced when user says "HTML version," "branded report," "for the deck," or uses `--html`. Enxoo-branded static report (navy #1F2043, light blue #D0EDFE, Lato / Plus Jakarta Sans) containing the full briefing content. Self-contained single-file HTML, suitable for sharing via email attachment, hosting internally, or PDF conversion. See Stage 8 for rendering rules.

HTML and markdown are complementary, not exclusive — user can request both in the same run ("full briefing in markdown and HTML").

## Communication style

The skill applies two distinct communication registers: **BDR-internal tone** for the briefing body, and **stakeholder-adapted tone** for the outreach angle block. This separation is mandatory — applying marketing tone to the briefing body weakens the analysis; applying BDR-analytical tone to outreach weakens the pitch.

### BDR-internal tone (default for briefing body, Stages 0–7)

All briefing content is written in BDR-oriented communication style:

- **Direct** — facts first, prose second; no lead-ins or softening
- **Structured** — tables, bullets, explicit markers; analytical not narrative
- **Business-focused** — commercial facts, segment discipline, gap honesty
- **Avoid** — generic marketing language ("transform your business"), unnecessary verbosity, vague positioning statements, unqualified superlatives

This applies to: group structure implications, segment landscape notes, Layer 2 classification rationale, signal scoring, stakeholder map annotations, motion fit rationale, flags.

### Stakeholder-adapted tone (mandatory for outreach angle, Stage 6)

When the briefing produces the outreach angle, the skill **MUST** identify the priority stakeholder archetype and adapt language and argumentation accordingly. Never produce a single generic outreach message when multiple senior stakeholders are named in Stage 5.

**Step 1 — Identify stakeholder archetype** from Stage 5 priority list:

| Archetype | Typical roles |
|---|---|
| **CFO** | CFO, Finance Director, VP Finance, Head of Revenue Management, investment director (infra-fund-owned) |
| **Sales Leadership** | Chief Enterprise Officer, Chief B2B Officer, Chief Commercial Officer, Chief Consumer Officer, Head of Wholesale, Head of Sales, Head of SMB, VP Sales, CCO |
| **CTO / CIO** | CTO, CIO, CDO, Chief Network Officer, Chief Interconnect Officer, Head of IT Platforms, Enterprise Architect, Head of BSS/OSS |
| **Operations / Delivery** | COO, Head of Delivery, Head of Service, Head of Operations, Facility Manager, PMO Director, Head of Project Delivery, Head of Field Service, Head of Contact Center, Asset Manager |

Some roles bridge two archetypes (e.g., a Head of Digital Transformation spans CTO and Sales Leadership depending on the prospect). When ambiguous, pick the archetype that matches the *motion being proposed*, not the role title alone — a CTO receiving a Motion E-1 Tender-to-Win pitch hears Sales Leadership arguments, not architecture arguments.

**Step 2 — Adapt language per archetype:**

**CFO archetype:**
- Emphasize: cost reduction, ROI, margin improvement, DSO / working capital, risk mitigation, consolidation TCO
- Quantify outcomes where ✅ RFP reference evidence supports it (cycle time reduction, margin lock at quote, DSO improvement)
- Avoid deep technical detail unless directly tied to financial impact
- Avoid architecture vocabulary (TMF, Mplify, MuleSoft) unless the CFO is also the BSS transformation sponsor
- Decision frame: "board-approvable commercial case"

**Sales Leadership archetype:**
- Emphasize: pipeline acceleration, conversion improvement, quoting speed, revenue growth, win-rate improvement, sales productivity per rep
- Use performance-oriented language ("from 4 months to 2 months," "+30% sales efficiency") anchored to ✅ RFP references
- Reference Motion E-1, E-3 for tender and ABM; Motion W-1, W-2 for carrier sales; Motion C-1, C-3 for consumer / SMB acquisition
- Avoid CLM / contract lifecycle depth unless directly tied to deal closure speed
- Decision frame: "quota coverage and pipeline discipline"

**CTO / CIO archetype:**
- Emphasize: architecture, scalability, integration, standards (TM Forum Open APIs, Mplify LSO Sonata/Cantata, ODA), platform consolidation
- Include system-level reasoning: where Salesforce sits in the four-layer NaaS architecture, what MuleSoft integrates, what stays specialist (OSS, consumer billing, DCIM, TAP/NRTRDE)
- Reference the NaaS whitepaper explicitly and the Experience + Business + parts-of-Operational boundary (R-22)
- Cite architecture caveat proactively if pursuing on-Core / RCA (DE-CIX is the on-Core reference)
- Decision frame: "reference architecture fit and multi-year platform roadmap"

**Operations / Delivery archetype:**
- Emphasize: process efficiency, automation, error reduction, operational visibility, handoff discipline, SLA adherence, case deflection
- Reference KB-1 Section 8 service patterns (zero-touch / low-touch / medium-touch / high-touch) to match the prospect's operational maturity
- Motion I-1 (Tenant Experience Unified), Motion W-1 (Zero-Touch Lead-to-Order), Motion C-1 (Digital Commerce-First FTTH) map well to ops narratives
- Avoid board-level ROI framing unless ops leader is also P&L holder
- Decision frame: "day-to-day operational improvement and team scalability"

**Step 3 — Emit stakeholder-adapted outreach variants.** When Stage 5 identifies two or more priority stakeholders from different archetypes, Stage 6 produces one outreach variant per archetype. The variants share the same underlying motion recommendations but frame them in the stakeholder's language. See Stage 6 outreach composition rules.

**Mandatory rules:**

- ALWAYS adapt tone when the briefing will be used for external communication
- NEVER use one generic message for all stakeholder archetypes when multiple senior contacts are named
- ALWAYS align arguments with the specific stakeholder's decision frame
- Internal briefing body (Stages 0–7 analytical content) stays BDR-tone regardless of stakeholder mix — the adaptation applies only to the outreach angle and any follow-up message drafts

### Result

| Output layer | Tone |
|---|---|
| Markdown briefing body (analytical content) | BDR-internal — structured, direct, analytical |
| Markdown outreach angle block | Stakeholder-adapted variants, one per archetype |
| HTML briefing body | BDR-internal — same substance as markdown, styled |
| HTML outreach angle block | Stakeholder-adapted variants, one per archetype, styled as quote cards |
| Mobile summary outreach | Single variant, keyed to highest-priority stakeholder's archetype |

Internal consistency (BDR discipline) plus external adaptivity (stakeholder specificity) — not a trade-off, a two-register system.

## Workflow — twelve stages (11 core + 1 conditional HTML)

### Stage 0 — Salesforce account history check (non-blocking)

Ask the user once:

> *If this is an existing Salesforce account, paste what you have now — account status, opportunity history, active contacts, any warm path. I'll start public research in parallel. If there's no SFDC history, I'll proceed public-only.*

**Do not wait.** Proceed to Stage 1 immediately. If the user provides SFDC data in their next message (or any subsequent message before briefing emission), integrate it and set `mode = SFDC-enriched`. Otherwise `mode = public-only`.

Never ask the SFDC question twice. If the user's next message addresses something else, default to `public-only` and proceed.

---

### Stage 1 — Group structure & ownership mapping

Identify the corporate structure before classification. Many telecom groups have parent-plus-operating-entity structures that change classification and outreach targeting.

For any prospect, identify:
- Operating entity vs holding company vs brand
- Parent company if any
- Subsidiaries and sister companies relevant to scope
- Rebrands, ticker changes, or ownership transitions in the last 5 years
- Ownership type per KB-1 Section 11.5.2 taxonomy (private, public-listed, state-owned, state-majority, infra-fund, PE, family-office, in-transition)

**Output: FigJam diagram (mandatory, only format)**

Call `Figma:generate_diagram` with Mermaid `flowchart TD` syntax. The diagram is the sole artifact for Stage 1 — do not emit a text tree, JSON block, or implications paragraph. All downstream stages must read structure facts from the Mermaid source you author here.

**Required diagram content:**

1. **Root node** — group name + ownership type tag (e.g., `"Deutsche Telekom AG<br/>public-listed"`)
2. **Parent node** — only if the group is itself a subsidiary; otherwise omit
3. **Entity nodes** — one per operating entity, ICT division, wholesale unit, DC/DigiInfra/IX/FTTH subsidiary in scope. Each entity node must contain, on separate lines inside the node label:
   - Entity name
   - Entity type (Telco | ICT | Wholesale | DataCenter | DigiInfra | IX | FTTH)
   - KB-1 segment tags (e.g., `SEG-2, SEG-7a`)
   - In-scope flag (`✅ target` | `⚠ peripheral` | `❌ out-of-focus`)
4. **Operating entity marker** — the operating entity node uses a distinct shape (double-bordered rectangle `[[...]]`) so Stage 3b classification target is unambiguous
5. **Recent transitions** — rebrands, ticker changes, ownership transitions in the last 5 years rendered as edge labels or a footnote node connected by dashed line (`-.->`)
6. **Color styling** — apply `style` directives sparingly: green fill for ✅ target entities, amber for ⚠ peripheral, grey for ❌ out-of-focus

**Diagram naming:** Pass `name` parameter as `"<Group Name> — Group Structure"`.

**Rule:** Layer 2 classification (Stage 3b) operates on the operating entity (the `[[double-bordered]]` node), not the holding or brand, unless the engagement track is explicitly group-level.

**Template:**

```
flowchart TD
    Parent["Parent Group Name<br/>ownership-type"]
    Parent --> OpCo
    OpCo[["Entity A<br/>Telco<br/>SEG-2, SEG-7a<br/>✅ target"]]
    Parent --> ICT["Entity B<br/>ICT<br/>SEG-3<br/>⚠ peripheral"]
    Parent --> WS["Entity C<br/>Wholesale<br/>SEG-1<br/>✅ target"]
    Parent -.->|"rebrand 2023"| Note["Recent: ticker change 2024"]
    style OpCo fill:#d4edda
    style ICT fill:#fff3cd
    style WS fill:#d4edda
```

---

### Stage 2a — Public research

Use `web_search` and `web_fetch` on the prospect's domain and supporting sources.

If `mode = SFDC-enriched`: research is delta-focused — what has changed since the last Close Date in the provided opportunity history. Usually 3–5 searches are sufficient.

If `mode = public-only`: research is comprehensive — 6–10 searches covering website, news, LinkedIn, standards bodies, trade press, and annual report.

Research priority:

1. Prospect website — homepage, about, products, wholesale/carriers page, investors, leadership, press
2. News in last 12 months — executive changes, transformation programmes, M&A, product launches, regulatory events
3. LinkedIn — company page; known executive profiles (CEO, CTO, CIO, CDO, CCO, and segment-relevant heads)
4. Standards bodies — Mplify Alliance (formerly MEF) member directory, TM Forum, GSMA / i3forum / Euro-IX as applicable
5. Trade press — Light Reading, TelecomTV, Capacity, Total Telecom, Data Centre Dynamics, Developing Telecoms
6. Annual report / investor day if listed, or parent's if applicable

Cite every factual claim inline using `(Source: [publisher], [date], [URL])`. No end-of-briefing Sources index.

---

### Stage 2b — Segment metrics enrichment

For each KB-1 segment the operator participates in, collect (best effort):

| Metric | Source preference | When unavailable |
|---|---|---|
| Revenue (absolute + %) | Financial report, investor day | Mark `Unknown (not disclosed at segment level)` |
| FTE estimate | Annual report, LinkedIn company size | Mark `Estimated from LinkedIn (n employees total)` |
| Customer base | Investor materials, press | Mark `Unknown` |
| ARPU/ACV (B2B, ICT) | Investor day, segment disclosure | Mark `Unknown — rarely disclosed` |
| Growth trend (↑/↓/→) | Year-over-year revenue comparison | Mark `Unknown` |
| Strategic importance | Strategy day, investor presentations | Mark `Inferred from [specific source]` |

**Discipline rule:** These metrics feed Stage 3a strategic prioritization only. They do NOT feed Stage 3b Q1–Q11 classification (per KB-1 R-04, AP-S3, AP-S4).

---

### Stage 2c — Source discipline & confidence scoring

Apply source hierarchy:

| Rank | Source | Confidence | Example use |
|---|---|---|---|
| 1 | Audited financial report, regulatory filing | High | Segment revenue, ownership, group structure |
| 2 | Investor day, strategy day, earnings call | High | Strategic direction, growth targets |
| 3 | Official company disclosures (press room) | High | Transformation programmes, exec appointments |
| 4 | Industry press (Capacity, Light Reading, TelecomTV) | Medium | Deals, launches, market positioning |
| 5 | LinkedIn, job postings | Medium | Role existence, hiring signals |
| 6 | CRM / SFDC data | High for account state only | Past opportunities, contacts, warm paths |
| 7 | AI inference without corroboration | Low | Flag as `inferred — no primary source` |

**Dual canonicality rule:**

- SFDC is canonical for **account state**: past opportunities, named contacts, close reasons, warm paths (KB-1 R-23)
- SFDC is NOT canonical for **commercial facts**: segmentation, segment revenue, group structure, FTE (Requirement 5)

**Confidence marker required on every numeric, structural, or classification claim** in the final briefing. Format: `(High)`, `(Medium)`, `(Low)`, `(Estimated)`, `(Unknown)`.

---

### Stage 3a — Full segment landscape (Layer 1)

Read `references/KB1_Customer_Segmentation_Reference_v1_9.md` if not already loaded.

Enumerate every KB-1 segment the operator participates in. Use KB-1 v1.9 taxonomy only — no invented categories. IoT, Cloud, AI are product families, not segments (AP-S3, AP-S4).

Output the Layer 1 segment landscape table:

| Segment (KB-1) | In Scope | Revenue % (confidence) | FTE (confidence) | Growth | Strategic Importance | Notes |
|---|---|---|---|---|---|---|
| SEG-1a Wholesale Voice | ❌ / ⚠ / ✅ | e.g. 8% (High) | ~200 (Estimated) | ↓ | Medium | PSTN switch-off underway |
| SEG-1b Wholesale Data | ✅ | 22% (High) | ~450 (Medium) | ↑ | High | Mplify LSO certified 2024 |
| SEG-1c Wholesale Mobility | ❌ | — | — | — | — | Not an MNO |
| SEG-2 Enterprise B2B | ✅ | 31% (High) | ~1,200 (High) | ↑ | High | Key growth vector |
| SEG-3 ICT / Digital Services | ⚠ | 12% (Medium) | ~300 (Estimated) | ↑ | Medium | Nascent, no vCIO role visible |
| SEG-4 Data Center / Ecosystem | ❌ | Not applicable | — | — | — | Does not operate DCs |
| SEG-5 Digital Infrastructure | ❌ | Not applicable | — | — | — | No IRU/dark fiber motion |
| SEG-6 Internet Exchange | ❌ | Not applicable | — | — | — | — |
| SEG-7a FTTH B2C | ⚠ / ✅ | 18% (High) | ~800 (Medium) | → | High | **FTTH exception — see rule below** |
| SEG-7b FTTH B2B | ✅ | 5% (Medium) | ~100 (Estimated) | ↑ | Medium | SMB push visible |

**FTTH exception rule (applies to Layer 1 scoring only):**

The general rule is that B2C mass-market segments are ❌ Out of Focus for Enxoo (consumer billing at scale is out of delivery scope per KB-1 SEG-7a "Gap"). FTTH B2C is an exception.

- SEG-7a FTTH B2C is ✅ Target when any of the following is visible:
  - Digital Commerce motion (Motion C-1)
  - Churn/retention programme with AI ambition (Motion C-2)
  - Field Service modernization
  - Data Cloud + Agentforce footprint
- SEG-7a FTTH B2C is ⚠ Peripheral when FTTH operations exist but Salesforce-relevant motion evidence is absent
- SEG-7a FTTH B2C is ❌ Out of Focus only when evidence specifically shows a billing-engine-centric roadmap with no commerce / churn / service Salesforce scope

**Other B2C segments** (prepaid mobile, retail mobile, pay-TV standalone) remain ❌ Out of Focus by default. They are not represented in KB-1 v1.9 as segments. List them as "B2C Mobile (out of KB-1 scope; ❌ Out of Focus)" if material to operator revenue.

**Government/Regulated rule preserved** (KB-1 R-05): Not a segment. Apply as compliance overlay on the base commercial segment.

---

### Stage 3a.1 — Segments intentionally not analyzed

Output a mandatory block listing every ❌ Out of Focus segment with one-sentence justification. Cite KB-1 rule where applicable.

Example:

```
Segments intentionally not analyzed:

• SEG-1c Wholesale Mobility — ❌ Out of Focus. Operator is fixed-line only; 
  no MNO licence. Not applicable.

• SEG-4 Data Center / Ecosystem — ❌ Out of Focus. Operator leases DC capacity 
  rather than operating facilities. Per KB-1 Section 2, SEG-4 applies only to 
  facility owners.

• B2C Mobile (prepaid, retail) — ❌ Out of Focus. Not in KB-1 v1.9 scope. 
  Enxoo focus on B2B/ICT/FTTH-Commerce motions. Billing engine dependency 
  out of Enxoo delivery scope.

• SEG-5 Digital Infrastructure — ❌ Out of Focus. No IRU/dark-fibre motion 
  visible; no NetCo carve-out signals.
```

**Discipline rule:** No ❌ segment is silently dropped. Every exclusion is explicit, justified, and sourced.

---

### Stage 3b — Primary segment confirmation (Layer 2)

For each ✅ Target segment (and relevant ⚠ Peripheral where strategic), apply KB-1 Q1–Q11. Produce primary segment classification per operating entity with High / Medium / Low confidence. Preserve KB-1 R-03: one primary per account/entity, secondary overlaps permitted only after primary confirmed.

**Where multiple entities exist** (per Stage 1): Run Q1–Q11 per operating entity. The briefing may end with multiple primary classifications, one per entity. Example: Group X has one primary SEG-2 (Enterprise arm) and one primary SEG-1b (Wholesale arm). This is valid per KB-1 Section 3 overlap patterns.

Cross-check against KB-1 Section 11 External Signal Set (R-21). If signals and questionnaire disagree, flag the conflict, prefer the questionnaire, note both.

Apply KB-1 R-20 sales-team diagnostic when role evidence is available — for example, a vCIO strongly indicates SEG-3 even if Q1–Q11 points to SEG-2.

**Anti-patterns to check before emitting Layer 2 classification:**

- AP-S1 (Government as segment) — apply overlay instead
- AP-S3 (industry classification)
- AP-S4 (size-based classification)
- AP-S6 (ICT vs Enterprise boundary — check for vCIO per R-20)
- AP-S7 (KB version mismatch)
- AP-S14 (FTTH B2B vs Enterprise DIA — check access technology per R-16)
- AP-S15 (IX as segment vs DC product family — check independence per R-17)
- AP-S20 (sales team structure contradicts segment assignment)
- AP-S21 (marketing-language-only classification)
- AP-S23 (SFDC history ignored)

If any is borderline, surface the reasoning explicitly in the briefing rather than silently deciding.

**AP-S inline citation discipline (v0.3):** Every classification rationale in the Layer 2 deep dive output must cite by AP-S code the anti-pattern that was *considered and ruled out*, not just the anti-patterns violated. This makes the reasoning auditable. Format: `(cleared AP-S3 — classification based on Q1+Q3 commercial signals, not industry vertical)` or `(AP-S6 borderline — vCIO role visible, trapped at SEG-2/SEG-3 boundary; resolved SEG-3 per R-20 sales-team diagnostic)`.

**AP-S code inventory** (24 codes in KB-1 v1.9 Section 7) — cite by code when rationale touches the rule:

| Code | Rule reminder |
|---|---|
| AP-S1 | Government is overlay, not segment (R-05) |
| AP-S2 | Portal is channel, not segment |
| AP-S3 | Don't classify by industry vertical alone |
| AP-S4 | Don't classify by company size alone |
| AP-S5 | One primary segment per Account; separate Accounts for separate businesses |
| AP-S6 | Managed router ≠ ICT; vCIO + multi-domain + outcome = ICT (R-20) |
| AP-S7 | Check KB version before applying definitions |
| AP-S8 | Dark fiber + IRU = DigiInfra; lit fiber = Wholesale or Enterprise |
| AP-S9 | SD-WAN not in Wholesale catalog |
| AP-S10 | PS / bespoke not in PCM catalog (R-14) |
| AP-S11 | UCaaS / security not in Wholesale catalog |
| AP-S12 | NNI not in Enterprise catalog; cross-connect is DC product |
| AP-S13 | Secondary products must attach to Core parent (R-15) |
| AP-S14 | Access tech determines SEG-7b vs SEG-2 (R-16) |
| AP-S15 | IX as segment only when independent BU (R-17) |
| AP-S16 | IPTV / home voice only in FTTH B2C |
| AP-S17 | Consumer billing model not for SEG-7b (B2B) |
| AP-S18 | Service pattern must match segment (R-18) |
| AP-S19 | Segment-specific journey in wrong segment (R-19) |
| AP-S20 | Sales team structure as classification cross-check (R-20) |
| AP-S21 | Marketing language alone ≠ classification (R-21) |
| AP-S22 | NaaS scope excludes Network Layer (R-22) |
| AP-S23 | SFDC history is canonical, not discarded (R-23) |
| AP-S24 | Distress prospects get Phase 1, not transformation (R-24) |

**Example classification rationale with AP-S citation:**

```
Primary segment: SEG-3 ICT / Digital Services (Medium confidence)

Rationale:
- Q1 answered "Yes, to enterprises as part of a managed service" → ICT candidate
- Q3 dominant revenue "MRC + milestone + vendor pass-through" → confirms ICT
- Q7 term set "vCIO, managed outcome, milestone, multi-vendor" → confirms ICT
- (cleared AP-S3 — not classifying from industry vertical; commercial Q1+Q3 
  signals lead)
- (cleared AP-S4 — company size not used as input; operator is mid-market 
  but this does not determine segment)
- (resolved AP-S6 boundary — managed-router element visible, but multi-domain 
  scope + named vCIO in leadership team confirms ICT not Enterprise, per R-20)
- (cleared AP-S21 — not classifying from "digital transformation" marketing 
  language alone; Q1–Q7 commercial signals independently confirm)
```

This discipline makes classification decisions reviewable. When v0.3 output is audited by senior pre-sales or delivery leadership, the AP-S citations show which traps were considered, which were cleared, and which resolved against which KB-1 rule.

---

### Stage 4 — Signal scoring + distress handling

Apply KB-1 v1.9 Section 11 signals for each confirmed primary segment. Note matched, absent, and conflicting signals with source URLs.

Run Section 11.5 (Governance & Distress Signals):

- Check for restructuring, bailout, layoffs, regulatory intervention in last 24 months
- Confirm ownership type from Stage 1 matches Section 11.5.2 detection
- Apply procurement-scale flag recalibration per Section 11.5.3

Scan `references/stakeholders-and-triggers.md` Part B trigger catalog for matched triggers in the last 12 months. Record each with:
- Warmth (Low / Medium / High / Very High)
- Source URL and date
- Recommended motion ID from the trigger row

**When any Section 11.5 signal is active, briefing emits all four outputs per Section 11.5.4:**

1. **Distress/governance banner** in briefing header (one line)
2. **Motion-sizing note** — explicit statement of why transformation-scale is/isn't appropriate (R-24)
3. **Procurement-pattern expectation** — derived from ownership type (Section 11.5.2)
4. **Timing recommendation** — engage now / watch and wait / defer 90 days / defer indefinitely

For NaaS-relevant segments (SEG-1b, SEG-1c, SEG-2, SEG-3, SEG-4), produce a NaaS maturity profile against the six Enxoo NaaS whitepaper characteristics.

---

### Stage 5 — Stakeholder map

Read `references/stakeholders-and-triggers.md` Part A.

Main briefing: **3–5 priority stakeholders** for the primary segment(s).

Optional appendix: "Extended stakeholder map" with up to 8 roles if user requests, or if the engagement is a Layer-2-confirmed strategic account.

For each stakeholder:

- Role and title variants
- Named person — from SFDC contact list (if provided) first, then from public research
- LinkedIn URL if found, or a LinkedIn search string using the role-variant list and the prospect's name
- Buying-role tag (DM, BH, CH, INF, GK, USR)
- One-line relevance to Enxoo outreach

Distinguish clearly:

- **Named and verified** — person confirmed at the prospect, contact data available
- **Named from SFDC but unverified** — in SFDC but last touch is old; may have moved
- **Role known, person unknown** — provide LinkedIn search string

If a named warm path exists from Stage 0 (internal Enxoo advocate, event meeting offer), that contact is priority #1 regardless of seniority ranking (KB-1 R-23).

**Warm-path detection via LinkedIn overlap (v0.3).** When profile URLs are retrieved for priority stakeholders, run the following overlap test to flag passive warm paths:

1. For each priority stakeholder with a resolved LinkedIn profile URL, check visible "mutual connections" and "shared experiences" signals on the profile.
2. An overlap is flagged when any of the following is visibly detectable:
   - **Direct connection signal** — the stakeholder appears in a known Enxoo employee's 1st-degree connections list (requires Enxoo employee LinkedIn visibility, typically available only under authenticated access — mark as `inferred` when working from public profile alone)
   - **Shared employer history** — stakeholder previously worked at an Enxoo customer in Section 3.1 of the credibility anchors file (e.g., ex-DTGC, ex-Arelion, ex-du, ex-Tele2 Latvia, ex-Upp, ex-Nexera, ex-Expereo, ex-HGC, ex-DE-CIX) — indicates prior exposure to Enxoo-delivered platform
   - **Shared conference / event history** — stakeholder and known Enxoo presence at same event (Mplify GNE, Capacity, ITW, MWC, TM Forum, Salesforce Dreamforce, Salesforce World Tour) in last 24 months
   - **Shared standards body membership** — stakeholder active in Mplify Alliance, TM Forum, GSMA, or Euro-IX alongside Enxoo participation
   - **Academic overlap** — shared alma mater with named Enxoo leadership where relevant (low-weight signal; only cite when combined with at least one of the above)

3. Warm-path scoring:

| Warmth | Signal pattern |
|---|---|
| **🔗🔗🔗 Strong warm path** | Named Enxoo advocate (Stage 0 SFDC data) OR direct 1st-degree connection to Enxoo employee |
| **🔗🔗 Medium warm path** | Shared employer history at ✅ RFP reference customer OR co-presence at named industry event in last 12 months |
| **🔗 Weak warm path** | Shared standards body membership OR event co-presence >12 months OR academic overlap only |
| **no overlap** | No detectable signal; cold outreach |

4. Output: For each priority stakeholder, emit a warm-path annotation in the stakeholder row: `🔗🔗 Medium — ex-DTGC, 2018–2022`. Confidence marker applies: `(High)` when verified via multiple signals, `(Medium)` when one clear signal, `(Low/inferred)` when pattern-matching without direct confirmation.

5. **Discipline rules for warm-path detection:**
   - Never fabricate a warm path. If signals aren't visible, mark `no overlap`.
   - LinkedIn data retrieved without authenticated access is limited — mark `(inferred)` when working from public profile text alone.
   - Ex-customer history is a *passive* warm path, not a guarantee of advocacy. The former employee may have had a neutral or negative experience. Frame as "prior platform exposure" not "champion."
   - In the outreach angle, a warm path may be gently referenced ("as someone who worked with the platform at DTGC, you'll recognize...") but never claimed as endorsement unless Stage 0 SFDC data confirms an active advocate relationship.
   - Warm-path detection augments but does not replace the Stage 0 SFDC advocate priority rule.

**Language variants in v0.2:**

- Polish role variants for V4 NatCo prospects (e.g., "Dyrektor ds. Hurtu" for Head of Wholesale)
- Arabic role variants for GCC prospects (primary English with Arabic in parentheses)
- English-only for other markets
- Czech, Hungarian, German variants deferred to v0.3

Apply procurement-scale flag (⚠) per KB-1 v1.9 Section 11.5.3 recalibration, using ownership type from Stage 1.

---

### Stage 6 — Motion matching

Read `references/sales-motions.md` and `references/salesforce-clouds.md`.

Select motions based on:

- Primary segment(s) from Stage 3b
- Observed signals and trigger events from Stage 4
- Active distress / governance signals (motion size bias per R-24)
- Stakeholder seniority and buying-role availability from Stage 5
- SFDC history — prior pursuits indicate motion alignment already established

**Hard cap: 2 primary motions.** Any third candidate goes in "Skip, and explicitly."

**Motion ID citation required.** Use explicit IDs from `sales-motions.md`: W-1, W-2, W-3, W-4, E-1, E-2, E-3, E-4, I-1, I-2, I-3, C-1, C-2, C-3, X-1, X-2.

**Motion → Segment matrix guardrail:** Only propose motions marked ● Primary or ○ Secondary in `sales-motions.md` §6 for the confirmed segment(s). If no primary motion is available for a confirmed segment, document as a capability gap in the briefing rather than forcing an ill-fitting motion.

**Salesforce cloud sequencing enforcement:** Validate proposed platform footprint against `references/salesforce-clouds.md` §3 sequencing rules:

1. Data Cloud before Agentforce
2. CMP vs on-Core depends on customer state — ask before recommending migration
3. MuleSoft proportional to integration complexity, not headcount
4. Field Service is segment-specific, not universal
5. Marketing Cloud is SEG-7a core; secondary or NA elsewhere
6. Digital Commerce excludes complex/negotiated

Flag any recommendation that violates a sequencing rule.

**Agentforce-first prohibition:** If Agentforce is part of any recommended motion (W-3, C-2, E-3), mark it explicitly as Phase 2. Phase 1 must be Data Cloud or equivalent foundation. The outreach angle must not lead with Agentforce.

**Pragmatic Phase 1 definition** (for distress-context briefings per R-24):

> Pragmatic Phase 1 scope = single primary segment; Communications Cloud CPQ core + customer or partner portal (Experience Cloud); 4–6 month delivery window; reference-led pricing conversation. Explicitly excluded: multi-cloud, RCA-on-Core, full BSS replacement, NaaS four-layer scope, ORD separation.

**NaaS boundary enforcement (R-22):** If any motion invokes NaaS, map against Experience / Business / Operational / Network layers. State explicitly: Network Layer is not Salesforce scope.

Read `references/enxoo-credibility-anchors.md` to weave verified Enxoo credentials into outreach framing — Salesforce Consulting Partner + Advisory Board membership, Mplify Alliance and TM Forum membership, 2024 NaaS whitepaper, and the reference customer matrix.

**Reference discipline in Stage 6 output:**

- Use only Section 3.1 (✅ RFP) references by name in outreach-facing text
- Section 3.2 (⚠ Internal) references may inform motion choice and internal notes but must appear anonymized in briefing outreach angle (e.g., "a Tier-1 African wholesale carrier" not "MTN")
- Never cite Section 3.3 (❌ Not usable) entries
- Never cite KB-1 market references (DE-CIX as KB-1 example, du as KB-1 reference operator, Bayobab, etc.) as Enxoo delivery references
- When the recommended motion has no ✅ RFP reference for the prospect's segment (e.g., SEG-4 Data Center, SEG-6 IX), surface the reference gap explicitly in the Flags section rather than stretching a neighbouring reference
- Apply architecture caveat when prospect is on-Core / RCA path — Enxoo's flagship references are CMP / Vlocity

Include a "Skip, and explicitly" note listing motions that might seem relevant but aren't appropriate for this prospect right now.

**Outreach angle composition — stakeholder-adapted variants (v0.3.1):**

Per the Communication Style rules, Stage 6 must produce stakeholder-adapted outreach variants when Stage 5 has identified two or more priority stakeholders from different archetypes.

**Variant count rule:**

- **1 priority stakeholder, or all in same archetype** → 1 outreach variant, keyed to that archetype
- **2 priority stakeholders in different archetypes** → 2 variants, one per archetype
- **3+ priority stakeholders spanning 3+ archetypes** → 3 variants max (pick the 3 highest-priority archetypes); do not produce 4 variants in a single briefing

**Variant discipline:**

- All variants cite the same motion(s) — the motion recommendation does not change per stakeholder
- Variants differ in language register, cited outcomes, and decision frame per archetype
- All variants maintain the same gap disclosure (architecture caveat, reference gap, distress context)
- Each variant: 2–4 sentences, grounded in specific research findings, uses appropriate language per prospect market (Polish, Arabic, English)
- Never append "hope you're well" or similar lead-ins
- Never produce a generic "for all audiences" variant alongside archetype variants

**Variant format:**

```
**Outreach angle — [Archetype name] variant** ([target stakeholder role])

[2–4 sentence pitch in archetype register]
```

Example — dual-variant output for a prospect with both a CFO and a CTO in the priority stakeholder list:

```
**Outreach angle — CFO variant** (Finance Director)

du International Wholesale cut their margin-erosion risk by locking supplier 
margin at customer-quote stage — the same pattern delivers DSO improvement 
and inter-carrier settlement accuracy. Short call to walk through the 
commercial case, not the platform architecture.

**Outreach angle — CTO/CIO variant** (Chief Network Officer)

Your NaaS positioning on the Mplify member directory suggests an active 
LSO Sonata roadmap. We've operationalized the Experience + Business layer 
of that architecture at DTGC — TMF-aligned north-south, LSO east-west, 
OSS stays specialist. Short session to map our blueprint against yours.
```

This matches the stakeholder-adapted tone specification in the Communication style section at the top of this document.

---

### Stage 7 — Compose the briefing

Emit a structured markdown briefing using this exact shape:

```
# [Prospect name] — Enxoo Prospect Briefing

**Briefing type:** [Public-only | SFDC-enriched]
**Briefing date:** [today]
**Research sources:** [count]

[If Section 11.5 signal active: one-line bold banner here]

## Group structure

[Embed the FigJam diagram link produced in Stage 1. Do not duplicate its content as text, JSON, or prose. The diagram is the canonical representation.]

## Segment landscape — Layer 1

[Full segment table with In Scope flags, revenue%, FTE, growth, importance, 
notes, confidence markers]

### Segments intentionally not analyzed

[Out-of-focus list with justifications]

## Target segment deep dive — Layer 2

[Per operating entity, per ✅ Target segment:]
- Primary segment classification with confidence (Q1–Q11 evidence)
- Secondary overlaps if applicable
- Signal profile (Section 11 matches)
- NaaS maturity profile (if cross-segment applicable)

## Governance & distress context

[Four outputs per Section 11.5.4, if applicable]

## Stakeholder map

[3–5 priority stakeholders with language variants, buying roles, 
warm-path flags, procurement ⚠]

## Recommended motions

[Maximum 2 motions by ID from sales-motions.md]

For each:
- Motion ID and name
- One-line fit rationale (segment + signals evidence)
- Enxoo accelerators involved
- Salesforce footprint (validated against sequencing rules)
- First-meeting anchor
- Boundary — what not to overclaim
- Phase 1 / Phase 2 sequencing if Agentforce involved

### Skip, and explicitly

[Motions that might seem relevant but aren't — 1-line rationale each]

## Outreach angle

[Stakeholder-adapted variants per Communication Style rules. 1 variant if single 
archetype, 2–3 variants if multiple archetypes. Each variant: 2–4 sentences, 
grounded in specific evidence, archetype-specific language register; Polish for 
Polish prospects, bilingual EN/AR for GCC public sector, English otherwise]

## Flags

- 🔴 Blockers / red-zone risk
- 🟡 Active risk
- 🟢 Positive differentiator

[Must include: procurement-scale risk per Section 11.5.3; language recommendation; 
NaaS Network Layer overclaim risk if X-1 proposed; SFDC data staleness if enriched; 
confidence markers summary if any Layer 1 cell is Low/Unknown]
```

**Every factual claim** carries a confidence marker and inline citation.

---

### Stage 8 — HTML output rendering (optional, v0.3)

When the user requests HTML output ("HTML version," "branded report," "for the deck," "executive summary," or uses `--html`), emit a self-contained single-file HTML document styled to Enxoo brand.

**Design tokens (Enxoo brand):**

- Primary navy: `#1F2043` (headings, accent bars, key metrics)
- Alternate navy: `#0B1E4D` (deeper accent, hover states)
- Light blue: `#D0EDFE` (secondary backgrounds, callout blocks)
- Cyan accent: `#00C8E0` (flags, confidence markers, active indicators)
- Background: white `#FFFFFF`; soft grey `#F5F7FA` for secondary panels
- Body text: `#1A1A2E` on white; adequate contrast ratios
- Typography: `Lato` primary (body), `Plus Jakarta Sans` fallback for headings; system font stack as ultimate fallback
- Base font size: 14px body, responsive scaling
- Layout: single-column, 800px max content width, generous whitespace

**Required structural elements:**

1. **Header block** — Enxoo wordmark (text-based; no external image dependency), prospect name (H1), briefing type (Public-only / SFDC-enriched), briefing date, research source count
2. **Distress banner** (if Section 11.5 signal active) — coloured banner at top of content, before group structure
3. **Group structure section** — embed the FigJam diagram link from Stage 1 as a prominent call-out card (e.g., styled button or link block labelled "Open group structure diagram in FigJam"). Do not render a text hierarchy or JSON block — the diagram is the sole representation.
4. **Layer 1 segment landscape** — styled HTML table with colour-coded in-scope cells (✅ green tint, ⚠ amber tint, ❌ grey tint)
5. **Segments intentionally not analyzed** — callout block with muted styling
6. **Layer 2 target segment deep dive** — per-entity card with classification + confidence + rationale (including AP-S citations per v0.3)
7. **Governance & distress context** — four-output block (banner / motion-sizing / procurement-pattern / timing) if applicable
8. **Stakeholder map** — card grid, 3–5 stakeholders visible, warm-path annotations visible
9. **Recommended motions** — max 2 motion cards, each with motion ID, rationale, accelerators, footprint, boundary
10. **Skip list** — muted section below motions
11. **Outreach angle** — one or more quote cards, each labelled with archetype and target role per Stakeholder-adapted variants from Communication Style rules. Each variant rendered as its own blockquote with an archetype badge header. When single-archetype briefing, one quote card only.
12. **Flags** — colour-coded indicator rows (🔴 red, 🟡 amber, 🟢 green) with icons
13. **Footer** — Enxoo wordmark, briefing date, "Generated by researching-telco-prospects v0.3" attribution

**Technical constraints:**

- Single-file HTML — all CSS inline in `<style>` block; no external stylesheets
- No external JavaScript — this is a static report, not an interactive dashboard
- No external images — Enxoo wordmark rendered as styled text or inline SVG (no logo file dependency)
- No network fetches at render time — prospect-specific images optional but must be base64-embedded if included
- PDF-conversion-friendly — pages should paginate cleanly when printed to PDF via browser print
- Works offline — opens correctly from local disk
- Semantic HTML5 — `<header>`, `<main>`, `<section>`, `<article>` for accessibility and PDF structure
- All content from Stage 7 markdown briefing preserved — no content omitted; the HTML is a re-rendering, not a summary

**Content parity rule:**

The HTML output contains **exactly the same content** as the markdown briefing — same citations, same confidence markers, same AP-S citations, same warm-path annotations, same motion recommendations. HTML is a presentation layer over the same substance. Anything that would appear in the markdown flags section appears in the HTML flags section. No "marketing polish" is added to the HTML — it is the same briefing, styled.

**File delivery:**

- Save to `/mnt/user-data/outputs/` with filename pattern: `{prospect-slug}-enxoo-briefing.html`
- Present via `present_files` tool
- If both markdown and HTML requested, produce both; the markdown goes first (easier to copy-paste), HTML second

**Do not use HTML mode for:**

- Mobile summary (use mobile markdown format instead — HTML over-styles a short briefing)
- Draft / iterative briefings where content is still being refined (markdown is faster to edit)
- Internal-only briefings that will never leave Slack (markdown is lighter)
- Briefings containing ⚠ Internal reference customers by name (HTML is shareable; anonymize rigorously or emit markdown only)

HTML output is for **external-audience-ready briefings** — client meetings, executive reviews, deal reviews, stakeholder distribution. For quick research and team chat, markdown is the right default.

---

## Mobile summary format

When user requests a mobile / quick version, produce:

```
# [Prospect] — Quick Briefing

[Banner if distress]

**Classification:** [Primary segment(s) per operating entity with confidence]

**Top 3 stakeholders:**
1. [Role, named person or search string, buying role]
2. [...]
3. [...]

**Top 2 motions:**
1. [Motion ID — 1-line fit]
2. [Motion ID — 1-line fit]

**Outreach:** [2 sentences, archetype-keyed to highest-priority stakeholder — single variant for mobile brevity]

**Critical flags:** [2–3 flags max]
```

Target: 25–30 lines, 1.5 screenfuls on mobile.

---

## Output discipline

- Full briefing target: ~100 lines. Mobile summary target: ~30 lines.
- Inline citations only: `(Source: publisher, date, URL)`. No end-of-briefing Sources index.
- Confidence marker on every numeric, structural, or classification claim: `(High)`, `(Medium)`, `(Low)`, `(Estimated)`, `(Unknown)`.
- AI inference without corroboration flagged as `inferred — no primary source`.
- Paraphrase sources. Do not quote more than 15 words from any source. One quote maximum per source.
- If distress or restructuring signals are active, the briefing header names it openly.
- If `mode = public-only`, note at the end that checking Salesforce history before outreach is recommended.

**Mandatory flags checklist before emission:**

- Procurement-scale flag result from Stage 1 ownership type
- Language recommendation based on prospect market
- SFDC data staleness note if `mode = SFDC-enriched`
- NaaS Network Layer boundary if Motion X-1 proposed
- Confidence-marker summary if any Layer 1 cell is Low/Unknown

**Anti-pattern compliance check before emission** — verify none of the following are violated:
AP-S1, S3, S4, S6, S7, S18, S19, S21, S22, S23, S24.

---

## References

The skill's `references/` directory contains:

- `KB1_Customer_Segmentation_Reference_v1_9.md` — canonical segmentation, qualification matrix, operational patterns, external signal set, governance & distress signals. Loaded in Stage 3a.
- `stakeholders-and-triggers.md` — per-segment stakeholder maps (Part A) and trigger catalog (Part B). Loaded in Stages 4 and 5.
- `sales-motions.md` — Enxoo motions per segment cluster with motion IDs. Loaded in Stage 6.
- `salesforce-clouds.md` — cloud-to-segment platform footprint and sequencing rules. Loaded in Stage 6 when platform-fit detail is needed.
- `enxoo-credibility-anchors.md` — verified Enxoo credentials, three-tier reference matrix (✅ RFP / ⚠ Internal / ❌ Not usable), segment-to-reference mapping, whitepaper, memberships. Loaded in Stage 6 for outreach framing.
- `html-briefing-template.html` — Enxoo-branded HTML template with inline CSS. Loaded in Stage 8 when HTML output is requested. Contains placeholder tokens (`{{PROSPECT_NAME}}`, `{{LAYER1_ROWS}}`, etc.) that Stage 8 populates from briefing content.

Progressive disclosure principle: load only what the current stage needs. Do not load all references at startup.

---

## What this skill does not do

- Produce interactive HTML dashboards — v0.3 emits a styled **static** HTML briefing, not an interactive dashboard with filters or drill-down
- Replace Salesforce queries — the BDR pastes SFDC data if relevant
- Guarantee classification accuracy for entities outside KB-1's 8-segment scope (pure media companies, financial services, retail are outside scope)
- Compose outreach in any language other than English, Polish, or bilingual English-Arabic in v0.3 — other languages flagged as needing translation
- Recommend competitor partners; if Enxoo is not a fit for a prospect's needs, the briefing says so
- Use CRM data to define segmentation, segment revenue, or group structure — CRM is canonical for account state only (R-23 + Source Discipline)
- Fabricate warm paths — warm-path detection (Stage 5) surfaces only observable LinkedIn overlap signals; absence of signal means `no overlap`, not inferred advocacy

---

## Open items for v0.4

Shipped in v0.3:
- ✅ Warm-path detection via LinkedIn overlap (Stage 5)
- ✅ AP-S code inline citations in classification rationale (Stage 3b)
- ✅ HTML output mode with Enxoo branding (Stage 8)

Deferred to v0.4:
1. No-public-data fallback for stealth / PE-owned operators — minimum viable briefing format
2. Trigger freshness decay logic (14+ months) — age-weight warmth scores
3. Czech, Hungarian, German role variants for remaining CEE / DACH markets
4. Native-language role variants for GCC beyond basic Arabic
5. PDF output (print-to-PDF works from HTML, but native PDF rendering could be v0.4)

---

## Version history

| Version | Date | Summary |
|---|---|---|
| 0.1 | — | Initial draft. Single-segment briefing per prospect. |
| 0.2 | 2026-04-24 | Dual-layer segmentation (Layer 1 landscape + Layer 2 deep dive). Group structure mapping. Source discipline with confidence scoring. Non-blocking Stage 0. Motion cap at 2 with ID citation. Salesforce sequencing enforcement. Pragmatic Phase 1 definition. FTTH exception to B2C exclusion rule. Mobile summary format. Polish and Arabic role variants. Credibility anchors file added. |
| 0.3 | 2026-04-24 | Warm-path detection via LinkedIn overlap in Stage 5. AP-S code inline citations in Stage 3b classification rationale (all 24 codes catalogued). Enxoo-branded HTML output mode (Stage 8) — single-file, offline-capable, PDF-conversion-friendly. Reference matrix updates: DTGC 🟢 live, DE-CIX 🟢 live (first on-Core reference), du split into International Wholesale 🟢 live + ICT 🚧 in progress. |
| 0.3.1 | 2026-04-24 | Communication Style discipline added. Two-register system: BDR-internal tone (direct, structured, analytical) for briefing body Stages 0–7; stakeholder-adapted tone for outreach angle Stage 6. Four archetypes: CFO, Sales Leadership, CTO/CIO, Operations/Delivery — each with emphasis priorities, vocabulary rules, decision frames. Outreach angle produces 1–3 variants per briefing depending on priority stakeholder mix. HTML template updated with variant badges and per-archetype colour coding. Mobile summary keeps single variant for brevity. |
| 0.3.2 | 2026-04-24 | Stage 1 output format replaced: group structure is now a FigJam diagram (via `Figma:generate_diagram` with Mermaid `flowchart TD`) as the sole artifact. Prior text hierarchy, JSON block, and implications paragraph removed. Diagram required for every briefing; operating entity marked with double-bordered shape; in-scope flags colour-coded. Stage 7 briefing and Stage 8 HTML rendering updated to embed the FigJam link in place of text/JSON duplication. |
