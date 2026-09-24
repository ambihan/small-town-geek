# M6 — Next.js Admin

阅读：

- AGENTS.md
- 当前 backend API
- 当前 web

---

# Goal

建立「小镇做题家」Web 管理后台。

Web V0.1 不是用户刷题端。

它主要用于：

- 题库管理
- 知识点管理
- AI 出题
- 用户数据查看

---

# Routes

```text
/admin
/admin/questions
/admin/questions/new
/admin/questions/[id]
/admin/knowledge-points
/admin/ai/generate
/admin/users
````

---

# Dashboard

显示：

```text
题目数量
知识点数量
用户数量
今日答题数
```

数据从 Backend 获取。

如果对应 API 尚未实现：

不要伪造复杂数据。

可以暂时显示：

```text
Coming soon
```

---

# Question List

支持：

* 搜索
* difficulty filter
* status filter
* pagination

表格显示：

```text
题目
知识点
难度
状态
创建时间
操作
```

---

# Question Editor

支持：

* content
* options
* answer
* explanation
* difficulty
* knowledge points
* status

使用 shadcn/ui。

---

# AI Generate

页面：

```text
知识点
难度
生成数量

[生成]
```

生成后展示 preview。

不要默认直接发布。

状态：

```text
draft
```

管理员确认后：

```text
published
```

---

# UX

不要做成密密麻麻的企业后台。

优先：

* 清晰
* 快速
* 表单简单
* preview 明确

---

# Quality

运行：

```bash
npm run lint
npm run build
```

修复所有 blocking errors。
