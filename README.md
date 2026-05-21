# 📚 RepoWiki Kit

> **AI-assisted Codebase Wiki Generator**  
> Put it in your repository, run the control prompt, get a browsable codebase Wiki.

RepoWiki Kit 是一个 **AI 辅助的代码库 Wiki 生成工具包**。

它通过本地脚本扫描代码库、提取结构化上下文、生成标准化 Prompt，并引导 AI 编程助手执行完整的 Wiki 生成流程，最终产出一个基于 **MkDocs** 的项目文档站点。

---

## ✨ Why RepoWiki Kit?

很多代码库并不缺代码，缺的是一套能帮助人快速理解系统的文档。

RepoWiki Kit 的目标不是生成一份简单 README，而是将代码库转化为结构化 Wiki：

- 🧭 项目总览
- 🏗️ 系统架构
- 🧩 模块说明
- 🔎 关键类与方法说明
- ⚙️ 配置说明
- 📈 Mermaid 架构图与流程图

它特别适合：

- 快速理解陌生代码库
- 为 Java 后端项目生成内部 Wiki
- 辅助新人 onboarding
- 没有大模型 API，但可以使用 AI 编程助手的场景
- 将代码分析、Prompt 编排和 MkDocs 文档输出串成稳定流程

---

## 🧠 How It Works

```text
Target Repository
        │
        ▼
Local Scanner
        │
        ├── repo_tree.md
        ├── java_symbols.json
        ├── important_files.json
        └── scan_summary.json
        │
        ▼
Prompt Builder
        │
        ├── 00_wiki_plan.prompt.md
        └── pages/*.prompt.md
        │
        ▼
AI Coding Assistant
        │
        ├── wiki_plan.json
        └── Wiki Markdown Pages
        │
        ▼
MkDocs
        │
        ▼
Browsable Codebase Wiki
````

RepoWiki Kit 将任务分为两类：

| 类型    | 负责方     | 说明                                     |
| ----- | ------- | -------------------------------------- |
| 确定性任务 | 本地脚本    | 扫描代码、提取结构、生成 Prompt、组织输出路径             |
| 生成性任务 | AI 编程助手 | 理解上下文、规划 Wiki、生成 Markdown、绘制 Mermaid 图 |
| 展示任务  | MkDocs  | 将 Markdown 渲染为可浏览的文档站点                 |

---

## 🚀 Features

* 📁 代码库目录扫描
* ☕ Java 类、方法、注解、`import` 信息提取
* 🌱 Spring `Controller` / `Service` / `Mapper` / `Configuration` 分层识别
* 📄 `README`、`pom.xml`、配置文件摘要提取
* 🧭 项目级 Wiki 规划 Prompt 生成
* 🧩 页面级 Wiki Prompt 生成
* 🧱 页面上下文隔离，减少生成污染
* 📝 Markdown Wiki 输出
* 🌐 MkDocs 文档站点构建
* 🤖 适配 AI 编程助手执行，无需大模型 API

---

## ⚡ Quick Start

将本工具放入目标项目根目录：

```text
your-project/
├── repo_wiki_kit/
│   ├── scanner.py
│   ├── prompt_builder.py
│   ├── run_repo_wiki.prompt.md
│   └── mkdocs.yml
├── src/
├── pom.xml
└── README.md
```

然后让 AI 编程助手执行：

```text
repo_wiki_kit/run_repo_wiki.prompt.md
```

它会按照总控提示词完成：

```text
扫描代码库
→ 生成结构化上下文
→ 生成 Wiki 规划
→ 生成页面 Prompt
→ 逐页生成 Markdown
→ 输出 MkDocs Wiki
→ 检查构建结果
```

最终输出目录：

```text
repo_wiki_kit/work/project/output/wiki_docs/
```

预览 Wiki：

```bash
cd repo_wiki_kit/work/project/output
mkdocs serve
```

---

## 📦 Output Example

```text
output/
├── mkdocs.yml
└── wiki_docs/
    ├── index.md
    ├── overview.md
    ├── architecture.md
    ├── configuration.md
    └── modules/
        ├── order.md
        ├── user.md
        └── cache.md
```

---

## 🧱 Context Isolation

RepoWiki Kit 强调 **页面级上下文隔离**。

生成每个 Wiki 页面时，只应使用：

```text
总控规则
+ 当前页面 Prompt
+ 当前页面所需源码上下文
```

禁止把上一个页面的正文、判断、推断或不确定项带入当前页面。

这可以减少：

* 幻觉
* 重复
* 跨页面污染
* 模块职责混淆
* 调用链误推断

---

## 🎯 Quality First

> 重要说明：不要为了节省上下文而选择短输出。宁可分批次处理，也必须保证质量优先，否则生成 Wiki 的工作将毫无意义。

RepoWiki Kit 追求的是能帮助研发人员理解代码库的高质量 Wiki，而不是形式化的 Markdown 堆叠。

如果上下文过长，应：

* 拆分页面
* 分批生成
* 明确续写边界
* 标注“需要人工确认”

不要用粗略总结替代关键分析。

---

## 🧬 What It Is

RepoWiki Kit is:

```text
AI-assisted
Prompt-driven
Codebase-aware
MkDocs-based
Human-in-the-loop
```

它不是一个完全自动调用大模型 API 的平台，而是一个适合 AI 编程助手执行的代码库 Wiki 生成工具包。

---

## 🗺️ Roadmap

* 自动生成 MkDocs nav
* Java 路由表提取
* Spring Bean 依赖图
* Controller → Service → Mapper 调用链分析
* Redis key / MQ topic 提取
* Git diff 增量更新
* 任务 manifest 与断点续跑
* Markdown 链接检查
* 本地模型 / API 执行模式

---

## 📄 License

MIT

```
