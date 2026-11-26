# Phase 6 — Facet investigation notes

**Status:** Superseded as the primary execution plan.  
**Current programme:** [Cross-repository, cross-stack replication](CROSS-REPOSITORY-REPLICATION-PROGRAM.md).

This document preserves the original facet investigation notes and Task Board probe backlog. Its earlier recommendation to create one richer full-stack reference target is superseded.

Phase 6 now uses multiple source repositories and an independent replication lab. Each source repository is selected for the rules it actually contains. Those rules are extracted into the technology-independent Software Rules model, independently implemented in another stack, exercised with equivalent scenarios, compared, and mutation-tested.

The Task Board remains a bounded fixture for its tested interface, behaviour, business-rule, data, and in-memory API-adapter observations. It is not required to implement persistence, identity, messaging, integrations, or background processing. Those facets are validated from other suitable source repositories.

For the full 15-facet matrix, source register, evidence requirements, case structure, and exit gate, follow the current programme linked above.
