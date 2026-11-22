"""Structural resolver tests on fictional data; not a Salesforce billing validation."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("solution_resolver", ROOT / "resolver.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Graph, GraphError = module.Graph, module.GraphError


def fixture():
    return json.loads((ROOT / "examples/wholesale-quote-to-order.synthetic.json").read_text())


class ResolverTests(unittest.TestCase):
    def test_two_routes_and_three_requirement_alternatives(self):
        r = Graph(fixture()).resolve("P-Q2O")
        self.assertEqual(r["route_status"], "PARTIAL")
        self.assertEqual(len(r["alternatives"]), 3)
        native = [a for a in r["alternatives"] if a["implementation_option_id"] == "OPTION-NATIVE"]
        self.assertEqual({tuple(a["requirements"]) for a in native}, {
            ("ENT-ADDON-A", "ENT-BASE"), ("ENT-ADDON-B", "ENT-BASE")
        })
        self.assertEqual({a["implementation_option_id"] for a in r["alternatives"]}, {
            "OPTION-NATIVE", "OPTION-MCP"
        })

    def test_trace_and_unpriced_never_zero(self):
        r = Graph(fixture()).resolve("CAP-QUOTE")
        self.assertIsNone(r["commercial_total"])
        self.assertEqual(r["calculation_status"], "NOT_RUN")
        self.assertTrue(all(not a["evidence_verified"] for a in r["alternatives"]))
        self.assertTrue(all(a["trace_claim_ids"] and a["trace_edge_ids"] for a in r["alternatives"]))
        self.assertTrue(any(a["usage_meter_ids"] == ["METER-UNKNOWN"] for a in r["alternatives"]))

    def test_reverse_impact_from_offer(self):
        impact = Graph(fixture()).impact("OFFER-A")["impacted"]
        self.assertEqual(impact["process"], ["P-Q2O"])
        self.assertEqual(impact["capability"], ["CAP-QUOTE"])

    def test_reverse_impact_from_meter(self):
        impact = Graph(fixture()).impact("METER-UNKNOWN")["impacted"]
        self.assertEqual(impact["implementation_option"], ["OPTION-MCP"])
        self.assertEqual(impact["process"], ["P-Q2O"])

    def test_rejects_dangling_edges(self):
        d = fixture()
        d["edges"][1]["target"] = "NONEXISTENT"
        with self.assertRaisesRegex(GraphError, "dangling"):
            Graph(d)

    def test_rejects_wrong_endpoint_kind(self):
        d = fixture()
        d["edges"].append({
            "id": "BAD", "source": "OPTION-MCP", "target": "CAP-QUOTE",
            "predicate": "USES_SKILL", "claim_id": "C-DEMO",
        })
        with self.assertRaisesRegex(GraphError, "endpoint kinds"):
            Graph(d)

    def test_same_name_different_product_variant(self):
        d = fixture()
        d["nodes"][7]["name"] = "Same name"
        d["nodes"][8]["name"] = "Same name"
        rows = Graph(d).resolve("CAP-QUOTE")["alternatives"]
        a = [r for r in rows if r["implementation_option_id"] == "OPTION-NATIVE"]
        b = [r for r in rows if r["implementation_option_id"] == "OPTION-MCP"]
        self.assertEqual({x for row in a for x in row["product_variant_ids"]}, {"VARIANT-MANAGED"})
        self.assertEqual({x for row in b for x in row["product_variant_ids"]}, {"VARIANT-CORE"})

    def test_requirement_cycle_blocks(self):
        d = fixture()
        d["edges"].append({
            "id": "CYCLE", "source": "GROUP-ADDON", "target": "GROUP-ROOT",
            "predicate": "HAS_MEMBER", "claim_id": "C-DEMO",
        })
        with self.assertRaisesRegex(GraphError, "cycle"):
            Graph(d).resolve("CAP-QUOTE")

    def test_verified_requires_precise_evidence(self):
        d = fixture()
        d["claims"][0]["evidence_status"] = "VERIFIED"
        with self.assertRaisesRegex(GraphError, "require URL"):
            Graph(d)

    def test_missing_applicability_visible(self):
        a = Graph(fixture()).resolve("CAP-QUOTE")["alternatives"]
        self.assertTrue(any("missing context region" in msg for row in a for msg in row["gaps"]))
        b = Graph(fixture()).resolve("CAP-QUOTE", {"region": "EU"})["alternatives"]
        self.assertFalse(any("missing context region" in msg for row in b for msg in row["gaps"]))
        c = Graph(fixture()).resolve("CAP-QUOTE", {"region": "US"})["alternatives"]
        self.assertTrue(any("inapplicable region" in msg for row in c for msg in row["gaps"]))

    def test_expired_claim_blocks(self):
        d = fixture()
        d["claims"][1]["effective_to"] = "2025-12-31"
        a = Graph(d).resolve("CAP-QUOTE", {"region": "EU", "as_of": "2026-11-22"})["alternatives"]
        self.assertTrue(any("outside effective period" in msg for row in a for msg in row["gaps"]))

    def test_retired_claim_not_promoted(self):
        d = fixture()
        d["claims"][1]["lifecycle_status"] = "RETIRED"
        a = Graph(d).resolve("CAP-QUOTE", {"region": "EU"})["alternatives"]
        self.assertTrue(any("retired claim" in msg for row in a for msg in row["gaps"]))

    def test_skill_without_delivers_edge_is_not_proven(self):
        d = fixture()
        d["nodes"].append({"id": "SKILL-MOCK", "kind": "functional_skill"})
        d["edges"].append({
            "id": "USE-SKILL", "source": "OPTION-MCP", "target": "SKILL-MOCK",
            "predicate": "USES_SKILL", "claim_id": "C-DEMO",
        })
        a = Graph(d).resolve("CAP-QUOTE")["alternatives"]
        self.assertTrue(any("does not have an evidenced DELIVERS" in msg for row in a for msg in row["gaps"]))

    def test_replay_is_deterministic(self):
        graph = Graph(fixture())
        a = graph.resolve("P-Q2O")
        b = graph.resolve("P-Q2O")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_unmapped_required_capability_not_dropped(self):
        d = fixture()
        d["nodes"].append({"id": "CAP-MISSING", "kind": "capability"})
        d["edges"].append({
            "id": "REQUIRED-MISSING", "source": "S-QUOTE", "target": "CAP-MISSING",
            "predicate": "REQUIRES_CAPABILITY", "claim_id": "C-DEMO",
        })
        r = Graph(d).resolve("P-Q2O")
        self.assertEqual(r["coverage"]["unmapped"], ["CAP-MISSING"])
        self.assertEqual(r["route_status"], "PARTIAL")

    def test_duplicate_inclusion_edge_does_not_duplicate_offer_candidate(self):
        d = fixture()
        d["edges"].append({
            "id": "E99", "source": "OFFER-BASE", "target": "ENT-BASE",
            "predicate": "INCLUDES", "claim_id": "C-DEMO",
        })
        a = Graph(d).resolve("CAP-QUOTE")["alternatives"]
        native = [row for row in a if row["implementation_option_id"] == "OPTION-NATIVE"]
        self.assertEqual(native[0]["providing_offer_candidates"]["ENT-BASE"], ["OFFER-BASE"])


if __name__ == "__main__":
    unittest.main()
