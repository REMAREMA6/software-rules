# Case — TypeORM transaction atomicity and rollback

**Case ID:** TYPEORM-PERSIST-001  
**Status:** PASSED for the declared two-scenario scope. Pinned TypeORM runtime and independent Python/SQLite replica match across eight facet/scenario projections; executable rollback mutation tests, Software Rules schema validation, cross-record evidence integrity, and artifact persistence all pass.  
**Facet(s):** Persistence; Data; Behaviour; Errors and recovery  
**Source:** https://github.com/typeorm/typeorm  
**Source commit:** b1e211fc2654d412612a08f8a7fb890f3352614f  
**Source version:** TypeORM 1.1.3  
**Source stack:** TypeScript / Node.js / TypeORM / better-sqlite3  
**Replica stack:** Python 3.12 / sqlite3  
**Licence:** MIT

## Declared scope

Use TypeORM's `EntityManager.transaction(callback)` with two required-field entities and an in-memory SQLite database. Probe:
1. Successful callback: both writes commit, the callback result is returned, and both rows are visible after the transaction.
2. Failing callback: two writes and reads succeed inside the transaction, a third write violates a NOT NULL constraint, the error propagates, and all earlier writes are rolled back.

This case is limited to the better-sqlite3 driver and these two scenarios. It does not establish behaviour for other drivers, isolation levels, nested transactions, concurrent operations, savepoints, or distributed transactions.

## Source evidence

- `packages/typeorm/src/entity-manager/EntityManager.ts` lines 109 onward: create/reuse a QueryRunner; start the transaction; invoke the callback with `queryRunner.manager`; commit and return the callback result on success; on failure attempt rollback and rethrow the original error; release a newly created QueryRunner in `finally`.
- `packages/typeorm/src/driver/sqlite-abstract/AbstractSqliteQueryRunner.ts` lines 77–160: SQLite transaction start, commit, and rollback implementation.
- `packages/typeorm/test/functional/transaction/transaction-in-entity-manager/transaction-in-entity-manager.test.ts` lines 23–63: successful operations are persisted after transaction completion.
- The same test file lines 65 onward: if a later operation fails, earlier writes are not persisted.

The source repository contains a committed `pnpm-lock.yaml` at the pinned commit. The runtime workflow uses the pinned pnpm version and frozen lockfile.

## Independent replica

The Python 3.12 implementation uses the standard-library `sqlite3` module and an explicit transaction context. It imports no TypeORM or Node.js code.

## Mutation tests

The replica tests deliberately commit the transaction after an exception instead of rolling it back. The comparison must detect the leaked post/category rows. Additional comparison mutations alter callback error propagation and committed callback results.

## Result

**Passed for the declared bounded scope.** The pinned TypeORM 1.1.3 source at commit `b1e211fc2654d412612a08f8a7fb890f3352614f` and the independent Python 3.12/sqlite3 model match both scenarios across eight facet/scenario projections. The executable commit-on-error mutation is detected. The Software Rules 0.2.0 source/replica captures and comparison report passed schema and cross-record evidence validation in [workflow run #5](https://github.com/REMAREMA6/software-rules/actions/runs/45927631068). Seven raw/structured evidence artifacts, including the frozen pnpm lockfile and dependency tree, are committed under `artifacts/` at [commit fabf45a](https://github.com/REMAREMA6/software-rules/commit/fabf45ae466d2b68bcc49f6596f6c6bb220ddef3). This result does not establish transaction behaviour for other database drivers, isolation levels, nested transactions, concurrency, or distributed transactions.
