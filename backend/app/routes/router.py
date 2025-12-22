from fastapi import APIRouter

from backend.app.routes.general import router as general_router
from backend.app.routes.game import router as game_router

api_router = APIRouter()
api_router.include_router(general_router)
api_router.include_router(game_router)