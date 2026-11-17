from fastapi import APIRouter, Depends, status

from github_analytics.api.dependencies import get_repository_service
from github_analytics.api.schemas import RepositoryCreateRequest, RepositoryResponse
from github_analytics.api.security import require_api_key
from github_analytics.application.repository_service import RepositoryService

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def register_repository(
    request: RepositoryCreateRequest,
    service: RepositoryService = Depends(get_repository_service),
) -> RepositoryResponse:
    repository = await service.register(request.full_name)
    return RepositoryResponse.from_domain(repository)
