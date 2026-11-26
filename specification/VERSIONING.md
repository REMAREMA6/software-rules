# Specification Maturity and Versioning

**Status:** Accepted project-governance policy  
**Policy version:** 0.1.0  
**Last updated:** 2026-11-26

This document defines how the maturity and versions of Software Rules documents and machine-readable formats are identified. It does not define the eventual runtime capture schema.

## 1. Maturity labels

Every substantial specification document and schema must state its maturity.

| Label | Meaning | Normative use |
|---|---|---|
| **Exploratory** | Research notes, candidate ideas, or incomplete investigations. | Not normative; do not implement as a requirement. |
| **Draft** | A proposed design with known gaps or unresolved questions. | Provisional; implementations may change. |
| **In Review** | A draft undergoing structured review against requirements, examples, and other facets. | Not final; review feedback may change it. |
| **Stable** | Reviewed and approved for the identified specification version. | Normative for that version. |
| **Deprecated** | Previously supported material retained for migration guidance. | Avoid for new implementations; follow stated replacement guidance. |
| **Retired** | No longer maintained or part of the current specification. | Informational only; retained for historical reference where useful. |

A document's maturity is independent of its version number. A document can have a version and still be Draft.

## 2. Versioning model

Software Rules uses separate version identifiers for:
- The overall specification release.
- Machine-readable schema releases.
- Individual facet specifications when independently versioned.

Do not assume these versions are identical. A capture manifest must eventually identify the exact specification and schema versions used.

### 2.1 Version format

Use MAJOR.MINOR.PATCH numeric versions.

- **MAJOR** — incompatible changes to normative meaning, required structure, or interpretation.
- **MINOR** — backward-compatible additions or clarifications that do not invalidate conforming existing captures.
- **PATCH** — backward-compatible corrections, editorial fixes, or tightened explanations that do not change intended meaning.

Before the first stable 1.0.0 release, use 0.y.z:
- 0.y.0 may introduce or change draft design in ways that are not yet stable.
- 0.y.z may correct or clarify the current draft without claiming stability.

A 0.x format is not promised to be backward compatible unless a specific document explicitly says otherwise.

### 2.2 Compatibility

Every released version must document:
- Which schema versions it uses.
- Whether older captures remain valid.
- Whether a migration is required.
- Whether a change affects parsing, validation, interpretation, or comparison.
- Any known lossy conversions.

Do not silently reinterpret an older capture under new semantics. Preserve its declared version and use an explicit migration or compatibility rule.

### 2.3 Schema identifiers

Schema files must carry an explicit schema identifier and version. Use versioned directories such as schemas/v1/ for a stable major schema line. Draft schema work must be clearly labelled and must not be mistaken for a released stable schema.

The draft schema identifier namespace is `urn:software-rules:schema:v1:`. These URNs are identifiers, not retrieval URLs. The `schemas/v1/` directory reserves the intended major compatibility family; the current pre-release schema version is `0.1.0`. The release publication mechanism remains undecided.

## 3. Normative language

When a specification uses the terms MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, or MAY, interpret them in their ordinary standards-writing sense:

- MUST / MUST NOT: absolute requirement or prohibition for conformance.
- SHOULD / SHOULD NOT: recommended; departures require a documented reason.
- MAY: optional.

Use normative terms only when the requirement is sufficiently defined and testable. Draft documents must identify unresolved normative proposals.

## 4. Change control

- Record consequential design choices in [DESIGN-DECISIONS.md](../research/DESIGN-DECISIONS.md).
- Record meaningful specification, schema, example, and structure changes in [CHANGELOG.md](../CHANGELOG.md).
- Track work and review status in [TRACKER.md](../TRACKER.md).
- Do not edit a released version in place. Make corrections in a later version and preserve the historical release.
- A change that affects compatibility must state its migration impact.

## 5. Current project status

The project has a draft machine-readable schema set at version `0.1.0` in the intended v1 compatibility family. It is not a stable 1.0.0 release and carries no backward-compatibility guarantee. Validation fixtures and instructions exist; the validation run and cross-record conformance checks remain to be completed.
