# Phase 6 — Living 15-facet evidence matrix

**Status date:** 2026-11-27  
**Overall:** In progress. No facet is complete for the full declared replication objective.

This is an evidence-status register, not a list of technologies that happen to contain similarly named features. A facet advances only when specific properties have source evidence, a technology-independent rule, an independent implementation, equivalent probes, comparison results, mutation detection, and reviewed completeness.

| # | Facet | Candidate source(s) | Current evidence | Independent replica | Status |
|---|---|---|---|---|---|
| 1 | Interface | Task Board fixture; OWASP Juice Shop candidate | Task Board has bounded multi-state visual/runtime evidence; two font/UI properties remain partial and full platform coverage is not established | Task Board independent variant; cross-repository replica case not yet accepted | Partial baseline only |
| 2 | Behaviour | Task Board; BullMQ; Express | Task Board has bounded workflow probes; BullMQ retry case is in progress | Python retry decision model; source/runtime comparison pending | In progress |
| 3 | Business rules | Medusa candidate; Task Board | Task Board has partial title/duplicate/count rules; Medusa pricing/cart source paths identified but not yet verified | None accepted yet | Candidate / partial baseline |
| 4 | Data | TypeORM; Medusa; Task Board | Task Board has partial entity/identifier/PATCH samples; TypeORM transaction/model implementation not yet case-reviewed | None accepted yet | Candidate / partial baseline |
| 5 | Persistence | TypeORM; Prometheus | No source/replica persistence case completed | None | Not started |
| 6 | API | Express; Task Board | Task Board only tests a deterministic in-memory adapter; Express route/error contract not yet selected | None accepted yet | Candidate / partial baseline |
| 7 | Messaging | BullMQ | BullMQ queue retry case is not yet a message-delivery/acknowledgement case | None | Not started |
| 8 | Identity and authentication | Keycloak; OWASP Juice Shop | Candidate repositories registered; no runtime capture | None | Not started |
| 9 | Authorization and permissions | Keycloak; OWASP Juice Shop; Grafana | Candidate repositories registered; no policy-matrix capture | None | Not started |
| 10 | Security controls | OWASP Juice Shop; Grafana | Task Board has limited literal-content output probes only; no comprehensive security-control case | None | Partial baseline only |
| 11 | Background processing | BullMQ | Source-derived retry rules and Python decision-model simulation exist; pinned BullMQ+Redis runtime comparison is pending | Python 3.12 model | In progress |
| 12 | Errors and recovery | BullMQ; Express; TypeORM | Task Board has bounded HTTP 503/no-recovery observations; BullMQ retry suppression and attempt limits are in progress | Python 3.12 model | In progress |
| 13 | Integrations | n8n; Grafana; Medusa | Candidates only; n8n licence restrictions require per-file review | None | Not started |
| 14 | Configuration | Grafana; Keycloak | Candidate source settings identified; runtime precedence not verified | None | Not started |
| 15 | Performance and resource behaviour | Prometheus; Grafana | Task Board has single-run navigation/paint/resource samples only; no repeatable load/throughput case | None | Partial baseline only |

## Interpretation

- “Candidate” means a repository is registered for investigation, not that the facet is captured.
- “Partial baseline” means the existing Task Board fixture provides some bounded evidence, not complete facet coverage.
- “In progress” means a case has actual artifacts or an active runtime/replica pipeline, but has not passed its full evidence loop.
- No row may be promoted to complete solely because a CI workflow passes. The case artifacts, comparison, mutations, and property inventory must be reviewed.
- One case may cover more than one facet, but each facet's property inventory and coverage conclusion remain separately auditable.

## Current next case

Finish BMQ-ER-002, then select the next source/replica case for API behaviour (Express) and continue the matrix. Expand to more repositories when the existing candidates do not adequately demonstrate a facet or rule class.
