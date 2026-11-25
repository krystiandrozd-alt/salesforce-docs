# Distribution — Salesforce Pricing Intelligence

## Two usable entry points

### Claude Code — portable project skill

**Canonical entrypoint:** `.claude/skills/sf-pricing-intelligence/SKILL.md` on this feature branch.

Invoke `/sf-pricing-intelligence`. It routes to the existing five specialist skills: research, license comparison, Flex Credit calculation, pricing audit, or native Agentforce ADLC bridge.

When the repository is checked out, use the deterministic calculator:

```bash
python pricing-intelligence/credit_calculator.py --list-meters
python pricing-intelligence/credit_calculator.py --scenario pricing-intelligence/examples/agentforce-example.json
python -m unittest discover -s pricing-intelligence/tests -v
```

Claude skills do not require installing the ChatGPT plugin, and public price lookups do not require Salesforce org authentication.

### ChatGPT — private skills plugin

- Name: `salesforce-pricing-intelligence`
- Plugin URL: https://chatgpt.com/plugins/plugins_6b02de2e09948191b22c8a38645cc902
- Initial release: `0.1.0` (2026-11-22)
- Scope: private to creator, not a public Marketplace plugin
- Bundled: one pricing orchestrator skill, evidence policy, runtime adapter contract and package manifests
- Does NOT bundle: an authenticated GitHub connection, Salesforce org or MCP server, running Python engine, full rate-card database or sales quotation integration

The private plugin's initial source archive was packaged separately from the repository. The Claude project skill is maintained here as the portable source of the routing contract. Changes to rates or workflows should be reviewed and explicitly released to both destinations; do not silently assume automatic sync.

## Decision

**Skill first for reproducible arithmetic; plugin for guided conversation.**

The most important unresolved step is a trusted read-only API/MCP adapter exposing *actual* deterministic calculations, versioned rate-card data and scoped graph queries to ChatGPT and other agents. Building a second price calculator inside prompts is not recommended.

## Verification criteria

1. CI runs the calculator tests and six-skill metadata/routing checks.
2. A user can request a concrete price lookup and get a cited, current product page.
3. A monthly credit scenario replays with the same JSON and rate-card version.
4. Missing/TBA or conflicting sources remain unknown rather than becoming zero.
5. Any claim of quote-ready pricing requires the customer's approved commercial terms.
