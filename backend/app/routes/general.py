from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/core", tags=["health"])


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")
