"""Controlled vocabulary for the 7-facet registry. Closed enums, one-line definitions, no "other".

`none` appears where a facet needs an explicit "nothing applies" value; it is a real,
defined value (mutually exclusive with the rest), not a catch-all.
"""

FACETS = ["trigger", "ui", "system", "connection", "harness", "model", "type"]

FACET_DEF = {
    "trigger": ("What causes one execution to start.", "Ranganathan: Energy"),
    "ui": ("Surface on which a human sees or steers the OUTPUT while it runs (how it is invoked is `trigger`, not `ui`).", "Ranganathan: Personality"),
    "system": ("External system of record the element reads from or writes to (access level stored per value).", "Ranganathan: Matter"),
    "connection": ("Transport the element uses to reach that system.", "Ranganathan: Matter (means)"),
    "harness": ("Agent runtime / product surface in which the element is loaded.", "Ranganathan: Space"),
    "model": ("Model the element pins; `inherit` means it runs on whatever the host session uses.", "Ranganathan: Time"),
    "type": ("Packaging kind of the element as declared by its manifest.", "Ranganathan: Personality (kind)"),
}

VOCAB = {
    "trigger": {
        "user-command": "A person starts it explicitly (slash command, argument-hint, user-invocable: true, or a commands/ file).",
        "model-selected": "The model decides to use it from its description or tool schema (autonomous selection while a person is present).",
        "delegated": "Another skill, router or agent starts it (user-invocable: false, agent file, or router-assigned advisor role).",
        "time": "A clock starts it (cron expression or one-shot run_once_at).",
        "event": "A harness or external event starts it (hook lifecycle event, webhook, PR activity).",
    },
    "ui": {
        "chat": "Result is conversational text in the transcript.",
        "rendered-artifact": "Produces a rendered page, artifact or HTML preview the person opens.",
        "file-deliverable": "Produces a document file (docx, xlsx, pptx, pdf, plugin package) as the result.",
        "embedded-app": "Draws an interactive viewer/canvas inside the host (MCP app, PDF viewer, diagram canvas).",
        "desktop-control": "Drives the person's browser or desktop (computer-use, Claude in Chrome).",
        "none": "Nothing human-facing at runtime (headless, background, tool plumbing).",
    },
    "system": {
        "crm": "Customer/pipeline records: accounts, contacts, leads, opportunities.",
        "salesforce-platform": "Salesforce org/platform metadata and runtime: Apex, flows, OmniStudio, Data Cloud, packaging.",
        "email": "Mailboxes and mail marketing inboxes (read, draft, send).",
        "calendar": "Calendars, scheduling links and availability.",
        "chat-messaging": "Team chat and messaging (Slack, Teams, RingCentral).",
        "docs-storage": "File storage and office documents (Drive, Box, Sheets, Docs, Adobe assets).",
        "docs-knowledge": "Wikis and knowledge bases (Notion, Confluence, Guru).",
        "project-tracker": "Work-item trackers (Jira, Asana, Linear, monday, ClickUp, Trello).",
        "source-control": "Git hosting and CI (GitHub repos, PRs, Actions).",
        "database": "Operational databases (Postgres/Neon) and their branches, roles and migrations.",
        "data-warehouse": "Analytical warehouses and BI query engines (Snowflake, BigQuery, Databricks, Hex).",
        "analytics": "Product, web and SEO analytics (Amplitude, Pendo, Ahrefs, Similarweb, Supermetrics).",
        "design-tool": "Design and diagram tools (Figma, Canva, Adobe, Excalidraw, Mermaid).",
        "finance-erp": "Accounting, ERP, payroll and spend (QuickBooks, Xero, Gusto, Expensify).",
        "payments-commerce": "Payments and storefronts (Stripe, PayPal, Square, Shopify, Wix).",
        "marketing-automation": "Campaign, sequence and ad execution (Klaviyo, Mailchimp, Outreach, TikTok Ads).",
        "sales-intelligence": "Prospect and company data vendors (Apollo, ZoomInfo, Clay, Lusha, Crunchbase, Common Room).",
        "call-transcripts": "Meeting and call recordings/transcripts (Gong, Fireflies, Otter, Zoom, Plaud, Granola).",
        "support-desk": "Ticketing, ITSM and customer-feedback desks (Intercom, Zendesk, Zoho Desk).",
        "monitoring-incident": "Observability and incident response (Datadog, PagerDuty).",
        "cms-content": "Content management and headless CMS (Sanity, AEM).",
        "web-reference": "Public documentation and web reference (Microsoft Learn, Context7, WebFetch targets, Academy).",
        "workspace-files": "Files and code in the working directory of the session.",
        "claude-runtime": "Claude's own configuration and runtime: sessions, scheduled tasks, environments, plugins, memory.",
        "none": "Acts on nothing outside the conversation (pure reasoning / drafting).",
    },
    "connection": {
        "mcp": "Reaches the system through an MCP server or connector.",
        "cli": "Reaches the system by shell commands or bundled scripts (sf, npx, python, git, curl).",
        "native-tool": "Uses harness built-in tools: file tools (Read/Edit/Write/Glob/Grep) and web tools (WebFetch/WebSearch).",
        "none": "No declared channel; text in, text out.",
    },
    "harness": {
        "claude-code": "Claude Code (terminal, desktop-code, cloud sessions).",
        "claude-ai": "Claude web/mobile chat.",
        "claude-desktop": "Claude desktop app chat.",
        "cowork": "Claude Cowork (desktop or remote).",
        "codex": "OpenAI Codex.",
        "cursor": "Cursor.",
        "copilot": "GitHub Copilot.",
        "devin": "Devin.",
        "kimi": "Kimi.",
        "antigravity": "Antigravity.",
        "muse": "Muse.",
    },
    "model": {
        "inherit": "Runs on the host session's model; the manifest pins none.",
        "haiku": "Pinned to a Haiku-class model.",
        "sonnet": "Pinned to a Sonnet-class model.",
        "opus": "Pinned to an Opus-class model.",
        "fable": "Pinned to a Fable-class model.",
    },
    "type": {
        "skill": "SKILL.md bundle of instructions (plus references/scripts).",
        "command": "Markdown slash-command file under commands/.",
        "agent": "Sub-agent definition under agents/ with its own model and prompt.",
        "plugin": "Distribution package declared by plugin.json that ships other elements.",
        "mcp-server": "MCP server or connector exposing tools (from .mcp.json or the session tool registry).",
        "scheduled-task": "Stored prompt fired by a schedule (routine / trigger).",
        "hook": "Shell/Python handler bound to a harness lifecycle event.",
    },
}

# Heuristic used by the classifier for tool-name -> write access (documented, not a vocabulary).
ACCESS = {
    "read": "Only read-like operations are evidenced.",
    "write": "At least one create/update/delete/send/merge-like operation is evidenced or granted.",
    "unknown": "Manifest names the system but gives no operation list.",
}
