# Windows 本地调试与环境初始化指南

本文面向使用 Windows 10/11 的开发者，介绍如何在本地完成 AI Study Pilot 项目的调试，包括 Docker 启动第三方服务、环境变量配置以及常见的开发工具链建议。

## 1. 先决条件

1. **Windows 10 21H2+ / Windows 11**，建议开启 [WSL2](https://learn.microsoft.com/windows/wsl/install)。
2. [**Docker Desktop**](https://www.docker.com/products/docker-desktop/)，安装时勾选启用 WSL2 Backend。
3. **Python 3.11+**，推荐在 PowerShell 中执行 `winget install Python.Python.3.11`。
4. **Node.js 18+**，可使用 `winget install OpenJS.NodeJS.LTS` 安装。
5. 推荐安装 **Visual Studio Code** 或 JetBrains 系 IDE，并启用 WSL Remote 开发能力以获得接近 Linux 的体验。

> **WSL 建议**：若计划在 WSL 内调试，使用 `wsl --install -d Ubuntu` 创建发行版，然后在 WSL 中完成后续步骤即可使用 Linux 命令行工具。

## 2. 仓库克隆与目录结构

在 PowerShell 或 WSL 终端中执行：

```powershell
# Windows PowerShell
cd $HOME\dev
git clone https://github.com/mxmore/ai-study-pilot.git
cd ai-study-pilot
```

或在 WSL 内：

```bash
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/mxmore/ai-study-pilot.git
cd ai-study-pilot
```

项目结构说明见根目录 `README.md`。

## 3. 环境变量与虚拟环境

在 `backend/fastapi_app` 目录下创建 `.env` 文件，用于配置数据库/存储连接信息：

```bash
cd backend/fastapi_app
copy NUL .env  # PowerShell
# 或
:> .env        # Git Bash/WSL
```

写入示例内容：

```
ENVIRONMENT=development
POSTGRES_DSN=postgresql+psycopg://ai_study:ai_study@localhost:5432/ai_study
MONGO_DSN=mongodb://localhost:27017
VECTOR_DIMENSION=1536
MINIO_ENDPOINT=http://127.0.0.1:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=changeme123
```

> Windows 中文件路径可使用正斜杠（`/`）或双反斜杠（`\\`）。当与 Docker 挂载目录交互时，推荐使用 WSL 路径或 `C:/Users/<name>` 形式。

创建 Python 虚拟环境并安装依赖：

```powershell
cd backend/fastapi_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Worker 与脚本可以共用同一虚拟环境，也可在 `backend/worker` 目录下分别安装。

## 4. Docker 启动第三方服务

以下命令在 PowerShell 中执行，若使用 WSL 终端请去掉反斜杠续行符。

### 4.1 PostgreSQL（含 pgvector）

```powershell
docker run -d --name ai-study-postgres ^
  -e POSTGRES_USER=ai_study ^
  -e POSTGRES_PASSWORD=ai_study ^
  -e POSTGRES_DB=ai_study ^
  -p 5432:5432 ^
  -v ${PWD}/.data/postgres:/var/lib/postgresql/data ^
  ankane/pgvector
```

初始化 Schema：

```powershell
psql "postgresql://ai_study:ai_study@localhost:5432/ai_study" -f sql/postgres_schema.sql
```

### 4.2 MongoDB

```powershell
docker run -d --name ai-study-mongo ^
  -p 27017:27017 ^
  -v ${PWD}/.data/mongo:/data/db ^
  mongo:6
```

导入种子数据：

```powershell
mongosh "mongodb://localhost:27017" mongo/init.js
```

### 4.3 MinIO 对象存储

```powershell
docker run -d --name ai-study-minio ^
  -p 9000:9000 -p 9090:9090 ^
  -e MINIO_ROOT_USER=admin ^
  -e MINIO_ROOT_PASSWORD=changeme123 ^
  -v ${PWD}/.data/minio:/data ^
  minio/minio server /data --console-address ":9090"
```

- MinIO 管理控制台地址：<http://localhost:9090>
- Access Key / Secret 与 `.env` 中保持一致。
- 可通过 MinIO Client (`mc`) 或浏览器创建 `documents`、`reports` 等 Bucket。

### 4.4 可选服务

- **向量数据库**：可使用 [Qdrant](https://qdrant.tech/) 或 [Milvus](https://milvus.io/)，Docker 命令与上方类似。
- **消息队列**：如需队列 Worker，可拉起 `redis` 或 `rabbitmq`。

## 5. 启动应用组件

1. **FastAPI**：
   ```powershell
   cd backend/fastapi_app
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Swagger UI 地址：<http://localhost:8000/docs>，Redoc：<http://localhost:8000/redoc>。

2. **Worker**：
   ```powershell
   cd backend/worker
   python worker.py
   ```

3. **前端 Next.js**：
   ```powershell
   cd frontend
   npm install
   npm run dev -- --hostname 0.0.0.0 --port 3000
   ```

## 6. VS Code 调试建议

- 使用 `Python: Select Interpreter` 选择 `.venv` 虚拟环境。
- 配置 `launch.json`，添加 Uvicorn 启动项：
  ```json
  {
    "name": "FastAPI",
    "type": "python",
    "request": "launch",
    "module": "uvicorn",
    "args": ["app.main:app", "--reload"],
    "cwd": "${workspaceFolder}/backend/fastapi_app"
  }
  ```
- 前端可使用 `npm run dev` 启动后，借助 VS Code Edge/Chrome Debugger 附加到浏览器。

## 7. 常见问题

- **端口被占用**：使用 `Get-Process -Id (Get-NetTCPConnection -LocalPort 5432).OwningProcess` 查找占用程序。
- **Docker 挂载失败**：确保路径在 Windows 文件系统中存在，或通过 WSL 路径 `/mnt/c/...` 访问。
- **网络代理**：公司网络需配置代理时，可在 PowerShell 设置 `setx HTTP_PROXY http://proxy:port`。

完成以上步骤后，即可在 Windows 本地完成端到端的调试与联调。
