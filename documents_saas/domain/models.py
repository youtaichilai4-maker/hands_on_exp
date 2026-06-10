from dataclasses import dataclass

from documents_saas.domain.roles import Role


@dataclass(frozen=True)
class User:
    id: str
    email: str
    name: str


@dataclass(frozen=True)
class Organization:
    id: str
    name: str


@dataclass(frozen=True)
class Membership:
    user_id: str
    org_id: str
    role: Role


@dataclass(frozen=True)
class Document:
    id: str
    org_id: str
    title: str
    body: str
    created_by: str
