# Case — Express session creation, regeneration, tamper rejection, and destruction

**Case ID:** SESSION-EXPRESS-001  
**Status:** Pending runtime and evidence validation.  
**Facet(s):** Identity and authentication; security controls; behaviour; data; errors and recovery  
**Source:** https://github.com/expressjs/session  
**Immutable source commit:** `8947e169ae838b22cc1af198e50e370e6fc09f96`  
**Source version:** express-session 1.19.0  
**Runtime framework:** Express 5.3.0  
**Source stack:** JavaScript / Node.js  
**Replica stack:** Python 3.12 standard library  
**Licence:** MIT

## Declared scope

The case exercises express-session middleware with a fixed secret, MemoryStore, `resave:false`, `saveUninitialized:false`, and an HttpOnly/Lax session cookie. It tests creation, retrieval, regeneration, tamper rejection, and destruction. It does not test credential verification, identity-provider login, distributed stores, expiry/rolling renewal, secure-cookie deployment behind TLS, CSRF protection, or MFA.

## Technology-independent rules

1. An unmodified, uninitialized session is not persisted and does not emit a session cookie when save-uninitialized is disabled.
2. Writing session data persists the session and emits a signed session cookie with the declared attributes.
3. A valid cookie restores the corresponding server-side session data on later requests.
4. Regeneration invalidates the old session identifier and issues a new identifier for the new session.
5. A tampered signature is rejected; the tampered identifier does not restore the stored session.
6. Destroying a session removes server-side state and expires/clears the client cookie.

## Probes and mutations

Nine sequential requests cover empty session, create, read, regenerate, old-ID rejection, new-ID read, tampered-cookie rejection, destroy, and post-destroy rejection. Six mutations target save-uninitialized, cookie signing, old-ID invalidation, tamper acceptance, destroy persistence, and cookie clearing.

## Acceptance gate

Accept only after the pinned middleware and independent Python model match all nine normalized lifecycle outcomes; all six mutations are detected; cookie signing and source provenance are retained; and Software Rules 0.2.0 captures/comparison pass schema and evidence integrity. This is bounded server-side session lifecycle evidence, not a full identity provider or complete identity/security facet.
