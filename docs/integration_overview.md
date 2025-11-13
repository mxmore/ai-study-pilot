# 第三方服务集成概览

| 服务 | 用途 | 备注 |
| ---- | ---- | ---- |
| MinIO | 题库原始文件、解析结果存储 | 与 ingestion worker 通过 S3 SDK 交互 |
| OpenAI / Qwen3 | 题目生成与质量评估 | 通过统一的 LLM Proxy 服务调用 |
| Document Intelligence (OCR) | PDF/图片解析 | 支持批量文档识别，输出结构化文本 |
| AI Search (pgvector + reranker) | 语义检索文档与题目 | 结合 Postgres + 向量索引 |
| Redis / RabbitMQ | 队列消息 | Worker 消费文档解析任务 |

> 生产环境中需要在 `.env` 或密钥管理系统中配置访问凭证。
