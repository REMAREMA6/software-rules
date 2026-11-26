# Task Board conformance target

This directory contains two independently authored implementations of the same small task-management product.

- `reference/index.html`: reference implementation. State is held in an array; controls are bound directly to rendered elements.
- `independent/index.html`: independent implementation. State is held in a Map; interactions use delegated event handling and rendering is derived from the selected view.

## Shared observable contract

1. Create a task from a non-empty title.
2. New tasks start incomplete.
3. All, Active, and Completed filters select the corresponding task subset.
4. Completing a task changes its completed state and active count.
5. Deleting a task removes it.
6. Task create/update/delete operations use JSON requests at `/api/tasks`.

## Intentional difference under test

The implementations are deliberately kept equivalent for core task operations. The comparison suite also includes a controlled mutation scenario in which the independent build's task summary uses an intentionally altered pluralization rule. This is a test mutation, not a claim about the baseline build.

## API boundary

The HTML clients call a JSON API. The browser conformance harness supplies a deterministic in-memory HTTP adapter for `/api/tasks`. API captures therefore describe observed client-to-adapter HTTP exchanges, not a production backend or durable database. Persistence beyond the test session is outside scope.

## Running locally

Open either HTML file in a modern browser. For complete interaction testing, serve the directory over HTTP and provide the documented JSON API routes. The conformance harness uses a controlled API adapter and a fixed 1280×800 CSS-pixel viewport.
