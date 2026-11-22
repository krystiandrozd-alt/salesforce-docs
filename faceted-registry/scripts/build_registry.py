#!/usr/bin/env python3
"""Classify every element from raw manifests under sources/ into the 7 facets.

Every facet value carries >=1 source ref {file, line, quote, kind}:
  explicit = a manifest field/line literally states it
  inferred = a keyword/structure in the manifest implies it (rule id in `rule`)
  default  = nothing contradicts it; anchored to the element's header line
Run: python3 scripts/build_registry.py
"""
import json, os, re, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
from vocab import VOCAB, FACETS, FACET_DEF, ACCESS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'sources')
_cache = {}

def L(rel):
    if rel not in _cache:
        _cache[rel] = open(os.path.join(SRC, rel), encoding='utf8', errors='replace').read().split('\n')
    return _cache[rel]

def ref(rel, line, kind, rule=None):
    q = L(rel)[line - 1].strip()[:140] if 0 < line <= len(L(rel)) else ''
    r = {'file': rel, 'line': line, 'quote': q, 'kind': kind}
    if rule: r['rule'] = rule
    return r

def frontmatter(rel):
    ls = L(rel)
    d, end = {}, 1
    if ls and ls[0].strip() == '---':
        for i in range(1, len(ls)):
            if ls[i].strip() == '---':
                end = i + 1; break
        top = None
        for i in range(1, end - 1):
            m = re.match(r'^([A-Za-z_-]+):\s*(.*)$', ls[i])
            if m:
                top = m.group(1); d[top] = (m.group(2).strip().strip('"'), i + 1); continue
            m = re.match(r'^\s+([A-Za-z_-]+):\s*(.*)$', ls[i])
            if m and top:
                d[f'{top}.{m.group(1)}'] = (m.group(2).strip().strip('"'), i + 1)
    return d, end

def first_line(rel, rx, flags=0, start=1):
    p = re.compile(rx, flags)
    for i, l in enumerate(L(rel), 1):
        if i >= start and p.search(l): return i
    return 0

def all_lines(rel, rx, flags=0, start=1):
    p = re.compile(rx, flags)
    return [i for i, l in enumerate(L(rel), 1) if i >= start and p.search(l)]

# ---------------------------------------------------------------- system patterns
SYS_PAT = {
 'crm': r'~~CRM|\bCRM\b|HubSpot|Close CRM|Zoho CRM|Pipedrive',
 'salesforce-platform': r'\bApex\b|SOQL|OmniStudio|OmniScript|Data Cloud|Data 360|Agentforce|scratch org|\b2GP\b|Salesforce org|Salesforce CLI|\bsf (org|data|project|apex)\b|Lightning Web|Vlocity|managed package',
 'email': r'~~email|Gmail|Outlook|Mailchimp inbox|\binbox\b',
 'calendar': r'~~calendar|Google Calendar|Calendly',
 'chat-messaging': r'~~chat|\bSlack\b|Microsoft Teams|RingCentral',
 'docs-storage': r'~~cloud storage|Google Drive|\bBox\b|OneDrive|SharePoint|Dropbox|Google Sheets',
 'docs-knowledge': r'~~knowledge base|\bNotion\b|Confluence|\bGuru\b|\bwiki\b',
 'project-tracker': r'~~project tracker|\bAsana\b|~~Jira|\bJira\b|linear\.app|Linear (issue|ticket|MCP)|monday\.com|ClickUp|Trello|~~task\b',
 'source-control': r'~~source control|GitHub|GitLab|pull request',
 'database': r'\bNeon\b|Postgres',
 'data-warehouse': r'~~data warehouse|Snowflake|BigQuery|Databricks|Redshift|\bHex\b',
 'analytics': r'~~product analytics|~~marketing analytics|Amplitude|Mixpanel|Pendo|Ahrefs|Similarweb|Supermetrics|Google Analytics',
 'design-tool': r'~~design tool|\bFigma\b|\bCanva\b|Adobe|Excalidraw|Mermaid',
 'finance-erp': r'~~erp|QuickBooks|\bXero\b|NetSuite|MYOB|Zoho Books|Expensify|Gusto|payroll|~~procurement|Airwallex',
 'payments-commerce': r'\bStripe\b|PayPal|\bSquare\b|Shopify|\bWix\b',
 'marketing-automation': r'~~marketing automation|Klaviyo|Mailchimp|TikTok|Outreach\.io|Outreach (sequence|MCP)',
 'sales-intelligence': r'\bApollo\b|ZoomInfo|Clay (MCP|enrich)|clay\.com|\bLusha\b|Crunchbase|Common Room',
 'call-transcripts': r'~~meeting transcription|\bGong\b|Fireflies|Otter|Granola|Zoom (call|meeting|MCP)|Plaud',
 'support-desk': r'~~support platform|~~ITSM|Intercom|Zendesk|ServiceNow|Zoho Desk|~~user feedback',
 'monitoring-incident': r'~~monitoring|~~incident management|Datadog|PagerDuty',
 'cms-content': r'\bSanity\b|Adobe Experience Manager|\bAEM\b|Contentful',
 'web-reference': r'WebFetch|WebSearch|Microsoft Learn|Context7|learn\.microsoft\.com|llms\.txt|developer\.salesforce\.com',
 'workspace-files': r'allowed-tools:.*\b(Read|Edit|Write|Glob|Grep)\b|\.(docx|xlsx|pptx)\b|\bworkspace\b|\bCLAUDE\.md\b|\bvault\b',
 'claude-runtime': r'plugin\.json|\.plugin file|SKILL\.md|scheduled task|\bsub-?agents?\b|Cowork plugin|mcp-builder|memory (file|store)',
}
SYS_RX = {k: re.compile(v, re.I if k in ('email',) else 0) for k, v in SYS_PAT.items()}
WRITE_RX = re.compile(r'\b(create|creates|update|updates|send|post|write|writes|log|logs|push|merge|deploy|publish|delete|assign|schedule|sync|commit|upsert|reply|forward|draft|drafts|append|edit|modify|move|file a|save|mark)\b', re.I)
SERVER_SYS = [  # (regex on server name/url, systems)
 (r'slack|teams|ringcentral', ['chat-messaging']), (r'hubspot|close\.com|zoho.*crm|zohocrm', ['crm']),
 (r'headless-360|salesforce', ['crm', 'salesforce-platform']), (r'monday|asana|linear|clickup|trello|atlassian|jira|zohoprojects', ['project-tracker']),
 (r'notion|guru|confluence', ['docs-knowledge']), (r'figma|canva|adobe|excalidraw|mermaid', ['design-tool']),
 (r'gmail|mailchimp inbox', ['email']), (r'calendar|calendly', ['calendar']), (r'drive|box\.com|sheets|docs', ['docs-storage']),
 (r'github', ['source-control']), (r'neon', ['database']), (r'snowflake|bigquery|databricks|hex\.tech|definite', ['data-warehouse']),
 (r'amplitude|pendo|ahrefs|similarweb|supermetrics', ['analytics']), (r'intercom|zohodesk|zendesk', ['support-desk']),
 (r'datadog|pagerduty', ['monitoring-incident']), (r'sanity|experience[_ ]manager', ['cms-content']),
 (r'apollo|zoominfo|clay|lusha|crunchbase|commonroom', ['sales-intelligence']),
 (r'gong|fireflies|otter|granola|zoom|plaud', ['call-transcripts']),
 (r'quickbooks|xero|myob|zohobooks|expensify|ramp|gusto|airwallex|docusign', ['finance-erp']),
 (r'stripe|paypal|square|shopify|wix', ['payments-commerce']), (r'klaviyo|mailchimp|outreach|tiktok', ['marketing-automation']),
 (r'microsoft365|microsoft_365', ['chat-messaging', 'email']), (r'learn\.microsoft|context7|academy|githubcopilot', ['web-reference']),
 (r'zapier', ['project-tracker']), (r'emergent', ['workspace-files']), (r'pdf', ['workspace-files']),
 (r'claude-code-remote|claude_docs', ['claude-runtime']),
]
TOOL_WRITE = re.compile(r'(create|update|delete|send|reply|forward|push|merge|run_sql|deploy|trash|share|label|apply|mark|insert|append|copy|set_|add_|remove|rotate|revoke|reset|restore|restart|start|suspend|enable|disable|provision|register|publish|write|edit|upload|respond|batch|archive|fire|interrupt|subscribe|switch|unarchive|import|redact|compress|convert|combine|split|reorder|ocr|vectorize|remove_background|fill|expand|crop|activate|migrate|invite|license|finalize|initialize|assign|resolve|request_|change_|download_design|write-api|delete-api)', re.I)

TILDE = {'chat': 'chat-messaging', 'project tracker': 'project-tracker', 'knowledge base': 'docs-knowledge', 'email': 'email',
         'cloud storage': 'docs-storage', 'crm': 'crm', 'design tool': 'design-tool', 'source control': 'source-control', 'erp': 'finance-erp',
         'calendar': 'calendar', 'support platform': 'support-desk', 'product analytics': 'analytics', 'monitoring': 'monitoring-incident',
         'data warehouse': 'data-warehouse', 'meeting transcription': 'call-transcripts', 'jira': 'project-tracker', 'itsm': 'support-desk',
         'user feedback': 'support-desk', 'procurement': 'finance-erp', 'marketing automation': 'marketing-automation',
         'marketing analytics': 'analytics', 'incident management': 'monitoring-incident'}

# ---------------------------------------------------------------- element helpers
ELEMENTS = []

def new(eid, name, typ, origin, plugin, files):
    e = {'id': eid, 'name': name, 'type_hint': typ, 'origin': origin, 'plugin': plugin, 'files': files,
         'facets': {f: [] for f in FACETS}, 'access': {}}
    ELEMENTS.append(e)
    return e

def add(e, facet, value, r):
    assert value in VOCAB[facet], (facet, value, e['id'])
    for v in e['facets'][facet]:
        if v['value'] == value:
            if all(x['line'] != r['line'] or x['file'] != r['file'] for x in v['refs']): v['refs'].append(r)
            return
    e['facets'][facet].append({'value': value, 'refs': [r]})

def set_access(e, system, level, r, note=None):
    cur = e['access'].get(system)
    rank = {'unknown': 0, 'read': 1, 'write': 2}
    if cur is None or rank[level] > rank[cur['level']]:
        e['access'][system] = {'level': level, 'ref': r, **({'note': note} if note else {})}

def plugin_harness(pdir):
    """harness values from sibling manifest dirs of a plugin"""
    out = []
    for sub, h in (('.claude-plugin', 'claude-code'), ('.codex-plugin', 'codex'), ('.cursor-plugin', 'cursor'), ('.github/plugin', 'copilot'),
                   ('.devin-plugin', 'devin'), ('.kimi-plugin', 'kimi'), ('.antigravity-plugin', 'antigravity'), ('.muse-plugin', 'muse')):
        rel = f'{pdir}/{sub}/plugin.json'
        if os.path.exists(os.path.join(SRC, rel)):
            out.append((h, ref(rel, first_line(rel, r'"name"') or 1, 'explicit', 'plugin-manifest-dir')))
    return out

PLUGIN_H = {}
def harness_for(pdir):
    if pdir not in PLUGIN_H: PLUGIN_H[pdir] = plugin_harness(pdir)
    return PLUGIN_H[pdir]

def classify_text(e, rel, start=1, allow_systems=True):
    """system/access/connection/ui from raw text of one manifest file."""
    ls = L(rel)
    fmd, fm_end = frontmatter(rel) if rel.endswith('.md') else ({}, 0)
    systems = {}
    for i, l in enumerate(ls, 1):
        if i < start: continue
        for m in re.finditer(r'~~([A-Za-z][A-Za-z ]*?)(?=[ ,.;:)\]/`*-]|$)', l):
            key = m.group(1).strip().lower()
            for k, s in TILDE.items():
                if key == k or key.startswith(k + ' ') and k in ('chat', 'email', 'project tracker', 'knowledge base', 'cloud storage'):
                    systems.setdefault(s, []).append(i)
        for s, rx in SYS_RX.items():
            if rx.search(l) and not (s in ('workspace-files',) and not rel.endswith('.md')):
                systems.setdefault(s, []).append(i)
    # tilde mentions already added; dedupe
    for s, lines_ in systems.items():
        lines_ = sorted(set(lines_))
        r = ref(rel, lines_[0], 'inferred', 'system-keyword')
        add(e, 'system', s, r)
        wl = [i for i in lines_ if WRITE_RX.search(ls[i - 1])]
        if wl: set_access(e, s, 'write', ref(rel, wl[0], 'inferred', 'write-verb-on-mention'))
        else: set_access(e, s, 'read', r)
    # connection
    fm_tools = fmd.get('allowed-tools') or fmd.get('tools')
    if fm_tools:
        t, ln = fm_tools
        if re.search(r'\bBash\b', t): add(e, 'connection', 'cli', ref(rel, ln, 'explicit', 'allowed-tools'))
        if re.search(r'WebFetch|WebSearch', t): add(e, 'connection', 'native-tool', ref(rel, ln, 'explicit', 'allowed-tools'))
        if re.search(r'\bmcp__', t): add(e, 'connection', 'mcp', ref(rel, ln, 'explicit', 'allowed-tools'))
        if re.search(r'\b(Read|Edit|Write|Glob|Grep)\b', t): add(e, 'connection', 'native-tool', ref(rel, ln, 'explicit', 'allowed-tools'))
    ln = first_line(rel, r'\bMCP\b|mcp__|~~[a-z]')
    if ln: add(e, 'connection', 'mcp', ref(rel, ln, 'inferred', 'mcp-mention'))
    ln = first_line(rel, r'^\s*(\$ )?(sf |sfdx |npx |npm |python3? |node |curl |git |bash |pip |jq )', 0) or first_line(rel, r'`(sf|npx|python3?|node|curl|git) [^`]+`')
    if ln: add(e, 'connection', 'cli', ref(rel, ln, 'inferred', 'shell-command'))
    ln = first_line(rel, r'WebFetch|WebSearch|https?://\S+\.(txt|md|html)\b')
    if ln: add(e, 'connection', 'native-tool', ref(rel, ln, 'inferred', 'web-fetch-mention'))
    # connection via the plugin's own .mcp.json when the text names a connector-backed system
    pd = e.get('plugin') and f"plugins/{e['plugin']}/.mcp.json"
    if pd and os.path.exists(os.path.join(SRC, pd)) and not any(v['value'] == 'mcp' for v in e['facets']['connection']):
        if any(s in e['facets']['system'] and False or v['value'] not in ('workspace-files', 'claude-runtime', 'web-reference', 'none', 'salesforce-platform') for v in e['facets']['system'] for s in [v['value']]):
            add(e, 'connection', 'mcp', ref(pd, first_line(pd, r'"mcpServers"') or 1, 'inferred', 'plugin-mcp-config'))
    # ui
    def ui(v, rx, rule):
        ln = first_line(rel, rx, re.I, start=max(start, fm_end + 1 if fm_end else 1))
        if ln: add(e, 'ui', v, ref(rel, ln, 'inferred', rule))
    ui('rendered-artifact', r'as an artifact|Artifact (tool|page)|(build|create|publish|render)[a-z]* (a|an|the) (\w+ )?artifact|\bHTML (page|file|template|dashboard)\b|\.html\b', 'ui-artifact')
    ui('file-deliverable', r'\.(docx|xlsx|pptx|pdf)\b|\.plugin file|\.zip\b', 'ui-file')
    ui('embedded-app', r'display_pdf|interactive (viewer|pdf)|\bMCP app\b|create_view', 'ui-embedded')
    ui('desktop-control', r'computer[- ]use|claude-in-chrome|Claude in Chrome|Claude_Browser|\bbrowser automation', 'ui-desktop')

def anchor(e, rel, line):
    return ref(rel, line, 'default', 'default-anchor')

def finish_defaults(e, anchor_ref, ui_default='chat'):
    if not e['facets']['system']:
        add(e, 'system', 'none', dict(anchor_ref, rule='no-system-evidence'))
        e['access']['none'] = {'level': 'read', 'ref': anchor_ref}
    if not e['facets']['connection']: add(e, 'connection', 'none', dict(anchor_ref, rule='no-channel-evidence'))
    if not e['facets']['ui']: add(e, 'ui', ui_default, dict(anchor_ref, rule='ui-default'))
    elif ui_default == 'chat' and not any(v['value'] == 'chat' for v in e['facets']['ui']) \
            and not any(v['value'] in ('command-menu', 'embedded-app', 'desktop-control') for v in e['facets']['ui']) is False:
        pass
    if not e['facets']['model']: add(e, 'model', 'inherit', dict(anchor_ref, rule='no-model-pin'))

# ---------------------------------------------------------------- skills / commands / agents
def plugin_dir_of(rel):
    parts = rel.split('/')
    return '/'.join(parts[:2]) if parts[0] == 'plugins' else None

def model_from(fmd, rel, e, anchor_ref):
    if 'model' in fmd:
        v, ln = fmd['model']
        key = next((m for m in ('haiku', 'sonnet', 'opus', 'fable') if m in v.lower()), None)
        add(e, 'model', key or 'inherit', ref(rel, ln, 'explicit', 'model-field'))

def build_skill(rel):
    parts = rel.split('/')
    if parts[0] == 'plugins': origin, plugin, pdir = 'plugin', parts[1], '/'.join(parts[:2])
    elif parts[0] == 'agentic-kit': origin, plugin, pdir = 'agentic-kit', 'oem-isv-advisor', 'agentic-kit'
    else: origin, plugin, pdir = 'org-skill', None, None
    fmd, end = frontmatter(rel)
    name = fmd.get('name', (parts[-2], 1))[0]
    e = new(f'skill:{plugin or origin}/{name}', name, 'skill', origin, plugin, [rel])
    nl = fmd.get('name', (None, 1))[1]
    a = anchor(e, rel, nl)
    add(e, 'type', 'skill', ref(rel, nl, 'explicit', 'name-field'))
    # trigger
    role = fmd.get('metadata.role', (None, 0))
    deleg = False
    if fmd.get('user-invocable', ('', 0))[0].lower() == 'false':
        add(e, 'trigger', 'delegated', ref(rel, fmd['user-invocable'][1], 'explicit', 'user-invocable-false')); deleg = True
    if role[0] in ('capability-router', 'focused-advisor'):
        add(e, 'trigger', 'delegated', ref(rel, role[1], 'explicit', 'router-role')); deleg = True
    if 'argument-hint' in fmd:
        add(e, 'trigger', 'user-command', ref(rel, fmd['argument-hint'][1], 'explicit', 'argument-hint'))
    if fmd.get('user-invocable', ('', 0))[0].lower() == 'true':
        add(e, 'trigger', 'user-command', ref(rel, fmd['user-invocable'][1], 'explicit', 'user-invocable-true'))
    if not deleg and 'description' in fmd:
        add(e, 'trigger', 'model-selected', ref(rel, fmd['description'][1], 'explicit', 'description-selected'))
    if not e['facets']['trigger']:
        add(e, 'trigger', 'model-selected', dict(a, rule='default-selectable'))
    # model / system / connection / ui
    model_from(fmd, rel, e, a)
    classify_text(e, rel, start=end + 1)
    # kit contract
    if origin == 'agentic-kit':
        crel = rel.replace('SKILL.md', 'references/skill-contract.json')
        if os.path.exists(os.path.join(SRC, crel)):
            e['files'].append(crel)
            add(e, 'system', 'salesforce-platform', ref(crel, first_line(crel, r'"id"') or 1, 'inferred', 'kit-contract-domain'))
            wl = first_line(crel, r'"mode":\s*"act"')
            set_access(e, 'salesforce-platform', 'write' if wl else 'read',
                       ref(crel, wl or first_line(crel, r'"mode":\s*"(ask|assess)"') or 1, 'explicit', 'contract-operation-mode'),
                       'approval-gated' if wl else None)
            ml = first_line(crel, r'mcp', re.I)
            if ml: add(e, 'connection', 'mcp', ref(crel, ml, 'inferred', 'contract-mcp'))
    # harness
    if pdir:
        for h, r in harness_for(pdir): add(e, 'harness', h, r)
    if origin == 'agentic-kit':
        pr = 'agentic-kit/profiles.json'
        for pid, hs in (('claude-app', ['claude-ai', 'claude-desktop', 'cowork']), ('cursor-local', ['cursor']), ('codex-local', ['codex'])):
            ln = first_line(pr, rf'"id": "{pid}"')
            for h in hs: add(e, 'harness', h, ref(pr, ln, 'explicit', 'adapter-profile'))
    comp = fmd.get('compatibility')
    if comp:
        for rx, h in ((r'Cowork', 'cowork'), (r'Claude Code', 'claude-code'), (r'claude\.ai', 'claude-ai'), (r'Claude Desktop', 'claude-desktop')):
            if re.search(rx, comp[0], re.I if h != 'cowork' else 0): add(e, 'harness', h, ref(rel, comp[1], 'explicit', 'compatibility'))
    ln = first_line(rel, r'\bCowork\b', start=end + 1)
    if ln and not any(v['value'] == 'cowork' for v in e['facets']['harness']): add(e, 'harness', 'cowork', ref(rel, ln, 'inferred', 'cowork-mention'))
    if not e['facets']['harness']:
        add(e, 'harness', 'claude-code', dict(a, rule='loaded-in-session'))
    finish_defaults(e, a)
    return e

def build_md(rel, kind):
    parts = rel.split('/')
    plugin, pdir = parts[1], '/'.join(parts[:2])
    fmd, end = frontmatter(rel)
    name = fmd.get('name', (os.path.splitext(parts[-1])[0], 1))[0]
    e = new(f'{kind}:{plugin}/{name}', name, kind, 'plugin', plugin, [rel])
    a = anchor(e, rel, 1)
    add(e, 'type', kind, ref(rel, 1, 'explicit', f'{kind}-path'))
    if kind == 'command':
        dl = fmd.get('description', (None, 1))[1]
        add(e, 'trigger', 'user-command', ref(rel, dl, 'explicit', 'commands-dir'))
    else:
        add(e, 'trigger', 'delegated', ref(rel, fmd.get('description', (None, 1))[1], 'explicit', 'agents-dir'))
    model_from(fmd, rel, e, a)
    classify_text(e, rel, start=end + 1)
    for h, r in harness_for(pdir): add(e, 'harness', h, r)
    finish_defaults(e, a, ui_default='chat' if kind == 'command' else 'none')
    if kind == 'agent' and not any(v['value'] == 'none' for v in e['facets']['ui']) and False: pass
    return e

# ---------------------------------------------------------------- plugins, MCP servers
def build_plugin(rel):
    pdir = rel.split('/')[1]
    base = '/'.join(rel.split('/')[:2]) if rel.startswith('plugins') else 'agentic-kit'
    plugin_json = rel
    d = json.loads('\n'.join(L(rel)))
    name = d.get('name', pdir)
    e = new(f'plugin:{name}', name, 'plugin', 'agentic-kit' if base == 'agentic-kit' else 'plugin', name, [rel])
    nl = first_line(rel, r'"name"') or 1
    a = anchor(e, rel, nl)
    add(e, 'type', 'plugin', ref(rel, nl, 'explicit', 'plugin-json'))
    for h, r in harness_for(base): add(e, 'harness', h, r)
    hk = f'{base}/hooks/hooks.json'
    if os.path.exists(os.path.join(SRC, hk)):
        add(e, 'trigger', 'event', ref(hk, first_line(hk, r'"SessionStart"|"hooks"') or 1, 'explicit', 'hooks-json')); e['files'].append(hk)
        add(e, 'connection', 'cli', ref(hk, first_line(hk, r'"command"') or 1, 'explicit', 'hook-command'))
    cm = sorted(glob.glob(os.path.join(SRC, base, 'commands', '*.md')))
    if cm:
        crel = os.path.relpath(cm[0], SRC)
        add(e, 'trigger', 'user-command', ref(crel, 1, 'explicit', 'commands-dir'))
    dl = first_line(rel, r'"description"') or nl
    add(e, 'trigger', 'model-selected', ref(rel, dl, 'inferred', 'plugin-ships-skills')) if glob.glob(os.path.join(SRC, base, '**', 'SKILL.md'), recursive=True) else None
    mcp = f'{base}/.mcp.json'
    if os.path.exists(os.path.join(SRC, mcp)):
        e['files'].append(mcp)
        add(e, 'connection', 'mcp', ref(mcp, first_line(mcp, r'"mcpServers"') or 1, 'explicit', 'mcp-json'))
        for ln_, l in enumerate(L(mcp), 1):
            m = re.match(r'^\s{4}"([^"]+)":\s*\{', l)
            if m:
                key = m.group(1)
                blob = key + ' ' + ' '.join(L(mcp)[ln_:ln_ + 4])
                for rx, ss in SERVER_SYS:
                    if re.search(rx, blob, re.I):
                        for s in ss:
                            add(e, 'system', s, ref(mcp, ln_, 'inferred', 'server-name'))
                            set_access(e, s, 'unknown', ref(mcp, ln_, 'inferred', 'server-name'))
                        break
    if not e['facets']['trigger']: add(e, 'trigger', 'model-selected', dict(a, rule='default-selectable'))
    finish_defaults(e, a, ui_default='none')
    return e

MCP_SERVERS = {}
def collect_mcp_json(rel):
    base = '/'.join(rel.split('/')[:2])
    plugin = rel.split('/')[1]
    ls = L(rel)
    for i, l in enumerate(ls, 1):
        m = re.match(r'^\s{4}"([^"]+)":\s*\{', l)
        if not m: continue
        key = m.group(1); blk = ' '.join(ls[i - 1:i + 6]); um = re.search(r'"url":\s*"([^"]*)"', blk); cm = re.search(r'"command":\s*"([^"]*)"', blk)
        url = um.group(1) if um else (cm.group(1) if cm else '')
        k = (key.lower().replace(' ', '-'), url)
        MCP_SERVERS.setdefault(k, []).append((rel, i, plugin, base, key, url))

def build_mcp_servers():
    for (kn, url), occ in sorted(MCP_SERVERS.items()):
        rel, ln, plugin, base, key, _ = occ[0]
        e = new(f'mcp:{kn}' + (f'@{re.sub(r"https?://", "", url)[:40]}' if url and False else ''), key, 'mcp-server', 'plugin', plugin, sorted({o[0] for o in occ}))
        e['url'] = url
        e['id'] = f'mcp:{kn}'
        if any(x['id'] == e['id'] for x in ELEMENTS[:-1]): e['id'] = f'mcp:{kn}:{re.sub(r"[^a-z0-9]+", "-", url.lower())[:30]}'
        a = anchor(e, rel, ln)
        add(e, 'type', 'mcp-server', ref(rel, first_line(rel, r'"mcpServers"') or ln, 'explicit', 'mcp-json'))
        add(e, 'connection', 'mcp', ref(rel, ln + 1, 'explicit', 'mcp-json-type'))
        add(e, 'trigger', 'model-selected', ref(rel, ln, 'inferred', 'tool-call'))
        blob = key + ' ' + url
        hit = False
        for rx, ss in SERVER_SYS:
            if re.search(rx, blob, re.I):
                for s in ss:
                    add(e, 'system', s, ref(rel, ln, 'inferred', 'server-name')); set_access(e, s, 'unknown', ref(rel, ln, 'inferred', 'server-name'))
                hit = True; break
        seen = set()
        for o in occ:
            for h, r in harness_for(o[3]):
                add(e, 'harness', h, r)
        e['occurrences'] = [{'file': o[0], 'line': o[1]} for o in occ]
        if not hit: add(e, 'system', 'none', dict(a, rule='server-unmapped')); e['access']['none'] = {'level': 'read', 'ref': a}
        if 'pdf' in blob.lower(): add(e, 'ui', 'embedded-app', ref(rel, ln, 'inferred', 'pdf-viewer-app'))
        finish_defaults(e, a, ui_default='none')

SESSION_SERVERS = [
 ('Adobe', ['design-tool', 'docs-storage']), ('Adobe_Experience_Manager', ['cms-content']), ('Claude_Academy', ['web-reference']),
 ('Claude_Docs', ['docs-knowledge']), ('Context7', ['web-reference']), ('Excalidraw', ['design-tool']), ('Gmail', ['email']),
 ('Google_Calendar', ['calendar']), ('Google_Drive', ['docs-storage']), ('Google_Sheets', ['docs-storage']), ('Mermaid_Chart', ['design-tool']),
 ('Microsoft_365', ['chat-messaging']), ('Microsoft_Learn', ['web-reference']), ('Neon', ['database']), ('PDF_Viewer', ['workspace-files']),
 ('Plaud', ['call-transcripts']), ('Salesforce', ['crm']), ('github', ['source-control']), ('claude-code-remote', ['claude-runtime']),
 ('plugin_pdf-viewer_pdf', ['workspace-files']),
]

def build_session_servers():
    rel = 'session/mcp-tools.txt'
    ls = L(rel)
    for srv, systems in SESSION_SERVERS:
        tools = [(i, l.strip()) for i, l in enumerate(ls, 1) if l.startswith(f'mcp__{srv}__')]
        e = new(f'connector:{srv}', srv, 'mcp-server', 'session', None, [rel])
        e['tool_count'] = len(tools)
        a = anchor(e, rel, tools[0][0])
        add(e, 'type', 'mcp-server', ref(rel, tools[0][0], 'explicit', 'tool-registry'))
        add(e, 'connection', 'mcp', ref(rel, tools[0][0], 'explicit', 'tool-registry'))
        add(e, 'trigger', 'model-selected', ref(rel, tools[0][0], 'inferred', 'tool-call'))
        wt = next(((i, t) for i, t in tools if TOOL_WRITE.search(t.split('__', 2)[2])), None)
        for s in systems:
            add(e, 'system', s, ref(rel, tools[0][0], 'inferred', 'server-name'))
            if wt: set_access(e, s, 'write', ref(rel, wt[0], 'inferred', 'tool-verb'))
            else: set_access(e, s, 'read', ref(rel, tools[0][0], 'inferred', 'tool-verb'))
        ui = next(((i, t) for i, t in tools if re.search(r'display_pdf|create_view|interactive|pdf_viewer|render_mermaid|render_layout', t)), None)
        if ui: add(e, 'ui', 'embedded-app', ref(rel, ui[0], 'inferred', 'viewer-tool'))
        if srv == 'plugin_pdf-viewer_pdf':
            for h, r in harness_for('plugins/pdf-viewer'): add(e, 'harness', h, r)
        else:
            add(e, 'harness', 'claude-code', ref(rel, 2, 'explicit', 'session-registry'))
            add(e, 'harness', 'claude-ai', ref(rel, 2, 'explicit', 'claude-ai-connector'))
        finish_defaults(e, a, ui_default='none')

# ---------------------------------------------------------------- scheduled tasks, hooks
def build_tasks():
    rel = 'session/scheduled-tasks.json'
    data = json.loads('\n'.join(L(rel)))['tasks']
    for t in data:
        idl = first_line(rel, re.escape(t['id']))
        blk_end = idl + 12
        e = new(f"task:{t['id']}", t['name'], 'scheduled-task', 'session', None, [rel])
        e['enabled'] = t['enabled']
        a = anchor(e, rel, idl)
        add(e, 'type', 'scheduled-task', ref(rel, idl, 'explicit', 'trigger-record'))
        tl = first_line(rel, r'"(cron_expression|run_once_at)": "[^"]+"', start=idl)
        add(e, 'trigger', 'time', ref(rel, tl, 'explicit', 'cron-or-run-once'))
        add(e, 'harness', 'claude-code', ref(rel, 2 if False else 1, 'explicit', 'scheduled-task-runs-in-session'))
        ml = first_line(rel, r'"model":', start=idl)
        m = t['model'].lower()
        add(e, 'model', next((k for k in ('haiku', 'sonnet', 'opus', 'fable') if k in m), 'inherit'), ref(rel, ml, 'explicit' if m else 'default', 'model-field' if m else 'no-model-pin'))
        pl = first_line(rel, r'"prompt":', start=idl)
        add(e, 'ui', 'none', dict(a, rule='headless-run'))
        mcp = 'session/mcp-tools.txt'
        if t['connectors']:
            cl = first_line(rel, r'"connectors"', start=idl)
            add(e, 'connection', 'mcp', ref(rel, cl, 'explicit', 'connectors-grant'))
            for c in t['connectors']:
                srv = next(s for s in SESSION_SERVERS if s[0] == c)
                tools = [(i, l.strip()) for i, l in enumerate(L(mcp), 1) if l.startswith(f'mcp__{c}__')]
                wt = next(((i, x) for i, x in tools if TOOL_WRITE.search(x.split('__', 2)[2])), None)
                for s in srv[1]:
                    add(e, 'system', s, ref(rel, cl, 'explicit', 'connectors-grant'))
                    if wt: set_access(e, s, 'write', ref(mcp, wt[0], 'inferred', 'granted-tool-verb'), 'capability: unrestricted connector grant exposes write tools; prompt intent is read-only')
                    else: set_access(e, s, 'read', ref(rel, cl, 'explicit', 'connectors-grant'))
        prompt_lines = [pl + k for k in range(len(t['prompt'].split('\n')))]
        # prompt text may be on one json line (escaped); search the line of the prompt itself
        ptxt = L(rel)[pl - 1]
        if re.search(r'tmf-workbench|salesforce-docs|\bCI\b|\bPR\b|merge', ptxt):
            add(e, 'system', 'source-control', ref(rel, pl, 'inferred', 'prompt-repo-ci'))
            if re.search(r'\bmerge\b', ptxt, re.I):
                set_access(e, 'source-control', 'write', ref(rel, pl, 'inferred', 'prompt-merge-verb'))
            else:
                set_access(e, 'source-control', 'read', ref(rel, pl, 'inferred', 'prompt-recheck'))
        if not e['facets']['connection']:
            add(e, 'connection', 'none', dict(a, rule='no-declared-connection'))
            e['notes'] = 'Task declares no connector; the acting capability comes from the bound session.'
        finish_defaults(e, a, ui_default='none')

def build_hooks():
    rel = 'plugins/superpowers/hooks/hooks.json'
    e = new('hook:superpowers/SessionStart', 'superpowers SessionStart', 'hook', 'plugin', 'superpowers', [rel])
    a = anchor(e, rel, 1)
    add(e, 'type', 'hook', ref(rel, first_line(rel, r'"hooks"'), 'explicit', 'hooks-json'))
    add(e, 'trigger', 'event', ref(rel, first_line(rel, r'"SessionStart"'), 'explicit', 'hook-event'))
    add(e, 'connection', 'cli', ref(rel, first_line(rel, r'"command"'), 'explicit', 'hook-command'))
    for h, r in harness_for('plugins/superpowers'): add(e, 'harness', h, r)
    finish_defaults(e, a, ui_default='none')
    for f, ev_rx in (('session/hooks/stop-hook-git-check.sh', r'git '), ('session/hooks/user-prompt-submit-reply-reminder.py', r'UserPromptSubmit')):
        e = new(f'hook:session/{os.path.basename(f)}', os.path.basename(f), 'hook', 'session', None, [f])
        a = anchor(e, f, 1)
        add(e, 'type', 'hook', ref(f, 1, 'explicit', 'hook-file'))
        evl = first_line(f, r'UserPromptSubmit|\bStop\b|stop_hook_active|"hook_event_name"') or 1
        add(e, 'trigger', 'event', ref(f, evl, 'explicit' if evl > 1 else 'inferred', 'hook-event'))
        add(e, 'connection', 'cli', ref(f, 1, 'explicit', 'shebang'))
        add(e, 'harness', 'claude-code', dict(a, rule='session-hook-claude-code'))
        gl = first_line(f, r'\bgit\b')
        if gl and f.endswith('.sh'):
            add(e, 'system', 'source-control', ref(f, gl, 'inferred', 'git-command'))
            wl = first_line(f, r'^(?!\s*(#|echo)).*\bgit (push|commit|merge(?!-base)|reset|checkout|add)\b')
            set_access(e, 'source-control', 'write' if wl else 'read', ref(f, wl or gl, 'inferred', 'git-verb'))
        finish_defaults(e, a, ui_default='none')

# ---------------------------------------------------------------- main
def main():
    skills = sorted(glob.glob(os.path.join(SRC, '**', 'SKILL.md'), recursive=True))
    plugin_jsons = []
    for p in sorted(glob.glob(os.path.join(SRC, '**', '.claude-plugin', 'plugin.json'), recursive=True)):
        plugin_jsons.append(os.path.relpath(p, SRC))
    # org skills first so same-named plugin skills are separate ids
    for p in skills: build_skill(os.path.relpath(p, SRC))
    for p in sorted(glob.glob(os.path.join(SRC, 'plugins', '*', 'commands', '*.md'))): build_md(os.path.relpath(p, SRC), 'command')
    for p in sorted(glob.glob(os.path.join(SRC, 'plugins', '*', 'agents', '*.md'))): build_md(os.path.relpath(p, SRC), 'agent')
    for rel in plugin_jsons: build_plugin(rel)
    for p in sorted(glob.glob(os.path.join(SRC, 'plugins', '*', '.mcp.json'))): collect_mcp_json(os.path.relpath(p, SRC))
    build_mcp_servers(); build_session_servers(); build_tasks(); build_hooks()
    # commands with a same-named skill in the same plugin also give that skill a user-command trigger
    by = {(e['plugin'], e['name']): e for e in ELEMENTS if e['type_hint'] == 'skill'}
    for e in ELEMENTS:
        if e['type_hint'] == 'command' and (e['plugin'], e['name']) in by:
            s = by[(e['plugin'], e['name'])]
            add(s, 'trigger', 'user-command', ref(e['files'][0], 1, 'explicit', 'sibling-command-file'))
    # drop skills' chat default when they are command-menu only? keep: chat is conversational output
    for e in ELEMENTS:
        e['type'] = e.pop('type_hint')
        e['facets'] = {f: sorted(v, key=lambda x: x['value']) for f, v in e['facets'].items()}
    reg = {'schema': 'faceted-registry/1', 'generated_from': 'sources/', 'facets': FACETS, 'count': len(ELEMENTS), 'elements': ELEMENTS}
    json.dump(reg, open(os.path.join(ROOT, 'registry.json'), 'w'), indent=1, ensure_ascii=False)
    voc = {'schema': 'faceted-registry-vocab/1', 'facets': {f: {'definition': FACET_DEF[f][0], 'pmest': FACET_DEF[f][1],
           'values': [{'value': k, 'definition': d} for k, d in VOCAB[f].items()]} for f in FACETS}, 'access_levels': ACCESS}
    json.dump(voc, open(os.path.join(ROOT, 'vocabulary.json'), 'w'), indent=1, ensure_ascii=False)
    # validation
    bad = 0
    ids = set()
    for e in ELEMENTS:
        assert e['id'] not in ids, e['id']; ids.add(e['id'])
        for f in FACETS:
            if not e['facets'][f]: print('EMPTY', e['id'], f); bad += 1
            for v in e['facets'][f]:
                if v['value'] not in VOCAB[f]: print('NOT IN VOCAB', e['id'], f, v['value']); bad += 1
                for r in v['refs']:
                    if not os.path.exists(os.path.join(SRC, r['file'])) or not (0 < r['line'] <= len(L(r['file']))): print('BAD REF', e['id'], f, r); bad += 1
    print('elements', len(ELEMENTS), 'problems', bad)

if __name__ == '__main__':
    main()
