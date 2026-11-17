from pymongo.asynchronous.database import AsyncDatabase

from github_analytics.domain.repository import GitHubRepository
from github_analytics.infrastructure.mongodb.repository_repository import MongoRepositoryRepository
from github_analytics.infrastructure.mongodb.schema import initialize_database


async def test_upsert_inserts_repository(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)
    repository_store = MongoRepositoryRepository(mongo_database["repositories"])

    saved = await repository_store.upsert(
        GitHubRepository(
            id=None,
            github_id=1,
            owner="octocat",
            name="hello-world",
            full_name="octocat/hello-world",
            default_branch="main",
            html_url="https://github.com/octocat/hello-world",
        )
    )

    assert saved.id is not None
    assert saved.github_id == 1
    assert saved.created_at is not None
    assert saved.updated_at is not None


async def test_upsert_updates_existing_repository_without_duplicate(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)
    repository_store = MongoRepositoryRepository(mongo_database["repositories"])

    first = await repository_store.upsert(
        GitHubRepository(
            id=None,
            github_id=2,
            owner="octocat",
            name="hello-world",
            full_name="octocat/hello-world",
            default_branch="master",
            html_url="https://github.com/octocat/hello-world",
        )
    )

    second = await repository_store.upsert(
        GitHubRepository(
            id=None,
            github_id=2,
            owner="octocat",
            name="hello-world",
            full_name="octocat/hello-world",
            default_branch="main",
            html_url="https://github.com/octocat/hello-world",
        )
    )

    assert second.id == first.id
    assert second.default_branch == "main"
    assert await mongo_database["repositories"].count_documents({"github_id": 2}) == 1


async def test_find_by_full_name_returns_repository(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)
    repository_store = MongoRepositoryRepository(mongo_database["repositories"])

    saved = await repository_store.upsert(
        GitHubRepository(
            id=None,
            github_id=3,
            owner="fastapi",
            name="fastapi",
            full_name="fastapi/fastapi",
            default_branch="master",
            html_url="https://github.com/fastapi/fastapi",
        )
    )

    found = await repository_store.find_by_full_name("fastapi/fastapi")

    assert found == saved


async def test_find_by_id_returns_none_for_invalid_object_id(
    mongo_database: AsyncDatabase[dict[str, object]],
) -> None:
    await initialize_database(mongo_database)
    repository_store = MongoRepositoryRepository(mongo_database["repositories"])

    assert await repository_store.find_by_id("invalid") is None
