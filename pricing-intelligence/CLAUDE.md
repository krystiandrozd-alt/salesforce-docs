# Claude Code project instructions — Salesforce Pricing Intelligence

This folder is a pricing knowledge graph + Flex Credit estimator, not the larger Salesforce developer documentation catalog.

Read AGENTS.md for the shared safety, evidence and output contract. Use one relevant project skill from the repository's .claude/skills directory:
- sf-pricing-research — public source verification.
- sf-license-compare — edition/bundle/technical license research.
- sf-flex-credit-estimate — deterministic rate-card calculator.
- sf-pricing-audit — independent release/claim verification.

For multi-stage work, conduct source lookup → license mapping → deterministic estimate → independent audit; do not run every skill for a simple lookup.

Read docs/agent-io-contract.md for CLI input/output. Use --list-meters before selecting a meter. Never call calculations quote-ready and never assume an existing Salesforce commercial contract.

Run tests from repository root:
python -m unittest discover -s pricing-intelligence/tests -v

The PR implements a CLI and fixtures, not a deployed interactive calculator or complete source collector.
