#!/usr/bin/env python3
"""Cohen's kappa between registry.json (rule classifier) and an independent blind annotator.
Unit of decision = (item, value) for every vocabulary value of a facet -> binary present/absent, pooled per facet."""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from vocab import VOCAB, FACETS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
reg = {e['id']: e for e in json.load(open(f'{R}/registry.json'))['elements']}
key = json.load(open(f'{R}/validation/blind_key.json')); lab = json.load(open(f'{R}/validation/blind_labels.json'))
def kappa(pairs):
    n = len(pairs); a = sum(1 for x, y in pairs if x == y) / n
    px = sum(x for x, _ in pairs) / n; py = sum(y for _, y in pairs) / n
    pe = px * py + (1 - px) * (1 - py)
    return (a - pe) / (1 - pe) if pe < 1 else 1.0, a
out = {'n_items': len(lab), 'facets': {}}
allp = []
disagree = collections.defaultdict(list)
for f in FACETS:
    pairs = []; exact = 0
    for it, eid in key.items():
        A = {v['value'] for v in reg[eid]['facets'][f]}; B = set(lab[it][f])
        exact += A == B
        for v in VOCAB[f]:
            pairs.append((v in A, v in B))
        for v in A ^ B: disagree[f].append((it, reg[eid]['name'], v, 'registry' if v in A else 'blind'))
    k, a = kappa(pairs); allp += pairs
    out['facets'][f] = {'kappa': round(k, 3), 'raw_agreement': round(a, 3), 'exact_set_match': round(exact / len(key), 3)}
k, a = kappa(allp); out['pooled'] = {'kappa': round(k, 3), 'raw_agreement': round(a, 3)}
out['disagreements'] = {f: v for f, v in disagree.items()}
json.dump(out, open(f'{R}/validation/kappa.json', 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('n_items', 'facets', 'pooled')}, indent=1))
for f in FACETS: print(f, len(disagree[f]), disagree[f][:14])
