from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.users.routers import router as user_router
# from src.modules.issues.routers import router as issue_router
from src.config import settings


def get_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user_router)
    # app.include_router(issue_router)
    return app