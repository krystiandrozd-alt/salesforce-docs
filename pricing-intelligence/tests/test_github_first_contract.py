"""Static contract tests for GitHub-first candidate; not external browser/agent behavior tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "workflows" / "github-first"
RECORD = json.loads((FOLDER / "communications-cloud-eu-2026-11-22.json").read_text(encoding="utf-8"))
GUIDE = (FOLDER / "WORKFLOW.md").read_text(encoding="utf-8")
SKILL = (FOLDER / "skill-candidate" / "SKILL.md").read_text(encoding="utf-8")

class GithubFirstWorkflowStaticTests(unittest.TestCase):
    def test_branch_mismatch_is_explicit(self):
        self.assertEqual(RECORD["github"]["default_branch"], "master")
        self.assertEqual(RECORD["github"]["default_branch_price_tree_status"], "NOT_FOUND")
        self.assertTrue(RECORD["github"]["verified_pricing_branch"].startswith("feature/"))
        self.assertIn("default_branch", GUIDE)
        self.assertIn("branch discovery", SKILL.lower())

    def test_price_conflict_is_preserved(self):
        rows = {r["offer"]: r for r in RECORD["normalized_facts"]}
        for name, older, newer in [
            ("Communications Cloud Growth", "325", "300"),
            ("Communications Cloud Advanced", "475", "450"),
        ]:
            row = rows[name]
            self.assertEqual(row["historic_amount"], older)
            self.assertEqual(row["newer_indexed_amount"], newer)
            self.assertEqual(row["status"], "CONFLICTED")
            self.assertEqual(row["effective_date"], "UNKNOWN")
        self.assertEqual(RECORD["conflict"]["status"], "CONFLICTED")

    def test_distinct_edition_taxonomies(self):
        x = RECORD["source_observations"]
        old = {y["edition"] for y in next(p for p in x if p["id"]=="EU_PAGE_OLDER")["offers"]}
        new = {y["edition"] for y in next(p for p in x if p["id"]=="EU_PAGE_NEWER")["offers"]}
        self.assertIn("Agentforce 1 Sales", old)
        self.assertIn("Sales Max", new)
        self.assertNotIn("Sales Max", old)
        self.assertIn("edition taxonomy", GUIDE)

    def test_bss_org_is_not_per_user(self):
        for row in RECORD["other_observations"]:
            self.assertEqual(row["original_unit"], "ORG")
            self.assertEqual(row["display_period"], "YEAR")
            self.assertEqual(row["current_validity"], "UNKNOWN")

    def test_status_and_execution_truthfulness(self):
        self.assertEqual(RECORD["execution"]["repository_unittests"], "NOT_RUN_IN_THIS_WORKFLOW")
        self.assertEqual(RECORD["execution"]["pricing_cli"], "NOT_APPLICABLE")
        for marker in ["NOT_RUN", "CONFLICTED", "UNKNOWN", "Salesforce", "GitHub"]:
            self.assertIn(marker, SKILL)
        self.assertIn("NOT INSTALLED", SKILL)

if __name__ == "__main__":
    unittest.main()
