from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.routers import router as user_router
from issues.routers import router as issue_router
from config import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(issue_router)

