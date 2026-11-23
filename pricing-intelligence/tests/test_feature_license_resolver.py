"""No fabricated SKU and no accidental inclusion claims from a pricing page."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("feature_license_resolver", PROJECT / "feature_license_resolver.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
DATA = json.loads((PROJECT / "data" / "feature-entitlements-2026-11-23.json").read_text(encoding="utf-8"))


class FeatureLicensingTests(unittest.TestCase):
    def test_graph_validates(self):
        features, offers, sources = mod.validate(DATA)
        self.assertEqual((len(features), len(offers), len(sources)), (5, 10, 5))

    def test_tmf_growth_and_advanced_are_distinct_evidence_paths(self):
        result = mod.resolve(DATA, "TMF APIs", "communications")
        self.assertEqual({p["offer_id"] for p in result["results"][0]["paths"]},
                         {"offer-comms-growth", "offer-comms-advanced"})
        self.assertTrue(all(p["relation"] == "INCLUDED_IN_EDITION" for p in result["results"][0]["paths"]))
        self.assertEqual(result["sku_count"], 0)

    def test_advanced_filter(self):
        result = mod.resolve(DATA, "TMF APIs", "communications", "Communications Cloud Advanced")
        self.assertEqual([p["offer_id"] for p in result["results"][0]["paths"]], ["offer-comms-advanced"])

    def test_web_api_professional_is_addon_not_included(self):
        result = mod.resolve(DATA, "Web Services API", "ai-app-dev", "Professional")
        item = result["results"][0]
        self.assertEqual(item["paths"][0]["relation"], "AVAILABLE_AS_ADDON")
        self.assertEqual(item["decision_status"], "PURCHASE_OPTION_NOT_CONFIRMED")
        self.assertEqual(item["paths"][0]["billing"]["billing_cadence"], "UNKNOWN")

    def test_web_api_enterprise_is_included_in_edition_not_customer_verified(self):
        item = mod.resolve(DATA, "Web Services API", "ai-app-dev", "Enterprise")["results"][0]
        self.assertEqual(item["paths"][0]["relation"], "INCLUDED_IN_EDITION")
        self.assertEqual(item["decision_status"], "INCLUDED_IN_EDITION_NOT_CUSTOMER_VERIFIED")

    def test_cpq_not_silently_equate_revenue_and_communications(self):
        revenue = mod.resolve(DATA, "CPQ", "sales")
        telecom = mod.resolve(DATA, "CPQ", "communications")
        self.assertEqual([r["feature_id"] for r in revenue["results"]], ["feature-revenue-cpq"])
        self.assertEqual([r["feature_id"] for r in telecom["results"]], ["feature-industries-cpq"])
        self.assertEqual(telecom["results"][0]["decision_status"], "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE")

    def test_unverified_bss_cannot_become_purchase_confirmation(self):
        item = mod.resolve(DATA, "B2B Enterprise Product Catalog")["results"][0]
        self.assertEqual(item["decision_status"], "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE")
        self.assertEqual(item["paths"][0]["verification"], "UNVERIFIED")

    def test_unknown_feature_not_treated_as_unavailable(self):
        result = mod.resolve(DATA, "Nonexistent Licensed Something")
        self.assertEqual(result["status"], "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE")
        self.assertEqual(result["results"], [])

    def test_verified_customer_holding_does_not_verify_technical_access(self):
        inv = {"holdings": [{"offer_id": "offer-comms-advanced", "verification": "CONTRACT_VERIFIED", "evidence_ref": "private:order-form-123"}]}
        item = mod.resolve(DATA, "TMF APIs", "communications", inventory=inv)["results"][0]
        self.assertEqual(item["decision_status"], "COMMERCIAL_PATH_INCLUDED_TECHNICAL_CHECK_REQUIRED")
        self.assertEqual(item["technical_license_status"], "UNKNOWN")

    def test_self_report_does_not_upgrade_to_contract_verified(self):
        inv = {"holdings": [{"offer_id": "offer-comms-advanced", "verification": "SELF_REPORTED"}]}
        item = mod.resolve(DATA, "TMF APIs", "communications", inventory=inv)["results"][0]
        self.assertEqual(item["decision_status"], "SELF_REPORTED_HOLDING_TECHNICAL_CHECK_REQUIRED")

    def test_false_contract_verified_is_rejected(self):
        with self.assertRaises(ValueError):
            mod.resolve(DATA, "TMF APIs", inventory={"holdings": [{"offer_id": "offer-comms-growth", "verification": "CONTRACT_VERIFIED"}]})

    def test_non_addon_cannot_be_available_as_addon(self):
        d = copy.deepcopy(DATA)
        d["feature_entitlement_paths"][0]["relation"] = "AVAILABLE_AS_ADDON"
        with self.assertRaises(ValueError):
            mod.validate(d)

    def test_fake_sku_rejected(self):
        d = copy.deepcopy(DATA)
        d["sku_records"].append({"id": "sku-invented", "offer_id": "offer-comms-growth", "actual_sku": "GUESS-001", "verification": "UNVERIFIED"})
        with self.assertRaises(ValueError):
            mod.validate(d)

    def test_unreferenced_source_rejected(self):
        d = copy.deepcopy(DATA)
        d["feature_entitlement_paths"][0]["source_id"] = "missing"
        with self.assertRaises(ValueError):
            mod.validate(d)

    def test_export_graph_counts(self):
        graph = mod.export_graph(DATA)
        self.assertEqual(graph["counts"], {"features": 5, "offers": 10, "edges": 8, "verified_orderable_skus": 0})


if __name__ == "__main__":
    unittest.main()
