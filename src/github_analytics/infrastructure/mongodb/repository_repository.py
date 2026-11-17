from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

from github_analytics.application.repository_repository import RepositoryRepository
from github_analytics.domain.repository import GitHubRepository
from github_analytics.infrastructure.mongodb.repository_mapper import (
    parse_object_id,
    repository_from_document,
    repository_to_document,
    utc_now,
)


class MongoRepositoryRepository(RepositoryRepository):
    def __init__(self, collection: AsyncCollection[dict[str, object]]) -> None:
        self._collection = collection

    async def upsert(self, repository: GitHubRepository) -> GitHubRepository:
        now = utc_now()
        document = repository_to_document(repository)

        updated = await self._collection.find_one_and_update(
            {"github_id": repository.github_id},
            {
                "$set": {
                    **document,
                    "updated_at": now,
                },
                "$setOnInsert": {
                    "created_at": now,
                },
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        if updated is None:
            raise RuntimeError("Repository upsert did not return a document")

        return repository_from_document(updated)

    async def find_by_id(self, repository_id: str) -> GitHubRepository | None:
        object_id = parse_object_id(repository_id)
        if object_id is None:
            return None

        document = await self._collection.find_one({"_id": object_id})
        return repository_from_document(document) if document is not None else None

    async def find_by_full_name(self, full_name: str) -> GitHubRepository | None:
        document = await self._collection.find_one({"full_name": full_name})
        return repository_from_document(document) if document is not None else None
