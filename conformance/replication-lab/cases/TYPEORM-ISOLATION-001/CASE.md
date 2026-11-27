# Case — TypeORM/PostgreSQL transaction isolation and serializable conflict handling

**Case ID:** TYPEORM-ISOLATION-001  
**Status:** Pending runtime and evidence validation.  
**Facets:** Persistence; behaviour; data; errors and recovery  
**Source:** https://github.com/typeorm/typeorm  
**Immutable source commit:** `b1e211fc2654d412612a08f8a7fb890f3352614f`  
**Source version:** TypeORM 1.1.3  
**Database:** PostgreSQL 16  
**Source stack:** TypeScript / Node.js / TypeORM  
**Replica stack:** Python 3.12 / psycopg 3  
**Licence:** MIT

## Declared boundary

The case uses TypeORM QueryRunner transactions against PostgreSQL to compare READ COMMITTED, REPEATABLE READ, and SERIALIZABLE behaviour. It tests a non-repeatable read, stable transaction snapshot, and prevention of a write-skew anomaly. It does not cover other database engines, distributed transactions, deadlock policy, advisory locks, connection pool exhaustion, migrations, or power-loss durability.

## Technology-independent rules under test

1. Under READ COMMITTED, each statement observes a fresh committed snapshot; a second read can see another transaction's committed update.
2. Under REPEATABLE READ, repeated reads within one transaction retain the transaction snapshot despite another transaction committing an update.
3. Under SERIALIZABLE, concurrent transactions that would jointly violate a predicate invariant cannot both commit; one transaction is aborted with a serialization failure.
4. Aborted serializable work is not visible after rollback, and the invariant remains true.
5. Transaction isolation outcomes, error categories, and final persisted state are observable properties.

## Probe matrix

Three overlapping-transaction scenarios cover non-repeatable reads, repeatable-read snapshots, and serializable write-skew prevention. Six deliberate mutations test incorrect isolation mapping, snapshot refresh, write-skew acceptance, serialization error classification, and invariant accounting.

## Acceptance gate

Accept only after pinned TypeORM/PostgreSQL and independent Python/psycopg transactions match all three normalized outcomes, all six mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and evidence-integrity validation. This is bounded PostgreSQL isolation evidence, not complete persistence or database-driver coverage.
