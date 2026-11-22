---
name: sf-pricing-audit
description: Audit Salesforce pricing and licensing claims, graph integrity, usage calculations, source freshness, conflicts and gaps before commercial decisions.
---

# Salesforce Pricing Evidence Audit

This skill is READ-ONLY unless the user separately authorizes repairs.

1. Source check: open the specific official Salesforce product pricing section, rate-card version and contract terms if permitted. Check amount, unit, currency, product edition, qualifier, billing period, region and effective date. A public page does not prove a customer entitlement.
2. Semantics check: detect missing source sections, technical license versus commercial edition conflation, optional versus included errors, bundle double counting, contract prerequisites, invalid SKUs, conversions without an FX source, and competing price units.
3. Calculation check: run Python unittest discovery under pricing-intelligence/tests and the sample calculator command. Confirm production/sandbox, tier crossing, calendar month reset, allowances, unpriceable Headless and partial totals. Passing fixtures does not prove billing parity.
4. Coverage check: enumerate EU pricing hub product and industry links, classify verified / pending / contact-sales / blocked, and report unresolved conflicts. The initial seed alone is not full portfolio coverage.
5. Release gate: BLOCK for unsourced or contradictory high-impact billing claims, REVIEW for untested contracts or source conflicts, PASS WITH CAVEAT for bounded validated estimates, PASS only for explicitly checked scope.

Return a findings table: ID | Severity | Atomic claim | Source and check date | Contradiction/gap | Action. Separate observed fact, inference and UNKNOWN. Preserve earlier historical observations in any approved fixes.
