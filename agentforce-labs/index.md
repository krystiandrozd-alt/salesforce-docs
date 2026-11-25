# Agentforce Labs -- Index

Source: [capability manifest](https://labs.agentforce.com/api/capabilities) published by Agentforce Labs (`labs.agentforce.com`). This folder is outside `developer.salesforce.com`, so `scripts/refresh_from_llms.py` skips it.

Full list extracted programmatically from the live manifest (48 entries in 8 categories; status: available 48; audience: public 48). Last refreshed 2026-11-21 by `scripts/refresh_agentforce_labs.py`. Categories are the manifest's own labels, in its order.

## Machine-readable entry points

| Entry point | URL | What it is |
|---|---|---|
| llms.txt | https://labs.agentforce.com/llms.txt | Getting-started instructions for coding agents and a short reference list |
| llms.html | https://labs.agentforce.com/llms.html | The same instructions as HTML |
| llms-full.txt | https://labs.agentforce.com/llms-full.txt | All documentation in one file |
| Capability manifest | https://labs.agentforce.com/api/capabilities | JSON list of every page, tool and experiment; the source of this index |

## GET STARTED (24 pages)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Build | https://labs.agentforce.com/docs/build | https://labs.agentforce.com/api/docs/build.md | instructions | Choose your tool. Build Agentforce agents from a visual builder, an AI-powered IDE, or a CLI agent. |
| Agentforce Builder | https://labs.agentforce.com/docs/agentforce-builder | https://labs.agentforce.com/api/docs/agentforce-builder.md | instructions | Build agents visually with Agentforce Builder |
| Agentforce Vibes | https://labs.agentforce.com/docs/agentforce-vibes | https://labs.agentforce.com/api/docs/agentforce-vibes.md | instructions | Build agents with Agentforce Vibes in Code Builder |
| Setting Up Claude Code for Agentforce | https://labs.agentforce.com/docs/claude-code | https://labs.agentforce.com/api/docs/claude-code.md | instructions | Getting Started with Claude Code |
| Agent API - Headless Communication | https://labs.agentforce.com/docs/agent-api | https://labs.agentforce.com/api/docs/agent-api.md | instructions | Control your agents programmatically via REST APIs |
| Setting Up Codex for Agentforce | https://labs.agentforce.com/docs/codex | https://labs.agentforce.com/api/docs/codex.md | instructions | Getting Started with Codex |
| Setting Up Gemini CLI for Agentforce | https://labs.agentforce.com/docs/gemini-cli | https://labs.agentforce.com/api/docs/gemini-cli.md | instructions | Getting Started with Gemini CLI |
| Setting Up Cursor for Agentforce | https://labs.agentforce.com/docs/cursor | https://labs.agentforce.com/api/docs/cursor.md | instructions | Getting Started with Cursor |
| Setting Up Windsurf for Agentforce | https://labs.agentforce.com/docs/windsurf | https://labs.agentforce.com/api/docs/windsurf.md | instructions | Getting Started with Windsurf |
| Setting Up Antigravity for Agentforce | https://labs.agentforce.com/docs/antigravity | https://labs.agentforce.com/api/docs/antigravity.md | instructions | Getting Started with Antigravity |
| LabBox | https://labs.agentforce.com/docs/org-configuration | https://labs.agentforce.com/api/docs/org-configuration.md | instructions | A pre-configured Salesforce org with Einstein, Agentforce, Data Cloud, and messaging ready to go. |
| Agent Script | https://labs.agentforce.com/docs/agent-script | https://labs.agentforce.com/api/docs/agent-script.md | instructions | The programming language for AI agents. Define exactly what your agent does — and where the AI reasons. |
| Salesforce Development Skills | https://labs.agentforce.com/docs/skills | https://labs.agentforce.com/api/docs/skills.md | instructions | Install Salesforce skills and Claude Code plugins |
| Experience Site | https://labs.agentforce.com/docs/salesforce-site | https://labs.agentforce.com/api/docs/salesforce-site.md | instructions | Connect your Agentforce Service Agent to a chat widget on your Experience Site |
| Deploy | https://labs.agentforce.com/docs/deploy | https://labs.agentforce.com/api/docs/deploy.md | instructions | Put your agent in front of customers on the web, over messaging, or via API. |
| Enhanced Chat | https://labs.agentforce.com/docs/salesforce-chat | https://labs.agentforce.com/api/docs/salesforce-chat.md | instructions | Deploy your Agentforce Service Agent as a chat widget on any website |
| WhatsApp Setup | https://labs.agentforce.com/docs/whatsapp-setup | https://labs.agentforce.com/api/docs/whatsapp-setup.md | instructions | Deploy your Agentforce Service Agent to WhatsApp for customer messaging |
| SMS Setup | https://labs.agentforce.com/docs/sms-setup | https://labs.agentforce.com/api/docs/sms-setup.md | instructions | Deploy your Agentforce Service Agent to SMS for text-based customer interactions |
| Messenger Setup | https://labs.agentforce.com/docs/messenger-setup | https://labs.agentforce.com/api/docs/messenger-setup.md | instructions | Deploy your Agentforce Service Agent to Facebook Messenger for customer conversations |
| Apple Messages Setup | https://labs.agentforce.com/docs/apple-messages-setup | https://labs.agentforce.com/api/docs/apple-messages-setup.md | instructions | Deploy your Agentforce Service Agent to Apple Messages for Business |
| LINE Setup | https://labs.agentforce.com/docs/line-setup | https://labs.agentforce.com/api/docs/line-setup.md | instructions | Deploy your Agentforce Service Agent to LINE for customer messaging |
| Custom Channel Setup (BYOC) | https://labs.agentforce.com/docs/byoc-setup | https://labs.agentforce.com/api/docs/byoc-setup.md | instructions | Deploy your Agentforce Service Agent to any messaging platform using Bring Your Own Channel |
| SF Pi | https://labs.agentforce.com/docs/sf-pi | https://labs.agentforce.com/api/docs/sf-pi.md | instructions | Use SF Pi locally or launch the Labs experiment with your selected Salesforce org. |
| Start Building | https://labs.agentforce.com/start | https://labs.agentforce.com/api/capabilities/start-building.md | browser | Use the Start Building experience in Agentforce Labs. |

## IDE Integrations (2 pages)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Connect an MCP Client to Salesforce | https://labs.agentforce.com/docs/platform-mcp | https://labs.agentforce.com/api/docs/platform-mcp.md | instructions | Connect Claude, ChatGPT, Cursor, Postman, or a custom client to a Salesforce hosted MCP server |
| Docs MCP | https://labs.agentforce.com/docs/salesforce-docs-mcp | https://labs.agentforce.com/api/docs/salesforce-docs-mcp.md | instructions | Search official Salesforce docs from your IDE. No tab-switching required. |

## Getting Started (1 page)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Agentforce Labs | https://labs.agentforce.com/docs/about | https://labs.agentforce.com/api/docs/about.md | instructions | Experimental features and upcoming capabilities from Salesforce |

## Labs (9 pages)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Feedback | https://labs.agentforce.com/docs/feedback | https://labs.agentforce.com/api/docs/feedback.md | instructions | Instructions for feedback. |
| Experiments | https://labs.agentforce.com/docs/experiments | https://labs.agentforce.com/api/docs/experiments.md | instructions | Early-access capabilities from the Agentforce team. Try what's available, see what's next. |
| Agentforce Grid MCP | https://labs.agentforce.com/docs/agentforce-grid | https://labs.agentforce.com/api/docs/agentforce-grid.md | instructions | Build and manage Agentforce Grid workbooks from Claude Code with the official @salesforce/sf-grid-mcp server. |
| Community | https://labs.agentforce.com/docs/community | https://labs.agentforce.com/api/docs/community.md | instructions | Join our Slack community to connect with fellow Agentblazers experimenting in Agentforce Labs. |
| Koa Decisions | https://labs.agentforce.com/koa-decisions | https://labs.agentforce.com/api/docs/koa-decisions.md | instructions | Turn text into decisions with Salesforce's decision model. |
| Setting up nanoRag | https://labs.agentforce.com/nanorag | https://labs.agentforce.com/api/docs/nanorag.md | instructions | Build BM25 document libraries for your Agentforce agent. |
| AgentLens Visualizer | https://labs.agentforce.com/agentlens | https://labs.agentforce.com/api/docs/agentlens-visualizer.md | instructions | Debug Agentforce traces with interactive visualizations. |
| Agentforce for Google Workspace | https://labs.agentforce.com/docs/agentforce-slides | https://labs.agentforce.com/api/docs/agentforce-slides.md | instructions | Ask your Agentforce agent questions inside Google Slides and drop the answers onto a slide. |
| Upgrade Agent | https://labs.agentforce.com/upgrade-agent | https://labs.agentforce.com/api/docs/upgrade-agent.md | instructions | Upgrade an Einstein Bot to an Agentforce Service Agent. |

## Build Agents (6 pages)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Agentforce Chat | https://labs.agentforce.com/chat | https://labs.agentforce.com/api/capabilities/chat.md | browser | Build, troubleshoot, and optimize agents. Work directly with your Salesforce org. |
| Agents | https://labs.agentforce.com/agents | https://labs.agentforce.com/api/capabilities/agents.md | browser | Create and edit Agentforce agents in a fast, lightweight editor. |
| Simulate | https://labs.agentforce.com/simulate | https://labs.agentforce.com/api/capabilities/simulate.md | browser | Simulate conversations against your agent to test its behavior before you ship. |
| Agentforce Spark | https://labs.agentforce.com/agentforce-spark | https://labs.agentforce.com/api/capabilities/agent-ideas.md | browser | Explore Agentforce use cases, create a blueprint, and start building your first agent. |
| Agentforce Voice | https://labs.agentforce.com/voice | https://labs.agentforce.com/api/capabilities/voice.md | browser | Talk to live voice agents that listen, reason, and take action. Explore demos and try a conversation right in your browser. |
| MCP Servers | https://labs.agentforce.com/mcp | https://labs.agentforce.com/api/capabilities/mcp.md | browser | Connect your agents to external tools and data via Model Context Protocol servers. |

## Research (3 pages)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| GUI Process Automation | https://www.salesforceairesearch.com/gpa | https://labs.agentforce.com/api/capabilities/gui-process-automation.md | external | GPA is the next generation of RPA, an agent that learns tasks by watching a user perform them once. |
| MCP+ | https://mcp-plus.github.io/ | https://labs.agentforce.com/api/capabilities/mcp-plus.md | external | A context optimization layer that filters MCP tool outputs down to only the relevant context, cutting inference costs. |
| SkillOrchestra | https://jiayuww.github.io/SkillOrchestra/ | https://labs.agentforce.com/api/capabilities/skill-orchestra.md | external | A skill-centric framework that routes tasks to the right agent based on competence and cost. |

## Tools & Integrations (1 page)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Voice Quality | https://labs.agentforce.com/voice-quality | https://labs.agentforce.com/api/capabilities/voice-quality.md | browser | Score a voice-agent call recording. |

## Agentforce Labs (2 pages)

| Page | Canonical page | Markdown | Type | Description |
|---|---|---|---|---|
| Home | https://labs.agentforce.com/ | https://labs.agentforce.com/api/capabilities/home.md | browser | Use the Home page in Agentforce Labs. |
| What's New | https://labs.agentforce.com/releases | https://labs.agentforce.com/api/capabilities/releases.md | browser | Use the What's New page in Agentforce Labs. |
