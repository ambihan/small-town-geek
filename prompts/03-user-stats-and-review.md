# M3 — Knowledge Stats + Review System

阅读：

- AGENTS.md
- 当前 models
- QuizService
- Quiz API
- tests

不要重新设计已有 Quiz API。

---

# Goal

当用户提交一道题后，系统开始真正“记住用户”。

实现：

```text
Answer
 ↓
Knowledge Stats
 ↓
Mastery Score
 ↓
Review Schedule
````

---

# 1. Update Knowledge Stats

提交答案后：

对于题目关联的每个 KnowledgePoint：

```text
attempt_count += 1

correct:
    correct_count += 1

wrong:
    wrong_count += 1
```

---

# 2. Mastery

实现：

```text
correct_rate = correct_count / attempt_count
```

V0.1：

```text
mastery_score = correct_rate
```

先不要复杂化。

确保：

```text
0 <= mastery_score <= 1
```

把算法集中到：

```text
KnowledgeService
```

以后方便替换。

---

# 3. Review Schedule

第一次：

正确：

```text
+1 day
```

第二次：

```text
+3 days
```

第三次：

```text
+7 days
```

第四次：

```text
+14 days
```

第五次：

```text
+30 days
```

答错：

```text
+1 day
```

逻辑集中到：

```text
ReviewService
```

---

# 4. Review API

实现：

```http
GET /api/v1/reviews/today
```

返回当前用户今天需要复习的内容。

返回：

```json
{
  "items": [
    {
      "id": "...",
      "knowledge_point": {
        "id": "...",
        "name": "Python Slice"
      },
      "question_id": "..."
    }
  ]
}
```

---

# 5. Complete Review

实现：

```http
POST /api/v1/reviews/{review_id}/complete
```

完成后：

```text
status = completed
```

---

# 6. Knowledge Stats API

实现：

```http
GET /api/v1/users/me/knowledge-stats
```

返回：

```json
[
  {
    "knowledge_point_id": "...",
    "name": "Python List",
    "attempt_count": 20,
    "correct_count": 16,
    "wrong_count": 4,
    "mastery_score": 0.8,
    "next_review_at": "..."
  }
]
```

---

# 7. Tests

必须测试：

* first correct → +1 day
* second correct → +3 days
* third correct → +7 days
* wrong → +1 day
* mastery calculation
* multiple knowledge points
* today's review
* completed review

---

# 8. Important

不要：

* Redis
* Celery
* ARQ
* pgvector
* AI

保持 PostgreSQL-only。