# S0: Existing estate: AI with what the customer already owns

*Decision file · researched 22 November 2026 · scenario S0 only*

**Customer as given.** Owns Microsoft 365 (Outlook, Word, Excel, PowerPoint, Teams, SharePoint, OneDrive), Microsoft Entra ID, Salesforce Sales Cloud and Service Cloud with Flow and custom logic.

| Field | Value |
|---|---|
| Communications Cloud | unknown |
| Revenue Cloud | unknown |
| Power BI | unknown |
| Tableau | unknown |
| Microsoft 365 plan | unknown |
| Salesforce edition | unknown. The brief says Agentforce, Slack and Tableau Next are not owned, which points to a legacy edition such as Enterprise or Unlimited (I). |
| Customer type | not stated |
| Industry | not stated (example given: B2B telecom) |

**Evidence classes.** V = vendor page opened this session · V2 = secondary source, or a vendor page seen only through a search extract · P = preview, beta or pilot · A = announced · I = inference · U = unknown.

**Research limits.** Salesforce Help pages would not render in this environment, so claims taken from them are marked V2. The Salesforce in Claude status was not re-checked because it is outside this scenario.

---

## 1. Verdict

**Fit: Limited, for any customer type.** Copilot Chat as included gives every employee secure, web-grounded chat. It can also work on an email or meeting the employee has open in Outlook or Teams (V). It cannot read Microsoft 365 work data on its own, cannot reach Salesforce, and cannot act in Salesforce (V). Every Microsoft route from Copilot into Salesforce requires a paid Microsoft 365 Copilot licence or usage billing, so the three test journeys stay manual: copy, paste and re-key (V, I).

**The counter-argument, "standing still means falling behind competitors who adopt AI now", only partly holds.**
- S0 is not standing still. It provides governed AI chat, Salesforce records in Microsoft Search, and existing Outlook and Teams CRM integrations at no new licence cost (V, V2).
- No evidence opened in this session shows competitive loss from waiting in this industry (U).
- The integrations that would change these journeys are preview or pilot today (P).
- Gartner forecasts that over 40% of agentic AI projects will be cancelled by the end of 2027 (V2, analyst).
- **Where the claim is right:** doing nothing about governance is the real risk. Unmanaged AI use is likely, and it is controllable today (I, V).

## 2. Choose this when / do not choose this when

**Choose S0 when:**
- The Salesforce renewal is more than six months away, and buying now would mean paying for preview features (I).
- The customer first needs to measure a baseline for meeting preparation and CRM logging before building a business case (I).
- The immediate priority is stopping CRM data leaking into personal AI tools. The controls sit in Entra, Copilot controls, Defender and Purview (V).
- The pilot group is small enough for standard Einstein Activity Capture, which is limited to 100 users (V2).

**Do not choose S0 when:**
- Sellers must update Salesforce from Outlook or Teams through an assistant. That needs Copilotforce, which in turn requires Microsoft 365 Copilot access and is in preview (V, P).
- Management expects natural-language analytics. Copilot in Power BI needs F2/P1 Fabric or Premium capacity (V), which is not part of this scenario.
- The customer is already on a Core, Advanced or Max Salesforce edition. Those include Agentforce, Agentforce Coworker and Flex Credits (V), so this file's assumptions no longer hold.

## 3. Products in scope

| Product | What it does in S0 | Status | Owned / new | Class | Source (date) |
|---|---|---|---|---|---|
| Copilot Chat (Basic) | Web-grounded chat with enterprise data protection. Work content only when uploaded or open in Outlook or Teams. Agents limited to instructions and public websites. | GA | Owned (eligible Microsoft 365 plans) | V | [learn.microsoft.com Copilot overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-chat-considerations) (opened 22 Nov 2026) |
| Microsoft 365 Copilot (Basic) in-app features | Draft and summarise in Word, Excel, PowerPoint and Outlook. Summarise and transcribe Teams meetings. No Graph grounding. | GA | Owned only if eligible. Eligibility may depend on tenant size (under 2,000 seats). | V (features) · V2 (eligibility) | same page; [iq-it.co.uk](https://www.iq-it.co.uk/blog/m365-copilot-basic-vs-premium) (22 Nov 2026) |
| Salesforce CRM synced connector | Indexes Account, Contact, Opportunity, Lead, Case, Event, Task and Campaign into Microsoft Search for any Microsoft 365 plan. No Copilot grounding without a Copilot licence. | GA (comments and attachments in private preview) | Owned. Indexing has no extra cost. | V | [connector overview](https://learn.microsoft.com/microsoft-365/copilot/connectors/salesforce-crm-overview), [prerequisites](https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/prerequisites) (22 Nov 2026) |
| Salesforce integration with Microsoft Teams | Mention, preview, edit and pin Salesforce records in chats, channels and meetings | GA. Needs a $0 SKU provisioned by the account executive. | Owned (Enterprise, Performance and Unlimited editions) | V2 | [help.salesforce.com](https://help.salesforce.com/s/articleView?id=sales.teams_int_use_get_the_app.htm&language=en_US&type=5) (search extract, 22 Nov 2026) |
| Outlook integration + Einstein Activity Capture (standard) | Manual logging from Outlook. Automatic email and event capture to the activity timeline. Standard licence covers up to 100 users. | GA. Salesforce for Outlook retires 30 Jan 2027. | Owned | V2 | [help.salesforce.com EAC](https://help.salesforce.com/s/articleView?id=sales.aac_limitations.htm&language=en_US&type=5) (search extract, 22 Nov 2026) |
| Flow, reports, dashboards | Business rules, validation, scheduled reports | GA | Owned per brief | I | customer brief (as supplied, 22 Nov 2026) |
| AI in the customer's current Salesforce edition | New editions include Agentforce, Coworker and 500,000–2.75M Flex Credits. Pricing for legacy editions is unchanged. Whether legacy editions gain these features is not stated. | GA (new editions, 3 Sep 2026) | Legacy: none confirmed | V · U (legacy entitlement) | [salesforce.com editions](https://www.salesforce.com/news/stories/salesforce-simplifies-editions-2026/) (3 Sep 2026) |
| Power BI / Tableau | Dashboards over Salesforce data. Copilot in Power BI needs F2/P1 capacity, and trial capacity is not supported. | GA | unknown | V | [Enable Copilot for Power BI](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi) (22 Nov 2026) |
| *Exit reference:* Salesforce in Copilot (Copilotforce) | 38+ sales skills. CRM writes require confirmation. Runs on Salesforce's **beta** MCP server under the Salesforce Beta Services Agreement. Requires Microsoft 365 Copilot access. | Public preview | New purchase | V, P | [Learn connector page](https://learn.microsoft.com/microsoft-365/copilot/connectors/salesforce-admin-published-federated-connector) (22 Nov 2026); [news.microsoft.com](https://news.microsoft.com/source/2026/11/17/microsoft-and-salesforce-announce-copilotforce-bringing-trusted-customer-context-and-action-into-microsoft-ai-experiences/) (17 Nov 2026) |
| *Exit reference:* Sales Cloud in Teams | Pipeline, deal alerts, opportunity updates in Teams | Pilot. Open beta "later this year". | New | V, P | news.microsoft.com (17 Nov 2026) |
| *Exit reference:* Salesforce Hosted MCP Servers | Any MCP client acting as the signed-in user | GA for Enterprise Edition and above. "Intended only for customers with Flex Credits." | New spend | V | [developer.salesforce.com blog](https://developer.salesforce.com/blogs/2026/04/salesforce-hosted-mcp-servers-are-now-generally-available), [overview](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.md) (opened 22 Nov 2026) |
| *Exit reference:* Copilot Cowork | Delegated multi-step tasks | GA, usage-billed. Requires a Microsoft 365 Copilot (Premium) licence. | New | V | Learn Copilot overview (22 Nov 2026) |

## 4. Journeys

### Meeting preparation

| Step | Surface | Agent that acts | How Salesforce is reached | Where the rule runs | Identity | Leave Outlook/Teams? |
|---|---|---|---|---|---|---|
| Open the invite and the related thread | Outlook | Copilot Chat summarises the open email (V) | Not reached | None | Entra user | No |
| Get account, opportunities and cases | Salesforce Lightning, Teams record preview, or Microsoft Search results | None | Salesforce UI; Teams integration (V2); synced index (V) | Salesforce sharing. The index applies record ACLs at crawl time (V). | Salesforce user; Entra-mapped identity for the index | Yes, for Lightning. No, for Teams preview and Search. |
| Assemble the brief | Copilot Chat | Copilot Chat, working on text the user pastes | Copy and paste | None. The user judges completeness. | Entra user (data stays under enterprise data protection, V) | No, but the work is manual |
| Recap after the meeting | Teams | Teams meeting summary, only if the user has Copilot (Basic) in-app (V/V2) | Not reached | None | Entra user | No |

### Email-to-Salesforce updates

| Step | Surface | Agent that acts | How Salesforce is reached | Where the rule runs | Identity | Leave Outlook/Teams? |
|---|---|---|---|---|---|---|
| Customer email arrives | Outlook | Einstein Activity Capture logs it to the timeline (V2) | Salesforce sync service | Capture settings in Salesforce | Salesforce user | No |
| Extract the commitment, next step or date | Outlook | Copilot Chat summarises the open thread (V) | Not reached | None | Entra user | No |
| Update the opportunity or task | Outlook integration side panel or Lightning | None: the human types it | Salesforce UI | Validation rules and Flow (I) | Salesforce user | No for the panel (I); yes for Lightning |
| Notify the team | Teams | None | Record mention via the Teams integration (V2) | Salesforce sharing | Salesforce user | No |

### Management analytics

| Step | Surface | Agent that acts | How Salesforce is reached | Where the rule runs | Identity | Leave Outlook/Teams? |
|---|---|---|---|---|---|---|
| Pipeline and forecast view | Salesforce dashboards | None in legacy editions (U) | Native | Report filters, sharing | Salesforce user | Yes |
| Cross-system view (finance, usage) | Power BI or Tableau, if owned (U) | Copilot in Power BI only on F2/P1 capacity (V) | Connector or extract | Semantic model | Power BI user | Yes |
| Narrative for leadership | Word, PowerPoint or Copilot Chat | Copilot Chat on pasted figures (V); in-app Copilot if eligible (V2) | Export and paste | None. Figures are unchecked by the assistant. | Entra user | No |

**Value test.**

| Journey | Frequent | Multi-system today | Measurable outcome | Value test | S0 coverage |
|---|---|---|---|---|---|
| Meeting preparation | Yes, daily per seller (I) | Yes: Outlook, Teams, Salesforce | Prep minutes per meeting | **Passes** | Partial and manual |
| Email-to-Salesforce | Yes, daily | Yes: Outlook and Salesforce | Logging lag, field completeness | **Passes** | Logging yes (V2); updates manual |
| Management analytics | Weekly or monthly (I) | Yes, if finance or usage data matters (U) | Report cycle time | **Fails** on frequency for most users, passes for sales operations (I) | Dashboards only |

## 5. Dependencies and hidden purchases

- **Blocking unsanctioned AI apps** needs Defender for Cloud Apps plus Defender for Endpoint on devices (V). Full Defender XDR is in E5, not E3 (V). On E3 this is a purchase (I).
- **DSPM for AI** discovery policies need Purview set up. Licence scope is not checked (U).
- **Work-data agents** in Copilot Chat are pay-as-you-go only (V). Any agent that grounds on SharePoint or Salesforce creates metered spend.
- **The synced connector** consumes Salesforce API quota on full crawls (V). If you opt in to index fields hidden by field-level security, it does not enforce that security in results (V).
- **Einstein Activity Capture beyond 100 users** needs a paid upgrade (V2).
- **The Teams integration** needs a $0 SKU from the Salesforce account executive (V2).
- **Salesforce for Outlook retires on 30 January 2027** (V2). If it is still in use, migrating to the Outlook integration is unavoidable work.

## 6. Overlaps with what the customer owns

| Capability | Microsoft side | Salesforce side | Note |
|---|---|---|---|
| Find a customer record | Microsoft Search via synced connector (V) | Salesforce global search | Duplicate index. Permissions are applied at crawl, not live (V). |
| CRM context in Teams | Salesforce integration with Teams (V2) | Sales Cloud in Teams (P) | Choose one when the pilot ends (I) |
| Email logging | Outlook integration (V2) | Einstein Activity Capture (V2) | Different storage and reporting behaviour; needs confirming (U) |
| Drafting emails | Copilot Chat or in-app Outlook (V) | Edition AI drafting, if any (U) | Possible double spend later (I) |
| Analytics | Power BI (U) | Reports, dashboards, Tableau (U) | Settle on one semantic layer before adding AI (I) |

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Sellers paste CRM data into personal AI accounts | Likely (I) | Promote Copilot Chat with Entra sign-in. Use tenant restrictions v2 for personal accounts (V). Turn on Defender cloud discovery for generative AI (V). |
| Users sign in to Copilot with personal Microsoft accounts | Possible | Personal-account entry points exist in Outlook and Teams (V). Block them with tenant restrictions v2 (V). |
| Pilot users treat Copilot output as CRM fact | Possible | Keep Flow and validation rules as the only write path. Train users that Copilot cannot see Salesforce (V). |
| Synced connector over-exposure | Unlikely if defaults are kept | Keep the field-level-security opt-in off. Keep the "only people with access" setting (V). |
| Waiting while previews change terms | Likely | Re-check status monthly; preview terms apply until GA (V). |
| Renewal locks in a legacy edition without AI | Possible | Get the edition-change quote before renewal (I). |

## 8. Questions to put to the vendors in writing

**Microsoft**
1. Which of our users get Microsoft 365 Copilot (Basic) in-app features, and does the 2,000-seat threshold apply to us?
2. Are Teams meeting summaries included for Copilot (Basic) users on our plan?
3. Can Copilot Chat (Basic) users use the Salesforce connector at all, through pay-as-you-go agents? What is the metering unit?
4. Which Purview DSPM for AI and Defender capabilities does our current plan include?

**Salesforce**
1. Do our legacy edition licences include any Agentforce, Coworker or Flex Credit entitlement today?
2. What does moving only sales users to a Core edition cost, and when is that allowed?
3. When will Salesforce in Copilot reach GA? Will it then still need Salesforce's beta MCP server, or will it move to the GA hosted server?
4. Confirm Einstein Activity Capture limits for our edition, and where captured emails are stored.
5. Does Agentforce Coworker in Teams require Data 360?

## 9. One validation experiment

- **Hypothesis:** with only owned tools, a pilot group cuts meeting-preparation time and CRM logging lag enough to defer any purchase until the Salesforce renewal.
- **Prerequisites:**
  - Copilot Chat pinned in Outlook and Teams.
  - Salesforce integration with Teams enabled.
  - Einstein Activity Capture for 20 or fewer pilot sellers.
  - Synced connector indexing Account, Opportunity and Contact.
  - Defender cloud discovery reporting on generative AI apps, if licensed.
- **Test steps:**
  1. Two-week baseline: prep minutes per external meeting, hours from customer email to CRM update, share of opportunities with a next step set.
  2. Four weeks with the owned tools and a one-hour training session.
  3. Weekly count of unsanctioned AI app use.
- **Pass criteria (proposed, set by the decision owner):** prep time down by an agreed share, logging lag below an agreed number of hours, and no increase in unsanctioned AI use.
- **Kill criteria:** no measurable change after four weeks, or more than half of pilot users still re-key data between tools daily. Either result means S0 cannot serve these journeys, so evaluate the Copilot-licensed scenario before renewal.
- **Decision owner:** head of sales operations, with the CIO for licensing.

**The single event that justifies leaving S0** is the Salesforce renewal quote. Today Copilotforce needs Microsoft 365 Copilot access, and it stays preview until Microsoft announces GA (V). New Salesforce editions bundle Agentforce, Coworker and Flex Credits at published prices, $195 per user per month for Core (V). So the decision point is the quote, compared against the experiment's measured gap.

## 10. Open gaps

| Gap | How to close |
|---|---|
| Customer's Salesforce edition, Microsoft 365 plan, and Power BI or Tableau ownership | Customer licence inventory |
| Salesforce Help pages for the Teams integration and Einstein Activity Capture could not be opened (V2 only) | Open them in a browser, or get written confirmation from the account executive |
| Whether legacy editions gain any AI (U) | Salesforce question 1 |
| Eligibility for Copilot (Basic) in-app features and Teams summaries (V2) | Microsoft questions 1 and 2; Microsoft service description |
| Purview and Defender licence scope (U) | Microsoft question 4 |
| Competitive evidence for the industry (U) | Ask peers or analysts for adoption data |
| Salesforce in Claude, Agentforce Coworker in Teams, and the Tableau Semantics dependency were not re-checked | Out of S0. Verify in the relevant scenario files. |
