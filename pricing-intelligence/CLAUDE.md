# Claude Code project instructions — Salesforce Pricing Intelligence

This folder is a pricing knowledge graph + Flex Credit estimator, not the larger Salesforce developer documentation catalog.

Read AGENTS.md for the shared safety, evidence and output contract. Follow [the solution skill routing policy](../solution-intelligence/docs/skill-routing.md) for architect-vs-pricing ownership; an experimental SPQ pricing plugin must not silently replace the canonical GitHub-first pricing workflow. For general Salesforce pricing requests, start with **`/sf-pricing-intelligence`** as the single entry point; it delegates to the relevant worker below and uses the deterministic calculator when appropriate. Use the specialist directly when the intent is already explicit:

- sf-pricing-research — public source verification.
- sf-license-compare — edition/bundle/technical license research.
- sf-flex-credit-estimate — deterministic rate-card calculator.
- sf-pricing-audit — independent release/claim verification.

Use the fifth skill `sf-pricing-agentforce-bridge` **only for explicitly requested Salesforce-native Agentforce development**. Follow Agentforce Labs https://labs.agentforce.com/llms.txt, and for Claude Code native agent lifecycle use the officially recommended `agentforce-adlc@claude-plugins-official` plugin when available/authorized. Public pricing research and local estimates never require Salesforce org login.

Before an org-bound change: confirm sf CLI, Salesforce project, authorized target org and authentication (private process; only safe alias/id returned), verify Organization via a read-only query, and use --target-org. Do not modify the default org. Ask before unapproved global skill installations or deployments. Connecting an org does not authorize deployment or activation.

For multi-stage work, conduct source lookup → license mapping → deterministic estimate → independent audit; do not run every skill for a simple lookup.

When the request starts from a designed business process, capability or functional skill, read [the process resolver prompt](../solution-intelligence/prompts/resolve-process-commercial.md) and [relationship contract](../solution-intelligence/docs/capability-commercial-contract.md). Use their typed evidence paths to reach the commercial inputs; do not infer package inclusion from a technical feature or skill name. A synthetic structural resolver pilot exists at `../solution-intelligence/resolver.py`, but verified Salesforce commercial relationship ingestion, a production resolver and an API/MCP endpoint are not implemented.

Read docs/agent-io-contract.md for CLI input/output. Use --list-meters before selecting a meter. Never call calculations quote-ready and never assume an existing Salesforce commercial contract.

Run tests from repository root:
python -m unittest discover -s pricing-intelligence/tests -v

The PR implements a CLI and fixtures, not a deployed interactive calculator or complete source collector.

