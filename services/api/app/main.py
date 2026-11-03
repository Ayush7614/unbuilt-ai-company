import logging

from fastapi import FastAPI

from app.api.tasks import router as tasks_router
from app.config import APP_ENV, LOG_LEVEL
from app.database import Base, engine
from app.models import Task  # noqa: F401 — ensure model metadata is registered

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))

app = FastAPI(
    title="Unbuilt AI Company API",
    version="0.1.0",
    description="Experimental task lifecycle API for the Unbuilt AI Company reference implementation.",
)

# For the initial local-development foundation only. Use Alembic migrations before production.
if APP_ENV == "development":
    Base.metadata.create_all(bind=engine)

app.include_router(tasks_router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "environment": APP_ENV}
