---
name: enxoo-artifact-forge
description: >
  Stamps out new Enxoo artifact-producing skills in house style, or retargets an
  org-coupled Salesforce skill (forcedotcom / afv-library pattern) into one that emits
  a deliverable ARTIFACT + reusable BLUEPRINT instead of deploying to an org.
  TRIGGER when: the user wants to create, scaffold, convert, retarget, or "przerobic"
  a skill so it produces artifacts/blueprints (docs, decks, diagrams, HTML cockpits,
  metadata bundles) - including "zrob skilla ktory generuje X", "przerob ten skill na
  artefakt", "fabryka skilli", "skill-forge".
  DO NOT TRIGGER when: the user wants to RUN an existing skill to produce a deliverable
  now (use that skill directly), author raw Apex/LWC/Flow for org deploy (use the
  forcedotcom skill as-is), or change brand tokens only (use enxoo-brand-theme).
metadata:
  client_safe: "false"
---

# Enxoo Artifact Forge - meta-blueprint for artifact/blueprint skills

Purpose: take the forcedotcom skill anatomy (SKILL.md contract + references/ + assets/
+ hooks/) and produce skills whose **definition of done is an emitted deliverable that
conforms to a blueprint and passes Enxoo brand + client-safe validation** - not an org
deploy. Reasoning in Polish; generated skill content and deliverables in English.

## Core model
Read `references/artifact-vs-blueprint.md` before authoring.
- ARTIFACT = one concrete deliverable file (this client's PDD / RFP section / diagram).
- BLUEPRINT = reusable, parametrised template + reference the artifact is generated FROM
  and validated AGAINST. Lives in references/ + assets/, versioned, brand-locked.
- Contract: skill reads blueprint -> produces artifact -> validates artifact vs blueprint
  + brand + client-safe -> emits artifact (and optionally an instantiated blueprint).

## Required inputs (gather or infer; ask only if genuinely blocking)
- Deliverable type + business goal (PDD, ADR, RFP section, reference-architecture diagram,
  capability deck, prospect cockpit, estimation model, ...).
- Blueprint source: an existing Enxoo skill/template to reuse, or "new".
- Output format(s): docx | pptx | html | md | diagramforce-json | xlsx | svg.
- client_safe tier: internal (client_safe:false) or client-facing (MUST pass redactor).
- Render skills to delegate to: docx, pptx, enxoo-deck, diagramforce / telco-diagramforce,
  enxoo-brand-theme.

## Workflow - follow in order. Do not skip, merge, or reorder. Mark N/A with a one-line reason.

### Phase 1 - Author the new skill
1. Pick the blueprint. If reusing, cite the source skill. If new, define the blueprint
   schema in references/ FIRST (required sections, parameters, brand slots).
2. Read house style in `references/artifact-vs-blueprint.md` (frontmatter fields, PL/EN
   rule, brand tokens, OKF facet rule, output-dir contract).
3. Write the new skill's SKILL.md as an ordered-phase contract whose Phase-2 exit criteria
   are ARTIFACT-based (see `assets/generated-skill-template.md`), NOT org-based.
4. Fill references/ with the decision tree (which blueprint variant for which situation),
   using consequences-over-commands ("X fails because Y"), one rule per short section.
5. Fill assets/ with a COMPLETE, brand-locked deliverable template (few-shot by example) -
   never a stub. Non-negotiables (brand tokens, OKF structure) baked into the template.

### Phase 2 - Validate (retargeted from Code Analyzer)
6. Run `hooks/validate-deliverable.py` against a dry-run generation. It checks:
   (a) artifact file(s) written to the declared output dir;
   (b) Enxoo brand tokens present;
   (c) if client-facing, enxoo-client-redactor passed with zero internal-canon leaks;
   (d) blueprint conformance (all required sections present).
   Remediate until clean.
7. Score against the rubric in references/ (completeness / brand / blueprint conformance /
   client-safety). Report the number; block below threshold.

### Phase 3 - Report
8. List generated files (paths), blueprint used, rubric score, install instructions, and
   one "how to invoke" example. State the output dir explicitly.

## Guardrails
- Never mark done without an artifact file physically written to the declared output dir.
- Client-facing artifacts MUST pass enxoo-client-redactor as a BLOCKING hook before done.
- Brand tokens come from enxoo-brand-theme - do NOT hardcode colours/fonts in generated skills.
- Segment is always a multi-valued facet on concepts (OKF rule), never a folder, in any
  generated blueprint that touches KB-1.
- The generated skill's frontmatter description MUST use TRIGGER / DO NOT TRIGGER and name
  the excluded skills explicitly.

## Two build paths
- NEW skill: scaffold from `assets/generated-skill-template.md`.
- CONVERT a forcedotcom skill: keep the phases / exit-criteria / scoring skeleton; then
  replace Validate(org) -> Validate(artifact); replace Report(deploy) -> Report(deliverable);
  convert .cls assets -> deliverable templates; swap the Code-Analyzer hook ->
  validate-deliverable.py.


## Reverse mode (universal, default operating principle)
Read `references/reversal-rule.md`. For ANY source skill - and especially org-mutating
forcedotcom / afv-library skills - the default action is to REVERSE it:
- Axis 1 (direction): org-deploy -> portable configuration artifact, org optional.
- Axis 2 (specificity): bespoke -> STANDARD out-of-the-box baseline that runs with zero
  required inputs, defaults grounded in TMF SID / eTOM / ODA / SF standard model / KB-1,
  every default citing its source. Parameters only refine the standard; they never gate
  first output.
Reversed-skill definition of done: running with no arguments emits a conformant standard
baseline artifact to the output dir. See the Data Cloud worked example in reversal-rule.md.


## Decompose mode (universal, the complement of Reverse)
Read `references/decompose-rule.md`. Given ANY artifact/blueprint (a PDD, reference
architecture, standard config, solution design, "b-07", ...), decompose it into the
configuration of individual environment elements, in recommended deploy order:
artifact -> VALIDATE decomposability (gap list, no guessing) -> DECOMPOSE into typed
elements -> SEQUENCE by the canonical deploy ladder (topological; cross-rung deps win) ->
EMIT a numbered deploy-plan where each step states which prerequisite gates its position.
Round-trip: Reverse (org -> standard config artifact) and Decompose (artifact -> deploy
plan) are inverses; an artifact produced by one should survive the other.
