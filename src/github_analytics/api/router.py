from fastapi import APIRouter

from github_analytics.api.system import router as system_router

api_router = APIRouter()
api_router.include_router(system_router)
