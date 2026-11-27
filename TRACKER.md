# Project Tracker

**Project:** Software Rules  
**Repository:** REMAREMA6/software-rules  
**Last updated:** 2026-11-27  
**Current phase:** Phase 7 — Review, release, and maintenance  
**Overall status:** Phase 6 exit approved for the declared 20-case cross-repository validation corpus across all 15 facets and 15 immutable source repositories. No facet is claimed universally complete; all case boundaries, exclusions, future extensions, and limitations are recorded in [PHASE6-EXIT-AUDIT.md](conformance/replication-lab/PHASE6-EXIT-AUDIT.md). Phase 7 is unblocked and not started. Accepted cases include: BullMQ retry/backoff, BullMQ messaging, Express routing, TypeORM transactions and file-backed durability, Medusa date validation, JOSE JWT verification, Casbin RBAC authorization, go-redis/redis-py integration, TASKBOARD-UI-001 (plain HTML/CSS to independent React UI replication), EXP-CONFIG-001 (Express routing configuration to independent Python model), PROM-PERF-001 (Prometheus write workload and independent Python model), CASBIN-ADV-AUTHZ-001 (Casbin domain RBAC, ABAC, deny override, and policy mutation), MEDUSA-PRICE-001 (Medusa calculated/original price selection), MEDUSA-ADJUST-001 (Medusa adjustment/tax allocation), MEDUSA-PROMO-001 (Medusa promotion rule eligibility), AXIOS-HTTP-001 (Axios external HTTP integration), SESSION-EXPRESS-001 (express-session identity/session lifecycle), and VIPER-CONFIG-001 (Viper configuration precedence). No entire facet is complete; several facet inventories and independent replications remain incomplete.

> This file is the persistent progress and handoff record. Update it whenever task status changes. Keep the current task, blockers, and next action explicit so work can resume in a new chat.

## Status key

- [ ] Not started
- [~] In progress
- [x] Completed
- [!] Blocked
- [?] Needs a decision or verification

## Current position

- **Current phase:** Phase 7 — Review, release, and maintenance
- **Current task:** Begin Phase 7 review, release, and maintenance: review the specification for contradictions/omissions, verify the Replication Completeness Rule and schema/evidence links, document limitations, and prepare a versioned release.
- **Blockers:** No blockers remain for the declared Phase 6 validation corpus. The exit audit explicitly lists future extensions, including discount application/cart totals/checkout, identity-provider credentials/MFA, authorization policy variants, persistence concurrency/isolation, messaging delivery guarantees, background scheduling/cancellation, integration resilience, and performance scaling. These are not claimed as captured or globally irrelevant. Casbin now covers simple RBAC plus bounded domain RBAC, ABAC owner matching, deny override, and policy mutation; other role hierarchies, policy priorities, resource-role models, and policy-adapter behaviours remain untested. JWT verification and signed-session lifecycle now have bounded independent cases; credential verification, identity-provider login/logout, refresh rotation, MFA, and distributed session lifecycle remain open. External HTTP integration now has a bounded Axios/urllib case covering nine request/response outcomes; TLS, proxies, credentials, retries, cancellation, and provider-specific behaviours remain open. PROM-PERF-001 provides bounded repeatable performance/resource evidence, but scaling, latency distributions, concurrency, saturation, and resource budgets remain untested. TASKBOARD-UI-001 now supplies a bounded independent UI-stack replica, but broader interface properties remain unresolved. Business-rule coverage now includes Medusa date validation, price selection, adjustment/tax allocation, promotion rule operators/context eligibility, and Task Board title/count rules; full cart totals, promotion application/precedence, campaign budgets/usage, quantity tiers, currency normalization, shipping discounts, and checkout combinations remain uncovered. Interface, data, persistence, API, messaging, background-processing, errors, and configuration still have unresolved property inventories; Viper and Express cover only bounded configuration classes.
- **Next action:** Execute the Phase 7 review checklist against the 20-case exit audit; do not upgrade the bounded corpus decision into a universal-equivalence claim.
- **Existing result:** The initial reference/independent Task Board baseline is pixel-identical across seven tested UI states at 1280×800 in Chromium 159.0.8154.6 on Linux; the deliberate mutation produces a 272-pixel visual mismatch. This is bounded evidence, not proof of complete interface capture or whole-system replication.

## Phase tracking

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Repository and project governance | [x] Complete | Roadmap, tracker, contribution guide, changelog, decision log, maturity/versioning policy, and navigation links established. |
| 1 | Research existing standards and prior art | [x] Complete | Comparative review, authoritative references, limitations, design implications, and revised facet proposal recorded. |
| 2 | Core concepts and common model | [x] Complete | Core vocabulary, rule/evidence classes, linked observation model, source-derived model, and interface/API conceptual tests completed. Schemas remain deferred. |
| 3 | Facet specifications | [x] Complete | Accepted 15-facet draft catalogue; all facets have boundaries, conceptual payload dimensions, scenario/evidence requirements, limitations, cross-facet links, and illustrative worked examples. Not empirical captures. |
| 4 | Machine-readable schemas | [x] Complete | Draft v0.2.0 schemas; 15 typed facets; positive/negative fixtures; Ajv 2020-12 CI passed. |
| 5 | Canonicalization and comparison | [x] Complete | Matching, normalization, classifications, coverage, bounded conclusions, report schema, example, and CI validation completed. |
| 6 | Cross-repository, cross-stack replication and conformance | [x] Complete for declared corpus | Phase 6 exit approved: 20 accepted bounded cases, 15 source repositories, all 15 facets represented, explicit case-scope exclusions and future coverage, and final report in [PHASE6-EXIT-AUDIT.md](conformance/replication-lab/PHASE6-EXIT-AUDIT.md). No universal equivalence or facet-wide completeness claim. |
| 7 | Review, release, and maintenance | [ ] Not started | Unblocked by the approved Phase 6 corpus exit; begin specification, schema, evidence, limitation, and release review. |

## Phase 0 — Repository and project governance

- [x] Create public GitHub repository.
- [x] Create initial `README.md`.
- [x] Confirm GitHub repository connection can create files.
- [x] Propose and document target repository layout.
- [x] Create project roadmap in `PLAN.md`.
- [x] Create persistent progress tracker.
- [x] Create contribution workflow in `CONTRIBUTING.md`.
- [x] Link plan and tracker and governance documents from the README.
- [x] Establish changelog and design-decision recording conventions.
- [x] Define specification maturity labels and versioning policy.

**Phase 0 exit gate: satisfied.** A new chat or contributor can find the project purpose, roadmap, progress, contribution process, decisions, change history, and versioning policy in the repository.

## Phase 1 — Research existing standards and prior art

- [x] Review requirements/specification standards (ISO/IEC/IEEE 29148).
- [x] Review platform-independent modelling (OMG MDA).
- [x] Review UML structural and behavioural modelling.
- [x] Review business-rule representation (OMG SBVR).
- [x] Review API contracts (OpenAPI).
- [x] Review event-driven API contracts (AsyncAPI).
- [x] Review runtime observability conventions (OpenTelemetry).
- [x] Review web runtime inspection (DOM, CSSOM, WebDriver).
- [x] Review native UI runtime inspection and accessibility semantics.
- [x] Review scenario-based behaviour specification (Gherkin/BDD).
- [x] Review JSON Schema for machine validation.
- [x] Review design-token interchange and its limits.
- [x] Write a comparative standards review.
- [x] Record design decisions, rejected approaches, and unresolved questions.
- [x] Revise the proposed facet list and record new candidate facets.

## Phase 2 — Core concepts and common model

- [x] Define and review canonical terminology.
- [x] Distinguish declared contracts, runtime observations, and source-derived inferences.
- [x] Separate scenario definitions, scenario executions, and individual observations.
- [x] Define external, platform-inspection, and instrumented runtime observation methods.
- [x] Define capture coverage and incomplete/unavailable dimensions.
- [x] Define system boundary, component, and facet concepts.
- [x] Define runtime-rule classification, proposition, status, and relationships.
- [x] Define source-derived-rule record and verification lifecycle.
- [x] Define scenario, trigger, condition, input, expected outcome, and actual outcome.
- [x] Define observation, outcome, state change, and side effect.
- [x] Define evidence and provenance requirements.
- [x] Distinguish unknown, not observed, unavailable, not applicable, redacted, and conflicting states.
- [x] Define identity relationships, units, timestamps, ordering, and correlation conceptually.
- [x] Define the common observation envelope and typed facet payload boundary.
- [x] Define the conceptual relationship to format versioning.
- [x] Test the model against interface resolved-layout and API request/response examples.

**Phase 2 exit gate: satisfied at the conceptual-model level.** The examples are model tests, not empirical captures or final conformance fixtures. Exact serialized fields, schemas, facet payloads, and the final facet taxonomy remain open.

## Phase 3 — Facet specifications

- [x] Interface — resolved hierarchy, presentation, geometry, stacking, accessibility, assets, and UI states.
- [x] Behaviour — triggers, conditions, transitions, outputs, and side effects.
- [x] Business rules — domain decisions, constraints, calculations, and policy outcomes.
- [x] Data — runtime structures, values, validation, and transformations.
- [x] Persistence — durable state, transactions, consistency, and lifecycle.
- [x] API — synchronous request/response exchanges.
- [x] Messaging — asynchronous message/event delivery and processing.
- [x] Identity and authentication — principal establishment and credential/session lifecycle.
- [x] Authorization and permissions — runtime access decisions and enforcement.
- [x] Security controls — security-relevant mechanisms and outcomes under authorized tests.
- [x] Background processing — queued, scheduled, and worker lifecycle.
- [x] Errors and recovery — failures, retries, fallbacks, compensation, and recovery.
- [x] Integrations — external-system interactions and dependency outcomes.
- [x] Configuration — effective runtime configuration and changes.
- [x] Performance and resource behaviour — measured workload and resource characteristics.
- [x] Review facet boundaries and cross-facet relationships.
- [x] Create a catalogue and explicit boundary/overlap matrix.
- [x] Define observation unit, conceptual payload dimensions, scenario requirements, evidence, limitations, and cross-facet links for every facet.
- [x] Add a worked conceptual example to every facet specification.

**Phase 3 exit gate: satisfied at the specification level.** All 15 facets have a boundary, conceptual typed payload inventory, evidence model, limitations, and illustrative worked example. These examples are not empirical captures. Machine schemas remain Phase 4; empirical end-to-end examples and conformance fixtures remain Phase 6.

## Phase 4 — Machine-readable schemas

- [x] Define schema conventions, dialect, identifiers, draft version, and extension policy.
- [x] Capture manifest schema.
- [x] Common target, coverage, scenario, execution, and observation record schemas.
- [x] Separate runtime-rule, source-derived-rule, and declared-contract schemas.
- [x] Evidence/provenance schema.
- [x] Typed payload schemas for all 15 facets.
- [x] Structural comparison-report envelope (comparison semantics deferred to Phase 5).
- [x] Positive and negative validation fixtures.
- [x] Automated validation runner and instructions.
- [x] Execute validation and verify expected fixture outcomes.
- [x] Document schema evolution and validation boundaries.

**Phase 4 exit gate: satisfied.** GitHub Actions run [#2](https://github.com/REMAREMA6/software-rules/actions/runs/45792470335) completed successfully on 2026-11-26. Ajv 2020-12 validated the valid fixture and rejected all three negative fixtures for the expected structural reasons. The schemas remain Draft version 0.1.0 in the intended v1 compatibility family; they are not a stable release. Cross-record reference integrity and evidence authenticity remain outside JSON Schema validation.

## Phase 5 — Canonicalization and comparison

- [x] Define capture alignment and identity matching.
- [x] Define normalization without loss of meaningful distinctions.
- [x] Define comparison bases: exact, normalized, semantic, and tolerance-based.
- [x] Define match, mismatch, missing, additional, unknown, conflicting, and not-comparable results.
- [x] Define missingness decision order; missing evidence never becomes a match.
- [x] Define coverage and bounded-equivalence reporting.
- [x] Expand comparison report schema.
- [x] Create and review a comparison example.
- [x] Add valid and invalid comparison fixtures to automated CI.

**Phase 5 exit gate: satisfied.** GitHub Actions run [#4](https://github.com/REMAREMA6/software-rules/actions/runs/45793398830) passed the capture and comparison fixture suites. The valid comparison example passed; the invalid report claiming universal equivalence was rejected. The example is illustrative, not empirical. Active work moved to Phase 6.

## Phase 6 — Cross-repository, cross-stack replication and conformance

**Status: [~] In progress.** Phase 6 uses multiple source repositories and a separate independent replication project. One application is not expected to implement all 15 facets. See [the full programme](examples/CROSS-REPOSITORY-REPLICATION-PROGRAM.md).

### Agreed operating model
- [x] Each facet may use a different source repository.
- [x] A separate independent replication project is required.
- [x] Rules must be extracted into a technology-independent specification before implementation.
- [x] Equivalent source/replica probes, comparison, and mutation detection are required.
- [x] Create the replication-lab skeleton, case template, source register, and source-record template.
- [x] Register and inspect fifteen immutable source repositories; source candidates remain distinct from accepted bounded cases.
- [x] Accept bounded BullMQ retry/backoff and Express routing/API cross-stack cases after reviewing successful runtime runs and retained artifacts.
- [x] TORM-PERSIST-001: TypeORM 1.1.3 pinned source + SQL.js versus Python 3.12 sqlite3; two scenarios, eight semantic projections, six mutations, schema 0.2.0 capture/report validation, and evidence integrity passed.
- [x] BMQ-MSG-001: BullMQ pinned source + Redis versus Python queue model; two scenarios, ten semantic projections, six mutations, Software Rules 0.2.0 capture/report validation, and evidence integrity passed in run [#45929249126](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126).
- [x] JOSE-AUTH-001: pinned jose 6.2.18 / Node.js WebCrypto versus Python 3.12 HMAC/JWT verifier; eleven scenarios, 55 facet/scenario projections, eight mutations, schema/report validation, and evidence integrity passed in run [#45930973956](https://github.com/REMAREMA6/software-rules/actions/runs/45930973956).
- [x] CASBIN-AUTHZ-001: pinned Apache Casbin Go source versus independent Python simple-RBAC evaluator; ten authorization requests, four executable mutations, Software Rules 0.2.0 captures, schema/report validation, and evidence integrity passed in run [#45931911753](https://github.com/REMAREMA6/software-rules/actions/runs/45931911753). Retained artifact ID `15168623669`.
- [x] REDIS-INT-001: pinned go-redis Go client versus independent Python redis-py against Redis 7; seven operations, five executable mutations, Software Rules 0.2.0 captures, schema/report validation, and evidence integrity passed in run [#45932496414](https://github.com/REMAREMA6/software-rules/actions/runs/45932496414). Retained artifact ID `15168909418`.
- [x] TASKBOARD-UI-001: independent React 19/Vite replica of the plain HTML/CSS Task Board passed nine viewport/state comparisons, semantic/API-trace checks, mutation detection, Software Rules 0.2.0 capture/report validation, and evidence integrity in run [#45934802401](https://github.com/REMAREMA6/software-rules/actions/runs/45934802401); artifact `15170370565` retained through 2026-12-27.
- [ ] Add broader commerce cases (cart, discount, tax, eligibility); extend identity/session lifecycle, TLS/proxy/retry integration, performance scaling, and incomplete property inventories.
- [x] BMQ-ER-002: BullMQ pinned TypeScript/Node.js + Redis source versus Python model; three scenarios, 12 semantic projections, mutation tests, schema/integrity validation, evidence retained..
- [ ] Complete the final evidence and coverage audit.

### Existing bounded evidence
- [x] Task Board reference, independent, and deliberately mutated implementations.
- [x] 13-state interface comparison, including three viewport widths, focus, hover, and colour-scheme preference, pixel-identical under recorded CI conditions.
- [x] Initial behaviour, business-rule, data, in-memory API adapter, error, limited security-output, and performance samples.
- [x] Runtime artifact and integrity/schema/comparison workflows recorded in the Task Board audit.
- [ ] Resolve Task Board's remaining partial properties if still in its declared scope; otherwise explicitly constrain that fixture's scope with evidence and justification.

### Fifteen-facet cross-repository programme

See the [living 15-facet evidence matrix](conformance/replication-lab/FACET-COVERAGE.md) for source candidates, current evidence, replica status, and blockers per facet.
- [ ] 1. Interface — screen/state capture and independent UI-stack replication.
- [ ] 2. Behaviour — triggers, transitions, side effects, ordering, and failure replication.
- [~] 3. Business rules — date validation, calculated/original price selection, adjustment/tax allocation, promotion rule operators/context eligibility, and Task Board title/count rules pass; full cart totals, promotion application/precedence, campaign budgets/usage, quantity tiers, currency normalization, shipping discounts, and checkout remain open.
- [ ] 4. Data — shapes, types, nullability, relationships, transformations, and serialization.
- [~] 5. Persistence — bounded TypeORM top-level commit/rollback case passed; durability/restart/concurrency and other drivers remain uncovered.
- [~] 6. API — Express routing case passed; payload validation/authentication/pagination/concurrency and broader failure contracts remain uncovered.
- [~] 7. Messaging — BullMQ duplicate-ID, event-order, completion, and failed-consumer runtime comparison, six mutations, schema-native captures, and evidence validation passed; delivery guarantees and idempotency breadth remain uncovered.
- [~] 8. Identity/authentication — bounded JWT signature/claims verification passes; principal establishment, credential/session lifecycle, refresh, revocation, and logout remain uncovered.
- [~] 9. Authorization — simple RBAC plus bounded domain RBAC, ABAC, deny override, and policy mutation pass; other role hierarchies, priorities, resource-role models, and policy adapters remain open.
- [~] 10. Security — bounded JWT signature-integrity and algorithm-allowlist controls pass; broader authorized bypass, containment, and security-control cases remain uncovered.
- [~] 11. Background processing — BullMQ retry/backoff case passed; scheduling/cancellation/duplicate/stalled-worker lifecycle remain uncovered.
- [~] 12. Errors/recovery — bounded BullMQ retry/suppression, Express 404, TypeORM rollback, Medusa invalid-date, and JOSE semantic JWT rejection cases passed; broader failure/recovery classes remain uncovered.
- [~] 13. Integrations — seven Redis operations and nine Axios HTTP interactions pass; TLS, proxies, credentials, retries, cancellation, and provider variability remain open.
- [~] 14. Configuration — Express routing defaults passed; precedence/invalid values/runtime changes remain uncovered.
- [~] 15. Performance/resources — three repeated Prometheus workload runs and independent model comparison pass; scaling, concurrency, latency distributions, saturation, and resource budgets remain open.

### Rule-level completion checklist
- [ ] Source repository, immutable commit, licence, runtime, and system boundary recorded.
- [ ] Runtime observations, source-derived inferences, and declared contracts distinguished.
- [ ] Technology-independent rule and facet payload captured.
- [ ] Independent replica implemented in a different stack.
- [ ] Equivalent normal, boundary, negative, and failure scenarios executed where applicable.
- [ ] Captures compared with no unexplained required mismatch or coverage gap.
- [ ] Meaningful mutation detected.
- [ ] Evidence, provenance, cross-facet links, and reproduction instructions retained.

**Current blocker:** twenty bounded cross-stack cases pass, but no entire facet is complete for the full objective. Authorization now covers simple RBAC plus bounded domain RBAC, ABAC, deny override, and policy mutation; broader models remain open. Integrations now cover seven Redis operations and nine Axios/urllib HTTP interactions; TLS, proxies, credentials, retries, cancellation, and provider-specific behaviours remain open. Security covers limited JWT controls and output encoding. PROM-PERF-001 passes a bounded workload case; broader performance properties remain open. The independent UI-stack gap is closed only for the bounded Task Board scope. Business rules now include date validation, price selection, tax/adjustment allocation, and promotion eligibility; discount application, cart totals, campaign budgets, and checkout remain open. Data, persistence, API, messaging, background processing, errors, and configuration have unresolved property inventories. TypeORM now covers top-level transactions and bounded file-backed reopen durability; concurrency, isolation, power-loss, and driver differences remain open. EXP-CONFIG-001 and VIPER-CONFIG-001 cover bounded routing and source-precedence configuration classes; remote providers, reload/watch, secrets, and multi-file merge remain open. The Task Board-only approach remains superseded. Do not claim Phase 6 complete until every 15-facet exit-gate requirement is evidenced.


### 2026-11-27 — JOSE JWT authentication/security case accepted

- [x] Pinned `panva/jose` source commit `f4457b3e3c5a40359b40ad6fa9721d11aa2a2bd0` (jose 6.2.18), compiled with TypeScript 6.0.2, and executed the source runtime on Node.js 22.
- [x] Compared eleven source-generated compact JWT scenarios against an independent Python 3.12 standard-library HMAC/JWT verifier; all 55 facet/scenario projections matched.
- [x] Detected eight executable verifier mutations covering signature, expiration, not-before, issuer, audience, algorithm allowlist, and required-claim checks.
- [x] Generated Software Rules 0.2.0 source/replica captures and comparison report; schema validation, comparison validation, and evidence-integrity validation passed in [run #45930973956](https://github.com/REMAREMA6/software-rules/actions/runs/45930973956).
- [x] Committed source/replica captures, comparison, pinned source excerpts, licence, and toolchain metadata under `conformance/replication-lab/cases/JOSE-AUTH-001/artifacts/` at commit [21334ff](https://github.com/REMAREMA6/software-rules/commit/21334ff55fe9ef5b29adc846ea8a49dfe849a80f); retained CI artifact ID `15168682159`.
- [~] This is bounded JWT verification evidence, not complete identity-provider, session, authorization, or security-facet coverage.


### 2026-11-27 — Casbin RBAC authorization case accepted

- [x] Pinned Apache Casbin commit `fa4023fd7d02d9b7d023515e76b19b3be637f613` and executed the Go enforcer against ten subject/resource/action requests.
- [x] Compared all ten source decisions with an independent Python 3.12 simple-RBAC model; no decision mismatch.
- [x] Detected four executable mutations: removed role relation, removed resource equality, removed action equality, and default-allow behaviour.
- [x] Generated Software Rules 0.2.0 captures and comparison; schema validation, cross-record integrity, and ten matching comparison results passed in [run #45931911753](https://github.com/REMAREMA6/software-rules/actions/runs/45931911753).
- [x] Retained source, replica, and Software Rules evidence in CI artifact `15168623669` (expires 2026-12-27).
- [~] This proves only the declared simple-RBAC scope; it does not complete the authorization facet.


### 2026-11-27 — Redis client integration case accepted

- [x] Pinned `redis/go-redis` commit `37d4d98e2ccf59df4973df3e5de9edc87492426b` and executed the Go client against an isolated Redis 7 service.
- [x] Compared seven normalized interactions with an independent Python 3.12 / redis-py client: PING, SET/GET, missing key, EXISTS, PTTL, WRONGTYPE, and connection failure.
- [x] Detected five executable mutations: skipped write, missing-value substitution, wrong-type suppression, zero TTL, and connection-failure suppression.
- [x] Generated Software Rules 0.2.0 source/replica captures and comparison; schema validation, cross-record integrity, and seven matching results passed in [run #45932496414](https://github.com/REMAREMA6/software-rules/actions/runs/45932496414).
- [x] Retained source, replica, and Software Rules evidence in CI artifact `15168909418` (expires 2026-12-27).
- [~] This proves only the declared seven-operation Redis boundary; it does not complete the integrations facet.

## Phase 7 — Review, release, and maintenance

**Status: [ ] Not started — blocked by Phase 6.**

- [ ] Review terminology, facet boundaries, provenance, schemas, and examples.
- [ ] Verify completeness and comparison claims against evidence.
- [ ] Document known limitations and unresolved issues.
- [ ] Publish a versioned specification release.
- [ ] Define maintenance and change process.

## Decision log

| ID | Decision | Status | Record |
|---|---|---|---|
| D-001 | Keep runtime-observed rules distinct from source-derived rules. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-002 | Use a shared conceptual envelope with facet-specific typed payloads. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md); serialization remains deferred. |
| D-003 | Bound equivalence claims to captured scenarios and evidence. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-004 | Compose existing standards; no reviewed standard supplies the complete capture-and-comparison format. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-005 | Keep declared contracts distinct from runtime observations. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-006 | Expand the facet taxonomy with configuration, performance/resource behaviour, and clearer identity/access boundaries. | Proposed | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md); validate in Phase 3. |
| D-007 | Separate scenario definitions, executions, and observations. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-008 | Treat rules as propositions supported/qualified/contradicted by observations. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-009 | Keep expected outcomes, actual outcomes, and evaluations separate. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-012 | Use evidence-backed alignment, loss-aware normalization, explicit result classes, and bounded comparison conclusions. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |\n| D-013 | Require evidence-backed, replication-sufficient captures for the declared scope; completeness is separate from observed agreement. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |

## Work log

### 2026-11-26
- Completed Phase 4: added the draft 0.1.0 capture and record schemas, all 15 typed facet payload schemas, and validation fixtures. GitHub Actions run #2 passed the four fixture expectations using Ajv 2020-12.
- Completed Phase 5: defined matching, normalization, comparison bases, result classification, coverage, and bounded conclusions; expanded the report schema and added comparison fixtures. GitHub Actions run #4 passed the capture and comparison fixture suites. The comparison example is illustrative, not empirical. Active work moved to Phase 6.
- Completed Phase 0 governance: added the contribution guide, changelog, design-decision log, and versioning policy.
- Completed Phase 1 research: reviewed candidate standards and prior art, collected authoritative references, documented limitations, and proposed the revised facet taxonomy.
- Completed Phase 2: added the core conceptual documents; separated scenario definitions, executions, observations, evidence, runtime rules, source-derived rules, and declared contracts; tested the model against interface and API examples.
- Accepted D-002 and recorded D-007 through D-009.
- Completed Phase 3: added the 15-facet catalogue, boundary/overlap matrix, and an individual specification for every facet. Each facet includes its scope, observation unit, conceptual payload dimensions, scenario requirements, evidence expectations, limitations, cross-facet links, and an illustrative worked example.
- Accepted D-010, the 15-facet catalogue for this specification draft. Phase 3 examples are illustrative model tests, not empirical captures. Machine schemas remain Phase 4; empirical end-to-end captures remain Phase 6.
- Verified the Phase 3 files and project navigation on GitHub. Active work moved to Phase 4: machine-readable schemas.



### Phase 6 initial completeness work — 2026-11-26

- [x] Record the Replication Completeness Rule as an accepted project requirement.
- [x] Require a declared replication scope and per-property inventory in the capture schema.
- [x] Require comparisons to report replication completeness separately from observed agreement.
- [x] Add cross-record integrity checks for unique inventory IDs, facet declarations, observation/evidence references, and false complete claims.
- [x] Add Task Board inventories for interface, behaviour, and API properties.
- [x] Bump the incompatible draft capture/report format from 0.1.0 to 0.2.0 and update the valid fixtures.
- [x] Audit all three inventories: 22 properties each; every required property is captured or explicitly not applicable, and optional exclusions have reasons.
- [x] Add tests rejecting a complete status when required properties are partial or unresolved.
- [x] Expand reference, independent, and mutated runtime captures to cover all required properties in the declared Task Board scope.
- [x] Capture full per-element computed CSS properties, DOM hierarchy, pseudo-element content, geometry, accessibility snapshots, and screenshots for every declared UI state.
- [x] Compare reference and independent baseline screenshots pixel-for-pixel across seven states; all seven comparisons have zero differing pixels.
- [x] Preserve and detect the deliberate mutation; its one-active screenshot differs by 272 pixels.
- [x] Execute empty/whitespace validation, keyboard-only create/filter/complete/delete, API success, and HTTP 503 failure scenarios.
- [x] Update all three capture records, schema fixtures, and both comparison reports with runtime evidence and completeness conclusions.
- [x] Re-run schema validation and cross-record integrity checks; both pass.

**Phase 6 redo result:** Complete for the declared Task Board replication scope. The three captures each account for all 22 inventory properties: 18 captured, one explicitly not applicable, and three optional dimensions explicitly excluded. The reference and independent baseline are pixel-identical in seven tested UI states at 1280×800 CSS px under Chromium 159.0.8154.6 on Linux. Keyboard, validation, API request/response, and failure outcomes agree. The mutated implementation remains fully captured but comparison correctly reports its deliberate pluralization mismatch. Runtime evidence: [successful Playwright run #45855076741](https://github.com/REMAREMA6/software-rules/actions/runs/45855076741), [capture artifact](https://github.com/REMAREMA6/software-rules/actions/runs/45854435953/artifacts/15136130524). Final schema and integrity validation: [run #45855135858](https://github.com/REMAREMA6/software-rules/actions/runs/45855135858).

**Boundary:** This proves completeness and pixel identity only for the declared Task Board scope and captured environment. It does not prove universal equivalence across every stack, browser, operating system, viewport, or arbitrary software system. Phase 7 is now active.


### Phase 6 expansion — 2026-11-26

- Reframed Phase 6 as the complete multi-facet empirical capture and conformance programme, rather than treating the initial Task Board fixture as the final scope.
- Kept the existing interface/behaviour/API runtime work as a bounded baseline. It does not establish complete interface capture or coverage of other software facets.
- Ordered the remaining work: interface evidence audit; behaviour/functionality; business rules; data; persistence; API/messaging/integrations; identity/authorization/security; background processing/errors/configuration/performance; cross-facet completeness.
- Phase 7 is blocked until the expanded Phase 6 exit gate is satisfied.
- Next action: extend the Playwright harness with title boundary cases, duplicate titles, mixed-task state/count truth tables, repeated toggles/deletes, malformed/unknown-ID API operations, and exact request/response data-shape capture.


### Phase 6A audit result — 2026-11-26

- Inspected the three capture inventories, evidence records, observation payloads, and integrity validator.
- Confirmed that the old reference interface observation itself explicitly reported partial completeness for its main-control snapshot; the later Playwright archive contains richer detail, but the inventory had no separate property for the font-rendering limitation.
- Added an explicit partial font-rendering property and partial business-rule/data observations to each Task Board capture. These include only the facts supported by the existing one-task workflow and in-memory API samples.
- Added six further partial rule/data properties across title normalization, initial completion state, summary counts, task record shape, identifier generation, and PATCH field-preservation semantics.
- Updated all three captures to 29 inventory entries: 18 captured, seven partial, one not applicable, and three optional exclusions. Completeness is now incomplete.
- Updated equivalent and deliberate-difference reports to preserve observed comparison results while reporting incomplete-both.
- Updated integrity tests to expect the Task Board captures to remain incomplete.
- Audit finding: the integrity validator checks reference existence, facet labels, and declared statuses; it does not verify that the linked evidence semantically proves the property or that the inventory is exhaustive. This limitation is now explicit. Stronger evidence-quality checks remain active work.


### Phase 6B probe implementation — 2026-11-26

- Added an expanded Playwright probe sequence to the runtime harness for leading/trailing whitespace normalization, duplicate titles, HTML-like/Unicode title safety, 512-character titles, mixed active/completed records, filter counts, completion toggle-back, deletion, and identifier samples.
- Added request/response synchronization and explicit outcome assertions so the test does not mistake a click for a completed asynchronous operation.
- The harness retains the probe results in the per-variant runtime output. This initial implementation was subsequently executed successfully in run #45858743131; verified results are recorded in the later work-log entry.


- Added .github/workflows/phase6-expanded-conformance.yml to run the expanded Playwright capture, evidence-link integrity tests, schema validation, and artifact upload on relevant pushes and pull requests. The workflow has been added; its first execution result still needs verification.


### Phase 6 expanded probe execution — 2026-11-26

- Corrected a Playwright strict-mode selector ambiguity found in the first workflow attempt; filter button locators now require exact accessible-name matches.
- Successful run: [GitHub Actions #45858743131](https://github.com/REMAREMA6/software-rules/actions/runs/45858743131). Runtime capture, cross-record/evidence-link integrity, and JSON Schema/comparison validation all passed.
- Retained 41 runtime artifact files in [artifact #15136459580](https://github.com/REMAREMA6/software-rules/actions/runs/45858743131/artifacts/15136459580), including three variant captures and expanded probe results.
- All three variants agreed on title trimming, duplicate acceptance, literal HTML-like/Unicode rendering, 512-character title acceptance, mixed-state counts/filters, completion toggle-back, PATCH field preservation, and three-task deletion.
- Updated all three captures with the new scenario, execution, evidence, and observations. Inventory now has 34 entries per capture: 28 captured, two partial, one not applicable, and three optional exclusions.
- Updated comparison coverage to 28 observed/captured units and two partial units; all reports remain incomplete-both.
- Remaining partial properties: font rendering beyond the recorded Chromium/Linux conditions and maximum title-length constraint.


- Updated the Phase 6 facet-expansion document with current 6B–6D progress and a clear statement of which facets the Task Board does not exercise.
- The latest documentation/capture validation run #45859552354 also completed successfully.

- Post-update verification: [run #45859279008](https://github.com/REMAREMA6/software-rules/actions/runs/45859279008) passed after the 34-entry capture inventories and comparison reports were updated; [run #45859552354](https://github.com/REMAREMA6/software-rules/actions/runs/45859552354) also passed after the latest documentation/plan updates.


### Supplemental Phase 6 probe expansion — 2026-11-26

- Expanded the runtime harness with responsive viewports (320×720, 768×900, 1920×1080), focus/hover/dark-colour-scheme states, SVG/script-shaped input probes, HTTP 503 failures for create/update/delete, and browser navigation/paint/resource measurements.
- Successful runtime workflow: [#45860499892](https://github.com/REMAREMA6/software-rules/actions/runs/45860499892). All 13 baseline UI screenshot comparisons were pixel-identical; the deliberate mutation remained detectable at 272 differing pixels.
- Runtime results: no horizontal overflow at the three tested widths; focus and hover states were reached; no disabled controls exist in the fixture; SVG/script-shaped titles were rendered literally with no injected SVG/script/image and no payload execution; all three failed API operations returned 503 and produced unhandled page errors with no user-facing recovery UI.
- Single-run local performance samples were recorded: navigation load event end 8.1–8.9 ms, first contentful paint 16 ms, and 14 resources per variant. These are CI-host measurements, not performance guarantees.
- Artifact: [#15137373210](https://github.com/REMAREMA6/software-rules/actions/runs/45860499892/artifacts/15137373210), 65 files, 30-day retention.
- Added `examples/task-board/FACET-APPLICABILITY.md`. It explicitly separates the five facets exercised by Task Board from facets absent from this fixture. It does not mark the project-wide Phase 6 complete.

- Task Board supplemental evidence now spans eight facets: interface, behaviour, business rules, data, API adapter, errors/recovery, limited security output encoding, and single-run performance. The three captures contain 38 inventory entries each (33 captured, two partial, one not applicable, two excluded) and remain explicitly incomplete.

- Corrected an intermittent screenshot race by waiting for PATCH/DELETE responses and the resulting DOM state before saving the pointer workflow. [Run #45861726449](https://github.com/REMAREMA6/software-rules/actions/runs/45861726449) passed runtime capture, cross-record integrity, and schema/comparison validation. Artifact #15137768292 contains the corrected 65-file evidence archive.


### Cross-repository Phase 6 implementation — 2026-11-26

- Replaced the single-rich-reference-target assumption with a multi-repository validation strategy. The source repository for each rule is selected according to the facet it actually demonstrates; an independent replication lab implements the extracted rule in a different stack.
- Added the full 15-facet matrix, source register requirements, independent replication layout, rule-level pass criteria, mutation requirement, and Phase 6 exit gate in examples/CROSS-REPOSITORY-REPLICATION-PROGRAM.md.
- Updated PLAN.md, TRACKER.md, and CHANGELOG.md to use the cross-repository strategy.
- Created conformance/replication-lab with case and source templates, shared layout, and Python test workflow.
- Registered fifteen source repositories with pinned commits and licence notes: BullMQ, Keycloak, OWASP Juice Shop, Grafana, TypeORM, n8n, Prometheus, Express, Medusa, Apache Casbin, and go-redis. Candidate status remains distinct from accepted bounded cases.
- Inspected BullMQ retry/backoff source, guide, and tests at commit 526668f2c5e6de9d5d664df577f09a6bdccac1b4. Added a source-derived Software Rules capture with two unverified rules and an explicitly incomplete scope.
- Added a narrow independent Python retry-decision model and eight tests, including an off-by-one mutation check. The Python rule-model, replica-simulation, and comparison mutation tests passed in GitHub Actions run [#4](https://github.com/REMAREMA6/software-rules/actions/runs/45923895261). The BullMQ source runtime workflow now checks out the exact source commit, starts Redis, builds BullMQ, captures three retry scenarios, generates the independent Python capture, and compares the results. The runtime workflow is still running; no source/replica pass is claimed.
- No Phase 6 completion claim is made. The current work demonstrates the cross-repository process has begun, not that all 15 facets have passed.


### 2026-11-27 — Phase 6 execution audit and corrected handoff

- Re-read the current plan, tracker, cross-repository programme, BullMQ case, Python replica, test module, workflow, and source capture.
- Confirmed the Python workflow runs only the isolated Python decision-model tests; it does not execute BullMQ, Redis, or an end-to-end queue scenario.
- Confirmed the BullMQ source capture is correctly marked source-inferred/unverified and incomplete. It is not a runtime capture and must not be used as proof of source/replica equivalence.
- Reconfirmed the pinned BullMQ package version at the selected commit is 6.7.10 and its package test command is Vitest. Runtime harness design must use the exact pinned source and Redis-backed test setup, not substitute a current npm release.
- Corrected the source register count to eleven repositories; individual rule cases must still pass before being accepted.
- Immediate execution order: (1) make the Python model's test run reproducible and verify its workflow; (2) build a pinned-commit BullMQ+Redis runtime probe and record actual outputs; (3) capture the independent implementation in a genuinely different stack; (4) compare both captures and mutation-test; (5) repeat for every required rule/property across all 15 facets.
- Phase 6 remains in progress; Phase 7 remains blocked. No completion claim is made.


### 2026-11-27 — Cross-stack case execution progress

- [x] Added a BullMQ pinned-commit runtime workflow with a Redis 7 service and an assertion-bearing probe for positive backoff, -1 suppression, zero-delay retry, attempt limits, terminal states, and observed event traces.
- [x] Fixed the workflow's unsupported `setup-node cache: none` configuration after the first two attempts failed before source checkout. Those failures were infrastructure/configuration failures, not BullMQ test failures.
- [x] Confirmed the Python rule-model workflow passes; the latest run also executes the independent scenario simulator and comparison mutation tests (run [#4](https://github.com/REMAREMA6/software-rules/actions/runs/45923895261)).
- [x] Added the BullMQ source-derived capture as a schema-valid fixture.
- [x] Corrected the cross-record validator so source-inferred properties may link directly to source-artifact evidence without fabricating runtime observations; it rejects runtime evidence misclassified as source-only evidence.
- [x] Schema and cross-record validation passed after that correction (run [#87](https://github.com/REMAREMA6/software-rules/actions/runs/45923807641)).
- [~] Pinned BullMQ runtime build/probe and Python-vs-source comparison are still executing in GitHub Actions. Do not count this case as passed until the workflow and artifacts are reviewed.


### Runtime workflow audit — 2026-11-27

- [x] Inspected artifacts from the first two green BullMQ workflow runs rather than accepting the job conclusion alone.
- [x] Found that the source runtime capture and comparison report were empty. The -1 scenario timed out because the probe checked the recorded attempt number instead of the backoff result; shell pipelines also lacked `pipefail`, masking the failed Node/Python commands behind successful `tee` processes.
- [x] Corrected the suppression assertion to inspect the returned backoff value, added explicit Redis/worker cleanup, and enabled `pipefail` for source-probe and comparison pipelines.
- [~] Re-run the pinned-source workflow and inspect non-empty source, replica, and comparison artifacts. Previous green runs are explicitly not counted as conformance evidence.


### 2026-11-27 — Bounded BullMQ cross-stack case accepted

- [x] Pinned BullMQ 6.7.10 to commit `526668f2c5e6de9d5d664df577f09a6bdccac1b4` and executed three scenarios with Redis 7.
- [x] Independently reproduced the retry decision model in Python 3.12.
- [x] Matched 12 semantic projections across background-processing, errors-recovery, data, and behavior.
- [x] Mutation tests detect off-by-one attempt limits, altered processor counts, backoff values, and transition sequences.
- [x] Generated and validated source/replica Software Rules 0.2.0 captures and the comparison report.
- [x] Committed six raw/structured evidence files under `conformance/replication-lab/cases/BMQ-ER-002/artifacts/` at commit [513766d](https://github.com/REMAREMA6/software-rules/commit/513766df3b9d4300df4c9297b79f221b54e29e42).
- [~] Phase 6 remains active: this proves portability only for the declared retry/backoff properties and three scenarios. Continue with Express API and the remaining facets.


### 2026-11-27 — Bounded Express API/routing case accepted

- [x] Pinned Express 5.3.0 to commit `43fca52d28a422c8be48fd489cbd4f2d6152bab6`; generated and retained a dependency lockfile because the source commit has no lockfile.
- [x] Executed seven HTTP requests against Express and an independent Python 3.12 HTTP server.
- [x] Matched 28 facet/scenario projections across API, behaviour, configuration, and errors/recovery.
- [x] Executable mutations detected incorrect HEAD wire-body handling, OPTIONS method enumeration/precedence, case-sensitive routing, strict trailing-slash matching, and query-path matching.
- [x] Generated and validated Software Rules 0.2.0 captures and the comparison report.
- [x] Committed raw/structured captures, comparison, package lock, and dependency tree under `conformance/replication-lab/cases/EXP-API-001/artifacts/` at commit [ad30376](https://github.com/REMAREMA6/software-rules/commit/ad3037693d32221a6d7bdb6b9883c45db7b2be9c).
- [~] Phase 6 remains active; this case proves only the declared seven-request scope, not complete Express/API coverage.


### 2026-11-27 — Cross-stack evidence audit and TypeORM case start

- [x] Re-checked GitHub Actions job steps and retained artifacts for BullMQ run [#45925568609](https://github.com/REMAREMA6/software-rules/actions/runs/45925568609): all source checkout/build/runtime, replica, comparison, schema/integrity, and artifact-retention steps succeeded.
- [x] Re-checked GitHub Actions job steps and retained artifacts for Express run [#45926714897](https://github.com/REMAREMA6/software-rules/actions/runs/45926714897): all pinned source runtime, Python replica, comparison, mutation/schema/integrity, and evidence-retention steps succeeded.
- [x] Corrected the facet evidence matrix to distinguish bounded case passes from facet-wide completeness.
- [x] Inspected TypeORM transaction manager and SQLite-compatible query-runner implementation at the registered immutable commit.
- [x] Added TORM-PERSIST-001 source probe, independent Python/sqlite3 model, comparator, mutation tests, and pinned-source CI workflow.
- [x] At the time of this entry, TypeORM workflow execution and generated runtime evidence were pending; this was superseded by the successful source/replica, mutation, schema, and integrity run recorded in the 2026-11-27 verification entry below.
- [ ] Messaging, identity/authentication, authorization, dedicated security, integrations, business rules, and repeatable performance/resource cases remain unimplemented or incomplete.


### 2026-11-27 — Bounded TypeORM transaction case accepted

- [x] Pinned TypeORM 1.1.3 to commit `b1e211fc2654d412612a08f8a7fb890f3352614f`; installed the frozen pnpm workspace dependencies and compiled the Node entrypoint.
- [x] Executed successful commit and NOT NULL failure/rollback scenarios with better-sqlite3.
- [x] Reproduced transaction commit/rollback semantics independently in Python 3.12/sqlite3.
- [x] Matched eight facet/scenario projections across persistence, data, behaviour, and errors/recovery.
- [x] Detected the executable commit-on-error mutation.
- [x] Generated and validated Software Rules 0.2.0 captures and the comparison report.
- [x] Committed raw/structured captures, frozen pnpm lockfile, and dependency tree under `conformance/replication-lab/cases/TYPEORM-PERSIST-001/artifacts/` at commit [fabf45a](https://github.com/REMAREMA6/software-rules/commit/fabf45ae466d2b68bcc49f6596f6c6bb220ddef3).
- [~] Phase 6 remains active; this case proves only the declared two-scenario transaction scope.


### 2026-11-27 — TypeORM persistence and BullMQ messaging case preparation

- [x] Inspected TypeORM EntityManager transaction handling and SQLite-compatible QueryRunner implementation at immutable commit `b1e211fc2654d412612a08f8a7fb890f3352614f`.
- [x] Added TORM-PERSIST-001 with a pinned-source compile/runtime workflow, SQL.js transaction probe, independent Python sqlite3 replica, comparator, and mutation tests.
- [x] Ran the Python/sqlite3 model logic locally in the analysis environment; rollback, original-error propagation, commit visibility, and callback return assertions passed. This does not establish TypeORM source-runtime equivalence.
- [x] Added BMQ-MSG-001 using pinned BullMQ source commit `526668f2c5e6de9d5d664df577f09a6bdccac1b4`: duplicate custom job ID suppression, stored-payload precedence, queue event sequence, successful completion, and terminal consumer failure.
- [x] Added independent Python queue model, comparator mutation tests, and Redis-backed pinned-source workflow for BMQ-MSG-001.
- [x] Ran the Python messaging model logic locally in the analysis environment; duplicate suppression, one processing outcome, completion acknowledgement, and failed-consumer terminal state assertions passed. This does not establish BullMQ source-runtime equivalence.
- [x] At the time of this entry, TypeORM and BullMQ messaging runtime/schema results were still unverified; this historical status was superseded by the successful runs recorded below.


### 2026-11-27 — Bounded Medusa date-validation case accepted

- [x] Pinned Medusa commit `6e28e10acb9676392315b3ff1a9c7147fce4b5ab` and executed the exact price-list validator, `isDate`, and `MedusaError` helper source files.
- [x] Compared ten optional/valid/invalid/Date-object/reversed-range inputs with an independent Python 3.12 ISO-8601 implementation.
- [x] Matched 40 facet/scenario projections across business rules, data, behaviour, and errors/recovery.
- [x] Detected four executable mutations: empty-string rejection, skipped end-date validation, added chronology enforcement, and reversed validation order.
- [x] Generated and validated Software Rules 0.2.0 captures and comparison report.
- [x] Committed source files, raw/structured captures, comparison, and TypeScript toolchain lock under `conformance/replication-lab/cases/MEDUSA-BR-001/artifacts/` at [dd0ad76](https://github.com/REMAREMA6/software-rules/commit/dd0ad76f0ec9557a41250c5fcc3efa14dc5aa1a2).
- [~] Phase 6 remains active; this case does not cover full Medusa pricing or the entire business-rules facet.


### 2026-11-27 — TypeORM and BullMQ messaging runtime verification

- [x] TORM-PERSIST-001: pinned TypeORM 1.1.3 source commit `b1e211fc2654d412612a08f8a7fb890f3352614f` compiled and executed with SQL.js; independent Python 3.12 sqlite3 replica matched two scenarios and eight facet/scenario projections.
- [x] TORM-PERSIST-001: six mutation tests passed; Software Rules 0.2.0 source/replica captures and comparison report passed schema and evidence-integrity validation in run [#45928766010](https://github.com/REMAREMA6/software-rules/actions/runs/45928766010). Artifact ID `15167104492`, retained until 2026-12-27.
- [x] BMQ-MSG-001: pinned BullMQ 6.7.10 source commit `526668f2c5e6de9d5d664df577f09a6bdccac1b4` + Redis 7 matched an independent Python queue model across duplicate-ID and consumer-failure scenarios; ten semantic projections matched.
- [x] BMQ-MSG-001: six mutation tests passed in run [#45928721261](https://github.com/REMAREMA6/software-rules/actions/runs/45928721261). Artifact ID `15167806675`, retained until 2026-12-27.
- [x] BMQ-MSG-001 schema-native captures, comparison report, schema validation, and evidence-integrity validation passed in run [#45929249126](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126); committed evidence is recorded below.
- [ ] Continue with identity/session lifecycle, additional authorization models, dedicated security controls, external HTTP integrations, broader commerce rules, and expanded performance/resource behaviour. No facet-wide completion claim.


### 2026-11-27 — Bounded BullMQ messaging case accepted

- [x] Executed two pinned BullMQ/Redis scenarios: duplicate custom job ID and terminal consumer failure.
- [x] Compared queue event order, processed payload, terminal acknowledgement/failure state, and job counts against an independent Python model.
- [x] Matched ten facet/scenario projections across messaging, background processing, behaviour, errors/recovery, and data.
- [x] Detected five executable replica mutations: duplicate delivery, payload overwrite, missing completion acknowledgement, event reordering, and failed-to-completed state mutation.
- [x] Generated and validated Software Rules 0.2.0 captures and comparison report.
- [x] Committed raw/structured captures and comparison under `conformance/replication-lab/cases/BMQ-MSG-001/artifacts/` at [ce9d0e1](https://github.com/REMAREMA6/software-rules/commit/ce9d0e1a0c62830418daa912c1a798561c897a3a).
- [~] Phase 6 remains active; the case does not establish exactly-once delivery or all messaging semantics.
