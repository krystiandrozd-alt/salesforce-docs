# GitHub-first Salesforce Pricing Intelligence — read-only evidence workflow v0.2 (candidate)

Status: PROPOSED, not installed, not merged. Created 2026-11-22.
Companion: `skill-candidate/SKILL.md`, `communications-cloud-eu-2026-11-22.json`.
Scope: PUBLIC_PRICE and LICENSE requests; CREDIT requests additionally use the deterministic CLI.

## Why this exists

The source repository default branch is `master`, but the pricing implementation lives on
`feature/pricing-licensing-knowledge-graph-20261122`. Default-branch-only GitHub lookup
returns NOT_FOUND and produces an incomplete answer despite a working connected GitHub app.
The source seed also lists Communications Growth / Advanced at EUR 325 / 475, while a newer
EU page variant lists EUR 300 / 450 plus Max editions. The discrepancy MUST be surfaced
and not silently normalized.

## Runtime prerequisites and capability gates

1. Identify the actual connected GitHub app/action. Confirm repository access to
   `krystiandrozd-alt/salesforce-docs` using repository discovery; never infer access
   merely from a URL or from installation of a skills-only ChatGPT plugin.
2. Inspect `default_branch` and attempt `pricing-intelligence/AGENTS.md` or
   `pricing-intelligence/README.md`. If absent, query matching branches and check explicit
   refs in order: user's selected branch, most recently verified pricing PR head,
   then candidate refs. Record `repo`, `ref`, `commit_sha`, and retrieval result.
   Do not silently fall back to an unrelated branch or assume `main`.
3. Read required files through the exact resolved ref, not the default:
   `data/seed-eu-2026-11-22.yaml`, `AGENTS.md`, `CLAUDE.md`,
   `docs/agent-io-contract.md`, `schema/scenario.schema.json`, and, only for CREDIT,
   `data/rate-card-2026-11-03.json` and `credit_calculator.py`.
4. GitHub read failure is not proof that product, data, or prices do not exist.
   Mark `REPOSITORY_UNAVAILABLE` / `REF_UNRESOLVED` and continue official public research.
   Include a clear access warning, not a fabricated graph lookup.

## Mandatory execution flow

A. INTENT — classify PUBLIC_PRICE / LICENSE / CREDIT / AUDIT; perform only needed stages.
B. REPO — resolve repository, branch/ref, version and relevant curated facts. Treat seed as
   an historical observation, not a live SKU catalog or evidence of current prices.
C. WEB — visit the official Salesforce region-specific product page, preserving its
   original currency and displayed unit. Search product name and alternate localized pages
   when snapshots disagree. Record exact URL, section, observation date, cache/crawl age
   if known, and any country-specific variant. Preserve old observations.
D. RECONCILE — compare facts per canonical product+offer+region+currency+unit+term:
   MATCH; CHANGED_WITH_PROVEN_HISTORY; CONFLICTED; UNKNOWN. Source recency alone is NOT
   authoritative proof of an offer's effective date. Do not convert old Agentforce 1
   editions into Max editions without verified Salesforce rename / supersession evidence.
E. LICENSE — distinguish marketing edition, verified SKU, technical UserLicense,
   PSL, capability, included entitlement, optional add-on, eligibility, and contract.
   B2B/B2C BSS Suites billed per org/year cannot be equated to per-user editions.
   `INCLUDES` and `AVAILABLE_FOR_PURCHASE` are different predicates.
F. CREDIT (only when requested) — discover current meter IDs, inspect rate card status
   and native units, build month-based JSON scenario, run the repository CLI if actually
   available, capture stdout/stderr/exit code and rate version. Otherwise `NOT_RUN`.
   Do not sum Conversations, other credit pools and Flex Credits as fungible units.
   Do not treat Headless Platform Interaction TBA as zero.
G. AUDIT — for every material price/entitlement claim, verify evidence + region + unit +
   purchasing conditions; mark source issues and unresolved customer-specific rights.
   For CLI changes run the existing unittest suite. Tests of local fixtures do not imply
   independent Salesforce billing, eligibility, or customer contract parity.
H. ANSWER — state: scope, repo/ref/sha, retrieved files, web URL and section, observed
   timestamp, price and original pricing unit, conflict status, execution status,
   uncovered items, and commercial-readiness status. Show the exact external sources
   supporting public claims. No product omission may be interpreted as "not offered".

## Evidence states and stop conditions

- SOURCE_VERIFIED: observed in cited official source and with verified scope/denominator.
- INFERRED: explicitly derived with claim references.
- UNKNOWN: missing or inaccessible evidence; NEVER zero.
- CONFLICTED: materially different observations not reconciled with evidence.
- Execution: EXECUTED, NOT_RUN, NOT_APPLICABLE.
- Commercial readiness: RESEARCH_ONLY, ESTIMATE_NOT_QUOTE, QUOTE_REVIEW_REQUIRED.
- A public listed price is never a signed quote or a verified orderable SKU.
- No Salesforce org login, token use, purchasing action, plugin upgrade, or deployment
  is authorized by a public pricing lookup.

## Communications Cloud 2026-11-22 worked read-only case

- Repo default `master` -> `pricing-intelligence/` NOT_FOUND.
- Explicit feature ref -> repository seed with Growth EUR 325 and Advanced EUR 475.
- Official EU base URL cached older content also shows EUR 325 / 475, and Agentforce 1
  EUR 850 offerings. Official `?bc=OTH` indexed variant newer by crawl recency shows
  Growth EUR 300, Advanced EUR 450, Sales Max EUR 800, Service Max EUR 800,
  Sales & Service Max EUR 825. All per user per month, billed annually.
- Thus `CONFLICTED` temporal snapshots and edition taxonomy; latest natively
  effective EU contract terms remain unverified. Do NOT overwrite historical seed.
- Older EU page also shows B2B and B2C BSS Suites starting EUR 4,000,000 per org/year;
  newer page's exact commercial details should be separately reverified.
- See the attached JSON observation record. No named-customer SKU, discounts,
  entitlements or binding quotation verified.

## Acceptance tests (do not claim these are behavioral tests)

1. Default-branch miss resolves via explicit feature ref or returns clear blocker.
2. Cannot assert Growth=325 as current solely from historical seed.
3. Cannot silently assert Growth=300 as contract-valid when official snapshots conflict.
4. Must not equate Agentforce 1 Sales/Service 850 with Sales/Service Max 800 as a rename.
5. Must preserve EUR/User/Month annual billing separately from EUR/Org/Year.
6. No invented SKU, implied inclusion, or Headless=zero.
7. CREDIT requires proven runtime execution; else NOT_RUN.
8. Every displayed result reports branch, source, time, status and gaps.

Proposed follow-up behavioral eval: add branch miss and temporal conflict cases to the
existing 16-case paired suite at `audits/spq-2026-11-22/paired-eval-suite.json`.
Keep the original suite unchanged and run controlled model tests before promotion.

## Source registry for this case

- Original branch: https://github.com/krystiandrozd-alt/salesforce-docs/tree/feature/pricing-licensing-knowledge-graph-20261122/pricing-intelligence
- Historical seed: https://github.com/krystiandrozd-alt/salesforce-docs/blob/feature/pricing-licensing-knowledge-graph-20261122/pricing-intelligence/data/seed-eu-2026-11-22.yaml
- Salesforce EU page: https://www.salesforce.com/eu/communications/pricing/
- Newer indexed EU variant: https://www.salesforce.com/eu/communications/pricing/?bc=OTH
- Salesforce global: https://www.salesforce.com/communications/pricing/?bc=OTH
- 2021 contractual limitations: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/legal/Agreements/additional-contractual-limitations-communications.pdf
  (historical; do not assume it governs 2026 orders, and PDF visual validation was blocked).
