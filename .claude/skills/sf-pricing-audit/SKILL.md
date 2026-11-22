---
name: sf-pricing-audit
description: Independently verify Salesforce pricing claims, licensing relationships, prompt/skill reliability and Flex Credit estimates; use before commercial decisions or requested audits. Do not use for a routine one-line price lookup; do not change the audited source without approval.
---

# Salesforce Pricing Verification (SPQ pilot)

Use pricing-intelligence/AGENTS.md for evidence vocabulary and authorization rules. Audit is read-only by default.

1. **Source check:** decompose high-impact claims; verify on the specific official URL/section/version, not just a source list. Record `SUPPORTED`, `CONTRADICTED`, `UNKNOWN`, `CONFLICTED`.
2. **Semantic check:** commercial edition vs technical license, included vs optional, SKU invention, buying model vs billing cadence, currency and period, bundle double-counting, version/applicability.
3. **Runtime check:** if executable, run `python -m unittest discover -s pricing-intelligence/tests -v` and re-run the supplied scenario. Record actual exit codes/logs. Fixtures do not prove Salesforce billing parity.
4. **Coverage:** compare registered links to the EU pricing hub and report verified, pending, CONTACT_SALES and inaccessible sources. Missing is not false.
5. **Release gate:** BLOCK for a binding quote resting on unresolved unit/entitlement or an unauthorized action; REVIEW for missing external validation; PASS WITH CAVEAT only for bounded evidence-backed use; PASS only within observed scope.

**Output:** `claim_id | scope | observed evidence | issue | severity | correction | retest status`. Keep fixes in a proposed patch until explicit approval; never replace historical observations silently.
