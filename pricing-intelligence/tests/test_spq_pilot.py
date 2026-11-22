"""Static SPQ pilot guards, NOT Claude Code behavioural evaluation."""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "pricing-intelligence"
SKILLS = ROOT / ".claude" / "skills"
NAMES = (
    "sf-pricing-intelligence", "sf-pricing-research", "sf-license-compare",
    "sf-flex-credit-estimate", "sf-pricing-audit", "sf-pricing-agentforce-bridge"
)
BASELINE_SHA = "6da8886c2cf2f1aecceb9270398dd98b0673b6e7"
EVALS = PROJECT / "evals/spq-pilot-20261122/paired-eval-suite.json"


def words(text):
    return len(text.split())


def baseline(path):
    result = subprocess.run(
        ["git", "show", f"{BASELINE_SHA}:{path}"],
        cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode:
        raise RuntimeError("Unable to inspect preserved Git baseline: " + result.stderr.strip())
    return result.stdout


class SPQPilotStaticTests(unittest.TestCase):
    def test_all_six_skills_have_distinct_names_and_negative_triggers(self):
        seen = set()
        for name in NAMES:
            with self.subTest(name=name):
                content = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
                match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
                self.assertIsNotNone(match, "missing YAML metadata")
                self.assertIn("name: " + name, match.group(1))
                self.assertRegex(match.group(1), r"(?m)^description: \S.*$")
                self.assertTrue(re.search(
                    r"do not use|do not trigger|not for|only when|only after",
                    match.group(1), re.I
                ), "negative invocation condition absent")
                self.assertIn("AGENTS.md", content, "missing shared policy link")
                self.assertNotIn(name, seen)
                seen.add(name)

    def test_original_skill_contents_remain_retrievable_in_git(self):
        for name in NAMES:
            path = f".claude/skills/{name}/SKILL.md"
            with self.subTest(name=name):
                self.assertTrue(baseline(path).startswith("---\n"))
                self.assertNotEqual(
                    baseline(path),
                    (ROOT / path).read_text(encoding="utf-8"),
                    "pilot must be a distinct revision"
                )

    def test_static_word_delta_is_reportable_not_quality_claim(self):
        before = sum(words(baseline(f".claude/skills/{n}/SKILL.md")) for n in NAMES)
        after = sum(words((SKILLS / n / "SKILL.md").read_text(encoding="utf-8")) for n in NAMES)
        self.assertGreater(before, after)
        print(f"SPQ STATIC ONLY: original={before} words, pilot={after} words, delta={after-before}; no model benchmark")

    def test_shared_commercial_and_safety_guards_survive(self):
        contract = (PROJECT / "AGENTS.md").read_text(encoding="utf-8").lower()
        required = ["source_verified", "conflicted", "unknown", "tba", "headless",
                    "not zero", "flex credits", "conversations", "permission",
                    "credential", "org", "not approval to modify", "not_run",
                    "do not install", "not tco"]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, contract)

    def test_build_prompt_preserves_detailed_original_acceptance(self):
        prompt = (PROJECT / "prompts/build-graph.md").read_text(encoding="utf-8")
        checklist = (PROJECT / "prompts/reference/build-graph-acceptance-v1.md").read_text(encoding="utf-8")
        self.assertIn("prompts/reference/build-graph-acceptance-v1.md", prompt)
        self.assertIn("Stage A", prompt)
        self.assertIn("Gate B", prompt)
        self.assertIn("Gate C", prompt)
        self.assertGreater(words(checklist), words(prompt))
        self.assertEqual(checklist, baseline("pricing-intelligence/prompts/build-graph.md"))

    def test_pairwise_eval_cases_are_unexecuted(self):
        p = json.loads(EVALS.read_text(encoding="utf-8"))
        self.assertEqual(len(p["cases"]), 16)
        self.assertEqual(sum(c["split"] == "holdout" for c in p["cases"]), 4)
        self.assertEqual(p["observed_baseline_runs"], 0)
        self.assertEqual(p["observed_candidate_runs"], 0)
        for case in p["cases"]:
            self.assertEqual(case["baseline"]["status"], "NOT_RUN")
            self.assertEqual(case["candidate"]["status"], "NOT_RUN")

if __name__ == "__main__":
    unittest.main()
