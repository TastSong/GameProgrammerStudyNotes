from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Iterable

from common import (
    INDEX_DIR,
    iter_csharp_files,
    load_all_metadata,
    read_text,
    relative_path,
    sha256_text,
    write_jsonl,
)

TYPE_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|internal|static|sealed|abstract|partial|readonly|ref|unsafe)\s+)*"
    r"(class|interface|struct|enum)\s+([A-Za-z_]\w*)"
)
METHOD_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|internal|static|virtual|override|abstract|sealed|async|extern|unsafe|new|partial)\s+)*"
    r"(?P<return>[A-Za-z_][\w<>,\[\]?\.]*)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*\((?P<args>[^;{}]*)\)\s*(?P<tail>\{|=>|;|$)"
)
CONTROL_KEYWORDS = {
    "if", "for", "foreach", "while", "switch", "catch", "using", "lock", "return",
    "throw", "new", "sizeof", "typeof", "nameof", "fixed", "checked", "unchecked",
}


def _strip_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_string:
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if not in_string and line[index : index + 2] == "//":
            return line[:index]
    return line


def _brace_delta(line: str) -> int:
    line = _strip_line_comment(line)
    return line.count("{") - line.count("}")


def find_block_end(lines: list[str], start_index: int) -> int:
    depth = 0
    found_open = False
    for index in range(start_index, len(lines)):
        code = _strip_line_comment(lines[index])
        opens = code.count("{")
        closes = code.count("}")
        if opens:
            found_open = True
        depth += opens - closes
        if found_open and depth <= 0:
            return index
    return len(lines) - 1


def find_signature_end(lines: list[str], start_index: int) -> tuple[int, bool, bool]:
    text = ""
    for index in range(start_index, min(len(lines), start_index + 8)):
        text += _strip_line_comment(lines[index]).strip() + " "
        if "{" in text:
            return index, True, False
        if "=>" in text:
            return index, False, True
        if ";" in text:
            return index, False, False
    return start_index, False, False


def related_doc_ids(path: str, metadata: Iterable[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for record in metadata:
        for code_path in record.get("code_paths", []):
            code_path = str(code_path).rstrip("/")
            if path == code_path or path.startswith(code_path + "/"):
                ids.append(str(record["id"]))
                break
    return sorted(set(ids))


def parse_csharp(path: Path, metadata: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    text = read_text(path)
    lines = text.splitlines()
    try:
        path_text = relative_path(path)
    except ValueError:
        path_text = path.as_posix()
    namespace_match = re.search(r"^\s*namespace\s+([A-Za-z_][\w.]*)", text, re.MULTILINE)
    namespace = namespace_match.group(1) if namespace_match else ""
    docs = related_doc_ids(path_text, metadata)
    symbols: list[dict[str, Any]] = []

    types: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        match = TYPE_RE.match(line)
        if not match:
            continue
        kind, name = match.group(1), match.group(2)
        end_index = find_block_end(lines, index)
        qualified = ".".join(part for part in (namespace, name) if part)
        block = "\n".join(lines[index : end_index + 1])
        symbol = {
            "schema_version": 1,
            "id": f"csharp:{qualified}:L{index + 1}",
            "language": "csharp",
            "kind": kind,
            "name": name,
            "qualified_name": qualified,
            "namespace": namespace,
            "type_name": name,
            "path": path_text,
            "start_line": index + 1,
            "end_line": end_index + 1,
            "signature": line.strip(),
            "related_doc_ids": docs,
            "content_hash": sha256_text(block),
        }
        symbols.append(symbol)
        types.append({"name": name, "start": index, "end": end_index, "qualified": qualified})

    for type_info in types:
        type_name = type_info["name"]
        for index in range(type_info["start"] + 1, type_info["end"] + 1):
            line = lines[index]
            match = METHOD_RE.match(line)
            is_constructor = False
            name = ""
            args = ""
            if match:
                name = match.group("name")
                return_type = match.group("return")
                if name in CONTROL_KEYWORDS or return_type in CONTROL_KEYWORDS:
                    continue
                args = match.group("args")
                kind = "method"
            else:
                constructor_match = re.match(
                    r"^\s*(?:(?:public|private|protected|internal)\s+)?"
                    r"(?P<name>[A-Za-z_]\w*)\s*\((?P<args>[^;{}]*)\)\s*(?:\{|$)",
                    line,
                )
                if not constructor_match or constructor_match.group("name") != type_name:
                    continue
                name = constructor_match.group("name")
                args = constructor_match.group("args")
                kind = "constructor"
                is_constructor = True

            signature_end, has_brace, expression_body = find_signature_end(lines, index)
            end_index = index if expression_body or not has_brace else find_block_end(lines, index)
            qualified_method = f"{type_info['qualified']}.{name}"
            signature = " ".join(
                part.strip() for part in lines[index : signature_end + 1] if part.strip()
            )
            block = "\n".join(lines[index : end_index + 1])
            symbols.append(
                {
                    "schema_version": 1,
                    "id": f"csharp:{qualified_method}:L{index + 1}",
                    "language": "csharp",
                    "kind": kind,
                    "name": name,
                    "qualified_name": qualified_method,
                    "namespace": namespace,
                    "type_name": type_name,
                    "path": path_text,
                    "start_line": index + 1,
                    "end_line": end_index + 1,
                    "signature": signature,
                    "arguments": args.strip(),
                    "is_constructor": is_constructor,
                    "related_doc_ids": docs,
                    "content_hash": sha256_text(block),
                }
            )

    return symbols


def build(output_dir: Path = INDEX_DIR) -> list[dict[str, Any]]:
    metadata = load_all_metadata()
    symbols: list[dict[str, Any]] = []
    for path in iter_csharp_files():
        symbols.extend(parse_csharp(path, metadata))
    symbols.sort(key=lambda item: (item["path"], item["start_line"], item["id"]))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "symbols.jsonl", symbols)
    return symbols


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a C# symbol index for Agent code navigation.")
    parser.add_argument("--output-dir", type=Path, default=INDEX_DIR)
    args = parser.parse_args()
    symbols = build(args.output_dir)
    kinds: dict[str, int] = {}
    for symbol in symbols:
        kinds[symbol["kind"]] = kinds.get(symbol["kind"], 0) + 1
    print(f"symbols: {len(symbols)}")
    print("kinds:", ", ".join(f"{key}={value}" for key, value in sorted(kinds.items())))
    print(f"output: {args.output_dir}")


if __name__ == "__main__":
    main()
