# Source repository register

Create one Markdown record per selected source repository using SOURCE-TEMPLATE.md. Record an immutable commit SHA and verify the repository licence, setup, runtime, system boundary, and exact facets/rules under investigation before treating a candidate as an active reference.

Do not mark a facet covered merely because a repository has a feature with a similar name. Link the specific source evidence and rule-level replication cases.


## Current candidates

| Repository | Candidate facets | Inspected immutable commit | Licence status | Current evidence status |
|---|---|---|---|---|
| [BullMQ](https://github.com/taskforcesh/bullmq) | Background processing; errors/recovery; messaging candidate | 526668f2c5e6de9d5d664df577f09a6bdccac1b4 | MIT verified | Retry/backoff and message lifecycle cases pass with independent Python models, mutation tests, schema validation, and committed evidence |
| [Keycloak](https://github.com/keycloak/keycloak) | Identity/authentication; authorization; configuration | d22c7c587818ecf3517c349e9efa199b24623bbe | Apache-2.0 verified | Authentication SPI documentation inspected; runtime pending |
| [OWASP Juice Shop](https://github.com/juice-shop/juice-shop) | Security; authentication; authorization; interface; API | c9f99228d9d56afb5f5ca7925376292f7fa44b13 | MIT verified | Security challenge taxonomy inspected; target challenge and runtime pending |
| [Grafana](https://github.com/grafana/grafana) | Configuration; integrations; identity/access; API; performance | d82f399ab7ff0aba6b762f6137fe72ec06be0480 | AGPL-3.0 verified | Defaults and NATS auth settings inspected; effective runtime precedence pending |
| [TypeORM](https://github.com/typeorm/typeorm) | Persistence; data; behaviour; errors/recovery | b1e211fc2654d412612a08f8a7fb890f3352614f | MIT verified | EntityManager transaction/rollback implementation and SQLite rollback tests inspected; two-scenario TypeORM/Python comparison passes with schema validation; retained CI artifact, not repository-committed captures |
| [n8n](https://github.com/n8n-io/n8n) | Integrations; behaviour; background processing; errors | c07a0ac9c7186d893fdea2123d550e0b19a57dce | Sustainable Use License with file/edition restrictions | Test guidance inspected; select only files with verified reuse rights |
| [Prometheus](https://github.com/prometheus/prometheus) | Performance/resources; data; API; persistence | 1e794b83ad0d1df86c26fc607f87197734b9d9d9 | Apache-2.0 verified | Changelog and remote-read test located; reproducible workload still to be selected |
| [Express](https://github.com/expressjs/express) | API; behaviour; configuration; errors/recovery | 43fca52d28a422c8be48fd489cbd4f2d6152bab6 | MIT verified | HEAD/OPTIONS/default routing tests and application defaults inspected; seven-request Express/Python case passes with 28 matching projections, mutation tests, schema validation, and committed evidence |
| [Medusa](https://github.com/medusajs/medusa) | Business rules; data; behaviour; errors/recovery | 6e28e10acb9676392315b3ff1a9c7147fce4b5ab | MIT for selected community files; Enterprise paths excluded | Ten-probe Medusa/Python date-validation case passes with 40 matching projections, executable mutations, schema/integrity validation, and committed source evidence; full pricing rules remain uncovered |
| [Apache Casbin](https://github.com/apache/casbin) | Authorization; behaviour; data | fa4023fd7d02d9b7d023515e76b19b3be637f613 | Apache-2.0 verified | Ten-request Go/Python simple-RBAC case passes with four mutations and schema/integrity validation; domains, ABAC, hierarchy, and deny policies remain uncovered |
| [go-redis](https://github.com/redis/go-redis) | Integrations; errors/recovery; data | 37d4d98e2ccf59df4973df3e5de9edc87492426b | BSD 2-Clause verified | Seven-operation Go/Python Redis-client integration case passes with five mutations and schema/integrity validation; broader Redis protocol/client behaviour remains uncovered |

The register includes source candidates and selected repositories with accepted bounded cases; a case passing does not make its entire facet complete. An immutable commit and a relevant search hit do not replace a property-level evidence review, runtime capture, independent replica, or comparison.
