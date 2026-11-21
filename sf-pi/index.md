# SF Pi -- Index

Source: [salesforce/sf-pi](https://github.com/salesforce/sf-pi) (Apache-2.0) and its documentation site [opensource.salesforce.com/sf-pi](https://opensource.salesforce.com/sf-pi/). This folder is outside `developer.salesforce.com`, so `scripts/refresh_from_llms.py` skips it.

Extracted programmatically from the repository's generated catalog files at version 0.365.4 (commit `034f47f`): 27 extensions (stable 13, experimental 14; 27 enabled by default), 9 optional companion packages, 13 top-level docs pages. Last refreshed 2026-11-21 by `scripts/refresh_sf_pi.py`.

## Documentation pages (13)

| Page | URL | Source file |
|---|---|---|
| sf-pi Agent Orientation | https://opensource.salesforce.com/sf-pi/agent-orientation | `docs/agent-orientation.md` |
| sf-pi Command Reference | https://opensource.salesforce.com/sf-pi/commands | `docs/commands.md` |
| Contributing | https://opensource.salesforce.com/sf-pi/contributing | `docs/contributing.md` |
| Browse SF Pi extensions | https://opensource.salesforce.com/sf-pi/extensions | `docs/extensions.md` |
| Welcome to SF Pi | https://opensource.salesforce.com/sf-pi/ | `docs/index.md` |
| Install SF Pi | https://opensource.salesforce.com/sf-pi/install | `docs/install.md` |
| Privacy & telemetry | https://opensource.salesforce.com/sf-pi/privacy | `docs/privacy.md` |
| Public sanitization | https://opensource.salesforce.com/sf-pi/public-sanitization | `docs/public-sanitization.md` |
| SF Pi Quickstart | https://opensource.salesforce.com/sf-pi/quickstart | `docs/quickstart.md` |
| Secure development | https://opensource.salesforce.com/sf-pi/secure-development | `docs/secure-development.md` |
| Security model | https://opensource.salesforce.com/sf-pi/security-model | `docs/security-model.md` |
| Bundled Extension Settings Surfaces | https://opensource.salesforce.com/sf-pi/settings-surfaces | `docs/settings-surfaces.md` |
| Troubleshooting | https://opensource.salesforce.com/sf-pi/troubleshooting | `docs/troubleshooting.md` |

Architecture decision records: 157 files in [`docs/adr`](https://github.com/salesforce/sf-pi/tree/main/docs/adr) (in the repository only; the docs site excludes them).

## Extensions: Build agents (5)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF Agent Script](https://opensource.salesforce.com/sf-pi/extensions/sf-agentscript) | `sf-agentscript` | agent-tool | stable | `/sf-agentscript` | 4 | Single-plugin lifecycle for `.agent` files: compile diagnostics, native quality, preview, local-first Eval Studio, exact-version release eval, inactive publication, and gated activation. |
| [SF Code Analyzer](https://opensource.salesforce.com/sf-pi/extensions/sf-code-analyzer) | `sf-code-analyzer` | agent-tool | experimental | `/sf-code-analyzer` | 1 | Salesforce Code Analyzer workflows for pi: setup readiness, explicit scans, rule discovery, config generation, report artifacts, deferred agent quality passes, and ApexGuru analysis. |
| [SF Docs](https://opensource.salesforce.com/sf-pi/extensions/sf-docs) | `sf-docs` | agent-tool | experimental | `/sf-docs` | 1 | Salesforce documentation lookup for agents and humans, with Pi-native bearer authentication, cited results, and a Manager settings surface. |
| [SF Fin](https://opensource.salesforce.com/sf-pi/extensions/sf-fin) | `sf-fin` | agent-tool | experimental | `/sf-fin` | 1 | Connect SF Pi to a Fin (formerly Intercom) workspace: Pi-owned masked credentials, Guardrail-mediated Fin CLI install, doctor and debug, Fin-as-code authoring (procedures, simulations, guidance, data connectors), a CLI vs MCP surface comparison, and a Fin Agent API test harness, and end-to-end Fin for Salesforce setup (package install, audit-field setting, Digital Experiences, permission set, dedicated Fin user, and Fin's Connect flow) in an explicit org. |
| [SF LSP](https://opensource.salesforce.com/sf-pi/extensions/sf-lsp) | `sf-lsp` | assistive | stable | `/sf-lsp` | 0 | Real-time Salesforce LSP diagnostics on write/edit with a working indicator, transcript rows, and one-line startup readiness in SF Welcome |

## Extensions: Build apps (4)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF Apex](https://opensource.salesforce.com/sf-pi/extensions/sf-apex) | `sf-apex` | agent-tool | experimental | `/sf-apex` | 1 | API-native Apex lifecycle workflows for pi: authoring guidance, diagnostics, trace/log/watch, Anonymous Apex, and targeted tests. |
| [SF Flow](https://opensource.salesforce.com/sf-pi/extensions/sf-flow) | `sf-flow` | agent-tool | experimental | `/sf-flow` | 1 | Lean Salesforce Flow lifecycle workflows for pi: core-five plus queue, direct-agent, skills, availability, and no-route Omni-Channel authoring; org grounding; preventive quality; bounded repair; Mermaid topology; check-only validation; guarded lifecycle; and targeted Flow tests. |
| [SF LWC](https://opensource.salesforce.com/sf-pi/extensions/sf-lwc) | `sf-lwc` | agent-tool | experimental | `/sf-lwc` | 1 | Local-native Lightning Web Component lifecycle workflows for pi: project scan, component inspection, focused diagnostics, targeted Jest tests, and artifacts. |
| [SF tldraw](https://opensource.salesforce.com/sf-pi/extensions/sf-tldraw) | `sf-tldraw` | agent-tool | experimental | `/sf-tldraw` | 1 | Deterministic, editable Salesforce diagrams rendered through the local tldraw offline Canvas API. |

## Extensions: Work safely (4)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF Brain](https://opensource.salesforce.com/sf-pi/extensions/sf-brain) | `sf-brain` | assistive | stable | — | 0 | Salesforce Engineering Constitution, compact SF Pi routing summary, and advisory display, instruction, and visual-response diagnostics |
| [SF Guardrail](https://opensource.salesforce.com/sf-pi/extensions/sf-guardrail) | `sf-guardrail` | safety | stable | `/sf-guardrail` | 0 | Salesforce-aware safety hooks — file protection policies, dangerous-command gating, org-aware confirmation, and native high-value mutation mediation |
| [SF Herdr](https://opensource.salesforce.com/sf-pi/extensions/sf-herdr) | `sf-herdr` | agent-tool | experimental | `/sf-herdr` | 1 | Non-mutating Salesforce workflow plans for the current split Herdr tools. |
| [SF Plannotator](https://opensource.salesforce.com/sf-pi/extensions/sf-planreview) | `sf-planreview` | ui | experimental | `/sf-planreview` | 0 | TUI-first review of Pi replies and local text artifacts through Herdr Annotate or Plannotator TUI |

## Extensions: Work with Salesforce orgs (4)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF Browser](https://opensource.salesforce.com/sf-pi/extensions/sf-browser) | `sf-browser` | agent-tool | experimental | `/sf-browser` | 13 | Salesforce-aware browser automation for last-mile UI work using agent-browser. |
| [SF Data Explorer](https://opensource.salesforce.com/sf-pi/extensions/sf-data-explorer) | `sf-data-explorer` | ui | experimental | `/sf-data-explorer` | 0 | Read-only interactive TUI explorer for SOQL, SOSL, and Data 360 SQL using sf-pi Salesforce transport plumbing. |
| [SF DevBar](https://opensource.salesforce.com/sf-pi/extensions/sf-devbar) | `sf-devbar` | ui | stable | `/sf-devbar`, `/sf-org` | 0 | Bespoke Salesforce developer status bar with org context, model info, git, and context window progress |
| [SF Integrate](https://opensource.salesforce.com/sf-pi/extensions/sf-integrate) | `sf-integrate` | agent-tool | experimental | `/sf-integrate` | 1 | Plan-bound Salesforce integration setup with hosted MCP activation and org-bound handoff, External Client App OAuth, outbound modern credentials, guarded apply, and resulting-state proof. |

## Extensions: Work with Data Cloud (1)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF Data 360](https://opensource.salesforce.com/sf-pi/extensions/sf-data360) | `sf-data360` | agent-tool | stable | `/sf-data360` | 1 | One Pi-native Data 360 SDK tool with discover, connect, prepare, harmonize, segment, activate, query, semantic, observe, orchestrate, and API actions |

## Extensions: Collaborate and improve (2)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF Feedback](https://opensource.salesforce.com/sf-pi/extensions/sf-feedback) | `sf-feedback` | assistive | stable | `/sf-feedback` | 0 | Guided feedback and bug-report flow that collects sanitized SF Pi diagnostics and opens a GitHub issue |
| [SF Slack](https://opensource.salesforce.com/sf-pi/extensions/sf-slack) | `sf-slack` | agent-tool | stable | `/sf-slack` | 10 | Slack integration — search messages, read threads, browse channel history |

## Extensions: Personalize pi (6)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF LLM Gateway](https://opensource.salesforce.com/sf-pi/extensions/sf-llm-gateway) | `sf-llm-gateway` | provider | stable | `/sf-llm-gateway` | 0 | Salesforce LLM Gateway provider with model discovery |
| [SF MCP](https://opensource.salesforce.com/sf-pi/extensions/sf-mcp) | `sf-mcp` | agent-tool | experimental | `/sf-mcp` | 1 | Conflict-aware Salesforce MCP preset catalog and org-bound connection-instance configuration for Pi's native MCP runtime |
| [SF Ohana Spinner](https://opensource.salesforce.com/sf-pi/extensions/sf-ohana-spinner) | `sf-ohana-spinner` | ui | stable | — | 0 | Short Salesforce waiting messages in Pi's working indicator |
| [SF Pi Manager](https://opensource.salesforce.com/sf-pi/extensions/sf-pi-manager) | `sf-pi-manager` | manager | stable | `/sf-pi` | 0 | Core manager — provides /sf-pi commands |
| [SF Skills](https://opensource.salesforce.com/sf-pi/extensions/sf-skills) | `sf-skills` | ui | stable | `/sf-skills` | 0 | Manage skills through one Skill Funnel: catalog every source (Claude/Codex/Cursor/custom/managed) → gate sources → toggle skills per scope (global/project) → resolve name conflicts, all compiled to native settings.skills[]. Toggle managed-library invocation via disable-model-invocation stamps on an effective tree. Plus a passive live-context HUD, forcedotcom/sf-skills install, per-skill usage counters, and prune. Pi's built-in MCP extension owns MCP configuration and readiness. |
| [SF Welcome](https://opensource.salesforce.com/sf-pi/extensions/sf-welcome) | `sf-welcome` | ui | stable | `/sf-welcome`, `/sf-setup-fonts` | 0 | Salesforce-branded splash screen with environment status, SF Pi release freshness, and community info |

## Extensions: Query data (1)

| Extension | ID | Category | Maturity | Commands | Tools | Description |
|---|---|---|---|---|---|---|
| [SF SOQL](https://opensource.salesforce.com/sf-pi/extensions/sf-soql) | `sf-soql` | agent-tool | experimental | `/sf-soql` | 1 | API-native, schema-grounded SOQL lifecycle workflows for pi with automatic REST/Tooling resolution, guarded execution, query plans, bounded results, and artifacts. |

## Optional companion packages (9)

Third-party Pi packages that SF Pi recommends. They are installed only on explicit request (`/sf-pi recommended`).

| Package | Source | License | Description |
|---|---|---|---|
| [pi-skills](https://github.com/badlogic/pi-skills) | `git:github.com/badlogic/pi-skills` | MIT | Curated skill collection for pi (brave-search, gmcli, gdcli, youtube-transcript, browser-tools, vscode, transcribe, and more). |
| [pi-web-access](https://github.com/nicobailon/pi-web-access) | `npm:pi-web-access` | MIT | Web search, URL fetching, GitHub repo cloning, PDF extraction, YouTube, and local video analysis. |
| [pi-fff / FFF Search](https://github.com/dmtrKovalenko/fff/tree/main/packages/pi-fff) | `npm:@ff-labs/pi-fff` | MIT | FFF-powered fuzzy file and content search for pi, with frecency ranking, Git-aware results, and a local background index. |
| [pi-aliases](https://github.com/xRyul/pi-aliases) | `npm:pi-aliases` | MIT | Command aliases for pi: /clear → /new, /exit → /quit, and related muscle-memory helpers. |
| [pi-interview](https://github.com/nicobailon/pi-interview-tool) | `npm:pi-interview` | MIT | Interactive interview form extension for pi — provides the `interview` tool. |
| [glimpseui](https://github.com/hazat/glimpse) | `npm:glimpseui` | MIT | Native micro-UI for scripts and agents — cross-platform WebView windows with bidirectional JSON. |
| [pi-tool-display](https://github.com/MasuRii/pi-tool-display) | `npm:pi-tool-display` | MIT | Compact tool-call rendering, diff visualization, and output truncation for cleaner TUI sessions. |
| [pi-subagents](https://github.com/nicobailon/pi-subagents) | `npm:pi-subagents` | MIT | Delegate work to builtin or custom subagents with single, chain, parallel, async, and forked-context execution. |
| [pi-herdr / Herdr](https://github.com/ogulcancelik/pi-extensions) | `npm:@ogulcancelik/pi-herdr` | MIT | Alpha Herdr-native workspace, tab, and pane orchestration for pi with command output watches and agent status waits. |
