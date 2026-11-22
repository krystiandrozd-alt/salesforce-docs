# Element matrix — validation report

- Elements: **79**, paths: **106**
- Sources: **104/109** verified (Doc 81, Kit 9, Up 14); 4 unverifiable (Ext, or file not supplied)
- False matrix cells avoided by the path model (vs. independent tags): **191**
- Path values marked as assumptions (not in any source): **34**
- Scenario queries: **23 passed, 0 failed**
- Hard errors: **0**, warnings: **9**

## Scenarios

| ID | Scenario | Result | Detail |
|---|---|---|---|
| S1 | Customer service on web, mobile and voice | PASS | top: af-voice |
| S1 | Customer service on web, mobile and voice | PASS | top: af-commerce-client, af-service-agent, enhanced-chat-v2, einstein-bots |
| S1 | Customer service on web, mobile and voice | PASS | top: mobile-sdk, af-service-agent |
| S2 | Sales employee assistant inside CRM | PASS | top: acc, af-employee-agent, af-it-service, af-prospecting |
| S3 | Enterprise search plus ask-and-act | PASS | top: af-coworker, slackbot |
| S4 | Claude / Claude Cowork on Salesforce data (MCP Out) | PASS | top: mcp-sobject, mcp-custom, mcp-headless360 |
| S4 | Claude / Claude Cowork on Salesforce data (MCP Out) | PASS | top: claude-apps, claude-cowork |
| S5 | Agent calls a third-party SaaS (MCP In) | PASS | top: action-mcp-in, external-services |
| S6 | ISV ships an agent on AgentExchange | PASS | top: packaging-agentexchange, action-mcp-in, mcp-custom, claude-code, claude-plugins, copilot-studio, hxl, mcp-partner |
| S7 | Native mobile app with embedded agent | PASS | top: mobile-sdk, lightning-types |
| S8 | Custom web app with employee chat | PASS | top: acc, af-employee-agent, tableau-agent |
| S9 | Agentic commerce | PASS | top: af-commerce-client, commerce-shopper-mcp |
| S10 | Document-heavy financial workflow | PASS | top: agent-telemetry, document-ai |
| S11 | Analytics Q&A on governed metrics | PASS | top: semantic-layer, tableau-agent, mcp-data360-tableau |
| S12 | Pro-code agent development with a coding agent | PASS | top: agentforce-dx, react-uibundle, dx-mcp, claude-code, lwc-mcp-tools, mcp-metadata-grounding |
| S13 | Marketing automation by an LLM | PASS | top: mcp-marketing |
| S14 | IT service and operations workflows | PASS | top: af-it-service, af-operations |
| S15 | Agent with long-term memory | PASS | top: agentic-memory, af-agent-api, semantic-layer |
| S16 | One rich result card on every channel | PASS | top: apex-slack-sdk, hxl |
| S16 | One rich result card on every channel | PASS | empty |
| S17 | Seller works from Microsoft 365 (Copilotforce) | PASS | top: mcp-custom, mcp-partner, copilotforce, m365-cowork, copilot-home, outlook-copilot, sales-cloud-teams, m365-workspaces |
| S17 | Seller works from Microsoft 365 (Copilotforce) | PASS | empty |
| S17 | Seller works from Microsoft 365 (Copilotforce) | PASS | empty |

## Errors

- none

## Warnings

- af-operations: maturity Unverified overrides doc-derived GA — Only one doc page and no marker; maturity not established.
- einstein-bots: maturity Legacy overrides doc-derived GA — Legacy is an inference: the Bot API pages carry no Legacy marker.
- claude-in-agentforce: only Ext/Inf sources — verify against vendor material
- claude-cowork: only Ext/Inf sources — verify against vendor material
- mcp-partner: declared Unverified but effective Beta via dependency — The Agentforce path does not depend on the plugin; the Copilot path rides the Beta Copilotforce plugin.
- m365-cowork: declared GA but effective Beta via dependency — Microsoft surface is GA; Salesforce data arrives through the Beta Copilotforce plugin.
- outlook-copilot: declared GA but effective Beta via dependency — Copilot in Outlook is GA; Salesforce data arrives through the Beta Copilotforce plugin.
- pipeline-review-ppt: declared GA but effective Beta via dependency — The brief calls the workflow GA (per the Salesforce newsroom) although the plugin it rides on is Public Preview; check before quoting.
- word-excel: declared GA but effective Beta via dependency — Word and Excel are GA; Salesforce data arrives through the Beta Copilotforce plugin.
