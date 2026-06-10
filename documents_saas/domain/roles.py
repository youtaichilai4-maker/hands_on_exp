from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"


class Action(str, Enum):
    DOCUMENT_READ = "document:read"
    DOCUMENT_CREATE = "document:create"
    DOCUMENT_DELETE = "document:delete"


ROLE_PERMISSIONS: dict[Role, frozenset[Action]] = {
    Role.ADMIN: frozenset(
        {
            Action.DOCUMENT_READ,
            Action.DOCUMENT_CREATE,
            Action.DOCUMENT_DELETE,
        }
    ),
    Role.MEMBER: frozenset({Action.DOCUMENT_READ}),
}
