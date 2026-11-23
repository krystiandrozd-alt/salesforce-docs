import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("capability_discover", ROOT / "discover.py")
discover = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discover)


class RegistryTests(unittest.TestCase):
    def test_schema_and_seed_load(self):
        document = discover.load()
        connection = discover.connect(document)
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        for name in (
            "processes", "business_capabilities", "skill_versions", "agent_versions",
            "action_definitions", "execution_bindings", "licensing_links",
            "relationship_claims", "user_stories", "test_cases",
        ):
            self.assertIn(name, tables)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM action_definitions").fetchone()[0], 0)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM execution_bindings").fetchone()[0], 0)

    def test_acceptance_query_returns_gaps_not_invented_matches(self):
        result = discover.account_preparation()
        self.assertEqual(result["matching_skill_ids"], [])
        self.assertEqual(result["candidate_skill_ids"], ["skillver-account-context-catalog"])
        self.assertEqual(result["matching_agent_ids"], [])
        self.assertEqual(result["action_count"], 0)
        self.assertEqual(result["user_story_ids"], ["story-prepare-account"])
        self.assertEqual(result["commercial_status"], "UNKNOWN")
        self.assertEqual(result["price_status"], "UNKNOWN")
        self.assertEqual(result["execution"], "NOT_RUN")
        gap_ids = {gap["id"] for gap in result["gaps"]}
        self.assertIn("gap-claudeforce-catalog", gap_ids)
        self.assertIn("gap-copilotforce-catalog", gap_ids)

    def test_delivery_skill_is_not_an_account_preparation_action(self):
        document = discover.load()
        skill = document["skill_versions"][0]
        self.assertEqual(skill["published"], "YES")
        self.assertEqual(skill["executable"], "UNKNOWN")
        self.assertEqual(skill["entitled"], "UNKNOWN")
        self.assertEqual(skill["installed"], "UNKNOWN")
        types = {claim["relationship_type"] for claim in document["relationship_claims"]}
        self.assertNotIn("EXECUTES", types)
        self.assertIn("DELIVERY_SKILL_CONFIGURES", types)

    def test_verified_claim_requires_verified_evidence(self):
        document = json.loads((ROOT / "data" / "registry.json").read_text(encoding="utf-8"))
        document["evidence_claims"][1]["evidence_status"] = "UNKNOWN"
        with self.assertRaises(ValueError):
            discover.validate(document)

    def test_unknown_price_is_not_an_entitlement(self):
        document = discover.load()
        link = document["licensing_links"][0]
        self.assertIsNone(link["commercial_ref"])
        self.assertEqual(link["price_status"], "UNKNOWN")
        self.assertEqual(link["entitlement_status"], "UNKNOWN")

    def test_three_stories_share_one_process(self):
        document = discover.load()
        self.assertEqual(len(document["user_stories"]), 3)
        self.assertEqual({story["epic_id"] for story in document["user_stories"]}, {"epic-b2b-telecom-sales"})
        kinds = {case["kind"] for case in document["test_cases"]}
        self.assertEqual(kinds, {"FUNCTIONAL", "SECURITY"})

    def test_candidate_name_match_cannot_verify_a_relationship(self):
        document = json.loads((ROOT / "data" / "registry.json").read_text(encoding="utf-8"))
        document["relationship_claims"].append({
            "id": "rel-name-guess",
            "source_id": "skillver-sales-pipeline-configure-1.0",
            "target_id": "cap-account-preparation",
            "relationship_type": "DELIVERY_SKILL_CONFIGURES",
            "applicability": "name similarity only",
            "evidence_id": "ev-headless-unreadable",
            "verification": "VERIFIED",
            "observed_at": "2026-11-23",
        })
        with self.assertRaises(ValueError):
            discover.validate(document)


if __name__ == "__main__":
    unittest.main()
