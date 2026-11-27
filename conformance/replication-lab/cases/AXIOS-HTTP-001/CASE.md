# Case — Axios HTTP client integration contract

**Case ID:** AXIOS-HTTP-001  
**Status:** PASSED for all nine declared HTTP interactions in [run #45940398493](https://github.com/REMAREMA6/software-rules/actions/runs/45940398493). Pinned Axios 1.21.1 and independent Python urllib matched all nine normalized outcomes; six deliberate mutations were detected; Software Rules 0.2.0 source/replica captures and comparison passed schema and cross-record integrity validation. Artifact `15172188627` retained through 2026-12-27. This is bounded HTTP integration evidence, not full Axios or integration-facet coverage.  
**Facet(s):** Integrations; API; behaviour; errors and recovery  
**Source:** https://github.com/axios/axios  
**Immutable source commit:** `71c87d506567e2fe37ba9f6fae6a4fc9411583d0`  
**Source version:** Axios 1.21.1 at the pinned commit  
**Source stack:** JavaScript / Node.js  
**Replica stack:** Python 3.12 standard library  
**Licence:** MIT

## Declared scope

The case exercises the pinned Axios Node HTTP adapter against a deterministic local HTTP service and independently reproduces the same client-visible contract with Python urllib. It covers JSON/text responses, redirect following, HTTP error statuses, JSON request serialization, query encoding, custom headers, timeout normalization, and malformed JSON fallback. It does not cover TLS, proxies, cookies, multipart uploads, streaming, cancellation, retries, or browser XHR.

## Technology-independent rules

1. Successful 2xx responses expose status and transformed response data.
2. Redirect responses are followed by default and expose the final response.
3. Non-2xx responses reject and preserve status plus response body.
4. Object request bodies are serialized as JSON and carry the JSON content type.
5. Query parameters are serialized consistently, including spaces.
6. Request headers are case-insensitive and custom headers reach the service.
7. A configured request timeout terminates the client operation and is distinguishable from an HTTP response.
8. With silent JSON parsing enabled, malformed JSON is returned as raw text rather than failing the whole response transform.

## Probes and mutations

Eight request scenarios cover JSON, text, 404, 503, redirect, POST echo/custom header, query serialization, timeout, and malformed JSON fallback. Six deliberate mutations target redirects, non-2xx handling, timeout, malformed JSON, custom headers, and query encoding.

## Acceptance gate

Accept only after all source/replica normalized outcomes match, all six mutations are detected, pinned source/dependency provenance is retained, and Software Rules 0.2.0 captures/comparison pass schema and cross-record integrity validation. This is bounded Axios HTTP integration evidence, not full Axios or integration-facet coverage.
