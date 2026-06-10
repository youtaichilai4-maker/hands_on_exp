from documents_saas.domain.models import Membership
from documents_saas.domain.roles import ROLE_PERMISSIONS, Action


def can(
    memberships: list[Membership],
    user_id: str,
    org_id: str,
    action: Action | str,
) -> bool:
    if isinstance(action, str):
        try:
            action = Action(action)
        except ValueError:
            return False

    membership = next(
        (m for m in memberships if m.user_id == user_id and m.org_id == org_id),
        None,
    )
    if membership is None:
        return False

    return action in ROLE_PERMISSIONS.get(membership.role, frozenset())
