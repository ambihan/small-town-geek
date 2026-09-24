# M5 — Taro Mini Program

阅读：

- AGENTS.md
- 当前 backend API
- 当前 miniapp

---

# Goal

把小程序从 mock UI 连接到真实 API。

---

# Pages

实现：

```text
首页
刷题
错题
学习
我的
````

---

# Home

调用：

```text
GET /api/v1/reviews/today
GET /api/v1/users/me/knowledge-stats
```

显示：

* 今日训练
* 今日进度
* 待复习知识点
* 连续学习天数（如果后端还没有，可以暂时 mock）

---

# Quiz

流程：

```text
创建 session
↓
获取 session
↓
显示题目
↓
选择答案
↓
提交
↓
显示结果
↓
下一题
```

必须支持：

* loading
* error
* submitting
* answered
* completed

避免重复提交。

---

# Answer Result

正确：

```text
✅ 回答正确
```

错误：

```text
❌ 答错了

正确答案：B
```

显示：

```text
AI 解析
```

如果 AI explanation 尚未完成，可以先显示普通 explanation。

---

# Learning

显示：

```text
知识点
掌握度
正确率
答题次数
下次复习
```

使用进度条。

---

# Mistakes

展示用户做错过的题。

V0.1 可以直接从：

```text
QuizAnswer.is_correct = false
```

查询。

不需要单独创建 Mistake 表。

---

# UI

风格：

* 简洁
* 温暖
* 少量游戏化
* 移动端优先
* 不要复杂动画

核心按钮：

```text
开始训练
提交答案
下一题
```

必须明显。

---

# API Layer

创建：

```text
src/services/api.ts
src/services/quiz.ts
src/services/knowledge.ts
src/services/review.ts
```

页面不要直接发 HTTP 请求。

---

# State

如果当前项目没有必要引入 Zustand / Redux：

不要添加。

优先：

```text
React state
```

---

# TypeScript

禁止：

```typescript
any
```

API response 创建明确类型。

---

# Quality

运行项目自己的：

```bash
typecheck
lint
build
```

如果没有这些 scripts，补充合理 scripts。