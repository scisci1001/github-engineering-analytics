from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pymongo.errors import PyMongoError

from github_analytics.api.dependencies import get_mongo_database
from github_analytics.infrastructure.mongodb.client import MongoHealthCheck

router = APIRouter(tags=["system"])

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
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


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(
        STATIC_DIR / "favicon.ico",
        media_type="image/x-icon",
    )
