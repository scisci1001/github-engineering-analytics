from typing import cast

from fastapi import Request

from github_analytics.infrastructure.mongodb.client import MongoDatabase, MongoHealthCheck


def get_mongo_database(request: Request) -> MongoHealthCheck:
    return cast(MongoDatabase, request.app.state.mongo)
