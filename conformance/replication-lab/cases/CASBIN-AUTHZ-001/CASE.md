# Case — Casbin RBAC authorization decisions

**Case ID:** CASBIN-AUTHZ-001  
**Status:** Source and independent replica probes prepared; pinned-source runtime, Software Rules capture validation, and CI pending  
**Facet(s):** Authorization and permissions; behaviour; data  
**Source:** https://github.com/apache/casbin  
**Source commit:** `fa4023fd7d02d9b7d023515e76b19b3be637f613`  
**Source module:** `github.com/casbin/casbin/v3`  
**Source stack:** Go  
**Replica stack:** Python 3.12 standard library  
**Licence:** Apache-2.0

## Declared scope

Evaluate ten requests against the pinned Casbin RBAC model and policy:
- direct subject-to-permission grant;
- direct subject with wrong action;
- role-derived resource read and write;
- role-derived request for an unlisted resource;
- direct policy grant for another subject;
- wrong resource/action combinations;
- unknown subject;
- unsupported action.

The same request tuples are sent to the pinned Casbin runtime and the independent Python model.

## Technology-independent rules

1. A request is permitted only when a policy subject matches the requesting subject directly or through the configured user-to-role relation.
2. The policy resource must equal the requested resource.
3. The policy action must equal the requested action.
4. If no policy row satisfies all three conditions, the request is denied.
5. A user-to-role link grants only the permissions assigned to that role; it does not grant all resources or actions.

## Source evidence

- `examples/rbac_model.conf`: request tuple, policy tuple, role relation, allow effect, and matcher.
- `examples/rbac_policy.csv`: direct grants, role grants, and the Alice-to-data2_admin relation.
- `rbac_api_test.go`: upstream direct and role-derived enforcement examples.
- `go.mod` and `LICENSE`: module identity and Apache-2.0 licence.

## Independent replica

The Python implementation evaluates the same fixed policy rows and role link without importing Casbin or translating its source code. It implements only the declared simple RBAC matcher.

## Mutation tests

Executable mutations remove the role relation, ignore resource equality, ignore action equality, and default-deny incorrectly changed to default-allow. Each must be detected against the source decisions.

## Acceptance gate

Accept only after the pinned Go source and Python replica match all ten decisions, all executable mutations are detected, and Software Rules 0.2.0 source/replica captures and comparison report pass schema and cross-record evidence validation. This case does not establish full authorization-facet completeness.
