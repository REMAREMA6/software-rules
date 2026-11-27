# Contributing to Software Rules

This document defines the working process for changing the repository. It is supplemented by [MAINTENANCE.md](MAINTENANCE.md), which defines issue triage, security/privacy handling, evidence retention, versioning, and release operations.

## 1. Before making a change

1. Read `README.md`, `PLAN.md`, and `TRACKER.md`.
2. Read the active task's relevant specification, research, and decision documents.
3. Check whether the question is already covered by an accepted decision or an existing standard.
4. Keep work within the active phase unless a dependency requires an explicit plan change.
5. Do not create a normative format rule from an unverified assumption. Mark proposals and unresolved questions clearly.

## 2. Making changes

- Prefer focused changes that solve one documented task.
- Preserve the distinction between runtime-observed evidence and source-derived inference.
- Keep shared concepts in the core specification and facet-specific details in their facet documents.
- Include sources for external factual claims and distinguish a standard's requirements from this project's interpretation of them.
- Add or update examples when a format rule changes.
- Do not create placeholder files or empty directories merely to imitate the target tree; add files when they have defined content and purpose.

## 3. Recording decisions and changes

- Update `research/DESIGN-DECISIONS.md` for consequential choices, using the next permanent decision ID.
- Update `CHANGELOG.md` for meaningful changes to specification meaning, schemas, examples, compatibility, or repository structure.
- Update `TRACKER.md` when work starts, changes status, becomes blocked, or is completed.
- Update `PLAN.md` only when the agreed scope, sequence, deliverables, or target structure changes.
- Update `README.md` when navigation or the project's public-facing summary changes.

## 4. Review checklist

Before treating a task as complete, check:

- Does the change satisfy the task and its phase exit criteria?
- Are terms used consistently with the current terminology and cited standards?
- Are observed facts, source-derived inferences, assumptions, and proposals distinguishable?
- Are limitations and unresolved questions explicit?
- Are links and repository paths correct?
- Do examples and schemas agree with the written specification, where applicable?
- Have the plan, tracker, decision log, and changelog been updated where required?

## 5. Handoffs between chats or contributors

The repository is the persistent project record. A handoff must leave `TRACKER.md` with the current phase, active task, completed work, blockers, and one clear next action. A new contributor should be able to resume by reading the README, plan, tracker, and files named by the active task without depending on private chat history.

## 6. Maturity and authority

Use the labels and versioning rules in `specification/VERSIONING.md`. A proposed or draft design is not a stable requirement. When documents conflict, record the conflict, inspect the relevant decision history, and resolve it explicitly rather than silently choosing one interpretation.
