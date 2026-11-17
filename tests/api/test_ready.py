from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import ServerSelectionTimeoutError

from github_analytics.api.dependencies import get_mongo_database
from github_analytics.app import create_app
from github_analytics.infrastructure.mongodb.client import MongoHealthCheck


class ReadyMongo:
    async def ping(self) -> None:
        return None


class UnavailableMongo:
    async def ping(self) -> None:
        raise ServerSelectionTimeoutError("MongoDB unavailable")


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


def test_ready_returns_200_when_mongodb_is_available(app: FastAPI, client: TestClient) -> None:
    def override() -> MongoHealthCheck:
        return ReadyMongo()

    app.dependency_overrides[get_mongo_database] = override

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "mongodb": "ok",
    }


def test_ready_returns_503_when_mongodb_is_unavailable(app: FastAPI, client: TestClient) -> None:
    def override() -> MongoHealthCheck:
        return UnavailableMongo()

    app.dependency_overrides[get_mongo_database] = override

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "MongoDB is unavailable"}
