---
name: enxoo-solution-design
description: >
  Structured solution design workflow for Enxoo presales and RFP engagements. Use this skill
  whenever working on any Enxoo client deliverable that involves requirements analysis, solution
  architecture, traceability, or executive narratives — including RFP responses, proposals,
  capability decks, SOW inputs, or client presentations. Triggers include: "analyze these
  requirements", "map to Salesforce", "build a traceability matrix", "create a capability
  section", "draft the executive summary", "define deliverables", or any time the user uploads
  an RFP, SOW, requirements list, or client brief. Always use this skill when the input is a
  client document and the output is a structured presales artifact, even if the user doesn't
  explicitly ask for a "skill".
---

# Enxoo Solution Design Skill

Six modular skills for structured presales and RFP work, covering the full arc from raw
requirements through to executive narrative. Each skill can run independently or as part of
a sequence.

---

## Skill Selection

Ask the user which skill(s) to apply — or infer from context:

| Skill | Trigger phrases / context |
|-------|--------------------------|
| **S1 Requirements Structuring** | "extract requirements", "analyze RFP", uploaded RFP/SOW/brief |
| **S2 Capability Synthesis** | "define capabilities", "what can we offer", requirements registry available |
| **S3 Architecture Mapping** | "map to Salesforce", "which components", "integration", capability list available |
| **S4 Deliverables Engineering** | "define deliverables", "what will they receive", "project timeline" |
| **S5 Traceability** | "traceability matrix", "compliance matrix", "golden thread", "coverage" |
| **S6 Executive Storytelling** | "executive summary", "board narrative", "C-level version", "one-pager" |

Skills build on each other (S1 → S2 → S3 → S4 → S5 → S6), but can be entered at any point
if prior outputs are already available (e.g., pasted requirements, existing capability list).

**Input types accepted:** RFP documents (.docx, .pdf), Excel requirements sheets (.xlsx),
pasted text, or structured Markdown from a previous skill output.

**Output format:** Structured Markdown by default. State this upfront; offer table variants
where noted.

---

## S1 — Requirements Structuring

**Purpose:** Extract explicit and implied requirements from source documents; produce a
structured Requirements Registry.

### Steps

1. **Parse the input.** Read the full document. Note: requirements appear in body text,
   tables, appendices, and footnotes — do not skip non-body sections.

2. **Extract explicit requirements.** Capture verbatim or near-verbatim statements of
   what the client requires. Assign sequential IDs: `REQ-001`, `REQ-002`, etc.

3. **Extract implied requirements.** Read "current state" descriptions, pain points, and
   problem statements for unstated needs (e.g., "our billing takes 3 days" implies a
   requirement for automation).

4. **Categorize each requirement:**
   - **Functional** — business process, user role, workflow, reporting
   - **Technical** — integration, performance, security, standards
   - **Business Outcome** — strategic objective, efficiency target, compliance

5. **Assign priority:** Mandatory / Preferred / Optional (use RFP language as signal:
   "shall" = Mandatory, "should" = Preferred, "may" = Optional).

6. **Cluster into business domains.** Group requirements by theme (e.g., CPQ, Billing,
   Order Management, Integration, Security). Use these clusters as the basis for S2
   capability groupings.

### Output: Requirements Registry

```markdown
## Requirements Registry

| REQ-ID | Category | Priority | RFP Ref | Requirement Statement | Domain | Stakeholder |
|--------|----------|----------|---------|-----------------------|--------|-------------|
| REQ-001 | Functional | Mandatory | Sec 3.1 | System shall support real-time billing for all service types | Billing | CFO, Billing Mgr |
| REQ-002 | Technical | Mandatory | Sec 4.2 | Solution must integrate with ERP via REST API | Integration | CTO |
| REQ-003 | Business | Preferred | Sec 2.1 | Reduce quote-to-order cycle from 5 days to 4 hours | CPQ | VP Sales |
```

**Also produce:** Domain summary — list each domain cluster with count of Mandatory /
Preferred / Optional requirements.

### Anti-patterns to avoid

- Do not paraphrase unnecessarily — risks keyword mismatch in compliance reviews
- Do not skip "obvious" requirements (e.g., security, data migration)
- Do not ignore non-functional requirements

---

## S2 — Capability Synthesis

**Purpose:** Translate requirement clusters into named business capabilities with defined
value and KPIs. This is the layer clients read — lead with outcomes, not features.

### Input
Requirements Registry from S1 (or pasted requirements list).

### Steps

1. **Group requirements into capabilities.** Each capability addresses multiple related
   requirements. One capability = one business function (e.g., "Convergent Real-Time
   Billing", not "Enxoo Billing Module").

2. **Name capabilities in business language.** Avoid product names and acronyms as
   capability names. Use outcome-oriented labels the client's C-suite would recognise.

3. **For each capability, define:**
   - **Business Purpose** — why this matters (outcomes first)
   - **Key Features** — what it includes (bullet list, business-readable)
   - **Addressed Requirements** — list REQ-IDs
   - **Differentiation** — specific advantage vs. alternatives (native Salesforce,
     pre-built telecom data model, TMF compliance, etc.)
   - **Proof Point** — reference an Enxoo case study or benchmark (Arelion, Nexera,
     Upp, DT Global Carrier, Quickline, Openserve, du ICT — use whichever is relevant)
   - **KPIs / Business Metrics** — quantified outcomes where possible

4. **Apply the "So What?" test** to every capability description. If removing the
   business outcome leaves only a feature list, rewrite.

### Output: Capability Catalogue

Use the format in `references/capability-template.md`. Example structure:

```markdown
## CAPABILITY: Convergent Real-Time Billing

**Business Purpose:**
Eliminate billing errors and revenue leakage across all service types (mobile, fixed,
broadband, IoT) on a unified invoice, with instant rating and charging.

**Addresses Requirements:** REQ-001, REQ-015, REQ-023, REQ-031

**Key Features:**
- Real-time event processing (<100ms latency)
- Multi-service convergent billing on single invoice
- Flexible pricing: subscription, usage-based, tiered, hybrid
- Automated revenue assurance validation at every step
- Multi-currency, multi-tax support

**Differentiation:**
Native Salesforce vs. external billing requiring integration; pre-built telecom billing
vs. generic financial systems; 80% out-of-box vs. extensive customisation.

**Proof Point:**
Arelion achieved substantial billing cost reductions and 30% sales efficiency improvement
via Enxoo Billing.

**KPIs:**
- Invoice generation: 3 days → 1 hour
- Billing accuracy: 88% → 99.5%
- Revenue leakage prevention: ~1.5% of revenue protected
```

### Anti-patterns to avoid

- Feature dumping: listing functions without connecting to requirements
- Vendor-speak: "robust", "comprehensive", "cutting-edge" without specifics
- Unclaimed differentiation: every differentiator must be provable

---

## S3 — Architecture Mapping

**Purpose:** Map capabilities to specific Salesforce and Enxoo technical components;
define integration patterns and TMF/MEF API touchpoints.

### Supported Salesforce Clouds (all except Commerce Cloud)

| Layer | Components |
|-------|-----------|
| **Platform** | Sales Cloud, Service Cloud, Communications Cloud (CMP / CCaaS on Core / Revenue Cloud), Experience Cloud, Agentforce, Einstein |
| **Enxoo Application** | Enxoo for Communications (EPC), PCM, Industries CPQ, OmniStudio / Vlocity, Order Management, Enxoo Billing, Enxoo API Hub |
| **Integration** | MuleSoft, MEF LSO Sonata APIs, TM Forum Open APIs (TMF620, TMF622, TMF641, TMF666, etc.) |
| **Data** | Product Catalog, Customer 360, Service Inventory |

### Architecture decision point

Before mapping, confirm which delivery architecture applies:
- **CMP (Vlocity/OmniStudio)** — managed package, typically wholesale/carrier
- **Communications Cloud on Core (Revenue Cloud)** — newer, product-led growth, enterprise

This determines which component names and deployment patterns to use.

### Steps

1. For each capability from S2, identify:
   - **Platform Foundation** (which Salesforce cloud)
   - **Application Layer** (which Enxoo product/module)
   - **Integration Layer** (MuleSoft connectors, API standards)
   - **Data Layer** (what data objects/catalog structures)

2. For each integration point, specify:
   - Protocol (REST, SOAP, event-driven)
   - Standard (TMF API number, MEF LSO Sonata, custom)
   - Direction (inbound / outbound / bidirectional)
   - System of record

3. Flag gaps: requirements that cannot be met out-of-box and require customisation,
   third-party tooling, or roadmap items.

### Output: Component Architecture Table

```markdown
## Component Architecture

### Capability: Convergent Real-Time Billing

| Layer | Component | Role | Notes |
|-------|-----------|------|-------|
| Platform | Salesforce Communications Cloud | Product Catalog, Order objects | TMF620 compliant |
| Application | Enxoo Billing Module | Billing runs, invoice generation, rating engine | AppExchange managed package |
| Application | Enxoo CPQ | Quote-to-invoice flow | Pre-built CPQ for telecom |
| Integration | MuleSoft | ERP financial sync | Standard ERP connector |
| Integration | Payment Gateway | Real-time payment processing | Stripe / custom |
| Data | Product Catalog | Service type definitions, pricing rules | Shared with CPQ |

**Integration Points:**
- ERP ← MuleSoft ← Salesforce (financial data sync, bidirectional, REST, nightly + event)
- Network Management System → MuleSoft → Service Cloud (service status, inbound, TMF641)
- Payment Gateway ↔ Enxoo Billing (real-time, REST)

**Gaps / Flags:**
- REQ-058: Legacy System X integration — custom REST wrapper required, +3 weeks
```

### Architecture diagram (text)

Include a layered ASCII diagram for complex architectures (see example in uploaded
`requirements_to_solution_mapping.md` Section 4.3).

---

## S4 — Deliverables Engineering

**Purpose:** Convert capabilities and components into concrete, role-specific, dated
deliverables with acceptance criteria. A deliverable is what the client receives and
can immediately use — not a feature.

### Deliverable rule: be specific

❌ "Comprehensive billing solution with invoice generation."
✓ "Automated invoice templates configured for 8 service types, matching client brand
guidelines, delivered Week 18, enabling immediate UAT with Q4 billing data."

### Deliverable categories

1. **Configured system components** — UI, workflows, approval rules, dashboards
2. **Data and content** — migrated records, loaded catalog SKUs, user accounts
3. **Documentation** — user guides, admin manuals, technical architecture docs
4. **Training** — role-specific workshops, train-the-trainer, knowledge base
5. **Operational artifacts** — SOPs, runbooks, monitoring dashboards

### Steps

1. For each capability, list deliverables **by recipient role** (not by component).
   Roles typically include: Sales Rep, Sales Ops, Billing Manager, Finance Team,
   Order Management, IT/Admin, Customer (via portal).

2. For each deliverable, specify:
   - **What** — exact artifact (e.g., "pre-configured approval workflow routing
     quotes >$50K to VP Sales")
   - **When** — project week number
   - **Who** — recipient role/team
   - **Acceptance Criteria** — measurable condition for sign-off
   - **Benefit** — one sentence on how they use it

3. Produce a **Deliverables Schedule Matrix** (phase / week / deliverable / owner /
   acceptance criteria).

### Output format

```markdown
## Deliverables: Automated Quote-to-Order Workflow

### For Sales Representatives
- Guided product selection wizard (15-min avg quote creation) — Week 16
- Mobile-optimised quoting interface — Week 16
- Electronic signature integration (DocuSign) — Week 18
- Pre-configured quote templates (client brand) — Week 16
- Training: "CPQ for Sales Users" 4-hour workshop — Week 24

### For Sales Operations
- Automated approval routing dashboard — Week 18
- Quote analytics and pipeline reports — Week 20
- Pricing rules configuration tool — Week 18

### For Order Management
- Automated order creation from approved quotes — Week 20
- Order validation rules (error prevention) — Week 20
- Order status tracking dashboard — Week 22

**Acceptance Criteria:**
- 95% of quotes generated in <20 minutes
- Automated quote-to-order in <2 minutes
- Zero manual data entry errors in validation testing
- 90% sales rep adoption within 30 days post go-live
```

---

## S5 — Traceability

**Purpose:** Build a complete REQ → Capability → Component → Deliverable golden thread.
Every requirement must have a path to a deliverable. No orphans.

### The "No Orphans" rule

- Every requirement maps to at least one capability
- Every capability maps to at least one component
- Every component produces at least one deliverable
- Gaps are explicitly stated with mitigation — never silently omitted

### Output formats

**Format A: Master Traceability Matrix** (requirement-centric, best for compliance appendix)

```markdown
| REQ-ID | Requirement | Priority | Capability | Components | Deliverable(s) | Compliance | Proof |
|--------|-------------|----------|------------|------------|----------------|------------|-------|
| REQ-001 | Real-time billing for all service types | Mandatory | Convergent Real-Time Billing | Enxoo Billing, Comm. Cloud Catalog | Invoice templates (Wk18), Rating engine (Wk20) | ✓ Full | Arelion case study |
| REQ-003 | Reduce quote-to-order cycle | Preferred | Automated Q2O Workflow | Enxoo CPQ, Approval Workflows | Quote wizard (Wk16), Order automation (Wk20) | ✓ Full | Arelion: +30% efficiency |
```

**Compliance indicators:**
- ✓ Fully Compliant — out-of-box or standard configuration
- ◐ Partially Compliant — requires customisation (explain)
- ○ Roadmap Item — planned release with date
- ✗ Not Supported — state alternative approach

**Format B: Capability-centric view** (best for solution narrative in Section 3)
Use the full capability block format from S2, with REQ-IDs embedded.

**Format C: Visual coverage map** (best for executive summary)

```
YOUR REQUIREMENTS    →    OUR CAPABILITIES    →    KEY DELIVERABLES

Billing & Revenue         Convergent Billing        • Real-time rating engine
- Real-time billing       - Event-driven engine     • Invoice automation (Wk18)
- Revenue assurance       - Automated validation    • Revenue dashboard (Wk26)
[REQ-036 to REQ-048]     [Section 3.3.4]           [Wk18-26 delivery]
```

### QA checklist (run before finalising)

- [ ] Every mandatory requirement shows ✓ Full or ◐ Partial with explanation
- [ ] No requirement has an empty Compliance cell
- [ ] All claimed proof points reference actual Enxoo case studies
- [ ] Component names are consistent across all sections
- [ ] Deliverable weeks are consistent with project timeline

---

## S6 — Executive Storytelling

**Purpose:** Convert the four-layer solution into a board-level narrative. Rule: 80%
business outcomes, 20% how you'll achieve them.

### Structure

1. **The client's situation** — their strategic challenge in their language (not ours)
2. **What changes** — the outcome state after implementation (not features, not phases)
3. **How we get there** — 3–5 capability headlines maximum (no component names)
4. **Why Enxoo** — one differentiated claim per point, backed by proof
5. **The ask** — clear next step

### Narrative principles

- Open with the client's pain or ambition, not with Enxoo
- Use the client's terminology from the RFP (mirrors their language back)
- Every claim needs a proof point — case study reference or benchmark
- Avoid: "industry-leading", "best-of-breed", "holistic", "end-to-end" as standalone
  claims — they are meaningless without specifics

### Output

Produce a structured Markdown narrative (3–5 paragraphs) suitable for:
- Executive Summary section of an RFP response
- Opening slide of a capability deck
- C-level briefing document

Optionally, produce a **"Golden Thread" one-liner** per major requirement cluster:
> "From [client pain] to [outcome] — via [capability] — delivered by [week]."

Example:
> "From 5-day manual quoting to 15-minute automated quotes — via Enxoo CPQ on
> Salesforce Communications Cloud — live in Week 16."

---

## Reference Files

| File | When to read |
|------|-------------|
| `references/capability-template.md` | When writing S2 capability blocks |
| `references/component-catalogue.md` | When mapping S3 architecture (Enxoo product details) |
| `references/proof-points.md` | When adding case study references (Arelion, Nexera, DT, du ICT, etc.) |

Read these files on demand — do not load all at once.

---

## Cross-Skill Quality Checks

Apply across all outputs:

1. **Terminology consistency** — same name for the same thing throughout; create a
   glossary if the RFP uses non-standard terms
2. **Quantity specificity** — replace "X" placeholders with client data when available
   (record volumes, user counts, SKU counts, transaction rates)
3. **No unattributed metrics** — every stat needs a source (APMP, case study, client data)
4. **Gap transparency** — partial compliance is always better than silence; state the gap,
   state the mitigation
