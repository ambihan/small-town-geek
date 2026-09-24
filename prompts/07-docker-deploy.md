# M7 — Docker + Local Production-like Environment

阅读：

- AGENTS.md
- 当前项目
- README

---

# Goal

让整个项目可以通过 Docker Compose 启动。

---

# Services

V0.1：

```text
postgres
backend
web
````

不要加入：

* redis
* celery
* arq
* pgvector

---

# Backend Docker

创建：

```text
backend/Dockerfile
```

要求：

* Python 3.12
* production-ish image
* non-root user if practical
* environment variables
* healthcheck

---

# Web Docker

创建：

```text
apps/web/Dockerfile
```

使用 Next.js production build。

---

# PostgreSQL

使用官方 PostgreSQL image。

数据 volume：

```text
postgres_data
```

---

# Compose

```text
docker-compose.yml
```

支持：

```bash
docker compose up --build
```

---

# Health

Backend：

```text
/api/v1/health
```

Postgres healthcheck：

```text
pg_isready
```

---

# Migration

不要在 Docker image build 阶段执行 migration。

容器启动后提供明确的 migration command。

例如：

```bash
docker compose exec backend alembic upgrade head
```

---

# Environment

不要提交：

```text
.env
```

只提交：

```text
.env.example
```

---

# README

更新：

```text
Local Development
Docker Development
Database Migration
Testing
```

---

# Final Verification

验证：

```bash
docker compose up --build
```

然后：

```text
Backend health
Web
Postgres
```

都正常。

---

# Important

不要为了部署引入：

* Kubernetes
* Terraform
* Nginx
* Redis
* Celery

除非已经存在明确需求。