"""Local integrity checks for Claude project skill metadata and agent I/O references."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'pricing-intelligence'
SKILLS = ROOT / '.claude' / 'skills'
EXPECTED = ('sf-pricing-intelligence', 'sf-pricing-research', 'sf-license-compare',
            'sf-flex-credit-estimate', 'sf-pricing-audit', 'sf-pricing-agentforce-bridge')

class AgentContractTests(unittest.TestCase):
    def test_all_six_project_skills_have_frontmatter_and_trigger(self):
        for name in EXPECTED:
            with self.subTest(skill=name):
                path = SKILLS / name / 'SKILL.md'
                self.assertTrue(path.exists(), str(path))
                content = path.read_text(encoding='utf-8')
                self.assertTrue(content.startswith('---\n'))
                match = re.match(r'---\n(.*?)\n---\n', content, flags=re.S)
                self.assertIsNotNone(match)
                self.assertIn('name: ' + name, match.group(1))
                self.assertRegex(match.group(1), r'(?m)^description: .+')

    def test_orchestrator_routes_and_blocks_unpriced_headless(self):
        content = (SKILLS / 'sf-pricing-intelligence' / 'SKILL.md').read_text(encoding='utf-8').lower()
        for required in ('sf-pricing-research', 'sf-license-compare',
                         'sf-flex-credit-estimate', 'sf-pricing-audit',
                         'sf-pricing-agentforce-bridge', 'not_run',
                         'unpriced rate', 'no explicit org authorization'):
            with self.subTest(required=required):
                self.assertIn(required.lower(), content)

    def test_cli_and_agent_docs_exist(self):
        required = ('AGENTS.md', 'CLAUDE.md', 'docs/agent-io-contract.md',
                    'schema/scenario.schema.json', 'audits/2026-11-22-agentforce-labs-llms-alignment.md')
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((PROJECT / relative).is_file())

    def test_labs_source_and_org_safety_gates_documented(self):
        content = (SKILLS / 'sf-pricing-agentforce-bridge' / 'SKILL.md').read_text(encoding='utf-8')
        for signal in ('https://labs.agentforce.com/llms.txt', 'AiAuthoringBundle',
                       'agentforce-test', '--target-org', 'Organization',
                       'not authorization', 'public Salesforce price research'):
            with self.subTest(signal=signal):
                self.assertIn(signal.lower(), content.lower())

    def test_owning_skill_does_not_require_salesforce_org_for_public_pricing(self):
        content = (PROJECT / 'AGENTS.md').read_text(encoding='utf-8').lower()
        self.assertIn('no salesforce org login', content)
        self.assertIn('connection ≠ authorization', content)
        self.assertIn('headless platform interaction', content)

    def test_upstream_sf_skills_do_not_mutate_default_org(self):
        content = (SKILLS / 'sf-pricing-agentforce-bridge' / 'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('sf config set target-org', content)
        self.assertIn('do **not** follow', content)
        self.assertIn('--target-org', content)
        self.assertIn('keep authentication json/token output private', content)

    def test_staged_build_prompt_preserves_original_acceptance_criteria(self):
        original = (PROJECT / 'prompts' / 'build-graph.md').read_text(encoding='utf-8')
        staged = (PROJECT / 'prompts' / 'build-graph-staged.md').read_text(encoding='utf-8')
        self.assertIn('Live evidence cases that MUST be tested', original)
        self.assertIn('prompts/build-graph.md', staged)
        self.assertIn('Do **not** delete its required source cases', staged)
        self.assertIn('Gate A', staged)
        self.assertIn('Gate C', staged)

    def test_research_uses_sf_docs_for_technical_not_commercial_facts(self):
        content = (SKILLS / 'sf-pricing-research' / 'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('platform-docs-get', content)
        self.assertIn('does not validate pricing pdfs', content)

if __name__ == '__main__':
    unittest.main()
