# Case — Medusa promotion rule evaluation and context eligibility

**Case ID:** MEDUSA-PROMO-001  
**Status:** PASSED in [run #45944011363](https://github.com/REMAREMA6/software-rules/actions/runs/45944011363). The exact pinned Medusa `evaluateRuleValueCondition` and `areRulesValidForContext` functions matched an independent Python evaluator across 32 scenarios covering all seven operators, scalar/array quantification, numeric comparison, missing context, nested paths, item/shipping scope prefixes, malformed rules, and multi-rule conjunction. Eight deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema, cross-record integrity, and comparison completeness validation. Artifact `15174046701` retained through 2026-12-27. This is bounded promotion-rule eligibility evidence, not discount application or full checkout coverage.  
**Facets:** Business rules; behaviour; data  
**Source:** https://github.com/medusajs/medusa  
**Immutable source commit:** `6e28e10acb9676392315b3ff1a9c7147fce4b5ab`  
**Source stack:** TypeScript  
**Replica stack:** Python 3.12  
**Licence:** MIT for selected community source files

## Declared boundary

The case extracts and executes the exact `evaluateRuleValueCondition` and `areRulesValidForContext` functions from `packages/modules/promotion/src/utils/validations/promotion-rule.ts`. It covers equality, inequality, membership, numeric comparisons, array quantification, missing context, nested attributes, item/shipping scope prefixes, and conjunction across multiple rules. It does not execute promotion discovery, SQL prefiltering, discount calculation, campaign budgets, promotion usage registration, or checkout workflows.

## Technology-independent rules under test

1. `eq` requires every observed context value to match one of the configured rule values.
2. `in` requires at least one observed context value to match.
3. `ne` requires every observed context value to differ; a missing/empty context value list passes `ne` but fails other operators.
4. `gt`, `gte`, `lt`, and `lte` compare numeric values, with inclusive operators accepting equality at the boundary.
5. Numeric context values are string-coerced for `eq`, `in`, and `ne`.
6. Rule evaluation strips `items.` or `shipping_methods.` only for the matching target scope and resolves nested attribute paths.
7. All rules must be valid for the context; missing attributes and rules without string values fail except the explicit `ne` missing-context behaviour after a valid rule is formed.
8. An empty rule set is valid.

## Probe matrix

Thirty-two deterministic probes cover all seven operators, scalar/array values, nested and scoped attributes, missing context, malformed rules, and multi-rule conjunction. Eight deliberate mutations target array quantification, missing-context handling, numeric comparison, scope stripping, multi-rule conjunction, and value filtering.

## Acceptance gate

Accept only after pinned Medusa functions and the independent Python implementation match all 30 normalized outcomes, all eight mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and evidence-integrity validation. This is bounded promotion-rule evaluation evidence, not full promotion lifecycle or complete business-rule facet coverage.
