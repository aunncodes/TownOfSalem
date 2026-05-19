from fastapi import APIRouter
from backend.app.enums.message import HealthResponse

router = APIRouter(prefix="/core", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")
