# 小镇做题家 (small-town-geek)

> 一个会记住用户每一次错误，并根据用户知识点掌握情况决定"下一道题应该练什么"的 AI 刷题小程序。

本仓库为 **M0 初始化版本**：一个可以在本地启动的 Monorepo，包含后端、管理后台与微信小程序骨架。业务功能将在后续 Milestone 中逐步实现（见 `prompts/`）。

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 小程序 | Taro + React + TypeScript |
| 管理后台 | Next.js (App Router) + TypeScript + Tailwind CSS + shadcn/ui |
| 后端 | Python 3.12+ · FastAPI · Pydantic v2 · SQLAlchemy 2.x (async) · Alembic |
| 数据库 | PostgreSQL |
| 本地编排 | Docker Compose |

## Repository Structure

```text
small-town-geek/
├── apps/
│   ├── miniapp/        # Taro 微信小程序
│   └── web/            # Next.js 管理后台
├── backend/            # FastAPI 后端
│   ├── app/
│   │   ├── api/        # 路由 (仅 HTTP，业务下沉到 service)
│   │   ├── core/       # 配置 / 数据库
│   │   ├── models/     # SQLAlchemy 模型
│   │   ├── repositories/
│   │   ├── schemas/    # Pydantic Schema
│   │   ├── services/   # 业务逻辑 (ai / quiz / review)
│   │   └── main.py
│   ├── alembic/        # 数据库迁移
│   └── pyproject.toml
├── docs/
├── prompts/            # 各 Milestone 任务说明
├── docker-compose.yml
├── AGENTS.md           # 技术与架构约束（必读）
└── README.md
```

## 本地开发

### 前置要求

- Python 3.12+
- Node.js 18+ 与 npm
- Docker / Docker Compose
- 微信开发者工具（用于预览小程序）

### 0. 准备环境变量

```bash
cp .env.example .env
# 按需填写 DATABASE_URL 与各 AI Key（V0.1 Key 可留空）
```

### 1. 启动 PostgreSQL

```bash
docker compose up -d postgres
```

数据库默认参数（仅本地开发）：

```text
database: small_town_geek
user:     postgres
password: postgres
port:     5432
```

### 2. 启动 Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 应用数据库迁移（当前无业务表，命令用于验证连通性）
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --port 8000
```

- 健康检查：<http://localhost:8000/api/v1/health> → `{"status": "ok"}`
- Swagger 文档：<http://localhost:8000/docs>

### 3. 启动 Web（管理后台）

```bash
cd apps/web
npm install
npm run dev
```

访问 <http://localhost:3000>，首页展示题目 / 用户 / 知识点计数（M0 均为 0，未连接 API）。

### 4. 启动 Mini Program（微信小程序）

```bash
cd apps/miniapp
npm install
npm run dev:weapp
```

然后用「微信开发者工具」打开 `apps/miniapp/` 目录（编译产物在 `dist/`）。
TabBar：首页 / 刷题 / 错题 / 学习 / 我的，页面均使用 mock data。

> H5 预览：`npm run dev:h5`。
> 说明：M0 未放置 TabBar 图标（避免引入二进制资源），微信端以纯文字展示。

## 质量校验

Backend：

```bash
cd backend
ruff check .
pytest
```

Frontend：

```bash
cd apps/web && npm run lint && npm run build
cd apps/miniapp && npm run type-check && npm run build:weapp
```

## 约束

开发前请阅读根目录 [`AGENTS.md`](./AGENTS.md)，其中定义了架构分层、AI 使用边界、数据库与 API 规范等硬性约束。
