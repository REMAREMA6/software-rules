# Source candidate — Keycloak

**Repository:** keycloak/keycloak  
**URL:** https://github.com/keycloak/keycloak  
**Immutable inspected commit:** d22c7c587818ecf3517c349e9efa199b24623bbe  
**Licence:** Apache License 2.0 (LICENSE.txt at inspected commit)  
**Primary stack:** Java server; browser-based administration/client surfaces  
**Candidate facets:** Identity and authentication; authorization; configuration; errors/recovery.

## Evidence inspected

- docs/documentation/server_development/topics/auth-spi.adoc includes credential validation and required-action lifecycle descriptions, including password-expiration-triggered actions.
- The inspected documentation is source documentation, not runtime proof of a deployed realm's authentication flow.

## Candidate rule areas

Credential validation for a user within a realm; required-action evaluation and challenge; password-expiration handling; authentication failure and session lifecycle.

## Boundary and limitations

Keycloak is a large identity platform. Select one small realm/authentication flow and pin its configuration and test environment before capture. Do not generalize one SPI document to all Keycloak authentication modes. Runtime evidence, role/permission cases, and replica remain unstarted.

**Status:** candidate only; no Phase 6 pass claimed.
