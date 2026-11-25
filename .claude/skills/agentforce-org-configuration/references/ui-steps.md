# Setup UI steps

From the Agentforce Labs LabBox page ("Browser Agent" tab). Give these to the user for every UI-only setting, or drive them with a browser agent only if the user approved changes. Setup menu labels can differ by release.

## 1. Core Platform
1. Setup → **Data Cloud Setup Home** → confirm Home Org shows Org Details (Data Cloud provisioned; Setup location "Org Provisioning", 30–60 min).
2. Setup → Quick Find **Einstein Setup** → confirm "Turn on Einstein" is on.
3. Setup → Quick Find **Agentforce Agents** → toggle on (top right). Refresh and confirm. (Page lists the Agentforce location as "Einstein Copilot Setup".)

## 2. API Access
Setup → Quick Find **User Interface** → check **Enable SOAP API Login** → Save.

## 3. Einstein Trust Layer
Setup → Quick Find **Einstein Trust** → Einstein → Einstein Generative AI → **Einstein Trust Layer** → **Data Masking** tab → turn **off** "Large Language Model Data Masking" → confirm.
*Client note: masking off is a lab/test convenience so prompts are not masked. Do not recommend this for a production org without a data-protection decision.*

## 4. Identity Verification
Setup → Quick Find **Identity Verification** → General → uncheck **Require identity verification for email address changes** → Save.
*Same caveat: lab convenience, weakens a security control.*

## 5. Permissions
1. Setup → **Permission Sets** → New → Label and API Name `AiAdmin` → Save.
2. System Permissions → Edit → check **Manage Agentforce Grids**, **Manage Agentforce Testing**, **Manage AI Agents**, **API Enabled** → Save.
3. Setup → **Users** → admin user → Permission Set Assignments → Edit Assignments → add `AiAdmin` and **Data Cloud User** → Save.

Permission sets assigned to the org user on a LabBox: AiAdmin, Data Cloud User, Access Agentforce Optimization, Tableau Next Admin, Tableau Next Platform Analyst, Contact Center Admin.
Also enabled on a LabBox: AI Workbench, Access Agentforce Default Agent, Agent Presence Status Access, Agentforce Default Admin, Agentforce Reference App, Agentforce Service Agent Configuration, Code Builder User, Contact Center Agent, Contact Center Supervisor, Customer Orders, Data Cloud Architect, Einstein Sales Emails, Prompt Template Manager, Prompt Template User, Tableau Next Consumer.
Only assign the extra ones the user's use case needs; availability depends on licences.

## 6. Observability & Analytics
1. Setup → Quick Find **Audit** → **Einstein Audit, Analytics, and Monitoring Setup** → enable **Audit and Feedback**, **Knowledge / RAG Quality Data and Metrics**, **Agent Analytics**, **Agentforce Session Tracing** (and Agent Optimization).
2. Setup → **Agent Analytics**. If blank, wait ~15 minutes.
3. Install **Service Agent Analytics**: down arrow → Install → Data Space: default → Ok → wait for "Installation Completed Successfully".
4. Assign **Access Agentforce Optimization** to the admin user.

## 7. Digital Experiences
Setup → Feature Settings → Digital Experiences → Settings → check **Enable Digital Experiences** → Save → OK on the domain popup.

## 8. Routing
1. Setup → Feature Settings → Service → **Omni-Channel Settings** → check **Enable Skills-Based and Direct-to-Agent Routing** and **Enable Secondary Routing Priority** → Save.
2. Setup → Feature Settings → Service → Messaging → **Messaging Settings** → toggle Messaging on.
3. Setup → **Routing Configurations** → New: name "Agentforce Service configuration", Routing Priority 1, Routing Model Most Available, Capacity 2/3.
4. Setup → **Queues** → New: label "Agentforce Service Queue", supported object Messaging Session, routing configuration from step 3, add the admin as member.

## 9. Agent Deployment
Setup → Agents → **Agent Builder** → import or create the agent → Activate / Publish → confirm status Active.

## 10. Messaging channel
Setup → Messaging Settings → **New Channel** → Enhanced Chat → Next:
- Channel Name: Salesforce Agent Channel; Developer Name: `Salesforce_Agent`
- Deployment Type: Web; Domain: the site domain
- Routing Type: Agentforce Service Agent; Agent: the agent from §9
- Fallback Queue: Agentforce Service Queue → Save

## 11. Embedded Service Deployment
Setup → Embedded Service → **Embedded Service Deployments** → New Deployment → Enhanced Chat → Web → Name "Salesforce Agent Web Deployment", API Name `Salesforce_Agent`, Domain, Messaging Channel "Salesforce Agent Channel" → Save → **Switch to V2** → **Publish**.

## 12. Experience Site
Setup → Digital Experiences → **All Sites** → New → **Build Your Own (LWR)** → Get Started → Name "Salesforce Agent" → Create. In Experience Builder: Settings → General → enable **Public Access**; drag **Enhanced Chat** into the Footer and select "Salesforce Agent Web Deployment"; **Publish**.

## 13. Site Domain & Trusted Domains
1. Setup → User Interface → **Sites and Domains → Sites** → accept terms → **Register My Salesforce Site Domain** → accept popup.
2. Open the **ESW_Salesforce_Agent_*** site → **Trusted Domains for Inline Frames** → add `*.my.site.com`.
3. Republish: Digital Experiences → All Sites → Salesforce Agent → Builder → Publish.

Without step 2 the widget fails silently — no button, no error.
