# AGENTS.md

## Project

项目名称：小镇做题家

英文代号：small-town-geek

产品定位：

> 一个会记住用户每一次错误，并根据用户知识点掌握情况决定“下一道题应该练什么”的 AI 刷题小程序。

V0.1 第一阶段只支持：

- Python
- 单选题
- 每日训练
- 答题
- 答案解析
- 错题
- 知识点掌握度
- 简单复习机制
- AI 题目解析
- AI 题目生成
- Next.js 管理后台

不要在 V0.1 引入不必要的复杂度。

---

# 1. 技术栈

## Mini Program

- Taro
- React
- TypeScript

## Web

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic

## Database

- PostgreSQL

## AI

- Python
- 各家 LLM API
- 必须通过统一 AI Provider 抽象层访问模型

## Storage

- S3 / Cloudflare R2

## Optional Infrastructure

只有存在真实需求时才添加：

- Redis
- Celery
- ARQ
- pgvector

V0.1 默认不使用这些组件。

## Deployment

- Docker
- Docker Compose
- 云服务器 / 托管平台

---

# 2. 核心原则

## 2.1 Keep It Simple

优先选择简单、明确、可维护的实现。

不要为了展示技术而引入：

- Redis
- Celery
- Kafka
- 微服务
- Event Bus
- CQRS
- Event Sourcing
- GraphQL
- Kubernetes

如果一个功能可以通过简单的 FastAPI + PostgreSQL 完成，就不要引入额外基础设施。

---

# 2.2 AI 不负责确定性业务逻辑

AI 负责：

- 题目生成
- 题目解析
- 错因分析
- 学习总结
- 个性化建议

AI 不负责：

- 判分
- 计算正确率
- 更新 mastery_score
- 决定 next_review_at
- 创建数据库关系
- 权限判断
- 核心业务规则

所有确定性业务逻辑必须由 Python Backend 实现。

---

# 2.3 LLM 输出必须结构化

禁止直接把自然语言 LLM 输出写入数据库。

流程必须是：

LLM
↓
Structured Output
↓
Pydantic Validation
↓
Business Validation
↓
Database

如果模型返回非法结构：

- 不要静默修复
- 返回明确错误
- 必要时重试

---

# 2.4 Backend 是业务真相来源

Mini Program 和 Web 都不能自己实现核心业务规则。

例如：

错误：

```text
Mini Program 自己计算 mastery_score
````

正确：

```text
Mini Program
    ↓
FastAPI
    ↓
Quiz Service
    ↓
PostgreSQL
```

---

# 3. Repository Structure

目标结构：

```text
small-town-geek/
│
├── apps/
│   ├── miniapp/
│   └── web/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai/
│   │   │   ├── quiz/
│   │   │   └── review/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── tests/
│   └── pyproject.toml
│
├── docs/
├── prompts/
├── docker-compose.yml
├── AGENTS.md
└── README.md
```

不要随意改变顶层结构。

如果认为必须改变：

1. 先说明原因
2. 评估影响
3. 优先选择最小改动

---

# 4. Python Coding Rules

使用：

* Python 3.12+
* async/await
* SQLAlchemy 2.x
* Pydantic v2
* Ruff
* pytest

尽量使用：

```python
async def
```

数据库访问使用 SQLAlchemy AsyncSession。

不要：

```python
session.query(...)
```

优先：

```python
result = await session.execute(
    select(User).where(User.id == user_id)
)
```

---

# 5. FastAPI Rules

Router 只负责：

* HTTP 参数
* Authentication
* 调用 Service
* 返回 Schema

不要在 Router 中堆业务逻辑。

错误：

```python
@router.post("/answers")
async def submit_answer(...):
    # 100 lines business logic
```

正确：

```python
@router.post("/answers")
async def submit_answer(...):
    return await quiz_service.submit_answer(...)
```

---

# 6. Service Layer

业务逻辑放在：

```text
backend/app/services/
```

主要 Service：

```text
QuizService
ReviewService
KnowledgeService
AIService
```

Service 可以调用 Repository。

---

# 7. Repository Layer

Repository 负责数据库访问。

例如：

```text
QuestionRepository
QuizSessionRepository
QuizAnswerRepository
KnowledgeRepository
ReviewRepository
```

不要在 Repository 中：

* 调用 LLM
* 修改 HTTP Response
* 处理 UI 逻辑

---

# 8. Database Rules

使用：

* PostgreSQL
* UUID primary key
* timezone-aware timestamp

推荐：

```python
created_at
updated_at
```

所有时间都使用 UTC 存储。

不要使用：

```python
datetime.now()
```

优先使用 timezone-aware datetime。

---

# 9. Database Models

V0.1 核心模型：

```text
User

Question
QuestionOption

KnowledgePoint
QuestionKnowledgePoint

QuizSession
QuizAnswer

UserKnowledgeStat

ReviewItem
```

关系：

```text
User
 ├── QuizSession
 │      └── QuizAnswer
 │             └── Question
 │
 ├── UserKnowledgeStat
 │      └── KnowledgePoint
 │
 └── ReviewItem
        └── KnowledgePoint


Question
 └── QuestionKnowledgePoint
        └── KnowledgePoint
```

---

# 10. Alembic Rules

任何数据库结构变化：

必须：

```text
修改 SQLAlchemy Model
↓
生成 Alembic migration
↓
检查 migration
↓
执行 migration
```

禁止直接修改线上数据库结构。

禁止手写与 Model 不一致的 migration。

---

# 11. API Versioning

API 使用：

```text
/api/v1
```

例如：

```text
/api/v1/auth
/api/v1/questions
/api/v1/quiz
/api/v1/reviews
/api/v1/knowledge
/api/v1/ai
```

---

# 12. API Response Rules

Pydantic Schema 必须明确。

不要直接返回 SQLAlchemy Model。

错误：

```python
return question
```

如果 response model 不明确。

正确：

```python
return QuestionResponse.model_validate(question)
```

---

# 13. Error Handling

API 错误必须结构化。

例如：

```json
{
  "code": "QUESTION_NOT_FOUND",
  "message": "Question not found"
}
```

不要把 Python traceback 返回给客户端。

开发环境可以记录详细日志。

生产环境不要泄露：

* SQL
* API key
* stack trace
* 内部路径

---

# 14. Authentication

V0.1 使用微信登录。

但认证系统必须抽象：

```text
AuthService
```

不要把微信 OpenID 逻辑散落在业务代码中。

未来可能支持：

* Email
* Google
* GitHub

所以业务层只应该关心：

```text
current_user
```

---

# 15. Question Domain

V0.1 只支持：

```text
single_choice
```

题目：

```text
Question
 ├── content
 ├── type
 ├── difficulty
 ├── answer
 └── explanation

QuestionOption
 ├── key
 ├── content
 └── sort_order
```

V0.1 不实现：

* coding question
* fill blank
* essay
* multiple choice

除非任务明确要求。

---

# 16. Knowledge Point

KnowledgePoint 使用树结构：

```text
Python
├── Data Types
│   ├── List
│   │   └── Slice
│   ├── Dict
│   └── Set
├── Function
│   ├── Lambda
│   └── Decorator
├── OOP
└── Async
```

使用：

```text
parent_id
```

实现树。

不要引入额外 graph database。

---

# 17. Quiz Rules

QuizSession 表示一次训练。

V0.1 支持：

```text
daily
practice
review
```

默认 daily：

```text
10 questions
```

用户提交答案后：

```text
validate question
↓
validate answer
↓
calculate correctness
↓
create QuizAnswer
↓
update KnowledgeStat
↓
update ReviewItem
```

必须保证数据库事务一致性。

---

# 18. Scoring Rules

V0.1 不做复杂算法。

mastery_score 范围：

```text
0.0 ~ 1.0
```

第一版可以使用简单加权算法：

```text
correct_rate * 0.7
+
recent_performance * 0.3
```

算法必须集中在：

```text
KnowledgeService
```

不要散落在 Router / Model 中。

---

# 19. Review Rules

第一版采用简单 spaced repetition。

建议：

```text
第一次答对 → +1 day
第二次答对 → +3 days
第三次答对 → +7 days
第四次答对 → +14 days
第五次答对 → +30 days
```

答错：

```text
review_count >= 1
→ next review +1 day
```

这些规则必须集中管理。

未来可以替换成 FSRS，但 V0.1 不需要。

---

# 20. AI Provider Architecture

必须抽象：

```text
AIProvider
```

例如：

```python
class AIProvider(Protocol):
    async def explain_question(...): ...
    async def generate_question(...): ...
    async def learning_summary(...): ...
```

Provider：

```text
OpenAIProvider
ClaudeProvider
GeminiProvider
```

不要让业务代码直接依赖具体 SDK。

---

# 21. AI Configuration

API Key 必须通过 environment variable：

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
```

禁止：

```text
hard-coded API keys
```

禁止提交：

```text
.env
```

仓库提交：

```text
.env.example
```

---

# 22. AI Question Generation

AI 生成题目必须包含：

```text
content
options
answer
explanation
knowledge_points
difficulty
```

生成之后必须：

1. Pydantic validation
2. option count validation
3. answer validation
4. difficulty validation
5. knowledge point validation
6. business validation
7. save to DB

---

# 23. Prompt Rules

Prompt 必须存放在：

```text
backend/app/services/ai/prompts/
```

不要把长 Prompt 写在 Router 中。

Prompt 应该版本化。

例如：

```text
question_generation_v1
question_explanation_v1
learning_summary_v1
```

---

# 24. Frontend Rules

## Taro

使用：

* React
* TypeScript
* hooks
* functional components

不要使用 class component。

业务 API 统一放：

```text
src/services/
```

不要在页面中直接：

```text
Taro.request(...)
```

---

# 25. Web Rules

Next.js 使用 App Router。

优先：

* Server Components
* Client Components only when needed

shadcn/ui 用于：

* Dialog
* Button
* Input
* Select
* Table
* Tabs
* Dropdown
* Toast

不要为了一个简单按钮创建复杂组件体系。

---

# 26. UI Principles

小镇做题家不是企业后台风格。

整体视觉：

* 简洁
* 温暖
* 有一点“升级打怪”
* 不要过度游戏化
* 不要满屏渐变
* 不要堆卡片
* 信息层级清楚

核心体验：

```text
打开
↓
马上做题
↓
马上得到反馈
```

不要让用户点击 5 层才能开始刷题。

---

# 27. TypeScript Rules

开启 strict mode。

禁止：

```typescript
any
```

除非有明确理由。

API 类型必须统一。

优先：

```text
API Schema
↓
TypeScript Type
```

不要让前端和后端各自猜 API 数据结构。

---

# 28. Testing

V0.1 必须至少覆盖：

### Backend Unit Tests

* submit answer
* correct answer
* wrong answer
* mastery calculation
* review scheduling

### API Tests

* create quiz
* get quiz
* submit answer
* get today's review

### AI

不要依赖真实 LLM API 才能运行测试。

使用 mock provider。

例如：

```text
MockAIProvider
```

---

# 29. Test Philosophy

不要为了 coverage 写没有意义的测试。

优先测试：

```text
业务规则
```

例如：

```text
答对一道题
→ correct_count + 1
→ mastery 更新
→ review 日期更新
```

---

# 30. Logging

使用 Python logging。

关键事件：

```text
quiz_started
answer_submitted
question_generated
ai_explanation_generated
review_completed
```

不要 log：

* API key
* access token
* 用户隐私
* 完整 Prompt（除非 debug 明确需要）

---

# 31. Git Rules

Commit 要小而明确。

推荐：

```text
feat: add quiz session API
feat: add question model
feat: add answer submission
fix: correct review scheduling
refactor: extract AI provider
test: add quiz service tests
```

不要：

```text
feat: finish everything
```

---

# 32. Coding Agent Behavior

执行任务时必须遵循：

1. 先读取 AGENTS.md
2. 读取相关现有代码
3. 不要假设不存在的文件
4. 先理解现有架构
5. 给出简短实施计划
6. 修改代码
7. 运行相关测试
8. 修复失败
9. 检查 lint / type errors
10. 最后总结修改内容

不要在没有必要时重构整个项目。

---

# 33. Avoid Scope Creep

如果当前任务是：

```text
实现 Quiz API
```

不要顺手实现：

* AI
* Redis
* Review
* 用户系统
* Admin Dashboard

除非任务明确要求。

---

# 34. Definition of Done

一个任务只有在以下条件满足时才算完成：

* 代码实现
* 类型检查通过
* lint 通过
* 相关测试通过
* migration 正确（如果涉及数据库）
* API 文档与实现一致
* 没有明显 TODO
* 没有硬编码 secret

---

# 35. Final Rule

当需求存在多个合理实现时：

优先选择：

> 最简单、最容易理解、最容易被未来的 Coding Agent 修改的实现。

这个项目的目标不是展示架构复杂度。

目标是：

> 快速做出一个真的有人愿意每天打开刷 10 道题的产品。
