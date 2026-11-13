#!/usr/bin/env python3
"""MCP server (stdio) over this Salesforce docs catalog.

Standard library only: no `pip install` needed. It exposes the same functions as
scripts/sfdocs.py as MCP tools:

  search_docs    rank the ~58k official page links for a query (offline)
  fetch_page     download one developer.salesforce.com page as Markdown (cached)
  list_areas     the 54 documentation areas with page counts
  list_sections  the sections inside one area

Run it from any MCP client as:  python3 /path/to/salesforce-docs/scripts/sfdocs_mcp.py
Transport: JSON-RPC 2.0, one message per line on stdin/stdout (MCP stdio transport).
Logs go to stderr only.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sfdocs  # noqa: E402

SERVER_INFO = {"name": "salesforce-docs", "title": "Salesforce Docs Catalog", "version": "1.0.0"}
PROTOCOL_VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")  # newest first

INSTRUCTIONS = """\
Official Salesforce developer documentation (developer.salesforce.com, 54 areas, ~58k pages).
Workflow: search_docs to find the exact page -> fetch_page to read it -> answer only from the
fetched text and cite the page URL for every claim. A search hit alone is not evidence.
Never state a Salesforce object, field, API, endpoint, TMF API number or release name that a
fetched page did not confirm; if a fetch fails, say the content is unverified.
Default to the latest API version unless the user names one.
Area hints: TM Forum Open APIs -> industries-integrations; Industries CPQ/EPC/Digital Commerce/
Advanced Orders -> industries; Revenue Cloud, Salesforce CPQ, Billing, Place Order -> revenue-cloud;
standard objects/fields -> platform-obj-meta-tool, platform-field-ref, product-docs;
Apex -> platform-apex; Agentforce -> genai; Data 360 -> data-cloud. help.salesforce.com is not covered."""

READ_ONLY = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}

TOOLS = [
    {
        "name": "search_docs",
        "title": "Search Salesforce docs catalog",
        "description": (
            "Rank official Salesforce developer documentation pages for a query. Matches page "
            "title, section, URL path and area; returns title, area/section and URL. Use 2-4 "
            "distinctive words (e.g. 'TMF622 product ordering', 'place order', 'StubProvider'). "
            "Then call fetch_page on the best 1-3 URLs before answering."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Words to look for."},
                "area": {"type": "string", "description": "Area folder or prefix to narrow the search, "
                         "e.g. 'revenue-cloud', 'industries-integrations', or 'industries' for all industries-*. "
                         "See list_areas."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                "require_all": {"type": "boolean", "default": False,
                                "description": "Only return pages matching every query word."},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "annotations": {**READ_ONLY, "openWorldHint": False},
    },
    {
        "name": "fetch_page",
        "title": "Fetch Salesforce doc page",
        "description": (
            "Download one official page from https://developer.salesforce.com as Markdown (legacy "
            "atlas .htm links are followed to the current page). Long pages come in windows: pass "
            "the offset given at the end of the text to read on. Links inside the page are "
            "relative; prefix https://developer.salesforce.com to fetch them."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "A https://developer.salesforce.com/docs/... URL, "
                        "usually from search_docs."},
                "offset": {"type": "integer", "minimum": 0, "default": 0,
                           "description": "Character position to start reading at."},
                "max_chars": {"type": "integer", "minimum": 1000, "maximum": 100000, "default": 20000},
                "refresh": {"type": "boolean", "default": False, "description": "Ignore the local cache."},
            },
            "required": ["url"],
            "additionalProperties": False,
        },
        "annotations": {**READ_ONLY, "openWorldHint": True},
    },
    {
        "name": "list_areas",
        "title": "List documentation areas",
        "description": "The 54 documentation areas (folder name, title, page count, description). "
                       "Use a folder name as search_docs 'area'.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {**READ_ONLY, "openWorldHint": False},
    },
    {
        "name": "list_sections",
        "title": "List sections of an area",
        "description": "The guides/sections inside one area with their page counts, to see what an area covers.",
        "inputSchema": {
            "type": "object",
            "properties": {"area": {"type": "string", "description": "Area folder name, e.g. 'revenue-cloud'."}},
            "required": ["area"],
            "additionalProperties": False,
        },
        "annotations": {**READ_ONLY, "openWorldHint": False},
    },
]


class ToolError(Exception):
    """Reported to the model as a tool result with isError=true."""


def _int(args: dict, key: str, default: int, lo: int, hi: int) -> int:
    v = args.get(key, default)
    if not isinstance(v, int) or isinstance(v, bool):
        raise ToolError(f"'{key}' must be an integer")
    return max(lo, min(hi, v))


def tool_search_docs(args: dict) -> str:
    query = args.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ToolError("'query' is required")
    area = args.get("area") or None
    try:
        res = sfdocs.search(query, area, _int(args, "limit", 10, 1, 50), bool(args.get("require_all", False)))
    except ValueError as e:
        raise ToolError(str(e))
    text = sfdocs.format_search(query, area, res)
    if res["results"]:
        text += "\n\nNext: fetch_page on the best 1-3 URLs and answer only from their text."
    return text


def tool_fetch_page(args: dict) -> str:
    url = args.get("url")
    if not isinstance(url, str) or not url.strip():
        raise ToolError("'url' is required")
    try:
        r = sfdocs.fetch(url, bool(args.get("refresh", False)))
    except sfdocs.FetchError as e:
        raise ToolError(str(e))
    chunk, note = sfdocs.page_slice(r["text"], _int(args, "offset", 0, 0, 10**9),
                                    _int(args, "max_chars", 20000, 1000, 100000))
    out = f"<!-- source: {r['url']} ({r['source']}) -->\n{chunk}"
    return out + ("\n\n" + note if note else "")


def tool_list_areas(args: dict) -> str:
    return "\n".join(f"- {a['area']} ({a['pages']} pages): {a['title']} — {a['description']}"
                     for a in sfdocs.areas())


def tool_list_sections(args: dict) -> str:
    try:
        return "\n".join(f"- {s}" for s in sfdocs.sections(str(args.get("area", ""))))
    except ValueError as e:
        raise ToolError(str(e))


HANDLERS = {
    "search_docs": tool_search_docs,
    "fetch_page": tool_fetch_page,
    "list_areas": tool_list_areas,
    "list_sections": tool_list_sections,
}


class RpcError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def handle(method: str, params: dict) -> dict:
    if method == "initialize":
        asked = params.get("protocolVersion")
        version = asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0]
        return {"protocolVersion": version, "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO, "instructions": INSTRUCTIONS}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name, args = params.get("name"), params.get("arguments") or {}
        if name not in HANDLERS:
            raise RpcError(-32602, f"unknown tool: {name}")
        if not isinstance(args, dict):
            raise RpcError(-32602, "arguments must be an object")
        try:
            return {"content": [{"type": "text", "text": HANDLERS[name](args)}], "isError": False}
        except ToolError as e:
            return {"content": [{"type": "text", "text": str(e)}], "isError": True}
    raise RpcError(-32601, f"method not found: {method}")


def send(msg: dict) -> None:
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def serve() -> int:
    sfdocs.load_entries()  # parse the catalog once, before the first request
    print(f"salesforce-docs MCP server ready ({len(sfdocs.load_entries())} pages)", file=sys.stderr)
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError as e:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"parse error: {e}"}})
            continue
        if not isinstance(msg, dict) or "method" not in msg:
            continue  # a response or junk: this server sends no requests, so ignore
        mid, is_request = msg.get("id"), "id" in msg
        try:
            result = handle(msg["method"], msg.get("params") or {})
            if is_request:
                send({"jsonrpc": "2.0", "id": mid, "result": result})
        except RpcError as e:
            if is_request:
                send({"jsonrpc": "2.0", "id": mid, "error": {"code": e.code, "message": str(e)}})
        except Exception as e:  # never crash the server on one bad call
            traceback.print_exc(file=sys.stderr)
            if is_request:
                send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": f"internal error: {e}"}})
    return 0


if __name__ == "__main__":
    sys.exit(serve())
