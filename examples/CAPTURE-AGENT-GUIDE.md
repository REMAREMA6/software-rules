# Capture-agent guidance

**Status:** Draft — Phase 6

A capture agent records observations; it must not convert guesses, source declarations, or missing evidence into runtime facts.

## Procedure

1. **Declare the boundary.** Identify the target, build/revision where known, included and excluded components, platform, OS, runtime, browser/device, viewport, locale, configuration, and actor state. Mark unavailable context explicitly.
2. **Define scenarios before execution.** Give each scenario a stable capture-local ID, purpose, facets, subject, preconditions, initial state, trigger, ordered actions, expected outcomes and stopping criteria. Do not write expected outcomes as observed results.
3. **Execute against the running target.** Record actual start/end times, target, scenario, actual inputs/context, actions, deviations, status, collector and tool versions.
4. **Collect observations per facet.** Each observation records target, execution or runtime interval, facet, subject, time/order, method class and procedure, conditions, trigger, typed payload, evidence references, status and limitations.
5. **Retain evidence.** Prefer structured platform output plus screenshots/video where useful. Record capture tool/version, source, timestamp, media type, digest, retention and redactions. A screenshot alone does not establish hierarchy, computed values or accessibility semantics.
6. **Keep evidence classes separate.** Runtime observations require runtime evidence. Source-derived rules use source-artifact evidence and an explicit unverified verification state unless independently confirmed at runtime. Declared contracts remain separate records.
7. **Record coverage honestly.** Include dimensions attempted but not observed, unavailable, partial or not applicable. Do not silently omit failed inspection attempts.
8. **Validate.** Run JSON Schema validation, then cross-record integrity validation. Resolve broken references and schema errors without inventing data.
9. **Compare only after capture.** Align scenarios/conditions and records using evidence. Preserve raw observations; apply named, versioned normalization; classify unknown or ambiguous results conservatively.
10. **Conclude within scope.** Report exactly which scenarios, conditions, facets and dimensions were covered. Never claim universal equivalence from finite captures.

## Minimum capture review

- Can every observation be traced to a target, scenario execution, method and evidence item?
- Are actual conditions materially equivalent between reference and implementation?
- Are raw values preserved alongside any normalized values?
- Are hidden/unavailable/not-observed states distinguished?
- Are source-derived rules clearly separate from runtime observations?
- Are screenshot and structured evidence linked to the same execution and time window?
- Are exclusions and limitations explicit?

This guide is procedural. It does not certify collector trustworthiness or evidence authenticity.

## Executed Phase 6 example

The Task Board conformance target in `examples/task-board/` demonstrates this procedure end to end:

- Capture the reference and independent baseline with the same 1280×800 viewport and scenario inputs.
- Retain interface geometry, behavior outputs, and instrumented adapter request/response events as runtime evidence.
- Keep the source-derived DELETE-call inference in the separate `sourceRules` collection with `verificationState: "unverified"`.
- Run the deliberately mutated build separately and compare its actual singular-count output against the reference.
- Validate every capture fixture with the capture schema and cross-record integrity validator; validate both comparison reports with the comparison schema.

The adapter is deliberately in-memory. Mark its boundary and do not generalize these API observations to a production server or durable persistence.
