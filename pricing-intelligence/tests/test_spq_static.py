"""SPQ candidate checks are STATIC ONLY, not model/Claude behavioral evaluations."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPQ = ROOT / "pricing-intelligence/audits/spq-2026-11-22"
CANDIDATES = SPQ / "candidates"
NAMES = ("sf-pricing-intelligence", "sf-pricing-research", "sf-license-compare",
         "sf-flex-credit-estimate", "sf-pricing-audit", "sf-pricing-agentforce-bridge")

def words(s):
    return len(s.split())

class StaticSkillPromptQualityTests(unittest.TestCase):
    def test_originals_and_candidates_exist_without_overlay(self):
        for name in NAMES:
            with self.subTest(name=name):
                self.assertTrue((ROOT / ".claude/skills" / name / "SKILL.md").is_file())
                self.assertTrue((CANDIDATES / "skills" / name / "SKILL.md").is_file())

    def test_candidate_frontmatter_and_negative_triggers(self):
        for name in NAMES:
            with self.subTest(name=name):
                t = (CANDIDATES / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
                self.assertIsNotNone(m)
                self.assertIn("name: " + name, m.group(1))
                self.assertRegex(m.group(1).lower(), r"do not use|only when|not for|do not trigger")

    def test_candidate_text_is_smaller_proxy_only(self):
        before = sum(words((ROOT / ".claude/skills" / n / "SKILL.md").read_text(encoding="utf-8")) for n in NAMES)
        after = sum(words((CANDIDATES / "skills" / n / "SKILL.md").read_text(encoding="utf-8")) for n in NAMES)
        self.assertLess(after, before, "Token proxy does not prove runtime savings.")
        self.assertGreater(after, 0)

    def test_shared_contract_keeps_key_security_guards(self):
        txt = (CANDIDATES / "AGENTS.md").read_text(encoding="utf-8").lower()
        for term in ("unknown", "tba", "conflicted", "not zero", "auth", "authorization",
                     "source", "original currency", "read-only", "not_run", "headless"):
            with self.subTest(term=term):
                self.assertIn(term, txt)

    def test_staged_build_prompt_has_release_gates(self):
        txt = (CANDIDATES / "prompts/build-graph.md").read_text(encoding="utf-8")
        for term in ("Stage A", "Stage B", "Stage C", "Gate A", "Gate B", "Gate C",
                     "STOP", "UNKNOWN", "No customer-ready quote"):
            with self.subTest(term=term):
                self.assertIn(term.lower(), txt.lower())

    def test_eval_suite_is_unexecuted_with_holdouts(self):
        p = json.loads((SPQ / "paired-eval-suite.json").read_text(encoding="utf-8"))
        self.assertEqual(len(p["cases"]), 16)
        self.assertEqual(sum(c["split"] == "holdout" for c in p["cases"]), 4)
        self.assertEqual(p["observed_baseline_runs"], 0)
        self.assertEqual(p["observed_candidate_runs"], 0)
        for case in p["cases"]:
            self.assertEqual(case["baseline"]["status"], "NOT_RUN")
            self.assertEqual(case["candidate"]["status"], "NOT_RUN")

if __name__ == "__main__":
    unittest.main()
