# Source candidate — TypeORM

**Repository:** typeorm/typeorm  
**URL:** https://github.com/typeorm/typeorm  
**Immutable inspected commit:** b1e211fc2654d412612a08f8a7fb890f3352614f  
**Version at commit:** 1.1.3  
**Licence:** MIT  
**Primary stack:** TypeScript / Node.js ORM  
**Candidate facets:** Persistence; data; behaviour; errors and recovery.

## Evidence inspected

- `packages/typeorm/src/entity-manager/EntityManager.ts` lines 109 onward: `transaction(callback)` creates or reuses a QueryRunner, starts the transaction, invokes the callback with `queryRunner.manager`, commits and returns the callback result on success, attempts rollback on failure, rethrows the original error, and releases a newly created QueryRunner in `finally`.
- `packages/typeorm/src/driver/sqlite-abstract/AbstractSqliteQueryRunner.ts`: SQLite-specific transaction start, commit, and rollback operations.
- `packages/typeorm/test/functional/transaction/transaction-in-entity-manager/transaction-in-entity-manager.test.ts` lines 23–63: successful transaction operations persist after completion.
- The same test file from line 65 onward: if a later operation fails, earlier writes are not saved.

The source commit contains a frozen `pnpm-lock.yaml`. The case workflow uses pnpm 12.22.0 with `--frozen-lockfile`, compiles the pinned source, and uses the better-sqlite3 driver.

## Selected bounded rule

With a fresh in-memory SQLite database and two entities with required fields:
1. A successful `EntityManager.transaction(callback)` commits both writes and returns the callback result.
2. If a later callback operation violates a NOT NULL constraint, the error propagates and all earlier writes in that transaction are rolled back.

## Independent replica

A Python 3.12 `sqlite3` implementation is prepared under `conformance/replication-lab/projects/typeorm-transaction-python/`. It uses an explicit SQLite transaction and imports no TypeORM or Node.js code.

## Boundary

The case covers only better-sqlite3, an in-memory database, and the two declared scenarios. It does not establish behaviour for other drivers, isolation levels, nested transactions, savepoints, concurrency, or distributed transactions.

## Status

Source implementation and tests have been inspected; the independent Python replica, mutation tests, capture generator, and pinned-source workflow are prepared. Runtime comparison and Software Rules evidence validation are pending.
