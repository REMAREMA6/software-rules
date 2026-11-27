# Phase 6 — Cross-repository replication exit audit

**Decision:** EXIT APPROVED for the declared Phase 6 validation corpus.  
**Date:** 2026-11-27  
**Corpus:** 23 accepted bounded cross-stack cases; 15 immutable source repositories; all 15 facets represented.  
**Important boundary:** This approves the validation method and declared corpus. It does not claim that every facet is universally complete, that every possible software rule has been catalogued, or that any two arbitrary systems are equivalent.

## 1. Exit decision

The Phase 6 exit gate is satisfied for the declared corpus because:

1. All 15 facets have a reviewed property inventory in [PHASE6-REQUIRED-PROPERTY-INVENTORY.md](PHASE6-REQUIRED-PROPERTY-INVENTORY.md).
2. Every facet has source-backed observations and at least one independent replica. Facets with materially different rule classes have multiple cases where the corpus requires them.
3. Every accepted case follows the source → technology-independent rule → independent replica → equivalent probes → comparison → mutation-detection loop.
4. Source and replica implementations use genuinely different languages, runtimes, frameworks, or data-access stacks. The replica does not delegate the tested rule back to the source implementation.
5. Each case has a declared boundary, local property inventory, explicit exclusions, and evidence links. Properties outside that case's declared boundary are resolved as not applicable to that case, not silently marked as globally irrelevant or captured.
6. Rule records and captures use the technology-independent Software Rules 0.2.0 format; source-specific code is retained as provenance/evidence, not embedded as the portable rule.
7. The accepted workflows validated source/replica captures, cross-record integrity, comparison schema/completeness, and mutation detection. Evidence and source provenance are linked from each case.
8. This report records outcomes, facet coverage, explicit exclusions, remaining limitations, and the absence of any universal equivalence claim.

## 2. Accepted case corpus

| # | Case | Bounded rule class and observed result | Evidence |
|---:|---|---|---|
| 1 | [BMQ-ER-002](cases/BMQ-ER-002/CASE.md) | BullMQ retry/backoff and failure outcomes independently modelled in Python; runtime and mutation evidence accepted. | Case-linked pinned source and CI evidence. |
| 2 | [EXP-API-001](cases/EXP-API-001/CASE.md) | Seven Express HTTP requests and 28 semantic projections matched an independent Python HTTP server; mutation detection passed. | Case-linked pinned source and CI evidence. |
| 3 | [TORM-PERSIST-001](cases/TORM-PERSIST-001/CASE.md) | TypeORM transaction commit/rollback matched Python sqlite3; two scenarios and eight semantic projections; six mutations passed in [run #45928766010](https://github.com/REMAREMA6/software-rules/actions/runs/45928766010), artifact `15167104492`. | Runtime capture, comparison, schema/integrity validation. |
| 4 | [MEDUSA-BR-001](cases/MEDUSA-BR-001/CASE.md) | Ten Medusa date-validation inputs and 40 projections matched an independent Python validator; mutation evidence accepted. | Source/helper artifacts committed at [dd0ad76](https://github.com/REMAREMA6/software-rules/commit/dd0ad76f0ec9557a41250c5fcc3efa14dc5aa1a2). |
| 5 | [BMQ-MSG-001](cases/BMQ-MSG-001/CASE.md) | BullMQ QueueEvents/message lifecycle matched an independent Python model; six mutations passed in [run #45929249126](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126), artifact `15167806675`. | Runtime capture, comparison, schema/integrity validation. |
| 6 | [JOSE-AUTH-001](cases/JOSE-AUTH-001/CASE.md) | Eleven JWT verification scenarios and 55 projections matched a Python verifier; eight mutations passed in [run #45930973956](https://github.com/REMAREMA6/software-rules/actions/runs/45930973956). | Runtime capture, comparison, schema/integrity validation. |
| 7 | [CASBIN-AUTHZ-001](cases/CASBIN-AUTHZ-001/CASE.md) | Ten simple-RBAC decisions matched Python; four mutations passed in [run #45931911753](https://github.com/REMAREMA6/software-rules/actions/runs/45931911753). | Runtime capture, comparison, schema/integrity validation. |
| 8 | [REDIS-INT-001](cases/REDIS-INT-001/CASE.md) | Seven go-redis/redis-py operations matched against Redis 7; five mutations passed in [run #45932496414](https://github.com/REMAREMA6/software-rules/actions/runs/45932496414). | Runtime capture, comparison, schema/integrity validation. |
| 9 | [TASKBOARD-UI-001](cases/TASKBOARD-UI-001/CASE.md) | Independent React 19/Vite UI replica: nine viewport/state comparisons, pixel equality, semantic/API trace matches, and deliberate mutation detection in [run #45934802401](https://github.com/REMAREMA6/software-rules/actions/runs/45934802401), artifact `15170370565`. | Source/replica captures, comparison, schema/integrity validation. |
| 10 | [EXP-CONFIG-001](cases/EXP-CONFIG-001/CASE.md) | Five Express routing configuration profiles and 18 path observations; three mutations passed in [run #45937990537](https://github.com/REMAREMA6/software-rules/actions/runs/45937990537), artifact `15171850580`. | Runtime capture, comparison, schema/integrity validation. |
| 11 | [PROM-PERF-001](cases/PROM-PERF-001/CASE.md) | Three pinned Prometheus TSDB workload runs and three independent Python workload-model runs; sample accounting matched and repeat/drop-scrape mutations were detected in [run #45938387274](https://github.com/REMAREMA6/software-rules/actions/runs/45938387274), artifact `15171587211`. | Workload capture, comparison, schema/integrity validation. |
| 12 | [CASBIN-ADV-AUTHZ-001](cases/CASBIN-ADV-AUTHZ-001/CASE.md) | Nineteen domain-RBAC, ABAC, deny-override, and policy-mutation decisions matched Python; four mutations passed in [run #45938792630](https://github.com/REMAREMA6/software-rules/actions/runs/45938792630), artifact `15172101161`. | Runtime capture, comparison, schema/integrity validation. |
| 13 | [MEDUSA-PRICE-001](cases/MEDUSA-PRICE-001/CASE.md) | Nine exact Medusa calculated/original price-selection scenarios matched Python; five mutations passed in [run #45939713683](https://github.com/REMAREMA6/software-rules/actions/runs/45939713683), artifact `15172460158`. | Runtime capture, comparison, schema/integrity validation. |
| 14 | [AXIOS-HTTP-001](cases/AXIOS-HTTP-001/CASE.md) | Nine Axios/Python urllib HTTP interactions matched; six mutations passed in [run #45940398493](https://github.com/REMAREMA6/software-rules/actions/runs/45940398493), artifact `15172188627`. | Runtime capture, comparison, schema/integrity validation. |
| 15 | [SESSION-EXPRESS-001](cases/SESSION-EXPRESS-001/CASE.md) | Nine express-session/Python session lifecycle transitions matched; five mutations passed in [run #45941194819](https://github.com/REMAREMA6/software-rules/actions/runs/45941194819), artifact `15172927152`. | Runtime capture, comparison, schema/integrity validation. |
| 16 | [VIPER-CONFIG-001](cases/VIPER-CONFIG-001/CASE.md) | Nine Viper/Python source-precedence and environment-mapping scenarios matched; six mutations passed in [run #45941776949](https://github.com/REMAREMA6/software-rules/actions/runs/45941776949), artifact `15172438139`. | Runtime capture, comparison, schema/integrity validation. |
| 17 | [TORM-PERSIST-002](cases/TORM-PERSIST-002/CASE.md) | Four TypeORM/Python file-backed post-reopen durability and atomicity scenarios matched; four mutations passed in [run #45942572930](https://github.com/REMAREMA6/software-rules/actions/runs/45942572930), artifact `15172764857`. | Runtime capture, comparison, schema/integrity validation. |
| 18 | [BMQ-RECOVERY-001](cases/BMQ-RECOVERY-001/CASE.md) | Two BullMQ stalled-job recovery/terminal-limit scenarios matched job counters, events, processed values, and queue counts; four mutations passed in [run #45943469678](https://github.com/REMAREMA6/software-rules/actions/runs/45943469678), artifact `15173607117`. | Runtime capture, comparison, schema/integrity validation. |
| 19 | [MEDUSA-ADJUST-001](cases/MEDUSA-ADJUST-001/CASE.md) | Nine Medusa adjustment/tax-allocation scenarios matched Python Decimal; six mutations passed in [run #45943612155](https://github.com/REMAREMA6/software-rules/actions/runs/45943612155), artifact `15173389412`. | Runtime capture, comparison, schema/integrity validation. |
| 20 | [MEDUSA-PROMO-001](cases/MEDUSA-PROMO-001/CASE.md) | Thirty-two Medusa promotion-rule eligibility scenarios matched Python; eight mutations passed in [run #45944011363](https://github.com/REMAREMA6/software-rules/actions/runs/45944011363), artifact `15174046701`. | Runtime capture, comparison, schema/integrity validation. |
| 21 | [TYPEORM-PERSIST-001](cases/TYPEORM-PERSIST-001/CASE.md) | TypeORM 1.1.3 transaction callback commit/rollback matched independent Python 3.12/sqlite3 across two scenarios and eight projections; rollback/error mutations and Software Rules schema/integrity validation passed in [run #45927631068](https://github.com/REMAREMA6/software-rules/actions/runs/45927631068), artifact `15166753118`. | Runtime capture, comparison, schema/integrity validation; better-sqlite3 driver boundary. |
| 22 | [BMQ-SCHED-001](cases/BMQ-SCHED-001/CASE.md) | BullMQ 6.7.10 delayed-job rescheduling and cancellation matched the independent Python state machine; six mutations and Software Rules schema/integrity validation passed in [run #45946359808](https://github.com/REMAREMA6/software-rules/actions/runs/45946359808), artifact `15174518117`. | Runtime capture, comparison, schema/integrity validation. |
| 23 | [MEDUSA-LINE-ITEM-001](cases/MEDUSA-LINE-ITEM-001/CASE.md) | Fourteen Medusa line-item subtotal/tax/discount/total scenarios matched the independent Python Decimal model; six mutations and Software Rules schema/integrity validation passed in [run #45946618440](https://github.com/REMAREMA6/software-rules/actions/runs/45946618440), artifact `15175295192`. | Runtime capture, comparison, schema/integrity validation. |

## 3. Fifteen-facet result

| Facet | Accepted independent evidence | Corpus result |
|---|---|---|
| Interface | TASKBOARD-UI-001 | Represented; browser UI scope only. |
| Behaviour | BullMQ, Express, TypeORM, Medusa, JOSE, Casbin, Task Board | Represented across request, state, and lifecycle rules. |
| Business rules | MEDUSA-BR-001, MEDUSA-PRICE-001, MEDUSA-ADJUST-001, MEDUSA-PROMO-001, MEDUSA-LINE-ITEM-001, Task Board | Represented across temporal validation, price selection, tax/adjustment, eligibility, and title/count rules. |
| Data | Task Board, TypeORM, BullMQ, Medusa, JOSE, Redis | Represented across records, payloads, claims, and values. |
| Persistence | TORM-PERSIST-001, TYPEORM-PERSIST-001, TORM-PERSIST-002 | Represented across transaction atomicity and file-backed reopen durability. |
| API | EXP-API-001, EXP-CONFIG-001, AXIOS-HTTP-001 | Represented across route semantics, configuration activation, and HTTP client outcomes. |
| Messaging | BMQ-MSG-001, BMQ-RECOVERY-001 | Represented across QueueEvents and stalled redelivery/failure. |
| Identity and authentication | JOSE-AUTH-001, SESSION-EXPRESS-001 | Represented across token verification and server-side session lifecycle. |
| Authorization and permissions | CASBIN-AUTHZ-001, CASBIN-ADV-AUTHZ-001 | Represented across simple RBAC, domain RBAC, ABAC, deny override, and policy mutation. |
| Security controls | JOSE, express-session, Task Board output handling | Represented across signature/algorithm checks, signed-cookie integrity, and output encoding. |
| Background processing | BMQ-ER-002, BMQ-MSG-001, BMQ-RECOVERY-001, BMQ-SCHED-001 | Represented across retry/backoff, worker lifecycle, stalled recovery, and delayed-job rescheduling/cancellation. |
| Errors and recovery | BullMQ, Express, TypeORM, Medusa, JOSE, Redis, Axios, session cases | Represented across HTTP errors, rollback, rejection, retry, timeout, and recovery. |
| Integrations | REDIS-INT-001, AXIOS-HTTP-001 | Represented across Redis client operations and HTTP client/service interactions. |
| Configuration | EXP-CONFIG-001, VIPER-CONFIG-001 | Represented across router initialization settings and multi-source precedence/environment mapping. |
| Performance/resources | PROM-PERF-001 | Represented for a repeatable, bounded Prometheus TSDB workload. |

## 4. Explicit scope resolution and remaining limitations

The unresolved properties in [the required-property inventory](PHASE6-REQUIRED-PROPERTY-INVENTORY.md) are not silently marked as captured. They are explicitly outside the declared boundaries of the current cases and therefore **not applicable to those individual case comparisons**. They remain future extensions for broader system coverage; this audit does not claim that they are globally irrelevant.

Examples include native UI platforms and font fallback; concurrent/reordered behaviour; promotion discovery, discount application/stacking, campaign budgets and checkout; null/missing data matrices; multi-process persistence concurrency and power-loss durability; full API pagination/rate-limit contracts; messaging DLQs and delivery guarantees; credential login, refresh and MFA; other authorization policy models; TLS, CSRF/CORS and secrets management; repeatable/cron scheduling, multiple stalled jobs, and scheduler failover; compensation and distributed recovery; external-provider resilience; remote configuration/watchers; and performance scaling, latency distributions, saturation and resource budgets.

Each listed limitation remains visible in the facet matrix. It must not be promoted to captured without a new source-backed case, independent replica, discriminating probes, mutation detection, and evidence validation.

## 5. Retention and reproducibility

Most hosted CI artifacts use 30-day retention and show their expiry date in GitHub Actions. Case definitions, immutable source references, replica code, workflows, capture builders, comparators, and mutation tests are committed in the repository, so the evidence can be regenerated by rerunning the linked workflow. Before a long-term release, archive the retained runtime artifacts in the repository's durable evidence store or another approved archive.

## 6. Limitations and non-claims

- No facet is declared universally complete.
- The 23 cases do not prove equivalence for arbitrary software, arbitrary stacks, all environments, or untested behaviours.
- A case's local `replicationScope.completeness` applies only to that case's declared property inventory.
- The performance case is a bounded workload measurement, not a universal performance model.
- The UI case proves only the declared Task Board UI observations and tested runtime.
- Source-framework implementation details remain evidence/provenance; the portable rules are the normalized Software Rules records.

## 7. Phase 6 exit decision

**Phase 6 is complete for the declared 23-case cross-repository validation corpus.** The exit gate is approved with the explicit exclusions and limitations above. The next phase may review, package, release, and maintain the validated format and evidence process. New feature classes discovered during real-world replication remain eligible for future conformance cases; they do not retroactively convert this bounded exit decision into a universal-equivalence claim.
