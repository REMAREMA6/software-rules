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

All three inventories are now explicitly **incomplete**. Each contains 34 entries: 28 captured properties, two partial properties, one explicitly not-applicable property, and three optional exclusions. The remaining partial properties are font rendering beyond the recorded Chromium/Linux conditions and the maximum title-length constraint. The expanded run also captured title trimming, duplicate-title acceptance, literal rendering of HTML-like/Unicode text, acceptance of a 512-character title, mixed-task counts/filters, bidirectional completion toggling, multiple deletion, task record shape, sequential string identifiers within the adapter session, and PATCH field preservation. The inventories remain incomplete; the comparison reports preserve observed agreement/differences separately.

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

The expanded probes were executed successfully in [GitHub Actions Phase 6 run #45858743131](https://github.com/REMAREMA6/software-rules/actions/runs/45858743131). Its [phase6-expanded-runtime-evidence artifact](https://github.com/REMAREMA6/software-rules/actions/runs/45858743131/artifacts/15136459580) contains 41 files, including per-variant JSON captures, probe results, screenshots, and pixel-diff outputs. The artifact expires after 30 days; rerunning the workflow regenerates it.

The earlier baseline run is [#45854435953](https://github.com/REMAREMA6/software-rules/actions/runs/45854435953).

**Interpretation:** pixel identity is established for the seven tested states in the recorded Chromium/Linux environment, not for every possible viewport, operating system, browser, font renderer, or untested application state. The declared scope explicitly fixes the viewport and excludes production network transport, durable persistence, authentication, and server behavior. The per-property audit also found unresolved font-rendering, business-rule, and data dimensions; all three captures now correctly report `incomplete`.

## Source-derived rule

The reference capture also contains a source-derived DELETE-call rule. It is kept separate from runtime rules, has source-artifact evidence, and remains explicitly `unverified` as runtime behavior.

## Running locally

Open either baseline HTML file in a modern browser. For complete interactions, serve the directory over HTTP and provide the documented JSON API routes. The committed captures were produced with a deterministic in-browser adapter; no production service is required to reproduce the examples.
