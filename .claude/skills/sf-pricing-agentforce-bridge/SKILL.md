---
name: sf-pricing-agentforce-bridge
description: Build or integrate Salesforce pricing intelligence as an Agentforce agent in an explicitly authorized Salesforce org; use Salesforce CLI, ADLC skills, and Agent Script only for org-bound Agentforce work. Do not use for public price research, offline credit estimates or licensing comparisons.
---

# Salesforce Pricing → Agentforce Bridge

**Trigger only** when the user requests native Salesforce Agentforce agent authoring, extension, deployment, testing, or org-backed actions. Do NOT use this skill for public Salesforce price research, local Flex Credit calculation or offline license comparison.

## Compatibility with maintained Salesforce skills

Use `forcedotcom/sf-skills` `agentforce-generate` and `agentforce-test` only for native Agent Script work. The upstream skill may instruct `sf config set target-org`; do **not** follow that side effect here. Preserve the user's default org and use explicit `--target-org <alias>` on supported org-bound commands. If the requested action cannot be completed without changing defaults, stop and request specific approval. Check supported flags with the installed CLI and keep authentication JSON/token output private; upstream generic examples do not override this project's credential controls.

`platform-docs-get` can supply technical Salesforce documentation, but not evidence of Salesforce commercial price applicability or proof that a rate-card PDF has been reconciled. Do not install all official Salesforce skills merely for public pricing questions.

## Read authoritative guidance

- Agentforce Labs: https://labs.agentforce.com/llms.txt
- Claude Code ADLC/skills recommendation: https://labs.agentforce.com/api/docs/skills.md
- Agent Script language: https://labs.agentforce.com/api/docs/agent-script.md
- Salesforce-hosted Platform MCP clients: https://labs.agentforce.com/api/docs/platform-mcp.md
- Project pricing contract: pricing-intelligence/AGENTS.md and pricing-intelligence/docs/agent-io-contract.md

## 1. Confirm intent, runtime, target

- Reuse the user's named Salesforce project and intended org; ask only for essential unknowns.
- Check `sf --version`, the existing `sfdx-project.json`, and required flags via installed CLI `--help` before changing environment. Do not upgrade on update notice alone.
- Only for an org-bound task, inspect Salesforce CLI auth inside a process; never print raw `sf org list auth --json`, usernames, access tokens, refresh tokens, device codes or secrets. Output only a needed safe alias and org ID.
- Do not mistake a local auth entry for verified connection. Confirm intended target with a read-only `sf data query --query 'SELECT Id, Name, IsSandbox FROM Organization' --target-org ALIAS --json`. Report only safe verified identification, not raw responses.
- Always pass `--target-org ALIAS` for intended-org calls and preserve the default org.
- If auth is absent, request normal user-driven login and avoid credential exposure. Connect through Agentforce Labs only when user explicitly requests Labs. A Labs connection cannot select an arbitrary org.

## 2. Choose the proper Salesforce agent-development capability

- In Claude Code, the official Agentforce Labs skills guide recommends the **Agentforce ADLC** Claude plugin for agent lifecycle tasks: `agentforce-adlc@claude-plugins-official`.
- Install or change plugins only when needed and permitted. Confirm via Claude `/plugin` that the plugin is enabled and commands load.
- Use `/agentforce-adlc:agentforce-generate` and `/agentforce-adlc:agentforce-test` and, if appropriate, `/agentforce-adlc:agentforce-observe`.
- For non-Claude coding tools, portable `agentforce-generate`, `agentforce-test`, `agentforce-observe` skills are available through `npx skills add forcedotcom/sf-skills`. Do not blindly install multiple overlapping copies.
- The project-local `/sf-pricing-research`, `/sf-license-compare`, `/sf-flex-credit-estimate`, and `/sf-pricing-audit` skills remain specialized *commercial/pricing* workflows. They are not replacements for ADLC deployment skills.

## 3. Build only after confirming the target and authorization

- Prefer source-controlled Agent Script (`.agent`) and deterministic action/tool implementations. Never put authoritative arithmetic in free-form LLM prompts.
- For an existing agent, verify its developer name and retrieve and inspect its `AiAuthoringBundle` before editing.
- If exposing pricing calculations, build a schema-validated action/API adapter for the deterministic CLI or a properly deployed equivalent; do not imply that a local Python process is already available inside Salesforce Agentforce.
- Ground every published price with source URL, pricing unit and version; product-specific contracting and org access must be validated separately.
- Agent Script can route tasks and invoke actions; keep quote approval, contract eligibility and license enforcement in deterministic systems, not just reasoning instructions.

## 4. Test and release gates

- Start with offline JSON/price validation and the local Python test suite.
- Follow `agentforce-test` for Agent Script tests. Obtain authorization before tests that deploy metadata, run live actions or consume billable resources.
- Do not deploy, publish or activate an agent unless the user authorizes the specific org and action. Merely connecting is not authorization to change Salesforce.
- For any activated agent, verify org, authoring-bundle version, tests and safe action output before reporting success.
- Record what changed, tests actually run, credential/security safeguards, remaining product limits and unknown commercial terms.

## Optional Labs authentication

Only when requested, follow the exact flow and current safeguards in https://labs.agentforce.com/llms.txt. Never emulate the device flow in the LLM context or paste raw token JSON into chat. Use an approved private subprocess. Respect blocked network access and rate limits; do not weaken TLS/proxy protections.

## Output contract

Return `task / intended org + safe alias / existing vs new agent / planned or executed changes / relevant source citations / test outcomes / authorization boundaries / remaining unknowns`. If the org cannot be verified, stop before mutation and continue with local artifacts only.
