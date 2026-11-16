from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pymongo.errors import PyMongoError

from github_analytics.api.dependencies import get_mongo_database
from github_analytics.config.settings import get_settings
from github_analytics.infrastructure.mongodb.client import MongoDatabase, MongoHealthCheck

STATIC_DIR = Path(__file__).resolve().parent / "static"


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

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", tags=["system"])
    async def ready(
        mongo: MongoHealthCheck = Depends(get_mongo_database),
    ) -> dict[str, str]:
        try:
            await mongo.ping()
        except PyMongoError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is unavailable",
            ) from exc

        return {
            "status": "ready",
            "mongodb": "ok",
        }

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon() -> FileResponse:
        return FileResponse(
            STATIC_DIR / "favicon.ico",
            media_type="image/x-icon",
        )

    return app


app = create_app()
