# Phase 6 — Living 15-facet evidence matrix

**Status date:** 2026-11-27  
**Overall:** In progress. Two bounded cross-stack cases pass. No entire facet is complete for the full replication objective.

A facet is not complete merely because one small rule has passed. The matrix distinguishes bounded evidence from facet-wide coverage.

| # | Facet | Sources and bounded evidence | Independent implementation | Current status / remaining coverage |
|---|---|---|---|---|
| 1 | Interface | Task Board: 13-state screenshot/runtime comparison across three viewports, focus, hover and colour-scheme preference; 13 baseline screenshots pixel-identical in the recorded Chromium/Linux environment. Two properties remain partial. | Independent Task Board variant; no separate UI-framework cross-repository case accepted yet. | Partial. Need a source UI system and independent implementation in a different UI stack, broader visual/accessibility/interaction state inventory, and mutation coverage. |
| 2 | Behaviour | Task Board workflows; BullMQ retry/backoff; Express route dispatch. BullMQ and Express each pass bounded source/replica cases. | Python retry decision model; Python HTTP server. | Partial. Need broader state-machine, ordering, repeated/interrupted workflow, and cross-facet behaviour cases. |
| 3 | Business rules | Task Board title/duplicate/count probes are partial. Medusa is a candidate for commerce pricing/cart rules. | No accepted independent business-rule replica yet. | Not complete. Need source-derived domain rule, boundary/precedence matrix, and independent implementation. |
| 4 | Data | Task Board record/identifier/PATCH samples are partial; BullMQ attemptsMade semantics are covered within its retry case. | Python model for BullMQ counters. | Partial. Need explicit typed data schema, nullability, relationships, validation, transformation, and round-trip cases. |
| 5 | Persistence | TypeORM transaction/rollback implementation inspected at pinned commit; TORM-PERSIST-001 runtime workflow and Python/sqlite3 replica prepared. | Python 3.12 sqlite3. | In progress; no pass until pinned source workflow and evidence validation succeed. |
| 6 | API | Express 5.3.0 seven-request HTTP case passes 28 facet/scenario projections; Task Board also has a deterministic in-memory API adapter sample. | Python 3.12 HTTP server. | Bounded case passed. Need broader payload validation, authentication, pagination, concurrency, and error contract classes before facet-wide coverage. |
| 7 | Messaging | BullMQ queue retry case covers job processing/retry outcomes, not the complete message delivery/acknowledgement contract. | Python decision-model simulator. | Not complete. Need publish/consume, delivery guarantee, ack/nack, duplicate, ordering, and idempotency case. |
| 8 | Identity and authentication | Keycloak and OWASP Juice Shop are registered candidates; no accepted runtime case. | None. | Not started. |
| 9 | Authorization and permissions | Keycloak, Juice Shop and Grafana are candidates; no actor/resource/action policy matrix. | None. | Not started. |
| 10 | Security controls | Task Board only tests literal rendering/output encoding in a bounded input probe; no dedicated security-control case. | No dedicated independent security-control replica. | Partial baseline only. Need authorized, controlled positive/negative/bypass/containment probes. |
| 11 | Background processing | BullMQ pinned TypeScript/Node.js + Redis case passes three retry scenarios and 12 semantic projections. | Independent Python 3.12 decision-model simulator. | Bounded case passed. Need scheduling, cancellation, duplicate jobs, stalled workers, and broader worker lifecycle coverage. |
| 12 | Errors and recovery | BullMQ retry suppression/attempt limits; Express 404 fallback; Task Board HTTP 503 outcomes. | Python retry model and HTTP server. | Partial. Need broader error classes, fallback, compensation, rollback, and recovered-state coverage. |
| 13 | Integrations | n8n, Grafana and Medusa candidates only; n8n file-level licence restrictions remain. | None. | Not started. |
| 14 | Configuration | Express default case-sensitive and strict-routing settings observed and reproduced in the seven-request case. | Python HTTP server. | Bounded case passed. Need precedence, invalid/missing settings, environment/file/CLI override, and runtime changes. |
| 15 | Performance/resources | Task Board single-run navigation/paint/resource samples only; Prometheus and Grafana candidates. | None. | Partial baseline only. Need repeatable workload, latency distributions, throughput, resource consumption, and limit behaviour. |

## Accepted bounded cases

1. **BMQ-ER-002 — BullMQ retry/backoff:** source commit `526668f2c5e6de9d5d664df577f09a6bdccac1b4`; pinned source runtime with Redis 7; independent Python 3.12 model; three scenarios; 12 semantic projections; mutation tests; schema and cross-record validation. Successful run [#45925568609](https://github.com/REMAREMA6/software-rules/actions/runs/45925568609); evidence commit [513766d](https://github.com/REMAREMA6/software-rules/commit/513766df3b9d4300df4c9297b79f221b54e29e42).
2. **EXP-API-001 — Express routing/API:** source commit `43fca52d28a422c8be48fd489cbd4f2d6152bab6`; pinned Express runtime; independent Python 3.12 HTTP server; seven requests; 28 semantic projections; mutation tests; schema and cross-record validation. Successful run [#45926714897](https://github.com/REMAREMA6/software-rules/actions/runs/45926714897); evidence commit [ad30376](https://github.com/REMAREMA6/software-rules/commit/ad3037693d32221a6d7bdb6b9883c45db7b2be9c).

## Active case

- **TORM-PERSIST-001 — TypeORM transaction commit/rollback:** pinned source commit `b1e211fc2654d412612a08f8a7fb890f3352614f`; compile source and run SQL.js driver; independent Python sqlite3 replica. Workflow added; result not yet verified.

## Exit-gate interpretation

- A passed case proves only the declared properties and scenarios for that source/replica pair.
- No entire facet is complete until its property inventory has been reviewed against the facet specification and required rule classes.
- Candidate repositories are not evidence of coverage.
- A passing unit test or schema validation without source-runtime comparison is not a cross-stack pass.
- Unknown, partial, unavailable, and excluded properties remain explicit.
- Finite evidence supports bounded portability claims, not universal guarantees for arbitrary software or every possible technology.
