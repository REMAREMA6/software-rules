# Case — Redis client integration outcomes

**Case ID:** REDIS-INT-001  
**Status:** PASSED for the declared seven-operation Redis integration scope. Pinned go-redis Go client and independent Python 3.12 / redis-py client matched all seven normalized outcomes against Redis 7; five executable mutations passed; Software Rules 0.2.0 captures, comparison, schema validation, and evidence-integrity checks passed in [workflow run #45932496414](https://github.com/REMAREMA6/software-rules/actions/runs/45932496414). Retained CI artifact ID `15168909418` (expires 2026-12-27). This is bounded Redis integration evidence, not complete integrations-facet coverage.  
**Facet(s):** Integrations; errors and recovery; data  
**Source:** https://github.com/redis/go-redis  
**Source commit:** `37d4d98e2ccf59df4973df3e5de9edc87492426b`  
**Module:** `github.com/redis/go-redis/v9`  
**Source stack:** Go  
**Replica stack:** Python 3.12 / redis-py  
**Licence:** BSD 2-Clause

## Declared scope

Execute seven controlled interactions against an isolated Redis 7 service:
1. PING succeeds.
2. SET followed by GET returns the stored value.
3. GET for a missing key returns the missing-value outcome.
4. EXISTS reports one for an existing key.
5. PTTL reports a positive remaining TTL.
6. GET against a list key returns a WRONGTYPE failure.
7. A connection to an unavailable endpoint produces a connection failure.

The source and replica use separate key namespaces but identical logical requests. Comparison normalizes client-specific error text into semantic outcomes.

## Technology-independent rules

- A successful Redis PING produces a successful response.
- SET followed by GET returns the value stored for that key.
- GET of an absent key is represented as a missing value, not a successful string.
- EXISTS reports the number of matching keys.
- PTTL for a key with an active expiry is positive.
- A command incompatible with the stored Redis value type fails with a wrong-type error.
- An unavailable Redis endpoint produces a connection failure.

## Source evidence

Pinned go-redis module, its public client command API, and BSD 2-Clause licence. The runtime probe records the pinned source commit and executes the client against a real Redis service.

## Independent replica

Python 3.12 with redis-py executes the same logical interactions against the same isolated Redis service. It does not import or wrap go-redis.

## Mutation tests

Mutations skip the write, convert missing values into strings, suppress WRONGTYPE errors, report a zero TTL, and turn connection failures into successes. Each must be detected.

## Acceptance gate

Accept only after source and replica outcomes match all seven interactions, all five executable mutations are detected, and Software Rules 0.2.0 captures/report pass schema and cross-record evidence validation. This is bounded Redis-client integration evidence, not complete integration-facet coverage.
