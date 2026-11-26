# Terminology

**Status:** Draft — Phase 2 conceptual model.

This vocabulary applies across Software Rules. Facet documents may define narrower terms but must not silently redefine these core meanings.

## System and scope

| Term | Definition |
|---|---|
| Software system | The product or bounded collection of cooperating software elements being captured. |
| System boundary | The declared separation between the target and external actors, services, platforms, or dependencies. |
| Component | An identifiable part of the target, whether logical or physical. It need not correspond to a code module or deployment unit. |
| Facet | A perspective used to organize rules and observations, such as interface, API, persistence, or background processing. A facet is not necessarily a component. |
| Capture | A bounded collection of target identity, scope, scenarios, executions, observations, rules, evidence references, and coverage. |
| Capture target | The particular system instance, build/revision, and environment examined. |

## Rules and claims

| Term | Definition |
|---|---|
| Rule | A normalized, scoped claim describing a relationship between conditions or triggers and an observable response, constraint, state transition, or other outcome. A rule is a claim, not raw evidence. |
| Runtime rule | A rule supported by observations collected while the target was executing. |
| Source-derived rule | A rule inferred from source artifacts without sufficient runtime evidence to establish it. It remains separate from runtime rules. |
| Declared contract | An explicit specification, schema, configuration declaration, policy, or design statement describing intended or permitted behaviour. It does not prove that a running implementation follows it. |
| Rule proposition | The precise assertion made by a rule, including scope, applicability conditions, and claimed outcome. |
| Rule support | Evidence consistent with a rule proposition under the conditions actually observed. |
| Rule contradiction | Evidence conflicting with a rule proposition under conditions where it applies. |
| Rule qualification | A refinement or limitation to a rule's scope established by evidence. |

A rule may be supported by multiple observations, and an observation may support multiple rules. A rule may remain proposed, qualified, contradicted, or unresolved.

## Scenario and execution

| Term | Definition |
|---|---|
| Scenario | A reusable description of a situation to examine: purpose, starting conditions, actions/stimuli, inputs, and observable questions. |
| Scenario execution | One actual attempt to perform a scenario against a particular capture target. Each attempt has its own identity, context, timing, and status. |
| Precondition | A condition required or established before a trigger/action. |
| Trigger | The event or stimulus initiating the behaviour, such as a user action, request, message, timer, or external event. |
| Action | An intentional operation performed by an actor or test driver. |
| Input | Data or a value supplied to the system or action. |
| Execution context | Circumstances relevant to interpreting an execution, including environment, actor/permissions where relevant, configuration, initial state, time, and dependencies. |
| Expected outcome | A prediction or requirement declared before or independently of an execution, with its source identified. |
| Actual outcome | The result established by observations of an execution. It must not be populated from expectation alone. |

A scenario describes what should be attempted. An execution records what was attempted. Observations record what was detected during or as a result.

## Observation and outcome

| Term | Definition |
|---|---|
| Observation | A bounded record of a fact detected about the target during a specific execution or explicitly identified runtime interval, using a stated method and evidence. |
| Observation subject | The system, component, facet, resource, interaction, or state to which an observation refers. |
| Observed value | The value/structure directly recorded before optional normalization. |
| Normalized value | A derived representation produced by a documented procedure for interpretation/comparison; it links to the raw observation. |
| Outcome | A facet-specific result, such as returned output, visible state, state transition, emitted event, side effect, error, or measurement. |
| State snapshot | Relevant state represented at a particular point in time. |
| State change | A difference between identified states, with ordering and observation limits recorded where available. |
| Side effect | An observable consequence beyond the immediate output, such as a persisted write, emitted message, external call, or scheduled job. |
| Observation method | External black-box observation, platform/runtime inspection, or runtime instrumentation. |
| Observation time | The time/interval to which the fact applies, distinct from record storage time. |

An observation is not automatically a rule. It is evidence from a particular execution.

## Evidence and provenance

| Term | Definition |
|---|---|
| Evidence | A retained artifact/record supporting inspection of an observation or claim: response, event, trace, DOM snapshot, accessibility tree, screenshot, state diff, log, or measurement. |
| Provenance | Where a record came from, how it was produced, by whom/what, and how it relates to source artifacts or earlier records. |
| Capture method | The concrete tool, protocol, instrumentation, or procedure used to obtain evidence. |
| Evidence reference | A stable reference to evidence, including type, location/embedded content, integrity metadata where available, and access constraints. |
| Source artifact | Source code, configuration, contract, schema, documentation, or other non-runtime artifact used for inference or interpretation. |
| Runtime evidence | Evidence produced by observing an executing target and linked to that execution. |
| Source evidence | Evidence obtained from a source artifact; it does not become runtime evidence because referenced code is intended to execute. |

## Coverage and uncertainty

| Term | Definition |
|---|---|
| Coverage | Which declared scope, facets, scenarios, conditions, and observable dimensions were examined and to what extent. |
| Capture completeness | Degree to which the declared capture scope was successfully examined and recorded; not a statement that the software itself is complete. |
| Not observed | The capture did not record the fact. This does not establish whether it occurred or exists. |
| Unknown | Available information is insufficient to determine the value/state. |
| Unavailable | The fact could not be obtained with available access, method, or environment. |
| Not applicable | The dimension does not apply to the explicitly stated subject/scope. |
| Conflicting | Relevant records disagree and the conflict is unresolved. |
| Inferred | A conclusion derived from other information rather than directly observed. |
| Verification state | A label describing evidential status, distinct from a numeric confidence score. |

These states are not interchangeable. In particular, not observed, unknown, unavailable, and not applicable must remain distinguishable.

## Comparison

| Term | Definition |
|---|---|
| Comparison scope | Aligned captures, facets, scenarios, conditions, and observable dimensions included in a comparison. |
| Canonicalization | A documented transformation into a stable representation for comparison. |
| Equivalence claim | A statement that captures agree within a stated scope/tolerance; it does not imply universal equivalence. |
| Difference | A disagreement, omission, addition, conflict, or inability to compare aligned records. |
| Conformance | Satisfaction of explicit specification requirements under a defined procedure. |

## Usage rules

1. Use scenario for the reusable description and scenario execution for one actual attempt.
2. Use observation for a detected fact and rule for a scoped claim supported or challenged by observations.
3. Use actual outcome only for what evidence establishes.
4. Use runtime only when the target was executing and evidence is linked to that execution.
5. Use source-derived for inferences based on source artifacts without sufficient runtime evidence.
6. Use declared contract for intended/specified behaviour, not actual implementation behaviour.
7. Never infer completeness or absence from missing observations.
