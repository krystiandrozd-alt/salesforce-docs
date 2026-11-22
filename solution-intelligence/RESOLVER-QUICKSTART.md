# Process-to-commercial resolver — runnable structural pilot

> **Status:** stdlib-only structural prototype with synthetic data, **not a production Salesforce licensing engine**. No live Salesforce org, vendor pricing, private contracts, authoritative commercial graph, pricing API or complete TCO estimator is connected here. The included fixture has fictional IDs/relationships, deliberately rated UNKNOWN/INFERRED.

## Usage

From the repo root, with Python 3.10+:

```bash
python solution-intelligence/resolver.py \
  --graph solution-intelligence/examples/wholesale-quote-to-order.synthetic.json \
  --resolve P-Q2O --context '{"region":"EU","as_of":"2026-11-22"}'

python solution-intelligence/resolver.py \
  --graph solution-intelligence/examples/wholesale-quote-to-order.synthetic.json \
  --impact OFFER-A

python -m unittest discover -s solution-intelligence/tests -v
```

Exit code 0 means the **structural query completed**, not that all claims are verified. Exit code 2 means query or graph validation failure; errors go to stderr. Results are JSON. The result's `data_class` identifies the synthetic fixture.

## Implemented in this prototype

- Typed directed nodes and relations; no joins by display name.
- Validated endpoint kinds, IDs, claim references, evidence fields and nonempty requirement groups.
- Process → step → capability → alternative implementation → technical feature/product variant → requirement group → right/entitlement → candidate offer and billing metric.
- Separate `ALL_OF` / `ANY_OF` alternatives, cycle detection and a 256-alternative safety limit.
- Trace IDs and gaps for evidence, source freshness, scope/applicability, dates, missing billing and unknown usage.
- Reverse impact exploration for offers, entitlements, meters, claims and explicit source-snapshot IDs.
- Optional queries by `functional_skill` ID when the graph includes `DELIVERS` and `USES_SKILL` edges.
- Candidate offer dependency inspection (`REQUIRES`, `ELIGIBLE_WITH`, `AVAILABLE_FOR_PURCHASE`); purchasing/ownership decisions remain unresolved.
- `commercial_total: null` and `calculation_status: NOT_RUN`: **no fabricated numbers**.

## Not implemented — do not claim these work

- Live ingestion or source verification from Salesforce Docs, Headless Toolkit or Pricing Intelligence. The reference registry remains navigation metadata only. **Even input claims labeled VERIFIED cannot make this pilot return `evidence_verified=true`; source attestation is absent.**
- Full conditional commercial offer prerequisite closure, buying model selection and customer-specific ownership/eligibility evaluation. The pilot only exposes offer prerequisites as unverified candidates.
- Calculation of actual price observations, regional rates, included allowances, pooled credit allocation, overages or implementation TCO.
- Adapter to the existing pricing Flex Credit calculator. This pilot does not call or replace that CLI.
- Search API/MCP server, similarity index, complete evidence snapshots, source-to-BOM diffs and production data refresh.
- Proof that a real Salesforce edition/license/feature is required or included.

## Next implementation gates

1. Ingest a small **independently sourced and verified** capability/offer chain using immutable IDs, exact official URL sections and dated applicability.
2. Pin Git commit SHAs per evidence run. Validate the source registry and page snapshots before promoting claims.
3. Implement recursive offer prerequisites, additive/substitutable entitlements, customer-owned rights and shared allowance logic.
4. Build an explicit pricing meter adapter, preserving the current `pricing-intelligence/credit_calculator.py` scenario schema, and test unknown/TBA behavior.
5. Expose read-only MCP/API only after end-to-end tests and a reviewed, verified source graph.

See the [full relationship contract](docs/capability-commercial-contract.md). This pilot is intentionally narrower; its synthetic tests must not be reported as acceptance of the full commercial contract.
