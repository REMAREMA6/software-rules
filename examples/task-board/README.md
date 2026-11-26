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

All three inventories are now explicitly **incomplete**. Each contains 29 entries: 18 captured properties, seven partial properties, one explicitly not-applicable property, and three optional exclusions. The added partial properties cover font rendering, title normalization, initial completion defaults, summary-count rules, task record shape, identifier generation, and PATCH field-preservation semantics. This is intentional: the existing runs contain useful samples but do not establish the full rules or boundary conditions. The comparison reports therefore retain observed agreement/differences while reporting incomplete replication coverage.

## Captures and comparisons

- [Reference capture](captures/reference.capture.json)
- [Independent baseline capture](captures/independent.capture.json)
- [Mutated implementation capture](captures/independent-mutated.capture.json)
- [Equivalent comparison](comparisons/equivalent.json)
- [Deliberate-difference comparison](comparisons/deliberate-difference.json)
- [API facet example](api/api-payload.example.json)
- [Raw adapter events](api/raw-adapter-events.json)

The reference and independent baseline were run under Chromium 159.0.8154.6 on Linux at 1280×800 CSS px. They produced pixel-identical screenshots in all seven compared UI states (zero differing pixels in each). Keyboard-only workflows, empty/whitespace validation, API request/response traces, and HTTP 503 failure outcomes also agree. API exchanges use a deterministic in-memory adapter, not a production service.

The mutation build was run through the same workflow. It actually displayed `1 tasks · 1 active` and `1 tasks · 0 active`, while the reference displayed `1 task · 1 active` and `1 task · 0 active`. The difference report records this observed mismatch.

## Runtime conformance

The Playwright harness in [`conformance/runtime/`](../../conformance/runtime/README.md) now performs a fresh runtime capture of all three builds. It retains complete per-element computed CSS property maps, pseudo-element content, DOM hierarchy, element geometry, accessibility-tree snapshots, semantics, screenshots for each tested state, API traces, keyboard outcomes, native validation, and failed-request behavior.

The baseline reference and independent implementation are compared pixel-for-pixel in seven states at 1280×800 CSS px. The deliberate mutation is required to produce a visual difference. The harness also asserts that baseline API traces and runtime error outcomes agree.

The successful runtime run is recorded in [GitHub Actions runtime conformance run #45854435953](https://github.com/REMAREMA6/software-rules/actions/runs/45854435953). Its [task-board-runtime-captures artifact](https://github.com/REMAREMA6/software-rules/actions/runs/45854435953/artifacts/15136130524) contains the screenshots, JSON captures, and pixel-diff outputs. The artifact has a 30-day retention period; rerunning the workflow regenerates it.

**Interpretation:** pixel identity is established for the seven tested states in the recorded Chromium/Linux environment, not for every possible viewport, operating system, browser, font renderer, or untested application state. The declared scope explicitly fixes the viewport and excludes production network transport, durable persistence, authentication, and server behavior. The per-property audit also found unresolved font-rendering, business-rule, and data dimensions; all three captures now correctly report `incomplete`.

## Source-derived rule

The reference capture also contains a source-derived DELETE-call rule. It is kept separate from runtime rules, has source-artifact evidence, and remains explicitly `unverified` as runtime behavior.

## Running locally

Open either baseline HTML file in a modern browser. For complete interactions, serve the directory over HTTP and provide the documented JSON API routes. The committed captures were produced with a deterministic in-browser adapter; no production service is required to reproduce the examples.
