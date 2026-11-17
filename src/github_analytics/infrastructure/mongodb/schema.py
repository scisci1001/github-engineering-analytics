from typing import Any

from pymongo import ASCENDING, IndexModel
from pymongo.asynchronous.database import AsyncDatabase

COLLECTION_VALIDATORS: dict[str, dict[str, Any]] = {
    "repositories": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["github_id", "owner", "name", "full_name", "default_branch", "html_url"],
            "properties": {
                "github_id": {"bsonType": ["int", "long"]},
                "owner": {"bsonType": "string"},
                "name": {"bsonType": "string"},
                "full_name": {"bsonType": "string"},
                "default_branch": {"bsonType": "string"},
                "html_url": {"bsonType": "string"},
                "github_created_at": {"bsonType": ["date", "null"]},
                "github_updated_at": {"bsonType": ["date", "null"]},
                "created_at": {"bsonType": ["date", "null"]},
                "updated_at": {"bsonType": ["date", "null"]},
            },
        }
    },
    "pull_requests": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "repository_id", "github_id", "number", "title", "author",
                "state", "draft", "created_at", "updated_at"
            ],
            "properties": {
                "repository_id": {"bsonType": "objectId"},
                "github_id": {"bsonType": ["int", "long"]},
                "number": {"bsonType": ["int", "long"]},
                "title": {"bsonType": "string"},
                "author": {
                    "bsonType": "object",
                    "required": ["login"],
                    "properties": {
                        "github_id": {"bsonType": ["int", "long", "null"]},
                        "login": {"bsonType": ["string", "null"]},
                    },
                },
                "state": {"bsonType": "string"},
                "draft": {"bsonType": "bool"},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"},
                "closed_at": {"bsonType": ["date", "null"]},
                "merged_at": {"bsonType": ["date", "null"]},
                "additions": {"bsonType": ["int", "long", "null"]},
                "deletions": {"bsonType": ["int", "long", "null"]},
                "changed_files": {"bsonType": ["int", "long", "null"]},
                "base_branch": {"bsonType": ["string", "null"]},
                "commits": {"bsonType": "array"},
                "reviews": {"bsonType": "array"},
            },
        }
    },
    "issues": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["repository_id", "github_id", "number", "title", "author", "state", "created_at", "updated_at"],
            "properties": {
                "repository_id": {"bsonType": "objectId"},
                "github_id": {"bsonType": ["int", "long"]},
                "number": {"bsonType": ["int", "long"]},
                "title": {"bsonType": "string"},
                "author": {
                    "bsonType": "object",
                    "required": ["login"],
                    "properties": {
                        "github_id": {"bsonType": ["int", "long", "null"]},
                        "login": {"bsonType": ["string", "null"]},
                    },
                },
                "state": {"bsonType": "string"},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"},
                "closed_at": {"bsonType": ["date", "null"]},
            },
        }
    },
    "sync_states": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["repository_id", "resource", "status"],
            "properties": {
                "repository_id": {"bsonType": "objectId"},
                "resource": {"enum": ["pull_requests", "issues"]},
                "status": {"bsonType": "string"},
                "last_started_at": {"bsonType": ["date", "null"]},
                "last_completed_at": {"bsonType": ["date", "null"]},
                "checkpoint": {"bsonType": ["date", "null"]},
                "processed_count": {"bsonType": ["int", "long", "null"]},
                "last_error": {"bsonType": ["string", "null"]},
            },
        }
    },
}

COLLECTION_INDEXES: dict[str, list[IndexModel]] = {
    "repositories": [
        IndexModel([("github_id", ASCENDING)], unique=True, name="ux_repositories_github_id"),
        IndexModel([("full_name", ASCENDING)], unique=True, name="ux_repositories_full_name"),
    ],
    "pull_requests": [
        IndexModel([("repository_id", ASCENDING), ("number", ASCENDING)], unique=True, name="ux_pull_requests_repository_number"),
        IndexModel([("repository_id", ASCENDING), ("created_at", ASCENDING)], name="ix_pull_requests_repository_created_at"),
        IndexModel([("repository_id", ASCENDING), ("merged_at", ASCENDING)], name="ix_pull_requests_repository_merged_at"),
        IndexModel([("repository_id", ASCENDING), ("author.github_id", ASCENDING)], name="ix_pull_requests_repository_author"),
    ],
    "issues": [
        IndexModel([("repository_id", ASCENDING), ("number", ASCENDING)], unique=True, name="ux_issues_repository_number"),
        IndexModel([("repository_id", ASCENDING), ("created_at", ASCENDING)], name="ix_issues_repository_created_at"),
        IndexModel([("repository_id", ASCENDING), ("closed_at", ASCENDING)], name="ix_issues_repository_closed_at"),
        IndexModel([("repository_id", ASCENDING), ("author.github_id", ASCENDING)], name="ix_issues_repository_author"),
    ],
    "sync_states": [
        IndexModel([("repository_id", ASCENDING), ("resource", ASCENDING)], unique=True, name="ux_sync_states_repository_resource"),
    ],
}


async def initialize_database(database: AsyncDatabase[dict[str, object]]) -> None:
    existing_collections = set(await database.list_collection_names())

    for collection_name, validator in COLLECTION_VALIDATORS.items():
        if collection_name not in existing_collections:
            await database.create_collection(
                collection_name,
                validator=validator,
                validationLevel="strict",
                validationAction="error",
            )
        else:
            await database.command(
                {
                    "collMod": collection_name,
                    "validator": validator,
                    "validationLevel": "strict",
                    "validationAction": "error",
                }
            )

        indexes = COLLECTION_INDEXES[collection_name]
        if indexes:
            await database[collection_name].create_indexes(indexes)
