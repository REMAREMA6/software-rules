# Design Decisions

This file records consequential decisions about the Software Rules specification. It is the durable record of why the project chooses one approach over alternatives.

## Decision status

- **Proposed** — under consideration; not binding.
- **Accepted** — agreed and currently governs the project.
- **Rejected** — considered and not selected; retain the rationale.
- **Superseded** — replaced by a later decision; link the replacement.
- **Deferred** — intentionally postponed until stated evidence or a dependency is available.

## Recording rules

1. Give each decision a permanent ID: D-001, D-002, and so on. Never reuse an ID.
2. Record the context/problem, options considered, decision, rationale, consequences, status, and date.
3. Record alternatives that were materially considered, including why they were not selected.
4. A proposal is not a requirement. Mark unsettled choices Proposed or Deferred.
5. When changing an accepted decision, create a new decision that supersedes it; do not silently rewrite history.
6. Update the changelog when an accepted decision changes the specification or repository structure.
7. Link affected specification files and tracker tasks where applicable.

## Decision template

~~~markdown
## D-NNN — Short decision title

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Rejected | Superseded | Deferred
- **Supersedes:** D-NNN (optional)

### Context
What problem or question requires a decision?

### Options considered
- Option A — advantages and disadvantages.
- Option B — advantages and disadvantages.

### Decision
What is being chosen, or what remains undecided?

### Rationale
Why is this the best-supported choice?

### Consequences
What follows from this decision? Include trade-offs and follow-up work.

### Evidence and references
Links to standards, research, experiments, or examples.
~~~

## Existing project decisions

## D-001 — Separate runtime-observed and source-derived rules

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
The specification must distinguish facts established by observing software while it runs from inferences made by reading source code.

### Decision
Runtime-observed rules and source-derived rules must be represented as distinct evidence classes. Source code may guide investigation, but source declarations alone do not establish runtime behaviour.

### Rationale
The project's primary purpose is to capture observable behaviour. Source code may be unused, unreachable, overridden, faulty, or inconsistent with actual execution.

### Consequences
The future data model, schemas, examples, and comparison rules must preserve this distinction. Source-derived information must never be presented as verified runtime evidence.

## D-002 — Shared envelope with facet-specific payloads

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
The project covers unlike software facets, including interfaces, behaviour, data, APIs, persistence, security, and integrations.

### Options considered
- One generic record for every facet.
- A shared common envelope with typed, facet-specific payloads.
- Entirely independent formats with no shared structure.

### Decision
Use a shared conceptual envelope for cross-facet identity, execution context, method, time, evidence, and coverage, with typed facet-specific payloads. The conceptual model has been tested against interface-layout and API request/response examples. The exact serialized fields remain deferred to later schema design.

### Rationale
A common identity, condition, provenance, and evidence model may enable cross-facet navigation and comparison without flattening different kinds of observations into generic prose.

### Consequences
The conceptual split is accepted. Do not freeze a schema yet: facet specifications must still test requiredness, cardinality, and specialized payload needs.

## D-003 — Bound equivalence claims to captured evidence

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
Two finite captures cannot establish that two systems behave identically for every possible input and environment.

### Decision
Comparison results must be scoped to the scenarios, inputs, environments, and observable dimensions actually covered. Missing or unknown observations must not count as matches.

### Rationale
This prevents comparison reports from claiming more than the evidence supports.

### Consequences
The comparison model must report coverage, unknowns, conflicts, and incomparable cases alongside matches and mismatches.


## D-004 — Compose existing standards; do not adopt one as the whole format

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
Phase 1 reviewed requirements, modelling, business-rule, API, messaging, observability, interface inspection, scenario, validation, design-token, and protocol standards.

### Options considered
- Adopt one existing standard as the complete Software Rules format.
- Compose relevant standards and define the missing cross-facet capture and comparison model.
- Invent all terminology and structures without mapping to prior art.

### Decision
Compose and map to established standards where they fit. Software Rules must define the missing cross-facet runtime capture, evidence/provenance, coverage, uncertainty, normalization, and comparison model itself.

### Rationale
Each reviewed candidate solves a bounded problem. None provides the complete technology-independent, evidence-backed, multi-facet runtime capture and independent implementation comparison workflow.

### Consequences
Facet specifications should reuse established concepts and mappings where appropriate. They must not misrepresent any candidate as a complete solution. See STANDARDS-REVIEW.md and REFERENCES.md.

## D-005 — Separate declared contracts from runtime observations

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
Standards such as OpenAPI, AsyncAPI, UML, SBVR, and design-token formats can describe declared interfaces, models, rules, or design decisions. Such declarations do not prove what a particular running implementation actually does.

### Decision
Declared contracts and models must be represented separately from runtime observations. Runtime evidence records what occurred under documented execution conditions. A mismatch between a declaration and runtime behaviour must remain visible.

### Rationale
The project's primary goal is to capture and compare actual running systems. Conflating intended/declared behaviour with observed behaviour would undermine the evidence model.

### Consequences
The core model must support declared-contract references without allowing them to satisfy runtime-evidence requirements. Phase 2 must define these relationships precisely.

## D-006 — Expand the facet taxonomy

- **Date:** 2026-11-26
- **Status:** Proposed

### Context
Phase 1 research found that the initial facet list did not clearly separate identity/authentication from authorization and did not explicitly account for runtime configuration or performance/resource observations.

### Options considered
- Keep the original facet list unchanged.
- Revise the list by clarifying identity/access boundaries and adding configuration and performance/resource behaviour as candidate facets.

### Decision
Use the revised 15-facet taxonomy in STANDARDS-REVIEW.md as the working proposal. Do not treat the list or its boundaries as normative yet.

### Rationale
The additional areas can affect runtime behaviour and comparison conditions. Authentication and authorization are distinct concepts. Configuration and performance/resource observations are not adequately represented by the original list.

### Consequences
Test the taxonomy against real system examples in Phases 2 and 3. Merge, split, rename, or remove facets when evidence supports doing so.


## D-007 — Separate scenario definitions, executions, and observations

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
A reusable test description, one actual attempt, and facts detected during that attempt have different identities and lifecycles. Combining them would make repeated runs, partial runs, and conflicting outcomes difficult to represent.

### Options considered
- Store scenario, execution, and observations as one combined record.
- Store a reusable scenario with separate execution records and linked observations.

### Decision
Represent scenario definitions, scenario executions, and observations as distinct linked entities. A scenario may have multiple executions; each execution may produce multiple observations.

### Rationale
This supports repeatability, state-dependent results, nondeterminism, execution failures, and evidence traceability without duplicating the scenario definition.

### Consequences
The common model and future schemas must preserve these links. Facet specifications define observation granularity.

## D-008 — A rule is a proposition supported by observations, not an observation itself

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
The project needs durable rules that can be compared across implementations, while each observation remains bounded to one execution and its conditions.

### Options considered
- Treat every captured observation as a rule.
- Treat a rule as a reusable proposition linked to one or more supporting, qualifying, or contradicting observations.

### Decision
A rule is a scoped proposition; observations are execution-specific findings that support, qualify, or contradict it. One rule may link to many observations and an observation may support more than one rule.

### Rationale
This avoids overgeneralizing from one test run and allows rules to accumulate evidence across scenarios, versions, and conditions.

### Consequences
Rule status must be interpreted with its evidence and coverage. Rule identity is distinct from observation identity.

## D-009 — Keep expected outcomes separate from actual outcomes

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
A test oracle or declared contract can state what should happen, but that expectation does not establish what the running system actually did.

### Options considered
- Store expected and actual outcomes in one result field.
- Preserve expected outcome, observed actual outcome, and evaluation as separate concepts.

### Decision
Represent expected outcome, actual outcome, and their evaluation separately. Expected outcomes identify their source; actual outcomes are grounded in observations.

### Rationale
This preserves the ability to record implementation/contract mismatches without allowing expectations to masquerade as runtime facts.

### Consequences
Future scenario and comparison formats must retain all three concepts and their provenance.


## D-010 — Accept the 15-facet catalogue for the current specification draft

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
The Phase 1 research proposed 15 observation facets. Phase 3 needed to validate whether their boundaries were sufficiently distinct to support individual payload specifications and cross-facet capture.

### Options considered
- Keep the taxonomy provisional until every facet has an empirical system capture.
- Accept the 15 facets as the working normative catalogue for this specification draft, with explicit overlap rules and the ability to revise based on later evidence.
- Collapse overlapping concerns into a smaller set of broad facets.

### Decision
Accept the 15-facet catalogue documented in `facets/README.md` for the current specification draft. Treat facets as observation perspectives, not mutually exclusive architectural modules. Use the boundary and overlap rules in `facets/FACET-BOUNDARIES.md`.

### Rationale
The boundary matrix distinguishes important questions such as domain decisions versus access permission, synchronous API exchanges versus asynchronous messaging, data values versus durable persistence, and message delivery versus worker lifecycle. Cross-facet links allow one execution to describe a connected operation without forcing all facts into one payload.

### Consequences
Each facet has an individual conceptual specification. The taxonomy is accepted for this draft but remains revisable through a new decision if empirical captures reveal missing or poorly separated concerns. Worked examples in Phase 3 are illustrative, not empirical. Machine schemas remain Phase 4; empirical end-to-end captures remain Phase 6.


## D-011 — Use JSON Schema Draft 2020-12 with a shared capture model and typed facet payloads

- **Date:** 2026-11-26
- **Status:** Accepted

### Context
Phase 3 established a common conceptual envelope and 15 facet-specific payload inventories. Phase 4 must serialize them without collapsing distinct evidence classes or prematurely defining comparison semantics.

### Options considered
- One generic payload schema for all facets.
- Independent unrelated capture formats for each facet.
- A common capture/record model with one typed schema per facet and explicit cross-record references.

### Decision
Use JSON Schema Draft 2020-12. Serialize captures through one manifest schema and shared record definitions, with separate runtime-rule, source-derived-rule, declared-contract, and evidence records. Each facet has its own payload schema. Use versioned URN identifiers under `urn:software-rules:schema:v1:`; the current draft version is 0.1.0. Preserve unknown/absent/redacted distinctions through explicit field-state records and use explicit `extensions` objects rather than silently accepting arbitrary core fields.

### Rationale
This reuses a reviewed standard for structural validation while retaining the common-envelope/facet-payload separation. Separate record classes make provenance differences machine-visible. Explicit extension points reduce accidental schema drift.

### Consequences
JSON Schema validates local structure, not reference existence, evidence authenticity, or semantic correctness. Those require additional conformance checks. The comparison-report schema is only a structural envelope; normalization, matching, tolerance, and difference classification remain Phase 5 work. The schema remains Draft and has no compatibility guarantee until stable release.

### Evidence and references
See `specification/SCHEMA-DESIGN.md`, `schemas/v1/README.md`, and the Phase 1 JSON Schema review in `research/STANDARDS-REVIEW.md`.
