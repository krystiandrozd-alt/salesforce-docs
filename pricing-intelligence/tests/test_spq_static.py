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
    def test_deployed_canonical_skills_and_audit_candidates_exist(self):
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

    def test_audit_baseline_word_counts_are_pinned_not_live_canonical(self):
        # From REPORT.md's original frozen baseline (feature branch pre-SPQ).
        baseline = 2255
        proposed = sum(words((CANDIDATES / "skills" / n / "SKILL.md").read_text(encoding="utf-8")) for n in NAMES)
        self.assertLess(proposed, baseline, "Only a word-count proxy, not observed runtime speed.")
        self.assertGreater(proposed, 0)

    def test_deployed_skills_match_reviewed_candidates_except_safety_bridges(self):
        for name in NAMES:
            live = (ROOT / ".claude/skills" / name / "SKILL.md").read_text(encoding="utf-8")
            proposal = (CANDIDATES / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertTrue(live.startswith("---\\n"))
                self.assertIn("name: " + name, live)
                if name == "sf-pricing-agentforce-bridge":
                    self.assertIn("sf config set target-org", live)
                    self.assertIn("Do not", live)
                else:
                    self.assertIn("AGENTS.md", live)
                    if name not in ("sf-pricing-research", "sf-license-compare"):
                        self.assertEqual(live, proposal)

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
