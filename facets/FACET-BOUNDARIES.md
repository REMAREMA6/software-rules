# Facet Boundary and Taxonomy Decision

**Maturity:** Draft — Software Rules specification 0.3.0.

## 1. Classification model

The 15 facets are observation perspectives. They are deliberately not a decomposition of source code or architecture. Classify each fact according to the question it answers and preserve links to related facts.

## 2. Boundary matrix

| Question | Primary facet |
|---|---|
| What is rendered and exposed to users/assistive technology? | Interface |
| What happened after a trigger? | Behaviour |
| Why was a domain decision/calculation made, and what outcome resulted? | Business Rules |
| What data structure/value/validation/transformation was observed? | Data |
| What was read/written durably, and what transaction/consistency result occurred? | Persistence |
| What synchronous request/response exchange occurred? | API |
| What asynchronous message was published/delivered/acknowledged? | Messaging |
| Which principal/session/identity was established? | Identity and Authentication |
| Was an action permitted for a principal/resource? | Authorization and Permissions |
| Did a security control detect, prevent, limit, or contain a defined threat/test? | Security Controls |
| What happened to a deferred/scheduled/worker job? | Background Processing |
| What failure/retry/fallback/compensation/recovery occurred? | Errors and Recovery |
| How did the target interact with an external provider/system? | Integrations |
| Which effective runtime setting conditioned behaviour? | Configuration |
| What measured performance/resource result occurred under a workload? | Performance and Resource Behaviour |

## 3. Overlap handling

Facets are allowed to overlap in the same real-world operation, but an individual observation should have a clear primary subject and purpose. Related facts are linked rather than duplicated as unstructured prose.

Example: a user submits a payment:
- Interface: button state and visible confirmation.
- Behaviour: submit trigger and state transition.
- API: synchronous request/response.
- Integrations: payment provider interaction.
- Business Rules: payment eligibility or fee calculation.
- Persistence: committed payment record.
- Background Processing: deferred settlement task.
- Errors and Recovery: declined/timeout/retry outcome.
- Performance: measured end-to-end latency under a defined workload.

Not every operation requires all these observations. Only record what is actually observed.

## 4. Deliberate separations

- **Business Rules vs Authorization:** domain eligibility is not access permission. A customer may be authenticated and authorized to submit an order but fail a business eligibility rule.
- **Identity vs Authorization:** authentication establishes or asserts a principal; authorization decides what that principal may do.
- **API vs Messaging:** request/response completion differs from asynchronous delivery and acknowledgement.
- **Messaging vs Background Processing:** message transport/delivery differs from the lifecycle of work performed by a consumer.
- **Data vs Persistence:** a runtime object/value does not prove durable storage; a database record does not fully describe the API/UI representation.
- **Behaviour vs Errors and Recovery:** behaviour records the intended/observed transition; the error facet captures failure and recovery semantics with a link to the originating operation.
- **Integrations vs API/Messaging:** integration identifies the external dependency relationship; API/Messaging capture protocol-level exchange.
- **Configuration vs affected facet:** a configuration value is a condition; the resulting effect is captured in its primary facet.
- **Performance vs measured operation:** measurements annotate a workload/operation and link to its facet rather than duplicating the full operation payload.

## 5. Taxonomy status

For this draft, accept the 15 facets as the working normative catalogue for subsequent specification work. They are not necessarily mutually exclusive, exhaustive for every future domain, or present in every target. A future change must document evidence, migration impact, and a revised boundary example.

## 6. Validation examples

The facet README files each include a conceptual scenario, observation dimensions, evidence expectations, limitations, and cross-facet links. The examples are illustrative model tests, not empirical captures from a real software target. The accepted empirical cross-stack evidence and its limits are recorded in the Phase 6 exit audit; future facet/property expansions require new cases.
