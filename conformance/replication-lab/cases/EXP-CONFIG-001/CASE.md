# Case — Express routing configuration activation and matching

**Case ID:** EXP-CONFIG-001  
**Status:** PASSED for the declared five-profile, 18-request routing-configuration scope. Pinned Express 5.3.0 and independent Python 3.12 matched all 18 effective-configuration/path outcomes; case-sensitive, strict-routing, and late-setting mutations were detected; Software Rules 0.2.0 source/replica captures and comparison passed schema and cross-record integrity validation in [run #45937990537](https://github.com/REMAREMA6/software-rules/actions/runs/45937990537). Retained evidence artifact ID `15171850580` (expires 2026-12-27). This is bounded configuration evidence, not full Express configuration-facet coverage.  
**Facet(s):** Configuration; API; behaviour  
**Source:** https://github.com/expressjs/express  
**Immutable source commit:** `43fca52d28a422c8be48fd489cbd4f2d6152bab6` (Express 5.3.0)  
**Source stack:** JavaScript / Node.js  
**Replica stack:** Python 3.12 standard library  
**Licence:** MIT

## Declared scope

This case tests Express's `case sensitive routing` and `strict routing` settings, including when settings are changed after the router has been lazily initialized. It does not claim coverage of every Express setting or configuration source.

## Technology-independent rules

- With case-sensitive routing disabled, route path matching ignores letter case.
- With case-sensitive routing enabled, path letter case must match.
- With strict routing disabled, a trailing slash does not distinguish the route.
- With strict routing enabled, a trailing slash distinguishes the route.
- The effective router settings are captured when the router is first initialized. Changing these settings after initialization does not retroactively rebuild the router.

## Probes

Four combinations of the two Boolean settings each receive `/Report`, `/report`, `/Report/`, and `/report/`. A fifth scenario sends the exact route first, changes case sensitivity after that first request, and then sends the lowercase path. The Python replica implements the same effective-configuration snapshot without importing Express.

## Mutation tests

Mutations that ignore case sensitivity, ignore strict trailing-slash matching, or dynamically apply a setting after router initialization must be detected.

## Acceptance gate

Accept only after the pinned Express runtime and independent Python replica agree across all 18 path observations; all mutations are detected; Software Rules 0.2.0 captures and comparison pass schema/integrity validation; and the post-initialization setting snapshot is evidenced.
