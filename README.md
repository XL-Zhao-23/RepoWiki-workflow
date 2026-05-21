
````markdown
# RepoWiki Workflow

RepoWiki Workflow 是一个面向代码库的 Wiki 生成工作流。它通过本地脚本扫描代码库、提取结构化上下文、生成标准化 Prompt，并配合 JoyCoder / 龙虾等代码助手生成 MkDocs Wiki 文档。


```text
扫描代码库
→ 提取结构化上下文
→ 生成 Wiki 规划 Prompt
→ 生成页面级 Prompt
→ 使用 JoyCoder / 龙虾生成 Markdown
→ 输出 MkDocs 文档站点
````

该工作流适合在没有大模型 API 的情况下，借助 JoyCoder / 龙虾等代码助手，为 Java 后端项目生成结构化、可维护、可浏览的项目 Wiki。

---

## 核心定位

Repo Wiki Manual 的定位是：

> 一个 Human-in-the-loop 的 Codebase Wiki Generation Workflow。

中文可以理解为：

> 人在回路的代码库 Wiki 生成工作流。

它将确定性的工程工作交给本地脚本完成，将需要理解和生成的工作交给 JoyCoder / 龙虾完成。

本地脚本负责：

```text
扫描代码
提取结构
整理上下文
生成 Prompt
组织输出目录
```

JoyCoder / 龙虾负责：

```text
理解代码上下文
规划 Wiki 结构
生成 Markdown 页面
生成 Mermaid 图
根据构建结果修正文档
```

---

## Features

* 扫描目标代码库并生成目录树
* 提取 Java 项目的类、方法、注解、import 信息
* 识别常见 Spring 分层组件，例如 Controller、Service、Mapper、Configuration
* 提取 README、pom.xml、application.yml 等关键文件摘要
* 生成项目级 Wiki 规划 Prompt
* 生成页面级 Wiki 写作 Prompt
* 支持 JoyCoder / 龙虾逐页生成 Markdown 文档
* 支持页面级上下文隔离，减少页面之间的信息污染
* 支持输出 MkDocs 兼容的 Wiki 文档目录
* 适合无大模型 API 场景下的半自动代码库文档生成

---

## Workflow Overview

```text
Target Repository
        │
        ▼
scanner.py
        │
        ├── repo_tree.md
        ├── files_index.json
        ├── java_symbols.json
        ├── important_files.json
        └── scan_summary.json
        │
        ▼
prompt_builder.py plan
        │
        ▼
00_wiki_plan.prompt.md
        │
        ▼
JoyCoder / 龙虾
        │
        ▼
wiki_plan.json
        │
        ▼
prompt_builder.py pages
        │
        ▼
prompts/pages/*.prompt.md
        │
        ▼
JoyCoder / 龙虾
        │
        ▼
output/wiki_docs/*.md
        │
        ▼
MkDocs
        │
        ▼
Browsable Project Wiki
```

---

## Core Concepts

### 1. Codebase Scanning

`scanner.py` 负责扫描目标代码库，并把原始代码转换成结构化中间文件。

输出包括：

```text
repo_tree.md              # 项目目录树
files_index.json          # 文件索引
java_symbols.json         # Java 类、方法、注解、import 等结构信息
important_files.json      # README、pom.xml、配置文件等摘要
scan_summary.json         # 扫描统计信息
```

这一步的目标不是生成最终文档，而是把代码库压缩成大模型更容易理解的上下文材料。

---

### 2. Wiki Planning

`prompt_builder.py plan` 会读取扫描结果，生成项目级 Wiki 规划 Prompt：

```text
prompts/00_wiki_plan.prompt.md
```

该 Prompt 交给 JoyCoder / 龙虾处理后，应生成：

```text
wiki_plan.json
```

`wiki_plan.json` 用于描述整个 Wiki 的页面结构，例如：

```text
项目总览
系统架构
模块说明
接口说明
配置说明
部署说明
常见问题
```

它决定后续要生成哪些页面、每个页面参考哪些源码路径、每个页面应该包含哪些章节。

---

### 3. Page-level Prompt Generation

`prompt_builder.py pages` 会读取 `wiki_plan.json`，并为每个 Wiki 页面生成独立 Prompt：

```text
prompts/pages/
├── overview.prompt.md
├── architecture.prompt.md
├── modules__order.prompt.md
└── modules__cache.prompt.md
```

每个页面 Prompt 都会包含当前页面需要的代码上下文、相关类、相关配置文件摘要和写作要求。

文件名中的双下划线 `__` 用于表示目录层级：

```text
modules__order.prompt.md
→ modules/order.md
```

---

### 4. JoyCoder-assisted Wiki Generation

JoyCoder / 龙虾负责读取页面 Prompt，并生成最终 Markdown 文档。

输入：

```text
prompts/pages/*.prompt.md
```

输出：

```text
output/wiki_docs/*.md
```

示例：

```text
prompts/pages/overview.prompt.md
→ output/wiki_docs/overview.md

prompts/pages/modules__order.prompt.md
→ output/wiki_docs/modules/order.md
```

---

### 5. Context Isolation

页面生成阶段必须保持上下文隔离。

这并不是清空所有上下文，而是：

```text
保留：
- 总控提示词
- 页面处理规则
- 当前页面 Prompt

隔离：
- 上一个页面的正文
- 上一个页面的模块判断
- 上一个页面的调用链推断
- 上一个页面的不确定项
- 上一个页面的措辞和结构细节
```

每个页面只能基于当前 `.prompt.md` 文件中的内容生成。

如果当前页面信息不足，应明确写：

```text
需要人工确认
```

不要从其他页面借用信息，也不要编造不存在的模块、类、方法或调用链。

---

### 6. Quality First

重要说明：不要为了节省上下文而选择短输出。宁可分批次处理，也必须保证质量优先，否则生成 Wiki 的工作将毫无意义。

本工具的目标不是快速生成一批形式化 Markdown，而是产出能够帮助研发人员理解代码库的高质量 Wiki。

JoyCoder / 龙虾在执行页面生成任务时，必须优先保证：

```text
内容完整
依据明确
结构清晰
模块关系准确
不确定项显式标注
不因上下文限制而省略关键分析
```

如果当前页面内容过多，应拆分页面、分批生成或保留明确的续写边界，不要用简略总结替代深入分析。

---

## Quick Start

### 1. 扫描代码库

```bash
python scanner.py /path/to/project --out work/my_project
```

生成：

```text
work/my_project/
├── repo_tree.md
├── files_index.json
├── java_symbols.json
├── important_files.json
└── scan_summary.json
```

---

### 2. 生成 Wiki 规划 Prompt

```bash
python prompt_builder.py plan --work work/my_project
```

生成：

```text
work/my_project/prompts/00_wiki_plan.prompt.md
```

将该文件内容复制给 JoyCoder / 龙虾。

JoyCoder / 龙虾 应返回严格 JSON，并保存为：

```text
work/my_project/wiki_plan.json
```

---

### 3. 生成页面级 Prompt

```bash
python prompt_builder.py pages --work work/my_project
```

生成：

```text
work/my_project/prompts/pages/
├── overview.prompt.md
├── architecture.prompt.md
└── modules__xxx.prompt.md
```

---

### 4. 逐页生成 Wiki Markdown

将 `prompts/pages/` 下的 `.prompt.md` 文件逐个交给 JoyCoder / 龙虾处理。

生成结果保存到：

```text
work/my_project/output/wiki_docs/
```

示例：

```text
work/my_project/output/wiki_docs/
├── index.md
├── overview.md
├── architecture.md
└── modules/
    └── xxx.md
```

---

### 5. 使用 MkDocs 预览

```bash
cp mkdocs.yml work/my_project/output/mkdocs.yml
cd work/my_project/output
mkdocs serve
```

如果 `mkdocs.yml` 使用自定义文档目录，请确保配置：

```yaml
docs_dir: wiki_docs
```

---

## Recommended Project Layout

```text
repo_wiki_manual/
├── README.md
├── scanner.py
├── prompt_builder.py
├── mkdocs.yml
├── requirements.txt
├── templates/
│   ├── manual_workflow.md
│   └── wiki_plan_example.json
└── work/
    └── my_project/
        ├── repo_tree.md
        ├── files_index.json
        ├── java_symbols.json
        ├── important_files.json
        ├── scan_summary.json
        ├── wiki_plan.json
        ├── prompts/
        │   ├── 00_wiki_plan.prompt.md
        │   └── pages/
        │       ├── overview.prompt.md
        │       ├── architecture.prompt.md
        │       └── modules__xxx.prompt.md
        └── output/
            ├── mkdocs.yml
            └── wiki_docs/
                ├── index.md
                ├── overview.md
                ├── architecture.md
                └── modules/
                    └── xxx.md
```

---

## Using with JoyCoder

如果将本工具放到目标项目根目录下，推荐结构如下：

```text
project/
├── repo_wiki_manual/
│   ├── scanner.py
│   ├── prompt_builder.py
│   ├── mkdocs.yml
│   └── ...
├── src/
├── pom.xml
├── README.md
└── ...
```

执行扫描时，需要避免把 `repo_wiki_manual/` 自身当成业务代码分析。

推荐命令：

```bash
python repo_wiki_manual/scanner.py . --out repo_wiki_manual/work/project
python repo_wiki_manual/prompt_builder.py plan --work repo_wiki_manual/work/project
```

然后由 JoyCoder 读取：

```text
repo_wiki_manual/work/project/prompts/00_wiki_plan.prompt.md
```

生成并保存：

```text
repo_wiki_manual/work/project/wiki_plan.json
```

继续执行：

```bash
python repo_wiki_manual/prompt_builder.py pages --work repo_wiki_manual/work/project
```

然后逐页处理：

```text
repo_wiki_manual/work/project/prompts/pages/*.prompt.md
```

最终输出：

```text
repo_wiki_manual/work/project/output/wiki_docs/
```

---

## What This Workflow Can Do

Repo Wiki Manual 当前适合完成：

```text
代码库结构梳理
Java 后端项目 Wiki 生成
模块职责说明
系统架构说明
配置文件说明
Controller / Service / Mapper 基础结构梳理
项目 onboarding 文档生成
无大模型 API 条件下的半自动文档生成
JoyCoder / 龙虾辅助代码库理解
```

---

## What This Workflow Does Not Do Yet

当前版本暂不支持：

```text
自动调用大模型 API
向量库 / embedding / RAG
完整方法调用链分析
完整数据库表关系分析
Redis key 专门提取
MQ topic 专门提取
自动增量更新
断点续跑
任务状态管理
自动链接校验
自动修复 MkDocs 构建错误
多语言深度 AST 解析
```

这些能力可以作为后续迭代方向。

---

## Design Philosophy

Repo Wiki Manual 的设计原则是：

> Deterministic first, generative second.

也就是：

确定性的部分由脚本完成：

```text
扫描文件
提取结构
生成索引
组织 Prompt
管理输出路径
```

生成性的部分由 JoyCoder / 龙虾完成：

```text
理解上下文
判断模块职责
生成文档内容
绘制 Mermaid 图
补充阅读说明
```

这样做的好处是：

```text
不依赖大模型 API
流程可检查
中间产物可追踪
Prompt 可复用
生成结果可人工校验
适合公司内部代码助手环境
```

---

## Roadmap

* 自动生成 MkDocs nav
* 增加 Java Controller 路由表提取
* 增加 Spring Bean 依赖图
* 增加 Controller → Service → Mapper 调用链分析
* 增加 Redis key / MQ topic 提取
* 增加 Git diff 增量更新
* 增加任务 manifest 和断点续跑
* 增加 Markdown 链接检查
* 增加 MkDocs build 自动校验
* 增加本地模型或 API 调用模式

```
```
