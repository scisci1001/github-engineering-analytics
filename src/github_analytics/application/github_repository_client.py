from typing import Protocol

from github_analytics.domain.repository import GitHubRepository


class GitHubRepositoryClient(Protocol):
    async def get_repository(self, full_name: str) -> GitHubRepository: ...
