from fastapi import FastAPI

from src.api import routers
from src.core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, root_path=settings.TASK1_ROOT_PATH)

    app.include_router(routers.router)

    return app
