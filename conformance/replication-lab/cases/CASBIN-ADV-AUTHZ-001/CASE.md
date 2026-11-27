# Case — Casbin domain RBAC, ABAC, deny override, and policy mutation

**Case ID:** CASBIN-ADV-AUTHZ-001  
**Status:** PASSED for all 19 declared requests in [run #45938792630](https://github.com/REMAREMA6/software-rules/actions/runs/45938792630). Pinned Casbin and independent Python decisions matched; domain-isolation, ABAC-owner, deny-override, and policy-mutation changes were all detected; Software Rules 0.2.0 captures/comparison passed schema and cross-record integrity validation. Artifact `15172101161` retained through 2026-12-27. This expands selected authorization classes but does not complete the authorization facet.  
**Facet(s):** Authorization and permissions; behaviour; data; security controls  
**Source:** https://github.com/apache/casbin  
**Immutable source commit:** `fa4023fd7d02d9b7d023515e76b19b3be637f613`  
**Source version:** Casbin v3.11.0  
**Source stack:** Go  
**Replica stack:** Python 3.12  
**Licence:** Apache-2.0

## Declared scope

This case expands beyond the simple RBAC case by executing pinned Casbin examples for domain-scoped RBAC, ABAC resource ownership, and deny-override policy effects. It also mutates the domain policy at runtime and checks that decisions change and revert.

## Rules under test

1. A role assignment is scoped to its domain; membership in one tenant does not grant the same role in another tenant.
2. ABAC compares subject and resource attributes as declared by the model. The selected Casbin example's matcher checks owner equality and does not inspect the action field.
3. Under deny-override effect, a matching deny policy overrides a matching allow policy, including an allow inherited through a role.
4. Adding a matching policy changes a denied request to permit; removing that policy restores deny.
5. Requests without a matching allow remain denied.

## Probes

Seven domain-RBAC requests, five ABAC requests, five deny-override requests, and two policy-mutation observations are compared. The source probe uses the exact model and policy files from the pinned Casbin repository. The Python replica independently implements the declared model semantics.

## Mutation tests

The suite mutates domain isolation, owner matching, deny-overrides-allow, and policy mutation propagation. Every mutation must be detected.

## Acceptance gate

Accept only after all 19 source/replica decisions match, all four mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and cross-record evidence validation. This remains bounded authorization evidence, not full Casbin or full authorization-facet coverage.
