# SF Pi — Content

Synthesis for Labs and local use of SF Pi. Upstream pages are linked from [index.md](index.md); this file is not copied from Salesforce developer-portal `llms.txt` prose.

SF Pi is Salesforce's open-source extension bundle for the [Pi coding agent](https://pi.dev). It adds Salesforce-aware tools, skills, lifecycle commands, and safety surfaces for building in an org.

External hubs:
- [SF Pi on GitHub](https://github.com/salesforce/sf-pi)
- [Upstream SF Pi documentation](https://opensource.salesforce.com/sf-pi/)

## Run it in Labs

Sign in to Labs when the SF Pi experiment is available on your account. Labs runs SF Pi in a disposable remote workspace.

Before launch:
1. Choose the Salesforce org in the org switcher.
2. Select **Start SF Pi in Labs**.

Labs injects the selected org into SF Pi automatically, so you should not need `sf org login` in the remote workspace. If the initial login fails, Labs retries a provisioned Dev Box once with a fresh browser authorization. For a connected BYOO org, use the authorization card to confirm the org and authorize it explicitly.

Labs prefers a warm runner when one is available. A cold fallback still has to start a private workspace and can take about one to two minutes. Once the terminal is ready, start with:

```text
/sf-pi doctor
```

## Install locally

Requirements: Node.js 22.19 or newer, a supported Pi coding agent, and Salesforce CLI.

These commands follow the upstream latest-release installation path. `--ignore-scripts` is part of SF Pi's official Pi install command; keep it unless the upstream guide changes.

```bash
npm install --global --ignore-scripts @earendil-works/pi-coding-agent
pi install git:github.com/salesforce/sf-pi
pi
```

Install Salesforce CLI if needed, then connect the org you want to use:

```bash
npm install --global @salesforce/cli@latest
sf org login web --alias myorg --set-default
sf org list
```

Inside Pi, reload the bundle and check its setup:

```text
/reload
/sf-pi doctor
/sf-skills defaults install global
```

Optional companion packages install only when you ask for them. For the current recommended bundle:

```text
/sf-pi recommended install bundle:default
/sf-pi recommended status
```

## Troubleshoot

Run `/sf-pi doctor` first. It checks local prerequisites, enabled extensions, and supported tooling. For installation options, platform notes, and the extension catalog, use the [upstream SF Pi documentation](https://opensource.salesforce.com/sf-pi/). For bugs or contribution guidance, use the [SF Pi GitHub repository](https://github.com/salesforce/sf-pi).

## Section breakdown

Guide and reference pages from the published SF Pi site (ADRs omitted from the catalog index):

- **Getting started** — Home, Install, Quickstart, Agent Orientation
- **References** — Extensions catalog, Commands, Settings Surfaces, Troubleshooting
- **Trust and contribution** — Privacy, Security Model, Secure Development, Public Sanitization, Contributing
- **Extensions** — Agent Script, Apex, Browser, Code Analyzer, Data 360, Guardrail, MCP, Slack, Skills, and related surfaces (27 extension pages)

*Source: [opensource.salesforce.com/sf-pi](https://opensource.salesforce.com/sf-pi/) and [github.com/salesforce/sf-pi](https://github.com/salesforce/sf-pi) — open-source project docs (not an `llms-*.txt` developer-portal section).*

*Catalogued 2026-11-23: 40 published guide/extension pages in 4 sections (ADRs excluded).*

## Extraction notes

Labs runbook text above is authored for this catalog (org switcher, warm/cold runners, BYOO authorization). Install and doctor commands align with the upstream Install / Quickstart pages. See [index.md](index.md) for the full published link list.
