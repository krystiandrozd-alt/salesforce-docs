---
name: enxoo-brand
description: >
  Apply Enxoo brand standards to Word documents (.docx), proposals, offers, capability decks,
  and RFP responses. Use this skill whenever producing or reviewing any Enxoo document
  deliverable — proposals, commercial offers, capability decks, RFP responses, or any
  client-facing Word document. Triggers include: "create a proposal", "write an offer",
  "draft a capability document", "make an RFP response", "apply Enxoo branding",
  "format this document", or any request for a client-facing .docx. Also use when
  reviewing an existing document for brand compliance. Always apply this skill before
  producing any Enxoo client deliverable, even if the user does not explicitly mention branding.
---

# Enxoo Brand Guide — Documents

This skill defines brand standards for all Enxoo client-facing documents.
For DOCX creation mechanics, always read `/mnt/skills/public/docx/SKILL.md` first.

## Quick decision

| Task | Action |
|------|--------|
| Create new branded document | Apply tokens below → use docx skill to build |
| Review existing document for compliance | Check against rules below → report violations |
| Both | Build first, then self-review against checklist |

---

## Brand Tokens

### Colors

| Role | Hex | Usage |
|------|-----|-------|
| Primary / dark navy | `#1f2043` | All body text, heading text, table header fill |
| Light blue | `#d0edfe` | Table label column fill (alternating rows in summary tables) |
| White | `#ffffff` | Table value cells, text on dark fills |
| Brand red | `#e42313` | Logo only — do not use in document body |
| Brand teal | `#6bbfa3` | Logo only — do not use in document body |
| Brand yellow | `#ffd500` | Logo only — do not use in document body |

**Rule:** Document body uses only `#1f2043`, `#d0edfe`, and `#ffffff`. The red/teal/yellow are logo brand marks, not document colors. Never use default Word black (`#000000`) or blue hyperlink color — all text is `#1f2043`.

### Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Body text | Lato | 11pt | Regular | #1f2043 |
| Heading 1 | Lato | 18pt | Bold | #1f2043 |
| Heading 2 | Lato | 14pt | Bold | #1f2043 |
| Heading 3 | Lato | 12pt | Bold | #1f2043 |
| Heading 4 | Lato | 11pt | Bold | #1f2043 |
| Heading 5 | Lato | 11pt | Regular | #1f2043 |
| Heading 6 | Lato | 11pt | Italic | #1f2043 |
| Table text | Lato | 11pt | Regular | #1f2043 |
| Caption | Lato | 10pt | Regular | #1f2043 |

**Rule:** Lato is the only permitted font. If Lato is unavailable, fall back to Arial — never Calibri, Cambria, or Times New Roman.

### Page Setup

| Property | Value |
|----------|-------|
| Format | A4 |
| Orientation | Landscape (default for proposals/decks) |
| Page size (DXA) | w: 16838, h: 11906 |
| Margins | ~820 DXA all sides (~0.57") |
| Body text alignment | Justified (`both`) |
| Line spacing | ~1.14× auto |
| Language | en-GB |

For portrait documents (e.g. short memos), use A4 portrait: w: 11906, h: 16838.

### Heading Indentation (DXA)

| Level | Left indent | Hanging |
|-------|-------------|---------|
| H1 | 720 | 360 |
| H2 | 1170 | 360 |
| H3 | 1710 | 360 |
| H4 | 2340 | 360 |
| H5 | 3060 | 360 |

Spacing before/after all headings: 400 before / 200 after (in twips).

---

## Document Structure

### Cover / Summary Table

Every document opens with a metadata table. Use this structure:

| Field | Value |
|-------|-------|
| Prepared for | [Customer Name] |
| Version | 1.0 |
| Creation Date | [Date] |
| Valid Until | [Date] |
| Sales Contact | [Name] |
| Technical Contact | [Name] |

Table style: no visible borders, label column bold, value column regular, both in Lato 11pt #1f2043.

### Standard Proposal Structure

For full proposals/offers, use this section order:

1. Management Summary
   - Customer challenges & goals
   - Our solution benefits
   - Why Enxoo
2. About Enxoo *(optional)*
3. The Solution
   - Solution Overview
   - Solution Modules
   - Assumptions (General / Commercial / Technical / Integrations / Migration)
4. Project Approach
   - Timeline, Phases, Teams, Methodology, Governance, Change Management
5. Support and Maintenance
   - Early Life Support (Hypercare)
   - Managed Services
6. Commercials (Capex / Opex)
7. Case Studies and References

For capability decks and RFP responses, use the sections relevant to the request — do not force the full proposal structure.

### Table of Contents

Always include a ToC after the summary metadata table. The ToC must:
- Use Word's automatic ToC field (not manual text)
- Show H1–H3 levels
- Use dot leaders to page numbers

---

## Tables

- Default cell padding: 100 DXA all sides
- **Summary/metadata table header row:** fill `#1f2043`, text white, bold, centered
- **Summary/metadata label column:** fill `#d0edfe`, text `#1f2043`, bold
- **Summary/metadata value column:** fill `#ffffff`, text `#1f2043`, regular
- Data tables in body: header row fill `#1f2043` white text; body rows alternate `#d0edfe` / `#ffffff`
- Borders: `#cccccc`, 1pt single — summary table uses no visible borders
- Always set `ShadingType.CLEAR` (never SOLID)
- Always specify both table `columnWidths` array AND per-cell `width` in DXA

---

## Bullet Lists

- Use Word numbering config with `LevelFormat.BULLET` — never insert `•` as a Unicode character
- Level 0 indent: left 720, hanging 360
- Two bullet styles in template:
  - **Simple list:** plain bullet items
  - **Definition list:** **Bold label:** followed by normal text on same bullet

---

## Brand Compliance Checklist

When reviewing an existing document, check each item:

- [ ] Font is Lato throughout (no Calibri, Cambria, Arial, Times)
- [ ] All text color is #1f2043 (no default black #000000 or Word blue)
- [ ] No colors outside the brand palette
- [ ] Page setup matches A4 landscape (or portrait if appropriate)
- [ ] Heading hierarchy is H1 → H2 → H3 (no skipped levels)
- [ ] Heading indentation matches brand spec
- [ ] Summary metadata table present on page 1
- [ ] Table header rows use #1f2043 fill with white text; label columns use #d0edfe
- [ ] No Unicode bullet characters — Word numbering used
- [ ] Language set to en-GB
- [ ] ToC present and linked (for documents > 5 pages)
- [ ] No stray fonts, colors, or styles from paste operations

---

## Assets

Logo files are in `assets/`:
- `enxoo_logo_header.png` — compact logo for page headers
- `enxoo_logo_footer.png` — full logo for footer or cover page

Logo placement in headers: anchored top-right, approx 1.4cm wide × 0.5cm tall (EMU: cx=1403769, cy=509588).

---

## Notes for Future Expansion

- **Slide layouts** (PPTX): to be added — see separate enxoo-brand-pptx skill when created
- **Offer commercial tables**: pricing table formatting to be defined
- **Cover page design**: full branded cover page template pending

See `references/document-examples.md` for annotated examples of compliant documents.
