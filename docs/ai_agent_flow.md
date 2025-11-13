# AI Agent 协作流程

1. **Document Agent**
   - 监听 MinIO 上传事件，触发文档解析 Worker。
   - 调用 OCR/Document Intelligence 服务提取结构化文本。
   - 将解析结果写入 MongoDB `documents` 集合，并向队列发布“待出题”任务。

2. **Question Generation Agent**
   - 消费“待出题”任务，根据文档片段 + 知识点调用 `prompts/question_generation.md` 模板。
   - 生成的题目使用 `schemas/question.schema.json` 验证并入库 PostgreSQL `questions` 表，向量字段写入 pgvector。

3. **Quality Assurance Agent**
   - 对新题调用 `prompts/question_quality.md` 进行多维度评分。
   - 对评分低于阈值的题目发送人工复核通知，并在 `recommendations` 表记录建议。

4. **Adaptive Tutor Agent**
   - 根据 `question_attempts`、`learning_snapshots` 更新掌握度，应用 SRS 公式计算下次复习时间。
   - 为前端提供实时推荐 API（`/api/questions/adaptive`、`/api/study-plans/schedule`）。

5. **Coach Agent**
   - 聚合学习计划进度、打卡数据生成每日报告，推送至移动端通知。

> 各 Agent 间通过消息队列与数据库事件联动，核心数据流均可在 `sql/postgres_schema.sql` 与 `mongo/init.js` 中找到落地结构。
