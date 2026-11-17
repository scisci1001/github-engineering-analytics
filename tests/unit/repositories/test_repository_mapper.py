from datetime import datetime, timezone

from bson import ObjectId

from github_analytics.domain.repository import GitHubRepository
from github_analytics.infrastructure.mongodb.repository_mapper import (
    parse_object_id,
    repository_from_document,
    repository_to_document,
)


def test_repository_to_document_excludes_internal_id_and_audit_fields() -> None:
    repository = GitHubRepository(
        id="ignored",
        github_id=123,
        owner="octocat",
        name="hello-world",
        full_name="octocat/hello-world",
        default_branch="main",
        html_url="https://github.com/octocat/hello-world",
    )

    document = repository_to_document(repository)

    assert document == {
        "github_id": 123,
        "owner": "octocat",
        "name": "hello-world",
        "full_name": "octocat/hello-world",
        "default_branch": "main",
        "html_url": "https://github.com/octocat/hello-world",
        "github_created_at": None,
        "github_updated_at": None,
    }


def test_repository_from_document_maps_object_id_to_string() -> None:
    object_id = ObjectId()
    now = datetime.now(timezone.utc)

    repository = repository_from_document(
        {
            "_id": object_id,
            "github_id": 123,
            "owner": "octocat",
            "name": "hello-world",
            "full_name": "octocat/hello-world",
            "default_branch": "main",
            "html_url": "https://github.com/octocat/hello-world",
            "created_at": now,
            "updated_at": now,
        }
    )

    assert repository.id == str(object_id)
    assert repository.github_id == 123
    assert repository.created_at == now
    assert repository.updated_at == now


def test_parse_object_id_returns_none_for_invalid_id() -> None:
    assert parse_object_id("not-an-object-id") is None
