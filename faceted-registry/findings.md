# Faceted registry: findings

496 elements, 7 facets, classified from raw manifests snapshotted under `sources/` (445 copied files plus the session tool registry, the scheduled-task list and three hooks). Every facet value links to a manifest line. Numbers below are produced by `scripts/analyze.py` and `scripts/kappa.py`; rerun `scripts/run_all.sh` to reproduce.

**About the name.** Nothing called "pompy" exists in either repo or in the GitHub account. We agreed the catalog is the whole toolkit visible to this session: 340 SKILL.md files (including the 27 ISV/OEM Advisor skills), 25 plugins, 15 commands, 5 agents, 100 MCP servers (80 distinct entries from plugin `.mcp.json` files and 20 session connectors with their tool lists), 8 scheduled tasks and 3 hooks. If pompy is a different set, replace `sources/` and rerun.

## Stretch targets

| Target | Result |
|---|---|
| 100% of elements have all 7 facets filled and sourced | **Met.** 496/496 elements, 4,532 values, every value has at least one ref that resolves to an existing file and line. |
| …but how strong is the sourcing? | Mixed. 43% of values are *explicit* (a manifest field states it), 34% *inferred* (keyword or structure), 23% *default* (nothing contradicts it, anchored to the element's header line). `type` and `trigger` are strong. `model` is 99% default, `ui` is 75% default, `system` is almost entirely inferred (1 explicit value). |
| Filtering under 50 ms at 500 elements | **Met.** Median under the 0.1 ms timer granularity, p95 about 0.1 ms for the bitmask filter over 500 elements (headless Chromium, 200 runs). Filter plus recount plus heatmap redraw is about 2 ms. |
| Blind re-classification, Cohen's kappa ≥ 0.8 | **Not met.** Pooled kappa **0.799** (raw agreement 95.3%) on 63 stratified elements. Per facet: type 1.00, model 1.00, trigger 0.93, ui 0.83, harness 0.73, system 0.66, connection 0.54. Details below. |

### Blind re-classification

An independent annotator (a fresh subagent restricted to a packet containing only the vocabulary, a short guide and copies of the raw manifests) labelled 63 elements sampled by type. Kappa is computed over (element, value) binary decisions, pooled per facet. Files: `validation/blind_labels.json`, `blind_key.json`, `kappa.json` (with every disagreement).

What the disagreements say, and what I did not do:

* **system (0.66):** 41 values only the registry assigned versus 32 only the annotator. The registry over-assigns from keyword mentions in prose (for example `canva-creator` picks up crm, email and payments from lists of connectors it can be combined with). It also misses implicit systems (`sql-queries` says nothing about a database and the annotator reasonably chose data-warehouse).
* **connection (0.54):** the split is symmetric. The annotator reads "no tools declared" as `none`; the registry infers `mcp` from the mere word MCP or from a plugin that ships a `.mcp.json`. The two readings are both defensible, which means the vocabulary definition needs a sharper rule: *declared* channel (allowed-tools, tool names) versus *available* channel (plugin config).
* **harness (0.73):** all 42 disagreements are values only the registry assigned. The registry gives every skill the full target list of its plugin (`superpowers` lists seven runtimes). The annotator was more conservative. This is a definitional question (plugin packaging versus per-skill support), not a labelling error.
* **trigger (0.93), ui (0.83):** disagreements are mostly `user-command` on skills where the registry accepted a sibling command file or an `argument-hint`, and `ui: chat` versus `none` for plugins and servers.

I did **not** tune the classifier to this sample: doing so would make a second kappa on the same items meaningless. The next step is to fix the three rule families above, then draw a fresh sample for a second blind round. 63 items is small, so the pooled 0.799 carries a wide interval and should be read as "about 0.8", not as pass or fail.

## Adversarial test: are the facets independent?

Method: normalised mutual information (NMI) and Cramér's V on every facet pair with multi-valued elements weighted once, plus phi on every value pair and conditional probabilities for the two suspicions in the brief. The full 21-pair matrix is `analysis.json`; the page's "Facet independence" tab shows it, once for all elements and once for authored elements only.

**Verdict: the facets are not independent. One pair was redundant by definition, one was partly redundant, and `type` structurally determines several others.** Two were fixed; the rest are reported.

### Your two suspicions

1. *"type: plugin almost always means connection: MCP."* **Rejected.** 18 of 25 plugins (72%) declare MCP, against a base rate of 67% across all elements, a lift of 1.07. Only 5% of MCP-connected elements are plugins. The strong correlation is elsewhere: `type: mcp-server` implies `connection: mcp` in 100% of cases, which is true by construction (an MCP server's own transport is MCP). For servers, `connection` carries no information.
2. *"type: process is just trigger: time."* There is no `process` type in this vocabulary, but the nearest case holds exactly: `type: scheduled-task` and `trigger: time` are the same eight elements (phi 1.0, both directions). Likewise `trigger: event` is 75% hooks (3 of 4; the fourth is the plugin that ships the hook). These are structural: a scheduled task is a thing whose trigger is a schedule.

### What the data did break, and the redefinitions applied (v1 → v2)

| Finding | Evidence | Change |
|---|---|---|
| `ui: command-menu` and `trigger: user-command` were the same set | phi 1.0, 77 of 77 | **Removed `command-menu` from `ui`.** UI is now only the output surface; invocation belongs to `trigger`. NMI(trigger, ui) fell from 0.355 to 0.129. |
| `connection: http` and `native-tool` almost always co-occurred | Jaccard 0.85 (45 elements, all from the same `allowed-tools: Read, WebFetch` pattern) | **Merged** `http` into `native-tool` (harness built-in file and web tools). Four connection values remain. |
| `type` determines `trigger` | Cramér's V 0.76 across all elements; NMI 0.37 (0.28 on authored elements). commands are 100% user-command, agents 100% delegated, MCP servers 100% model-selected | **Kept both.** Packaging and activation are different questions, but report them together: filter on one before reading the other. |
| `model` is almost constant | 99% `inherit`; 0.11 bits of entropy; only 5 agents and one task pin a model (`fable` is never used) | **Kept** for completeness but it carries almost no discriminating power. Treat as a data-quality field. |
| `harness` is almost constant, and its values come in blocks | 99% claude-code; codex and cursor co-occur at Jaccard 0.89; claude-desktop and cowork at 0.78 | **Kept.** The blocks reflect plugin-level packaging. A per-element support claim would need runtime evidence the manifests do not give. |
| `system: none` and `connection: none` coincide | phi 0.56 | Expected: both mean "pure reasoning". Not merged. |
| `system: crm` and `email` overlap | Jaccard 0.50 (58 elements, mostly the sales plugin) | Real workflow overlap, not a vocabulary defect. Not merged. |

Residual dependence after the redefinitions (NMI, all elements): `model × type` 0.85, `ui × type` 0.63, `trigger × model` 0.45, `trigger × type` 0.37, `system × connection` 0.33. Everything above 0.3 involves `type` or the near-constant `model`. Among authored elements only (skills, commands, agents, plugins) `ui × type` is still 0.66, because most skills default to `chat`; that is a measurement weakness in the `ui` rule (default-anchored), not independent signal.

### MECE check per vocabulary

* **Exclusive:** after the two fixes no value pair inside a facet overlaps above Jaccard 0.5 except the harness blocks and `crm/email` noted above.
* **Exhaustive:** no "other" exists. Fallbacks are `none` (system, connection, ui) and `inherit` (model). `system: none` is assigned to 66 elements (13%) and `connection: none` to 100 (20%); these are the vocabulary's escape hatches and the first place to look for missing values. The 25 system values are broad; `database` has only 4 elements and `monitoring-incident` 7. `model: fable` is unused.
* **Structural note on multi-valued facets:** mean values per element is 2.1 for `system` and 1.6 for `harness`; every other facet is 1.0 to 1.1. Multi-valued `system` makes the heatmap row totals exceed 496.

## Gaps (empty cells with an expected count of at least 8 under independence)

Most empty cells are structural zeros (a hook is never a skill). The gaps worth a look are those where independence predicts a populated cell:

* **`trigger: user-command` × `system: salesforce-platform` (expected 13.7, observed 0).** The 27 ISV/OEM Advisor skills declare no `argument-hint` or `user-invocable`, so no manifest says a person can start them directly, even though the harness allows it. A manifest convention gap, not a capability gap.
* **`system: project-tracker` × `connection: none` (11.5).** Anything that touches a tracker declares a channel. Good hygiene.
* **`connection: mcp` × harnesses muse, kimi, devin, antigravity (11.4 each).** Those four harness manifests ship only from `superpowers`, which uses no MCP. No evidence either way for the 70 MCP-using plugins on those runtimes.
* **`ui: rendered-artifact` and `system: email/crm` × `harness: codex/cursor` (10 to 12 each).** The artifact-producing and CRM-connected plugins have no Codex or Cursor manifest.
* **Unattended triggers:** no skill, command or agent carries a `time` or `event` trigger. Only 12 elements are unattended (8 scheduled tasks, 3 hooks, 1 plugin that ships a hook).

## Duplicates and crowded cells

* **Crowding:** the cell `trigger: model-selected × type: skill` holds 304 elements, 147 of which share an identical seven-facet signature with at least one other element. Largest identical-signature groups: 23 sales skills, 22 prose-only skills with no system or channel, 20 ISV/OEM Advisor skills. There are 284 distinct signatures over 496 elements, so seven facets separate elements only about as finely as plugin membership does.
* **Cross-plugin candidates (same or near name, 5 to 7 of 7 facets equal):**
  * `frontend-design` exists as an org skill and as the `frontend-design` plugin skill (all 7 facets identical), and `design-superpowers:design` and `engineering:system-design` sit one facet away.
  * `competitive-brief` in `marketing` and `product-management` (6 of 7 identical); `sales:competitive-intelligence` is a third relative.
  * `account-research` and `call-prep` in `common-room` versus `sales` (5 of 7).
  * `lead-triage` in `sales` versus `small-business`; `social-content` (org) versus `small-business:social-content-engine`.
  * `productivity:update` against `product-management:roadmap-update` and `stakeholder-update`.
  * `brand-voice` ships `discover-brand` as both a skill and a command; they differ only by `type`, which is by design.
* **Servers listed twice:** seven services appear both as a plugin-declared server and a session connector (GitHub, Gmail, Google Calendar, Google Drive, Microsoft 365, Microsoft Learn, Salesforce). They keep separate ids so the origin stays visible; treat them as one capability when counting.

## Risk overlay: unattended and write access

Definition: a `time` or `event` trigger **and** write access to a system of action. Access is recorded per system with its evidence line: tool-name verbs for connectors, contract mode for the kit skills, grant plus tool list for scheduled tasks, a verb on the line that mentions the system otherwise.

**7 of the 12 unattended elements are flagged, all as write:**

* 6 PR re-check tasks (source-control): their prompts say "merge master into neon-tls". All six are disabled or already fired, so the live exposure is zero today. Their manifests declare **no connector**, so the write capability comes from whichever session they are bound to. That is a gap in the manifest, not a safe default.
* `Briefing` (enabled, weekdays 14:30 Warsaw): its prompt is read-only (summarise mail and calendar), but its Gmail connector grant is unrestricted (`permitted_tools: []`) and Gmail exposes `send_message`, `reply`, `forward` and `trash_*`. Flagged as capability versus intent. Restricting the grant to read tools would clear it. Its last run failed with a usage limit.
* The `stop-hook-git-check.sh` hook is **not** flagged. An earlier rule matched a git verb inside a comment and then inside an `echo` message; the hook only inspects git state and tells the model what to do. This is a worked example of how keyword evidence produces false risk.

Not flagged, but relevant: 40 skills that can write to a system also mention scheduled or unattended use in their text (for example the `sales` skills: "Scheduled or unattended runs take the actions the user set"). Their manifests declare a user or model trigger, so the strict definition cannot see them; `analysis.json` lists them as `latent_unattended`. If scheduling is how these get used, the trigger facet understates the real exposure.

## Limits to keep in mind

* Source refs prove where a value came from, not that it is right. 23% of values are defaults and 34% inferred.
* "Access" for plugin-declared MCP servers is `unknown` because `.mcp.json` lists no tools; the risk overlay therefore cannot flag them (amber state exists but nothing currently triggers it).
* The session tool registry and the scheduled-task list are snapshots checked in by hand (`sources/session/`); the rest is copied by `scripts/snapshot_sources.py`.
* Kappa was measured on 63 items with one annotator (a model), not two humans.
