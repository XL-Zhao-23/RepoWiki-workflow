# Repo Wiki Manual

一个“无大模型 API”的代码库 Wiki 生成工作流脚手架。

核心思想：

1. 本地扫描代码库，生成结构化事实。
2. 本地生成 Prompt。
3. 手动把 Prompt 复制到公司内部大模型/龙虾/JoyClaw 对话框。
4. 把模型返回的 Markdown 保存到 `output/wiki_docs/`。
5. 使用 MkDocs 本地预览 Wiki。

## 快速开始

```bash
cd repo_wiki_manual
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scanner.py /path/to/your/project --out work/my_project
python prompt_builder.py plan --work work/my_project
```

然后打开：

```text
work/my_project/prompts/00_wiki_plan.prompt.md
```

复制给大模型，让它返回 `wiki_plan.json`，保存到：

```text
work/my_project/wiki_plan.json
```

继续生成页面级 Prompt：

```bash
python prompt_builder.py pages --work work/my_project
```

把 `work/my_project/prompts/pages/*.prompt.md` 逐个复制给大模型，返回结果保存到：

```text
work/my_project/output/wiki_docs/
```

本地预览：

```bash
cp mkdocs.yml work/my_project/output/mkdocs.yml
cd work/my_project/output
mkdocs serve
```