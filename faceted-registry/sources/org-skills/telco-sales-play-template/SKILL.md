---
name: telco-sales-play-template
description: Standardised solution-selling sales play template for Enxoo's eight KB-1 telecom segments — durable, segment-anchored, reusable. Twelve-section structure synthesised from Salesforce Sales Play methodology, Miller Heiman Strategic Selling, and Challenger Sale, with Internal (sales enablement) and External (customer-facing) blocks separated. Trigger when an Enxoo user asks to build, draft, refine, document, review, or instantiate a sales play, segment play, go-to-market play, account play, or solution-selling play — including informal phrasings ("how should we approach selling to wholesale", "what's our story for ICT", "help me think through the FTTH pitch"). Trigger also when the user asks for a segment's ICP, discovery questions, objection handling, buying criteria, or exit criteria without naming a specific prospect. For per-prospect work on a named company, use `telco-prospect-briefing` instead.
---

# Telco Sales Play Template

Segment-anchored sales play structure for Enxoo's eight KB-1 telecom segments. Output is structure-first, dual-use (Internal / External blocks separated), slide-friendly, and grounded in documented enterprise sales methodologies.

This skill is the segment-level half of Enxoo's telecom sales motion. Pair with `telco-prospect-briefing` for per-prospect intelligence. The play is durable per-segment; the briefing instantiates the play against one named prospect.

## When to use this skill vs. the briefing skill

| Trigger | Skill |
|---|---|
| "Build the play for SEG-1b" / "what's our ICP for wholesale data?" / "draft discovery questions for ICT" | **This skill** |
| "Research [Company X]" / "brief me on [operator]" / "qualify [name]" | `telco-prospect-briefing` |
| "Apply the wholesale play to [Company X]" | Both — start here for the play, then run the briefing skill against the prospect |

## Methodology spine

Synthesis of three documented frameworks:

| Framework | Used for |
|---|---|
| Salesforce Sales Play | 12-section structure; Internal/External block separation; value hypothesis as testable claim |
| Miller Heiman Strategic Selling | Buying-role tags (DM, BH, CH, INF, GK, USR); Single Sales Objective; Personal Win analysis; Red Flags; decision-process map |
| Challenger Sale | Commercial Insight / reframe in core-problem section; acknowledge → reframe → evidence pattern in objection handling; Mobiliser identification (distinct from DM) |

**Why the synthesis works.** MH provides *who* (buying roles, decision navigation). Challenger provides *how* (insight, reframing, take-control). Salesforce Plays provide the *structural spine*. Where the frameworks disagree, choices are documented in `references/methodology-notes.md` — read that file when calibrating the play, not on first use.

**Assumption flagged:** "Salesforce Sales Play methodology" is documented in Salesforce enablement materials but not in a single canonical published spec. The 12-section list represents the union of section headings observed across published Salesforce play templates; if Enxoo has an internal definition that differs, that takes precedence.

## Inputs

Required: **target segment** (one of SEG-1a, 1b, 1c, 2, 3, 4, 5, 6, 7a, 7b per KB-1 v1.13).
Optional: existing Enxoo motion ID (W-1, E-1, etc.) if the play should be anchored to a specific motion.
Optional: language (EN default; PL or EN+AR available per `telco-prospect-briefing` Stage 7 rule).

## Workflow when populating a play

1. **Confirm segment.** Ask which KB-1 segment if not stated. Don't proceed without it — the play is segment-anchored, not generic.
2. **Read `references/play-spec.md`** — the canonical 12-section specification with Internal/External block guidance. This is the structural spine.
3. **Load supporting references progressively** (mirrors `telco-prospect-briefing` Stage discipline):
   - Segment confirmation: KB-1 segment row + Q1–Q11 only (not full KB-1)
   - Personas: `stakeholders-and-triggers.md` segment-specific section
   - North Star: `sales-motions.md` motion matching the segment
   - External wording: `enxoo-customer-facing-profile.md` Sections 4 + 5 + 7
   - Proof categories: `enxoo-credibility-anchors.md` Section 5.1 (categories only — not named references)
4. **Populate each of the 12 sections** in order. **Internal block first, then External block.** Don't write External and back-fill Internal — guidance language leaks. The reason is operational, not stylistic: once leak occurs, the seller has to manually scrub before customer use, which negates the time the play saves.
5. **Validate against anti-patterns** before publishing — see Anti-pattern audit section below.
6. **Read `references/worked-example-SEG-1b.md`** for calibration. It's the populated play for SEG-1b Wholesale Data anchored to motion W-1, demonstrating section depth, dual-block discipline, and anti-pattern enforcement. Use it as a level-of-specificity reference when populating other segments.

## Output discipline

- Internal and External blocks remain visually separated. No interleaving.
- No pricing, no ROI numbers, no specific customer stories at the play level (those live in the briefing).
- No invented frameworks. Where a structural choice isn't documented in Salesforce / MH / Challenger published material, mark the assumption explicitly.
- A populated play is segment-anchored. Do not write a generic cross-segment play.
- Per AP-S25: External blocks never lead with accelerator IDs (ACC-###). Accelerators support, never lead.
- Per AP-S26: no standalone Agentforce play. Agentic variants are companion-only.
- Per R-22: Network Layer (SDN, optical activation, OTN device-level orchestration, GIS) never claimed as Enxoo scope.
- Per R-26: per-segment customer-facing names ("Enxoo for Carriers" etc.) used externally; "Enxoo for Communications" deprecated.
- Permanent named-entity exclusions per skill memory honoured throughout.

## Anti-pattern audit (run before publishing the play)

Tick each before declaring the play complete:

- ☐ AP-S25 — External blocks lead with operator outcome / North Star, not accelerator IDs. ACC-### IDs appear only in Internal blocks.
- ☐ AP-S26 — No standalone Agentforce; Agentic variants positioned as companions only.
- ☐ AP-S1 / R-05 — Government / regulated treated as overlay tag on the primary segment, not as a separate "Government" segment.
- ☐ R-22 — Network Layer scope explicitly excluded in Section 6 boundaries and Section 8 stance.
- ☐ R-25 — Motion is outcome-led; accelerators support, never lead.
- ☐ R-26 — Customer-facing name from the per-segment list used; deprecated "Enxoo for Communications" not used.
- ☐ R-27 — Reference-status logic operates at the *briefing* layer (per-prospect), not the *play* layer. The play applies whether the prospect is a confirmed reference or cold; the briefing tunes the messaging.
- ☐ Permanent exclusion — no excluded named entities appear anywhere in the play.

## Slide layout guidance

The 12 sections do not map 1:1 to slides. Recommended slide compression:

| Slide | Sections |
|---|---|
| 1 — Segment frame | 1 (ICP) + 3 (Core problem) |
| 2 — Buyer landscape | 2 (Personas) |
| 3 — Pain & impact | 4 (Pains) |
| 4 — Discovery toolkit | 5 (Discovery questions) |
| 5 — Value hypothesis | 6 (North Star) + 7 (Proof categories) |
| 6 — Competitive position | 8 (Differentiation) + 9 (Objection handling, top 3 only) |
| 7 — Decision navigation | 10 (Decision process) + 11 (Sales motion stages) |
| 8 — Success criteria | 12 (Metrics & exit) |
| Appendix | Section 9 full objection table; Section 11 internal artefact map |

Eight slides plus appendix. Internal-only material in speaker notes or a separately bound enablement deck.

## References

- `references/play-spec.md` — canonical 12-section specification (purpose, expected detail, Internal/External guidance per section). **Read this first when populating a play.**
- `references/play-template.md` — empty copy-and-fill template, formatted for direct use.
- `references/worked-example-SEG-1b.md` — fully populated play for SEG-1b Wholesale Data, anchored to motion W-1. Use as calibration reference for level of specificity, dual-block discipline, and anti-pattern enforcement.
- `references/methodology-notes.md` — synthesis notes: which framework contributed what, where they disagree, where assumptions were made. Read when calibrating, not on first use.

## What this skill does not do

- Does not generate prospect-specific briefings — that is `telco-prospect-briefing`.
- Does not produce numeric ROI, pricing, or specific customer stories.
- Does not invent new sales methodologies — synthesises documented ones.
- Does not cover segments outside KB-1's 8-segment scope.
- Does not replace the briefing skill's stakeholder map for a *named* prospect; provides the persona *template* the briefing instantiates.
- Does not name entities under permanent exclusion per skill memory.
