# AI Study Pilot

智能考试学习平台的参考实现，涵盖数据库 Schema、后端骨架、前端原型、AI Prompt 库与校验工具。

## 目录结构

```
.
├── backend
│   ├── fastapi_app        # FastAPI API 骨架
│   ├── nestjs_app         # NestJS 方案说明
│   └── worker             # 文档解析与入库流水线
├── docs                   # 集成说明
├── frontend               # Next.js + TypeScript 前端原型
├── mongo                  # MongoDB 初始化脚本
├── prompts                # AI Agent Prompt 库
├── schemas                # JSON Schema 定义
├── scripts                # 校验脚本
├── samples                # 示例数据
└── sql                    # PostgreSQL Schema + 种子数据
```

## 快速开始

### 数据库
- PostgreSQL：执行 `sql/postgres_schema.sql` 启用 `pgcrypto` 与 `pgvector` 扩展并导入种子数据。
- MongoDB：在 mongo shell 中运行 `load('mongo/init.js')`。

### 后端
```
cd backend/fastapi_app
uvicorn app.main:app --reload
```

FastAPI 提供基础接口：
- `GET /health`
- `GET /api/questions`
- `POST /api/questions/adaptive`
- `POST /api/questions/{id}/review`
- `POST /api/documents/ingest`

接口的 OpenAPI/Swagger 文档默认托管在 `http://localhost:8000/docs`，Redoc 版本位于 `http://localhost:8000/redoc`，支持直接试调请求。

### Worker
```
python backend/worker/worker.py
```

该脚本演示如何消费队列任务并调用 `DocumentIngestionPipeline` 完成下载、切分、生成Embedding与持久化的流程（示例实现使用本地文件）。

### 前端
```
cd frontend
npm install
npm run dev
```

Next.js 原型包含首页、刷题、资料阅读、学习报告与计划页面，并内置一个 `pages/api/questions` Mock 接口。

### Prompt 质量校验
```
pip install jsonschema
python scripts/validate_question.py
```

会基于 `schemas/question.schema.json` 校验 `samples` 目录下的 JSON。

## 第三方能力

详见 [docs/integration_overview.md](docs/integration_overview.md)，涵盖 MinIO、OpenAI/Qwen3、Document Intelligence、向量搜索与消息队列等对接要点。

Windows 本地调试与第三方服务 Docker 启动流程，请参考 [docs/windows_local_debug.md](docs/windows_local_debug.md)。
