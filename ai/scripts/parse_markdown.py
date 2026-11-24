from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from common import (
    extract_summary,
    extract_title,
    read_text,
    relative_path,
    sha256_text,
    stable_doc_id,
)

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t#]*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")


def _slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[`*_~>|#]+", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-.")
    return text or "section"


def _is_blank(line: str) -> bool:
    return not line.strip()


def _split_long_section(
    lines: list[str],
    section_start: int,
    heading_path: list[str],
    max_chars: int,
) -> list[tuple[int, int, list[str]]]:
    """Group blank-line-delimited Markdown blocks without cutting code fences."""
    if sum(len(line) + 1 for line in lines) <= max_chars:
        return [(section_start, section_start + len(lines) - 1, lines)]

    segments: list[tuple[int, int, list[str]]] = []
    segment_start = 0
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        if not in_fence and _is_blank(line):
            segment = lines[segment_start : index + 1]
            if any(part.strip() for part in segment):
                segments.append((segment_start, index, segment))
            segment_start = index + 1
    if segment_start < len(lines):
        segment = lines[segment_start:]
        if any(part.strip() for part in segment):
            segments.append((segment_start, len(lines) - 1, segment))

    parts: list[tuple[int, int, list[str]]] = []
    current: list[str] = []
    current_start = 0
    current_end = 0
    current_size = 0
    for start, end, segment in segments:
        segment_size = sum(len(line) + 1 for line in segment)
        if current and current_size + segment_size > max_chars:
            parts.append((section_start + current_start, section_start + current_end, current))
            current = []
            current_size = 0
        if not current:
            current_start = start
        current.extend(segment)
        current_end = end
        current_size += segment_size
    if current:
        parts.append((section_start + current_start, section_start + current_end, current))

    # Validate that splitting did not leave a chunk with an unbalanced fence.
    for _, _, part in parts:
        if sum(1 for line in part if FENCE_RE.match(line)) % 2:
            return [(section_start, section_start + len(lines) - 1, lines)]
    return parts or [(section_start, section_start + len(lines) - 1, lines)]


def parse_markdown_document(path: Path, metadata: dict[str, Any], max_chars: int = 2200) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    text = read_text(path)
    lines = text.splitlines()
    doc_id = str(metadata["id"])
    doc_title = str(metadata.get("title") or extract_title(text, path.stem))
    doc_hash = sha256_text(text)
    try:
        content_path = relative_path(path)
    except ValueError:
        content_path = str(metadata.get("content_path") or path.as_posix())

    headings: list[dict[str, Any]] = []
    stack: list[tuple[int, str]] = []
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        headings.append(
            {
                "level": level,
                "title": title,
                "line": index + 1,
                "heading_path": [item[1] for item in stack],
            }
        )

    sections: list[dict[str, Any]] = []
    if not headings:
        if text.strip():
            sections.append(
                {
                    "heading": doc_title,
                    "heading_path": [doc_title],
                    "start_line": 1,
                    "end_line": len(lines),
                    "lines": lines,
                }
            )
    else:
        first_heading_line = headings[0]["line"]
        preamble = lines[: first_heading_line - 1]
        if any(line.strip() for line in preamble):
            sections.append(
                {
                    "heading": doc_title,
                    "heading_path": [doc_title],
                    "start_line": 1,
                    "end_line": first_heading_line - 1,
                    "lines": preamble,
                }
            )
        for idx, heading in enumerate(headings):
            start_line = heading["line"]
            end_line = headings[idx + 1]["line"] - 1 if idx + 1 < len(headings) else len(lines)
            section_lines = lines[start_line - 1 : end_line]
            content_lines = section_lines[1:]
            if not any(line.strip() for line in content_lines) and idx + 1 < len(headings):
                continue
            sections.append(
                {
                    "heading": heading["title"],
                    "heading_path": heading["heading_path"],
                    "start_line": start_line,
                    "end_line": end_line,
                    "lines": section_lines,
                }
            )

    chunks: list[dict[str, Any]] = []
    for section in sections:
        section_lines = section["lines"]
        for part_index, (start_line, end_line, part_lines) in enumerate(
            _split_long_section(
                section_lines,
                int(section["start_line"]),
                list(section["heading_path"]),
                max_chars,
            ),
            start=1,
        ):
            chunk_text = "\n".join(part_lines).strip()
            if not chunk_text:
                continue
            heading = str(section["heading"])
            chunk_id = f"{doc_id}:{_slug(heading)}:{start_line}"
            if part_index > 1 and any(
                existing["id"] == chunk_id for existing in chunks
            ):
                chunk_id = f"{chunk_id}:p{part_index}"
            chunks.append(
                {
                    "schema_version": 1,
                    "id": chunk_id,
                    "doc_id": doc_id,
                    "content_path": content_path,
                    "title": doc_title,
                    "heading": heading,
                    "heading_path": list(section["heading_path"]),
                    "start_line": start_line,
                    "end_line": end_line,
                    "summary": extract_summary(chunk_text, limit=220),
                    "status": metadata["status"],
                    "category": metadata["category"],
                    "difficulty": metadata["difficulty"],
                    "version_scope": list(metadata.get("version_scope", [])),
                    "tags": list(metadata.get("tags", [])),
                    "aliases": list(metadata.get("aliases", [])),
                    "code_paths": list(metadata.get("code_paths", [])),
                    "content_hash": sha256_text(chunk_text),
                    "doc_content_hash": doc_hash,
                    "text": chunk_text,
                }
            )

    catalog = {
        "schema_version": 1,
        "id": doc_id,
        "content_path": content_path,
        "metadata_path": metadata.get("_meta_path"),
        "title": doc_title,
        "category": metadata["category"],
        "status": metadata["status"],
        "difficulty": metadata["difficulty"],
        "summary": metadata["summary"],
        "version_scope": list(metadata.get("version_scope", [])),
        "tags": list(metadata.get("tags", [])),
        "aliases": list(metadata.get("aliases", [])),
        "code_paths": list(metadata.get("code_paths", [])),
        "test_paths": list(metadata.get("test_paths", [])),
        "reviewed_at": metadata.get("reviewed_at"),
        "line_count": len(lines),
        "section_count": len(chunks),
        "content_hash": doc_hash,
    }
    return catalog, chunks
