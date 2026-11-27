# Source record — Axios HTTP client

**Repository:** axios/axios  
**URL:** https://github.com/axios/axios  
**Immutable inspected commit:** 71c87d506567e2fe37ba9f6fae6a4fc9411583d0  
**Package version at commit:** 1.21.1  
**Licence:** MIT  
**Primary stack:** JavaScript / Node.js; browser adapters also exist  
**Selected facet:** Integrations; API; behaviour; errors and recovery

## Evidence inspected

- Pinned package manifest and Node ESM source entrypoint.
- The Node HTTP adapter and transform pipeline are exercised by AXIOS-HTTP-001.
- The case tests status rejection, redirects, request body serialization, query parameters, custom headers, timeouts, and malformed JSON fallback against a deterministic local HTTP service.

## Accepted bounded case

[AXIOS-HTTP-001](../../conformance/replication-lab/cases/AXIOS-HTTP-001/CASE.md) compares the pinned Axios Node HTTP adapter with an independent Python 3.12 urllib model across nine HTTP interaction scenarios. Six deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema and evidence-integrity validation in [run #45940398493](https://github.com/REMAREMA6/software-rules/actions/runs/45940398493), artifact `15172188627`.

## Boundary and limitations

The case covers a deterministic local HTTP service, not real-provider variability. TLS, proxies, credentials, cookies, multipart, streaming, cancellation, retries, and browser XHR remain outside scope. This is not complete Axios or integration-facet coverage.
