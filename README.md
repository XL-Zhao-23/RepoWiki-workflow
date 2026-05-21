
# 📚 RepoWiki Kit

> **A Codebase Wiki Generation Skill & Toolkit for AI Agents**  
> 为 AI Agent 提供的代码库 Wiki 生成 Skill 与工具包。

RepoWiki Kit 是一个面向 AI Agent 的代码库 Wiki 生成 **Skill + 工具包**。

它将可执行提示词、上下文管理规则、本地扫描脚本、Prompt 生成器和 MkDocs 输出规范组合在一起，使 AI Agent 能够按照既定流程读取代码库、提取结构化上下文、规划 Wiki、生成页面文档，并最终构建出一个可浏览的项目 Wiki。

---

## ✨ What is RepoWiki Kit?

RepoWiki Kit 不是一个单纯的脚本工具，也不是一组零散 Prompt。

它由两部分组成：

| 组成 | 作用 |
|---|---|
| **Skill** | 定义 AI Agent 如何执行代码库 Wiki 生成任务，包括总控提示词、页面处理规则、上下文隔离策略和质量优先原则 |
| **Toolkit** | 提供本地脚本和工程化能力，包括代码扫描、结构提取、Prompt 生成、输出目录组织和 MkDocs 构建支持 |

换句话说：

```text
Skill 负责告诉 AI Agent 怎么做
Toolkit 负责提供 AI Agent 执行任务所需的工具
````

AI Agent 只需要按照总控提示词执行，即可完成从代码库扫描到 Wiki 输出的完整过程。

---

## 🧭 Why RepoWiki Kit?

很多代码库并不缺代码，缺的是一套能帮助人快速理解系统的结构化文档。

RepoWiki Kit 的目标不是生成一份简单 README，而是帮助 AI Agent 将代码库转化为一套可浏览、可维护、可继续迭代的项目 Wiki：

* 🧭 项目总览
* 🏗️ 系统架构
* 🧩 模块说明
* 🔎 关键类与方法说明
* ⚙️ 配置说明
* 📈 Mermaid 架构图与流程图

它适合用于：

* 快速理解陌生代码库
* 为 Java 后端项目生成内部 Wiki
* 辅助新人 onboarding
* 将代码扫描、Prompt 编排、AI Agent 执行和 MkDocs 输出串成稳定流程
* 为 AI Agent 提供可复用的代码库文档生成能力

---

## 🧠 How It Works

```text
Target Repository
        │
        ▼
RepoWiki Kit
        │
        ├── Skill
        │   ├── run_repo_wiki.prompt.md
        │   ├── page generation rules
        │   ├── context isolation rules
        │   └── quality-first rules
        │
        └── Toolkit
            ├── scanner.py
            ├── prompt_builder.py
            └── mkdocs.yml
        │
        ▼
AI Agent
        │
        ├── runs local scripts
        ├── reads generated prompts
        ├── creates wiki_plan.json
        └── writes Wiki Markdown pages
        │
        ▼
MkDocs
        │
        ▼
Browsable Codebase Wiki
```

RepoWiki Kit 将任务分为三类：

| 类型    | 负责方      | 说明                                     |
| ----- | -------- | -------------------------------------- |
| 确定性任务 | Toolkit  | 扫描代码、提取结构、生成 Prompt、组织输出路径             |
| 生成性任务 | AI Agent | 理解上下文、规划 Wiki、生成 Markdown、绘制 Mermaid 图 |
| 展示任务  | MkDocs   | 将 Markdown 渲染为可浏览的文档站点                 |

---

## 🚀 Features

* 📁 代码库目录扫描
* ☕ Java 类、方法、注解、`import` 信息提取
* 🌱 Spring `Controller` / `Service` / `Mapper` / `Configuration` 分层识别
* 📄 `README`、`pom.xml`、配置文件摘要提取
* 🧭 项目级 Wiki 规划 Prompt 生成
* 🧩 页面级 Wiki Prompt 生成
* 🧱 页面上下文隔离，减少生成污染
* 🎯 质量优先规则，避免低质量短输出
* 📝 Markdown Wiki 输出
* 🌐 MkDocs 文档站点构建
* 🤖 面向 AI Agent 执行

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

然后让 AI Agent 执行：

```text
repo_wiki_kit/run_repo_wiki.prompt.md
```

AI Agent 会按照总控提示词完成：

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

RepoWiki Kit 的 Skill 部分强调 **页面级上下文隔离**。

生成每个 Wiki 页面时，AI Agent 只应使用：

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

如果当前页面信息不足，应明确标注：

```text
需要人工确认
```

而不是猜测或编造。

---

## 🎯 Quality First

> 重要说明：不要为了节省上下文而选择短输出。宁可分批次处理，也必须保证质量优先，否则生成 Wiki 的工作将毫无意义。

RepoWiki Kit 追求的是能帮助研发人员理解代码库的高质量 Wiki，而不是形式化的 Markdown 堆叠。

如果上下文过长，AI Agent 应：

* 拆分页面
* 分批生成
* 明确续写边界
* 标注“需要人工确认”
* 保留关键源码依据和模块关系

不要用粗略总结替代关键分析。

---

## 🧬 What It Is

RepoWiki Kit is:

```text
AI-agent-ready
Skill-based
Toolkit-backed
Prompt-driven
Codebase-aware
MkDocs-based
Human-in-the-loop
```

它的核心不是“自动生成一份文档”，而是为 AI Agent 提供一套可执行、可检查、可复用的代码库 Wiki 生成能力。

---

## 🗂️ Project Structure

```text
repo_wiki_kit/
├── README.md
├── scanner.py
├── prompt_builder.py
├── run_repo_wiki.prompt.md
├── run_pages_to_wiki.prompt.md
├── mkdocs.yml
├── requirements.txt
└── templates/
    ├── manual_workflow.md
    └── wiki_plan_example.json
```

核心文件说明：

| 文件                            | 作用                                  |
| ----------------------------- | ----------------------------------- |
| `run_repo_wiki.prompt.md`     | AI Agent 执行完整 Wiki 生成任务的总控提示词       |
| `run_pages_to_wiki.prompt.md` | 页面级 Prompt 批量处理规则                   |
| `scanner.py`                  | 扫描代码库，提取目录树、Java 符号和重要文件摘要          |
| `prompt_builder.py`           | 根据扫描结果生成 Wiki 规划 Prompt 和页面级 Prompt |
| `mkdocs.yml`                  | MkDocs 文档站点配置                       |
| `templates/`                  | 示例模板和参考文件                           |

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


