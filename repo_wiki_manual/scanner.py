import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any

IGNORE_DIRS = {
    ".git", ".idea", ".vscode", "target", "build", "dist", "node_modules",
    ".gradle", ".mvn", "out", "__pycache__", ".venv", "logs",
    "repo_wiki_manual"
}

TEXT_EXTS = {
    ".java", ".xml", ".yml", ".yaml", ".properties", ".md", ".gradle",
    ".sql", ".json", ".txt", ".sh"
}

IMPORTANT_FILE_NAMES = {
    "pom.xml", "build.gradle", "settings.gradle", "README.md", "readme.md",
    "application.yml", "application.yaml", "application.properties",
    "bootstrap.yml", "bootstrap.yaml", "bootstrap.properties"
}

JAVA_CLASS_RE = re.compile(r'\b(public|private|protected)?\s*(abstract\s+|final\s+)?(class|interface|enum)\s+([A-Za-z_][A-Za-z0-9_]*)')
JAVA_METHOD_RE = re.compile(
    r'(?P<anno>(?:\s*@[\w.]+(?:\([^)]*\))?\s*)*)'
    r'(?P<mods>(?:public|private|protected|static|final|synchronized|abstract|native|\s)+)?'
    r'(?P<ret>[A-Za-z_][A-Za-z0-9_<>\[\].?,\s]*)\s+'
    r'(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*'
    r'\((?P<params>[^)]*)\)\s*(?:throws\s+[^{]+)?\{'
)
PACKAGE_RE = re.compile(r'^\s*package\s+([\w.]+)\s*;', re.MULTILINE)
IMPORT_RE = re.compile(r'^\s*import\s+([\w.*]+)\s*;', re.MULTILINE)
ANNOTATION_RE = re.compile(r'@([A-Za-z_][A-Za-z0-9_.]*)(?:\(([^)]*)\))?')

ROUTE_ANNOS = {
    "RequestMapping", "GetMapping", "PostMapping", "PutMapping",
    "DeleteMapping", "PatchMapping"
}

LAYER_ANNOS = {
    "RestController": "controller",
    "Controller": "controller",
    "Service": "service",
    "Component": "component",
    "Repository": "repository",
    "Mapper": "mapper",
    "Configuration": "configuration",
    "FeignClient": "client",
}

INJECTION_ANNOS = {"Autowired", "Resource", "Inject"}


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def safe_read(path: Path, limit: int = 200_000) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
        return data[:limit]
    except Exception:
        return ""


def build_tree(root: Path) -> str:
    lines = []
    for path in sorted(root.rglob("*")):
        if should_ignore(path):
            continue
        rel = path.relative_to(root)
        depth = len(rel.parts) - 1
        if path.is_dir():
            lines.append("  " * depth + f"- {path.name}/")
        elif path.suffix in TEXT_EXTS or path.name in IMPORTANT_FILE_NAMES:
            lines.append("  " * depth + f"- {path.name}")
    return "\n".join(lines)


def extract_annotations(text: str) -> List[Dict[str, str]]:
    result = []
    for m in ANNOTATION_RE.finditer(text):
        name = m.group(1).split(".")[-1]
        args = (m.group(2) or "").strip()
        result.append({"name": name, "args": args})
    return result


def detect_layer(annotations: List[Dict[str, str]]) -> str:
    for a in annotations:
        if a["name"] in LAYER_ANNOS:
            return LAYER_ANNOS[a["name"]]
    return "unknown"


def route_from_annotations(annotations: List[Dict[str, str]]) -> List[Dict[str, str]]:
    routes = []
    for a in annotations:
        if a["name"] in ROUTE_ANNOS:
            routes.append({"method_annotation": a["name"], "value": a["args"]})
    return routes


def parse_java_file(path: Path, root: Path) -> Dict[str, Any]:
    text = safe_read(path)
    package = ""
    pm = PACKAGE_RE.search(text)
    if pm:
        package = pm.group(1)

    imports = IMPORT_RE.findall(text)

    class_match = JAVA_CLASS_RE.search(text)
    class_name = class_match.group(4) if class_match else path.stem
    class_type = class_match.group(3) if class_match else "unknown"

    class_region = text[:class_match.start()] if class_match else text[:1000]
    class_annotations = extract_annotations(class_region[-3000:])
    layer = detect_layer(class_annotations)

    methods = []
    for m in JAVA_METHOD_RE.finditer(text):
        method_region = m.group("anno") or ""
        annos = extract_annotations(method_region)
        name = m.group("name")
        # 过滤常见控制结构误识别
        if name in {"if", "for", "while", "switch", "catch", "try"}:
            continue
        methods.append({
            "name": name,
            "return_type": " ".join((m.group("ret") or "").split()),
            "params": " ".join((m.group("params") or "").split()),
            "annotations": annos,
            "routes": route_from_annotations(annos),
        })

    injected_fields = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if any(f"@{anno}" in line for anno in INJECTION_ANNOS):
            nearby = "\n".join(lines[i:i+3])
            injected_fields.append(nearby.strip())

    return {
        "path": str(path.relative_to(root)),
        "package": package,
        "class_name": class_name,
        "class_type": class_type,
        "layer": layer,
        "annotations": class_annotations,
        "imports": imports,
        "methods": methods,
        "injected_fields": injected_fields,
    }


def summarize_file(path: Path, root: Path) -> Dict[str, Any]:
    rel = str(path.relative_to(root))
    text = safe_read(path, limit=40_000)
    return {
        "path": rel,
        "suffix": path.suffix,
        "name": path.name,
        "size": path.stat().st_size,
        "head": text[:3000],
    }


def scan_repo(root: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    java_symbols = []
    important_files = []
    all_files = []

    for path in sorted(root.rglob("*")):
        if should_ignore(path) or not path.is_file():
            continue
        if path.suffix not in TEXT_EXTS and path.name not in IMPORTANT_FILE_NAMES:
            continue

        rel = str(path.relative_to(root))
        all_files.append(rel)

        if path.suffix == ".java":
            java_symbols.append(parse_java_file(path, root))

        if path.name in IMPORTANT_FILE_NAMES or path.suffix in {".yml", ".yaml", ".properties", ".xml", ".gradle", ".md"}:
            important_files.append(summarize_file(path, root))

    tree = build_tree(root)

    (out / "repo_tree.md").write_text(tree, encoding="utf-8")
    (out / "files_index.json").write_text(json.dumps(all_files, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "java_symbols.json").write_text(json.dumps(java_symbols, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "important_files.json").write_text(json.dumps(important_files, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "root": str(root),
        "file_count": len(all_files),
        "java_class_count": len(java_symbols),
        "layers": {},
    }
    for s in java_symbols:
        summary["layers"][s["layer"]] = summary["layers"].get(s["layer"], 0) + 1

    (out / "scan_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scan finished. Output: {out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", help="Path to target repository")
    parser.add_argument("--out", default="work/default", help="Output work directory")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    out = Path(args.out).resolve()

    if not root.exists():
        raise SystemExit(f"Repository path not found: {root}")

    scan_repo(root, out)


if __name__ == "__main__":
    main()