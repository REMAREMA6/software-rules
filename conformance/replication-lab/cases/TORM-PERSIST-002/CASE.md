# Case — TypeORM file-backed commit durability and rollback recovery

**Case ID:** TORM-PERSIST-002  
**Status:** PASSED for all four file-backed durability scenarios in [run #45942572930](https://github.com/REMAREMA6/software-rules/actions/runs/45942572930). Pinned TypeORM 1.1.3 and independent Python sqlite3 matched all four post-reopen states; four deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema and cross-record integrity validation. Artifact `15172764857` retained through 2026-12-27. This is bounded SQLite file-durability evidence, not complete persistence-facet coverage.  
**Facets:** Persistence; data; behaviour; errors and recovery  
**Source:** https://github.com/typeorm/typeorm  
**Immutable source commit:** `b1e211fc2654d412612a08f8a7fb890f3352614f`  
**Source version:** TypeORM 1.1.3  
**Source stack:** TypeScript / Node.js / TypeORM / better-sqlite3  
**Replica stack:** Python 3.12 / sqlite3  
**Licence:** MIT

## Declared boundary

The case uses a file-backed SQLite database and closes/reopens the TypeORM DataSource between write and read phases. It tests committed-row durability across reopen, rollback survival, committed update durability, and constraint-failure rollback. It does not claim multi-process concurrency, production database isolation semantics, crash/power-loss durability, migrations, WAL tuning, or cross-driver equivalence.

## Technology-independent rules

1. A successful transaction commit remains visible after the database connection is closed and reopened.
2. A transaction that throws after writing rolls back all writes from that transaction; the rollback remains effective after reopen.
3. A committed update remains visible after reopen.
4. A constraint failure rolls back earlier writes in the same transaction and the database remains in its pre-transaction state after reopen.

## Probes and mutations

Four file-backed scenarios compare TypeORM and Python sqlite3. Four deliberate mutations test lost commit durability, rollback leakage, lost update durability, and partial constraint rollback.

## Acceptance gate

Accept only after all four post-reopen database states match, all four mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and cross-record integrity validation. This is bounded SQLite file-durability evidence, not complete persistence-facet coverage.
