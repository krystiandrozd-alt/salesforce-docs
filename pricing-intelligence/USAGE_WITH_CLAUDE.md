# Salesforce pricing intelligence — Claude Code quick start

> **Current status (2026-11-22):** Five project-scoped Claude skills, a limited sourced price seed, a machine-readable 2026-11-03 Flex Credit rate card, and a deterministic Python credit-estimation CLI are committed to draft PR #8. No UI, comprehensive product collector, customer SKU book, or negotiated pricing module has been implemented. GitHub Actions run https://github.com/krystiandrozd-alt/salesforce-docs/actions/runs/45020898343 succeeded (13/13 initial calculator fixtures); a later [17/17 test run](https://github.com/krystiandrozd-alt/salesforce-docs/actions/runs/45021458675) also checks five skill metadata/paths and org-mode safety gates; live Salesforce calculator parity and contract applicability remain unverified.

## Use in Claude Code

1. Check out this repository and the PR feature branch. Claude Code loads project skills from .claude/skills/ when launched from the repository (or a subfolder). No user-global installation needed.
2. Use the skill directly as a Claude Code command, or allow Claude to choose it based on its description.

| Skill command | Use |
|---|---|
| /sf-pricing-research | Find and verify current published Salesforce edition prices and source evidence |
| /sf-license-compare | Build cross-cloud licensing matrix, identify bundle inclusions, prerequisites and unknowns |
| /sf-flex-credit-estimate | Turn monthly Agentforce / Data 360 usage into source-versioned Flex Credit estimates |
| /sf-pricing-audit | Audit a price assertion, a comparison or calculator result against official sources and executable tests |
| /sf-pricing-agentforce-bridge | Only for a requested Salesforce-native Agentforce agent: verify CLI/org, use official ADLC plugin, build/test Agent Script with authorization |

Example prompts:
- /sf-pricing-research Compare Sales Cloud Core and Max EU prices and included capabilities, citing original sections.
- /sf-license-compare Model a B2B telecom architecture with Communications Cloud, Data 360 and Agentforce; distinguish user licenses, bundles and usage charges.
- /sf-flex-credit-estimate Estimate 5,000 Agentforce standard actions per month in production and 1M Data 360 Prep rows, using the current versioned rate card. Explain all assumptions.
- /sf-pricing-audit Check the Marketing Intelligence billing denominator conflict and verify the last calculations against the official rate card.

## Runnable calculator

Required: Python 3.10+ (only standard library).

From repository root:

    python pricing-intelligence/credit_calculator.py --scenario pricing-intelligence/examples/agentforce-example.json

Run fixtures:

    python -m unittest discover -s pricing-intelligence/tests -v

To create a new scenario, start from pricing-intelligence/examples/agentforce-example.json. Each usage record needs:
- month YYYY-MM,
- meter ID from pricing-intelligence/data/rate-card-2026-11-03.json,
- environment production/sandbox,
- quantity as decimal string expressed in the published meter's native unit.

Data 360 rows means individual rows (not millions of rows): a quantity of "1000000" corresponds to one million-row unit. Sandbox and production have separate rate rules. Data 360 tiering resets monthly for each meter. The CLI reports priced credit lines, missing/TBA lines, and an EU-list-price usage equivalent.

### Interpret output correctly

- ESTIMATE_NOT_QUOTE: all supplied meters are priced, **but contract applicability is not confirmed** and the number is not an invoice or guaranteed SKU.
- INCOMPLETE_UNPRICEABLE_USAGE: at least one meter (e.g. Headless Platform Interaction) has no published multiplier in the selected rate card; any reported amount covers **priced lines only**.
- The EU public amount of EUR 500/100,000 credits is an *equivalent list rate*, not proof of pack rounding, prepaid purchasing, inclusion limits or negotiated customer terms.
- Do not add Conversation pricing to Flex Credit usage in a single calculator scenario without checking product and org eligibility separately.
- This CLI does not price seat licenses, Data 360 profile purchase models, platform login credits, services, tax, migrations or implementation.


## Agentforce Labs guidance — separate mode

The official [Agentforce Labs `llms.txt`](https://labs.agentforce.com/llms.txt) guides **Salesforce org-bound Agentforce development**, not public Salesforce price research. No Salesforce org login, Salesforce CLI setup, LabBox or native Agentforce plugin is needed for the four public-price/local-calculator workflows.

If asked to author, deploy or test an Agentforce agent in a Salesforce org, use `/sf-pricing-agentforce-bridge`, follow the official [Salesforce Development Skills guide](https://labs.agentforce.com/api/docs/skills.md) and prefer `agentforce-adlc@claude-plugins-official` for Claude Code native Agentforce lifecycle. Verify existing `sf` CLI and sfdx-project.json, authenticate privately, confirm the intended org with a read-only Organization query and explicit `--target-org` before any changes; do not disclose auth JSON or credentials.

Agent Script makes deterministic action chains possible, but the current credit CLI is **not automatically available as a native Agentforce action or an MCP service**. A separate controlled adapter and live org validation are required. Connecting an org is not authorization to deploy.

See [Labs alignment audit](audits/2026-11-22-agentforce-labs-llms-alignment.md) and [agent input/output contract](docs/agent-io-contract.md).

## Planned architecture improvements (priority order)

P0. Validate the official rate-card transcription visually against the PDF and run CI tests; verify sample against Salesforce's published calculator.  
P1. Implement strict JSON Schema for prices, eligibility, purchasing models, meter rate versions, source snapshot and historical price observations.  
P2. Build a source registry and bounded discovery across every EU pricing-hub product/industry link; explicitly surface CONTACT_SALES and conflicting pages.  
P3. Add verified entitlement and bundle scopes to avoid double-counting across Sales, Slack, Tableau, Communications and Agentforce.  
P4. Build interactive scenario UI and contract-aware estimation only after P0-P3.  
P5. Consider graph database only when real multi-hop query complexity is demonstrated.

## Product integrity rules

A public pricing page is not a binding quote. A product edition is not a technical Salesforce license. A reported inclusion is not a boundless entitlement. Source capture dates do not prove effective dates. UNKNOWN is not zero, and CONFLICTED cannot be silently accepted.

**Project skills are instructions; they do not install Salesforce credentials or grant external data access.** The price seed has limited coverage and must not be presented as a full Salesforce price book.

Official Claude Code skill standard: https://code.claude.com/docs/en/skills
