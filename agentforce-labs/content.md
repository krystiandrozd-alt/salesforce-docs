# Agentforce Labs — Content

Synthesis written independently from the source pages (not copied text). Retrieved 2026-11-21. **Inference** marks my own reading, not the source's.

## What the site is

Agentforce Labs (`labs.agentforce.com`) is a Salesforce site for experimental Agentforce tools, open-source projects and early capabilities ([home]). The homepage is explicit about what to expect:

- pre-GA, for testing only;
- fast-changing, with no SLAs;
- bugs and breaking changes are to be expected;
- direction is shaped by user feedback.

Its stated purpose is building, testing and deploying Agentforce agents from your IDE or coding agent.

The site is written for AI coding agents as much as for people:

- **`llms.txt` is a set of instructions, not a page list.** It tells a coding agent to use the Salesforce CLI in an existing SFDX project, install the `agentforce-generate` and `agentforce-test` skills, build with Agent Script, test locally first, and change an org only when asked to ([llms]).
- **Agents can get an org on their own.** The homepage says agents and CLIs can self-provision an org through device authorization (RFC 8628): a person approves at `/device`, and the agent receives an SFDX auth URL ([home]). Labs picks the user's active LabBox, otherwise their connected own org, otherwise it provisions a new LabBox ([llms]). What a LabBox contains is covered in [org-configuration.md](org-configuration.md).
- **A JSON capability manifest lists every page, tool and experiment** ([manifest]). [index.md](index.md) is generated from it.

## 1. Build: choosing a tool

- **In the browser, with no local setup:**
  - Agentforce Builder is the visual route: describe the agent, configure subagents and actions, preview it, deploy it ([builder]).
  - Agentforce Vibes is AI-assisted Agent Script inside Code Builder ([vibes]).
  - Overview of all routes: [build].
- **Coding agents:** there is one guide each for Claude Code, Codex and Gemini CLI, and for the Cursor, Windsurf and Antigravity editors. All follow the same four steps: install the tool, connect Salesforce through the CLI, add the Agentforce skills or plugin, build an agent. Each assumes an org with Agentforce enabled and points to a LabBox if you don't have one ([claude-code] and the sibling pages in [index.md](index.md)).
- **Skills** ([skills]):
  - Claude Code: the Agentforce ADLC plugin (skills to generate, test and observe agents) and the Salesforce Development plugin (Apex, Flow, metadata). The page says both are in Anthropic's official plugin marketplace.
  - Other coding tools: the Salesforce Skills Library (`forcedotcom/sf-skills`), which includes the same Agentforce skills.
  - ChatGPT: Salesforce's Agentforce Sales app (Beta).
- **SF Pi:** Salesforce's open-source extension bundle for the Pi coding agent. You can run it in Labs or install it locally ([sf-pi]).

## 2. Agent Script and Agent API

**Agent Script** ([agent-script]):

- One file defines the whole agent: subagents, actions, transitions and guardrails.
- Two kinds of instruction keep the split explicit. Logic lines run deterministically before the LLM sees anything; prompt lines go to the LLM.
- Variables can be filled from the conversation.
- Each subagent has its own instructions, actions and an `after_reasoning` block.
- Actions can target Apex, Flows and External Services.
- Build, publish and test with the Salesforce CLI (the page shows `sf agent publish authoring-bundle` and `sf agent test run`) or from Claude Code.
- The page lists roadmap items, which are forward-looking: MCP integration, richer control flow and variable types, and agents that call other agents.

**Agent API** ([agent-api]):

- REST, under `https://api.salesforce.com/einstein/ai-agent/v1`.
- Sequence: get an OAuth access token → start a session (external session key, instance endpoint, optional variables) → send messages, either synchronously or streamed as Server-Sent Events → end the session.
- Stated limits: 1,000 sessions per hour per org, 100 messages per session, 50 concurrent sessions per org. The page links Salesforce's own rate-limits page; confirm the figures there before quoting them.
- Includes Node.js and Python examples.

## 3. Deploy: channels

The [Deploy][deploy] hub covers three routes: the Agent API for custom clients, web chat, and messaging apps. Each channel guide follows the same outline:

1. check the prerequisites;
2. enable Messaging and Omni-Channel;
3. set up the external platform;
4. create the channel;
5. route it to the Agentforce Service Agent;
6. test, usually with SOQL checks on `MessagingSession`;
7. confirm against a definition of done.

Like the LabBox page, each step has CLI, REST and click-path variants.

| Channel | External prerequisite (per guide) | Guide's estimate | Notable points (per guide) |
|---|---|---|---|
| [Experience Site][site-guide] | — | 45 min | Enhanced Chat widget on an Experience Cloud site; a fallback queue is required even with direct agent routing |
| [Enhanced Chat][chat-guide] (external website) | — | 30 min | No Experience Cloud needed. Covers Enhanced Chat v1 only ([note 2](#cross-page-notes--verify-before-reuse)) |
| [WhatsApp][whatsapp] | Meta Business Manager; a phone number not already registered with WhatsApp (it is migrated) | 30 min | Uses the Meta Cloud API |
| [SMS][sms] | None: Salesforce provisions the number | 30 min | Long code, toll-free (US/Canada) or short code. Short codes need weeks of carrier approval |
| [Messenger][messenger] | Facebook Page with admin rights, Meta Business Manager, Digital Engagement licence | 30 min | 2,000 characters per message, 25 MB attachments, 24-hour reply window |
| [Apple Messages for Business][apple] | Apple Business Register approval, which takes days to weeks | 30 min, plus the approval wait | Conversations start from Apple Maps, Safari and Spotlight; list and time pickers, Apple Pay, authentication |
| [LINE][line] | LINE Official Account with the Messaging API | 30 min | No reply window; the user must add the account as a friend; main markets Japan, Taiwan, Thailand, Indonesia |
| [Custom channel (BYOC)][byoc] | The messaging provider's managed package (e.g. Twilio, Vonage, MessageBird), built on the Interaction Service API | 45 min | Most effort; the provider implements message ingestion and delivery |

## 4. MCP and documentation tools

- **Platform MCP** ([platform-mcp]): connect any MCP client (Claude, ChatGPT, Cursor, Postman or your own) to the org's Salesforce-hosted MCP servers through one External Client App. Scopes and PKCE are the same for every client; only the OAuth callback URL differs. For server-level detail, see [org-configuration.md § MCP servers](org-configuration.md#7-mcp-servers).
- **Docs MCP** ([docs-mcp]): search and fetch Salesforce documentation from the IDE (`salesforce_docs_search`, `salesforce_docs_fetch`), optionally scoped to one documentation collection. See [note 3](#cross-page-notes--verify-before-reuse).
- **Agentforce Grid MCP** ([grid]): the `@salesforce/sf-grid-mcp` server exposes the Grid Connect API. An MCP client can then build Grid workbooks and run agent tests and evaluations. It runs through `npx`.

## 5. Labs experiments

| Experiment | What it does (per its page) | Form |
|---|---|---|
| Agentforce Chat | Build, troubleshoot and optimise agents against your org | Browser app |
| Agents | Lightweight agent editor | Browser app |
| Simulate | Simulated conversations to test an agent before release | Browser app |
| Agentforce Spark | Explore use cases and produce an agent blueprint | Browser app |
| Agentforce Voice | Live voice-agent demos in the browser | Browser app |
| Voice Quality | Scores a voice-agent call recording | Browser app |
| [Upgrade Agent][upgrade] | Converts an Einstein Bot into an Agentforce Service Agent. Groups of dialogs become subagents and action steps become actions; the bot stays live during cut-over | Browser app and guide |
| [Koa Decisions][koa] | Answers a plain-English question about a text with probabilities, not generated text. Three question types: true/false, pick one, score. Three API formats (Decisions, Chat Completions-compatible, System One); callable from Apex. See [note 4](#cross-page-notes--verify-before-reuse) | Playground and API |
| [nanoRag][nanorag] | Salesforce CLI plugin that builds BM25 keyword-search libraries, stored in the org as `ContentDocument` and `StaticResource` records. No embeddings, vector database or Data Cloud | CLI plugin |
| [AgentLens Visualizer][agentlens] | Open-source VS Code extension that turns agent traces into graphs and step-by-step inspectors | VS Code extension |
| [Agentforce for Google Workspace][gws] | Google Slides add-on: ask your agent a question, insert the answer as text or a table | Add-on |

The site also links three Salesforce AI Research projects hosted elsewhere ([experiments]):

- **GUI Process Automation:** learns a task from one demonstration.
- **MCP+:** filters MCP tool output to cut inference cost.
- **SkillOrchestra:** routes tasks to agents by competence and cost.

## Cross-page notes — verify before reuse

1. **Experimental by design.** The homepage disclaims SLAs and warns of breaking changes ([home]). **Recommendation:** treat Labs tools as prototypes and demo aids. For client delivery, use the GA product equivalent or confirm its status first.
2. **Enhanced Chat v2 is described two ways.** The Enhanced Chat guide says v2 needs custom Lightning Web Components ([chat-guide]). The LabBox page switches its deployment to V2 with a Setup button ([org-configuration.md § 5](org-configuration.md#5-service-agent-channel-stack-source-sections-712)). Check Salesforce's Messaging for In-App and Web documentation before you scope v2 work.
3. **Docs MCP runs on a herokuapp.com host.** The page's one-click Cursor install points at a `herokuapp.com` endpoint, not a `salesforce.com` domain ([docs-mcp]). **Inference:** this is a service run by Labs. Avoid putting client-confidential context into queries until its data handling is confirmed.
4. **Koa Decisions is beta** ([koa]):
   - its Core package can't be installed in a production org;
   - it has been verified only in internal test orgs;
   - it needs outbound access to `labs.agentforce.com`;
   - it uses an API key that an admin stores in the org.

   Not for client production.
5. **API versions differ between guides.** The seven web and messaging channel guides pin REST calls to v64.0; the LabBox page uses v65.0. Use your org's current version.
6. **Some pages still name agentforce.dev.** The Agent API, Enhanced Chat and Experience Site pages mention `agentforce.dev`; on the last two, the interactive Quick Setup widgets are labelled "on agentforce.dev". **Inference:** an older name for the same site.
7. **The SMS guide doesn't state country coverage.** It describes Salesforce-provisioned numbers, and the only market it names is US/Canada, for toll-free numbers. **Inference:** check country availability before proposing native SMS outside North America. BYOC with a messaging provider may be the realistic route.
8. **No RCS guide.** The channel list has no RCS Business Messaging entry. **Inference:** for telcos with their own messaging platforms, BYOC and the Agent API are the integration points to evaluate.

Section breakdown:
- **GET STARTED** — 24 pages
- **IDE Integrations** — 2 pages
- **Getting Started** — 1 page
- **Labs** — 9 pages
- **Build Agents** — 6 pages
- **Research** — 3 pages
- **Tools & Integrations** — 1 page
- **Agentforce Labs** — 2 pages

*Sources: [home page][home], [capability manifest][manifest], [`llms.txt`][llms] and the pages linked above, retrieved 2026-11-21.*

## Extraction notes

- Built from the capability manifest (48 entries) and the homepage. `scripts/refresh_agentforce_labs.py` regenerates [index.md](index.md) and the section breakdown above; it leaves the prose alone.
- Depth: the LabBox page is reviewed in full in [org-configuration.md](org-configuration.md). The other 47 pages were skimmed (opening paragraphs, section headings, and the sections on limits, prerequisites and constraints), not reviewed line by line. Code samples are not reproduced.
- This folder is not a `developer.salesforce.com` `llms.txt` area, so `scripts/refresh_from_llms.py` skips it (`EXTRA_SOURCES`).

[home]: https://labs.agentforce.com/
[llms]: https://labs.agentforce.com/llms.txt
[manifest]: https://labs.agentforce.com/api/capabilities
[build]: https://labs.agentforce.com/docs/build
[builder]: https://labs.agentforce.com/docs/agentforce-builder
[vibes]: https://labs.agentforce.com/docs/agentforce-vibes
[claude-code]: https://labs.agentforce.com/docs/claude-code
[skills]: https://labs.agentforce.com/docs/skills
[sf-pi]: https://labs.agentforce.com/docs/sf-pi
[agent-script]: https://labs.agentforce.com/docs/agent-script
[agent-api]: https://labs.agentforce.com/docs/agent-api
[deploy]: https://labs.agentforce.com/docs/deploy
[site-guide]: https://labs.agentforce.com/docs/salesforce-site
[chat-guide]: https://labs.agentforce.com/docs/salesforce-chat
[whatsapp]: https://labs.agentforce.com/docs/whatsapp-setup
[sms]: https://labs.agentforce.com/docs/sms-setup
[messenger]: https://labs.agentforce.com/docs/messenger-setup
[apple]: https://labs.agentforce.com/docs/apple-messages-setup
[line]: https://labs.agentforce.com/docs/line-setup
[byoc]: https://labs.agentforce.com/docs/byoc-setup
[platform-mcp]: https://labs.agentforce.com/docs/platform-mcp
[docs-mcp]: https://labs.agentforce.com/docs/salesforce-docs-mcp
[grid]: https://labs.agentforce.com/docs/agentforce-grid
[experiments]: https://labs.agentforce.com/docs/experiments
[upgrade]: https://labs.agentforce.com/upgrade-agent
[koa]: https://labs.agentforce.com/koa-decisions
[nanorag]: https://labs.agentforce.com/nanorag
[agentlens]: https://labs.agentforce.com/agentlens
[gws]: https://labs.agentforce.com/docs/agentforce-slides
