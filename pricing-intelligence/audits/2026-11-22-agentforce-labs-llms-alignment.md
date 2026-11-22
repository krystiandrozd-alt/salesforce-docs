# Agentforce Labs llms.txt — prompt and agent architecture alignment audit

Date: 2026-11-22 | Status: VERIFIED SOURCE REVIEW, PARTIAL PROJECT IMPLEMENTATION
Source fetched directly: https://labs.agentforce.com/llms.txt
Supplemental official references: https://labs.agentforce.com/api/docs/skills.md, https://labs.agentforce.com/api/docs/agent-script.md, https://labs.agentforce.com/api/docs/platform-mcp.md
Repository: krystiandrozd-alt/salesforce-docs | branch feature/pricing-licensing-knowledge-graph-20261122

## Decision

**Keep public commercial-price research and local pricing calculations independent from Salesforce org login.** The Labs llms.txt instructions address an org-bound Agentforce agent development workflow; they do not make Salesforce CLI or a LabBox a prerequisite for a public-page pricing agent. For native Agentforce agent development, adopt the official org validation, ADLC plugin, Agent Script, deployment safety and testing sequence.

## Actual comparison

| Official Labs recommendation | Existing state before audit | Assessment | Corrective action |
|---|---|---|---|
| Reuse user's project/org; ask only for missing details that change outcome | Project-local Claude pricing skills and limited data already exist; no org needed for public queries | PASS in local pricing mode | Explicitly declare public/offline and org-bound modes |
| For Salesforce agent development, check sf CLI and sfdx-project.json; use documented flags | No org-development workflow or CLI target verification in pricing skills | GAP when building native agents | Add optional sf-pricing-agentforce-bridge skill; no automatic CLI installation |
| Verify authorized target with read-only Organization query, explicit --target-org; avoid exposing auth JSON | No org integration implemented | NOT APPLICABLE to public pricing; BLOCK for org writes until checked | Make org verification mandatory only on org-bound workflow |
| Use agentforce-generate/agentforce-test skills for Agent Script build/test; retrieve existing AiAuthoringBundle | Current pricing skills do not build native Agentforce agents | GAP for Agentforce deployment | Delegate native build/test to official ADLC, not to pricing skills |
| For Claude Code specifically, official skills page recommends agentforce-adlc@claude-plugins-official | Existing four pricing skills are useful, but not substitutes for ADLC | GAP for native build lifecycle | Document optional ADLC installation and scope; check /plugin before use |
| For Codex/Cursor, official portable skills install via npx skills add forcedotcom/sf-skills | Current repo uses portable local SKILL.md format | PARTIAL | Reference portable install only if platform-agent tasks require it; don't duplicate installed skills |
| Deterministic Agent Script steps vs LLM decisions | Local credit calculation already deterministic (Python); Salesforce-native adapter not implemented | PASS for local math, NOT IMPLEMENTED in Salesforce | Define deterministic API action contract before any Agent Script deployment |
| Follow agentforce-test; authorize org-changing tests; report real outcomes | 13 local Python fixtures passed in GitHub Actions, but no Agentforce tests run | PARTIAL | Explicitly separate local fixtures from Agentforce tests and org deployment |
| Labs device authentication optional only on user request; protect device codes/access tokens | No Labs login implemented or requested | PASS / NOT APPLICABLE | Document optional private-process flow; never log credentials or change default org |
| Salesforce-hosted MCP servers require org setup and OAuth | Not part of local pricing CLI | NOT APPLICABLE / FUTURE | Do not claim MCP integration exists; use only with explicit authorized Salesforce configuration |

## Prompt architecture changes

1. **Intent router:** public pricing research, license comparison, deterministic credit estimate, independent audit, and optional native Agentforce bridge. Each has a separate skill.
2. **Context segmentation:** pricing agents use public-page evidence and a versioned rate card; native Agentforce builders use org auth and metadata only after explicit authorization.
3. **Action boundaries:** source retrieval cannot instruct the model to run unsafe commands; only the controlled workflow chooses tools. Never expose raw org auth/credential JSON.
4. **Deterministic finance:** meter rate and arithmetic remain outside LLM prompts; Agent Script may call a validated action but must not be treated as an executable local CLI.
5. **Release boundaries:** public estimates are never Salesforce quotes; local unit tests never imply a live Agentforce deployment/test.

## Source precedence clarification

The top-level llms.txt mentions selecting agentforce-generate and agentforce-test through the portable Salesforce Skills Library. Its *dedicated Claude Code skills page* more specifically recommends the Agentforce ADLC plugin from the official Claude marketplace. Apply that Claude-specific recommendation for native Claude Agentforce lifecycle tasks; retain project-local pricing skills independently.

## Explicit exclusions

- Do not call Salesforce CLI, authenticate an org, install a Salesforce ADLC plugin, deploy metadata or provision a Labs LabBox merely to answer a public Salesforce price question.
- Do not infer real customer SKU prices or license entitlements from Agentforce Labs technical docs.
- Do not call the local Python calculator a deployed Salesforce Agentforce action or MCP service.

## Verification status and next tests

- Factual source reviewed via direct fetch of llms.txt, skills.md, agent-script.md, platform-mcp.md. GitHub files inspected: pricing-intelligence/AGENTS.md, CLAUDE.md, sf-flex-credit-estimate skill and USAGE_WITH_CLAUDE.md.
- Files added: docs/agent-io-contract.md; .claude/skills/sf-pricing-agentforce-bridge/SKILL.md; this audit.
- Local rate calculator previously passed 13 fixture tests (GitHub Actions: https://github.com/krystiandrozd-alt/salesforce-docs/actions/runs/45020898343).
- Not run: Salesforce CLI discovery, Salesforce org auth or Organization query, native ADLC installation, Agent Script tests, publishing, MCP activation, or live Claude Code behavioral routing. These require a real org-bound request and environment.
- Verified GitHub Actions: https://github.com/krystiandrozd-alt/salesforce-docs/actions/runs/45021458675 completed successfully with 17/17 offline tests (13 credit-calculation fixtures + 4 agent-contract integrity checks); example output remained 100,040 Flex Credits.

**Acceptance:** PASS WITH CAVEAT for designing Claude *public pricing skills*. BLOCK for claiming native Agentforce integration or deployment until the org is confirmed and ADLC tests run.
