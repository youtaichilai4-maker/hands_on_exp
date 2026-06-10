"""Step 3 DocumentService の実験。python3 -m mt_docs.experiment_documents で実行。"""

from mt_docs.document_service import (
    AuthorizationError,
    DocumentNotFoundError,
    DocumentService,
)
from mt_docs.models import Document, Membership
from mt_docs.roles import Role


def run_scenario(label: str, fn) -> None:
    try:
        fn()
        print(f"[OK] {label}")
    except (AuthorizationError, DocumentNotFoundError, AssertionError) as exc:
        print(f"[NG] {label}: {exc}")


def main() -> None:
    memberships = [
        Membership("user1", "orgA", Role.ADMIN),
        Membership("user2", "orgA", Role.MEMBER),
        Membership("user3", "orgB", Role.ADMIN),
    ]
    documents: list[Document] = []
    svc = DocumentService(memberships, documents)

    print("=== DocumentService ===\n")

    run_scenario(
        "Org A admin creates document",
        lambda: svc.create_document("user1", "orgA", "議事録", "body A"),
    )

    run_scenario(
        "Org B admin creates document",
        lambda: svc.create_document("user3", "orgB", "設計書", "body B"),
    )

    run_scenario(
        "Org A member cannot create",
        lambda: _expect_authz_error(
            lambda: svc.create_document("user2", "orgA", "x", "y")
        ),
    )

    run_scenario(
        "Org A member sees only Org A documents",
        lambda: _assert_count(svc.list_documents("user2", "orgA"), 1),
    )

    run_scenario(
        "Org A member cannot list Org B",
        lambda: _expect_authz_error(lambda: svc.list_documents("user2", "orgB")),
    )

    run_scenario(
        "Org B admin does not see Org A documents",
        lambda: _assert_count(svc.list_documents("user3", "orgB"), 1),
    )

    run_scenario(
        "Org A member cannot delete",
        lambda: _expect_authz_error(
            lambda: svc.delete_document("user2", "orgA", "doc-1")
        ),
    )

    run_scenario(
        "Org A admin deletes Org A document",
        lambda: svc.delete_document("user1", "orgA", "doc-1"),
    )

    run_scenario(
        "Org B admin cannot delete Org A document (not found)",
        lambda: _expect_not_found(
            lambda: svc.delete_document("user3", "orgB", "doc-1")
        ),
    )


def _expect_authz_error(fn) -> None:
    try:
        fn()
        raise AssertionError("expected AuthorizationError")
    except AuthorizationError:
        pass


def _expect_not_found(fn) -> None:
    try:
        fn()
        raise AssertionError("expected DocumentNotFoundError")
    except DocumentNotFoundError:
        pass


def _assert_count(docs: list[Document], expected: int) -> None:
    assert len(docs) == expected, f"expected {expected} docs, got {len(docs)}"


if __name__ == "__main__":
    main()
