# Feature → Entitlement → Edition / Add-on → SKU: executable public-source slice

**Status:** 2026-11-23 · Public marketing observation only; NOT an orderable-SKU database or a customer quote.

## Entry points

- `salesforce_pricing_tree.json`: source-aware public features, offers, paths, review-gated price observations, license type vocabulary, conflict register. `sku_records` is deliberately empty.
- `feature_sku_resolver.py`: stdlib CLI, exact normalized alias matching, edition-aware entitlement paths and JSON output.
- `solution-intelligence/tests/test_feature_sku_resolver.py`: contracts and integration with `solution-intelligence/resolver.py`.

## Example commands (from repository root)

    python feature_sku_resolver.py --feature 'CPQ' --product sales --json
    python feature_sku_resolver.py --feature 'TMF APIs' --product communications --edition 'Communications Cloud Advanced' --json
    python feature_sku_resolver.py --feature 'Web Services API' --product ai-app-dev --edition 'Professional Edition' --json
    python feature_sku_resolver.py --feature 'B2B EPC' --product communications --json
    python feature_sku_resolver.py --graph-fragment > /tmp/feature-paths.json
    python -m unittest discover -s solution-intelligence/tests -v

## Contract

Business capability → exact normalized Salesforce feature → 0..N entitlement paths → editions/add-ons → candidate offer/price observation → **UNKNOWN orderable SKU** until sourced from a customer-specific order form/price book. `INCLUDED_IN_EDITION` means *listed on public page*, not that the org owns the license, permissions, usage capacity or API limits. An add-on listed on a page does not prove eligibility for every edition.

Each path carries a public URL, section, observed date, evidence and SKUs statuses. A price observation preserves source currency, unit, qualifier and `REVIEW_REQUIRED` without silent USD/EUR conversion. Empty/missing means `NO_EVIDENCE_NOT_PROOF_OF_ABSENCE`, not 'unavailable'. `--edition` on an unknown add-on relationship preserves `ELIGIBILITY_UNKNOWN`; it does not promote it to a confirmed match.

## Integration with Solution Intelligence

The `--graph-fragment` form exports stable `technical_feature` IDs, path-scoped `access_entitlement` nodes and commercial `offer` nodes with `ANY_OF` requirement groups. All claims are explicitly `UNKNOWN` in the structural graph; they are not promoted to independently VERIFIED by caller-provided public data. Compose with the process/functional-skill graph using shared feature IDs; customer-side entitlement, purchase prerequisites, contract SKU and pricing still require separate official/customer evidence and an integration approval gate.

## Source / quality caution

Communications Cloud pricing pages show differing tier amounts depending on page version; and the B2B BSS Suite advertises an unusual public **USD 4,000,000/org/year** starting figure. The older EU seed records **EUR 4,000,000**: this discrepancy is an unresolved *source/region/variant conflict*, not a currency conversion. Both are excluded from binding pricing calculations.

Do not equate Revenue Cloud CPQ, legacy Salesforce CPQ, and Communications Industries CPQ. Do not infer technical `UserLicense`, `PermissionSetLicense`, `FeatureLicense`, permission sets or billing allowances from a marketed product name.

Remaining production gates: independently captured immutable official snapshots; real technical and contract verification; coverage across products/editions; eligibility and allowance calculations; end-to-end test against authorized customer data; API/MCP exposure only after review.
