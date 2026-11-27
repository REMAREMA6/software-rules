# Case — TypeORM transaction commit and rollback

**Case ID:** TORM-PERSIST-001  
**Status:** Source implementation inspected; CI verification is running; not passed until pinned source execution, Python comparison, mutation tests, and Software Rules validation succeed.  
**Facets:** Persistence; Data; Behaviour; Errors and recovery  
**Source:** https://github.com/typeorm/typeorm  
**Source commit:** b1e211fc2654d412612a08f8a7fb890f3352614f  
**Source version:** 1.1.3  
**Source stack:** TypeScript / Node.js / TypeORM / SQL.js  
**Replica stack:** Python 3.12 / sqlite3  
**Licence:** MIT

## Declared boundary

One in-memory SQLite-compatible database and one table with an integer primary key and non-null text value. The case validates the transaction callback contract for one successful and one failing transaction. It does not claim that all TypeORM drivers have identical transaction semantics.

## Extracted technology-independent rules

1. A transaction callback receives a transaction-scoped manager that can read its own writes.
2. If the callback completes successfully, the transaction commits its writes and returns the callback's return value.
3. If the callback throws, the transaction rolls back its writes and rethrows the original callback error.
4. A failed transaction leaves no rows written within that transaction visible after rollback.

## Source evidence

- packages/typeorm/src/entity-manager/EntityManager.ts: transaction creates/reuses a query runner, starts a transaction, passes queryRunner.manager to the callback, commits and returns the callback result; on callback/commit error it attempts rollback and rethrows the original error; a query runner created by the method is released in finally.
- packages/typeorm/src/driver/sqlite-abstract/AbstractSqliteQueryRunner.ts: top-level SQLite transaction uses BEGIN TRANSACTION, COMMIT, and ROLLBACK; nested transactions use savepoints. This case covers only the top-level transaction.
- The source commit and package version are pinned. CI compiles the checked-out TypeORM source and runs the probe against SQL.js; it does not substitute a separately published package.

## Probe matrix

| Scenario | Required observation |
|---|---|
| Rollback | Read the inserted row inside the callback; throw a sentinel error; verify the original error is rethrown and the post-rollback table is empty |
| Commit | Insert a row; return a sentinel value; verify the callback return is propagated and the row is visible to subsequent reads |

## Independent replica and mutation

Python sqlite3 implements the same declared transaction contract without importing TypeORM. Comparator tests mutate rollback visibility, error propagation, commit persistence, and callback return propagation. Each mutation must be detected.

## Acceptance gate

Do not mark this case passed until the pinned source commit compiles and runs, source and replica captures match, mutation tests pass, schema/integrity validation passes, and evidence artifacts are retained. Driver-specific and nested transaction behaviour remain explicitly out of scope.
