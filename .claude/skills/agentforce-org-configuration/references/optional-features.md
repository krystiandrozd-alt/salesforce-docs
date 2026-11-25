# Optional features: MCP Servers, Agentforce Coworker, Agentforce Voice, Vibes

From the Agentforce Labs LabBox page. The Coworker, Voice and Vibes parts were only retrievable as a summary of the page, not verbatim — confirm with the linked Salesforce pages before client use.

## Hosted MCP Servers
- Availability per the page: Enterprise, Developer, Unlimited editions; GA April 2026.
- Enable: Setup → **User Interface** → check **Enable MCP Service (Beta)**.
- Activate: Setup → Integrations → **API Catalog → MCP Servers** → "Salesforce Servers" tab → open a server → Activate → confirm. Standard servers ship **Inactive**; activate one at a time.
- UI only: the page says there is no Metadata API type or Tooling API field for activation.
- Standard servers (tool counts per the page): `sobject-reads` (6), `sobject-mutations` (9), `sobject-deletes` (8), `sobject-all` (11 tools + 2 prompts), `data-cloud-queries` (2), `metadata-experts` (1), `salesforce-api-context` (6).
- External clients: an External Client App with OAuth scopes `api`, `sfap_api`, `refresh_token`, `einstein_gpt_api`. Keep `refresh_token` or clients disconnect often.
- Endpoints: `https://api.salesforce.com/platform/mcp/v1/platform/<server>` (standard), `.../v1/custom/<name>` (custom).
- See also this repo's `hosted-mcp-servers/` folder for the official docs index.

## Agentforce Coworker
Enablement is UI only; CLI/API can only verify.

Prerequisites:
- Edition: Enterprise, Unlimited or A1 (from the summary).
- Licence: **AgenticEnterpriseSearchAddOn** (paired with EinsteinAgentPlatform). Bundled with Flex Foundations / A1E / A4X / Agentforce for Service or Sales; otherwise added via SKU. The add-on auto-provisions PSLs **AI Search Permission Set License** (`AISearchUserPsl`) and **AI Search Setup Permission Set License** (`AISearchAdminPsl`); the add-on itself does not appear in `PermissionSetLicense`.
- Data 360 (Data Cloud) with a data space; a Data 360 app visible in the App Launcher.
- Setup → Einstein Setup → **Beta Generative AI Models** on.
- Configuring user has Data 360 Admin or Data 360 Architect.

Steps:
1. Assign **Agentforce Coworker Admin** to yourself (consumes the "Agentforce Coworker Setup" PSL) and refresh — the Setup node appears only after this.
2. Setup → Quick Find **Agentforce Coworker** (pre-262 orgs: "Ask Agentforce").
3. Set Up Data Space → choose the data space.
4. Get Started → **Turn On** → confirm.
5. Enable the Global Search Bar.
6. Give users access through **Manage Access to Agentforce Coworker**. Do not assign the bare "Agentforce Coworker User" or "Ask Agentforce User" permission set — it grants the UI but not the agent.

Verify:
```bash
sf data query --target-org <alias> --query "SELECT DeveloperName, MasterLabel FROM PermissionSetLicense WHERE DeveloperName IN ('AISearchUserPsl','AISearchAdminPsl')"
```
Reference: https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-turn-on-infrastructure.html

## Agentforce Voice
- Licences: Agentforce licence + Service Cloud Voice licence.
- Voice Settings unlock after adding a voice connection: Agent Builder → open agent → **Voice Settings**.
- Paths: (a) **Telephony** — full PSTN/SIP voice, separate manual setup (~40 min: AWS contact center, call flows, phone numbers); (b) **Enhanced Chat v2 voice-in-chat** ("Voice-Enabled Agents in Enhanced Chat v2", Summer '26) — the lighter path.
- Verify:
  ```bash
  sf data query --use-tooling-api --target-org <alias> --query "SELECT IsServiceCloudVoiceEnabled FROM ServiceCloudVoiceSettings"
  ```
- Reference: https://help.salesforce.com/s/articleView?id=ai.agentforce_voice_setup_prereqs.htm&type=5

## Vibes (Agentforce Vibes) — information only
- Surfaces: Vibes Chat (VS Code desktop), Vibes IDE (browser, launched from the org).
- Free in Developer Edition; model per the page: Anthropic Claude Sonnet (current generation).
- Lifetime limit per org: 110 requests / 1.5M tokens, one-time, no refresh, no fallback model.
- DE orgs cannot get the unmetered per-user-per-month licence; ISVs cannot get unmetered access in DE orgs. Not available in EU Operating Zone or Government Cloud.
- Values last verified by the page June 2026 — may have changed.
