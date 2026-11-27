# Maintenance and Release Policy

**Policy status:** Accepted for the Software Rules 0.3.0 draft release  
**Policy version:** 0.1.0  
**Applies from:** 2026-11-27

## 1. Maintained project surfaces

The project maintains four related but separately versioned surfaces:

1. The technology-independent specification and its normative terminology, facet definitions, completeness rule, evidence model, and comparison semantics.
2. The machine-readable JSON Schema set (currently draft schema version 0.2.0 in the reserved `schemas/v1/` compatibility family).
3. The validation/conformance implementation, fixtures, independent replication cases, and evidence provenance.
4. Release documentation, decisions, known limitations, and migration guidance.

A change to one surface must be assessed for effects on the others.

## 2. Authority and change control

- `specification/` contains normative conceptual requirements. A document marked Draft is not a stable conformance target.
- `schemas/v1/` defines the current draft serialization constraints; it does not override the written completeness or evidence requirements.
- `conformance/` implements structural, cross-record, and case-specific checks. Passing automation does not establish that a declared property inventory is exhaustive.
- `TRACKER.md` is the operational progress source; `PLAN.md` is the roadmap; `research/DESIGN-DECISIONS.md` records consequential decisions; `CHANGELOG.md` records user-visible changes.
- Changes to normative meaning require a decision-log entry, examples/fixtures where applicable, and a compatibility assessment.
- Do not rewrite a published version in place. Correct it in a later version and preserve the previous release snapshot.

## 3. Contribution and review requirements

Every substantive change must:
1. Identify the affected requirements, facets, schemas, examples, and conformance checks.
2. Preserve runtime observations, source-derived inferences, and declared contracts as distinct evidence classes.
3. Preserve unknown, not observed, unavailable, not applicable, redacted, partial, and conflicting states.
4. Apply the Replication Completeness Rule to the declared replication scope; no successful comparison may conceal an unresolved required property.
5. Include a focused test or explain why an automated test is not appropriate.
6. Update relevant documentation, links, decisions, changelog, and tracker.
7. Receive review by someone other than the author for normative or schema changes before a stable release.

## 4. Issue triage

Classify reports as:
- **Specification defect:** contradiction, ambiguity, missing definition, or requirement that cannot be tested.
- **Schema/validator defect:** serialization or conformance implementation diverges from the specification.
- **Evidence defect:** provenance, reproducibility, integrity, retention, or runtime/source classification is inadequate.
- **Coverage gap:** a relevant property class or condition is not represented by current cases.
- **Enhancement:** a proposed capability that does not correct current behaviour.

A report should include the version, affected file/schema, a minimal example or scenario, expected interpretation, actual result, and evidence. Do not require or accept production secrets or unnecessary personal data in an issue.

Prioritize security/privacy and false-positive completeness/equivalence claims first, then correctness defects, interoperability, and enhancements. Record accepted normative changes in the decision log.

## 5. Security and privacy handling

Never commit credentials, live tokens, session cookies, private customer data, or unredacted production captures. Minimize collection, redact before upload, and preserve a record that redaction occurred. Security-sensitive reports should be sent through a private maintainer-approved channel rather than a public issue. Do not publish exploit details that would create an avoidable risk before a fix is available.

## 6. Versioning and release process

- Overall specification version and schema version are independent.
- The 0.x line is pre-stable; compatibility is not guaranteed unless a release explicitly says otherwise.
- A release candidate must pass schema fixtures, cross-record integrity tests, applicable independent case tests, documentation/link review, and the Replication Completeness Rule review.
- Release notes must identify the specification version, schema version, maturity, compatibility statement, known limitations, and evidence/validation commit.
- Stable 1.0.0 requires closure of all release-blocking normative contradictions, a reviewed schema compatibility policy, an independent implementation review, and maintainer approval. It must not be inferred from a green CI run alone.
- After publication, fixes are made in a later version; prior release material remains available.

## 7. Evidence retention

GitHub Actions artifacts currently use finite retention (commonly 30 days in the Phase 6 workflows). A workflow link is not a permanent archive. Before relying on an artifact for a long-lived release, preserve the required evidence in a durable, access-controlled location and record its digest, provenance, and retention policy. Reproducible source probes and workflows should remain committed. Never imply that an expired artifact remains retrievable.

## 8. Maintenance cadence and ownership

Review open specification issues and known limitations at each substantive release and at least once per quarter while the project is active. Review dependency versions and workflow actions before changing them. The repository maintainer is responsible for approving releases, deciding whether a report changes normative meaning, and ensuring that the tracker and changelog match the repository state.
