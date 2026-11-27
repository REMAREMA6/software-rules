# Source — Apache Casbin

- **Repository:** https://github.com/apache/casbin
- **Pinned commit:** `fa4023fd7d02d9b7d023515e76b19b3be637f613`
- **Licence:** Apache-2.0 (`LICENSE` inspected at the pinned commit)
- **Module:** `github.com/casbin/casbin/v3`
- **Source stack:** Go
- **Candidate facets:** Authorization and permissions; behaviour; data; configuration
- **Selected bounded rule:** RBAC permission decision using subject, resource, action, direct policy assignments, and one user-to-role link.
- **Inspected files:** `examples/rbac_model.conf`, `examples/rbac_policy.csv`, `rbac_api_test.go`, `go.mod`, and `LICENSE`.
- **Runtime verification:** Pending. The source runtime probe must execute the pinned commit; this source record alone is not an accepted conformance result.

The model grants a request when the subject is directly named in a policy or is linked to the policy subject by the role relation, and the resource and action both match. The selected case does not cover domains, deny-override policies, ABAC, role inheritance, policy adapters, or mutation APIs.
