# M0 — 项目初始化

你现在负责初始化「小镇做题家」项目。

请先完整阅读仓库根目录的：

- AGENTS.md

严格遵守其中的技术和架构约束。

---

## Goal

建立一个可以本地启动的 Monorepo。

最终必须能够启动：

1. PostgreSQL
2. FastAPI
3. Next.js Admin
4. Taro 微信小程序项目

---

# 1. Repository

如果当前目录为空，创建：

```text
small-town-geek/
````

目录：

```text
apps/
  miniapp/
  web/

backend/

docs/
prompts/

AGENTS.md
README.md
docker-compose.yml
.gitignore
.env.example
```

如果项目已经存在，不要重复创建。

---

# 2. Backend

创建：

```text
backend/
```

使用：

* Python 3.12+
* FastAPI
* Pydantic v2
* SQLAlchemy 2.x
* Alembic
* asyncpg
* pytest
* httpx
* ruff

建议使用：

```text
pyproject.toml
```

管理 Python dependencies。

创建：

```text
backend/app/
  api/
  core/
  models/
  repositories/
  schemas/
  services/
  main.py
```

---

# 3. FastAPI

创建：

```text
GET /api/v1/health
```

返回：

```json
{
  "status": "ok"
}
```

API 应该可以通过：

```text
http://localhost:8000/api/v1/health
```

访问。

同时开启：

```text
/docs
```

Swagger。

---

# 4. PostgreSQL

创建 Docker Compose。

PostgreSQL：

```text
database: small_town_geek
user: postgres
password: postgres
port: 5432
```

这些只用于本地开发。

不要把生产密码写死进代码。

使用：

```text
.env
.env.example
```

---

# 5. Database

配置：

```text
DATABASE_URL
```

使用 SQLAlchemy Async Engine。

创建：

```text
backend/app/core/database.py
```

至少提供：

```python
engine
async_session_factory
get_db_session
```

---

# 6. Alembic

初始化 Alembic：

```text
backend/alembic/
backend/alembic.ini
```

确保 Alembic 可以正常连接 PostgreSQL。

---

# 7. Next.js

创建：

```text
apps/web/
```

使用：

* Next.js
* TypeScript
* Tailwind CSS
* shadcn/ui

创建一个简单 Admin Dashboard。

首页显示：

```text
小镇做题家

Admin Dashboard

题目
0

用户
0

知识点
0
```

不需要连接 API。

---

# 8. Taro

创建：

```text
apps/miniapp/
```

使用：

* Taro
* React
* TypeScript

至少创建：

```text
pages/index
pages/quiz
pages/mistakes
pages/learning
pages/profile
```

TabBar：

```text
首页
刷题
错题
学习
我的
```

页面先使用 mock data。

---

# 9. Environment

创建：

```text
.env.example
```

至少包含：

```env
DATABASE_URL=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
```

不要创建真实 secret。

---

# 10. Docker Compose

V0.1 只启动：

```text
postgres
```

暂时不要添加：

* redis
* celery
* arq
* pgvector

---

# 11. README

README 至少说明：

* 项目简介
* 技术栈
* Repository Structure
* 本地开发
* 如何启动 PostgreSQL
* 如何启动 Backend
* 如何启动 Web
* 如何启动 Mini Program

---

# 12. Quality Gate

完成之后执行：

Backend：

```bash
ruff check .
pytest
```

Frontend：

```bash
npm run lint
npm run build
```

如果 Taro 项目提供对应 build/typecheck 命令，也执行。

修复明显错误。

---

# 13. Final Response

完成后不要写长篇报告。

只告诉我：

1. 创建了哪些主要文件
2. 如何启动
3. 执行了哪些测试
4. 是否存在未解决问题

不要主动实现下一个 Milestone。