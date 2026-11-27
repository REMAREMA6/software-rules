# Case — Express HTTP routing and method semantics

**Case ID:** EXP-API-001  
**Status:** PASSED for the declared seven-request scope. Pinned Express runtime and independent Python HTTP replica match across 28 facet/scenario projections; executable mutation tests, Software Rules schema validation, cross-record evidence integrity, and artifact persistence all pass.  
**Facet(s):** API; Behaviour; Configuration; Errors and recovery  
**Source:** https://github.com/expressjs/express  
**Source commit:** 43fca52d28a422c8be48fd489cbd4f2d6152bab6  
**Source version:** Express 5.3.0  
**Source stack:** JavaScript / Node.js / Express router  
**Replica stack:** Python 3.12 standard-library HTTP server  
**Licence:** MIT

## Declared scope

A minimal Express application registers GET and PUT handlers for `/widgets`, one explicit OPTIONS handler for `/override`, and a deterministic 404 fallback. The case tests:

1. HEAD falling back to a GET handler, with the response body suppressed, zero body bytes on the raw HTTP wire, and selected headers preserved.
2. Automatic OPTIONS responses listing the unique methods registered for a path, including HEAD for GET.
3. An explicit OPTIONS route overriding automatic method discovery.
4. Default case-insensitive routing and optional trailing slashes.
5. Query strings not participating in route-path matching.
6. Deterministic unmatched-path 404 behaviour.

This is not a complete Express router or HTTP server replica. Only these declared request/response and configuration rules are in scope.

## Source evidence

Pinned source inspection:
- `lib/application.js` lines 72–80: router created using effective `case sensitive routing` and `strict routing` settings.
- `lib/application.js` lines 94–99: default configuration does not enable either setting; query parser defaults to `simple`.
- `test/app.head.js` lines 8–18 and 21–44: HEAD defaults to GET and response headers match GET (excluding date).
- `test/app.options.js` lines 7–18 and 20–32: automatic OPTIONS reports unique route methods and includes HEAD for GET; lines 100–115 test explicit override.
- `test/app.router.js` lines 170–180: regular-expression route matches pathname only, not query string.
- `test/app.router.js` trailing-slash and case-sensitivity suites: trailing slash optional by default; case sensitivity disabled by default.

The source repository has no package lockfile at this commit. The runtime workflow generates and retains a lockfile for the exact installed dependency tree so the test environment can be reproduced.

## Runtime probe matrix

| Scenario | Expected rule |
|---|---|
| GET /widgets | Registered GET route returns 200 |
| HEAD /widgets | GET fallback, 200, empty body, same content length as GET |
| OPTIONS /widgets | Automatic Allow/body: GET, HEAD, PUT |
| OPTIONS /missing | Deterministic 404 fallback |
| OPTIONS /override | Explicit OPTIONS handler overrides automatic response |
| GET /WIDGETS/ | Default case-insensitive, non-strict route matching |
| GET /widgets?color=blue | Query string does not alter pathname route matching |

## Independent replica

The Python 3.12 replica uses only the standard-library HTTP server. It does not import Express, Node.js, or Express router code. It implements the extracted route and method semantics independently.

## Mutation tests

The comparison tests deliberately mutate the executable Python replica's HEAD wire-body suppression, OPTIONS method enumeration, case-sensitive routing, strict trailing-slash matching, query-path handling, and explicit OPTIONS precedence. Each mutation must produce a mismatch.

## Acceptance gate

**Passed for the declared bounded scope.** The pinned Express 5.3.0 runtime and independent Python 3.12 HTTP server match across all seven requests and 28 facet/scenario projections. The comparison covers API responses, behaviour, routing configuration, and 404 fallback. Executable mutation tests detect incorrect HEAD wire-body handling, OPTIONS method enumeration/precedence, case sensitivity, strict trailing-slash behaviour, and query-path handling. The Software Rules 0.2.0 source/replica captures and comparison report passed schema and cross-record integrity validation in [workflow run #20](https://github.com/REMAREMA6/software-rules/actions/runs/45926714897). Seven evidence files, including the generated npm dependency lockfile and dependency tree, are committed under `artifacts/` at [commit ad30376](https://github.com/REMAREMA6/software-rules/commit/ad3037693d32221a6d7bdb6b9883c45db7b2be9c). This does not establish equivalence for all Express routing behaviour or complete any entire facet.
