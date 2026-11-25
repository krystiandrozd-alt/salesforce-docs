#!/usr/bin/env python3
"""Compute MECE checks, all-pairs co-occurrence, independence tests, duplicates and the risk overlay.
Writes analysis.json (consumed by findings.md and the matrix page)."""
import json, os, re, itertools, math, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
from vocab import VOCAB, FACETS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
reg = json.load(open(os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'registry.json')))
E = reg['elements']
vals = lambda e, f: [v['value'] for v in e['facets'][f]]
N = len(E)

def cooc(fa, fb):
    m = collections.Counter()
    for e in E:
        for a in vals(e, fa):
            for b in vals(e, fb): m[(a, b)] += 1
    return m

def weighted_stats(fa, fb, E=E):
    """Normalised mutual information + Cramer's V on a contingency table where each element
    spreads weight 1 over the cross product of its values (so multi-valued elements count once)."""
    tab = collections.defaultdict(float)
    for e in E:
        A, B = vals(e, fa), vals(e, fb)
        for a in A:
            for b in B: tab[(a, b)] += 1 / (len(A) * len(B))
    ra, rb = collections.Counter(), collections.Counter()
    for (a, b), w in tab.items(): ra[a] += w; rb[b] += w
    n = sum(tab.values())
    mi = sum(w / n * math.log((w / n) / ((ra[a] / n) * (rb[b] / n))) for (a, b), w in tab.items() if w > 0)
    ha = -sum(x / n * math.log(x / n) for x in ra.values()); hb = -sum(x / n * math.log(x / n) for x in rb.values())
    nmi = mi / min(ha, hb) if min(ha, hb) > 0 else 0
    chi = sum((tab.get((a, b), 0) - ra[a] * rb[b] / n) ** 2 / (ra[a] * rb[b] / n) for a in ra for b in rb)
    k = min(len(ra), len(rb)) - 1
    v = math.sqrt(chi / (n * k)) if k > 0 else 0
    return {'nmi': round(nmi, 3), 'cramers_v': round(v, 3), 'H_a': round(ha, 3), 'H_b': round(hb, 3)}

def phi(fa, a, fb, b):
    n11 = sum(1 for e in E if a in vals(e, fa) and b in vals(e, fb))
    n1_ = sum(1 for e in E if a in vals(e, fa)); n_1 = sum(1 for e in E if b in vals(e, fb))
    n10, n01 = n1_ - n11, n_1 - n11; n00 = N - n11 - n10 - n01
    d = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    return ((n11 * n00 - n10 * n01) / d if d else 0, n11, n1_, n_1)

out = {'n': N}
# ---- facet profile + MECE
prof = {}
for f in FACETS:
    c = collections.Counter(v for e in E for v in vals(e, f))
    multi = sum(1 for e in E if len(vals(e, f)) > 1)
    defaults_only = sum(1 for e in E if all(r['kind'] == 'default' for v in e['facets'][f] for r in v['refs']))
    unused = [v for v in VOCAB[f] if c[v] == 0]
    # exclusivity: pairs of values that co-occur on the same element above jaccard .5
    overlaps = []
    for a, b in itertools.combinations(VOCAB[f], 2):
        both = sum(1 for e in E if a in vals(e, f) and b in vals(e, f))
        either = sum(1 for e in E if a in vals(e, f) or b in vals(e, f))
        if either and both / either >= 0.5 and both >= 3: overlaps.append({'a': a, 'b': b, 'jaccard': round(both / either, 2), 'n': both})
    mean_vals = sum(len(vals(e, f)) for e in E) / N
    prof[f] = {'counts': dict(c.most_common()), 'multi_valued_elements': multi, 'mean_values': round(mean_vals, 2),
               'default_only_elements': defaults_only, 'unused_values': unused, 'overlaps': overlaps,
               'entropy_bits': round(-sum(x / sum(c.values()) * math.log2(x / sum(c.values())) for x in c.values()), 2),
               'top_share': round(max(c.values()) / N, 2)}
out['facets'] = prof

# ---- all-pairs
pairs = {}
for fa, fb in itertools.combinations(FACETS, 2):
    m = cooc(fa, fb)
    cells = {f'{a}|{b}': n for (a, b), n in m.items()}
    empty = [f'{a}|{b}' for a in VOCAB[fa] for b in VOCAB[fb] if m[(a, b)] == 0]
    pairs[f'{fa}x{fb}'] = {'stats': weighted_stats(fa, fb), 'cells': cells, 'empty_cells': len(empty), 'total_cells': len(VOCAB[fa]) * len(VOCAB[fb]),
                           'max_cell': max(cells.values())}
out['pairs'] = pairs
AUTH = [e for e in E if e['type'] in ('skill', 'command', 'agent', 'plugin')]
out['authored_only'] = {'n': len(AUTH), 'pairs': {f'{a}x{b}': weighted_stats(a, b, AUTH) for a, b in itertools.combinations(FACETS, 2)}}

# ---- strongest value associations (phi) across all facet pairs
assoc = []
for fa, fb in itertools.combinations(FACETS, 2):
    for a in VOCAB[fa]:
        for b in VOCAB[fb]:
            p, n11, na, nb = phi(fa, a, fb, b)
            if n11 >= 8 and na >= 8 and nb >= 8 and abs(p) >= 0.5:
                assoc.append({'a': f'{fa}:{a}', 'b': f'{fb}:{b}', 'phi': round(p, 2), 'n11': n11, 'p_b_given_a': round(n11 / na, 2), 'p_a_given_b': round(n11 / nb, 2)})
assoc.sort(key=lambda x: -abs(x['phi']))
out['associations'] = assoc[:60]

def cond(fa, a, fb, b):
    na = sum(1 for e in E if a in vals(e, fa)); n11 = sum(1 for e in E if a in vals(e, fa) and b in vals(e, fb))
    nb = sum(1 for e in E if b in vals(e, fb))
    return {'P(b|a)': round(n11 / na, 3) if na else None, 'P(a|b)': round(n11 / nb, 3) if nb else None, 'n_a': na, 'n_b': nb, 'n_both': n11, 'base_rate_b': round(nb / N, 3)}
out['hypotheses'] = {
    'type:plugin -> connection:mcp': cond('type', 'plugin', 'connection', 'mcp'),
    'type:mcp-server -> connection:mcp': cond('type', 'mcp-server', 'connection', 'mcp'),
    'type:scheduled-task -> trigger:time': cond('type', 'scheduled-task', 'trigger', 'time'),
    'trigger:time -> type:scheduled-task': cond('trigger', 'time', 'type', 'scheduled-task'),
    'trigger:event -> type:hook': cond('trigger', 'event', 'type', 'hook'),
    'trigger:user-command -> ui:command-menu': cond('trigger', 'user-command', 'ui', 'command-menu'),
    'type:command -> trigger:user-command': cond('type', 'command', 'trigger', 'user-command'),
    'type:agent -> trigger:delegated': cond('type', 'agent', 'trigger', 'delegated'),
    'type:mcp-server -> trigger:model-selected': cond('type', 'mcp-server', 'trigger', 'model-selected'),
    'type:mcp-server -> ui:none': cond('type', 'mcp-server', 'ui', 'none'),
    'connection:mcp -> type:mcp-server': cond('connection', 'mcp', 'type', 'mcp-server'),
}

# ---- duplicates: same 7-facet signature (type excluded from matching names) + similar name tokens
def sig(e, skip=()):
    return tuple(tuple(sorted(vals(e, f))) for f in FACETS if f not in skip)
def toks(e): return set(re.split(r'[^a-z0-9]+', e['name'].lower())) - {'', 'the', 'and', 'for'}
dups = []
skills = [e for e in E if e['type'] in ('skill', 'command')]
for a, b in itertools.combinations(skills, 2):
    if a['plugin'] == b['plugin'] and a['type'] == b['type']: continue
    ta, tb = toks(a), toks(b)
    j = len(ta & tb) / len(ta | tb) if ta | tb else 0
    if j >= 0.5 and (a['name'] != b['name'] or a['plugin'] != b['plugin']) or a['name'] == b['name']:
        same = sum(1 for f in FACETS if set(vals(a, f)) == set(vals(b, f)))
        dups.append({'a': a['id'], 'b': b['id'], 'name_jaccard': round(j, 2), 'facets_identical': same, 'kind': 'same-name' if a['name'] == b['name'] else 'similar-name'})
dups.sort(key=lambda d: (-d['facets_identical'], -d['name_jaccard']))
out['duplicate_candidates'] = dups[:80]
groups = collections.defaultdict(list)
for e in E: groups[sig(e)].append(e['id'])
out['signature_groups'] = sorted([{'size': len(v), 'ids': v} for v in groups.values() if len(v) >= 6], key=lambda x: -x['size'])[:15]
out['distinct_signatures'] = len(groups)

# ---- risk overlay
risk = []
for e in E:
    unatt = [v for v in vals(e, 'trigger') if v in ('time', 'event')]
    if not unatt: continue
    for s, a in e['access'].items():
        if a['level'] in ('write', 'unknown') and s not in ('none',):
            risk.append({'id': e['id'], 'name': e['name'], 'type': e['type'], 'unattended_by': unatt, 'system': s, 'access': a['level'], 'note': a.get('note'),
                         'enabled': e.get('enabled', True), 'evidence': a['ref']})
out['risk'] = risk
out['risk_summary'] = {'unattended_elements': sum(1 for e in E if any(v in ('time', 'event') for v in vals(e, 'trigger'))),
                       'flagged_write': len({r['id'] for r in risk if r['access'] == 'write'}),
                       'flagged_unknown': len({r['id'] for r in risk if r['access'] == 'unknown'})}
# latent: elements whose text asks for a schedule but trigger is not time/event
latent = []
for e in E:
    if e['type'] in ('skill', 'command') and not any(v in ('time', 'event') for v in vals(e, 'trigger')):
        wr = [s for s, a in e['access'].items() if a['level'] == 'write']
        if wr:
            for fn in e['files'][:1]:
                p = os.path.join(ROOT, 'sources', fn)
                txt = open(p, encoding='utf8', errors='replace').read().split('\n')
                for i, l in enumerate(txt, 1):
                    if re.search(r'\b(cron|every (day|week|morning|hour)|on a schedule|scheduled task|/loop|nightly|daily at|weekly at|unattended|autonomous(ly)?)\b', l, re.I):
                        latent.append({'id': e['id'], 'write_systems': wr, 'file': fn, 'line': i, 'quote': l.strip()[:140]}); break
out['latent_unattended'] = latent[:40]

# ---- coverage quality
kinds = collections.Counter(); per_facet = {f: collections.Counter() for f in FACETS}
for e in E:
    for f in FACETS:
        for v in e['facets'][f]:
            k = 'explicit' if any(r['kind'] == 'explicit' for r in v['refs']) else ('inferred' if any(r['kind'] == 'inferred' for r in v['refs']) else 'default')
            per_facet[f][k] += 1; kinds[k] += 1
out['source_strength'] = {'overall': dict(kinds), 'per_facet': {f: dict(c) for f, c in per_facet.items()}}
out['completeness'] = {'elements_all_7_facets': sum(1 for e in E if all(e['facets'][f] for f in FACETS)),
                       'values_total': sum(len(e['facets'][f]) for e in E for f in FACETS),
                       'values_with_source': sum(1 for e in E for f in FACETS for v in e['facets'][f] if v['refs'])}
json.dump(out, open(os.path.join(ROOT, 'analysis.json' if len(sys.argv) < 3 else sys.argv[2]), 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('completeness', 'source_strength', 'risk_summary', 'hypotheses')}, indent=1))
for f in FACETS: print(f, prof[f]['top_share'], prof[f]['entropy_bits'], prof[f]['overlaps'][:4], prof[f]['unused_values'])
for k, v in sorted(pairs.items(), key=lambda kv: -kv[1]['stats']['nmi'])[:8]: print(k, v['stats'], v['empty_cells'], '/', v['total_cells'])
for a in out['associations'][:25]: print(a)
