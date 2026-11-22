# Lightning Web Components (LWC) — Content

Synthesis written independently from the two sources below (not copied text).

## What's in the aggregated doc index

829 pages across 5 sections: the core **Lightning Web Components Developer Guide** (689 pages — by far the bulk: framework fundamentals, lifecycle, wire service, events, testing, deployment, etc.), **Security for Lightning Components** (73 pages — Lightning Web Security and the legacy Locker Service model), **SLDS Linter** (17), **SLDS Validator** (9), and **UI Test Automation Model / UTAM** (41).

*Source: [`llms-lwc.txt`](https://developer.salesforce.com/docs/llms-lwc.txt) — official aggregated index (developer doc page), overview section.*

## The LWC Developer Center (curated landing page, not part of llms.txt)

Requested directly via [developer.salesforce.com/developer-centers/lightning-web-components](https://developer.salesforce.com/developer-centers/lightning-web-components) — a separate, human-curated hub page (not one of the `llms-*.txt` aggregated indexes). Note on extraction: a plain text-body fetch returned only page chrome (nav/footer) — the real content lives in a client-rendered region that only `read_page` (accessibility tree) picked up, not `get_page_text`.

It organizes LWC resources into four groups:

- **Documentation**: the Developer Guide, the interactive **Lightning Component Reference** (base component docs), Salesforce Extensions for VS Code, the **LWC Open Source** guide (using LWC outside a Salesforce org, at lwc.dev), Security for Lightning Components, and a link to filtered "All Docs" search results.
- **Tools**: Salesforce CLI, VS Code Extensions, Salesforce Code Analyzer, SLDS Linter, SLDS Validator, **LWS Console** (check JS compatibility with Lightning Web Security), **LWS Distortion Viewer** (look up which JS APIs LWS blocks/modifies), **Locker Console** and **Locker API Viewer** (the older Lightning Locker equivalents).
- **Trailhead**: "Build Lightning Web Components" trail (7475 points), "Lightning Web Components for Visualforce Developers" module, "Lightning Web Components Specialist" superbadge (16000 points), and a quick-start project for the OSS Recipes sample app.
- **Code Samples** (all on GitHub under `trailheadapps/`): `lwc-recipes`, `ebikes-lwc` (sample retail app), `dreamhouse-lwc` (sample real estate app), `lwc-recipes-oss`, and `visualforce-to-lwc` (migration examples).

*Source: [Lightning Web Components | Salesforce Developer Center](https://developer.salesforce.com/developer-centers/lightning-web-components) — developer doc page (curated hub, browser-rendered via accessibility-tree extraction).*

## Two distinct "LWC stacks" worth not conflating

This index's **Security** section and the Developer Center's **Tools** both surface **two parallel security models**: Lightning Web Security (LWS, current) and Lightning Locker (legacy) — each with its own console/viewer pair (LWS Console + Distortion Viewer vs. Locker Console + API Viewer). Don't assume they're interchangeable; check which one an org/runtime actually uses before citing either tool.



*Last refreshed 2026-11-22: 830 pages in 5 sections (counts from the live source).*

## Extraction notes

Full link list extracted programmatically from the live `llms-lwc.txt` (one fetch, no deep page-by-page review). The Developer Center page was read via the accessibility tree after a plain-text fetch returned shell content — a genuine extraction caveat, not a missing page.
