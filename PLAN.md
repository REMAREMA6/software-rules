# Project Plan

**Project:** Software Rules  
**Repository:** REMAREMA6/software-rules  
**Status:** Phase 6 — cross-repository, cross-stack replication and conformance in progress; seventeen bounded cases pass: the eight original cases plus TASKBOARD-UI-001 (React UI replication), EXP-CONFIG-001 (Express configuration), PROM-PERF-001 (Prometheus workload measurement), CASBIN-ADV-AUTHZ-001 (advanced authorization policy classes), MEDUSA-PRICE-001 (calculated-price selection), AXIOS-HTTP-001 (Axios HTTP integration), SESSION-EXPRESS-001 (server-side session lifecycle), VIPER-CONFIG-001 (Viper configuration precedence), and TORM-PERSIST-002 (file-backed TypeORM durability). No facet-wide completeness claim is justified; broader commerce rules, identity-provider credential/login lifecycle, additional authorization/security models, integration resilience, persistence concurrency/isolation and power-loss durability, messaging guarantees, background-job lifecycle, expanded performance/resource classes, and incomplete property inventories remain. The independent UI-stack case is accepted only for its bounded Task Board scope.  
**Plan version:** 0.3.0  
**Last updated:** 2026-11-27

## 1. Mission

Define a technology-independent, machine-readable format for capturing the complete rules needed to reproduce a declared software scope in an independent implementation across technologies and stacks. Capture and comparison are the evidence and conformance process for that replication purpose.

The intended workflow is:

1. Identify the software system and the scenarios to examine.
2. Trigger controlled scenarios against the running reference system.
3. Capture observable results and supporting evidence in the Software Rules format.
4. Build an independent implementation in any suitable technology.
5. Run equivalent scenarios against that implementation.
6. Capture its results using the same format.
7. Normalize and compare the captures.
8. Report matches, differences, unknowns, and coverage limits.

The specification describes software rules and observable outcomes in technology-independent terms. It is not a source-code translation format and does not prescribe the implementation stack. The conformance programme must test transfer across materially different implementation stacks; finite tests can establish portability for the tested rules, stacks, and conditions, not mathematically guarantee compatibility with every possible stack.

## 2. Foundational distinctions

### 2.1 Runtime rules

A runtime rule is supported by evidence collected while the target software is executing. It must record the scenario or trigger, relevant preconditions and environment, observations, outcomes, and evidence references.

Source code may guide an investigator toward scenarios or explain what to inspect. Merely finding a declaration in source code does not make it a runtime observation.

### 2.2 Source-derived rules

A source-derived rule is a cautious inference from source code used when the relevant fact cannot be established through runtime observation. It must be stored separately, carry source provenance, and remain explicitly unverified as runtime behaviour.

### 2.3 Unknown is not false

The format must distinguish at least: observed, not observed, unknown, inferred from source, not applicable, and contradicted. Missing evidence must never silently become a negative result or a pass.

### 2.4 Comparison is bounded

A matching pair of captures demonstrates agreement only for the scenarios, inputs, environments, and observable dimensions covered by those captures. It does not prove universal equivalence.

### 2.5 Common envelope, facet-specific payloads

All rule records should share a common identity, provenance, condition, and evidence envelope. Each software facet must have its own typed payload. Do not force unrelated facets into one generic schema.

## 3. Work phases and completion gates

### Phase 0 — Repository and project governance

- [x] Create repository and initial README.
- [x] Establish this plan and persistent tracker.
- [x] Establish contribution, decision, and change-recording conventions.
- [x] Define specification maturity labels and versioning policy.
- [x] Link governance documents from the README.
- [x] Establish changelog and design-decision recording conventions.
- [x] Define initial specification maturity labels and versioning policy.

**Exit gate:** A new contributor or new chat can understand the mission, current state, next task, and where decisions are recorded. The repository has a maintained roadmap, tracker, contribution guide, changelog, decision log, and explicit maturity/versioning policy.

### Phase 1 — Research existing standards and prior art

Investigate relevant standards and formats before fixing the Software Rules model. Record each source's publication status, what it solves, what it does not solve, and whether Software Rules should reuse, map to, or deliberately differ from it.

Research areas include:

- Requirements engineering and specification quality (for example, ISO/IEC/IEEE 29148).
- Platform-independent modelling (for example, OMG MDA).
- Structural and behavioural modelling (for example, UML).
- Business vocabulary and rules (for example, OMG SBVR).
- API contracts (for example, OpenAPI).
- Event-driven and message API contracts (for example, AsyncAPI).
- Runtime telemetry and semantic conventions (for example, OpenTelemetry).
- Web interface runtime inspection and resolved style values (for example, DOM/CSSOM and WebDriver).
- Native interface inspection (for example, Android UI Automator and accessibility semantics).
- Scenario-based behavioural specification (for example, Gherkin/BDD).
- Machine-readable validation (for example, JSON Schema).
- Visual design token interchange (for example, the W3C Design Tokens Community Group format).

Deliverables:
- `research/STANDARDS-REVIEW.md`
- `research/REFERENCES.md`
- `research/DESIGN-DECISIONS.md`

- [x] Complete comparative review of all listed candidate standards.
- [x] Record publication status, scope, limitations, and project treatment for each.
- [x] Collect authoritative primary references.
- [x] Distinguish declared contracts from actual runtime observations.
- [x] Revise the working facet taxonomy and record unresolved boundaries.

**Exit gate: satisfied.** The candidate standards have been evaluated, their limits and design implications documented, authoritative references collected, and the facet taxonomy revised as a proposal. No capture schema has been frozen.

### Phase 2 — Core concepts and common model

Define the language and shared structure before designing facet payloads.

Tasks:
- Define system, boundary, component, facet, rule, observation, scenario, trigger, condition, outcome, evidence, provenance, and comparison.
- Define the distinction between declared contracts, runtime observations, and source-derived inferences.
- Decide whether scenario executions and individual observations are separate entities.
- Define capture method classes, including external observation, platform inspection, and runtime instrumentation.
- Define capture coverage and the meaning of incomplete or unavailable dimensions.
- Define runtime versus source-derived rule classes.
- Define rule identity and relationships.
- Define preconditions, inputs, environment, execution context, and time/order.
- Define observed state, emitted outputs, side effects, and evidence references.
- Define confidence and verification states without conflating them.
- Define unknown, unavailable, not applicable, and not observed.
- Define how multiple observations support, qualify, or contradict a rule.
- Define conceptual identity, time/order/correlation, and value/unit provenance; defer identifier syntax and canonicalization mechanics to Phases 4–5.
- Define the relationship between capture format version and target build/version; defer schema compatibility mechanics to Phase 4.

Deliverables:
- `specification/TERMINOLOGY.md`
- `specification/PRINCIPLES.md`
- `specification/RULE-CLASSIFICATION.md`
- `specification/EVIDENCE-AND-PROVENANCE.md`
- `specification/OBSERVATION-MODEL.md`
- `specification/CORE.md`
- `specification/SOURCE-DERIVED-RULES.md`
- `specification/VERSIONING.md`

**Exit gate: satisfied (conceptual model).** The vocabulary and linked entity model distinguish scenario definitions, executions, observations, evidence, runtime rules, source-derived rules, and declared contracts. The common model has been exercised against two unlike conceptual cases (resolved interface layout and API request/response behaviour) without flattening their facet-specific payloads. This validates the conceptual envelope, not a final serialization, empirical capture, or complete facet taxonomy. Machine schemas and facet payloads remain deferred.

### Phase 3 — Facet specifications

Design each facet as its own specification with explicit scope, observable dimensions, scenario requirements, payload fields, evidence requirements, limitations, and examples.

Proposed facets, revised after Phase 1 research:

1. Interface — web/native hierarchy, visual properties, geometry, stacking, accessibility, assets, and UI states.
2. Behaviour — triggers, preconditions, transitions, observable outputs, and side effects.
3. Business rules — domain constraints, decisions, calculations, policies, and rule outcomes.
4. Data — runtime data shapes, fields, types, relationships, transformations, and validation outcomes.
5. Persistence — durable state, reads/writes, transactions, consistency, and lifecycle observations.
6. API — synchronous request/response interfaces and actual runtime exchanges.
7. Messaging — channels, messages, publishing, receiving, delivery, and processing outcomes.
8. Identity and authentication — identity context, authentication events, and outcomes.
9. Authorization and permissions — roles, capabilities, policy decisions, and access outcomes.
10. Security controls — security-relevant runtime outcomes and authorized test observations.
11. Background processing — jobs, schedules, retries, lifecycle, and outcomes.
12. Errors and recovery — validation failures, exposed exceptions, retries, recovery, and failure outcomes.
13. Integrations — interactions and contracts with external systems.
14. Configuration — runtime configuration values and changes that affect behaviour.
15. Performance and resource behaviour — duration, throughput, latency, resource use, and performance outcomes.

The Phase 3 review accepts the 15 facets as the working normative catalogue for this draft. Facets are observation perspectives, may overlap in one execution, and are not required to exist in every system. Their boundaries and cross-facet relationships are documented in `facets/FACET-BOUNDARIES.md`. Each facet specification defines scope, observation unit, conceptual payload dimensions, scenario requirements, evidence, limitations, cross-facet links, and a worked conceptual example.

Deliverables:
- `facets/README.md` catalogue.
- `facets/FACET-BOUNDARIES.md` taxonomy and overlap rules.
- `facets/<facet>/README.md` for each of the 15 facets.
- Worked conceptual examples in each facet specification.

**Exit gate: satisfied at the facet-specification level.** All 15 facets have defined boundaries, conceptual typed payload inventories, evidence requirements, limitations, cross-facet relationships, and reviewed illustrative examples. These are not empirical captures. Exact machine schemas remain Phase 4; empirical end-to-end captures and conformance fixtures remain Phase 6.

### Phase 4 — Machine-readable schemas

Formalize the serialized capture model without beginning normalization or comparison semantics.

Tasks:
- Define JSON Schema Draft 2020-12 conventions, schema identifiers, draft version, and extension policy.
- Define the capture manifest and common target, coverage, scenario, execution, observation, evidence, contract, runtime-rule, and source-rule records.
- Require runtime method/procedure and evidence references for runtime observations.
- Keep source-derived rules and declared contracts structurally separate.
- Define one typed payload schema for each of the 15 facets.
- Define a structural comparison-report envelope only; defer match classifications and equivalence semantics to Phase 5.
- Add positive and negative fixtures.
- Provide a repeatable automated validation command.
- Document validation limits, schema evolution, and compatibility.

Deliverables:
- `specification/SCHEMA-DESIGN.md`
- `schemas/v1/*.schema.json` (draft schema version 0.1.0; not a stable 1.0.0 release)
- `schemas/v1/fixtures/valid/` and `schemas/v1/fixtures/invalid/`
- `conformance/validation/`

**Exit gate:** All schemas parse and resolve their references; the valid fixture passes; every negative fixture fails for the intended structural reason; validation instructions are reproducible. Cross-record referential integrity and evidence truth are explicitly outside JSON Schema validation.

### Phase 5 — Canonicalization and comparison

Specify how independently produced captures are aligned and compared without erasing meaningful differences or exceeding evidence.

Tasks:
- [x] Define capture, scenario, execution, subject, observation, and rule alignment.
- [x] Define identity evidence, ambiguity, and one-to-many/many-to-one alignment constraints.
- [x] Define normalization profiles and preserve raw observations/evidence.
- [x] Define rules for identifiers, timestamps, units, numbers, ordering, text, structured values, geometry, and performance measurements.
- [x] Define exact, normalized, semantic, and tolerance-based comparison bases.
- [x] Define match, mismatch, missing, additional, unknown, conflicting, and not-comparable classifications.
- [x] Define decision ordering so missing evidence cannot become a match.
- [x] Define coverage counts and bounded conclusions.
- [x] Expand the comparison-report JSON Schema.
- [x] Add a valid comparison example and an invalid universal-equivalence fixture.
- [x] Validate capture and comparison fixtures in CI.

Deliverables:
- `comparison/COMPARISON-MODEL.md`
- `comparison/NORMALIZATION.md`
- `comparison/MATCHING-RULES.md`
- `comparison/DIFFERENCE-CLASSIFICATION.md`
- `comparison/COVERAGE-AND-LIMITATIONS.md`
- `comparison/examples/`
- Updated `schemas/v1/comparison-report.schema.json`

**Exit gate: satisfied (2026-11-26).** The illustrative report demonstrates alignment, a matched dimension, an excluded/not-comparable dimension, separate per-capture coverage, and an inconclusive scope-bounded conclusion. GitHub Actions run [#4](https://github.com/REMAREMA6/software-rules/actions/runs/45793398830) passed the capture fixtures and comparison-report fixtures, including rejection of a universal-equivalence claim. The example is a model demonstration, not an empirical system capture.

### Phase 6 — Cross-repository, cross-stack replication and conformance

Phase 6 uses **multiple source repositories and a separate independent replication project**. One application is not expected to implement all 15 facets. The existing Task Board is retained as a bounded initial fixture; other facets are validated using suitable source repositories that actually demonstrate their rules.

The operating model, source register, replication-lab layout, rule-level pass criteria, and exit gate are defined in [the cross-repository replication programme](examples/CROSS-REPOSITORY-REPLICATION-PROGRAM.md). Live facet-by-facet evidence status is tracked in [FACET-COVERAGE.md](conformance/replication-lab/FACET-COVERAGE.md).

**Required loop:** source repository and immutable commit → observe/inspect → extract technology-independent rule → capture in Software Rules → independent implementation in a different stack → equivalent probes → capture and compare → mutation test → evidence-backed result.

**Work sequence**
- [x] Establish the independent replication-lab structure, case manifests, evidence layout, and initial runners; reports are generated per case as evidence becomes available.
- [x] Re-audit Task Board and preserve it as bounded evidence; unresolved properties remain partial/incomplete rather than being promoted to complete.
- [x] Register fifteen immutable source repositories and inspect the selected source implementations.
- [x] Accept BMQ-ER-002 (BullMQ retry/backoff) and EXP-API-001 (Express routing/API) after successful pinned-source runtime, independent Python replica, comparison, mutation, schema/integrity, and artifact-retention runs.
- [x] TORM-PERSIST-001: pinned TypeORM source + SQL.js vs Python sqlite3; two scenarios, eight semantic projections, six mutation tests, schema 0.2.0 capture/report and evidence-integrity validation passed.
- [x] BMQ-MSG-001: pinned BullMQ source + Redis vs Python queue model; two scenarios, ten semantic projections, six mutation tests, schema-native capture/report validation, and evidence integrity passed in run [#45929249126](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126).
- [x] JOSE-AUTH-001: pinned jose 6.2.18 / Node.js WebCrypto vs independent Python 3.12 HMAC/JWT verifier; eleven scenarios, 55 facet/scenario projections, eight executable mutations, Software Rules 0.2.0 schema/report validation, and evidence integrity passed in [run #45930973956](https://github.com/REMAREMA6/software-rules/actions/runs/45930973956).
- [x] CASBIN-AUTHZ-001: pinned Apache Casbin Go source vs independent Python 3.12 RBAC evaluator; ten requests, four executable mutations, Software Rules 0.2.0 captures, schema/report validation, and evidence integrity passed in [run #45931911753](https://github.com/REMAREMA6/software-rules/actions/runs/45931911753).
- [x] REDIS-INT-001: pinned go-redis Go client vs Python redis-py against Redis 7; seven operations, five executable mutations, Software Rules 0.2.0 captures, schema/report validation, and evidence integrity passed in [run #45932496414](https://github.com/REMAREMA6/software-rules/actions/runs/45932496414).
- [x] Extract and validate the bounded runtime rules in the accepted BullMQ and Express cases; source-derived inferences remain distinct where runtime evidence is absent.
- [x] Extracted and compared bounded TypeORM top-level transaction rules; broader transaction/durability semantics remain outside the case.
- [x] Independently replicate BullMQ retry decisions and Express HTTP routing in Python 3.12.
- [x] Independently replicate TypeORM top-level transaction outcomes in Python sqlite3; bounded source/replica comparison passed.
- [x] Independently replicate BullMQ duplicate-ID and consumer terminal outcomes in a Python queue model; bounded source/replica comparison passed.
- [x] Run and retain the pinned BullMQ+Redis runtime probe and Python replica capture; 12 semantic projections matched.
- [x] Run and retain the pinned Express runtime probe and Python HTTP replica capture; 28 semantic projections matched.
- [x] TypeORM source and replica probes, comparison, mutations, schema capture/report validation, and evidence integrity passed.
- [x] BullMQ messaging source and replica probes, comparison, six mutations, schema capture/report validation, and evidence integrity passed.
- [x] Accept BullMQ and Express comparison/mutation results after reviewing successful GitHub Actions runs.
- [x] Execute TypeORM source/replica comparison, mutation tests, schema validation, and evidence-integrity checks in CI.
- [x] Validate accepted BullMQ and Express Software Rules captures and comparison reports against schemas and cross-record integrity checks.
- [x] Validate TypeORM schema-native captures and comparison; evidence is retained in CI artifact `15167104492` (not committed to repository). Continue evidence-quality audit case by case.
- [x] Publish and update the living 15-facet evidence matrix.
- [x] TASKBOARD-UI-001 independent React 19/Vite UI-stack case passed its declared nine-observation conformance gate in run [#45934802401](https://github.com/REMAREMA6/software-rules/actions/runs/45934802401).
- [x] EXP-CONFIG-001 pinned Express 5.3.0 routing configuration and Python model matched 18 path observations; three mutations and Software Rules 0.2.0 schema/integrity validation passed in run [#45937990537](https://github.com/REMAREMA6/software-rules/actions/runs/45937990537).
- [x] PROM-PERF-001 pinned Prometheus workload passed three repeated runs, semantic sample-count comparisons, mutation tests, Software Rules schema/integrity validation in [run #45938387274](https://github.com/REMAREMA6/software-rules/actions/runs/45938387274).
- [x] CASBIN-ADV-AUTHZ-001 pinned Casbin domain-RBAC, ABAC, deny-override, and policy mutation case passed 19 decisions, four mutations, and Software Rules schema/integrity validation in [run #45938792630](https://github.com/REMAREMA6/software-rules/actions/runs/45938792630).
- [x] MEDUSA-PRICE-001 extracted the exact pinned Medusa service method body and matched nine calculated/original price-selection scenarios; five mutations and Software Rules schema/integrity passed in [run #45939713683](https://github.com/REMAREMA6/software-rules/actions/runs/45939713683).
- [x] AXIOS-HTTP-001 pinned Axios 1.21.1 and independent Python urllib matched nine HTTP interactions; six mutations and Software Rules schema/integrity passed in [run #45940398493](https://github.com/REMAREMA6/software-rules/actions/runs/45940398493).
- [x] SESSION-EXPRESS-001 pinned express-session 1.19.0 matched nine server-side session lifecycle transitions; five mutations and Software Rules schema/integrity passed in [run #45941194819](https://github.com/REMAREMA6/software-rules/actions/runs/45941194819).
- [x] VIPER-CONFIG-001 pinned Viper v1.21.0 matched nine source-precedence/environment scenarios; six mutations and Software Rules schema/integrity passed in [run #45941776949](https://github.com/REMAREMA6/software-rules/actions/runs/45941776949).
- [x] TORM-PERSIST-002 pinned TypeORM 1.1.3 matched four file-backed post-reopen durability/atomicity scenarios; four mutations and Software Rules schema/integrity passed in [run #45942572930](https://github.com/REMAREMA6/software-rules/actions/runs/45942572930).
- [ ] Add broader cart/discount/tax/eligibility business-rule cases; expand identity-provider credential/login lifecycle and HTTP integration properties (TLS, proxies, retries, cancellation); extend performance/resource coverage; complete the property-gap audit.

**Exit gate:** all 15 facets have reviewed property inventories and suitable source/independent-replica cases; each required rule class and claimed property passes the source→technology-independent rule→independent replica→equivalent probes→capture→comparison→mutation loop; replication cases span materially different stacks and architectures; no required unknown or partial property is silently passed; stack-specific assumptions are explicit; schema and cross-record validation pass; and the final report bounds conclusions to evidence. A finite conformance suite supports a bounded portability claim for the tested rules and stacks, not a universal guarantee for every possible technology. A green CI run alone cannot satisfy this gate.

### Phase 7 — Review, release, and maintenance

Phase 7 is blocked until the expanded Phase 6 exit gate is satisfied.

- [ ] Review the full specification for contradictions and omissions.
- [ ] Enforce the Replication Completeness Rule across every applicable facet.
- [ ] Verify schema, examples, conformance checks, and evidence provenance.
- [ ] Review comparison claims and limitations.
- [ ] Document unresolved questions and known limitations.
- [ ] Publish a versioned specification release and maintenance process.

**Exit gate:** The expanded Phase 6 conformance programme is complete, the release checklist is satisfied, known limitations are documented, and the specification version is clearly identified.

## 4. Target repository layout

~~~text
software-rules/
├── README.md
├── PLAN.md
├── TRACKER.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── specification/
│   ├── CORE.md
│   ├── TERMINOLOGY.md
│   ├── PRINCIPLES.md
│   ├── RULE-CLASSIFICATION.md
│   ├── EVIDENCE-AND-PROVENANCE.md
│   ├── OBSERVATION-MODEL.md
│   ├── SOURCE-DERIVED-RULES.md
│   └── VERSIONING.md
├── facets/
│   ├── interface/
│   ├── behavior/
│   ├── business-rules/
│   ├── data/
│   ├── persistence/
│   ├── api/
│   ├── messaging/
│   ├── identity-authentication/
│   ├── authorization-permissions/
│   ├── security-controls/
│   ├── background-processing/
│   ├── errors-recovery/
│   ├── integrations/
│   ├── configuration/
│   └── performance-resource-behaviour/
├── schemas/
│   └── v1/
├── comparison/
├── examples/
│   ├── CROSS-REPOSITORY-REPLICATION-PROGRAM.md
│   ├── cross-repository/
│   │   ├── sources/
│   │   └── captures/
│   ├── interface/
│   ├── behavior/
│   └── api/
├── conformance/
│   ├── integrity/
│   ├── validation/
│   └── replication-lab/
│       ├── cases/
│       ├── artifacts/
│       ├── projects/
│       ├── probes/
│       ├── runners/
│       └── reports/
├── .github/
│   └── workflows/
└── research/
│   ├── STANDARDS-REVIEW.md
│   ├── DESIGN-DECISIONS.md
│   └── REFERENCES.md
~~~

This is the target layout, not a statement that every planned file has already been created. Directories will appear in Git when their first tracked file is added.

## 5. Working rules for this project

1. Research before standardizing. Do not invent a term or structure where a relevant established standard already provides a suitable one.
2. Do not adopt an existing standard blindly. Explain its scope and limitations and why it fits.
3. Keep runtime observations and source-derived inferences separate in both data and documentation.
4. Describe observed outcomes, not presumed implementation intent.
5. Keep the core model small and shared; keep facet-specific details in facet specifications.
6. Every normative field must have a defined meaning, type, constraints, and evidence expectations.
7. Every important rule must have examples and validation tests.
8. Never silently treat missing observations as false, absent, or passing.
9. Never claim universal equivalence from finite test captures.
10. Update `TRACKER.md` whenever work starts, changes status, is blocked, or is completed.
11. Update `CHANGELOG.md` when a meaningful specification or structure change is made.
12. Record consequential design choices in `research/DESIGN-DECISIONS.md` using permanent decision IDs and explicit statuses.
13. Keep this plan as the roadmap. If the roadmap changes, update it rather than relying on chat history.
14. Apply the maturity labels and versioning policy in `specification/VERSIONING.md` to substantial specification and schema documents.
15. Follow `CONTRIBUTING.md` for the repository change and review workflow.

## 6. How to resume in a new chat

At the beginning of a new chat, provide this repository URL:

`https://github.com/REMAREMA6/software-rules`

The assistant should read, in order:
1. `README.md` — project purpose and core distinctions.
2. `PLAN.md` — full roadmap, structure, and working rules.
3. `TRACKER.md` — exact current progress, active task, blockers, and next action.
4. Any files listed under the active task in the tracker.

The tracker is the operational source of truth for progress. The plan is the source of truth for intended scope and sequence. If chat history conflicts with these repository documents, inspect the repository and resolve the discrepancy explicitly.

## 7. Immediate next work

Continue Phase 6 by adding broader commerce rules for cart totals, discounts, tax, quantity tiers, currency handling, and eligibility; expand identity-provider credential/login lifecycle and integration resilience beyond the accepted Axios/Redis scopes. Then resolve remaining required property gaps across all 15 facets, especially identity/session lifecycle, security controls, persistence durability/isolation, messaging guarantees, background-job lifecycle, error recovery, configuration precedence, and performance scaling/concurrency. The 16 accepted cases prove only their declared bounded scopes; no facet is complete. Keep the 15-facet inventory explicit, do not silently promote partial/unknown properties, and keep Phase 7 blocked until every Phase 6 exit-gate requirement is evidenced or explicitly resolved.
