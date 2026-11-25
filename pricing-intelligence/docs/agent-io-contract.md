# Agent I/O contract v1 — pricing knowledge and Flex Credit estimates

## Tool ownership

- Claude/other agents: intent routing, evidence collection, interpreting license dependencies, and reviewing assumptions.
- Deterministic CLI: metering, tier allocation, credit arithmetic and original-currency list-price equivalent.
- Salesforce org: **not required** to query public prices or run the local estimator. Use Salesforce CLI and an authorized org only for an explicitly org-bound activity.

## Discover valid meters

From repository root: `python pricing-intelligence/credit_calculator.py --list-meters`.
Read returned `contract_version`, `rate_card_version`, `source_url`, `review_status`, and `meters` (id, native unit, unit_size and status by environment). Never fabricate an ID or a sandbox multiplier.

## Input contract

Follow `pricing-intelligence/schema/scenario.schema.json`. Example:

```json
{
  "scenario_id": "sample-01",
  "pricing_model": "FLEX_CREDITS",
  "usage": [
    {"month":"2026-12","meter":"agentforce-standard-action","environment":"production","quantity":"5000"},
    {"month":"2026-12","meter":"data360-prep","environment":"production","quantity":"1000000"}
  ],
  "included_credits": "0"
}
```

Usage quantity uses raw native units: 1,000,000 Data 360 rows, **not** 1,000,000 million-row units. The metering denominator is specified by `unit_size` in the rate-card JSON.

Invocation: `python pricing-intelligence/credit_calculator.py --scenario pricing-intelligence/examples/agentforce-example.json`. To pipe JSON from the executing agent process: `python pricing-intelligence/credit_calculator.py --scenario -` with stdin redirected from a local file or process. Never pass customer contracts, access tokens or private personal data through tool arguments.

## Output semantics

| Field | Meaning |
|---|---|
| `contract_version` | Version of this local tool's I/O contract, **not** a Salesforce agreement |
| `status` | ESTIMATE_NOT_QUOTE or INCOMPLETE_UNPRICEABLE_USAGE |
| `rate_card_version` | Salesforce rate-card version used |
| `rate_card_review_status` | Transcription/verification status |
| `priced_lines` | Calculation for supported meters and source URL |
| `unpriceable_usage` | TBA or unsupported meters: **not zero** |
| `priced_credits_only` | Sum of calculable usage |
| `net_priced_credits_only` | Calculable usage after explicit allowance assumption |
| `partial_list_price_equivalent` | Public list-rate usage equivalent, **not** payable order total |

The tool exits with status 2 on invalid input. Agents must treat any such error as failure, not a blank or zero estimate. If any usage is unpriceable, report only the priced subtotal and explicitly disclose that the overall cost is unknown.

## Evidence envelope for other agents

Recommended response shape:

```json
{
  "status": "ESTIMATE_NOT_QUOTE",
  "source_status": "VERIFIED_OR_UNKNOWN",
  "rate_card_version": "2026-11-03",
  "credits": "100040",
  "evidence": [{"url": "https://www.salesforce.com/eu/agentforce/pricing/", "section": "Flex Credits"}],
  "assumptions": ["Customer applicability unverified"],
  "unpriceable_usage": [],
  "commercial_gaps": ["No Order Form or negotiated credits supplied"]
}
```

Do not label the source as VERIFIED without actually checking its applicable page, pricing metric and version. Internal unit tests only verify local arithmetic against the committed fixtures.

## Org-dependent extension gate (Agentforce Labs alignment)

Only if asked to build or deploy an Agentforce agent in a Salesforce org: follow `.claude/skills/sf-pricing-agentforce-bridge/SKILL.md` and official `https://labs.agentforce.com/llms.txt`. Verify CLI/project, authenticated org using a harmless Organization query, choose an explicit target alias and retrieve the existing authoring bundle before editing. Ask before installs/deployments/activations outside the authorized task. An org connection does not constitute permission to mutate org metadata.

## Tests

From repository root: `python -m unittest discover -s pricing-intelligence/tests -v`. CI provides independent runtime evidence for fixture compatibility, not actual Salesforce financial billing equivalence.
