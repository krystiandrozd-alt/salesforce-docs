#!/usr/bin/env python3
"""Source-traceable Salesforce feature licensing paths (NOT an orderable SKU quote)."""
import argparse
import json
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent / "data" / "feature-entitlements-2026-11-23.json"
RELATIONS = {"INCLUDED_IN_EDITION", "AVAILABLE_AS_ADDON", "DOCUMENTED_ELIGIBILITY", "REQUIRES", "INCOMPATIBLE_WITH"}
VERIFICATIONS = {"SOURCE_VERIFIED", "UNVERIFIED", "INFERRED", "CONFLICTED"}


def key(value):
    return " ".join(str(value).casefold().split())


def _unique(items, label):
    ids = [row["id"] for row in items]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate IDs in {label}")
    return {row["id"]: row for row in items}


def validate(graph):
    """Fail closed on missing refs, invented SKU evidence, and unsourced paths."""
    for field in ("features", "offers", "sources", "feature_entitlement_paths", "sku_records"):
        if not isinstance(graph.get(field), list):
            raise ValueError(f"{field} must be a list")
    features = _unique(graph["features"], "features")
    offers = _unique(graph["offers"], "offers")
    sources = _unique(graph["sources"], "sources")
    _unique(graph["feature_entitlement_paths"], "feature_entitlement_paths")
    _unique(graph["sku_records"], "sku_records")
    for path in graph["feature_entitlement_paths"]:
        if path.get("feature_id") not in features or path.get("offer_id") not in offers:
            raise ValueError(f"invalid feature/offer reference in {path.get('id')}")
        if path.get("source_id") not in sources or not path.get("source_section"):
            raise ValueError(f"missing source/section in {path.get('id')}")
        if path.get("relation") not in RELATIONS or path.get("verification") not in VERIFICATIONS:
            raise ValueError(f"invalid relation/verification in {path.get('id')}")
        if any(offer_id not in offers for offer_id in path.get("eligible_offer_ids", [])):
            raise ValueError(f"invalid eligible offer in {path.get('id')}")
        if path["relation"] == "AVAILABLE_AS_ADDON" and offers[path["offer_id"]]["type"] != "ADDON":
            raise ValueError(f"add-on relation must point to an ADDON: {path['id']}")
    for offer in offers.values():
        billing = offer.get("billing")
        if billing and (not billing.get("unit") or not billing.get("display_period") or not billing.get("billing_cadence")):
            raise ValueError(f"incomplete billing metadata for {offer['id']}")
    for sku in graph["sku_records"]:
        if (sku.get("offer_id") not in offers or not sku.get("actual_sku") or
                sku.get("verification") != "ORDERABLE_SKU_VERIFIED" or not sku.get("official_evidence")):
            raise ValueError("SKU may only be added with an actual orderable code and official evidence")
    return features, offers, sources


def _edition_id(edition, offers):
    if not edition:
        return None
    matches = [o["id"] for o in offers.values() if key(edition) in (key(o["id"]), key(o["name"]))]
    if len(matches) != 1:
        raise ValueError(f"edition/offer not uniquely found: {edition}")
    return matches[0]


def _inventory_holdings(inventory, offers):
    if inventory is None:
        return {}
    if not isinstance(inventory, dict) or not isinstance(inventory.get("holdings"), list):
        raise ValueError("inventory must be an object with a holdings array")
    holdings = {}
    for row in inventory["holdings"]:
        if not isinstance(row, dict) or row.get("offer_id") not in offers:
            raise ValueError("inventory holding must refer to a known offer")
        if row.get("verification") not in ("CONTRACT_VERIFIED", "SELF_REPORTED"):
            raise ValueError("inventory verification must be CONTRACT_VERIFIED or SELF_REPORTED")
        if row["verification"] == "CONTRACT_VERIFIED" and not row.get("evidence_ref"):
            raise ValueError("CONTRACT_VERIFIED needs a private evidence_ref (do not commit contracts)")
        if row["offer_id"] in holdings:
            raise ValueError("duplicate inventory offer_id")
        holdings[row["offer_id"]] = row
    return holdings


def _status(paths, holdings, inventory_supplied):
    verified = [p for p in paths if p["verification"] == "SOURCE_VERIFIED"]
    if any(p["verification"] == "CONFLICTED" for p in paths):
        return "CONFLICTED"
    for p in verified:
        if p["relation"] == "INCLUDED_IN_EDITION" and holdings.get(p["offer_id"], {}).get("verification") == "CONTRACT_VERIFIED":
            return "COMMERCIAL_PATH_INCLUDED_TECHNICAL_CHECK_REQUIRED"
    for p in verified:
        if p["relation"] == "INCLUDED_IN_EDITION" and p["offer_id"] in holdings:
            return "SELF_REPORTED_HOLDING_TECHNICAL_CHECK_REQUIRED"
    for p in verified:
        if p["relation"] == "AVAILABLE_AS_ADDON" and holdings.get(p["offer_id"], {}).get("verification") == "CONTRACT_VERIFIED":
            return "ADDON_PURCHASE_CONFIRMED_TECHNICAL_CHECK_REQUIRED"
    if verified and inventory_supplied:
        if any(p["relation"] == "AVAILABLE_AS_ADDON" for p in verified):
            return "PURCHASE_OPTION_NOT_CONFIRMED"
        return "CUSTOMER_ENTITLEMENT_UNKNOWN"
    if any(p["relation"] == "INCLUDED_IN_EDITION" for p in verified):
        return "INCLUDED_IN_EDITION_NOT_CUSTOMER_VERIFIED"
    if any(p["relation"] == "AVAILABLE_AS_ADDON" for p in verified):
        return "PURCHASE_OPTION_NOT_CONFIRMED"
    return "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE"


def resolve(graph, feature, product=None, edition=None, inventory=None):
    features, offers, sources = validate(graph)
    edition_id = _edition_id(edition, offers)
    holdings = _inventory_holdings(inventory, offers)
    found = [f for f in features.values() if
             (not product or key(f["product"]) == key(product)) and
             (key(feature) == key(f["id"]) or any(key(feature) in key(n) for n in [f["name"], *f.get("aliases", []), *f.get("capabilities", [])]))]
    results = []
    for item in found:
        paths = []
        for p in graph["feature_entitlement_paths"]:
            if p["feature_id"] != item["id"]:
                continue
            if edition_id and edition_id not in [p["offer_id"], *p.get("eligible_offer_ids", [])]:
                continue
            offer = offers[p["offer_id"]]
            source = sources[p["source_id"]]
            paths.append({
                "id": p["id"], "relation": p["relation"], "verification": p["verification"],
                "offer_id": offer["id"], "offer_name": offer["name"], "offer_type": offer["type"],
                "eligible_offer_ids": p.get("eligible_offer_ids", []),
                "billing": offer.get("billing", {"status": "UNKNOWN"}),
                "source": {"id": source["id"], "url": source["url"], "section": p["source_section"], "type": source["type"]},
                "conditions": p.get("conditions", []), "sku_code": None, "sku_status": "UNVERIFIED"
            })
        results.append({
            "feature_id": item["id"], "feature": item["name"], "product": item["product"],
            "aliases": item["aliases"], "capabilities": item.get("capabilities", []),
            "skills": item.get("skills", []), "technical_license_status": item["technical_license_status"],
            "decision_status": _status(paths, holdings, inventory is not None), "paths": paths
        })
    return {
        "schema_version": graph["schema_version"], "as_of": graph["as_of"],
        "query": {"feature": feature, "product": product, "edition": edition, "inventory_supplied": inventory is not None},
        "status": "MATCHES_FOUND" if found else "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE",
        "results": results, "sku_count": len(graph["sku_records"]),
        "disclaimer": "Published offer relationships, not technical org validation or binding quote. UNKNOWN is not FALSE. No verified orderable SKU provided."
    }


def export_graph(graph):
    features, offers, sources = validate(graph)
    nodes = [{"id": f["id"], "type": "FEATURE", "label": f["name"]} for f in features.values()]
    nodes += [{"id": o["id"], "type": o["type"], "label": o["name"]} for o in offers.values()]
    nodes += [{"id": s["id"], "type": "SOURCE", "label": s["url"]} for s in sources.values()]
    edges = []
    for p in graph["feature_entitlement_paths"]:
        edges.append({"id": p["id"], "from": p["feature_id"], "to": p["offer_id"], "type": p["relation"], "verification": p["verification"], "source_id": p["source_id"]})
    return {"as_of": graph["as_of"], "nodes": nodes, "edges": edges,
            "counts": {"features": len(features), "offers": len(offers), "edges": len(edges), "verified_orderable_skus": len(graph["sku_records"])}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", help="Feature name or alias; matches multiple contexts if needed")
    parser.add_argument("--product", help="Exact product context: communications, sales, ai-app-dev")
    parser.add_argument("--edition", help="Exact offer ID or offer name")
    parser.add_argument("--inventory", type=Path, help="Private local JSON customer inventory (never commit contract data)")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--list-features", action="store_true")
    parser.add_argument("--graph", action="store_true", help="Export nodes/typed edges")
    parser.add_argument("--json", action="store_true", help="Compatibility flag; JSON is always output")
    args = parser.parse_args(argv)
    if not any((args.feature, args.list_features, args.graph)):
        parser.error("provide --feature, --list-features or --graph")
    try:
        data = json.loads(args.data.read_text(encoding="utf-8"))
        validate(data)
        if args.list_features:
            output = {"as_of": data["as_of"], "features": [{"id": f["id"], "name": f["name"], "product": f["product"]} for f in data["features"]]}
        elif args.graph:
            output = export_graph(data)
        else:
            inventory = json.loads(args.inventory.read_text(encoding="utf-8")) if args.inventory else None
            output = resolve(data, args.feature, args.product, args.edition, inventory)
    except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
