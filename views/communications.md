# Communications Cloud — Telco Entry Page

Curated view for Enxoo telco engagements. It sits on top of the generated link catalog and brings together the Communications-relevant parts of five catalog areas, which are otherwise spread across 9,000+ links.

| | |
|---|---|
| Audience | Enxoo consultants, solution architects, developers, AI agents |
| Built from | [`industries/`](../industries/index.md), [`industries-integrations/`](../industries-integrations/index.md), [`revenue-cloud/`](../revenue-cloud/index.md), [`diagrams/`](../diagrams/index.md), [`data-cloud/`](../data-cloud/index.md), [`genai/`](../genai/index.md), [`hosted-mcp-servers/`](../hosted-mcp-servers/index.md), [`event-bus/`](../event-bus/index.md) |
| Source | Official `developer.salesforce.com` pages only. Every URL below appears in a generated `index.md` (checked by [`scripts/check_views.py`](../scripts/check_views.py)). |
| Verified | 2026-11-27. The TMF availability tables were read from the live pages that day. |
| Not covered | Setup, licensing and edition availability (help.salesforce.com), architecture guidance (architect.salesforce.com), release notes. See [Gaps](#gaps-and-next-steps). |

Markers used: **[Doc]** means stated on the linked official page. **[Inference]** means Enxoo interpretation drawn from page titles or structure; check it before using it with a customer.

---

## 1. Start here: two implementation tracks

The developer docs describe Communications sales and order capture on **two technical foundations**. Pick the track first, because the APIs, objects and TMF coverage differ.

| | Track A — Industries CPQ (managed package) | Track B — Salesforce Platform (standard / core) |
|---|---|---|
| What the docs call it | "Communications, Media, Energy and Utilities APIs (Managed Package)" section; Industries CPQ, Classic Cart APIs, Digital Commerce APIs | "CME Developer Guide" plus Revenue Management (Product Catalog Management, Product Configurator, Salesforce Pricing, Transaction Management, Dynamic Revenue Orchestrator) |
| Engine | **[Doc]** "Classic Cart APIs run the CPQ engine in managed-package Apex", while Standard Cart API operations go to "Salesforce core (Java) handlers" ([Industries CPQ Introduction](https://developer.salesforce.com/docs/industries/cme/guide/introduction.md)) | Core platform objects and Connect REST / invocable actions |
| Catalog | Enterprise Product Catalog (EPC) | Product Catalog Management (PCM) |
| TMF Open APIs | v4 family (620, 622, 637, 648) plus outbound service/geo APIs | v5 family (622, 637, 632, 666, 679) plus 671 |
| Entry page | [Get Started with CME Common APIs](https://developer.salesforce.com/docs/industries/cme/guide/get-started.md) | [Get Started with CME Developer Resources](https://developer.salesforce.com/docs/industries/cme-dev/guide/rev-cloud-for-comms-get-started.md) · [Get Started with Revenue Management](https://developer.salesforce.com/docs/revenue/revenue-management/guide/rlm-get-started.md) |

**[Inference]** The managed-package guide includes migration pages ([Migrate to Standard Cart APIs](https://developer.salesforce.com/docs/industries/cme/guide/comms-migrate-to-std-cart.md), [Migrate to Standard Digital Commerce](https://developer.salesforce.com/docs/industries/cme/guide/comms-migrate-to-sdc.md), [CPQ APIs to Replace OmniCPQServiceWrapper](https://developer.salesforce.com/docs/industries/cme/guide/comms-cpq-apis-to-replace-omnicpqservicewrapper.md)). That points to Salesforce moving capability toward the core platform. For new greenfield work, assess Track B first. For existing Vlocity/EPC customers, plan migration on purpose instead of assuming it.

---

## 2. Find the right page by job

| I need to… | Go to |
|---|---|
| Understand the Communications data model | [Data model: Communications](https://developer.salesforce.com/docs/platform/data-models/guide/communications-cloud-category.md) · [Revenue Management](https://developer.salesforce.com/docs/platform/data-models/guide/revenue-cloud-category.md) · [Commercial Configuration](https://developer.salesforce.com/docs/platform/data-models/guide/commercial-configuration.md) · [Industries](https://developer.salesforce.com/docs/platform/data-models/guide/industries-category.md) |
| Model products and offers (core) | [Product Catalog Management](https://developer.salesforce.com/docs/revenue/revenue-management/guide/pcm-overview.md) · [Product Configurator](https://developer.salesforce.com/docs/revenue/revenue-management/guide/prod-config-overview.md) · [Product Discovery](https://developer.salesforce.com/docs/revenue/revenue-management/guide/product-discovery-overview.md) |
| Price offers, including attribute-based pricing | Core: [Salesforce Pricing](https://developer.salesforce.com/docs/revenue/revenue-management/guide/pricing-overview.md) · Managed package: [Set up Attribute-Based Pricing](https://developer.salesforce.com/docs/industries/cme/guide/comms-set-up-attribute-based-pricing.md) |
| Run quote → order (core) | [Transaction Management](https://developer.salesforce.com/docs/revenue/revenue-management/guide/qoc-overview.md) · [Place Order REST API](#5-revenue-lifecycle-for-telco) · [Create Sales Transaction (POST)](#3-communications-apis-on-the-core-platform) |
| Decompose and orchestrate orders | [Dynamic Revenue Orchestrator](https://developer.salesforce.com/docs/revenue/revenue-management/guide/dynamic-revenue-orchestrator-overview.md) · [DRO callouts](https://developer.salesforce.com/docs/revenue/revenue-management/guide/dynamic-revenue-orchestrator-callouts-overview.md) |
| Build cart / quote APIs (managed package) | [CPQ Cart APIs](https://developer.salesforce.com/docs/industries/cme/guide/comms-cart-based-apis-for-industries-cpq.md) · [Standard Cart APIs](https://developer.salesforce.com/docs/industries/cme/guide/std-cart-get-started.md) · [Create a CpqAppHandler Hook](https://developer.salesforce.com/docs/industries/cme/guide/comms-create-a-cpqapphandler-hook.md) |
| Build B2C / digital self-service | [Get Started with Standard Digital Commerce](https://developer.salesforce.com/docs/industries/cme/guide/comms-get-started-with-standard-digital-commerce.md) · [Digital Commerce API Quick-Start](https://developer.salesforce.com/docs/industries/cme/guide/comms-t-digital-commerce-api-quick-start-guide.md) · [SDK Architecture](https://developer.salesforce.com/docs/industries/cme/guide/comms-t-digital-commerce-sdk-architecture.md) |
| Integrate with BSS/OSS over TM Forum APIs | [Section 4](#4-tm-forum-open-apis) |
| Handle usage, rating, billing | [Usage Management](https://developer.salesforce.com/docs/revenue/revenue-management/guide/usage-management-overview.md) · [Rate Management](https://developer.salesforce.com/docs/revenue/revenue-management/guide/rate-management-overview.md) · [Billing](https://developer.salesforce.com/docs/revenue/revenue-management/guide/billing-overview.md) |
| Write business rules / lookups | [Business Rules Engine](https://developer.salesforce.com/docs/industries/industries-common-dev/guide/business-rules-engine.md) · [Decision Matrix Actions](https://developer.salesforce.com/docs/industries/industries-common-dev/guide/actions-obj-decision-matrix.md) · [Expression Set Actions](https://developer.salesforce.com/docs/industries/industries-common-dev/guide/actions-obj-expression-set.md) · [Context Service](https://developer.salesforce.com/docs/industries/industries-common-dev/guide/context-service-overview.md) |
| Add AI agents or MCP access | [Section 6](#6-agentforce-data-360-and-mcp) |

---

## 3. Communications APIs on the core platform

Source section: *Communications, Media, Energy and Utilities (CME) Developer Guide* (132 pages) in [`industries/index.md`](../industries/index.md).

| Area | Key pages |
|---|---|
| REST reference | [REST Reference](https://developer.salesforce.com/docs/industries/cme-dev/guide/comms-api-rest-references.md) · [Resources](https://developer.salesforce.com/docs/industries/cme-dev/guide/comms-apis-resources.md) · [Request Bodies](https://developer.salesforce.com/docs/industries/cme-dev/guide/comms-apis-requests.md) · [Response Bodies](https://developer.salesforce.com/docs/industries/cme-dev/guide/comms-apis-responses.md) |
| Invocable actions (Flow / agents) | [Create Order From Cart](https://developer.salesforce.com/docs/industries/cme-dev/guide/actions-obj-create-order-from-cart.md) · [Create or Update Asset From Order](https://developer.salesforce.com/docs/industries/cme-dev/guide/actions-obj-create-update-asset-from-order.md) · [Initiate Asset Amendment](https://developer.salesforce.com/docs/industries/cme-dev/guide/actions-obj-initiate-amend-for-consumer-sales.md) · [Get Products for Consumer Sales](https://developer.salesforce.com/docs/industries/cme-dev/guide/actions-obj-get-products-consumer-sales.md) · [Place Sales Transaction for Consumer Sales](https://developer.salesforce.com/docs/industries/cme-dev/guide/actions-obj-place-sales-transaction-consu-sls.md) |
| Objects | [Standard Objects](https://developer.salesforce.com/docs/industries/cme-dev/guide/b2b-std-objects-parent.md) · [Fields on Standard Objects](https://developer.salesforce.com/docs/industries/cme-dev/guide/b2b-fields-on-std-objects-parent.md) |
| Older versions | [Previous Versions (PDF archive)](https://developer.salesforce.com/docs/industries/cme-dev/guide/cme-dev-pdf-archive.md) |

Notable resources and objects in this guide (search [`industries/index.md`](../industries/index.md) for the exact title): Create Sales Transaction (POST), Manage Product Configuration (POST), Retrieve Products List (POST), Initiate Asset Amend (POST), Manage Product Relationship Rules (POST), Get Redeemed Coupons (GET). Objects include BillingAccount, AccountBillingAccount, AssetRelationship, ProductRelationshipRule, QuoteRecipientGroup, OrderItemRecipient and CartToOrderCompletedEvent.

---

## 4. TM Forum Open APIs

Source section: *Communications Cloud TM Forum API* (216 pages) in [`industries-integrations/index.md`](../industries-integrations/index.md).

Start with: [Get Started with Industry API](https://developer.salesforce.com/docs/industries/communications/guide/get_started_industry_API.md) · [TM Forum Conformance and Availability](https://developer.salesforce.com/docs/industries/communications/guide/TMF_compliance.md) · [Get Started with MuleSoft Direct Integrations](https://developer.salesforce.com/docs/industries/communications/guide/get_started_industry_integrations.md) · [Extensibility for TMF APIs](https://developer.salesforce.com/docs/industries/communications/guide/introduction_ext.md) · [Import TMFOpenAPI Static Resources](https://developer.salesforce.com/docs/industries/communications/guide/import_datapacks.md) · [Known Issues](https://developer.salesforce.com/docs/industries/communications/guide/known_issues.md) · [FAQ](https://developer.salesforce.com/docs/industries/communications/guide/FAQ.md)

### Inbound APIs (Salesforce exposes)

**[Doc]** From [Deployment Availability of TMF Inbound APIs](https://developer.salesforce.com/docs/industries/communications/guide/inbound_deployment_availability.md), read 2026-11-27. "TMF certified" comes from [TM Forum Conformance and Availability](https://developer.salesforce.com/docs/industries/communications/guide/TMF_compliance.md).

| API | Managed package | Salesforce Platform | TMF certified | Spec page |
|---|:-:|:-:|:-:|---|
| TMF620 v4 Product Catalog | ✓ | | ✓ | [TMF620](https://developer.salesforce.com/docs/industries/communications/guide/TMF620.md) |
| TMF621 v5 Trouble Ticket | ✓ | ✓ | | [TMF621 v5](https://developer.salesforce.com/docs/industries/communications/guide/TMF621v5.md) |
| TMF622 v4 Product Ordering | ✓ | | ✓ | [TMF622](https://developer.salesforce.com/docs/industries/communications/guide/TMF622.md) |
| TMF622 v5 Product Ordering | | ✓ | | [TMF622 v5](https://developer.salesforce.com/docs/industries/communications/guide/TMF622v5.md) |
| TMF629 v4 Customer Management | ✓ | ✓ | ✓ | [TMF629](https://developer.salesforce.com/docs/industries/communications/guide/TMF629.md) |
| TMF632 v5 Party Management | ✓ | ✓ | | [TMF632](https://developer.salesforce.com/docs/industries/communications/guide/TMF632.md) |
| TMF637 v4 Product Inventory | ✓ | | ✓ | [TMF637](https://developer.salesforce.com/docs/industries/communications/guide/TMF637.md) |
| TMF637 v5 Product Inventory | | ✓ | | [TMF637 v5](https://developer.salesforce.com/docs/industries/communications/guide/TMF637v5.md) |
| TMF648 v4 Quote Management | ✓ | | ✓ | [TMF648](https://developer.salesforce.com/docs/industries/communications/guide/TMF648.md) |
| TMF651 v4 Agreement Management | ✓ | ✓ | ✓ | [TMF651](https://developer.salesforce.com/docs/industries/communications/guide/TMF651.md) |
| TMF666 v5 Account Management | | ✓ | | [TMF666](https://developer.salesforce.com/docs/industries/communications/guide/TMF666.md) |
| TMF667 v4 Document Management | ✓ | ✓ | ✓ | [TMF667](https://developer.salesforce.com/docs/industries/communications/guide/TMF667.md) |
| TMF671 v4 Promotion Management | | ✓ | ✓ | [TMF671](https://developer.salesforce.com/docs/industries/communications/guide/TMF671.md) |
| TMF679 v5 Product Offering Qualification | | ✓ | ✓ | [TMF679](https://developer.salesforce.com/docs/industries/communications/guide/TMF679.md) |

> **Source conflict:** the inbound availability page lists TMF632 v5 as "Managed Package and Salesforce Platform", while the conformance page lists it under Salesforce Platform only. Treat managed-package support for TMF632 v5 as unconfirmed until checked in an org.

### Outbound APIs (Salesforce calls)

**[Doc]** From [Deployment Availability of TMF Outbound APIs](https://developer.salesforce.com/docs/industries/communications/guide/outbound_deployment_availability.md). All of these are **managed package only**. That's significant for OSS integration on Track B.

| API | Spec page |
|---|---|
| TMF620 v4 Product Catalog Management | [TMF620 outbound](https://developer.salesforce.com/docs/industries/communications/guide/TMF620_outbound.md) |
| TMF622 v4 Product Ordering Management | [TMF622 outbound](https://developer.salesforce.com/docs/industries/communications/guide/TMF622_outbound.md) |
| TMF641 v4 Service Order Management | [TMF641](https://developer.salesforce.com/docs/industries/communications/guide/tmf641.md) |
| TMF645 v4 Service Qualification | [TMF645](https://developer.salesforce.com/docs/industries/communications/guide/tmf645.md) |
| TMF673 v4 Geographic Address | [TMF673](https://developer.salesforce.com/docs/industries/communications/guide/tmf673.md) |
| TMF674 v4 Geographic Site | [TMF674](https://developer.salesforce.com/docs/industries/communications/guide/TMF674.md) |
| TMF675 v4 Geographic Location | [TMF675](https://developer.salesforce.com/docs/industries/communications/guide/TMF675.md) |

Outbound notifications go through the [TMF Outbound Notifications Framework](https://developer.salesforce.com/docs/industries/communications/guide/TMF_notification_framework.md). TMF621, TMF632 and TMF651 notifications are available on both tracks. TMF622, TMF629 and TMF637 notifications are managed package only.

**[Inference]** On Track B, the docs list no outbound service-order (TMF641) or address/site (TMF673–675) API. Expect to build OSS hand-off through Dynamic Revenue Orchestrator callouts, MuleSoft or custom integration. Validate this in every Track B design.

Catalog mapping pages (how Salesforce catalog records map to TMF resources): [Catalog Use Cases](https://developer.salesforce.com/docs/industries/communications/guide/catalog-use-cases.md) · [Product Offering Mappings](https://developer.salesforce.com/docs/industries/communications/guide/product_offering.md). Search the index for *Product Specification Mappings*, *Product Offering Price Mappings* and *Category Mappings*.

---

## 5. Revenue lifecycle for telco

Source section: *Revenue Management Developer Guide* (1,410 pages) and related guides in [`revenue-cloud/index.md`](../revenue-cloud/index.md).

| Capability | Overview page | Telco use |
|---|---|---|
| Product Catalog Management | [PCM](https://developer.salesforce.com/docs/revenue/revenue-management/guide/pcm-overview.md) | Product specs, offers, bundles |
| Product Configurator | [Configurator](https://developer.salesforce.com/docs/revenue/revenue-management/guide/prod-config-overview.md) · [Business APIs](https://developer.salesforce.com/docs/revenue/revenue-management/guide/product-configurator-business-api-overview.md) | Bundle rules, attribute validation |
| Salesforce Pricing | [Pricing](https://developer.salesforce.com/docs/revenue/revenue-management/guide/pricing-overview.md) | Price books, attribute pricing, discounts |
| Transaction Management | [Quote & order capture](https://developer.salesforce.com/docs/revenue/revenue-management/guide/qoc-overview.md) | Quote → order, amendments, renewals |
| Dynamic Revenue Orchestrator | [DRO](https://developer.salesforce.com/docs/revenue/revenue-management/guide/dynamic-revenue-orchestrator-overview.md) | Order decomposition and fulfilment |
| Usage Management | [Usage](https://developer.salesforce.com/docs/revenue/revenue-management/guide/usage-management-overview.md) | Usage-based and consumption offers |
| Rate Management | [Rating](https://developer.salesforce.com/docs/revenue/revenue-management/guide/rate-management-overview.md) | Rating usage |
| Billing | [Billing](https://developer.salesforce.com/docs/revenue/revenue-management/guide/billing-overview.md) · [Billing Business APIs](https://developer.salesforce.com/docs/revenue/revenue-management/guide/billing-business-api-overview.md) | Invoicing, billing schedules |
| Advanced Approvals | [Approvals](https://developer.salesforce.com/docs/revenue/revenue-management/guide/advanced-approvals-overview.md) | Deal desk, B2B discount approval |
| Deployment | [Revenue Management Deployment](https://developer.salesforce.com/docs/revenue/revenue-management/guide/deployment-overview.md) | Metadata and data moves between orgs |

Related sections in the same index: *Salesforce Contracts* (199 pages), *Place Order REST API Developer Guide* (18 pages), *Salesforce Billing Developer Guide* (143 pages; managed-package Billing). The legacy *Salesforce CPQ* guides cover Steelbrick-based CPQ, which is not the Communications track.

---

## 6. Agentforce, Data 360 and MCP

| Need | Pages |
|---|---|
| Build agents | [Agentforce Developer Guide – Get Started](https://developer.salesforce.com/docs/ai/agentforce/guide/get-started.md) · [Agent API](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-get-started.md) · [Testing API](https://developer.salesforce.com/docs/ai/agentforce/guide/testing-api-get-started.md) |
| Expose Salesforce to external AI clients | [Hosted MCP Servers](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.md) · [Headless Experience Layer](https://developer.salesforce.com/docs/platform/hxl/guide/get-started.md). The companion repo [headless-toolkit](https://github.com/krystiandrozd-alt/headless-toolkit) covers these in depth. |
| Stream order and asset events to OSS | [Pub/Sub API](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/intro.md) |
| Subscriber consent data in Data 360 | Communication Subscription DMOs, for example [Communication Subscription DMO](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-communication-subscription-dmo.md) and [Consent DMO](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-communication-subscription-consent-dmo.md) |

**[Inference]** The invocable actions in [section 3](#3-communications-apis-on-the-core-platform) are the natural building blocks for telco agent actions, for example "show my products", "amend my plan" and "place an order". The developer docs don't cover a telco-specific agent template.

---

## Not telco, despite the name

These sections sit next to Communications content in [`industries/index.md`](../industries/index.md) but belong to other industries. Skip them in telco work: *Advanced Orders for Telesales* and *Penny Perfect Pricing* (Consumer Goods), *Energy and Utilities Cloud*, *Media Cloud* (relevant only for media/advertising scenarios), *Industries Core* (Consumer Goods TPM).

---

## Gaps and next steps

| Gap | Why it matters | Proposed fix |
|---|---|---|
| No help.salesforce.com content | Setup, permission sets, licensing and edition availability can't be answered from this repo | Add a `help-communications` catalog |
| No release-notes tracking | Track B coverage changes each release (e.g. new v5 TMF APIs) | Add a per-release diff of this page |
| TMF tables are a snapshot | Availability changes between releases | Re-read the three TMF availability pages at each refresh; the check script only verifies URLs still exist |
| TMF632 v5 source conflict | Managed-package support unclear | Verify in an org and record the result here |
| No Enxoo patterns | This page shows where docs live, not how Enxoo delivers | Link from the private Enxoo knowledge layer (KB-1 segments, PDD templates) |

---

*Maintained by hand. Generated catalog files are refreshed by `scripts/refresh_from_llms.py`. After a refresh, run `python3 scripts/check_views.py` to confirm every link on this page still exists in the catalog.*
