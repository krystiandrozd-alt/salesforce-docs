"""Local integrity checks for Claude project skill metadata and agent I/O references."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'pricing-intelligence'
SKILLS = ROOT / '.claude' / 'skills'
EXPECTED = ('sf-pricing-research', 'sf-license-compare', 'sf-flex-credit-estimate',
            'sf-pricing-audit', 'sf-pricing-agentforce-bridge')

class AgentContractTests(unittest.TestCase):
    def test_all_five_project_skills_have_frontmatter_and_trigger(self):
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
        self.assertIn('public pricing and local calculator mode needs no salesforce cli', content)
        self.assertIn('not approval to modify', content)

if __name__ == '__main__':
    unittest.main()
