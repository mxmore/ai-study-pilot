from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import questions, study_plans, documents, health


def create_app() -> FastAPI:
    app = FastAPI(title="AI Study Pilot", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(questions.router, prefix="/api")
    app.include_router(study_plans.router, prefix="/api")
    app.include_router(documents.router, prefix="/api")

    return app


app = create_app()
