import asyncio

from github_analytics.config.settings import get_settings
from github_analytics.infrastructure.mongodb.client import MongoDatabase
from github_analytics.infrastructure.mongodb.schema import initialize_database


async def initialize() -> None:
    settings = get_settings()

    mongo = MongoDatabase(
        uri=settings.mongodb_uri,
        database_name=settings.mongodb_database,
        server_selection_timeout_ms=settings.mongodb_server_selection_timeout_ms,
    )

    try:
        await mongo.ping()
        await initialize_database(mongo.database)
    finally:
        await mongo.close()


def main() -> None:
    asyncio.run(initialize())


if __name__ == "__main__":
    main()
