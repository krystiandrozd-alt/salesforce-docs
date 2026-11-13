# Finding Salesforce documentation

This repository is a **page-title and URL catalog with short syntheses**. A result
identifies where to read; it does not establish the behavior described by a page.
Fetch the linked official documentation before answering an implementation question.
The existing catalog records its last source refresh as **2026-11-06**. Rebuilding
search copies does not refresh Salesforce content or change that date.

## Choose the source and then the query

| Need | Repository or area | Short search terms to try separately |
|---|---|---|
| Headless Experience Layer, HXL, agent UI, widgets | This repo's `headless-experience-layer/`; deeper synthesis in `krystiandrozd-alt/headless-toolkit` | `HXL`, `UiWidgetBundle`, `renderer.json` |
| Headless 360, hosted MCP, setup automation | `headless-three-sixty/`, `hosted-mcp-servers/`; companion `headless-toolkit` | `Headless 360`, `MCP`, exact tool name |
| Communications Cloud Managed Package, CME, Industries CPQ, EPC | `industries/` | `Cart APIs`, `OmniCPQServiceWrapper`, `assetToOrder` |
| Communications Cloud TM Forum integration APIs | `industries-integrations/` | `TM Forum`, an exact API or Apex interface name |
| Agentforce, Agent API, Models API, Agent Script | `genai/` and the relevant Agentforce product folder | `Agent Script`, `Models API`, exact operation name |
| Revenue Cloud | `revenue-cloud/` | Exact API or feature name; identify the product generation first |
| Salesforce development skills | Upstream `forcedotcom/sf-skills` | Exact capability or skill name; fetch its current file |
| Project-specific implementation | The relevant project repository | Object, class, flow, integration, or error identifier |

These are query suggestions, not proof that every alias appears in every source.
Do not equate HXL with Headless 360, or Communications Cloud on Core with the
Industries Managed Package. Keep commercial names, implementation generations,
and API versions explicit when relevant.

## GitHub connector workflow

1. Convert a question into one or two distinctive terms. For example,
   “How do I set up Headless Experience Layer widgets?” becomes `HXL`, then
   the relevant setup or metadata term. Keep the user's original question for
   interpreting results; do not submit the full sentence as a keyword query.
2. Set `repository_name` explicitly. The file-search tool accepts one repository
   or an array, so HXL can search `krystiandrozd-alt/salesforce-docs` and
   `krystiandrozd-alt/headless-toolkit` together. Start with roughly five results.
3. Use the connector's structured scope parameters. Its `search` operation
   expects plain search text, not issue/PR flags or the GitHub website's full
   advanced query syntax. Repository-name search and file-content search are
   different operations.
4. Fetch the matching file, preferably at the commit from the result, and read
   the relevant lines. If a file only contains links, follow the official link.
5. For current Salesforce behavior, verify against the live official page.
   Context7's resolved Salesforce source `/llmstxt/developer_salesforce_llms_txt`
   is another retrieval route; resolve it with that connector before use unless
   an exact library ID is provided. Verify its cited primary pages when currency matters.
6. Report the source URL or GitHub path/ref, its snapshot date when known, and
   any coverage gap. Do not claim “not documented” from a zero-result search.

Read-only tool shapes tested with this connection:

```json
{"query":"HXL","repository_name":["krystiandrozd-alt/salesforce-docs","krystiandrozd-alt/headless-toolkit"],"topn":5}
```

```json
{"repository_full_name":"krystiandrozd-alt/salesforce-docs","path":"industries/index.md","start_line":25,"end_line":45}
```

These are tool arguments, not commands to paste into GitHub's search bar.

## Empty results and large files

GitHub's [REST code-search documentation](https://docs.github.com/en/search-github/searching-on-github/searching-code)
states that only the default branch and files smaller than 384 KB are searchable.
Its [new code-search documentation](https://docs.github.com/en/search-github/github-code-search/about-github-code-search)
also describes size, line-length, and other indexing exclusions. A repository-level
“indexed” flag does not mean every file is indexed.

The catalogs are preserved intact, including their large original indexes.
`scripts/build_search_index.py` adds lossless copies for originals at least 320,000
bytes, with each copy at most 200,000 UTF-8 bytes. See
[`search-index/README.md`](search-index/README.md) and the hash/range manifest.
The normal catalog refresh rebuilds these copies. Original lines remain in order;
the copies add only source references and context headers.

This makes their size suitable for code search. It does **not** force GitHub to
index them, add a semantic search engine, or fetch the linked page bodies.
Changes on a PR branch are not searchable through default-branch code search;
after merge, indexing may take time and must be checked with real queries.

When a lookup misses:

- Try the acronym, full product name, and exact API identifier as separate queries.
- Inspect the repository tree and fetch the known index or small search part directly.
- If a large file read returns empty content, verify the expected file size and
  use `fetch_blob` with the blob SHA from the tree. This was needed for
  `product-docs/index.md` in the test below.
- Use the official documentation search when the answer depends on page text.
- For exhaustive catalog matching, a local checkout plus `rg` avoids the remote
  code-search index. This still searches titles and URLs, not absent page bodies.

## Observed connector checks — 2026-11-13

Source commit: `611321c8e836c56221c84427d065376921c890a1`.
One call per test; times are elapsed tool-call times, not a statistical benchmark
or a guarantee of end-to-end answer speed. Different routes retrieve different content.

| Test | Time | Result |
|---|---:|---|
| Full question about setting up HXL widgets, scoped to this repo | 1.0 s | No matches |
| `HXL`, same repo | 1.0 s | Three matching files |
| `HXL`, this repo plus `headless-toolkit` | 0.9 s | Six returned files, including deeper HXL synthesis |
| `Communications`, this repo | 1.4 s | Relevant summaries plus unrelated uses of the word |
| `OmniCPQServiceWrapper`, this repo | 0.7 s | No matches, despite its presence in `industries/index.md` |
| `assetToOrder`, this repo | 1.1 s | No matches, despite its presence in `industries/index.md` |
| Official-domain HXL search plus an attempted `llms.txt` open | 3.4 s | Relevant official pages; direct index opening failed |
| Context7 Salesforce source resolution | 126.8 s | Official documentation source resolved |
| Context7 HXL setup query after resolution | 2.6 s | Relevant official-source excerpts |

The two exact-identifier misses and the 606,227-byte Industries index are
consistent with GitHub's file-size restriction. They do not prove size is the
only cause of every search miss. Live before/after connector verification must
wait until the copies are on the default branch and indexed.

## Maintenance

```bash
python3 scripts/build_search_index.py
python3 scripts/build_search_index.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The builder uses the Python standard library and makes no network requests.
The existing `scripts/refresh_from_llms.py` retains its original Playwright
requirements and also invokes the builder after a successful source refresh.
