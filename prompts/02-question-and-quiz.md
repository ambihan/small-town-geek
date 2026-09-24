# M2 — Question + Quiz Core

先阅读：

- AGENTS.md
- 当前数据库 models
- 当前 Alembic migrations
- 当前 FastAPI structure

不要重构已有架构。

---

# Goal

实现「小镇做题家」核心刷题 API。

用户必须能够：

1. 获取题目
2. 创建一次训练
3. 获取训练题目
4. 提交答案
5. 获得正确/错误结果
6. 查看训练进度

---

# 1. Question API

实现：

```http
GET /api/v1/questions/{question_id}
````

返回：

```json
{
  "id": "...",
  "content": "...",
  "type": "single_choice",
  "difficulty": 2,
  "options": [
    {
      "key": "A",
      "content": "..."
    }
  ]
}
```

注意：

普通用户获取题目时：

**不要返回 answer。**

---

# 2. Quiz API

实现：

```http
POST /api/v1/quiz/sessions
```

request：

```json
{
  "mode": "daily",
  "count": 10
}
```

response：

```json
{
  "id": "...",
  "mode": "daily",
  "total_count": 10,
  "completed_count": 0
}
```

---

# 3. Question Selection

V0.1 先实现简单规则：

1. status = published
2. 排除用户最近做过的题
3. 优先选择 difficulty 2~3
4. 随机选择
5. 不足时允许重复

不要实现 AI recommendation。

---

# 4. Get Session

实现：

```http
GET /api/v1/quiz/sessions/{session_id}
```

返回：

```json
{
  "id": "...",
  "mode": "daily",
  "total_count": 10,
  "completed_count": 3,
  "questions": []
}
```

不要返回答案。

---

# 5. Submit Answer

实现：

```http
POST /api/v1/quiz/sessions/{session_id}/answers
```

request：

```json
{
  "question_id": "...",
  "answer": "B",
  "time_spent_ms": 12000
}
```

response：

```json
{
  "question_id": "...",
  "is_correct": true,
  "correct_answer": "B",
  "explanation": "...",
  "completed_count": 4,
  "total_count": 10
}
```

---

# 6. Business Rules

提交答案必须：

1. 验证 session 存在
2. 验证 session 属于当前用户
3. 验证 question 属于 session
4. 验证 answer 合法
5. 判断正确性
6. 创建 QuizAnswer
7. 更新 completed_count
8. 使用 transaction

重复提交同一道题：

V0.1 禁止。

返回：

```text
QUESTION_ALREADY_ANSWERED
```

---

# 7. Quiz Completion

当：

```text
completed_count == total_count
```

自动：

```text
completed_at = now
```

---

# 8. Service Layer

至少：

```text
QuizService
QuestionService
```

Router 不允许包含核心业务逻辑。

---

# 9. Tests

必须测试：

### Happy path

```text
create session
→ get session
→ submit answer
→ progress +1
```

### Wrong answer

验证：

```text
is_correct = false
```

### Unauthorized session

不能访问其他用户的 session。

### Question not in session

返回明确错误。

### Duplicate answer

第二次提交失败。

### Completion

最后一道题提交后：

```text
completed_at != null
```

---

# 10. Quality Gate

运行：

```bash
ruff check .
pytest
```

确保通过。

不要实现 AI。
