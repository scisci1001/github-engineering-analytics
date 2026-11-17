from datetime import datetime, timezone

import httpx
import pytest

from github_analytics.domain.errors import GitHubApiError, GitHubRateLimitError, RepositoryNotFoundError
from github_analytics.infrastructure.github.client import HttpGitHubRepositoryClient


def create_client(handler: httpx.MockTransport) -> HttpGitHubRepositoryClient:
    http_client = httpx.AsyncClient(
        base_url="https://api.github.test",
        transport=handler,
    )
    return HttpGitHubRepositoryClient(
        token="secret-token",
        api_version="2026-03-10",
        base_url="https://api.github.test",
        client=http_client,
    )


async def test_get_repository_maps_github_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/fastapi/fastapi"
        assert request.headers["accept"] == "application/vnd.github+json"
        assert request.headers["authorization"] == "Bearer secret-token"
        assert request.headers["x-github-api-version"] == "2026-03-10"

        return httpx.Response(
            200,
            json={
                "id": 160919119,
                "name": "fastapi",
                "full_name": "fastapi/fastapi",
                "owner": {"login": "fastapi"},
                "html_url": "https://github.com/fastapi/fastapi",
                "default_branch": "master",
                "created_at": "2018-12-08T08:21:47Z",
                "updated_at": "2026-11-17T10:00:00Z",
            },
        )

    client = create_client(httpx.MockTransport(handler))

    repository = await client.get_repository("fastapi/fastapi")

    assert repository.github_id == 160919119
    assert repository.owner == "fastapi"
    assert repository.name == "fastapi"
    assert repository.full_name == "fastapi/fastapi"
    assert repository.default_branch == "master"
    assert repository.github_created_at == datetime(2018, 12, 8, 8, 21, 47, tzinfo=timezone.utc)
    assert repository.github_updated_at == datetime(2026, 11, 17, 10, 0, tzinfo=timezone.utc)


async def test_get_repository_maps_404_to_not_found() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "Not Found"})

    client = create_client(httpx.MockTransport(handler))

    with pytest.raises(RepositoryNotFoundError):
        await client.get_repository("missing/repository")


async def test_get_repository_maps_rate_limit_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            headers={
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1893456000",
            },
            json={"message": "API rate limit exceeded"},
        )

    client = create_client(httpx.MockTransport(handler))

    with pytest.raises(GitHubRateLimitError):
        await client.get_repository("fastapi/fastapi")


async def test_get_repository_maps_server_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"message": "Internal Server Error"})

    client = create_client(httpx.MockTransport(handler))

    with pytest.raises(GitHubApiError) as exc_info:
        await client.get_repository("fastapi/fastapi")

    assert exc_info.value.status_code == 500


async def test_get_repository_rejects_invalid_full_name() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("HTTP request must not be executed")

    client = create_client(httpx.MockTransport(handler))

    with pytest.raises(ValueError):
        await client.get_repository("invalid")
