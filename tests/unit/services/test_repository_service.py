from dataclasses import replace

from github_analytics.application.repository_service import RepositoryService
from github_analytics.domain.repository import GitHubRepository


class FakeGitHubClient:
    def __init__(self, repository: GitHubRepository) -> None:
        self.repository = repository
        self.requested_full_name: str | None = None

    async def get_repository(self, full_name: str) -> GitHubRepository:
        self.requested_full_name = full_name
        return self.repository


class FakeRepositoryRepository:
    def __init__(self, saved: GitHubRepository) -> None:
        self.saved = saved
        self.upserted: GitHubRepository | None = None

    async def upsert(self, repository: GitHubRepository) -> GitHubRepository:
        self.upserted = repository
        return self.saved

    async def find_by_id(self, repository_id: str) -> GitHubRepository | None:
        return None

    async def find_by_full_name(self, full_name: str) -> GitHubRepository | None:
        return self.saved if self.saved.full_name == full_name else None


async def test_register_fetches_from_github_and_persists() -> None:
    github_repository = GitHubRepository(
        id=None,
        github_id=123,
        owner="fastapi",
        name="fastapi",
        full_name="fastapi/fastapi",
        default_branch="master",
        html_url="https://github.com/fastapi/fastapi",
    )
    saved_repository = replace(
        github_repository,
        id="507f1f77bcf86cd799439011",
    )

    github_client = FakeGitHubClient(github_repository)
    repository_repository = FakeRepositoryRepository(saved_repository)
    service = RepositoryService(github_client, repository_repository)

    result = await service.register("fastapi/fastapi")

    assert github_client.requested_full_name == "fastapi/fastapi"
    assert repository_repository.upserted == github_repository
    assert result == saved_repository
