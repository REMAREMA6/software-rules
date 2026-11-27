# Source candidate — TypeORM

**Repository:** typeorm/typeorm  
**URL:** https://github.com/typeorm/typeorm  
**Immutable inspected commit:** b1e211fc2654d412612a08f8a7fb890f3352614f  
**Source package version:** 1.1.3  
**Licence:** MIT  
**Primary stack:** TypeScript / JavaScript ORM; multiple database drivers.  
**Investigated facets:** Persistence; data; behaviour; errors and recovery.

## Evidence inspected at the pinned commit

- `packages/typeorm/src/entity-manager/EntityManager.ts`, `transaction` overload and implementation: starts a transaction, invokes the callback with the query runner's manager, commits and returns the callback result; on error it attempts rollback and rethrows the original error; it releases a query runner created by the method in `finally`.
- `packages/typeorm/src/driver/sqlite-abstract/AbstractSqliteQueryRunner.ts`: top-level SQLite-compatible transactions use `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK`; nested transaction depth uses savepoints.
- `packages/typeorm/src/driver/sqljs/SqljsDriver.ts`: SQL.js is an implemented SQLite-compatible driver suitable for a deterministic in-memory probe.

## Selected case

`TORM-PERSIST-001` exercises one rollback and one commit against the pinned source checkout using the SQL.js driver. The independent replica uses Python 3.12 sqlite3. It checks read-your-writes inside the callback, rollback visibility, original error propagation, commit visibility, and callback return propagation.

## Boundaries

This is a single-driver, top-level transaction case. It does not establish identical semantics for every TypeORM driver, nested/savepoint behaviour, concurrent transactions, isolation levels, crash recovery, or durable storage across process restarts.

## Status

Source implementation and driver paths are inspected. A pinned-source compile/runtime workflow and independent Python replica have been added. No case pass is claimed until the workflow, comparison, mutation tests, and Software Rules artifact validation are verified.
