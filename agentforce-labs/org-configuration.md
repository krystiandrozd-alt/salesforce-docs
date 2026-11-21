# Agentforce Labs — LabBox Org Configuration

Synthesis written independently from the source page (not copied prose). Setting labels, permission-set names and API names are quoted exactly, because those are the strings you search for in Setup; everything else is paraphrased. The source's scripts are described, not reproduced: open the source for runnable code.

- **Source page:** [LabBox · Agentforce Labs][src] (Markdown version: [`org-configuration.md`](https://labs.agentforce.com/api/docs/org-configuration.md))
- **Retrieved:** 2026-11-21. The page has no version or "last updated" date. The only date on it says the Vibes model and limits were last verified in June 2026.
- **Inference** marks my own reading, not the source's. [Review notes](#review-notes--verify-before-reuse) at the end list where the source's replication scripts look wrong or risky.

## What a LabBox is

A LabBox is a Salesforce org that Agentforce Labs provisions with the AI stack switched on and a working service-agent channel already set up. That covers Einstein, Agentforce, Data Cloud, Omni-Channel routing, an Enhanced Chat messaging channel, and a public Experience Cloud site with the chat widget ([src] intro). LabBox users don't need to configure anything. The page documents what is already there and how to rebuild it in your own org. Each section offers three ways to do that: Salesforce CLI (`sf`), REST API, and a click path the page calls "Browser Agent" ([src], every section).

How you get one: through a Labs connection. Labs uses your active LabBox if you have one, otherwise your connected own org, otherwise it provisions a new LabBox once you approve. The response can include an expiry time for the org (`org.expires_at`) ([llms] "Optional: connect through Labs").

## At a glance

| # | Area (source section) | State in a LabBox (per source) | Scriptable per source? |
|---|---|---|---|
| 1 | Core Platform | Einstein, Agentforce, Data Cloud on. Data Cloud provisioning takes 30–60 min | Verification queries only |
| 2 | API Access | "Enable SOAP API Login" on | No, UI only |
| 3 | Einstein Trust Layer | Large Language Model Data Masking **off** | No, UI only |
| 4 | Identity Verification | Verification for email-address changes **off** | No, UI only |
| 5 | Permissions | Custom `AiAdmin` permission set; 21 permission sets on the org user | Yes (CLI, Metadata API, REST) |
| 6 | Observability & Analytics | Audit and feedback, RAG quality metrics, Agent Analytics, Session Tracing, Agent Optimization, Service Agent Analytics app | Toggles UI only; permission-set assignment scriptable |
| 7 | Digital Experiences | Enabled | No, UI only |
| 8 | Routing | Omni-Channel skills-based and secondary routing on; a routing configuration and a queue | Partly. See [notes 1–2](#review-notes--verify-before-reuse) |
| 9 | Messaging | Enhanced Chat channel `Salesforce_Agent` routed to the service agent | Yes (Apex or REST) |
| 10 | Embedded Service Deployment | Web deployment `Salesforce_Agent`, switched to V2 and published | No, Setup wizard only |
| 11 | Experience Site | Public LWR site "Salesforce Agent" with the chat in the footer | Partly (`sf community create` / `publish`; chat component added in Builder) |
| 12 | Site Domain & Trusted Domains | Site domain registered; `*.my.site.com` trusted | Yes. See [note 3](#review-notes--verify-before-reuse) |
| 13 | Agent Deployment | Default Agentforce Service Agent deployed, compiled, published and active | Yes. See [note 6](#review-notes--verify-before-reuse) |
| 14 | MCP Servers | MCP Service available; standard servers ship inactive | Server activation UI only |
| 15 | Agentforce Coworker | Prerequisites and permissions documented. Not stated whether it is on in a LabBox | UI only; licences can be checked by query |
| 16 | Agentforce Voice | Documented. Telephony explicitly **not** pre-configured | UI only |
| 17 | Vibes | Documented. Availability depends on edition and region | Not applicable |

## 1. Core platform

These three are the foundation toggles; every other AI feature depends on them ([src] §Core Platform):

- **Einstein:** Setup → Einstein Setup.
- **Agentforce:** the table names "Einstein Copilot Setup" (the legacy name). The click path uses the toggle on the "Agentforce Agents" Setup page.
- **Data Cloud:** switched on at org provisioning. Allow 30–60 minutes.

The source only verifies these: it queries the `Organization` record and checks org limits. The REST variant reads the `EinsteinGenAiStandard` entry from `/services/data/v65.0/limits`.

## 2. Org-level access and trust toggles (source sections 2–4)

| Setting (label as written in the source) | Where | LabBox state | Reason given | Route |
|---|---|---|---|---|
| Enable SOAP API Login | Setup → User Interface | On | Programmatic login for CLI tools and back-end services | UI only |
| Large Language Model Data Masking | Einstein Trust Layer → Data Masking tab | Off | Larger LLM context; sensitive-data patterns are not masked in prompts | UI only |
| Require identity verification for email address changes | Identity Verification → General | Off (unchecked) | Lets org automation change user email addresses without verification flows | UI only |

Read [notes 4 and 5](#review-notes--verify-before-reuse) before you copy any of these into a customer org.

## 3. Permissions

LabBox creates a custom permission set `AiAdmin` (label and API name both AiAdmin) with four system permissions ([src] §Permissions):

| System permission (UI label) | API name in the source's metadata | Grants |
|---|---|---|
| Manage Agentforce Grids | `ManageAgentforceGrids` | Agentforce Grid worksheets |
| Manage Agentforce Testing | `ManageAgentforceTesting` | Running agent tests (the source says "Agent Eval Labs" tests) |
| Manage AI Agents | `ManageAiAgents` | Creating, editing and publishing agents |
| API Enabled | `ApiEnabled` | API access for CLI tools and integrations |

Permission sets assigned to the org user (21 in total):

- **Listed with a stated purpose:** AiAdmin, Data Cloud User, Access Agentforce Optimization, Tableau Next Admin, Tableau Next Platform Analyst, Contact Center Admin.
- **Also listed:** AI Workbench, Access Agentforce Default Agent, Agent Presence Status Access, Agentforce Default Admin, Agentforce Reference App, Agentforce Service Agent Configuration, Code Builder User, Contact Center Agent, Contact Center Supervisor, Customer Orders, Data Cloud Architect, Einstein Sales Emails, Prompt Template Manager, Prompt Template User, Tableau Next Consumer.

How the source scripts it:

1. Create the `PermissionSet` record if it doesn't exist.
2. Deploy the four `userPermissions` with a Metadata API package (API version 65.0) through `sf project deploy start`.
3. Assign `AiAdmin` and "Data Cloud User" to the oldest active System Administrator, using `PermissionSetAssignment` records.

The REST route can create the permission set and the assignments, but the system permissions still need the Metadata API or the UI. To check, look for one `PermissionSetAssignment` row for `AiAdmin` held by a System Administrator.

## 4. Observability & analytics

These are switched on in "Einstein Audit, Analytics, and Monitoring Setup" ([src] §Observability & Analytics):

- **Einstein Audit and Feedback:** logging of AI interactions.
- **Knowledge / RAG Quality Data and Metrics:** retrieval-quality metrics.
- **Agent Analytics:** dashboards and usage data.
- **Agentforce Session Tracing:** debug traces for each session.
- **Agent Optimization:** optimisation recommendations.

Next, install the "Service Agent Analytics" app (default data space) from Agent Analytics Setup. It can take about 15 minutes after provisioning to appear, because it waits for Agent Analytics. Last, assign "Access Agentforce Optimization". That assignment is the only step here the source can script.

## 5. Service-agent channel stack (source sections 7–12)

The source builds this stack in order: Digital Experiences → Omni-Channel routing → Messaging → Embedded Service Deployment → Experience Site → domains. The named resources a LabBox ships with:

| Resource | Name / API name | Key settings (per source) | How the source replicates it |
|---|---|---|---|
| Digital Experiences | — | Enabled; accept the domain-registration prompt | UI only |
| Omni-Channel settings | — | "Enable Skills-Based and Direct-to-Agent Routing", "Enable Secondary Routing Priority" | UI only |
| Routing configuration | Agentforce Service configuration (`Agentforce_Service_configuration`) | Priority 1, Most Available, capacity "2/3" (the source doesn't explain the notation) | UI. CLI and REST create a `ServiceChannel` record instead; see [note 1](#review-notes--verify-before-reuse) |
| Queue | Agentforce Service Queue (`Agentforce_Service_Queue`) | Supported object Messaging Session; routing configuration attached (UI route); admin as member | `Queue` metadata, or REST `Group` + `QueueSobject`; see [note 2](#review-notes--verify-before-reuse) |
| Messaging setting | — | Messaging Settings toggle on | UI only |
| Messaging channel | Salesforce Agent Channel (`Salesforce_Agent`) | Enhanced Chat, Web, routing type "Agentforce Service Agent", fallback queue Agentforce Service Queue | Inserts a `MessagingChannel` record through anonymous Apex or REST. Field values: `MessageType` = `EmbeddedMessaging`, `SessionHandlerId` = the agent's `BotDefinition` Id, `FallbackQueueId` = the queue Id, a unique `MessagingPlatformKey` |
| Embedded Service Deployment | Salesforce Agent Web Deployment (`Salesforce_Agent`) | Enhanced Chat, Web, linked to the channel; switched to V2, then published | Setup wizard only |
| Experience Cloud site | Salesforce Agent (URL prefix `salesforceagent`) | Template "Build Your Own (LWR)"; public access on; Enhanced Chat component in the footer, bound to the deployment | `sf community create` and `sf community publish`, or the Connect API publish call. The chat component is placed in Experience Builder |
| Site domain | — | Salesforce Site domain registered | UI. The script only queries `Domain` |
| Trusted domain | `*.my.site.com` | Added so the widget can load | UI: the site's "Trusted Domains for Inline Frames". CLI and REST: `CorsWhitelistEntry`. See [note 3](#review-notes--verify-before-reuse) |

One warning from the source is worth keeping: without the trusted-domain step, the widget fails silently. No chat button appears and no error is shown. The page calls this the most common cause of "chat doesn't work" ([src] §Site Domain & Trusted Domains).

The source also gives checks: the queue exists in `Group` (Type = Queue), and the site's `Network` record "Salesforce Agent" has Status = Live.

## 6. Agent deployment

The LabBox deploys a default Agentforce Service Agent, compiles it, publishes a version and activates it ([src] §Agent Deployment). The scripted route:

1. Deploy the agent metadata, an `aiAuthoringBundles` bundle holding a `.agent` Agent Script file, from a Labs project folder (`data/AgentforceDotCom`).
2. Exchange the CLI session for a "NamedUser" JWT (JSON Web Token) at `{instance}/agentforce/bootstrap/nameduser`.
3. Compile the Agent Script at `https://api.salesforce.com/einstein/ai-agent/v1.1/authoring/scripts`. The page calls this the "SFAP authoring endpoint" and doesn't expand SFAP.
4. Publish a version at `…/authoring/agents`. The response returns a `botVersionId`.
5. Activate it through the Connect API: `POST /services/data/v65.0/connect/bot-versions/{botVersionId}/activation`.

UI route: Agent Builder → import or create the agent → Activate or Publish. See [note 6](#review-notes--verify-before-reuse).

## 7. MCP servers

MCP stands for Model Context Protocol ([src] §MCP Servers):

- Check "Enable MCP Service (Beta)" (Setup → User Interface). Then activate each server you need in Setup → Integrations → API Catalog → MCP Servers, on the "Salesforce Servers" tab.
- Standard servers ship Inactive. The page says activation is UI-only: no Metadata API type or Tooling API field exists for it.
- Per the source, MCP is available on Enterprise, Developer and Unlimited editions and went GA in April 2026. See [note 7](#review-notes--verify-before-reuse).

| Server | Tools (per source) | Exposes |
|---|---|---|
| `sobject-reads` | 6 | Reading standard and custom records |
| `sobject-mutations` | 9 | Creating and updating records |
| `sobject-deletes` | 8 | Deleting records |
| `sobject-all` | 11 + 2 prompts | Read, write and delete, with guided prompts |
| `data-cloud-queries` | 2 | Data Cloud objects and unified profiles |
| `metadata-experts` | 1 | Inspecting org metadata |
| `salesforce-api-context` | 6 | Salesforce API reference for grounding agent responses |

- **External MCP clients:** they authenticate through an External Client App (ECA) with OAuth scopes `api`, `sfap_api`, `refresh_token` and `einstein_gpt_api`. The page stresses keeping `refresh_token`; without it, clients disconnect often.
- **Endpoints:** `https://api.salesforce.com/platform/mcp/v1/platform/<server>` for standard servers, `/v1/custom/<name>` for custom ones.
- **Deeper coverage:** [../hosted-mcp-servers/](../hosted-mcp-servers/) and the companion `headless-toolkit` repo.

## 8. Agentforce Coworker

A single switch (Setup → Agentforce Coworker → Get Started → Turn On) provisions six components: Agentforce Studio, CRM connectivity, AI search indexing, the pre-built coworker agent, per-user personalisation, and Data 360 user ingestion with identity resolution ([src] §Agentforce Coworker).

Prerequisites (per source):

- **Licence:** `AgenticEnterpriseSearchAddOn`, paired with `EinsteinAgentPlatform`. The page says it is bundled with Flex Foundations, A1E, A4X and Agentforce for Service or Sales. Those bundle names are written that way on the page and not expanded. Without one of those, the licence is added per SKU.
- **Data:** a Data Cloud data space. A Data 360 app must be visible in the App Launcher.
- **Models:** "Beta Generative AI Models" enabled in Einstein Setup.
- **Role:** Data 360 Admin or Data 360 Architect.

The page stresses how the licensing works:

- The add-on licence provisions two permission set licences (PSLs) automatically: `AISearchUserPsl` (AI Search Permission Set License) and `AISearchAdminPsl` (AI Search Setup Permission Set License). Admins do not request them.
- The add-on itself has no `PermissionSetLicense` row. To confirm provisioning, query those two PSLs.

Permissions:

- **To configure:** permission set "Agentforce Coworker Admin". The "Agentforce Coworker Setup" PSL is consumed automatically. The Setup node appears only after this assignment and a page refresh.
- **To use:** grant access in the "Manage Access to Agentforce Coworker" section of Coworker Setup. It assigns an AI Search access permission set group that setup creates; the page says to confirm the group's exact name in your org. Don't assign the bare "Agentforce Coworker User" / "Ask Agentforce User" permission set: it gives the UI but not the agent.
- Orgs not yet on release 262 may still show the legacy label "Ask Agentforce" for the same product. See [note 9](#review-notes--verify-before-reuse).

Salesforce guide: [Turn On Agentforce Coworker Infrastructure][coworker].

## 9. Agentforce Voice

You unlock Voice per agent by adding a voice connection in Agent Builder → Voice Settings ([src] §Agentforce Voice). There are two paths:

| Path | Result | Effort (per source) |
|---|---|---|
| Telephony connection | Phone calls over PSTN/SIP | Manual setup of the AWS contact centre, call flows and phone numbers, about 40 minutes end to end. **Not** pre-configured in a LabBox |
| Enhanced Chat v2 (ECv2) | Microphone input inside the chat window ("voice in chat") | Lighter. The source ties it to the Summer '26 feature "Voice-Enabled Agents in Enhanced Chat v2" |

- **Licences:** an Agentforce licence and a Service Cloud Voice licence, because Agentforce Voice runs on top of Service Cloud Voice telephony. Salesforce reference: [Agentforce Voice prerequisites][voice].
- **Check:** whether Service Cloud Voice is on is a Tooling API query on `ServiceCloudVoiceSettings.IsServiceCloudVoiceEnabled`, as given in the source.
- **Ready-made orgs:** the page suggests an OrgFarm "AgentforceVoice" checkout template for an org with voice already set up. See [note 8](#review-notes--verify-before-reuse).

## 10. Vibes

Vibes is Salesforce's agentic coding assistant inside the platform. It has two surfaces: Vibes Chat (in VS Code Desktop) and Vibes IDE (browser-based, launched from the org) ([src] §Vibes).

| Aspect | Per source (last verified by the page's authors in June 2026) |
|---|---|
| Price in Developer Edition | Free |
| Model | Anthropic Claude Sonnet, current generation |
| Developer Edition allowance | One-time 110 requests / 1.5M tokens per org. It doesn't refresh, and there is no fallback model once it runs out |
| Unmetered per-user-per-month (PUPM) licence | Not available in Developer Edition, which has no billing. Also not available to ISVs in Developer Edition |
| Not available in | EU Operating Zone, Government Cloud |

## Review notes — verify before reuse

Facts are cited. **Inference** marks my own reading.

1. **The routing-configuration script targets the wrong object (high confidence).** The source's CLI and REST routes create a `ServiceChannel` record with a routing-model value, and its check queries `ServiceChannel`. Salesforce's reference puts the routing-model picklist (LeastActive / MostAvailable / ExternalRouting) on `QueueRoutingConfig`, the object for "settings that determine how work items are routed to agents" ([QueueRoutingConfig][qrc]). The `ServiceChannel` reference lists no such field ([ServiceChannel][sc]). The site's own channel guides use `ServiceChannel` the documented way, as the `sfdc_livemessage` Messaging channel (for example the [SMS guide](https://labs.agentforce.com/docs/sms-setup)). **Inference:** the scripted step fails or creates the wrong record. Use the UI route, or create a `QueueRoutingConfig`.
2. **The scripted routes don't link the queue to the routing configuration.** The UI route sets "Routing Config" on the queue. The `Queue` metadata and the REST `Group` + `QueueSobject` calls don't. **Inference:** work in that queue isn't routed with that configuration until you link them. The site's [Experience Site guide](https://labs.agentforce.com/docs/salesforce-site) treats the queue only as the fallback for direct agent routing, so the gap mainly affects escalation to human agents.
3. **The UI and scripted routes set two different allowlists for the same step.** The UI route adds `*.my.site.com` to the ESW site's "Trusted Domains for Inline Frames". The CLI and REST routes add `https://*.my.site.com` to the org's CORS allowlist (`CorsWhitelistEntry`). Salesforce's Trailhead walkthrough for deploying the messaging connection to a site asks for the Experience site domain on the CORS allowlist. It describes the same symptom when it's missing: the chat window doesn't load and no error is shown ([Trailhead][cors]). **Recommendation (inference):** in customer orgs, add the exact site domain rather than the wildcard. The wildcard allows every `*.my.site.com` site.
4. **SOAP API login() is being retired.** Salesforce has scheduled `login()` retirement for Summer '27. It stays supported in API versions 62.0–64.0 for at least two years after each version's release ([SOAP API End-of-Life Policy][soap]). **Inference:** Salesforce CLI logins are OAuth-based and don't need this toggle. Don't build new integrations on `login()`; use OAuth through an External Client App.
5. **The security relaxations suit a lab org only.** LLM data masking is off, identity verification for email changes is off, the site is public, and SOAP login is on. **Recommendation:** don't replicate these in customer production orgs without a security and data-protection review.
6. **The agent-deployment script isn't portable.** It depends on a Labs project folder (`data/AgentforceDotCom`), a JWT bootstrap that uses a session cookie, and authoring endpoints I couldn't find in public Salesforce documentation. **Inference:** treat these as internal and liable to change. For repeatable work, follow the route Labs' own `llms.txt` recommends: Agent Script with the `agentforce-generate` and `agentforce-test` skills from `forcedotcom/sf-skills` ([llms] "Getting started").
7. **The MCP status wording is inconsistent.** The page calls MCP GA (April 2026), but the Setup checkbox it names is "Enable MCP Service (Beta)". Check the label and the release notes for your org's release.
8. **Two routes are Salesforce-internal.** Licences are provisioned "internally via Black Tab" (the page's words; customers use their SKU), and the page suggests an OrgFarm template for voice orgs. The site's [Upgrade Agent page](https://labs.agentforce.com/upgrade-agent) refers to "an internal orgfarm sandbox org", which confirms that OrgFarm is internal too. Partners and customers go through their own SKU or account team instead.
9. **Release 262 is an internal release number.** **Inference:** it corresponds to Summer '26. That fits the page's note that the rename rolled out around early June.
10. **"AWS Contact Center":** **Inference:** this means Amazon Connect, the AWS contact-centre service behind Service Cloud Voice.
11. **No Industries content.** Nothing on the page suggests a LabBox includes Industries or Communications Cloud features. **Inference:** for Communications Cloud or Industries demos, plan a separate Industries-enabled org, and treat a LabBox as a sandbox for service agents.

## Extraction notes

- Built from one fetch of the HTML page and one of its Markdown version, both on 2026-11-21. Both have the same 17 top-level sections. Code blocks were read but not reproduced.
- Notes 1, 3 and 4 were checked against the linked Salesforce sources on the same date. Notes 1, 2 and 8 were also cross-checked against the site's other pages. Everything else is as stated on the source page.
- The rest of the site is summarised in [content.md](content.md) and listed in full in [index.md](index.md).

[src]: https://labs.agentforce.com/chat/docs/org-configuration
[llms]: https://labs.agentforce.com/llms.txt
[qrc]: https://developer.salesforce.com/docs/platform/api-tooling/references/tooling-objects/tooling-queueroutingconfig.html
[sc]: https://developer.salesforce.com/docs/platform/object-reference/references/standard-objects/object-servicechannel.html
[soap]: https://developer.salesforce.com/docs/platform/api/guide/api-eol-soap.html
[cors]: https://trailhead.salesforce.com/content/learn/modules/agentforce-deployment-quick-look/deploy-the-messaging-connection-to-a-website
[coworker]: https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-turn-on-infrastructure.html
[voice]: https://help.salesforce.com/s/articleView?id=ai.agentforce_voice_setup_prereqs.htm&type=5
