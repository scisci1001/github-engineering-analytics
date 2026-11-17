from typing import Protocol

from github_analytics.domain.repository import GitHubRepository


class RepositoryRepository(Protocol):
    async def upsert(self, repository: GitHubRepository) -> GitHubRepository: ...

    async def find_by_id(self, repository_id: str) -> GitHubRepository | None: ...

    async def find_by_full_name(self, full_name: str) -> GitHubRepository | None: ...
