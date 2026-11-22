#!/usr/bin/env python3
"""Copy raw manifests verbatim into sources/ so every source ref (file + line) stays resolvable.

Origins:
  plugins/   <- ~/.claude/plugins/synced/<org>/<plugin-dir>/   (plugin.json, .mcp.json, SKILL.md, commands, agents, hooks)
  org-skills/<- ~/.claude/skills/synced/<org>/<skill>/SKILL.md  and ~/.claude/skills/<skill>/SKILL.md
  agentic-kit/ <- partner-ecosystem-agentic-kit (SKILL.md, skill-contract.json, plugin manifests)
Files are copied byte-for-byte; line numbers in registry.json refer to these copies.
"""
import os, shutil, glob, sys
HOME = os.path.expanduser('~/.claude')
KIT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/partner-ecosystem-agentic-kit'
OUT = os.path.join(os.path.dirname(__file__), '..', 'sources')
WANT = ('SKILL.md', 'plugin.json', '.mcp.json', 'hooks.json', 'skill-contract.json')

def take(rel, src):
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)

import json
def plugin_name(d):
    for m in ('.claude-plugin/plugin.json', 'plugin.json'):
        try: return json.load(open(os.path.join(d, m)))['name']
        except Exception: pass
    return os.path.basename(d)

n = 0
for org in glob.glob(f'{HOME}/plugins/synced/*/'):
    for root, dirs, files in os.walk(org):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git')]
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, org)
            top = rel.split(os.sep)[0]
            rel = os.path.join(plugin_name(os.path.join(org, top)), *rel.split(os.sep)[1:])
            if f in WANT or (f.endswith('.md') and os.path.basename(root) in ('commands', 'agents')):
                take(os.path.join('plugins', rel), p); n += 1
for p in glob.glob(f'{HOME}/skills/synced/*/*/SKILL.md'):
    take(os.path.join('org-skills', os.path.basename(os.path.dirname(p)), 'SKILL.md'), p); n += 1
for p in glob.glob(f'{HOME}/skills/*/SKILL.md'):
    take(os.path.join('org-skills', os.path.basename(os.path.dirname(p)), 'SKILL.md'), p); n += 1
for root, dirs, files in os.walk(KIT):
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        if f in WANT:
            p = os.path.join(root, f); take(os.path.join('agentic-kit', os.path.relpath(p, KIT)), p); n += 1
for f in ('stop-hook-git-check.sh', 'user-prompt-submit-reply-reminder.py'):
    take(os.path.join('session', 'hooks', f), os.path.join(HOME, f)); n += 1
take('agentic-kit/profiles.json', os.path.join(KIT, 'adapters', 'profiles.json')); n += 1
print('copied', n)
# session/mcp-tools.txt and session/scheduled-tasks.json are captured from the live session (list_triggers / tool registry) and checked in by hand.
