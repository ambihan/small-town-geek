# M1 — Database + Domain Models

你现在负责实现「小镇做题家」V0.1 的数据库模型。

先阅读：

- AGENTS.md
- docs/product.md（如果存在）
- docs/architecture.md（如果存在）
- 当前 backend 代码

不要破坏已经完成的 M0。

---

# Goal

实现 V0.1 核心数据库模型和 Alembic migration。

---

# 1. Models

创建以下 SQLAlchemy 2.x models：

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
````

---

# 2. User

字段：

```text
id UUID PK
openid VARCHAR UNIQUE
nickname VARCHAR
avatar_url VARCHAR NULL
created_at
updated_at
```

要求：

* UUID
* timezone-aware timestamps
* created_at / updated_at

---

# 3. Question

字段：

```text
id UUID PK
content TEXT
type VARCHAR
difficulty SMALLINT
answer JSONB
explanation TEXT
status VARCHAR
source VARCHAR NULL
created_at
updated_at
```

V0.1 type：

```text
single_choice
```

difficulty：

```text
1 ~ 5
```

status：

```text
draft
published
archived
```

增加合理 database constraints。

---

# 4. QuestionOption

字段：

```text
id UUID PK
question_id FK
key VARCHAR
content TEXT
sort_order INTEGER
```

Question 删除时：

```text
cascade
```

---

# 5. KnowledgePoint

字段：

```text
id UUID PK
name VARCHAR
description TEXT
parent_id UUID NULL
created_at
updated_at
```

parent_id 指向：

```text
knowledge_points.id
```

实现 self-referential relationship。

---

# 6. QuestionKnowledgePoint

many-to-many：

```text
question_id
knowledge_point_id
```

主键：

```text
(question_id, knowledge_point_id)
```

---

# 7. QuizSession

字段：

```text
id UUID PK
user_id FK
mode VARCHAR
total_count INTEGER
completed_count INTEGER
started_at
completed_at NULL
```

mode：

```text
daily
practice
review
```

---

# 8. QuizAnswer

字段：

```text
id UUID PK
session_id FK
user_id FK
question_id FK
answer JSONB
is_correct BOOLEAN
time_spent_ms INTEGER NULL
answered_at
```

---

# 9. UserKnowledgeStat

字段：

```text
id UUID PK
user_id FK
knowledge_point_id FK

attempt_count INTEGER
correct_count INTEGER
wrong_count INTEGER

mastery_score FLOAT

last_attempt_at NULL
next_review_at NULL
```

增加：

```text
unique(user_id, knowledge_point_id)
```

mastery_score：

```text
0.0 ~ 1.0
```

---

# 10. ReviewItem

字段：

```text
id UUID PK
user_id FK
knowledge_point_id FK
question_id FK NULL

scheduled_at
status
review_count
created_at
updated_at
```

status：

```text
pending
completed
```

---

# 11. Indexes

合理添加：

```text
questions.status
questions.difficulty

knowledge_points.parent_id

quiz_answers.user_id
quiz_answers.question_id
quiz_answers.answered_at

user_knowledge_stats.user_id
user_knowledge_stats.knowledge_point_id

review_items.user_id
review_items.scheduled_at
review_items.status
```

不要无脑给所有字段加 index。

---

# 12. Alembic

生成 migration。

确认：

```bash
alembic upgrade head
```

可以成功执行。

然后：

```bash
alembic downgrade -1
alembic upgrade head
```

都必须成功。

---

# 13. Tests

至少测试：

* model metadata 能正常加载
* migration 能成功执行
* 主要 relationships 正确
* unique constraint 存在

---

# 14. Quality Gate

运行：

```bash
ruff check .
pytest
```

修复错误。

---

# 15. Important

不要实现：

* Quiz Service
* AI
* Review Algorithm
* API
* Admin UI

这些属于后续 Milestones。

当前任务只负责数据库 Domain Layer。