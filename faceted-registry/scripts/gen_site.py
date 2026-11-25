#!/usr/bin/env python3
"""Generate site/data.json (compact registry + vocab + lexicon + independence stats) and site/index.html."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from vocab import VOCAB, FACETS, FACET_DEF

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
reg = json.load(open(os.path.join(ROOT, 'registry.json')))
ana = json.load(open(os.path.join(ROOT, 'analysis.json')))

files, fidx = [], {}
def fi(f):
    if f not in fidx: fidx[f] = len(files); files.append(f)
    return fidx[f]

els = []
for e in reg['elements']:
    f = {}
    for fa in FACETS:
        f[fa] = [[v['value'], [[fi(r['file']), r['line'], r['kind'][0], r['quote'][:110]] for r in v['refs'][:3]]] for v in e['facets'][fa]]
    a = {s: [x['level'], fi(x['ref']['file']), x['ref']['line'], x.get('note', '')] for s, x in e['access'].items()}
    d = {'id': e['id'], 'n': e['name'], 't': e['type'], 'p': e.get('plugin') or '', 'f': f, 'a': a}
    if 'enabled' in e: d['en'] = e['enabled']
    els.append(d)

L = lambda f, v, rx: [f, v, rx]
LEX = [
 L('trigger', 'time', r'every (day|morning|evening|week|hour|month)|daily|weekly|nightly|cron|schedul|recurring|on a timer|each morning'),
 L('trigger', 'event', r'whenever|webhook|hook|on (push|commit|session start)|when (a|an|the) .{0,30}(opened|merged|arrives|created|fails)|pr activity'),
 L('trigger', 'user-command', r'slash|/[a-z-]+|on demand|when i (ask|type|run)|command'),
 L('trigger', 'model-selected', r'automatically pick|when relevant|auto-?select'),
 L('trigger', 'delegated', r'sub-?agent|delegat|route[sd]? to|hand ?off|orchestrat'),
 L('ui', 'chat', r'tell me|explain|summari[sz]e|answer|chat'),
 L('ui', 'rendered-artifact', r'dashboard|artifact|html|web ?page|visual report|interactive page'),
 L('ui', 'file-deliverable', r'docx|word doc|excel|xlsx|pptx|powerpoint|slide deck|\bpdf\b|spreadsheet'),
 L('ui', 'embedded-app', r'viewer|annotate|canvas|whiteboard'),
 L('ui', 'desktop-control', r'browser|click|screen|computer use|chrome'),
 L('ui', 'none', r'silent|in the background|headless|without me|unattended|no one watching'),
 L('system', 'crm', r'\bcrm\b|hubspot|pipeline|opportunit|\bleads?\b|\bdeals?\b|accounts?\b'),
 L('system', 'email', r'e-?mail|inbox|gmail|outlook|reply|draft'),
 L('system', 'calendar', r'calendar|meeting|availability|calendly|book a'),
 L('system', 'chat-messaging', r'slack|teams|channel|dm\b|message'),
 L('system', 'docs-storage', r'\bdrive\b|\bbox\b|sheets|file storage|share a file'),
 L('system', 'docs-knowledge', r'notion|confluence|wiki|knowledge base|guru'),
 L('system', 'project-tracker', r'jira|asana|linear|ticket|sprint|backlog|monday|clickup|task'),
 L('system', 'source-control', r'github|\brepo\b|pull request|\bprs?\b|commit|branch|\bci\b'),
 L('system', 'database', r'database|postgres|neon|migration'),
 L('system', 'data-warehouse', r'warehouse|snowflake|bigquery|databricks|sql quer'),
 L('system', 'analytics', r'analytics|amplitude|\bseo\b|traffic|funnel|pendo'),
 L('system', 'design-tool', r'figma|canva|design|diagram|mermaid|adobe'),
 L('system', 'finance-erp', r'invoice|payroll|quickbooks|xero|accounting|expense|ledger|\bbills?\b|\btax\b|\berp\b'),
 L('system', 'payments-commerce', r'stripe|paypal|shopify|payments?|checkout|storefront'),
 L('system', 'marketing-automation', r'campaign|klaviyo|mailchimp|newsletter|\bads?\b|sequence'),
 L('system', 'sales-intelligence', r'prospect|apollo|zoominfo|enrich|crunchbase|lead list'),
 L('system', 'call-transcripts', r'transcript|gong|call recording|fireflies|zoom|otter'),
 L('system', 'support-desk', r'support ticket|zendesk|intercom|helpdesk|escalation|customer support'),
 L('system', 'monitoring-incident', r'incident|pagerduty|datadog|outage|monitoring|on-?call'),
 L('system', 'cms-content', r'\bcms\b|sanity|\baem\b|content model'),
 L('system', 'web-reference', r'documentation|look ?up|api reference|microsoft learn|research'),
 L('system', 'workspace-files', r'local files?|my repo|codebase|folder|working directory'),
 L('system', 'claude-runtime', r'plugin|skill|claude\.md|memory|scheduled task|environment|session'),
 L('system', 'salesforce-platform', r'salesforce|apex|\bflows?\b|omnistudio|data cloud|agentforce|\bisv\b|\boem\b|package|\borg\b'),
 L('connection', 'mcp', r'\bmcp\b|connector|integration'),
 L('connection', 'cli', r'\bcli\b|command line|terminal|shell|\bscript'),
 L('connection', 'native-tool', r'web fetch|web search|read files|edit files'),
 L('harness', 'claude-code', r'claude code'), L('harness', 'cowork', r'cowork'), L('harness', 'codex', r'codex'),
 L('harness', 'cursor', r'cursor'), L('harness', 'copilot', r'copilot'), L('harness', 'claude-ai', r'claude\.ai|web chat'),
 L('harness', 'claude-desktop', r'desktop app'), L('harness', 'devin', r'devin'), L('harness', 'kimi', r'kimi'),
 L('harness', 'antigravity', r'antigravity'), L('harness', 'muse', r'\bmuse\b'),
 L('model', 'opus', r'opus'), L('model', 'sonnet', r'sonnet'), L('model', 'haiku', r'haiku'), L('model', 'fable', r'fable'),
 L('type', 'skill', r'\bskill\b'), L('type', 'command', r'slash command'), L('type', 'agent', r'\bagent\b'), L('type', 'plugin', r'\bplugin\b'),
 L('type', 'mcp-server', r'mcp server|connector'), L('type', 'scheduled-task', r'scheduled|routine|recurring task'), L('type', 'hook', r'\bhook\b'),
]
data = {
    'facets': FACETS,
    'facetDef': {f: FACET_DEF[f][0] for f in FACETS},
    'vocab': {f: [[k, d] for k, d in VOCAB[f].items()] for f in FACETS},
    'files': files, 'elements': els, 'lexicon': LEX,
    'nmi': {k: v['stats']['nmi'] for k, v in ana['pairs'].items()},
    'nmiAuthored': {k: v['nmi'] for k, v in ana['authored_only']['pairs'].items()},
    'ghBase': 'https://github.com/krystiandrozd-alt/salesforce-docs/blob/claude/pompy-faceted-registry-i4gdd3/faceted-registry/sources/',
}
os.makedirs(os.path.join(ROOT, 'site'), exist_ok=True)
json.dump(data, open(os.path.join(ROOT, 'site', 'data.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
print('data.json', os.path.getsize(os.path.join(ROOT, 'site', 'data.json')) // 1024, 'KB', len(els), 'elements')
