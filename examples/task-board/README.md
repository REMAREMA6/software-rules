# Task Board conformance target

This directory contains two independently authored implementations of the same task-management product and one deliberately mutated test build.

## Applications

- `reference/index.html` — reference implementation; array-backed state and direct event handlers.
- `independent/index.html` — independent baseline; Map-backed state, derived rendering, and delegated event handling.
- `independent-mutated/index.html` — mutation build with one intentional defect: the singular task count is rendered as `1 tasks`.

## Shared observable contract

1. Create a task from a non-empty title.
2. New tasks start incomplete.
3. All, Active, and Completed filters select the corresponding task subset.
4. Completing a task changes its completed state and active count.
5. Deleting a task removes it.
6. Create/update/delete operations use JSON exchanges at `/api/tasks`.

## Replication-scope inventory

Each capture includes `replicationScope.propertyInventory`, which lists the properties required to reproduce the declared Task Board scope. Every item records its facet, subject, dimension, required/optional status, capture state, and evidence references where available.

The current inventories intentionally mark all three captures **incomplete**. The initial DOM/style/geometry snapshots are partial; no retained screenshot or pixel comparison is linked; and keyboard, validation, error/recovery, and other relevant states remain unobserved. The comparison reports separately record agreement among observed properties and replication completeness. Matching selected properties does **not** establish full screen equivalence or faithful replication.

## Captures and comparisons

- [Reference capture](captures/reference.capture.json)
- [Independent baseline capture](captures/independent.capture.json)
- [Mutated implementation capture](captures/independent-mutated.capture.json)
- [Equivalent comparison](comparisons/equivalent.json)
- [Deliberate-difference comparison](comparisons/deliberate-difference.json)
- [API facet example](api/api-payload.example.json)
- [Raw adapter events](api/raw-adapter-events.json)

The baseline pair was run under the same isolated Chromium environment and 1280×800 CSS-pixel viewport. Both produced the same initial main-container geometry and the same create/complete/filter/delete outputs. The API exchanges were instrumented at the deterministic in-memory adapter boundary. They do not establish production network, server, database, authentication, or persistence behavior.

The mutation build was run through the same workflow. It actually displayed `1 tasks · 1 active` and `1 tasks · 0 active`, while the reference displayed `1 task · 1 active` and `1 task · 0 active`. The difference report records this observed mismatch.

## Source-derived rule

The reference capture also contains a source-derived DELETE-call rule. It is kept separate from runtime rules, has source-artifact evidence, and remains explicitly `unverified` as runtime behavior.

## Running locally

Open either baseline HTML file in a modern browser. For complete interactions, serve the directory over HTTP and provide the documented JSON API routes. The committed captures were produced with a deterministic in-browser adapter; no production service is required to reproduce the examples.
