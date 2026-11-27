# Phase 6 — Fifteen-facet evidence coverage

**Overall status:** In progress. Four bounded cross-stack cases have passed: BullMQ retry/backoff, Express routing, TypeORM transaction commit/rollback, and Medusa price-list date validation. The BullMQ messaging case is active. No entire facet is complete for the project-wide objective.

This matrix distinguishes a facet having some validated evidence from a facet being complete. A bounded case does not establish complete facet coverage.

## Coverage matrix

| # | Facet | Source evidence / current result | Independent replica | Status |
|---|---|---|---|---|
| 1 | Interface | Task Board has a bounded 1280×800 UI capture with pixel-identical tested states and detected visual mutation; two inventory properties remain partial and broader interface environments are not covered. | Independent browser UI fixture | Partial |
| 2 | Behaviour | BullMQ retry/backoff, Express routing, and TypeORM transaction workflows each have bounded cross-stack matches. Medusa date-validation order passes in a bounded ten-probe case. | Python retry model, HTTP server, SQLite transaction model, and date validator | In progress |
| 3 | Business rules | Medusa price-list date validation passes ten probes and 40 projections. Full cart, discount, tax, and price-selection rules remain uncovered. | Python ISO-8601 validator with mutation tests | In progress |
| 4 | Data | TypeORM Post/Category snapshots and BullMQ attempt counters have bounded evidence; Task Board data properties remain partial. Medusa date-field representations pass in a bounded ten-probe case. | Python/SQLite and Python retry/date models | Partial |
| 5 | Persistence | TypeORM 1.1.3 commit-on-success and rollback-on-NOT-NULL-failure match the Python/SQLite model across two scenarios. Other drivers, concurrency, isolation, and durability remain untested. | Python 3.12 / sqlite3 | In progress |
| 6 | API | Express 5.3.0 matches an independent Python HTTP implementation across seven requests and 28 facet/scenario projections. This does not cover the complete Express API surface. | Python 3.12 HTTP server | In progress |
| 7 | Messaging | BullMQ QueueEvents/message lifecycle case has a source probe, independent model, and workflow scaffold; end-to-end evidence and comparison remain pending. | Python messaging model | In progress |
| 8 | Identity and authentication | Keycloak is a registered source candidate; no source/replica case has passed. | None yet | Not started |
| 9 | Authorization and permissions | Keycloak is a registered source candidate; no actor/resource/action policy matrix has passed. | None yet | Not started |
| 10 | Security controls | OWASP Juice Shop is a registered source candidate; no authorized source/replica security case has passed. | None yet | Not started |
| 11 | Background processing | BullMQ retry eligibility/backoff case passes its bounded source/replica probes. Scheduling, cancellation, concurrency, stalled jobs, and full lifecycle remain uncovered. | Python retry-decision model | In progress |
| 12 | Errors and recovery | BullMQ retry suppression, Express 404 fallback, and TypeORM rollback pass bounded cases. Medusa invalid_data error behavior passes in a bounded ten-probe case; broader failure classes remain uncovered. | Python retry, HTTP, SQLite, and date models | In progress |
| 13 | Integrations | Grafana, n8n, and Medusa are candidates; no external-system integration contract has passed an independent replica case. | None yet | Not started |
| 14 | Configuration | Express default case-sensitive/strict routing settings pass in the seven-request case. Effective configuration precedence in Grafana/Keycloak remains untested. | Python HTTP server | In progress |
| 15 | Performance and resource behaviour | Prometheus is a registered candidate; no reproducible source workload and independent measurement case has passed. | None yet | Not started |

## Accepted bounded cases

| Case | Facets | Evidence |
|---|---|---|
| [BMQ-ER-002](cases/BMQ-ER-002/CASE.md) | Background processing; errors/recovery; data; behaviour | Source/replica runtime comparison, mutation detection, Software Rules captures, schema/integrity validation, and committed artifacts |
| [EXP-API-001](cases/EXP-API-001/CASE.md) | API; behaviour; configuration; errors/recovery | Seven HTTP requests, 28 matching projections, executable mutations, Software Rules captures, schema/integrity validation, and committed artifacts |
| [TYPEORM-PERSIST-001](cases/TYPEORM-PERSIST-001/CASE.md) | Persistence; data; behaviour; errors/recovery | Two transaction scenarios, eight matching projections, executable commit-on-error mutation, Software Rules captures, schema/integrity validation, and committed artifacts |
| [MEDUSA-BR-001](cases/MEDUSA-BR-001/CASE.md) | Business rules; data; behaviour; errors/recovery | Ten date inputs, 40 matching projections, executable mutations, Software Rules captures, schema/integrity validation, and committed source evidence |

## Active cases

- [BMQ-MSG-001](cases/BMQ-MSG-001/CASE.md) — BullMQ queue-event/message lifecycle; source runtime and independent model comparison pending.


## Completion rule

Do not mark a facet complete because a repository has a similarly named feature or because one bounded case passes. Completion requires a reviewed property inventory for that facet, suitable source evidence, independent implementations in different stacks, equivalent normal/boundary/negative/failure probes, comparison, meaningful mutation detection, validated Software Rules captures, and explicit resolution of every required unknown or partial property.
