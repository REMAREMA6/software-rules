# Standards and Prior-Art Review

**Maturity:** Draft  
**Review version:** 0.1.0  
**Research date:** 2026-11-26

## 1. Executive conclusion

None of the reviewed standards provides the complete artifact Software Rules needs: a technology-independent, evidence-backed representation of what a running software system actually does and exposes across multiple facets, suitable for comparison against an independent implementation.

The recommended approach is to **compose and map to established standards where they fit**, while defining the missing cross-facet capture, provenance, coverage, uncertainty, normalization, and comparison model ourselves.

Strongest inputs:
- DOM/CSSOM, WebDriver, WAI-ARIA, and native UI automation for runtime interface inspection.
- Gherkin for preconditions, triggers, and observable outcomes.
- OpenTelemetry for runtime operation/event context and cross-language semantic conventions.
- OpenAPI, AsyncAPI, and HTTP semantics for API and messaging interfaces.
- SBVR for business vocabulary and business rules.
- ISO/IEC/IEEE 29148, OMG MDA, and UML for requirements quality, platform independence, and selected structural/behavioural models.
- JSON Schema 2020-12 for machine validation after the conceptual model is stable.
- Design Tokens Format for reusable design-system values, not full runtime appearance.

## 2. Problem being evaluated

Software Rules is intended to support this sequence:

1. Select a reference system and define scenarios.
2. Trigger those scenarios against the actual running system.
3. Capture runtime-observed facts, conditions, state, outputs, and evidence in a fixed technology-independent format.
4. Build an independent implementation using another stack.
5. Run equivalent scenarios against that implementation.
6. Capture it using the same format.
7. Compare captures and report matches, mismatches, unknowns, and coverage.

The primary artifact is not source code, a design mockup, a requirements list, or an implementation plan. It is a structured representation of evidence about a system in execution.

Source inspection may guide the investigator toward routes, actions, conditions, and likely test cases. Source declarations alone cannot establish that a rule executes or that a declared result is actually produced. Source-derived inferences must remain separate from runtime observations.

### 2.1 Contract versus observation

Several standards describe what a system is supposed to expose or what an implementation claims to support. Those descriptions are useful, but they are not proof of what the running system does.

Software Rules must distinguish:
- **Declared contract:** what a specification or published interface contract says should happen.
- **Runtime observation:** what was observed when the system executed under stated conditions.
- **Source-derived inference:** what source inspection suggests without runtime confirmation.

A discrepancy between a declared contract and runtime behaviour is valuable evidence. The capture model must not silently choose one and discard the other.

## 3. Comparative assessment

| Standard or format | Main contribution | Relevance | What it does not provide |
|---|---|---|---|
| ISO/IEC/IEEE 29148 | Requirements engineering processes and information-item quality | High for specification discipline | Runtime capture and cross-implementation comparison |
| OMG MDA | Platform-independent and platform-specific model separation | High for technology independence | General runtime observation interchange |
| UML 2.5.1 | Structural and behavioural modelling notation and metamodel | Medium-high for selected models | Evidence-backed runtime capture of all facets |
| OMG SBVR 1.5 | Formal business vocabulary and business-rule semantics | High for business rules | Complete software execution observation |
| OpenAPI 3.2.1 | Language-independent HTTP API description | High for API contracts | Proof of actual runtime responses or whole-system behaviour |
| AsyncAPI 3.1.0 | Event-driven API and message contract description | High for messaging | Complete delivery traces or general system capture |
| OpenTelemetry | Cross-language telemetry model and semantic conventions | High for runtime operation evidence | Exhaustive observation or full intended-behaviour specification |
| DOM and CSSOM | Web document structure and resolved style inspection | Very high for web UI capture | Native UI, backend rules, or full pixel equivalence |
| WebDriver | Platform- and language-neutral browser control and introspection | High for reproducible browser scenarios | Canonical complete capture schema |
| WAI-ARIA 1.2 | Accessible roles, states, and properties | High as a complementary UI semantic layer | Visual geometry, full styling, or general behaviour |
| Android UI Automator | Native Android UI hierarchy, properties, bounds, and interaction | High for Android UI capture | Full visual styling or cross-platform capture |
| Gherkin / Cucumber | Scenario structure: context, event, expected outcome | High for triggers and conditions | Complete structured runtime observations |
| JSON Schema 2020-12 | Machine validation of JSON structure and constraints | Very high for schema validation | Domain semantics, runtime truth, or comparison logic |
| Design Tokens Format 2025.10 | Interchange of platform-agnostic design tokens | Medium for design-system values | Per-node resolved styles, geometry, stacking, or runtime state |
| HTTP Semantics (RFC 9110) | Standard protocol semantics for HTTP | High for HTTP observations | Application business logic or non-HTTP facets |

## 4. Detailed findings

### 4.1 ISO/IEC/IEEE 29148 — requirements engineering

**Status:** ISO/IEC/IEEE 29148:2018, Edition 2, published and confirmed in 2024. ISO lists Edition 3 as a Draft International Standard under development; it entered the enquiry phase in 2026.

**Contribution:** Requirements-engineering processes and information items, including guidance on contents and formats. Relevant to precision, traceability, completeness, and review discipline.

**Limitation:** It is not a schema for capturing actual runtime state and outputs across arbitrary software facets. It does not solve runtime evidence collection or independent capture comparison.

**Treatment:** Reuse principles for specification quality; do not adopt it as the capture format. Monitor Edition 3, but do not cite the DIS as a published International Standard.

### 4.2 OMG Model Driven Architecture (MDA)

**Contribution:** MDA starts with a Platform-Independent Model (PIM) describing business functionality and behaviour without tying it to a particular technology. Platform-Specific Models (PSMs) describe realization on particular platforms.

**Limitation:** MDA is a model-driven engineering approach. It does not prescribe inspection of a running system, runtime evidence capture, or comparison of actual outcomes.

**Treatment:** Adopt the platform-independence principle, not the full MDA workflow. Describe observable meaning independently of implementation technology; do not require a PIM-to-PSM pipeline or treat a model as proof of runtime behaviour.

### 4.3 UML 2.5.1

**Status:** UML 2.5.1, adopted December 2017. OMG publishes the normative specification and machine-readable XMI metamodel documents.

**Contribution:** Established structural and behavioural models, including class, component, activity, state-machine, and sequence models. The metamodel and XMI artifacts are useful references for formal model structure and interchange.

**Limitation:** UML models often describe design or intended behaviour rather than facts from a particular execution. They do not automatically record runtime values, evidence, environment, or comparison coverage.

**Treatment:** Optional modelling aid. Use UML where it clarifies a facet; do not require every capture to become a UML model.

### 4.4 OMG SBVR 1.5

**Status:** SBVR 1.5, adopted December 2019; OMG publishes normative machine-readable XMI-related artifacts.

**Contribution:** Formal approach to business vocabulary and business rules. Relevant to domain constraints, obligations, permissions, calculations, and decisions.

**Limitation:** It does not cover UI geometry, API traces, background job execution, or the complete evidence and comparison lifecycle.

**Treatment:** Reuse concepts for the business-rules facet. Preserve runtime evidence showing when a rule was evaluated and what result occurred. A rule declaration does not prove that an implementation enforces it.

### 4.5 OpenAPI Specification

**Status:** OpenAPI 3.2.1, dated 10 September 2026.

**Contribution:** Programming-language-agnostic HTTP API description, including paths, operations, parameters, request/response bodies, status codes, schemas, and security requirements.

**Limitation:** An OpenAPI document is a contract/description. It does not establish that a live service conforms to it or describe the complete system. A declared response schema is not evidence that a particular response occurred.

**Treatment:** Map the API facet to OpenAPI where possible, but keep declared contracts separate from actual runtime exchanges. Capture observed method, target, status, headers, payload, and execution conditions.

### 4.6 AsyncAPI 3.1.0

**Contribution:** Describes event-driven and message-based APIs, including channels, operations, messages, payloads, and protocol bindings.

**Limitation:** It describes communication contracts, not a complete runtime record of actual delivery, ordering, retries, duplicates, processing outcomes, or end-to-end state changes.

**Treatment:** Map the messaging facet to AsyncAPI concepts. Separately record observed publish/receive/processing events and evidence for delivery, ordering, correlation, and outcome.

### 4.7 OpenTelemetry

**Contribution:** Cross-language telemetry model. A span represents an operation with identity, parent/child relationships, timestamps, attributes, events, links, and status. Semantic conventions provide common names across languages and technologies. Events represent point-in-time occurrences such as state changes, checkpoints, lifecycle events, and exceptions.

**Limitation:** Telemetry is not automatically exhaustive. It depends on instrumentation, sampling, configuration, retention, and what developers record. An absent span/event does not prove an operation did not occur. Telemetry does not define all expected software rules or a cross-stack equivalence report.

**Treatment:** Reuse operation identity, causal relationships, timestamps, events, attributes, and semantic names selectively. Preserve observation method and coverage limitations. Missing telemetry must not be interpreted as proof of absence.

### 4.8 DOM and CSSOM

**Status:** WHATWG DOM is a living standard. The reviewed CSSOM publication is a W3C Working Draft dated 26 August 2021. Its resolved-values section describes values returned by getComputedStyle().

**Contribution:** DOM provides a structured web document tree. CSSOM exposes style-related state. Resolved CSS values are relevant to capturing effective browser values after cascade and related processing, rather than copying source declarations.

**Limitation:** Web-specific. A resolved CSS value is not a complete pixel-level rendering record. It does not alone capture all geometry, stacking, compositing, animation, font rendering, or screenshot details. CSSOM's reviewed publication status is Working Draft and must be checked before relying on it as a stable normative dependency.

**Treatment:** Define a web runtime capture profile. Capture actual DOM hierarchy and relevant attributes/properties, resolved styles, geometry, visibility, stacking/paint-related information where available, accessibility semantics, assets, and screenshots where visual evidence is needed. Preserve source declarations separately from resolved runtime values.

### 4.9 WebDriver

**Status:** W3C WebDriver Working Draft dated 9 November 2026.

**Contribution:** Platform- and language-neutral remote-control protocol for browser introspection and control. Useful for reproducible actions such as locating elements, clicking, typing, and controlling a user agent.

**Limitation:** It is an automation/control protocol, not a canonical whole-page capture schema. It does not standardize every browser-internal or rendered visual property. The reviewed publication is a Working Draft, not a W3C Recommendation.

**Treatment:** Use as a scenario execution adapter where suitable. Extraction may additionally require DOM/CSSOM access, browser inspection interfaces, accessibility information, and image evidence.

### 4.10 WAI-ARIA 1.2

**Status:** WAI-ARIA 1.2, W3C Recommendation dated 6 June 2023.

**Contribution:** Defines roles, states, and properties for accessible UI semantics, including button, checkbox, navigation, checked, expanded, and disabled.

**Limitation:** Accessibility semantics do not describe full visual presentation, geometry, stacking, or all interaction behaviour. Accessibility representation is related to, but not interchangeable with, DOM or rendered pixels.

**Treatment:** Include accessibility semantics as a distinct UI observation dimension alongside hierarchy, geometry, resolved style, and interaction state.

### 4.11 Android UI Automator

**Reviewed API:** AndroidX Test UI Automator UiObject2.

**Contribution:** Exposes native Android UI object properties and relationships such as parent, text, content description, visible bounds, and drawing order. Supports interaction with UI objects.

**Limitation:** Android-specific, not a platform-neutral specification. The UI object representation does not expose every visual rendering property. Screenshots or additional instrumentation may still be required.

**Treatment:** Define native-UI adapter profiles, beginning with Android as one platform example. Map facts to platform-neutral concepts while preserving adapter metadata and source fields. Treat screenshots as complementary evidence.

### 4.12 Gherkin / Cucumber

**Contribution:** Scenario structure using Given for initial context, When for an event/action, and Then for an expected outcome. It encourages implementation details to remain hidden in step definitions and outcomes to be observable to users or external systems.

**Limitation:** Gherkin is a scenario language, not a complete record of every runtime property. An expected Then outcome must not be confused with the actual value captured during execution.

**Treatment:** Reuse the scenario pattern, but separate expected outcomes from actual observations. Capture actual runtime observations and supporting evidence independently.

### 4.13 JSON Schema 2020-12

**Status:** JSON Schema Draft 2020-12, published 16 June 2022.

**Contribution:** Standard way to describe and validate JSON structure and constraints, with reusable schemas, references, vocabularies, and validation outputs.

**Limitation:** A structurally valid document can still be factually wrong, unsupported by evidence, contradictory, or incomplete. JSON Schema cannot prove runtime truth or equivalence.

**Treatment:** Use for machine validation after the conceptual model is stable. Pair with semantic checks, evidence checks, conformance fixtures, and comparison tests. Pin the dialect explicitly.

### 4.14 Design Tokens Community Group Format 2025.10

**Status:** Design Tokens Format Module 2025.10, published 28 October 2025 as a Final Community Group Report. It explicitly states that it is not a W3C Standard and is not on the W3C Standards Track; it describes itself as stable and intended for implementation.

**Contribution:** Platform-agnostic interchange format for reusable design tokens such as color, dimension, and typography values.

**Limitation:** Tokens do not describe every runtime node, resolved style after cascading, geometry, layout, clipping, stacking, or dynamic state. A token may contribute to a rendered property, but it is not the rendered property itself.

**Treatment:** Optional mapping for token provenance and design-system context. A UI capture must preserve actual resolved values even when it can identify the token that contributed to them.

### 4.15 HTTP Semantics — RFC 9110

**Status:** RFC 9110, June 2022, IETF Internet Standards Track.

**Contribution:** Defines shared HTTP semantics, including methods, status codes, fields, representations, and protocol concepts.

**Limitation:** Defines protocol semantics, not application business rules or non-HTTP communication.

**Treatment:** Reuse protocol vocabulary directly in the HTTP/API facet. Preserve observed request/response facts and keep application-level interpretation separate.

## 5. Cross-cutting findings

### 5.1 Platform adapters are necessary

Different platforms expose different runtime surfaces:
- Web: DOM, CSSOM, browser automation, accessibility semantics.
- Native Android: UI object hierarchy, properties, bounds, drawing order.
- APIs: protocol messages and contracts.
- Distributed/event-driven systems: operation traces, events, and messages.

Software Rules should standardize the **meaning and representation of captured facts**, not require every platform to use the same inspection mechanism. Platform adapters may differ while mapping to common concepts where appropriate.

### 5.2 Runtime observation may be black-box or instrumented

A runtime fact may be established through an externally visible output, a supported runtime inspection interface, or instrumentation recording an operation while the system executes. The capture must record the observation method and limitations. Instrumentation can expose internal runtime facts but may be incomplete or alter execution. Source declarations alone remain source-derived.

### 5.3 Coverage must be explicit

A capture is not exhaustive merely because an agent visited every visible page or because a telemetry export contains no errors. Record scenarios, inputs, state preconditions, environment/configuration, available observation channels, captured dimensions, unavailable dimensions, and possible omissions due to sampling, permissions, or tooling.

### 5.4 Preserve raw evidence and normalized meaning

Canonical representation is necessary for comparison, but normalization can hide meaningful differences. Preserve raw observations and evidence references alongside normalized comparison values. Normalization must be documented, deterministic where possible, and facet-aware.

### 5.5 Declared intent and observed outcome remain separate

OpenAPI, AsyncAPI, UML, SBVR, design tokens, and Gherkin can describe intended or declared structures and rules. Runtime capture records what happened under a particular execution. Both can be useful, but their provenance must remain distinct.

### 5.6 Visual equivalence requires multiple evidence channels

DOM/UI hierarchy and accessibility semantics do not fully describe rendered appearance. Detailed UI capture may need hierarchy, resolved properties, geometry, stacking, accessibility, assets, and screenshots. Screenshot comparison alone is also insufficient because it does not explain the structure or semantics behind a pixel difference.

### 5.7 Finite captures do not prove universal equivalence

Finite observations establish agreement only under the recorded conditions. Comparison must state coverage and distinguish match, mismatch, unknown, and not-comparable results.

## 6. Revised facet taxonomy — working proposal

Research supports retaining most existing facets, clarifying overlaps, and adding two candidates. This taxonomy is **proposed, not a frozen schema**.

| Proposed facet | Scope | Relevant prior art |
|---|---|---|
| Interface | Web/native hierarchy, visual properties, geometry, stacking, accessibility, assets, UI states | DOM, CSSOM, WebDriver, WAI-ARIA, Android UI Automator, Design Tokens |
| Behaviour | Triggers, preconditions, transitions, observable outputs and side effects | Gherkin, UML state/activity/sequence, OpenTelemetry |
| Business rules | Domain constraints, decisions, calculations, policies and rule outcomes | SBVR |
| Data | Runtime data shapes, fields, types, relationships, transformations and validation outcomes | JSON Schema and API schemas |
| Persistence | Durable state, reads/writes, transactions, consistency and lifecycle observations | OpenTelemetry DB conventions and platform-specific evidence |
| API | Synchronous request/response interfaces and actual runtime exchanges | OpenAPI, HTTP Semantics |
| Messaging | Channels, messages, publishing, receiving, delivery and processing outcomes | AsyncAPI, OpenTelemetry messaging conventions |
| Identity and authentication | Identity context, authentication events and outcomes | API security descriptions; further security research required |
| Authorization and permissions | Roles, capabilities, policy decisions and access outcomes | SBVR concepts and API security descriptions |
| Security controls | Security-relevant runtime outcomes and authorized test observations | Requires focused security-standard research |
| Background processing | Jobs, schedules, retries, lifecycle and outcomes | OpenTelemetry spans/events, AsyncAPI |
| Errors and recovery | Validation failures, exposed exceptions, retries, recovery and failure outcomes | OpenTelemetry exception conventions, HTTP semantics |
| Integrations | Interactions and contracts with external systems | OpenAPI, AsyncAPI, HTTP and other protocols |
| Configuration | Runtime configuration values and changes that affect behaviour | OpenTelemetry configuration conventions and platform inspection |
| Performance and resource behaviour | Duration, throughput, latency, resource use and performance outcomes | OpenTelemetry traces and metrics |

Taxonomy notes:
- Identity/authentication and authorization/permissions are separate: establishing who is acting differs from deciding what that actor may do.
- Security controls remain a separate candidate because security is broader than identity and access control.
- Configuration and performance/resource behaviour are added because runtime conditions and measurable operational outcomes can affect behaviour and comparisons.
- Behaviour is cross-cutting, but remains useful for scenario-driven transitions and outcomes. Other facets may link to the same scenario and event sequence.
- Facets are not a description of internal software architecture. One runtime event may relate to multiple facets.
- Phase 2 and Phase 3 must test these boundaries and may merge, split, or rename facets.

## 7. What Software Rules must define itself

1. Common capture manifest and system/environment identity.
2. Scenario/condition model connecting triggers to runtime observations.
3. Distinction between expected outcomes, actual observations, declared contracts, and source-derived inferences.
4. Provenance describing observation method, adapter/tool, time, environment, and evidence source.
5. Typed facet-specific payloads for unlike runtime facts.
6. Coverage and completeness reporting.
7. Explicit unknown, unavailable, not observed, not applicable, and conflicting states.
8. Preservation of raw observations alongside normalized values.
9. Cross-facet identity and relationship handling.
10. Canonicalization and comparison rules, including justified tolerances.
11. Comparison reports bounded by captured scenarios.
12. Conformance examples showing different adapters producing comparable records.

## 8. Open questions carried forward

- What is the minimum genuinely shared information across all observations?
- Should a scenario execution be a separate entity from each observation it produces?
- How should a capture identify exact system build, configuration, platform, and runtime environment?
- Should evidence be embedded, externally referenced, hashed, or a combination?
- How should privileged runtime instrumentation be represented?
- How should nondeterminism, asynchronous timing, retries, and eventual consistency be captured?
- How should visual comparison handle fonts, device pixel ratio, rendering engines, animation, and tolerances?
- What security/privacy rules govern captured secrets, personal data, tokens, and production data?
- Which additional standards are appropriate for identity, authentication, authorization, security testing, persistence, and performance?
- How should adapters report unavailable fields without implying every platform exposes the same capabilities?

## 9. Phase 1 recommendation

Move to Phase 2 with these guardrails:

- Keep runtime-observed and source-derived information separate.
- Keep declared contracts separate from actual runtime observations.
- Retain a shared common model as a proposal; test it against unlike facets before accepting it.
- Use facet-specific payloads and platform-specific capture adapters.
- Use Gherkin-like scenario structure as a reference, not necessarily the serialization format.
- Use OpenTelemetry concepts selectively for operation/event context and cross-language semantics.
- Map OpenAPI, AsyncAPI, HTTP, and SBVR where they naturally apply.
- Use JSON Schema 2020-12 as the initial validation-dialect candidate, subject to implementation testing.
- Preserve raw evidence and report capture coverage.
- Treat the expanded facet taxonomy as proposed pending Phase 2/3 validation.

**Phase 1 exit assessment:** Candidate standards have been reviewed; their scope, status, limitations, and design implications are documented; references are collected; and the facet taxonomy has been revised as a working proposal. The project is ready to begin Phase 2. No capture schema has been frozen.
