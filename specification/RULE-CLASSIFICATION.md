# Rule Classification

**Maturity:** Draft — Software Rules specification 0.3.0.

## 1. Evidence classes

### Runtime rule

A scoped proposition supported by one or more observations collected while the target was executing.

It must state the proposition, target/facet scope, applicability conditions, relevant trigger, claimed response/constraint/transition, supporting evidence links, and limitations. It must not claim behaviour outside examined conditions.

A runtime rule may be inferred from a set of runtime observations, but the inference must be explicit and the observations remain available.

### Source-derived rule

A proposition inferred from source artifacts where runtime observation is absent or insufficient. It is stored separately and must identify the artifact/revision/location, reasoning, assumptions, and whether reachability, deployment, or execution was independently established.

Source declarations alone do not establish runtime behaviour.

### Declared contract

An identified artifact stating intended, required, or permitted behaviour: for example an API description, schema, requirement, policy, configuration declaration, or design token set. Record issuer, artifact/version, scope, and relevant section.

A contract may agree with or conflict with runtime observations. Do not rewrite either record to conceal a mismatch.

## 2. Rule is not observation

Example:
- Scenario: submit a form with an invalid email.
- Execution: one attempt on a specified build/environment.
- Observation: validation message appears and progression is blocked.
- Evidence: DOM/accessibility snapshot, screenshot, and interaction record.
- Rule: under the specified form state and invalid-email condition, submission is blocked and a validation message is exposed.

The observation is limited to that execution. Further inputs, states, roles, and environments may qualify the rule.

## 3. Rule status

| Status | Meaning |
|---|---|
| Proposed | Candidate proposition not yet evaluated against sufficient evidence. |
| Supported | Applicable observations are consistent with it; scope remains bounded by coverage. |
| Qualified | Evidence supports it only after narrowing/refining its conditions or scope. |
| Contradicted | An applicable observation conflicts with it and no justified scope distinction resolves the conflict. |
| Unresolved | Evidence is insufficient, ambiguous, or conflicting. |
| Retired | No longer current for the identified target/version or replaced; preserve history and reason. |

Status is not a probability or numeric confidence score. Interpret it together with the evidence set and coverage. Supported does not mean universally proven.

For source-derived rules, maintain a separate verification state such as unverified, runtime-supported, runtime-contradicted, or superseded. If runtime evidence later supports the proposition, link the observations and runtime rule; do not relabel the original source evidence as runtime evidence.

## 4. Rule identity and relationships

Rule identity represents a proposition and its scope, not one observation. It should account for target/system scope, facet/subject, trigger, applicability conditions, and claimed outcome. The current draft schema constrains serialized identifiers to the documented ID pattern in `schemas/v1/records.schema.json`; semantic identity remains the proposition plus its scope, not merely the serialized ID.

Do not rely only on a hash of serialized content: wording or ordering changes should not automatically erase history. A material proposition change requires a new identity or explicit revision relationship.

The model must express:
- Rule supported/qualified/contradicted by observations.
- Rule derived from source artifacts.
- Rule declared by or aligned with a contract.
- Rule applies to a component, facet, target version, or condition.
- Rule supersedes/is superseded by another rule.
- Observation occurred during an execution and is supported by evidence.
- Observations are correlated when reliable correlation exists.

## 5. Multiple and conflicting observations

- Consistent observations broaden support only across conditions actually covered.
- One reliable counterexample may contradict a universal proposition if the rule applies to that case.
- Apparent conflicts may reflect different builds, actors, permissions, configurations, states, or timing. Record those distinctions.
- If conditions cannot be aligned or evidence cannot be resolved, retain an unresolved/conflicting status.
- Absence of an observation is not evidence that behaviour does not exist.

## 6. Expected outcomes

An expected outcome is a predeclared prediction or requirement from a test oracle, contract, or requirement. An actual outcome is established by runtime observations. Evaluation compares them.

A runtime rule must not be generated solely from an expected outcome. A failed expectation shows a mismatch; it does not prove the implementation follows the expectation.
