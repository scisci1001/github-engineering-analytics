from typing import cast

from fastapi import Depends, Request

from github_analytics.application.github_repository_client import GitHubRepositoryClient
from github_analytics.application.repository_repository import RepositoryRepository
from github_analytics.application.repository_service import RepositoryService
from github_analytics.infrastructure.github.client import HttpGitHubRepositoryClient
from github_analytics.infrastructure.mongodb.client import MongoDatabase, MongoHealthCheck
from github_analytics.infrastructure.mongodb.repository_repository import MongoRepositoryRepository


def get_mongo_database(request: Request) -> MongoHealthCheck:
    return cast(MongoDatabase, request.app.state.mongo)


def get_github_client(request: Request) -> GitHubRepositoryClient:
    return cast(HttpGitHubRepositoryClient, request.app.state.github_client)


def get_repository_repository(request: Request) -> RepositoryRepository:
    mongo = cast(MongoDatabase, request.app.state.mongo)
    return MongoRepositoryRepository(mongo.database["repositories"])


def get_repository_service(
    github_client: GitHubRepositoryClient = Depends(get_github_client),
    repository_repository: RepositoryRepository = Depends(get_repository_repository),
) -> RepositoryService:
    return RepositoryService(
        github_client=github_client,
        repository_repository=repository_repository,
    )
