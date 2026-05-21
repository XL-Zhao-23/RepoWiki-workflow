# 手动龙虾工作流

## 第 1 步：扫描项目

```bash
python scanner.py /path/to/project --out work/my_project
```

## 第 2 步：生成 Wiki 规划 Prompt

```bash
python prompt_builder.py plan --work work/my_project
```

打开：

```text
work/my_project/prompts/00_wiki_plan.prompt.md
```

复制给龙虾。

## 第 3 步：保存 Wiki 规划

龙虾必须返回 JSON。保存为：

```text
work/my_project/wiki_plan.json
```

## 第 4 步：生成页面 Prompt

```bash
python prompt_builder.py pages --work work/my_project
```

## 第 5 步：逐页生成 Markdown

逐个复制：

```text
work/my_project/prompts/pages/*.prompt.md
```

龙虾返回 Markdown 后，保存到：

```text
work/my_project/output/wiki_docs/
```

## 第 6 步：本地预览

```bash
cd work/my_project/output
mkdocs serve
```