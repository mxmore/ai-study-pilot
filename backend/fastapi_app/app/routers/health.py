from fastapi import APIRouter

from ..core.config import get_settings

router = APIRouter()


@router.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "environment": settings.environment}
