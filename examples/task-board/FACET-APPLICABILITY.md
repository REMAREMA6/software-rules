# Task Board — 15-facet applicability assessment

**Date:** 2026-11-26  
**Status:** Boundary audit; not a Phase 6 exit approval  
**Target:** The three static browser implementations plus the deterministic in-memory Playwright API adapter.

## Target boundary

The target is the complete Task Board fixture as committed in this directory: HTML, CSS, browser JavaScript, and the deterministic API adapter used by the conformance harness. It is not a deployed full-stack Task Board service. The fixture has no production backend, durable database, identity provider, role model, message broker, external integration, or worker process.

This assessment distinguishes:
- a facet that is genuinely exercised by this target;
- a facet absent from this target's declared boundary;
- a facet that is relevant but only partially observed.

Absence from this toy fixture is not evidence that the facet is generally unnecessary. Facets outside this target's boundary remain uncovered by the project's multi-facet programme and require a richer target.

## Facet matrix

| # | Facet | Target applicability | Evidence / finding | Phase 6 disposition |
|---:|---|---|---|---|
| 1 | Interface | Applicable | Runtime DOM, resolved CSS, geometry, accessibility snapshots, screenshots, and tested UI states. Responsive, focus, hover, and colour-scheme probes are being added. | In progress |
| 2 | Behaviour | Applicable | Create, complete, filter, delete, keyboard operations, validation, and failure paths are exercised by Playwright. | In progress |
| 3 | Business rules | Applicable | Title trimming, blank submission, duplicate acceptance, initial completion, and count/filter rules have runtime samples. No finite maximum title length is established. | Partial |
| 4 | Data | Applicable at adapter boundary | Task fields/types, identifier samples, JSON exchanges, and PATCH field preservation are observed. Nullability, malformed payloads, and full constraints remain unresolved. | Partial |
| 5 | Persistence | Outside target boundary | The browser implementations keep state in memory; the test adapter resets for each page execution. There is no durable store or transaction system in this fixture. | Not covered; requires another target |
| 6 | API | Applicable only at deterministic adapter boundary | Playwright records JSON POST/PATCH/DELETE exchanges and simulated status failures. This is not a production server or network API. | Partial/bounded |
| 7 | Messaging | Outside target boundary | Source inspection of the complete three HTML fixtures finds no message broker, publish/subscribe channel, or asynchronous message-delivery subsystem. | Not applicable to this target; not covered by project-wide capture |
| 8 | Identity and authentication | Outside target boundary | The fixture has no login, credential, principal, session, or identity-provider flow. | Not applicable to this target; not covered by project-wide capture |
| 9 | Authorization and permissions | Outside target boundary | The fixture has no users, roles, protected resources, or permission-decision path. | Not applicable to this target; not covered by project-wide capture |
| 10 | Security controls | Partially applicable | HTML-like, SVG-like, and script-like task titles are tested for literal rendering and absence of injected elements/execution. This does not establish a broader security posture. | Partial; only output-encoding behaviour is in scope |
| 11 | Background processing | Outside target boundary | No job queue, scheduler, worker, retry loop, or deferred processing subsystem exists in the fixture. | Not applicable to this target; not covered by project-wide capture |
| 12 | Errors and recovery | Applicable | A rejected API operation is observed; the implementation currently has no user-facing error/recovery UI. Create, update, and delete failure probes are being added. | In progress |
| 13 | Integrations | Outside target boundary | The adapter is local and deterministic; the fixture has no external-system client or dependency. | Not applicable to this target; not covered by project-wide capture |
| 14 | Configuration | Limited | The harness records browser/runtime conditions. The static app has no demonstrated application-level runtime configuration surface. | Limited; environment capture only |
| 15 | Performance and resource behaviour | Limited | Navigation/paint/resource measurements are being added for a controlled local browser run. There is no workload, throughput, resource-budget, or production SLO contract. | Partial; local measurements only |

## Source inspection boundary

The three application files are complete, self-contained HTML documents. They define their own styles and browser-side behaviour. The only network-shaped calls are the Task Board JSON requests intercepted by the Playwright adapter. No additional server, database, authentication, authorization, messaging, integration, or background-worker source is present in this fixture directory.

This is a source-boundary finding, not runtime proof that a deployed system elsewhere has no such components. The target is deliberately defined as these committed fixture files and the test adapter; production services are excluded.

## Phase 6 consequence

The Task Board can validate multi-facet capture for the facets it actually implements. It cannot complete the project's Phase 6 objective across the accepted 15-facet catalogue by relabelling absent full-stack facets as universally irrelevant.

To close Phase 6 as a multi-facet programme, add a richer controlled reference target that actually exercises persistence, messaging, identity/authentication, authorization, security controls, background processing, integrations, application configuration, and meaningful performance behaviour. Capture those facets at runtime, build an independent implementation/capture, and compare the results. The Task Board remains the interface/behaviour/data/API conformance fixture.
