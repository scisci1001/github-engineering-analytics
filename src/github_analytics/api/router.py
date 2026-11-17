from fastapi import APIRouter

from github_analytics.api.repositories import router as repositories_router
from github_analytics.api.system import router as system_router

api_router = APIRouter()
api_router.include_router(system_router)
api_router.include_router(repositories_router)
