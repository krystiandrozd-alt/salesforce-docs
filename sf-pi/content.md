# SF Pi — Content

Synthesis written independently from the source (not copied text). Retrieved 2026-11-21 at version 0.365.4. **Inference** marks my own reading, not the source's.

## What it is

SF Pi is an open-source bundle of Salesforce extensions for Pi, a third-party terminal coding agent created by Mario Zechner ([README]). Salesforce publishes it under the Apache-2.0 licence ([licence]). It adds:

- Salesforce lifecycle tools;
- org-aware status and safety surfaces;
- Agent Script authoring;
- one Manager (`/sf-pi`) for settings and for turning extensions on and off.

Pi remains the agent runtime. The project's non-goals rule out becoming an IDE or adding a second plugin API on top of Pi's ([roadmap]).

How it fits with other Salesforce AI tooling:

- [Agentforce Labs](../agentforce-labs/content.md) lists SF Pi among its experiments. Labs can run it in a disposable remote workspace with the chosen org injected ([labs-page]).
- The SF Skills extension manages skills from several sources (Claude, Codex, Cursor, custom and managed). The quick start installs the default skills with `/sf-skills defaults install global` ([README]).
- **Inference:** SF Pi runs only inside Pi. Teams standardised on Claude Code, Cursor or Codex get the Agentforce lifecycle skills from the Salesforce Skills Library or the Agentforce ADLC plugin instead (see [Agentforce Labs § 1](../agentforce-labs/content.md#1-build-choosing-a-tool)).

## Getting it running

| Route | What you need | Notes (per source) |
|---|---|---|
| Local install | Node.js 22.19 or newer; Pi in the supported range (`>=1.5.1 <2.0.0`, with 1.6.0 the audited, recommended version); Salesforce CLI | The install guide recommends Pi's managed installer, which pins dependencies. npm is supported but doesn't pin Pi's transitive dependencies. Then run `pi install git:github.com/salesforce/sf-pi`, and inside Pi `/reload` and `/sf-pi doctor` ([install]) |
| Agentforce Labs | A Labs sign-in with the experiment enabled | Disposable remote workspace; Labs injects the selected org; a cold start takes about one to two minutes ([labs-page]) |

## What it adds

There are 27 extensions, grouped below by the catalog's own intent groups. The full list, with commands and maturity, is in [index.md](index.md). 13 are marked stable and 14 experimental.

| Intent group | Extensions | What they do (per the catalog) |
|---|---|---|
| Build agents | SF Agent Script, SF Code Analyzer, SF Docs, SF Fin, SF LSP | **Agent Script lifecycle:** compile diagnostics, quality checks, preview, local evaluation, publication of an inactive version, then activation gated on evaluation. **Code Analyzer:** scans, including ApexGuru. **SF Docs:** cited Salesforce documentation lookup. **SF Fin:** a connector to a Fin workspace (the catalog says Fin was formerly Intercom). **SF LSP:** live diagnostics as files are written |
| Build apps | SF Apex, SF Flow, SF LWC, SF tldraw | **Apex** through the API: diagnostics, logs, anonymous Apex, targeted tests. **Flow** authoring, including Omni-Channel routing flows, with check-only validation. **LWC:** local inspection and Jest tests. **tldraw:** editable Salesforce diagrams |
| Query data | SF SOQL | Schema-grounded SOQL with automatic REST/Tooling selection, guarded execution and query plans |
| Work with Salesforce orgs | SF Browser, SF Data Explorer, SF DevBar, SF Integrate | **Browser:** automation for last-mile UI work. **Data Explorer:** read-only SOQL, SOSL and Data 360 SQL explorer. **DevBar:** status bar with org context. **Integrate:** integration setup (hosted MCP activation, External Client App OAuth, outbound credentials) with guarded apply |
| Work with Data Cloud | SF Data 360 | One tool for connect, prepare, harmonise, segment, activate, query, semantic, observe and orchestrate actions |
| Work safely | SF Guardrail, SF Brain, SF Herdr, SF Plannotator | **Guardrail:** see below. **Brain:** an engineering "constitution" and response diagnostics. **Herdr:** read-only workflow plans. **Plannotator:** review of agent replies and local text files |
| Collaborate and improve | SF Slack, SF Feedback | **Slack:** search and thread reading; the README says write actions need human confirmation. **Feedback:** sanitised bug reports filed as GitHub issues |
| Personalize Pi | SF Pi Manager, SF Skills, SF MCP, SF LLM Gateway, SF Welcome, SF Ohana Spinner | **Manager** (`/sf-pi`): the only always-on extension. **Skills:** one funnel for skills from all sources. **MCP:** org-bound MCP presets. **LLM Gateway:** an optional model provider. **Welcome / Ohana Spinner:** splash screen and spinner |

## Safety and privacy model

All points below are from the security model ([security-model]) unless marked otherwise.

- **SF Guardrail** mediates the risky operations that SF Pi can recognise: file-protection policies, gating of dangerous commands, org-aware confirmation, and mediation of high-value changes made through native tools.
- **No silent approvals.** Actions that need confirmation fail closed when there is no interactive UI, unless an operator explicitly enables unattended execution. Operator modes are set outside the model and are audited.
- **Prompt injection** is treated as an action-integrity risk. The goal: untrusted content alone must never be enough to trigger a high-value change, broad data disclosure or an external write.
- **Stated limits:** SF Pi doesn't sandbox arbitrary shell commands or third-party tools, doesn't replace target-system authorisation, and doesn't remove the need for user review and least-privilege credentials.
- **No telemetry:** no active runtime telemetry. SF Pi also turns off Pi's anonymous install/update ping unless the user has already made a choice ([README], [privacy]).
- **Credentials:** SF Docs, SF Slack and SF LLM Gateway need separately provided credentials. SF LLM Gateway ships with no endpoint configured ([README], [llm-gateway]).

## Review notes — verify before reuse

1. **The install command differs between sources.**
   - The README quick start uses plain `npm install --global`.
   - The Labs page uses npm with `--ignore-scripts` and calls that the official command.
   - The install guide recommends Pi's managed installer (`curl … | sh`), which pins dependencies.

   Sources: [README], [labs-page], [install]. **Recommendation:** follow the install guide. Where a client blocks `curl | sh`, use npm with `--ignore-scripts`.
2. **A small project with one maintainer.** The governance file describes a small project maintained in spare time, with a single maintainer for all areas ([governance]). Security reports go through Salesforce's vulnerability process ([security]). **Inference:** there is no product support commitment; plan for that before a client depends on it.
3. **The release cadence is very fast.** There were 703 releases between v0.1.0 (22 April 2026) and v0.365.4 (21 November 2026), six of them on 21 November alone ([changelog]). **Recommendation:** pin a version for demos and run `/sf-pi doctor` after each update.
4. **All 27 extensions are enabled by default, including the 14 experimental ones** ([index.md](index.md)). **Recommendation:** before pointing SF Pi at a client org, turn off what you don't need, especially extensions that can change org state.
5. **Some pieces are third-party.** Pi itself and the nine recommended companion packages are community projects; the companions are MIT-licensed and install only on explicit request ([recommendations]). The project also states that it doesn't present community-built extensions as official Salesforce product features ([roadmap]). **Recommendation:** vet these like any open-source dependency, and don't position SF Pi capabilities to clients as Salesforce product features.
6. **Hosted MCP activation is described two ways.** SF Integrate says it activates hosted MCP servers through a Tooling object, `McpServerAccess`, when the org exposes it, and falls back to browser automation otherwise ([integrate]). Salesforce's public guide describes activation in Setup only ([Activate MCP Servers][sf-activate]). I couldn't find `McpServerAccess` in public documentation. See also [LabBox note 12](../agentforce-labs/org-configuration.md#review-notes--verify-before-reuse).
7. **No dedicated Industries or OmniStudio extension.** SF Skills recognises an OmniStudio skill group (skills prefixed `omnistudio-`), but none of the 27 extensions targets Industries or OmniStudio. **Inference:** OmniStudio and EPC work still runs through skills and standard tooling.

Section breakdown:
- **Build agents** — 5 extensions
- **Build apps** — 4 extensions
- **Work safely** — 4 extensions
- **Work with Salesforce orgs** — 4 extensions
- **Work with Data Cloud** — 1 extension
- **Collaborate and improve** — 2 extensions
- **Personalize pi** — 6 extensions
- **Query data** — 1 extension

*Sources: the [salesforce/sf-pi repository][repo] at commit `034f47f` and its [documentation site][site], retrieved 2026-11-21.*

## Extraction notes

- [index.md](index.md) is generated from the repository's catalog files by `scripts/refresh_sf_pi.py` (run it against a local clone). The script also updates the section breakdown above and leaves the prose alone.
- Read for this synthesis: README, roadmap, governance, security policy, install guide, security model, the catalog, and the READMEs of SF Docs, SF LLM Gateway and SF Integrate. The other extension READMEs, the 157 architecture decision records and the changelog contents were not reviewed; the changelog was used only for release counts and dates.
- This folder is outside `developer.salesforce.com`, so `scripts/refresh_from_llms.py` skips it (`EXTRA_SOURCES`).

[repo]: https://github.com/salesforce/sf-pi
[site]: https://opensource.salesforce.com/sf-pi/
[README]: https://github.com/salesforce/sf-pi/blob/main/README.md
[licence]: https://github.com/salesforce/sf-pi/blob/main/LICENSE.txt
[roadmap]: https://github.com/salesforce/sf-pi/blob/main/ROADMAP.md
[governance]: https://github.com/salesforce/sf-pi/blob/main/GOVERNANCE.md
[security]: https://github.com/salesforce/sf-pi/blob/main/SECURITY.md
[changelog]: https://github.com/salesforce/sf-pi/blob/main/CHANGELOG.md
[recommendations]: https://github.com/salesforce/sf-pi/blob/main/catalog/recommendations.json
[install]: https://opensource.salesforce.com/sf-pi/install
[privacy]: https://opensource.salesforce.com/sf-pi/privacy
[security-model]: https://opensource.salesforce.com/sf-pi/security-model
[llm-gateway]: https://opensource.salesforce.com/sf-pi/extensions/sf-llm-gateway
[integrate]: https://opensource.salesforce.com/sf-pi/extensions/sf-integrate
[labs-page]: https://labs.agentforce.com/docs/sf-pi
[sf-activate]: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/activate-mcp-servers.html
