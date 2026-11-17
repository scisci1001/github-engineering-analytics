import asyncio
from collections.abc import AsyncIterator, Iterator
from uuid import uuid4

import pytest
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import PyMongoError
from testcontainers.community.mongodb import MongoDbContainer


@pytest.fixture(scope="module")
def mongo_container() -> Iterator[MongoDbContainer]:
    # MongoDB 5.0+ requires AVX. The current development machine does not support it,
    # so integration tests intentionally use MongoDB 4.4 as the local compatibility target.
    with MongoDbContainer("mongo:4.4") as container:
        yield container


async def wait_until_mongodb_is_ready(
    client: AsyncMongoClient[dict[str, object]],
    attempts: int = 40,
    delay_seconds: float = 0.25,
) -> None:
    last_error: PyMongoError | None = None

    for _ in range(attempts):
        try:
            await client.admin.command("ping")
            return
        except PyMongoError as exc:
            last_error = exc
            await asyncio.sleep(delay_seconds)

    raise RuntimeError("MongoDB test container did not become ready") from last_error


@pytest.fixture
async def mongo_database(
    mongo_container: MongoDbContainer,
) -> AsyncIterator[AsyncDatabase[dict[str, object]]]:
    client: AsyncMongoClient[dict[str, object]] = AsyncMongoClient(
        mongo_container.get_connection_url(),
        serverSelectionTimeoutMS=1000,
    )

    await wait_until_mongodb_is_ready(client)

    database_name = f"github_analytics_test_{uuid4().hex}"
    database = client[database_name]

    try:
        yield database
    finally:
        await client.drop_database(database_name)
        await client.close()
