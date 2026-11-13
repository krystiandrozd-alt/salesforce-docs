# CLAUDE.md

This repo is a catalog of official Salesforce developer documentation: ~58k page
links in 54 area folders (`<area>/index.md`), built from
`https://developer.salesforce.com/docs/llms.txt`. It holds links, not page text.

## Answering Salesforce questions

Use the `salesforce-docs` skill (`.claude/skills/salesforce-docs/SKILL.md`):

```bash
python3 scripts/sfdocs.py search "<query>" --area <folder>   # find the page
python3 scripts/sfdocs.py fetch <url>                       # read it as Markdown
```

If the `salesforce-docs` MCP server is connected (tools `search_docs`, `fetch_page`,
`list_areas`, `list_sections`), use those tools instead of the CLI; same functions.

Cite the URL for every claim. Never state a Salesforce object, field, API, TMF API
number or release name that a fetched page did not confirm.

## Maintaining the catalog

- `python3 scripts/refresh_from_llms.py` regenerates every `index.md`, the content
  list and README counts; hand-written `content.md` prose is kept.
- Do not edit `index.md` files by hand; they are generated.
- `.cache/` holds fetched pages and is git-ignored.
- `scripts/sfdocs_mcp.py` is the MCP server (stdlib only) and imports `scripts/sfdocs.py`;
  keep the CLI and the server on the same functions (`search`, `fetch`, `areas`, `sections`).
