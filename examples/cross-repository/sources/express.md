# Source candidate — Express

**Repository:** expressjs/express  
**URL:** https://github.com/expressjs/express  
**Immutable inspected commit:** 43fca52d28a422c8be48fd489cbd4f2d6152bab6  
**Version at commit:** 5.3.0  
**Licence:** MIT  
**Primary stack:** JavaScript / Node.js  
**Candidate facets:** API; behaviour; configuration; errors and recovery.

## Evidence inspected

- `lib/application.js` lines 72–80: lazy router construction passes the effective `case sensitive routing` and `strict routing` settings to the router.
- `lib/application.js` lines 94–99: application defaults are initialized; neither case-sensitive nor strict routing is enabled here.
- `test/app.head.js` lines 8–18 and 21–44: HEAD defaults to GET when no explicit HEAD route exists; selected response headers are compared with GET (excluding the date header).
- `test/app.options.js` lines 7–18 and 20–32: automatic OPTIONS reports unique methods for a route and includes HEAD for GET.
- `test/app.options.js` lines 100–115: an explicit OPTIONS handler overrides automatic method discovery.
- `test/app.router.js` lines 170–180: regular-expression routes match the pathname, not the query string.
- `test/app.router.js` lines 243–263: case-sensitive routing is disabled by default.
- `test/app.router.js` lines 423–439: trailing slashes are optional by default.

The pinned source repository has no package lockfile. The case workflow generates and retains a lockfile for the exact installed production dependency graph, records its digest, and reuses that lockfile on subsequent runs.

## Candidate rules

1. HEAD falls back to a matching GET route when no explicit HEAD route exists; the response body is suppressed.
2. Automatic OPTIONS returns the unique methods registered for the matching path and includes HEAD when GET exists.
3. An explicit OPTIONS route takes precedence over automatic method enumeration.
4. Default routing is case-insensitive and non-strict; trailing slashes are optional.
5. Query strings do not participate in route-path matching.
6. Unmatched paths continue through middleware to the configured 404 fallback.

## Independent replica

A Python 3.12 standard-library HTTP server is prepared under `conformance/replication-lab/projects/express-routing-python/`. It does not import Express, Node.js, or Express router code.

## Status

Source evidence has been inspected and the bounded seven-request runtime/replica workflow is configured. No cross-stack case pass is claimed until the pinned Express runtime, Python replica, comparison, mutation tests, Software Rules captures, and evidence validation all pass.
