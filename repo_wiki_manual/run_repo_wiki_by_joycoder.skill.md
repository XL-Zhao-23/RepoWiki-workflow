````markdown

# Quality First

重要说明：不要为了节省上下文，选择短输出。宁可分批次处理，也要质量优先。  
如果为了压缩上下文而省略关键分析、源码依据、模块关系或实现细节，那么生成的 Wiki 将失去实际价值。

在使用 JoyCoder / 龙虾生成 Wiki 页面时，应遵循以下原则：

- 优先保证内容完整性和准确性；
- 不要为了“一次生成完”而牺牲页面质量；
- 如果单个页面内容过长，应拆分为多个子页面或分批生成；
- 每个页面都应包含足够的源码路径、关键类、关键方法和不确定项说明；
- 对于架构、调用链、模块职责等内容，宁可明确写“需要人工确认”，也不要模糊带过或编造。

# 任务：在当前项目根目录中执行 repo_wiki_manual 工具，生成代码库 Wiki

你现在是一个代码库 Wiki 生成执行器。请在当前工程目录中，按照本总控提示词执行任务。

重要说明：本总控提示词是全局规则，必须在整个任务过程中始终保留。不要清空、忽略或覆盖本总控提示词。所谓“上下文隔离”，只针对不同 Wiki 页面之间的页面生成上下文，不针对本总控提示词。


## 一、当前目录约定

当前工程根目录是：

```text
project/
````

在 `project/` 目录下，已经包含代码库本身，也包含 Wiki 工具目录：

```text
project/
├── repo_wiki_manual/
│   ├── scanner.py
│   ├── prompt_builder.py
│   ├── mkdocs.yml
│   ├── run_pages_to_wiki.prompt.md
│   └── ...
├── src/
├── pom.xml
├── README.md
└── ...
```

其中：

* `project/` 是需要分析的代码库根目录；
* `project/repo_wiki_manual/` 是 Wiki 生成工具目录；
* `project/repo_wiki_manual/run_pages_to_wiki.prompt.md` 是页面批量生成提示词；
* 你需要使用已有 Python 环境和 MkDocs 环境，不要安装依赖，不要执行 `pip install`。

## 二、总体目标

请完成以下工作：

1. 使用 `repo_wiki_manual/scanner.py` 扫描当前代码库；
2. 使用 `repo_wiki_manual/prompt_builder.py` 生成 Wiki 规划提示词；
3. 读取生成的 `00_wiki_plan.prompt.md`，根据其中要求生成 `wiki_plan.json`；
4. 使用 `repo_wiki_manual/prompt_builder.py` 根据 `wiki_plan.json` 生成页面级 Prompt；
5. 读取 `repo_wiki_manual/run_pages_to_wiki.prompt.md`；
6. 按照该提示词逐一处理 `pages/` 下的 `.prompt.md` 文件；
7. 将最终 Wiki Markdown 保存到 `output/wiki_docs/`；
8. 输出处理汇总。

## 三、必须排除的目录

扫描项目代码时，不要把 Wiki 工具自身当成业务代码分析。

也就是说，分析 `project/` 时，应排除：

```text
repo_wiki_manual/
```

还应排除常见无关目录：

```text
.git/
.idea/
.vscode/
target/
build/
dist/
node_modules/
.gradle/
.mvn/
out/
__pycache__/
.venv/
logs/
```

如果当前 `scanner.py` 还没有排除 `repo_wiki_manual/`，请先修改 `scanner.py`，把 `repo_wiki_manual` 加入 `IGNORE_DIRS`。

修改目标类似：

```python
IGNORE_DIRS = {
    ".git", ".idea", ".vscode", "target", "build", "dist", "node_modules",
    ".gradle", ".mvn", "out", "__pycache__", ".venv", "logs",
    "repo_wiki_manual"
}
```

## 四、工作目录约定

请把所有中间产物和最终结果都放到：

```text
project/repo_wiki_manual/work/project/
```

最终 Wiki 文档保存到：

```text
project/repo_wiki_manual/work/project/output/wiki_docs/
```

也就是说，最终目录应类似：

```text
project/repo_wiki_manual/work/project/
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
│       └── ...
└── output/
    └── wiki_docs/
        ├── index.md
        ├── overview.md
        ├── architecture.md
        └── ...
```

## 五、执行步骤

执行过程中必须管理上下文。

重要原则：

1. 每一个 Step 都必须独立执行。
2. 每一个 Step 开始前，都不要依赖上一个 Step 的对话记忆。
3. 每一个 Step 需要什么输入，就必须从本提示词指定的文件路径重新读取。
4. 不要说“根据上一步结果继续”，而要明确读取对应文件。
5. 本总控提示词始终保留；隔离的是步骤之间的临时推理和页面生成内容。
6. 如果某一步需要前一步产物，必须从磁盘上的产物文件读取，而不是从对话上下文中回忆。

请在 `project/` 根目录下执行。

### Step 1：确认当前目录

先确认当前目录是项目根目录，应该能看到：

```text
repo_wiki_manual/
```

以及业务代码文件，例如：

```text
src/
pom.xml
README.md
```

如果当前不在 `project/` 根目录，请切换到 `project/` 根目录后再继续。

### Step 2：扫描代码库

执行：

```bash
python repo_wiki_manual/scanner.py . --out repo_wiki_manual/work/project
```

扫描完成后，确认生成以下文件：

```text
repo_wiki_manual/work/project/repo_tree.md
repo_wiki_manual/work/project/files_index.json
repo_wiki_manual/work/project/java_symbols.json
repo_wiki_manual/work/project/important_files.json
repo_wiki_manual/work/project/scan_summary.json
```

### Step 3：生成 Wiki 规划 Prompt

执行：

```bash
python repo_wiki_manual/prompt_builder.py plan --work repo_wiki_manual/work/project
```

确认生成：

```text
repo_wiki_manual/work/project/prompts/00_wiki_plan.prompt.md
```

### Step 4：根据 00_wiki_plan.prompt.md 生成 wiki_plan.json

读取：

```text
repo_wiki_manual/work/project/prompts/00_wiki_plan.prompt.md
```

请严格按照该文件中的要求生成 Wiki 规划 JSON。

要求：

1. 只基于 `00_wiki_plan.prompt.md` 中提供的项目结构和静态分析结果；
2. 不要编造不存在的模块、类、方法、接口或依赖；
3. 输出必须是严格 JSON；
4. 不要输出 Markdown；
5. 不要在 JSON 外添加解释文字；
6. 如果不确定，请写入 `uncertainties` 字段。

然后把生成结果保存为：

```text
repo_wiki_manual/work/project/wiki_plan.json
```

### Step 5：生成页面级 Prompt

执行：

```bash
python repo_wiki_manual/prompt_builder.py pages --work repo_wiki_manual/work/project
```

确认生成目录：

```text
repo_wiki_manual/work/project/prompts/pages/
```

其中应包含多个 `.prompt.md` 文件，例如：

```text
overview.prompt.md
architecture.prompt.md
modules__xxx.prompt.md
```

### Step 6：读取页面批量处理提示词

读取：

```text
repo_wiki_manual/run_pages_to_wiki.prompt.md
```

这个文件是页面生成阶段的总控提示词。

注意：如果该文件中的输入目录、输出目录仍然写的是相对简写路径，例如：

```text
pages/
output/wiki_docs/
```

请在实际执行时映射为：

```text
输入目录：
repo_wiki_manual/work/project/prompts/pages/

输出目录：
repo_wiki_manual/work/project/output/wiki_docs/
```

不要把页面保存到错误位置。

### Step 7：逐一生成 Wiki 页面

请遍历：

```text
repo_wiki_manual/work/project/prompts/pages/
```

下所有 `.prompt.md` 文件。

对每个 `.prompt.md` 文件，按以下规则处理。

#### 7.1 页面上下文隔离

本总控提示词必须始终保留。

处理每个页面时，只允许使用：

```text
本总控提示词
+ repo_wiki_manual/run_pages_to_wiki.prompt.md
+ 当前正在处理的 .prompt.md 文件内容
```

禁止使用上一个页面的正文、结论、模块判断、调用链推断、措辞和不确定项。

也就是说：

* 不要清空本总控提示词；
* 不要清空 `run_pages_to_wiki.prompt.md` 的规则；
* 只隔离不同页面之间的生成上下文；
* 当前页面只能基于当前 `.prompt.md` 文件提供的信息生成；
* 如果当前 `.prompt.md` 信息不足，请写“需要人工确认”，不要借用其他页面的信息补全。

#### 7.2 生成 Markdown

严格按照当前 `.prompt.md` 文件中的要求生成 Markdown 页面。

生成内容要求：

* 面向新接手项目的研发同学；
* 先讲结论，再讲细节；
* 类名、方法名、路径、配置项使用代码格式；
* 能画图的地方使用 Mermaid；
* 不确定的地方写“需要人工确认”；
* 不要编造不存在的类、方法、接口、模块、调用链或业务含义；
* 不要把 Markdown 正文包裹在代码块里。

#### 7.3 保存 Markdown

把生成结果保存到：

```text
repo_wiki_manual/work/project/output/wiki_docs/
```

命名规则：

1. 去掉 `.prompt.md` 后缀；
2. 把文件名中的双下划线 `__` 转换为目录分隔符 `/`；
3. 加上 `.md` 后缀；
4. 保存到 `repo_wiki_manual/work/project/output/wiki_docs/` 下。

示例：

```text
repo_wiki_manual/work/project/prompts/pages/overview.prompt.md
→ repo_wiki_manual/work/project/output/wiki_docs/overview.md

repo_wiki_manual/work/project/prompts/pages/architecture.prompt.md
→ repo_wiki_manual/work/project/output/wiki_docs/architecture.md

repo_wiki_manual/work/project/prompts/pages/modules__order.prompt.md
→ repo_wiki_manual/work/project/output/wiki_docs/modules/order.md
```

如果目标子目录不存在，请自动创建。

### Step 8：生成首页 index.md

如果页面 Prompt 中没有生成 `index.md`，请额外创建：

```text
repo_wiki_manual/work/project/output/wiki_docs/index.md
```

内容可以基于 `wiki_plan.json` 生成。

要求：

1. 简要说明项目用途；
2. 给出推荐阅读顺序；
3. 列出主要 Wiki 页面链接；
4. 不要编造业务细节；
5. 不确定信息写“需要人工确认”。

### Step 9：生成 MkDocs 配置

把：

```text
repo_wiki_manual/mkdocs.yml
```

复制到：

```text
repo_wiki_manual/work/project/output/mkdocs.yml
```

如果需要，请根据实际生成的 Markdown 文件更新 `nav`，保证常见页面能被访问。

Wiki 文档目录是：

```text
repo_wiki_manual/work/project/output/wiki_docs/
```

如果 MkDocs 默认要求文档目录为 `docs/`，请在 `mkdocs.yml` 中设置：

```yaml
docs_dir: wiki_docs
```

### Step 10：输出汇总

全部完成后，请输出一个简短汇总，包括：

1. 是否成功完成扫描；
2. 是否成功生成 `wiki_plan.json`；
3. 一共处理了多少个 `.prompt.md` 页面；
4. 生成了哪些 `.md` 文件；
5. 哪些页面包含“需要人工确认”；
6. 是否修改了 `scanner.py` 的忽略目录；
7. 最终 Wiki 输出目录；
8. 如何预览，例如：

```bash
cd repo_wiki_manual/work/project/output
mkdocs serve
```

## 六、失败处理规则

如果某一步失败，请不要跳过。

请说明：

1. 失败发生在哪一步；
2. 失败原因；
3. 已经生成了哪些文件；
4. 下一步我应该如何修复。

## 七、再次强调上下文隔离

不要执行“清空全部记忆”。

正确做法是：

```text
保留：
- 本总控提示词
- run_pages_to_wiki.prompt.md 的全局规则
- 当前正在处理的 .prompt.md 文件内容

隔离：
- 上一个页面的生成正文
- 上一个页面的模块判断
- 上一个页面的调用链推断
- 上一个页面的不确定项
- 上一个页面的措辞和结构细节
```

现在请开始执行。

```
```
