# Source-Derived Rules

**Maturity:** Draft — Software Rules specification 0.3.0.

## 1. Purpose

Source-derived rules preserve useful findings from source code and other static artifacts when runtime observation cannot establish the relevant fact. They are a fallback evidence class, not a way to label unexecuted declarations as runtime behaviour.

## 2. What qualifies

A source-derived rule is a proposition inferred from source artifacts such as application code, static configuration/deployment manifests, build scripts, feature-flag declarations, migrations/schema declarations, API descriptions, or policy files.

A document that merely states intended behaviour should normally be recorded as a declared contract, not automatically converted into a source-derived rule.

## 3. Required distinction

| Record class | What it establishes |
|---|---|
| Runtime observation | A fact detected while the target executed under recorded conditions. |
| Source-derived inference | A reasoned proposition based on a source artifact; runtime effect is unverified. |
| Declared contract | What an identified artifact says is intended, required, or permitted. |

They may be linked, but their evidence classes must not be merged.

## 4. Minimum record content

A source-derived rule should identify:
- Stable rule ID and proposition.
- Facet and target scope.
- Source artifact type, origin, revision, and immutable identity where possible.
- File/document location, symbol, section, or line range.
- Retrieval time and method.
- Relevant excerpt, digest, or durable reference where permitted.
- Reasoning connecting artifact to proposition.
- Assumptions and unresolved dependencies.
- Whether code path reachability, configuration, build inclusion, deployment, or execution was established; use unknown otherwise.
- Verification state and linked runtime observations/contracts, if any.

## 5. Source does not prove execution

The existence of a function, route, branch, schema, configuration key, or policy does not prove it is included in the deployed build, reachable, enabled, invoked, unoverridden, or effective in the target environment. A source-derived rule must disclose these uncertainties.

## 6. Verification lifecycle

If runtime evidence later supports the proposition, link the observations and corresponding runtime rule while preserving the source-derived record as historical provenance. If runtime evidence contradicts it, preserve the contradiction and update verification state. If the path cannot be inspected, retain source-derived status and document the gap. Source revisions must be tracked.

Do not silently convert the original source-derived record into a runtime rule. Runtime support requires runtime evidence and a traceable relationship.

## 7. Comparison

Source-derived rules may guide scenario selection. They must not count as runtime matches between implementations. A comparison may display them separately as unverified context, never mixed into runtime equivalence results.
