# Agentforce Labs — Content

Synthesis written independently from the source (not copied text).

Agentforce Labs (`labs.agentforce.com`) is a Salesforce site for building and testing Agentforce agents from a coding agent, against either your own org or a pre-configured "LabBox" org ([llms]). Its full documentation has getting-started guides for Claude Code, Codex, Gemini CLI, Cursor, Windsurf and Antigravity ([full]).

The site's `llms.txt` is written as instructions to a coding agent, not as a list of pages ([llms] "Getting started"). The main points:

- Work through the Salesforce CLI (`sf`) in an existing SFDX project. Name the target org explicitly and leave the user's default org unchanged.
- Install the `agentforce-generate` and `agentforce-test` skills (`npx skills add forcedotcom/sf-skills`).
- Build with Agent Script (`.agent` files) and test locally first. Deploy, publish or activate only when asked to.
- Keep credentials, device codes and tokens out of chat, logs and commits.

The optional Labs connection is a device-code approval flow ([llms] "Optional: connect through Labs"):

- The user approves the request in a browser.
- The agent polls for the result, then imports the org into the CLI.
- Labs picks the user's active LabBox, otherwise their connected own org, otherwise it provisions a new LabBox after approval.
- The response can include the org's expiry time.

**Inference:** the flow follows the OAuth 2.0 device authorization grant; it uses the same field names.

**LabBox org configuration** is covered in detail in [org-configuration.md](org-configuration.md). It lists:

- what is pre-enabled: Einstein, Agentforce, Data Cloud, Omni-Channel, Enhanced Chat, an Experience site and a default service agent;
- the permission sets;
- MCP servers, plus the prerequisites for Agentforce Coworker, Voice and Vibes;
- review notes where the page's replication scripts need correcting before reuse.

Section breakdown:
- **Reference** — 11 links
- **Full Documentation** — 2 links

*Source: [`llms.txt`][llms] and the [LabBox page](https://labs.agentforce.com/chat/docs/org-configuration), retrieved 2026-11-21.*

## Extraction notes

This folder is not part of the `developer.salesforce.com` `llms.txt` set. It is a snapshot, and `scripts/refresh_from_llms.py` skips it (it is listed in `EXTRA_SOURCES`). Only the LabBox page was reviewed in depth; for the other pages, follow the links in [index.md](index.md).

[llms]: https://labs.agentforce.com/llms.txt
[full]: https://labs.agentforce.com/llms-full.txt
