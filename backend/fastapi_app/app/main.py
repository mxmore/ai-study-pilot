from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from .routers import questions, study_plans, documents, health


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Study Pilot API",
        description=(
            "AI Study Pilot 提供题目管理、自适应出题、学习计划与资料解析等服务，"
            "通过统一的 REST API 对外暴露能力。"
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=[
            {"name": "system", "description": "系统状态与健康检查接口。"},
            {"name": "questions", "description": "题目检索、自适应出题与质检反馈。"},
            {"name": "study_plans", "description": "学习计划与打卡相关接口。"},
            {"name": "documents", "description": "学习资料解析、入库与进度相关接口。"},
        ],
        swagger_ui_parameters={
            "defaultModelsExpandDepth": 0,
            "displayRequestDuration": True,
        },
    )

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

    @app.get("/swagger", include_in_schema=False)
    def swagger_ui() -> HTMLResponse:
        """提供显式 Swagger UI 入口，便于 Portal 或运维文档引用。"""

        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI",
            swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        )

    return app


app = create_app()
