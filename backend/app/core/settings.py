from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware


class Settings(BaseModel):
    app_name: str = "tos"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

settings = Settings()
