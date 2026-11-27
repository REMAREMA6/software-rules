# Source record — express-session

**Repository:** expressjs/session  
**URL:** https://github.com/expressjs/session  
**Immutable inspected commit:** 8947e169ae838b22cc1af198e50e370e6fc09f96  
**Package version at commit:** 1.19.0  
**Licence:** MIT  
**Primary stack:** JavaScript / Node.js  
**Selected facets:** Identity/authentication; security; behaviour; data; errors and recovery

## Evidence inspected

- Pinned middleware entrypoint and MemoryStore implementation.
- Session creation and save policy with `saveUninitialized:false` and `resave:false`.
- Signed session cookie creation, regeneration, tamper rejection, and destruction.

## Accepted bounded case

[SESSION-EXPRESS-001](../../conformance/replication-lab/cases/SESSION-EXPRESS-001/CASE.md) compares the pinned express-session middleware against an independent Python 3.12 session/cookie model across nine sequential transitions. Five deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema and evidence-integrity validation in [run #45941194819](https://github.com/REMAREMA6/software-rules/actions/runs/45941194819), artifact `15172927152`.

## Boundary and limitations

The case uses MemoryStore, a fixed secret, and HttpOnly/Lax cookies. Credential verification, identity-provider login/logout, distributed stores, expiry/rolling renewal, MFA, CSRF, TLS secure-cookie deployment, and provider outages remain outside scope. This is not complete identity/authentication or security-facet coverage.
