# Live-source evidence slice — Salesforce Hosted MCP and Flex Credits

**Observed:** 2026-11-22 (public official Salesforce pages read in review)
**Status:** source-observed **partial chain**, NOT a licensed/quote-ready graph and NOT a customer-specific rights check.
**Scope:** generic Salesforce Hosted MCP Servers, not automatically every server or every MCP action.

| Claim ID | Narrow statement supported by source | Official source / exact locator | Source status |
| --- | --- | --- | --- |
| \`MCP-PUBLIC-01\` | Salesforce Hosted MCP Servers expose data/automation to compatible MCP clients with per-user OAuth 2.0 + PKCE authentication, respecting assigned permissions. | [Salesforce Developers — Get Started](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.html), "Salesforce Hosted MCP Servers", paragraphs 1–4; bullets "Secure Authentication" and "SObject Operations". | SOURCE_OBSERVED |
| \`MCP-PUBLIC-02\` | Salesforce says Hosted MCP Servers are intended for customers with Flex Credits and **may** be billed for server usage. It directs customers to their account executive or Salesforce Foundations to obtain credits. | [Salesforce Developers — Get Started](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.html), paragraph after setup checklist, "Flex Credits". | SOURCE_OBSERVED |
| \`CREDITS-EU-01\` | The public EU Agentforce pricing page displays **€500 / 100,000 Flex Credits**. This is a published observation, not a binding SKU or customer contract. | [Salesforce EU — Agentforce Pricing](https://www.salesforce.com/eu/agentforce/pricing/), section "Flex Credits" and feature comparison "Flex Credits". | SOURCE_OBSERVED |

## What this evidence **does not prove**

- That buying a specific Flex Credit pack is always required (rather than a separately included credit entitlement), or which org/user/edition can activate each Hosted MCP server.
- That the general public \`€500/100,000 credits\` amount is a complete price for **one MCP request, interaction, action, API call or feature**.
- A published Headless Platform Interaction credit multiplier, the exact list of chargeable events, reset/overage rules, or contractual eligibility.
- That a named org has enabled the relevant MCP server, an authenticated client can access it, or a contractual user/license entitlement is present.
- That a source statement is active for every geographic region and Salesforce release. Re-check original docs and applicable rate card for production use.

## Candidate path (partly supported, not a complete purchasable route)

\`Business need: AI client calls Salesforce records/automation\`
→ \`Implementation option: Salesforce Hosted MCP Servers\` (MCP-PUBLIC-01)
→ \`Customer credit condition: intended for customers with Flex Credits\` (MCP-PUBLIC-02)
→ \`Public credit price observation: €500 / 100k credits\` (CREDITS-EU-01)

**Blocked edges:**
\`MCP operation → specific priced meter and multiplier\`;
\`customer's offer/contract → actual entitlement\`;
\`server/edition → activation rights and conditions\`.
The public credit **pack price cannot price these missing edges**.

Keep this as a review/evidence register, **not** a synthetic graph fixture and not a \`VERIFIED\` customer-license claim. Import into a production graph only after the independently validated source snapshot, claim IDs, applicable region/version and direct edge evidence can be preserved.
