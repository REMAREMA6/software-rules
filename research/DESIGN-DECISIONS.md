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
- **Status:** Proposed

### Context
The project covers unlike software facets, including interfaces, behaviour, data, APIs, persistence, security, and integrations.

### Options considered
- One generic record for every facet.
- A shared common envelope with typed, facet-specific payloads.
- Entirely independent formats with no shared structure.

### Decision
Proceed with a shared envelope and facet-specific payloads as the working proposal. Validate the boundary and required shared fields during Phase 1 and Phase 2 before making it normative.

### Rationale
A common identity, condition, provenance, and evidence model may enable cross-facet navigation and comparison without flattening different kinds of observations into generic prose.

### Consequences
Do not freeze a schema yet. Research and cross-facet examples must test whether the proposed shared fields are genuinely common and whether any facet requires a different treatment.

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
