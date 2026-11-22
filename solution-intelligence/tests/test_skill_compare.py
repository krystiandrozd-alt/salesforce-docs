"""Unit tests for independent graded A/B result comparison (synthetic scores)."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skills_comparator", ROOT / "benchmarks/compare.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def suite():
    return json.loads((ROOT / "examples/skills-holdout-cases.json").read_text())


def run(pass_all=True):
    return {
        "model": "frozen-model",
        "tool_profile": "frozen-tools",
        "source_snapshot_id": "frozen-sources",
        "reviewed_by": "independent-reviewer",
        "responses": [
            {
                "case_id": item["case_id"], "artifact_ref": "artifact:" + item["case_id"],
                "review": {name: pass_all for name in module.CRITERIA},
            }
            for item in suite()["cases"]
        ],
    }


class CompareTests(unittest.TestCase):
    def test_six_holdout_cases_are_registered_and_not_pre_scored(self):
        cases = suite()
        self.assertEqual(len(cases["cases"]), 6)
        self.assertEqual(cases["status"], "NOT_EXECUTED")

    def test_full_a_b_comparison(self):
        result = module.compare(suite(), run(False), run(True))
        self.assertEqual(result["case_count"], 6)
        self.assertEqual(result["baseline_total_pass"], 0)
        self.assertEqual(result["candidate_total_pass"], 36)
        self.assertFalse(result["candidate_blocked"])

    def test_rejects_missing_case(self):
        b = run()
        b["responses"].pop()
        with self.assertRaisesRegex(module.BenchmarkError, "missing cases"):
            module.compare(suite(), b, run())

    def test_rejects_unreviewed_agent_self_rating(self):
        b = run()
        b["reviewed_by"] = "tested_agent"
        with self.assertRaisesRegex(module.BenchmarkError, "independent reviewer"):
            module.compare(suite(), b, run())

    def test_rejects_different_source_snapshot(self):
        c = run()
        c["source_snapshot_id"] = "different"
        with self.assertRaisesRegex(module.BenchmarkError, "different source"):
            module.compare(suite(), run(), c)

    def test_candidate_critical_failure_blocks_comparison(self):
        c = run()
        c["responses"][0]["review"]["no_unsupported_claims"] = False
        result = module.compare(suite(), run(), c)
        self.assertTrue(result["candidate_blocked"])
        self.assertEqual(result["cases"][0]["candidate_critical_failures"], ["no_unsupported_claims"])


if __name__ == "__main__":
    unittest.main()
