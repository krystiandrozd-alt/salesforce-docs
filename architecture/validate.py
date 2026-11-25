#!/usr/bin/env python3
"""Validate architecture/elements.json against the doc catalog, the partner kit, rules and scenarios.

Usage:
  python3 architecture/validate.py [--kit ../partner-ecosystem-agentic-kit] [--brief path/to/brief.md] [--report out.md]

Exit code 0 when every hard check passes. Warnings (unverifiable sources, overrides) do not fail.
"""
import argparse, json, os, re, sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PATH_DIMS = ["tr", "ui", "h", "c", "soa", "id", "w", "m"]
EL_DIMS = {"type": "type", "persona": "persona", "vendor": "vendor", "maturity": "maturity"}
MAT_RANK = {"GA": 0, "Unverified": 1, "Beta": 2, "Pilot": 3, "Preview / Frontier": 4, "Legacy": 5}
# Clients the hosted-MCP docs (or the kit / brief) name. Any other harness on a hosted-MCP path must be marked assumed.
DOC_MCP_CLIENTS = {"Claude apps", "ChatGPT", "Cursor / VS Code Copilot", "Agentforce Vibes", "Agentforce runtime", "Slackbot", "Copilot Studio"}
SRC_RANK = {"Doc": 0, "Kit": 1, "Up": 2, "Inf": 3, "Ext": 4}
CONFIRM_HARNESS = {"Microsoft 365 Copilot", "Copilot Studio"}  # the brief documents confirm-before-write only for Copilot


def L(v):
    return v if isinstance(v, list) else [v]


# ---------------------------------------------------------------- path finder
def path_matches(path, q):
    for k in PATH_DIMS:
        if k in q and q[k] and not set(L(path[k])) & set(q[k]):
            return False
    return True


def element_matches(el, q):
    for qk, ek in EL_DIMS.items():
        if qk in q and q[qk] and not set(L(el[ek])) & set(q[qk]):
            return False
    return True


def best_source(el):
    return min(SRC_RANK[s["label"]] for s in el["sources"])


def find(elements, q):
    """Return [(element, path)] best path per element, ranked."""
    out = []
    for el in elements:
        if not element_matches(el, q):
            continue
        hits = [p for p in el["paths"] if path_matches(p, q)]
        if hits:
            out.append((el, hits[0]))
    out.sort(key=lambda t: (MAT_RANK[t[0].get("effective", t[0]["maturity"])], best_source(t[0]), 0 if t[0].get("primary") else 1, t[0]["name"]))
    return out


# ---------------------------------------------------------------- doc index
def load_index(folder, cache={}):
    if folder in cache:
        return cache[folder]
    rows, section = {}, ""
    p = os.path.join(ROOT, folder, "index.md")
    for line in open(p, encoding="utf-8"):
        if line.startswith("## "):
            section = line[3:].strip()
        m = re.match(r"^\| (.+?) \| (https?://\S+) \|", line)
        if m and m.group(1) != "Page":
            rows.setdefault(m.group(1), (m.group(2), section))
    cache[folder] = rows
    return rows


def maturity_from(text):
    for marker, mat in (("(Pilot)", "Pilot"), ("(Developer Preview)", "Preview / Frontier"), ("(Beta)", "Beta"),
                        ("(Legacy)", "Legacy"), ("Beta)", "Beta")):
        if marker in text:
            return mat
    return None


# ---------------------------------------------------------------- checks
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", default=os.path.join(ROOT, "..", "partner-ecosystem-agentic-kit"))
    ap.add_argument("--brief")
    ap.add_argument("--report")
    a = ap.parse_args()

    data = json.load(open(os.path.join(HERE, "elements.json"), encoding="utf-8"))
    scen = json.load(open(os.path.join(HERE, "scenarios.json"), encoding="utf-8"))
    V, E = data["vocab"], data["elements"]
    ids = {e["id"] for e in E}
    errors, warns, lines = [], [], []
    stats = {"doc_ok": 0, "kit_ok": 0, "up_ok": 0, "unverified": 0}

    # 1. ids + vocab
    if len(ids) != len(E):
        errors.append("duplicate element ids")
    for e in E:
        for k, vk in (("type", "type"), ("persona", "persona"), ("vendor", "vendor"), ("maturity", "maturity")):
            for v in L(e[k]):
                if v not in V[vk]:
                    errors.append(f"{e['id']}: {k} value not in vocab: {v}")
        if not e["paths"]:
            errors.append(f"{e['id']}: no paths")
        for i, p in enumerate(e["paths"]):
            for k in PATH_DIMS:
                for v in L(p[k]):
                    if v not in V[k]:
                        errors.append(f"{e['id']} path {i}: {k} value not in vocab: {v}")
        for ref in ([e["successor"]] if e.get("successor") else []) + [b for s in e["sources"] if s["label"] == "Inf" for b in s["basis"]]:
            if ref not in ids:
                errors.append(f"{e['id']}: reference to unknown element {ref}")

    # 2. sources
    brief = open(a.brief, encoding="utf-8").read().lower() if a.brief and os.path.exists(a.brief) else None
    for e in E:
        derived = None
        for s in e["sources"]:
            lab = s["label"]
            if lab == "Doc":
                rows = load_index(s["folder"])
                if s["title"] not in rows:
                    errors.append(f"{e['id']}: Doc title not in {s['folder']}/index.md: {s['title']}")
                    continue
                s["url"] = rows[s["title"]][0]
                if "(Deprecated)" in rows[s["title"]][1]:
                    errors.append(f"{e['id']}: cites a page in a deprecated guide ({rows[s['title']][1]}): {s['title']}")
                stats["doc_ok"] += 1
                if derived is None:
                    derived = maturity_from(s["title"]) or maturity_from(rows[s["title"]][1]) or "GA"
            elif lab == "Kit":
                p = os.path.join(a.kit, s["file"])
                if not os.path.exists(p):
                    warns.append(f"{e['id']}: Kit file not found (pass --kit): {s['file']}")
                    stats["unverified"] += 1
                elif s["text"] not in open(p, encoding="utf-8").read():
                    errors.append(f"{e['id']}: Kit text '{s['text']}' not in {s['file']}")
                else:
                    stats["kit_ok"] += 1
            elif lab == "Up":
                if brief is None:
                    warns.append(f"{e['id']}: Up source not checked (no --brief)")
                    stats["unverified"] += 1
                elif s["text"].lower() not in brief:
                    errors.append(f"{e['id']}: Up text '{s['text']}' not found in brief")
                else:
                    stats["up_ok"] += 1
            elif lab == "Ext":
                stats["unverified"] += 1
        # 3. maturity derived from the first Doc anchor
        if derived and derived != e["maturity"]:
            if e.get("maturity_override"):
                warns.append(f"{e['id']}: maturity {e['maturity']} overrides doc-derived {derived} — {e['maturity_override']}")
            else:
                errors.append(f"{e['id']}: maturity {e['maturity']} but doc title/section says {derived}")
        if not any(s["label"] in ("Doc", "Kit", "Up") for s in e["sources"]):
            warns.append(f"{e['id']}: only Ext/Inf sources — verify against vendor material")
            if e["vendor"] == "Salesforce" or e["id"] == "claude-in-agentforce":
                if e["maturity"] != "Unverified":
                    errors.append(f"{e['id']}: a Salesforce-side claim with no Doc/Kit/Up source must be Unverified")

    # 4. consistency rules
    byid = {e["id"]: e for e in E}
    assumed_n = 0
    for e in E:
        eff = e["maturity"]
        for dep in e.get("depends_on", []):
            if dep not in byid:
                errors.append(f"{e['id']}: depends_on unknown {dep}"); continue
            dm = byid[dep]["maturity"]
            if MAT_RANK[dm] > MAT_RANK[eff]:
                eff = dm
        if eff != e["maturity"]:
            if e.get("maturity_override"):
                warns.append(f"{e['id']}: declared {e['maturity']} but effective {eff} via dependency — {e['maturity_override']}")
            else:
                errors.append(f"{e['id']}: declared {e['maturity']} is better than its dependency ({eff}); add a maturity_override or downgrade")
        e["effective"] = eff
    for e in E:
        if e["maturity"] == "Legacy" and not e.get("successor"):
            errors.append(f"{e['id']}: Legacy element without successor")
        for i, p in enumerate(e["paths"]):
            h, c, idv, m, ui, tr = set(p["h"]), set(p["c"]), set(p["id"]), set(p["m"]), set(p["ui"]), set(p["tr"])
            tag = f"{e['id']} path {i}"
            if "Hosted MCP (MCP Out)" in c and not (idv & {"User OAuth via ECA"}
                                                    or (h <= {"Slackbot", "Agentforce runtime"} and "Salesforce user" in idv)
                                                    or ("Commerce Cloud" in p["soa"] and "Guest / verified customer" in idv)):
                errors.append(f"{tag}: hosted MCP path must authenticate via ECA OAuth (Slackbot / Agentforce: Salesforce user; Commerce: shopper)")
            if h & {"Agentforce runtime", "Agentforce Coworker"} and h <= {"Agentforce runtime", "Agentforce Coworker", "Tableau Agent", "None (deterministic)"} \
                    and "None" not in m and "Salesforce Models API (multi-provider)" not in m:
                errors.append(f"{tag}: Agentforce harness must run on the Salesforce Models API")
            if p["w"] == "Write with confirmation" and not h <= CONFIRM_HARNESS:
                errors.append(f"{tag}: 'write with confirmation' is only documented for Microsoft 365 Copilot")
            asm = set(p.get("assumed", []))
            assumed_n += len(asm)
            for a_ in asm:
                k_, v_ = a_.split(":", 1)
                if v_ not in L(p[k_] if k_ != "w" else [p["w"]]):
                    errors.append(f"{tag}: assumed value {a_} is not on the path")
            if "Hosted MCP (MCP Out)" in c:
                for hv in h - DOC_MCP_CLIENTS:
                    if f"h:{hv}" not in asm:
                        errors.append(f"{tag}: {hv} is not a documented hosted-MCP client; mark it assumed")
            if "Local MCP server (stdio)" in c and "Developer credentials" not in idv:
                errors.append(f"{tag}: local MCP runs with developer credentials")
            if ui == {"Headless (no UI)"} and tr == {"Conversational (chat/voice)"}:
                errors.append(f"{tag}: conversational trigger needs a UI")

    # 5. cross-product sanity: every (dim, dim) pair shown in a matrix cell must come from one path — guaranteed by
    # construction, so instead report how many false cells the old tag model would have produced.
    false_cells = 0
    for e in E:
        def U(k): return {v for p in e["paths"] for v in L(p[k])}
        for d1, d2 in (("tr", "h"), ("ui", "h"), ("ui", "w"), ("tr", "ui")):
            union = set(product(U(d1), U(d2)))
            real = {(x, y) for p in e["paths"] for x in L(p[d1]) for y in L(p[d2])}
            false_cells += len(union - real)

    # 6. scenarios
    passed = failed = 0
    for s in scen["scenarios"]:
        for q in s["queries"]:
            res = find(E, q["q"])
            got = [el["id"] for el, _ in res[: q.get("k", 8)]]
            if q.get("expect_empty"):
                ok = not res
                detail = "empty" if ok else "unexpected: " + ", ".join(el["id"] for el, _ in res)
            else:
                miss = [x for x in q["expect"] if x not in got]
                ok = not miss
                detail = "top: " + ", ".join(got) if ok else f"missing {miss}; top: {', '.join(got)}"
            passed += ok
            failed += not ok
            lines.append(f"| {s['id']} | {s['name']} | {'PASS' if ok else 'FAIL'} | {detail} |")
            if not ok:
                errors.append(f"scenario {s['id']} failed: {detail}")

    total_src = sum(len(e["sources"]) for e in E)
    verified = stats["doc_ok"] + stats["kit_ok"] + stats["up_ok"]
    rep = [
        "# Element matrix — validation report", "",
        f"- Elements: **{len(E)}**, paths: **{sum(len(e['paths']) for e in E)}**",
        f"- Sources: **{verified}/{total_src}** verified (Doc {stats['doc_ok']}, Kit {stats['kit_ok']}, Up {stats['up_ok']}); {stats['unverified']} unverifiable (Ext, or file not supplied)",
        f"- False matrix cells avoided by the path model (vs. independent tags): **{false_cells}**",
        f"- Path values marked as assumptions (not in any source): **{assumed_n}**",
        f"- Scenario queries: **{passed} passed, {failed} failed**",
        f"- Hard errors: **{len(errors)}**, warnings: **{len(warns)}**", "",
        "## Scenarios", "", "| ID | Scenario | Result | Detail |", "|---|---|---|---|", *lines, "",
        "## Errors", "", *(f"- {x}" for x in errors or ["none"]), "",
        "## Warnings", "", *(f"- {x}" for x in warns or ["none"]), "",
    ]
    text = "\n".join(rep)
    print(text)
    if a.report:
        open(a.report, "w", encoding="utf-8").write(text)
    # write resolved URLs back for the page build
    json.dump(data, open(os.path.join(HERE, "elements.resolved.json"), "w", encoding="utf-8"), ensure_ascii=False)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
