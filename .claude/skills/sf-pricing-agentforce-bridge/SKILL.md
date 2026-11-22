---
name: sf-pricing-agentforce-bridge
description: Author, test or integrate a pricing-related Salesforce Agentforce agent in a specifically authorized org. Do not trigger for public Agentforce price research, Flex Credit scenario estimation, or an offline licensing question.
---

# Agentforce Native Development Bridge (SPQ pilot)

Read `pricing-intelligence/AGENTS.md` for shared permissions, evidence boundaries and release requirements.

Use this skill only after confirmed **org-bound** user intent. Follow https://labs.agentforce.com/llms.txt and Claude-specific ADLC guidance at https://labs.agentforce.com/api/docs/skills.md. Keep pricing business rules in the deterministic engine, not Agent Script narrative.

**Boundary:** Public Salesforce price research is not a native agent-build request. A connected org is **not authorization** to modify its metadata. Native actions require a named target and user approval.

1. Check actual `sf --version`, project `sfdx-project.json`, installed ADLC skills and CLI `--help` for required flags. Do not install or upgrade just for public pricing.
2. Verify the **intended** org with a private auth check and read-only Organization query. Use explicit `--target-org`; do not expose raw credentials or change default org.
3. Use official `agentforce-adlc:agentforce-generate` and `agentforce-adlc:agentforce-test` only for authorized native work. For existing agent, retrieve and inspect `AiAuthoringBundle` before editing. For Claude, use official `agentforce-adlc` generate/test/observe skill as needed; for other tools use the supported portable skills, not duplicate installations.
4. Build a validated external action/API adapter if the agent must call the pricing engine. A Python CLI in the repo is not deployed to Salesforce and no MCP service should be assumed.
5. Run offline checks first; obtain authorization for org-changing tests, deployment, publishing or activation. Record actual target/version/logs; stop safely on missing org, permissions or approval.

**Output:** authorized target (safe alias), existing/new agent, changes and evidence, tests run, action boundary, remaining limitations. Never claim Salesforce integration merely because this skill exists.
