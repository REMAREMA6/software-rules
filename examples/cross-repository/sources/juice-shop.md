# Source candidate — OWASP Juice Shop

**Repository:** juice-shop/juice-shop  
**URL:** https://github.com/juice-shop/juice-shop  
**Immutable inspected commit:** c9f99228d9d56afb5f5ca7925376292f7fa44b13  
**Licence:** MIT (LICENSE at inspected commit)  
**Primary stack:** Web application; exact runtime stack and test setup must be recorded from package metadata before case acceptance.  
**Candidate facets:** Security controls; identity/authentication; authorization; interface; business rules; data; API; errors.

## Evidence inspected

- The repository includes challenge categories for broken access control, broken authentication, improper input validation, injection, insecure deserialization, security misconfiguration, sensitive data exposure, XSS, and related security classes.
- The inspected challenge metadata is not proof of a vulnerability or security control's runtime outcome.

## Candidate rule areas

Choose a single safe, local challenge/control boundary and document the expected allowed/blocked outcome. Do not probe a public deployment or any third-party target. Use only a locally controlled instance and non-destructive test data.

## Boundary and limitations

The project is deliberately security-training-oriented; challenge behavior must not be generalized to ordinary production applications. Confirm the exact challenge implementation, test harness, dependencies, and licence conditions for any assets before use.

**Status:** candidate only; no Phase 6 pass claimed.
