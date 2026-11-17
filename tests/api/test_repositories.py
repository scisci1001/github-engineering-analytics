from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from github_analytics.api.dependencies import get_repository_service
from github_analytics.api.security import require_api_key
from github_analytics.app import create_app
from github_analytics.domain.repository import GitHubRepository


class FakeRepositoryService:
    async def register(self, full_name: str) -> GitHubRepository:
        assert full_name == "fastapi/fastapi"
        now = datetime.now(timezone.utc)
        return GitHubRepository(
            id="507f1f77bcf86cd799439011",
            github_id=160919119,
            owner="fastapi",
            name="fastapi",
            full_name="fastapi/fastapi",
            default_branch="master",
            html_url="https://github.com/fastapi/fastapi",
            github_created_at=now,
            github_updated_at=now,
            created_at=now,
            updated_at=now,
        )


def test_register_repository_returns_201() -> None:
    app: FastAPI = create_app()
    app.dependency_overrides[require_api_key] = lambda: None
    app.dependency_overrides[get_repository_service] = lambda: FakeRepositoryService()

    with TestClient(app) as client:
        response = client.post(
            "/repositories",
            json={"full_name": "fastapi/fastapi"},
        )

    assert response.status_code == 201
    body = response.json()
    assert body["full_name"] == "fastapi/fastapi"
    assert body["github_id"] == 160919119
