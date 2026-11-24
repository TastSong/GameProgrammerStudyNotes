from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import INDEX_DIR, ROOT, read_jsonl, read_text, relative_path


def parse_lines(value: str) -> tuple[int, int | None]:
    if "-" in value:
        start_text, end_text = value.split("-", 1)
        start = int(start_text)
        end = int(end_text) if end_text else None
        return start, end
    return int(value), int(value)


def resolve_path(value: str) -> Path:
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit(f"path escapes repository: {value}") from exc
    if not candidate.exists():
        raise SystemExit(f"path does not exist: {value}")
    if not candidate.is_file():
        raise SystemExit(f"path is not a file: {value}")
    return candidate


def find_chunk(chunk_id: str, index_dir: Path = INDEX_DIR) -> dict[str, Any]:
    for chunk in read_jsonl(index_dir / "chunks.jsonl"):
        if chunk["id"] == chunk_id:
            return chunk
    raise SystemExit(f"chunk not found: {chunk_id}")


def read_lines(path: Path, start: int, end: int | None = None) -> dict[str, Any]:
    lines = read_text(path).splitlines()
    if start < 1:
        raise SystemExit("start line must be >= 1")
    final = len(lines) if end is None else end
    if final < start:
        raise SystemExit("end line must be >= start line")
    selected = lines[start - 1 : final]
    return {
        "path": relative_path(path),
        "start_line": start,
        "end_line": min(final, len(lines)),
        "line_count": len(lines),
        "text": "\n".join(selected),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Read a source file or indexed chunk with line citations.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", help="Repository-relative source path")
    group.add_argument("--chunk-id", help="Chunk ID from chunks.jsonl")
    parser.add_argument("--lines", help="Line range such as 10-40")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.chunk_id:
        chunk = find_chunk(args.chunk_id)
        path = resolve_path(chunk["content_path"])
        result = read_lines(path, int(chunk["start_line"]), int(chunk["end_line"]))
        result["chunk_id"] = chunk["id"]
        result["heading_path"] = chunk["heading_path"]
    else:
        if not args.lines:
            start, end = 1, None
        else:
            start, end = parse_lines(args.lines)
        result = read_lines(resolve_path(args.path), start, end)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return

    print(f"{result['path']}:{result['start_line']}-{result['end_line']}")
    if result.get("heading_path"):
        print(" > ".join(result["heading_path"]))
        print()
    print(result["text"])


if __name__ == "__main__":
    main()
