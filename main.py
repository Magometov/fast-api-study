from fastapi import FastAPI

from users.routers import router as user_router
from issues.routers import router as issue_router

app = FastAPI()

app.include_router(user_router)
app.include_router(issue_router)

