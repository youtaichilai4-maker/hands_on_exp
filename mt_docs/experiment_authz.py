"""Step 2 認可ロジックの実験。python3 -m mt_docs.experiment_authz で実行。"""

from mt_docs.can import can
from mt_docs.models import Membership
from mt_docs.roles import Role


def main() -> None:
    memberships = [
        Membership("user1", "orgA", Role.ADMIN),
        Membership("user2", "orgA", Role.MEMBER),
        Membership("user3", "orgB", Role.ADMIN),
    ]

    scenarios: list[tuple[str, str, str, str, bool]] = [
        ("Org A admin", "user1", "orgA", "document:read", True),
        ("Org A admin", "user1", "orgA", "document:create", True),
        ("Org A admin", "user1", "orgA", "document:delete", True),
        ("Org A member", "user2", "orgA", "document:read", True),
        ("Org A member", "user2", "orgA", "document:create", False),
        ("Org A member", "user2", "orgA", "document:delete", False),
        ("Org A member → Org B", "user2", "orgB", "document:read", False),
        ("Org B admin → Org A", "user3", "orgA", "document:read", False),
        ("unknown action", "user1", "orgA", "document:update", False),
    ]

    print("=== Can(user_id, org_id, action) ===\n")
    for label, user_id, org_id, action, expected in scenarios:
        result = can(memberships, user_id, org_id, action)
        status = "OK" if result == expected else "NG"
        print(
            f"[{status}] {label}: "
            f'Can("{user_id}", "{org_id}", "{action}") = {result} '
            f"(expected {expected})"
        )


if __name__ == "__main__":
    main()
