from datetime import datetime

import httpx

from github_analytics.application.github_repository_client import GitHubRepositoryClient
from github_analytics.domain.errors import GitHubApiError, GitHubRateLimitError, RepositoryNotFoundError
from github_analytics.domain.repository import GitHubRepository


class HttpGitHubRepositoryClient(GitHubRepositoryClient):
    def __init__(
        self,
        *,
        token: str | None,
        api_version: str,
        base_url: str = "https://api.github.com",
        client: httpx.AsyncClient | None = None,
    ) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": api_version,
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._client = client or httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=30.0,
        )
        self._owns_client = client is None
        self._headers = headers

    async def get_repository(self, full_name: str) -> GitHubRepository:
        owner, repository_name = _split_full_name(full_name)

        response = await self._client.get(
            f"/repos/{owner}/{repository_name}",
            headers=self._headers,
        )

        if response.status_code == 404:
            raise RepositoryNotFoundError(full_name)

        if response.status_code in {403, 429} and (
            response.headers.get("x-ratelimit-remaining") == "0" or "retry-after" in response.headers
        ):
            raise GitHubRateLimitError(
                response.status_code,
                f"GitHub rate limit reached for repository: {full_name}",
            )

        if response.is_error:
            raise GitHubApiError(
                response.status_code,
                f"GitHub API request failed with status {response.status_code}",
            )

        payload = response.json()

        return GitHubRepository(
            id=None,
            github_id=payload["id"],
            owner=payload["owner"]["login"],
            name=payload["name"],
            full_name=payload["full_name"],
            default_branch=payload["default_branch"],
            html_url=payload["html_url"],
            github_created_at=_parse_github_datetime(payload.get("created_at")),
            github_updated_at=_parse_github_datetime(payload.get("updated_at")),
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()


def _split_full_name(full_name: str) -> tuple[str, str]:
    parts = full_name.split("/", maxsplit=1)

    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Repository full name must have the form 'owner/repository'")

    return parts[0], parts[1]


def _parse_github_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))
