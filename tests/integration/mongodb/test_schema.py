import pytest
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError, WriteError

from github_analytics.infrastructure.mongodb.schema import initialize_database

EXPECTED_COLLECTIONS = {
    "repositories",
    "pull_requests",
    "issues",
    "sync_states",
}


async def test_initialize_database_creates_expected_collections(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)

    collections = set(await mongo_database.list_collection_names())

    assert collections == EXPECTED_COLLECTIONS


async def test_initialize_database_creates_expected_indexes(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)

    repository_indexes = await mongo_database["repositories"].index_information()
    pull_request_indexes = await mongo_database["pull_requests"].index_information()
    issue_indexes = await mongo_database["issues"].index_information()
    sync_state_indexes = await mongo_database["sync_states"].index_information()

    assert "ux_repositories_github_id" in repository_indexes
    assert "ux_repositories_full_name" in repository_indexes

    assert "ux_pull_requests_repository_number" in pull_request_indexes
    assert "ix_pull_requests_repository_created_at" in pull_request_indexes
    assert "ix_pull_requests_repository_merged_at" in pull_request_indexes
    assert "ix_pull_requests_repository_author" in pull_request_indexes

    assert "ux_issues_repository_number" in issue_indexes
    assert "ix_issues_repository_created_at" in issue_indexes
    assert "ix_issues_repository_closed_at" in issue_indexes
    assert "ix_issues_repository_author" in issue_indexes

    assert "ux_sync_states_repository_resource" in sync_state_indexes


async def test_repository_github_id_is_unique(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)

    repositories = mongo_database["repositories"]

    await repositories.insert_one(
        {
            "github_id": 123,
            "owner": "example",
            "name": "repo-one",
            "full_name": "example/repo-one",
            "default_branch": "main",
            "html_url": "https://github.com/example/repo-one",
        }
    )

    with pytest.raises(DuplicateKeyError):
        await repositories.insert_one(
            {
                "github_id": 123,
                "owner": "example",
                "name": "repo-two",
                "full_name": "example/repo-two",
                "default_branch": "main",
                "html_url": "https://github.com/example/repo-two",
            }
        )


async def test_schema_validation_rejects_invalid_repository(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)

    with pytest.raises(WriteError):
        await mongo_database["repositories"].insert_one(
            {
                "github_id": 999,
                # Missing owner, name, full_name, default_branch and html_url.
            }
        )


async def test_initialize_database_is_idempotent(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)
    await initialize_database(mongo_database)

    collections = set(await mongo_database.list_collection_names())

    assert collections == EXPECTED_COLLECTIONS
