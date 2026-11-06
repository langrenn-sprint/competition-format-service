"""The role model for competition-format-service, shared by the integration and contract tests.

See langrenn-sprint/event-service-gui#215. All GET operations are open. Only
admin may change competition formats.
"""

ADMIN = "admin"
EVENT_ADMIN = "event-admin"
RESULT_ADMIN = "result-admin"
CONTESTANT_ADMIN = "contestant-admin"

ROLES = [ADMIN, EVENT_ADMIN, RESULT_ADMIN, CONTESTANT_ADMIN]
# Roles that no longer exist, or never did, and must not give access:
REMOVED_ROLES = ["user-admin", "race-result", "race-office", "user"]

ADMIN_ONLY = {ADMIN}

WRITE_ACCESS: dict[tuple[str, str], set[str]] = {
    ("POST", "/competition-formats"): ADMIN_ONLY,
    ("PUT", "/competition-formats/{competition_format_id}"): ADMIN_ONLY,
    ("DELETE", "/competition-formats/{competition_format_id}"): ADMIN_ONLY,
}


def access_cases(roles: list[str]) -> list[tuple[str, str, str, bool]]:
    """Return (method, path, role, allowed) for every write operation and role."""
    return [
        (method, path, role, role in allowed)
        for (method, path), allowed in WRITE_ACCESS.items()
        for role in roles
    ]
