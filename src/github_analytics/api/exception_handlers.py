from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from github_analytics.domain.errors import GitHubApiError, GitHubRateLimitError, RepositoryNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RepositoryNotFoundError)
    async def repository_not_found_handler(
        request: Request,
        exc: RepositoryNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(GitHubRateLimitError)
    async def github_rate_limit_handler(
        request: Request,
        exc: GitHubRateLimitError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "GitHub API rate limit reached"},
        )

    @app.exception_handler(GitHubApiError)
    async def github_api_error_handler(
        request: Request,
        exc: GitHubApiError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": "GitHub API request failed"},
        )
