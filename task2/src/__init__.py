from fastapi import FastAPI

from src.api.routers import record_router, user_router
from src.core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, root_path=settings.TASK2_ROOT_PATH)

    app.include_router(user_router.router)
    app.include_router(record_router.router)

    return app
