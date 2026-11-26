# Source candidate — TypeORM

**Repository:** typeorm/typeorm  
**URL:** https://github.com/typeorm/typeorm  
**Immutable inspected commit:** b1e211fc2654d412612a08f8a7fb890f3352614f  
**Licence:** MIT (LICENSE at inspected commit)  
**Primary stack:** TypeScript/JavaScript ORM; supports multiple database drivers.  
**Candidate facets:** Persistence; data; API-independent transaction semantics; errors/recovery.

## Evidence inspected

- The changelog at the inspected commit includes a fix concerning query data being preserved for commit/rollback subscribers.
- This search hit alone is insufficient to establish transaction semantics. The transaction implementation and tests must be inspected at the same commit before selecting a concrete rule.

## Candidate rule areas

Transaction commit/rollback outcomes; subscriber notification order; preservation of transaction-scoped data; behaviour when operations fail.

## Boundary and limitations

Choose one database driver and pin its version/configuration. ORM abstraction does not guarantee identical behaviour across every supported database. Record driver-specific semantics and do not claim all-driver equivalence from one test.

**Status:** candidate only; no Phase 6 pass claimed.
