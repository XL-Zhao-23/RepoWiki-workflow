import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PLAN_PROMPT_TEMPLATE = """
你现在是一个资深代码库文档架构师。我要为这个代码库生成一个内部 Wiki。

请你只基于我提供的代码库结构和静态分析结果，不要编造不存在的模块、接口或依赖。

你的任务：
1. 判断项目类型、技术栈、主要业务边界。
2. 识别核心模块、分层结构和关键入口。
3. 设计一套适合新同事阅读的 Wiki 目录。
4. 输出严格 JSON，不要输出 Markdown，不要解释。

JSON 格式如下：

{{
  "project_name": "项目名称",
  "project_summary": "一句话说明项目用途",
  "tech_stack": ["技术1", "技术2"],
  "main_modules": [
    {{
      "name": "模块名",
      "paths": ["相关路径"],
      "responsibility": "模块职责",
      "suggested_pages": ["建议页面文件名"]
    }}
  ],
  "wiki_pages": [
    {{
      "file": "overview.md",
      "title": "项目总览",
      "purpose": "页面目的",
      "source_paths": ["建议参考的源码路径或配置文件路径"],
      "sections": ["背景", "整体架构", "核心流程"]
    }}
  ],
  "diagrams": [
    {{
      "file": "architecture.md",
      "type": "mermaid flowchart",
      "description": "系统架构图"
    }}
  ],
  "uncertainties": ["哪些地方需要人工确认"]
}}

下面是代码库信息。

# 目录树

```text
{repo_tree}
```

# 扫描摘要

```json
{scan_summary}
```

# Java 符号摘要

```json
{java_symbols_compact}
```

# 重要配置和说明文件摘要

```json
{important_files_compact}
```
""".strip()


PAGE_PROMPT_TEMPLATE = """
你现在是一个资深代码库文档工程师。请为代码库 Wiki 生成一个 Markdown 页面。

要求：
1. 只基于我提供的事实写，不要编造。
2. 先讲结论，再讲细节。
3. 面向新接手项目的研发同学。
4. 涉及类名、方法名、路径、配置项时使用代码格式。
5. 如果信息不足，请写“需要人工确认”，不要猜。
6. 如果适合画图，请使用 Mermaid。
7. 直接输出 Markdown 正文，不要包裹在代码块里。

# 当前页面

文件名：{file}
标题：{title}
页面目的：{purpose}

# 建议章节

{sections}

# 相关源码路径

{source_paths}

# 代码库目录树

```text
{repo_tree}
```

# 与本页面相关的 Java 类/接口/方法

```json
{related_symbols}
```

# 重要文件摘要

```json
{related_files}
```

# 写作模板建议

请尽量按下面结构组织：

# {title}

## 1. 这个页面解决什么问题

## 2. 核心结论

## 3. 相关代码位置

## 4. 模块/流程说明

## 5. 关键类与方法

## 6. Mermaid 图

## 7. 常见问题与注意事项

## 8. 需要人工确认的点
""".strip()


def read_json(path: Path, default: Any):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def compact_symbols(symbols: List[Dict[str, Any]], max_methods: int = 8) -> List[Dict[str, Any]]:
    compact = []
    for s in symbols:
        compact.append({
            "path": s.get("path"),
            "package": s.get("package"),
            "class_name": s.get("class_name"),
            "class_type": s.get("class_type"),
            "layer": s.get("layer"),
            "annotations": s.get("annotations", [])[:8],
            "imports": s.get("imports", [])[:20],
            "methods": s.get("methods", [])[:max_methods],
            "injected_fields": s.get("injected_fields", [])[:5],
        })
    return compact


def compact_files(files: List[Dict[str, Any]], max_len: int = 1200) -> List[Dict[str, Any]]:
    result = []
    for f in files:
        item = dict(f)
        item["head"] = item.get("head", "")[:max_len]
        result.append(item)
    return result


def build_plan_prompt(work: Path) -> Path:
    prompts = work / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)

    repo_tree = (work / "repo_tree.md").read_text(encoding="utf-8")
    scan_summary = read_json(work / "scan_summary.json", {})
    java_symbols = read_json(work / "java_symbols.json", [])
    important_files = read_json(work / "important_files.json", [])

    prompt = PLAN_PROMPT_TEMPLATE.format(
        repo_tree=repo_tree,
        scan_summary=json.dumps(scan_summary, ensure_ascii=False, indent=2),
        java_symbols_compact=json.dumps(compact_symbols(java_symbols, max_methods=5), ensure_ascii=False, indent=2),
        important_files_compact=json.dumps(compact_files(important_files, max_len=800), ensure_ascii=False, indent=2),
    )

    out = prompts / "00_wiki_plan.prompt.md"
    out.write_text(prompt, encoding="utf-8")
    return out


def path_matches(symbol_path: str, source_paths: List[str]) -> bool:
    if not source_paths:
        return True
    return any(p and (symbol_path.startswith(p) or p in symbol_path) for p in source_paths)


def build_page_prompts(work: Path) -> Path:
    wiki_plan_path = work / "wiki_plan.json"
    if not wiki_plan_path.exists():
        raise SystemExit(f"Missing {wiki_plan_path}. Please save LLM returned JSON there first.")

    plan = read_json(wiki_plan_path, {})
    repo_tree = (work / "repo_tree.md").read_text(encoding="utf-8")
    java_symbols = read_json(work / "java_symbols.json", [])
    important_files = read_json(work / "important_files.json", [])

    pages_dir = work / "prompts" / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    for page in plan.get("wiki_pages", []):
        file = page.get("file", "untitled.md")
        title = page.get("title", file)
        purpose = page.get("purpose", "")
        sections = page.get("sections", [])
        source_paths = page.get("source_paths", [])

        related_symbols = [
            s for s in java_symbols
            if path_matches(s.get("path", ""), source_paths)
        ][:80]

        related_files = [
            f for f in important_files
            if path_matches(f.get("path", ""), source_paths)
        ][:30]

        prompt = PAGE_PROMPT_TEMPLATE.format(
            file=file,
            title=title,
            purpose=purpose,
            sections="\n".join(f"- {x}" for x in sections),
            source_paths="\n".join(f"- {x}" for x in source_paths),
            repo_tree=repo_tree,
            related_symbols=json.dumps(compact_symbols(related_symbols, max_methods=12), ensure_ascii=False, indent=2),
            related_files=json.dumps(compact_files(related_files, max_len=2000), ensure_ascii=False, indent=2),
        )

        safe_name = file.replace("/", "__").replace("\\", "__").replace(".md", "")
        (pages_dir / f"{safe_name}.prompt.md").write_text(prompt, encoding="utf-8")

    return pages_dir


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("plan")
    p1.add_argument("--work", required=True)

    p2 = sub.add_parser("pages")
    p2.add_argument("--work", required=True)

    args = parser.parse_args()
    work = Path(args.work).resolve()

    if args.cmd == "plan":
        out = build_plan_prompt(work)
        print(f"Plan prompt generated: {out}")

    if args.cmd == "pages":
        out = build_page_prompts(work)
        print(f"Page prompts generated: {out}")


if __name__ == "__main__":
    main()