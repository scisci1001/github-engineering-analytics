from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class GitHubRepository:
    id: str | None
    github_id: int
    owner: str
    name: str
    full_name: str
    default_branch: str
    html_url: str
    github_created_at: datetime | None = None
    github_updated_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
