from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from github_analytics.config.settings import get_settings

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon() -> FileResponse:
        return FileResponse(
            STATIC_DIR / "favicon.ico",
            media_type="image/x-icon",
        )

    return app


app = create_app()
