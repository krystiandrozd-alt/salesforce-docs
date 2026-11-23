"""Strict public feature/SKU lookup regression tests; no live Salesforce claims."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "feature_sku_resolver.py"
DATA = ROOT / "salesforce_pricing_tree.json"
spec = importlib.util.spec_from_file_location("sf_feature_resolver", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class FeatureSkuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, _ = mod.read_catalog(DATA)

    def test_tmf_api_growth_and_advanced(self):
        r = mod.resolve(self.data, "TM Forum APIs", "communications")
        paths = r["features"][0]["paths"]
        self.assertEqual(len(paths), 2)
        self.assertTrue(all(p["relation"] == "INCLUDED_IN_EDITION" for p in paths))
        self.assertTrue(all(p["sku_code"] is None for p in paths))

    def test_advanced_filter_picks_only_advanced(self):
        r = mod.resolve(self.data, "TMF APIs", edition="Communications Cloud Advanced")
        self.assertEqual([p["offer"]["name"] for p in r["features"][0]["paths"]],
                         ["Communications Cloud Advanced"])

    def test_web_api_professional_vs_enterprise(self):
        professional = mod.resolve(self.data, "Web Services API", edition="Professional Edition")
        enterprise = mod.resolve(self.data, "Web Services API", edition="Enterprise Edition")
        self.assertEqual(professional["features"][0]["paths"][0]["relation"], "AVAILABLE_AS_ADDON")
        self.assertEqual(enterprise["features"][0]["paths"][0]["relation"], "INCLUDED_IN_EDITION")
        self.assertEqual(enterprise["customer_entitlement_status"], "UNKNOWN")

    def test_unknown_feature_never_implies_false(self):
        r = mod.resolve(self.data, "Completely unsupported example")
        self.assertEqual(r["status"], "NO_EVIDENCE_NOT_PROOF_OF_ABSENCE")

    def test_bss_anomaly_is_not_quote_ready(self):
        r = mod.resolve(self.data, "B2B EPC")
        p = r["features"][0]["paths"][0]
        self.assertEqual(p["billing_observations"][0]["amount"], 4000000)
        self.assertEqual(p["billing_observations"][0]["currency"], "USD")
        self.assertEqual(p["billing_observations"][0]["verification"], "REVIEW_REQUIRED")
        self.assertIsNone(r["commercial_total"])

    def test_cannot_invent_direct_feature_sku(self):
        copy = json.loads(json.dumps(self.data))
        copy["features"][0]["sku_direct_mapping"] = "FAKE-SKU-001"
        with self.assertRaises(mod.CatalogError):
            mod.validate(copy)

    def test_unknown_path_offer_rejected(self):
        copy = json.loads(json.dumps(self.data))
        copy["feature_entitlement_paths"][0]["offer_id"] = "missing"
        with self.assertRaises(mod.CatalogError):
            mod.validate(copy)

    def test_all_routes_have_source_and_no_orderable_sku(self):
        self.assertEqual(self.data["sku_records"], [])
        for route in self.data["feature_entitlement_paths"]:
            self.assertEqual(route["sku_status"], "UNVERIFIED")
            self.assertTrue(route["source_section"])

    def test_graph_fragment_valid_with_existing_resolver(self):
        graph_data = mod.graph_fragment(self.data)
        existing = ROOT / "solution-intelligence" / "resolver.py"
        pspec = importlib.util.spec_from_file_location("sf_structural_resolver", existing)
        structural = importlib.util.module_from_spec(pspec)
        pspec.loader.exec_module(structural)
        g = structural.Graph(graph_data)
        self.assertEqual(len(g.edges), len(graph_data["edges"]))
        self.assertTrue(all(claim["evidence_status"] == "UNKNOWN" for claim in g.claims.values()))

    def test_cli_json(self):
        output = subprocess.check_output(
            [sys.executable, str(SCRIPT), "--feature", "CPQ", "--product", "sales", "--json"],
            text=True)
        result = json.loads(output)
        self.assertEqual(result["sku_records"], [])
        self.assertGreaterEqual(len(result["features"][0]["paths"]), 2)
        self.assertIsNone(result["commercial_total"])

if __name__ == "__main__":
    unittest.main()
