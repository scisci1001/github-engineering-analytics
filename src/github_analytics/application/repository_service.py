from github_analytics.application.github_repository_client import GitHubRepositoryClient
from github_analytics.application.repository_repository import RepositoryRepository
from github_analytics.domain.repository import GitHubRepository


class RepositoryService:
    def __init__(
        self,
        github_client: GitHubRepositoryClient,
        repository_repository: RepositoryRepository,
    ) -> None:
        self._github_client = github_client
        self._repository_repository = repository_repository

    async def register(self, full_name: str) -> GitHubRepository:
        repository = await self._github_client.get_repository(full_name)
        return await self._repository_repository.upsert(repository)

    async def get_by_full_name(self, full_name: str) -> GitHubRepository | None:
        return await self._repository_repository.find_by_full_name(full_name)
