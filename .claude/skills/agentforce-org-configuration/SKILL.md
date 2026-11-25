---
name: agentforce-org-configuration
description: Configure or audit a Salesforce org so Agentforce agents can be built, deployed and tested end to end — the "LabBox" baseline from Agentforce Labs. Use when the user asks to set up, enable, check, verify or troubleshoot an org for Agentforce: Einstein / Agentforce / Data Cloud enablement, AiAdmin permission set, Einstein Trust Layer masking, observability (Session Tracing, Agent Analytics, Optimization), Omni-Channel routing and queue, Enhanced Chat messaging channel, Embedded Service deployment, LWR Experience Site with chat widget, trusted domains, agent compile/publish/activate, Hosted MCP servers, Agentforce Coworker, Agentforce Voice or Vibes limits. Also use when a chat widget "doesn't work" or shows no button.
---

# Agentforce org configuration (LabBox baseline)

Source: Agentforce Labs "LabBox" page — https://labs.agentforce.com/api/docs/org-configuration.md (human view: https://labs.agentforce.com/chat/docs/org-configuration). Captured 2026-11-21. A **LabBox** is an Agentforce Labs–provisioned org where all of this is already done; use this skill to reproduce the same baseline in the user's own org, or to audit an org against it.

## Rules before touching an org

1. **Read-only until told otherwise.** Connecting an org is not permission to change it. Deploy, create records, publish or activate only when the user asked for that change. Verification queries are fine.
2. **Identify the org first** and always pass `--target-org <alias>` explicitly:
   ```bash
   sf org list auth --json
   sf data query --query "SELECT Id, Name, IsSandbox FROM Organization" --target-org <alias> --json
   ```
   Report alias, org Id and sandbox flag; never echo access tokens.
3. **If it is a LabBox, change nothing** — every setting below is pre-enabled. If something looks disabled there, the page says to contact the Agentforce Labs team.
4. Run `scripts/verify-org.sh <alias>` (read-only) to see what is already in place before proposing changes.
5. Many steps are **Setup-UI only**. Do not invent CLI/API workarounds for them; give the user the UI path (see `references/ui-steps.md`) or drive it with a browser agent if one is available and the user approved.

## Configuration areas, method availability and order

Order below is the dependency order to follow. ✅ = documented on the source page, — = page says no equivalent.

| # | Area | What gets configured | CLI | REST | UI |
|---|---|---|---|---|---|
| 1 | Core Platform | Einstein, Agentforce, Data Cloud on (Data Cloud provisioning 30–60 min) | verify only | verify only | ✅ |
| 2 | API Access | Enable SOAP API Login | — | — | ✅ |
| 3 | Einstein Trust Layer | Large Language Model Data Masking **OFF** | — | — | ✅ |
| 4 | Identity Verification | "Require identity verification for email address changes" **off** | — | — | ✅ |
| 5 | Permissions | `AiAdmin` permission set + assignments | ✅ | partial (system perms need Metadata API) | ✅ |
| 6 | Observability & Analytics | Audit & Feedback, RAG quality, Agent Analytics, Session Tracing, Optimization, Service Agent Analytics app | PS assignment only | PS assignment only | ✅ |
| 7 | Digital Experiences | Enable Digital Experiences | — | — | ✅ |
| 8 | Routing | Omni-Channel settings (UI), routing config + `Agentforce_Service_Queue` | ✅ (after UI enable) | ✅ | ✅ |
| 9 | Agent Deployment | Deploy, compile Agent Script, publish version, activate | ✅ | endpoints only | ✅ |
| 10 | Messaging | Enable Messaging (UI) + `Salesforce_Agent` Enhanced Chat channel | ✅ | ✅ | ✅ |
| 11 | Embedded Service Deployment | `Salesforce_Agent` web deployment, switch to V2, publish | — | — | ✅ |
| 12 | Experience Site | "Salesforce Agent" LWR site, public, Enhanced Chat in footer | create + publish | publish only | ✅ |
| 13 | Site Domain & Trusted Domains | Register site domain; trusted domain `*.my.site.com`; republish | ✅ (not domain registration) | ✅ (not domain registration) | ✅ |
| 14 | MCP Servers (optional) | Enable MCP Service (Beta); activate servers one by one | — | — | ✅ |
| 15 | Agentforce Coworker (optional) | Licences, data space, turn on, user access | verify only | verify only | ✅ |
| 16 | Agentforce Voice (optional) | Voice connection in Agent Builder | verify only | verify only | ✅ |
| 17 | Vibes (info) | Limits only | — | — | — |

Ordering notes:
- **Agent Deployment (9) before Messaging (10)** — the channel needs the agent's `BotDefinition` Id. *(Inference: the source lists Messaging first, but its script queries `BotDefinition` and would return nothing otherwise.)*
- Omni-Channel and Messaging must be enabled in Setup **before** the CLI/REST routing and channel steps.
- Embedded Service Deployment needs the messaging channel; the Experience Site's Enhanced Chat component needs the deployment; the trusted-domain entry is on the `ESW_Salesforce_Agent_*` site the deployment creates. Republish the site after adding the trusted domain.
- The page reuses one sample agent, `Reservation_Agent` (placeholder `{{AGENT_NAME}}`). Ask the user which agent to use.

## Fixed names used by the baseline

| Item | Value |
|---|---|
| Permission set | `AiAdmin` — system perms `ManageAgentforceGrids`, `ManageAgentforceTesting`, `ManageAiAgents`, `ApiEnabled` |
| Also assigned to the admin | Data Cloud User, Access Agentforce Optimization (plus, on a LabBox: Tableau Next Admin, Tableau Next Platform Analyst, Contact Center Admin) |
| Routing configuration (`ServiceChannel`) | `Agentforce_Service_configuration` / "Agentforce Service configuration", Most Available, secondary routing priority 1, capacity 2/3 |
| Queue | `Agentforce_Service_Queue` / "Agentforce Service Queue", supports `MessagingSession` |
| Messaging channel | `Salesforce_Agent` / "Salesforce Agent Channel", Enhanced Chat, Web, routing type Agentforce Service Agent, fallback queue above |
| Embedded Service Deployment | "Salesforce Agent Web Deployment", API name `Salesforce_Agent` |
| Experience Site | "Salesforce Agent", template "Build Your Own (LWR)", URL prefix `salesforceagent` |
| CORS / trusted domain | `https://*.my.site.com` |
| API version in recipes | v65.0 |

The full list of permission sets enabled on a LabBox is in `references/ui-steps.md` §5.

## How to work

- **Audit request** ("is my org ready?", "what's missing?"): run `scripts/verify-org.sh <alias>`, then report per area in a table: in place / missing / cannot verify by API (UI-only — ask the user to confirm in Setup).
- **Setup request**: confirm the target org and which areas, then follow `references/cli-recipes.md` (preferred) or `references/rest-recipes.md`, and hand UI-only steps to the user from `references/ui-steps.md`. Run each area's verify query after it.
- **Optional features** (MCP, Coworker, Voice, Vibes): `references/optional-features.md`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Chat widget shows no button, no errors | Missing trusted domain `*.my.site.com` (the page calls this the most common cause) | Add it under Sites → `ESW_Salesforce_Agent_*` → Trusted Domains for Inline Frames, or create `CorsWhitelistEntry`; republish the site |
| Agent Analytics page blank | Still installing | Wait ~15 min after enabling Agent Analytics, then install Service Agent Analytics |
| Data Cloud not usable yet | Provisioning in progress | Allow 30–60 minutes |
| "Get Started with Agentforce Coworker" node missing | Admin PS not assigned | Assign "Agentforce Coworker Admin", refresh Setup; pre-262 orgs show "Ask Agentforce" |
| Users see Coworker UI but no agent | Bare "Agentforce Coworker User" / "Ask Agentforce User" PS assigned | Grant access via "Manage Access to Agentforce Coworker" instead |
| MCP clients keep disconnecting | `refresh_token` scope missing on External Client App | Scopes: `api`, `sfap_api`, `refresh_token`, `einstein_gpt_api` |
| Messaging channel script fails on bot Id | Agent not deployed yet | Run Agent Deployment first |

## Accuracy notes

- Everything here comes from the Agentforce Labs page, not from official Salesforce docs, and has not been tested against an org. Treat object/field names that the page alone uses (e.g. `CorsWhitelistEntry`, `QueueSobject`, `limits.EinsteinGenAiStandard`, the `api.salesforce.com/einstein/ai-agent/v1.1/authoring/*` endpoints, `/agentforce/bootstrap/nameduser`) as **unverified**; check `sf ... --help` and the official docs before relying on them in client work.
- Coworker, Voice and Vibes details came from a part of the page that was only available as a summary — lower confidence; confirm with the linked Salesforce help pages.
- Release-dependent facts (MCP GA April 2026, Summer '26 ECv2 voice, release 262 naming, Vibes limits verified June 2026) may change.
