# Case — JOSE JWT signature and claim verification

**Case ID:** JOSE-AUTH-001  
**Status:** Pinned jose source and tests inspected; source runtime and independent Python HMAC/JWT model prepared; CI pending  
**Facet(s):** Identity and authentication; Security controls; Data; Behaviour; Errors and recovery  
**Source:** https://github.com/panva/jose  
**Source commit:** f4457b3e3c5a40359b40ad6fa9721d11aa2a2bd0  
**Package version:** jose 6.2.18  
**Source stack:** TypeScript / JavaScript / Node.js WebCrypto  
**Replica stack:** Python 3.12 standard-library HMAC, base64, and JSON  
**Licence:** MIT

## Declared scope

Verify compact HMAC-signed JWTs with a fixed test clock, a fixed test key, an explicit HS256 algorithm allowlist, and configured issuer/audience. The same source-generated token strings are passed to the independent Python verifier.

Eleven scenarios cover valid, expired, not-before, issuer mismatch, audience mismatch, tampered signature, disallowed algorithm, absent optional expiry, audience-array matching, missing issuer, and missing audience.

This is a token-verification case, not a complete identity provider, login flow, session manager, refresh-token system, or authorization policy engine. RSA/ECDSA keys, remote JWKS, key rotation, revocation, and other JOSE formats are excluded.

## Source evidence

- `src/jwt/verify.ts`: `jwtVerify` verifies the compact JWS before validating the JWT Claims Set.
- `src/lib/jws_verify.ts`: an explicit algorithm allowlist is checked before signature verification.
- `src/lib/jwt_claims_set.ts`: issuer/audience required-claim checks and matching, not-before, expiration, and current-date semantics.
- `test/jwt/verify.test.ts`: upstream tests for issuer/audience, algorithm allowlists, expiry, not-before, and optional claims.

The pinned source is compiled with TypeScript 6.0.2 and executed from its generated `dist/webapi` output. The independent Python implementation uses only the standard library and verifies the exact token strings emitted by the source probe.

## Rules under test

1. The token signature must verify with the supplied key.
2. An explicit algorithm allowlist rejects a token signed with an unlisted algorithm.
3. An `exp` claim is rejected when its NumericDate is at or before the verification time.
4. An `nbf` claim is rejected when it is later than the verification time.
5. Configured issuer and audience options require the respective claims and enforce their values.
6. An audience array is accepted when it contains the configured audience.
7. Expiration is not required by default when no required-claims policy includes it.

## Mutation tests

The independent Python verifier is mutated to skip signature, expiry, not-before, issuer, audience, or required-claim checks, and to allow HS384 despite the HS256-only policy. Each mutation must be detected.

## Acceptance gate

Accept only after the pinned jose runtime and independent Python implementation match all eleven scenarios, executable mutations are detected, and Software Rules 0.2.0 captures plus comparison report pass schema and cross-record evidence validation.
