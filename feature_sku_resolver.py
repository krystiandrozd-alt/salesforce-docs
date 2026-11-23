#!/usr/bin/env python3
"""Public feature-to-entitlement lookup. Never equates a public offer with an orderable SKU.

Stand-alone: Python 3.10+ stdlib. --graph-fragment exports a typed 0.1.0
fragment compatible with solution-intelligence/resolver.py for composition.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

DEFAULT_DATA = Path(__file__).with_name("salesforce_pricing_tree.json")
RELATIONS = {"INCLUDED_IN_EDITION", "AVAILABLE_AS_ADDON", "DOCUMENTED_ELIGIBILITY"}
EVIDENCE = {"PUBLIC_PAGE_OBSERVED", "REVIEW_REQUIRED", "CONFLICTED"}
SKUS = {"UNVERIFIED", "CONFIRMED"}
class CatalogError(ValueError):
    pass

def norm(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    return re.sub(r"[^a-z0-9]", "", value.casefold())

def validate(data):
    if data.get("schema_version") != "0.1.0":
        raise CatalogError("Expected schema_version 0.1.0")
    indexes = {}
    for field in ("features", "offers", "sources", "feature_entitlement_paths",
                  "price_observations", "sku_records"):
        items = data.get(field)
        if not isinstance(items, list):
            raise CatalogError(f"{field} must be an array")
        entries = {}
        for item in items:
            ident = item.get("id")
            if not ident or ident in entries:
                raise CatalogError(f"Missing/duplicate {field} id: {ident}")
            entries[ident] = item
        indexes[field] = entries
    for feature in data["features"]:
        if feature.get("sku_direct_mapping") != "UNKNOWN":
            raise CatalogError("A public feature may not assert a direct SKU mapping")
    for offer in data["offers"]:
        if offer.get("sku_status") != "UNVERIFIED" or offer.get("orderable_sku") is not None:
            raise CatalogError("A public offer is not a validated orderable SKU")
    for source in data["sources"]:
        if not source.get("url", "").startswith("https://") or not source.get("section"):
            raise CatalogError("Each source needs an official HTTPS URL and section")
    for path in data["feature_entitlement_paths"]:
        for field, key in (("feature_id", "features"), ("offer_id", "offers"),
                           ("source_id", "sources")):
            if path.get(field) not in indexes[key]:
                raise CatalogError(f"{path.get('id')}: unknown {field}")
        if path.get("relation") not in RELATIONS:
            raise CatalogError(f"{path['id']}: unsupported relation")
        if path.get("evidence_status") not in EVIDENCE:
            raise CatalogError(f"{path['id']}: unsupported evidence status")
        if path.get("sku_status") != "UNVERIFIED" or not path.get("source_section"):
            raise CatalogError(f"{path['id']}: unverified SKU and source_section required")
        for edition in path.get("applicable_editions", []):
            if edition not in indexes["offers"]:
                raise CatalogError(f"{path['id']}: unknown edition {edition}")
    for price in data["price_observations"]:
        if (price.get("offer_id") not in indexes["offers"] or
                price.get("source_id") not in indexes["sources"] or
                price.get("verification") not in {"REVIEW_REQUIRED", "CONFLICTED", "PUBLIC_OBSERVATION"}):
            raise CatalogError(f"{price['id']}: invalid price observation")
    for sku in data["sku_records"]:
        if not all(sku.get(key) for key in ("sku_code", "offer_id", "source_id", "effective_from")):
            raise CatalogError("SKU requires exact code, offer, source and effective date")
        if sku["offer_id"] not in indexes["offers"] or sku["source_id"] not in indexes["sources"]:
            raise CatalogError("SKU has unknown provenance")
        if sku.get("validation_status") != "CONFIRMED_REQUIRED_SKU":
            raise CatalogError("SKU may only be stored when separately confirmed")
    return indexes

def read_catalog(path=DEFAULT_DATA):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return data, validate(data)

def _applicability(path, edition, offers):
    if not edition:
        return "NOT_FILTERED"
    selected = [oid for oid, o in offers.items()
                if norm(edition) in {norm(oid), norm(o["name"])}]
    if not selected:
        return "UNKNOWN_EDITION"
    if path["offer_id"] in selected and path["relation"] == "INCLUDED_IN_EDITION":
        return "MATCH"
    editions = path.get("applicable_editions") or []
    if editions:
        return "MATCH" if any(item in editions for item in selected) else "EXCLUDED"
    if path["relation"] == "INCLUDED_IN_EDITION":
        return "EXCLUDED"
    return "ELIGIBILITY_UNKNOWN"

def resolve(data, feature_query, product=None, edition=None):
    ix = validate(data)
    matches = []
    q = norm(feature_query)
    for feature in data["features"]:
        if q and q in {norm(feature["name"]), norm(feature["id"]),
                       *(norm(a) for a in feature.get("aliases", []))}:
            if not product or norm(product) in {norm(p) for p in feature.get("product_contexts", [])}:
                matches.append(feature)
    if not matches:
        return {"query": feature_query, "status": "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE",
                "features": [], "customer_entitlement_status": "UNKNOWN", "sku_records": []}
    results = []
    for feature in matches:
        routes = []
        for path in data["feature_entitlement_paths"]:
            if path["feature_id"] != feature["id"]:
                continue
            applicability = _applicability(path, edition, ix["offers"])
            if applicability == "EXCLUDED":
                continue
            offer = ix["offers"][path["offer_id"]]
            source = ix["sources"][path["source_id"]]
            prices = [p for p in data["price_observations"] if p["offer_id"] == offer["id"]]
            status = ("PUBLIC_EDITION_INCLUSION" if path["relation"] == "INCLUDED_IN_EDITION"
                      else "POTENTIAL_PURCHASE_OPTION" if path["relation"] == "AVAILABLE_AS_ADDON"
                      else "DOCUMENTED_ROUTE_REQUIRES_REVIEW")
            if path["evidence_status"] != "PUBLIC_PAGE_OBSERVED" or applicability != "MATCH" and edition:
                status = "REVIEW_REQUIRED"
            routes.append({"id": path["id"], "relation": path["relation"],
                           "offer": {"id": offer["id"], "name": offer["name"],
                                     "type": offer["offer_type"]},
                           "path_status": status, "edition_applicability": applicability,
                           "evidence_status": path["evidence_status"],
                           "sku_status": "UNVERIFIED", "sku_code": None,
                           "technical_entitlement_status": "UNKNOWN",
                           "customer_entitlement_status": "UNKNOWN",
                           "billing_observations": prices,
                           "source": {"url": source["url"], "section": path["source_section"],
                                      "observed_at": source["observed_at"],
                                      "verification": source["verification"]},
                           "notes": path.get("notes", "")})
        results.append({"feature_id": feature["id"], "feature": feature["name"],
                        "aliases": feature.get("aliases", []), "paths": routes,
                        "status": ("PUBLIC_ROUTES_FOUND_NOT_CUSTOMER_VALIDATED" if routes else
                                   "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE")})
    return {"query": feature_query, "product_filter": product, "edition_filter": edition,
            "as_of": data["as_of"], "catalog_status": data["catalog_status"],
            "features": results, "customer_entitlement_status": "UNKNOWN",
            "sku_records": [], "commercial_total": None,
            "note": "Public claim != actual contract or Salesforce org entitlement; never assume SKU."}

def graph_fragment(data):
    """Build self-contained structural fragment; no public claim is promoted to VERIFIED."""
    validate(data)
    nodes, edges, claims = [], [], []
    def claim(ident, source_id, section):
        source = next(s for s in data["sources"] if s["id"] == source_id)
        claims.append({"id": ident, "evidence_status": "UNKNOWN",
                       "evidence_refs": [{"url": source["url"], "locator": section,
                                          "retrieved_at": source["observed_at"]}],
                       "independent_source_attestation": False})
    for item in data["features"]:
        nodes.append({"id": item["id"], "kind": "technical_feature", "name": item["name"]})
    for item in data["offers"]:
        nodes.append({"id": item["id"], "kind": "commercial_offer", "name": item["name"],
                      "orderable_sku_status": "UNVERIFIED"})
    for feature in data["features"]:
        paths = [p for p in data["feature_entitlement_paths"] if p["feature_id"] == feature["id"]]
        if not paths:
            continue
        group_id = f"sf:group:alternatives:{feature['id']}"
        nodes.append({"id": group_id, "kind": "requirement_group", "operator": "ANY_OF"})
        for i, path in enumerate(paths):
            eid = f"sf:public-entitlement:{path['id']}"
            nodes.append({"id": eid, "kind": "access_entitlement", "name": "Public offer path, not verified technical entitlement"})
            claim_id = f"sf:claim:{path['id']}"
            claim(claim_id, path["source_id"], path["source_section"])
            for edge_id, src, pred, dst in (
                (f"sf:edge:member:{path['id']}", group_id, "HAS_MEMBER", eid),
                (f"sf:edge:includes:{path['id']}", path["offer_id"], "INCLUDES", eid)):
                edges.append({"id": edge_id, "source": src, "target": dst,
                              "predicate": pred, "claim_id": claim_id})
        p = paths[0]
        claim_id = f"sf:claim:requires:{feature['id']}"
        claim(claim_id, p["source_id"], p["source_section"])
        edges.append({"id": f"sf:edge:requires:{feature['id']}", "source": feature["id"],
                      "target": group_id, "predicate": "REQUIRES", "claim_id": claim_id})
    return {"graph_version": "0.1.0",
            "metadata": {"data_class": "PUBLIC_UNATTESTED", "sku_records": 0,
                         "note": "Composable graph fragment; merge by stable IDs, validate claims independently."},
            "nodes": nodes, "edges": edges, "claims": claims}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", help="Feature or alias (e.g. CPQ)")
    parser.add_argument("--product", help="Product context (communications, sales, platform)")
    parser.add_argument("--edition", help="Optional target edition; unknown add-on eligibility remains unknown")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--graph-fragment", action="store_true", help="Emit structural Graph v0.1.0 JSON")
    args = parser.parse_args()
    try:
        data, _ = read_catalog(args.data)
        if args.graph_fragment:
            result = graph_fragment(data)
        else:
            if not args.feature:
                parser.error("--feature is required unless --graph-fragment")
            result = resolve(data, args.feature, args.product, args.edition)
        if args.json or args.graph_fragment:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Status: {result.get('catalog_status', result.get('status'))}")
            for feature in result.get("features", []):
                print(f"{feature['feature']} [{feature['status']}]")
                for path in feature["paths"]:
                    print(f"  {path['relation']}: {path['offer']['name']} | {path['path_status']}")
                    print(f"    SKU: UNVERIFIED | contract entitlement: UNKNOWN | {path['source']['url']}")
            print("No confirmed SKU or customer-specific entitlement; commercial total: UNKNOWN")
    except (CatalogError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
