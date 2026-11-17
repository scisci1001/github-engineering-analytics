from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from github_analytics.api.router import api_router
from github_analytics.config.settings import get_settings
from github_analytics.infrastructure.mongodb.client import MongoDatabase


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    mongo = MongoDatabase(
        uri=settings.mongodb_uri,
        database_name=settings.mongodb_database,
        server_selection_timeout_ms=settings.mongodb_server_selection_timeout_ms,
    )
    app.state.mongo = mongo

    try:
        yield
    finally:
        await mongo.close()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    app.include_router(api_router)

    return app
