from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from github_analytics.domain.repository import GitHubRepository


def repository_to_document(repository: GitHubRepository) -> dict[str, Any]:
    return {
        "github_id": repository.github_id,
        "owner": repository.owner,
        "name": repository.name,
        "full_name": repository.full_name,
        "default_branch": repository.default_branch,
        "html_url": repository.html_url,
        "github_created_at": repository.github_created_at,
        "github_updated_at": repository.github_updated_at,
    }


def repository_from_document(document: dict[str, Any]) -> GitHubRepository:
    return GitHubRepository(
        id=str(document["_id"]),
        github_id=document["github_id"],
        owner=document["owner"],
        name=document["name"],
        full_name=document["full_name"],
        default_branch=document["default_branch"],
        html_url=document["html_url"],
        github_created_at=document.get("github_created_at"),
        github_updated_at=document.get("github_updated_at"),
        created_at=document.get("created_at"),
        updated_at=document.get("updated_at"),
    )


def parse_object_id(repository_id: str) -> ObjectId | None:
    try:
        return ObjectId(repository_id)
    except Exception:
        return None


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
