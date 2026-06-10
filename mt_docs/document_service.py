from mt_docs.can import can
from mt_docs.models import Document, Membership
from mt_docs.roles import Action


class AuthorizationError(Exception):
    pass


class DocumentNotFoundError(Exception):
    pass


class DocumentService:
    def __init__(
        self,
        memberships: list[Membership],
        documents: list[Document] | None = None,
    ):
        self._memberships = memberships
        self._documents: list[Document] = documents if documents is not None else []
        self._next_id = len(self._documents) + 1

    def _require(self, user_id: str, org_id: str, action: Action) -> None:
        if not can(self._memberships, user_id, org_id, action):
            raise AuthorizationError(
                f"denied: user={user_id} org={org_id} action={action.value}"
            )

    def list_documents(self, user_id: str, org_id: str) -> list[Document]:
        self._require(user_id, org_id, Action.DOCUMENT_READ)
        return [d for d in self._documents if d.org_id == org_id]

    def create_document(
        self, user_id: str, org_id: str, title: str, body: str
    ) -> Document:
        self._require(user_id, org_id, Action.DOCUMENT_CREATE)
        doc = Document(
            id=f"doc-{self._next_id}",
            org_id=org_id,
            title=title,
            body=body,
            created_by=user_id,
        )
        self._next_id += 1
        self._documents.append(doc)
        return doc

    def delete_document(self, user_id: str, org_id: str, document_id: str) -> None:
        self._require(user_id, org_id, Action.DOCUMENT_DELETE)
        doc = next((d for d in self._documents if d.id == document_id), None)
        if doc is None or doc.org_id != org_id:
            raise DocumentNotFoundError(f"document not found: {document_id}")
        self._documents.remove(doc)
