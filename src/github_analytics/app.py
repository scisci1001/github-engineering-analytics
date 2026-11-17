from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from github_analytics.api.exception_handlers import register_exception_handlers
from github_analytics.api.router import api_router
from github_analytics.config.settings import get_settings
from github_analytics.infrastructure.github.client import HttpGitHubRepositoryClient
from github_analytics.infrastructure.mongodb.client import MongoDatabase


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    mongo = MongoDatabase(
        uri=settings.mongodb_uri,
        database_name=settings.mongodb_database,
        server_selection_timeout_ms=settings.mongodb_server_selection_timeout_ms,
    )
    github_client = HttpGitHubRepositoryClient(
        token=settings.github_token,
        api_version=settings.github_api_version,
        base_url=settings.github_api_base_url,
    )

    app.state.mongo = mongo
    app.state.github_client = github_client

    try:
        yield
    finally:
        await github_client.close()
        await mongo.close()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    register_exception_handlers(app)
    app.include_router(api_router)

    return app
