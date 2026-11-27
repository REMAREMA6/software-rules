# Software Rules 0.3.0 — Draft Release Snapshot

**Release:** 0.3.0  
**Maturity:** Draft / pre-stable  
**Release date:** 2026-11-27  
**Schema version:** 0.2.0  
**Schema family:** `schemas/v1/` (reserved compatibility namespace; not a stable 1.0 schema release)  
**Status:** Versioned repository release snapshot; not a stable standards publication.

## Included

- The common capture model and evidence-class separation.
- The accepted 15-facet catalogue and facet-specific schema payloads.
- The normative Replication Completeness Rule and scope-bounded comparison model.
- JSON Schema Draft 2020-12 capture and comparison-report schemas.
- Cross-record integrity validation and positive/negative fixtures.
- A 24-case Phase 6 cross-repository conformance corpus spanning 15 immutable source repositories and all 15 facets.
- The Phase 6 exit audit, explicit limitations, and Phase 7 maintenance policy.

## Validation baseline

The latest verified main-branch checks before this snapshot's documentation review are recorded in the Phase 7 audit. The Phase 6 TypeORM/PostgreSQL isolation runtime and Python rule-model workflows passed on commit `e152dea189f7ef4f473b0aedb5ac17d34e10ae65`. The full schema/fixture and integrity workflow must pass on the release candidate commit before this snapshot is treated as reviewed.

## Compatibility

This is a 0.x draft. No backward-compatibility guarantee is made. The schema version remains 0.2.0 and is independent of specification version 0.3.0. Consumers must pin both versions and must not assume that a future draft will accept or interpret this format identically.

## Known limitations

The 24 cases establish bounded cross-stack evidence only. They do not establish universal equivalence or facet-wide completeness. The Phase 6 exit audit and required-property inventory list uncovered property classes. In particular, the Task Board case is bounded to its declared interface scope; database isolation beyond the PostgreSQL 16 scenarios, full cart/checkout rules, identity-provider flows, broader authorization/security properties, scheduler failover, provider resilience, and performance scaling remain future coverage.

## Release integrity

The canonical source is the repository at the commit identified by the Phase 7 release audit and subsequent merge history. This file is a versioned release snapshot and release note; it does not itself create a Git tag or GitHub Release object.
