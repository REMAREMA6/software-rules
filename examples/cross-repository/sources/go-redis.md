# Source — go-redis

- **Repository:** https://github.com/redis/go-redis
- **Pinned commit:** `37d4d98e2ccf59df4973df3e5de9edc87492426b`
- **Licence:** BSD 2-Clause (the pinned `LICENSE` file was inspected)
- **Module:** `github.com/redis/go-redis/v9`
- **Source stack:** Go
- **Candidate facets:** Integrations; errors and recovery; data
- **Selected bounded rule:** Redis command/response and dependency-error semantics for PING, SET/GET, missing-key GET, EXISTS, PTTL, WRONGTYPE, and connection failure.
- **Inspected files:** `go.mod`, `LICENSE`, and the client command APIs at the pinned commit.
- **Runtime verification:** The pinned Go client was executed against Redis 7 and matched an independent Python redis-py client across seven normalized operations; five mutations, Software Rules schema validation, and evidence integrity passed in [run #45932496414](https://github.com/REMAREMA6/software-rules/actions/runs/45932496414).

The selected case tests the external Redis boundary and normalized outcomes. It does not claim that two client libraries have identical internals or cover the full Redis command surface.
