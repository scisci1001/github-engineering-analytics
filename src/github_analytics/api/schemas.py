from datetime import datetime

from pydantic import BaseModel, Field

from github_analytics.domain.repository import GitHubRepository


class RepositoryCreateRequest(BaseModel):
    full_name: str = Field(
        examples=["fastapi/fastapi"],
        description="GitHub repository in owner/name form.",
    )


class RepositoryResponse(BaseModel):
    id: str
    github_id: int
    owner: str
    name: str
    full_name: str
    default_branch: str
    html_url: str
    github_created_at: datetime | None
    github_updated_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def from_domain(cls, repository: GitHubRepository) -> "RepositoryResponse":
        if repository.id is None:
            raise ValueError("Persisted repository must have an internal ID")

        return cls(
            id=repository.id,
            github_id=repository.github_id,
            owner=repository.owner,
            name=repository.name,
            full_name=repository.full_name,
            default_branch=repository.default_branch,
            html_url=repository.html_url,
            github_created_at=repository.github_created_at,
            github_updated_at=repository.github_updated_at,
            created_at=repository.created_at,
            updated_at=repository.updated_at,
        )
