# Analytics — Content

Synthesis written independently from the source index below (not copied text).

Analytics is the largest single index in this catalog: <!--pages-->1,023<!--/pages--> page links across <!--sections-->16<!--/sections--> sections. It spans two generations of Salesforce's BI stack:

- **CRM Analytics (the older "Wave" stack)**: embedding dashboards via Aura/LWC components, the full dashboard-interactions/bindings syntax (SAQL, SQL, data manipulation/selection/serialization functions), the Analytics Dashboard JSON format, the Analytics CLI plugin, Extended Metadata (XMD), the External Data API, and LWC-in-dashboard support. These sections (SAQL Developer Guide <!--pages:Analytics SAQL Developer Guide-->173<!--/pages--> pages, SQL Developer Guide <!--pages:SQL for Analytics Developer Guide-->108<!--/pages--> pages, Templates Developer Guide <!--pages:Analytics Templates Developer Guide-->95<!--/pages--> pages, Reports and Dashboards REST API <!--pages:Salesforce Reports and Dashboards REST API Developer Guide-->84<!--/pages--> pages) account for most of the bulk.
- **Tableau Next (the newer stack)**: a REST API for managing dashboards/insights programmatically, and — by far the single largest section in the entire index — the **Tableau Next Embedding SDK** (<!--pages:Tableau Next Embedding SDK-->317<!--/pages--> pages), which is mostly a generated TypeScript API reference repeated across at least three SDK versions (`sdk-js-v1`, `sdk-js-v2`, `sdk-js-v11`), each enumerating the same ~90 classes/types/enums (Action, AnalyticsDashboard, AnalyticsFilter, DashboardMetadata, etc.) almost verbatim.

*Source: [`llms-analytics.txt`](https://developer.salesforce.com/docs/llms-analytics.txt) — official aggregated index (developer doc page), overview section.*

*Last refreshed 2026-11-23: 1023 pages in 16 sections (counts from the live source).*

## Extraction notes

- The full <!--pages-->1,023<!--/pages-->-link list was extracted programmatically (DOM text parsed into sections via a browser script, not read link-by-link) to make reproducing it in full tractable — see [index.md](index.md).
- Most of the apparent size is **repetition across SDK versions**, not 1,003 unique concepts — if you need the Embedding SDK reference, pick one version (the highest, `sdk-js-v11` as of capture) rather than cross-referencing all three.
- No deep page-by-page review beyond the index file's own overview text.
