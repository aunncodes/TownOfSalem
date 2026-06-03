from fastapi import FastAPI
from core.settings import settings, add_cors


def create_app():
    app = FastAPI(title=settings.app_name)
    add_cors(app)
    app.include_router(api_router)
    return app


app = create_app()
