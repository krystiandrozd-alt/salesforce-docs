# Feature → Entitlement → Offer → SKU: executable bounded pilot

**As of:** 2026-11-23. **Status:** bounded public-source pilot, not a Salesforce orderable SKU database, full license graph, or contract reconciliation service.

This implements the attached `FEATURE_LICENSE_MAPPING.md` pattern inside `pricing-intelligence/`, using canonical JSON, evidence-linked paths, deterministic CLI, JSON Schema and unit tests. Existing pricing blueprint and Flex Credit estimator remain unchanged.

## Supported relationships

- Business capability, aliases and feature context map to zero or more **typed entitlement paths**.
- `INCLUDED_IN_EDITION` differs from `AVAILABLE_AS_ADDON`; optional add-ons explicitly record eligible editions.
- Commercial offer and billing unit remain distinct from technical UserLicense / PSL / FeatureLicense / permission sets.
- Historical EU prices are referenced by ID in `seed-eu-2026-11-22.yaml`, not presented as new prices. Current US marketing observations retain their USD currency.
- `sku_records = []`: marketing names and prices cannot prove an orderable SKU.
- Uploaded-note B2B EPC → BSS Suite claim is `UNVERIFIED`, not included.
- `skills` is a currently empty, first-class per-feature reference list. Populate only after verifying exact skill identifiers in `forcedotcom/sf-skills` or the local skill inventory.

## Run from repository root

```bash
python pricing-intelligence/feature_license_resolver.py --list-features
python pricing-intelligence/feature_license_resolver.py --feature "TMF APIs" --product communications --edition "Communications Cloud Advanced" --json
python pricing-intelligence/feature_license_resolver.py --feature "CPQ" --product sales
python pricing-intelligence/feature_license_resolver.py --feature "CPQ" --product communications
python pricing-intelligence/feature_license_resolver.py --feature "Web Services API" --product ai-app-dev --edition Professional
python pricing-intelligence/feature_license_resolver.py --graph
python -m unittest discover -s pricing-intelligence/tests -v
```

Customer holdings are **local and private**, never checked in. Example local file outside this repository:

```json
{"holdings":[{"offer_id":"offer-comms-advanced","verification":"SELF_REPORTED"}]}
```

Pass `--inventory /private/path/customer-inventory.json`. A `CONTRACT_VERIFIED` holding requires a local private `evidence_ref`, but even a confirmed purchase does **not** prove that the Salesforce org has the necessary technical license or permission.

## Output contract

Paths return feature, offer, relation, eligibility, billing metadata, source URL + source section, verification, conditions, `sku_code: null`, `sku_status: UNVERIFIED`. Decision status separates edition availability from actual customer-held rights and technical configuration.

**Implemented:** 5 normalized features, 10 offers, 8 source-backed path records (7 verified, 1 unverified), 5 sources, 0 verified orderable SKUs, 15 unit tests run in a local file-equivalent workspace.

**Not implemented:** source crawler, exhaustive products and hub coverage, certifiable SKU/Order Form import, permission-set licenses or org inventory automation, TMF API volume limits, customer invoicing, full skill-to-feature mapping, MCP server, interactive UI, or production integration. `NO_EVIDENCE_NOT_PROOF_OF_ABSENCE` is not a license denial.

### Official pages verified on 2026-11-23

- TMF APIs and Advanced inheritance: https://www.salesforce.com/communications/pricing/
- Revenue Cloud Growth/Advanced CPQ: https://www.salesforce.com/sales/revenue-lifecycle-management/pricing/
- Web Services API add-on vs included editions: https://www.salesforce.com/platform/pricing-add-ons/
- Technical API access background: https://help.salesforce.com/s/articleView?id=000005140&language=en_US&type=1

Marketing price information is not a contractual quote.
