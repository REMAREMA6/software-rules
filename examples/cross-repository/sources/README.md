# Source repository register

Create one Markdown record per selected source repository using SOURCE-TEMPLATE.md. Record an immutable commit SHA and verify the repository licence, setup, runtime, system boundary, and exact facets/rules under investigation before treating a candidate as an active reference.

Do not mark a facet covered merely because a repository has a feature with a similar name. Link the specific source evidence and rule-level replication cases.

**Current register:** 13 immutable source repositories. A repository may support more than one bounded case; a passing case does not complete its entire facet.

## Source register

| Repository | Candidate facets | Inspected immutable commit | Licence status | Current evidence status |
|---|---|---|---|---|
| [BullMQ](https://github.com/taskforcesh/bullmq) | Background processing; errors/recovery; messaging | `526668f2c5e6de9d5d664df577f09a6bdccac1b4` | MIT verified | BMQ-ER-002 retry/backoff and BMQ-MSG-001 message lifecycle pass with independent Python models, mutation tests, Software Rules schema validation, and evidence integrity. |
| [Keycloak](https://github.com/keycloak/keycloak) | Identity/authentication; authorization; configuration | `d22c7c587818ecf3517c349e9efa199b24623bbe` | Apache-2.0 verified | Authentication SPI documentation inspected; runtime identity/session lifecycle case pending. |
| [OWASP Juice Shop](https://github.com/juice-shop/juice-shop) | Security; authentication; authorization; interface; API | `c9f99228d9d56afb5f5ca7925376292f7fa44b13` | MIT verified | Security challenge taxonomy inspected; target challenge and runtime pending. |
| [Grafana](https://github.com/grafana/grafana) | Configuration; integrations; identity/access; API; performance | `d82f399ab7ff0aba6b762f6137fe72ec06be0480` | AGPL-3.0 verified | Defaults and NATS auth settings inspected; effective runtime precedence pending. |
| [TypeORM](https://github.com/typeorm/typeorm) | Persistence; data; behaviour; errors/recovery | `b1e211fc2654d412612a08f8a7fb890f3352614f` | MIT verified | TORM-PERSIST-001 transaction commit/rollback matches Python sqlite3 across two scenarios and eight projections; schema/integrity passed. CI evidence artifact retained. |
| [n8n](https://github.com/n8n-io/n8n) | Integrations; behaviour; background processing; errors | `c07a0ac9c7186d893fdea2123d550e0b19a57dce` | Sustainable Use License with file/edition restrictions | Test guidance inspected; select only files with verified reuse rights. |
| [Prometheus](https://github.com/prometheus/prometheus) | Performance/resources; data; API; persistence | `1e794b83ad0d1df86c26fc607f87197734b9d9d9` | Apache-2.0 verified | PROM-PERF-001 runs pinned TSDB write benchmark and independent Python workload model three times each; sample accounting matches, mutation tests and Software Rules schema/integrity pass in [run #45938387274](https://github.com/REMAREMA6/software-rules/actions/runs/45938387274). |
| [Express](https://github.com/expressjs/express) | API; behaviour; configuration; errors/recovery | `43fca52d28a422c8be48fd489cbd4f2d6152bab6` | MIT verified | EXP-API-001 matches seven requests/28 projections; EXP-CONFIG-001 matches five routing configuration profiles/18 path observations, including lazy router configuration snapshot semantics. |
| [Medusa](https://github.com/medusajs/medusa) | Business rules; data; behaviour; errors/recovery | `6e28e10acb9676392315b3ff1a9c7147fce4b5ab` | MIT for selected community files; Enterprise paths excluded | MEDUSA-BR-001 date validation and MEDUSA-PRICE-001 exact pinned calculated/original price-selection method both pass independent Python comparisons, mutation tests, and Software Rules schema/integrity validation. |
| [Apache Casbin](https://github.com/apache/casbin) | Authorization; behaviour; data | `fa4023fd7d02d9b7d023515e76b19b3be637f613` | Apache-2.0 verified | CASBIN-AUTHZ-001 simple RBAC plus CASBIN-ADV-AUTHZ-001 domain RBAC, ABAC, deny override, and policy mutation pass independent Python comparisons and mutation/schema/integrity checks. |
| [go-redis](https://github.com/redis/go-redis) | Integrations; errors/recovery; data | `37d4d98e2ccf59df4973df3e5de9edc87492426b` | BSD 2-Clause verified | REDIS-INT-001 matches seven Go/Python Redis client operations against Redis 7; five mutations and Software Rules schema/integrity pass. |
| [jose](https://github.com/panva/jose) | Identity/authentication; security; behaviour; data; errors/recovery | `f4457b3e3c5a40359b40ad6fa9721d11aa2a2bd0` | MIT verified | JOSE-AUTH-001 matches 11 JWT verification scenarios/55 projections with eight mutations and Software Rules validation; full identity/session lifecycle remains uncovered. |
| [Axios](https://github.com/axios/axios) | Integrations; API; behaviour; errors/recovery | `71c87d506567e2fe37ba9f6fae6a4fc9411583d0` | MIT verified | AXIOS-HTTP-001 matches nine pinned Axios/Python urllib HTTP interactions; six mutations and Software Rules schema/integrity pass in [run #45940398493](https://github.com/REMAREMA6/software-rules/actions/runs/45940398493). |

A source record is not a facet completion claim. An immutable commit and a relevant source hit do not replace a property-level evidence review, runtime capture, independent replica, mutation test, or comparison.
