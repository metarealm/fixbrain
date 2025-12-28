# app/main.py
from fastapi import FastAPI
from app.api.routes_tasks import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="FixBrain Orchestrator", version="0.1.0")
    app.include_router(tasks_router)
    return app


app = create_app()

