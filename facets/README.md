# Facet Catalogue

**Maturity:** Draft — Software Rules specification 0.3.0.

A facet is an observation perspective, not necessarily a code module, deployment, database, or team boundary. A real operation may produce linked observations in several facets.

## Accepted facet set for the current specification draft

| Facet | Primary concern | Specification |
|---|---|---|
| Interface | Rendered UI hierarchy, resolved presentation, geometry, accessibility, assets, and visible UI state | [interface](interface/README.md) |
| Behaviour | Triggered reactions, transitions, outputs, and side effects | [behaviour](behavior/README.md) |
| Business rules | Domain decisions, constraints, calculations, and policies | [business rules](business-rules/README.md) |
| Data | Runtime data structures, values, validation, and transformations | [data](data/README.md) |
| Persistence | Durable state, transactions, consistency, and lifecycle | [persistence](persistence/README.md) |
| API | Synchronous request/response exchanges | [API](api/README.md) |
| Messaging | Asynchronous message/event delivery and processing | [messaging](messaging/README.md) |
| Identity and authentication | Principal establishment and session/credential lifecycle | [identity and authentication](identity-authentication/README.md) |
| Authorization and permissions | Runtime access decisions and enforcement | [authorization and permissions](authorization-permissions/README.md) |
| Security controls | Security mechanisms and outcomes under authorized tests | [security controls](security-controls/README.md) |
| Background processing | Deferred, scheduled, queued, and worker execution | [background processing](background-processing/README.md) |
| Errors and recovery | Failure, retry, fallback, compensation, and recovery | [errors and recovery](errors-recovery/README.md) |
| Integrations | Relationships and runtime interactions with external systems | [integrations](integrations/README.md) |
| Configuration | Effective runtime configuration and changes | [configuration](configuration/README.md) |
| Performance and resource behaviour | Measured latency, throughput, resource use, and workload behaviour | [performance and resource behaviour](performance-resource-behaviour/README.md) |

## Boundary rules

1. Classify by the primary question being answered, not by the code location that produced the result.
2. Keep transport details in API or Messaging; link to Integrations when the external-system relationship is relevant.
3. Keep principal establishment in Identity/Authentication; keep permission decisions in Authorization.
4. Keep domain eligibility/calculation in Business Rules; keep access permission in Authorization.
5. Keep runtime data shape/value in Data; keep durable transaction/lifecycle in Persistence.
6. Keep queued message delivery in Messaging; keep worker/job lifecycle in Background Processing.
7. Keep the failure/recovery lifecycle in Errors and Recovery while retaining the originating facet's detailed observation.
8. Treat configuration as a condition/source of behaviour, not as a replacement for the facet in which the effect is observed.
9. Treat performance measurements as measurements of a defined operation/workload, linked to the facet being measured.
10. A single execution can have observations in multiple facets. Do not force mutually dependent facts into one facet.

## Status and limits

This catalogue accepts the 15 facets as the working specification taxonomy for Phase 3. It does not claim that every system uses every facet, that facets are mutually exclusive, or that a facet corresponds to one implementation component. New facets or boundary changes require a documented decision and examples. Phase 4 will formalize payload schemas; Phase 5 will define cross-capture matching and comparison.
