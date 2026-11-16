from typing import Protocol

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase


class MongoHealthCheck(Protocol):
    async def ping(self) -> None: ...


class MongoDatabase:
    def __init__(
        self,
        uri: str,
        database_name: str,
        server_selection_timeout_ms: int,
    ) -> None:
        self._client: AsyncMongoClient[dict[str, object]] = AsyncMongoClient(
            uri,
            serverSelectionTimeoutMS=server_selection_timeout_ms,
        )
        self.database: AsyncDatabase[dict[str, object]] = self._client[database_name]

    async def ping(self) -> None:
        await self._client.admin.command("ping")

    async def close(self) -> None:
        await self._client.close()
