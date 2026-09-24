# 小镇做题家 — Coding Agent Master Prompt

你正在开发：

# 小镇做题家

这是一个 AI 刷题小程序。

产品定位：

> 一个会记住用户每一次错误，并根据知识点掌握情况动态安排练习和复习的 AI 刷题教练。

---

# FIRST STEP

在做任何事情之前：

1. 阅读 AGENTS.md
2. 阅读 README.md
3. 阅读 docs/ 下与当前任务相关的文档
4. 检查 git status
5. 检查当前项目结构
6. 检查已经完成的功能
7. 不要假设文件存在

---

# PRODUCT PRINCIPLE

核心不是：

> “拥有很多题。”

核心是：

> “知道用户下一步应该练什么。”

核心循环：

```text
做题
↓
记录
↓
分析
↓
掌握度
↓
复习
↓
下一题
````

---

# TECH PRINCIPLE

Backend：

```text
FastAPI
Python
SQLAlchemy
Alembic
PostgreSQL
```

Frontend：

```text
Taro
React
TypeScript
```

Admin：

```text
Next.js
React
TypeScript
Tailwind
shadcn/ui
```

AI：

```text
Python
AI Provider abstraction
Structured Output
Pydantic validation
```

---

# CURRENT V0.1 SCOPE

必须支持：

* Python
* single choice
* daily quiz
* answer submission
* explanation
* knowledge stats
* review
* AI explanation
* AI question generation
* mini program
* admin dashboard

---

# OUT OF SCOPE

不要主动实现：

* social
* leaderboard
* payments
* advertisements
* multiple subjects
* coding questions
* agent
* Redis
* Celery
* ARQ
* pgvector

除非任务明确要求。

---

# IMPLEMENTATION PROCESS

每个任务：

## Step 1

分析现有代码。

## Step 2

给出不超过 10 条的实施计划。

## Step 3

实施。

## Step 4

运行：

```text
tests
lint
typecheck
build
```

根据项目实际 scripts 执行。

## Step 5

修复错误。

## Step 6

检查：

```text
security
types
database
API compatibility
```

## Step 7

总结：

```text
Implemented
Tests
Potential Issues
Next Suggested Step
```

---

# IMPORTANT

不要因为发现代码可以重构，就顺便重构整个项目。

遵循：

> Minimal Change Principle

只修改完成当前任务所必需的代码。

---

# DATABASE

任何 schema change：

```text
SQLAlchemy Model
↓
Alembic Migration
↓
Migration Test
```

不能只改 Model 不生成 migration。

---

# API

Router：

```text
HTTP layer
```

Service：

```text
Business logic
```

Repository：

```text
Database access
```

不要混在一起。

---

# AI

AI 永远不是业务真相。

例如：

```text
AI says answer = B
```

不能直接相信。

Backend 必须：

```text
load question
↓
load expected answer
↓
deterministic comparison
↓
determine correctness
```

AI 只负责解释。

---

# QUALITY

如果测试失败：

不要简单删除测试。

找到真正原因并修复。

如果类型错误：

不要使用：

```typescript
any
```

或者：

```python
cast(Any, ...)
```

来掩盖问题。

---

# VIBE CODING STYLE

你是一个 coding agent，不是技术博客作者。

不要输出大量理论。

优先：

```text
inspect
plan
code
test
fix
```

每完成一个明确任务就停下来。

不要一次实现未来 10 个 Milestone。