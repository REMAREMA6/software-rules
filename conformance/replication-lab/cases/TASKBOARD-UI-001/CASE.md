# Case — Cross-stack Task Board interface and workflow replication

**Case ID:** TASKBOARD-UI-001  
**Status:** Runtime comparison passed in [run #45934299299](https://github.com/REMAREMA6/software-rules/actions/runs/45934299299): zero differing pixels across three viewport sizes and six workflow states; semantic snapshots matched; deliberate active-count mutation detected. Schema-native capture generation and validation are being added before acceptance.  
**Source:** `examples/task-board/reference/index.html` on the repository's pinned commit  
**Source stack:** HTML, CSS, browser-native JavaScript  
**Replica stack:** React 19.1.1, JSX, Vite 7.1.7  
**Replica runtime:** Chromium, served as a production Vite build  
**Facet:** Interface (behavioural workflows are used as state-transition probes; API traces are test controls, not claims of full API-facet coverage)

## Declared boundary

The source is the self-contained Task Board reference document and its browser-visible client behaviour. The API is a deterministic in-memory test adapter, not a production server. Authentication, durable persistence, external integrations, and server-side business logic are outside this case.

The replica is independently implemented in React. It does not import the source HTML or its JavaScript. It must reproduce the declared rendered interface, semantics, and client workflows through its own React state and event handlers.

## Rules to capture and compare

- Page geometry, typography, colours, borders, spacing, and task-row presentation.
- Empty, populated, completed, active-filter, and completed-filter states.
- Task title input, creation, completion toggle, deletion, and summary counts.
- Accessible names, filter pressed state, native required-field semantics, and live summary.
- Equivalent POST, PATCH, and DELETE adapter requests and resulting visible state.
- Deterministic failed-request propagation where exercised.

## Captured interface properties

The accepted capture scope is limited to six required properties: viewport geometry, responsive layout at 1280/768/320 CSS px, exact visual presentation, semantic hierarchy, accessible control state, and workflow-state presentation. It explicitly excludes other browsers/operating systems, unprobed hover/focus/colour-scheme states, font fallback across environments, production APIs, persistence, and other software facets.

## Required discriminating probes

1. Pixel comparison at 1280×800 for empty, populated, completed, and filtered states.
2. DOM/semantic comparison for headings, form controls, navigation, list items, accessible names, and live summary.
3. Create, complete, filter, toggle-back, delete, and blank submission workflows.
4. Responsive screenshot comparison at 320×720 and 768×900.
5. Deliberately mutate the replica's active-count calculation and verify that the same probes detect the mismatch.

## Acceptance gate

This case passes only after the pinned source and React production build execute in CI; all declared probes are captured; source/replica observations are compared; the intentional mutation is detected; and Software Rules captures, schema validation, and evidence-integrity checks pass. Matching CSS declarations alone are not acceptance evidence.

## Limitations

A passing case establishes only this declared Task Board boundary and the tested Chromium conditions. It does not establish full interface-facet completeness, cross-browser font/raster equivalence, production API behaviour, or whole-system replication.
