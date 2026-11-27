# Phase 7 — Specification Review and Release Audit

**Review date:** 2026-11-27  
**Target specification version:** 0.3.0 (Draft)  
**Schema version:** 0.2.0 (Draft; `schemas/v1/` compatibility family)  
**Phase 6 baseline:** 24 accepted bounded cases, 15 source repositories, 15 facets.

## 1. Review decision

Phase 7 review is complete for a versioned **draft** release. It is not a stable 1.0.0 approval. The repository's normative model, schemas, examples, conformance implementation, evidence provenance, and stated limitations have been reconciled to the actual Phase 6 baseline. The known gaps below remain explicit and block any claim of universal or facet-wide completeness.

## 2. Specification consistency review

- [x] Core model, terminology, principles, rule classes, observation model, source-derived rules, and evidence/provenance reviewed together.
- [x] The Replication Completeness Rule retained as the controlling replication requirement; its historical Phase 6 Task Board note no longer describes Phase 6 as still in progress.
- [x] Fifteen facet boundaries and facet-specific payload specifications reviewed against the 15 schema payloads.
- [x] Comparison model, normalization, matching, classifications, and coverage semantics reviewed for bounded conclusions and missingness.
- [x] Phase 2/3/4/5 documents no longer describe completed work as future-phase work.
- [x] Design-decision status/version references reconciled where superseded by later accepted decisions.

## 3. Schema and conformance review

- [x] JSON Schema Draft 2020-12 schema set contains capture, shared records, comparison report, facet union, and 15 facet payload schemas.
- [x] Capture and comparison schemas declare draft schema version 0.2.0; the schema family path/URN remains `v1` and is not represented as stable 1.0.0.
- [x] Validation workflow installs its dependencies from `conformance/validation/`; documentation now gives the same reproducible command.
- [x] Cross-record integrity checks enforce unique IDs, reference resolution, evidence class, inventory links, and completeness-status consistency.
- [x] The validator's boundary is explicit: it cannot prove that the human-declared property inventory is exhaustive or that evidence semantically proves a property.
- [x] Positive/negative fixture and integrity workflows are required release checks.

## 4. Replication Completeness Rule review

The controlling rule requires every relevant property necessary to reproduce the declared scope to be inventoried and adequately evidenced. An unresolved required property prevents a complete status. Observed agreement and replication-scope completeness remain separate. Schema validity, a passing test suite, or a bounded case result cannot independently establish inventory exhaustiveness.

Phase 6's exit approval applies only to the declared 24-case validation corpus. It does not override unresolved property inventories or future-coverage entries in the case reports and facet matrix.

## 5. Evidence and provenance review

- [x] Runtime observations, source-derived inferences, and declared contracts remain separate record classes.
- [x] Runtime observations require execution/runtime interval, method, and runtime evidence references.
- [x] Source-derived rules retain source artifact provenance and cannot satisfy runtime completeness.
- [x] Case manifests identify immutable source revisions, source/replica stacks, probes, mutation tests, and workflow evidence.
- [x] CI artifacts have finite retention; the maintenance policy requires durable archiving for evidence needed beyond that window.

## 6. Known limitations carried into the draft release

- No facet is universally complete.
- The finite 24-case corpus does not prove arbitrary software or stack equivalence.
- The Task Board UI case is complete only for its explicitly declared bounded interface inventory.
- Native UI platform coverage, additional states/viewports/font rendering, and broader interface conditions remain future work.
- Full commerce promotion application/stacking, cart totals, campaign budgets, quantity tiers, shipping discounts, and checkout combinations remain uncovered.
- Identity-provider credential flows, refresh rotation, MFA, and distributed session lifecycle remain uncovered.
- Authorization policy models beyond the accepted Casbin cases and broader security controls (TLS, CSRF/CORS, secrets, and other threat classes) remain uncovered.
- Persistence multi-process concurrency, non-PostgreSQL isolation semantics, deadlocks, pool exhaustion, distributed transactions, and crash/power-loss durability remain uncovered.
- Messaging delivery guarantees/DLQs, multi-job scheduler failure/failover, integration resilience, dynamic configuration watchers, and performance scaling/latency distributions/resource budgets remain uncovered.
- Hosted workflow artifacts may expire; durable archival is not implied by a workflow link.

## 7. Release gate

- [x] A versioned 0.3.0 draft snapshot and maintenance policy are committed in the repository.
- [x] Schema version 0.2.0 is clearly distinguished from specification version 0.3.0.
- [x] Stable 1.0.0 is explicitly deferred until the criteria in `specification/VERSIONING.md` are met.
- [ ] Full schema/fixture and cross-record integrity workflow passes on the final release-candidate commit.
- [ ] Final release commit SHA and CI run URLs are recorded after merge.

The Phase 7 draft review can be accepted when all review changes are merged and the final release-candidate validation passes. Do not mark Phase 7 complete while the final CI gate is pending or failing.
