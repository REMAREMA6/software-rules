import json
from pathlib import Path

POLICIES = [
    ("alice", "data1", "read"),
    ("bob", "data2", "write"),
    ("data2_admin", "data2", "read"),
    ("data2_admin", "data2", "write"),
]
ROLE_LINKS = [("alice", "data2_admin")]
REQUESTS = [
    ("alice-data1-read", "alice", "data1", "read"),
    ("alice-data1-write", "alice", "data1", "write"),
    ("alice-data2-read-via-role", "alice", "data2", "read"),
    ("alice-data2-write-via-role", "alice", "data2", "write"),
    ("alice-data3-read", "alice", "data3", "read"),
    ("bob-data2-write", "bob", "data2", "write"),
    ("bob-data2-read", "bob", "data2", "read"),
    ("bob-data1-read", "bob", "data1", "read"),
    ("unknown-data1-read", "unknown", "data1", "read"),
    ("alice-data2-delete", "alice", "data2", "delete"),
]


def decide(subject, resource, action, policies=None, role_links=None,
           ignore_resource=False, ignore_action=False, ignore_roles=False,
           default_allow=False):
    policies = POLICIES if policies is None else policies
    role_links = ROLE_LINKS if role_links is None else role_links
    candidate_subjects = {subject}
    if not ignore_roles:
        candidate_subjects.update(role for user, role in role_links if user == subject)
    for policy_subject, policy_resource, policy_action in policies:
        subject_matches = policy_subject in candidate_subjects
        resource_matches = ignore_resource or resource == policy_resource
        action_matches = ignore_action or action == policy_action
        if subject_matches and resource_matches and action_matches:
            return True
    return bool(default_allow)


def capture(mutations=None):
    mutations = mutations or {}
    return {
        "implementation": "Independent Python 3.12 RBAC evaluator",
        "scenarios": [
            {
                "label": label,
                "request": {"subject": subject, "resource": resource, "action": action},
                "decision": "permit" if decide(subject, resource, action, **mutations) else "deny",
            }
            for label, subject, resource, action in REQUESTS
        ],
    }


if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))
