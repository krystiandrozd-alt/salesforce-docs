# Faceted registry

Seven-facet registry of the agent toolkit (skills, commands, agents, plugins, MCP servers, scheduled tasks, hooks), classified from raw manifests.

| File | What |
|---|---|
| `registry.json` | 496 elements, each with 7 facets; every value carries source refs `{file, line, quote, kind}` into `sources/` |
| `vocabulary.json` | Closed enums with one-line definitions (v2). `vocabulary.v1.json` / `registry.v1.json` / `analysis.v1.json` are the pre-redefinition versions |
| `findings.md` | Gaps, duplicates, risk overlay, facet-independence result, kappa |
| `analysis.json` | Co-occurrence for all 21 facet pairs, NMI, associations, duplicates, risk |
| `site/` | Matrix page (`index.html` + `data.json`). Serve it: `cd site && python3 -m http.server` |
| `sources/` | Verbatim copies of the manifests the refs point to |
| `validation/` | Blind annotator labels and Cohen's kappa |
| `scripts/` | `run_all.sh` rebuilds everything from `sources/` (`--snapshot` re-copies from a live `~/.claude`) |
