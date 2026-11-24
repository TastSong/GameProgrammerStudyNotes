from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[2]
AI_DIR = ROOT / "ai"
META_DIR = AI_DIR / "meta"
NOTES_META_DIR = META_DIR / "notes"
INDEX_DIR = AI_DIR / "indexes"
SCRIPTS_DIR = AI_DIR / "scripts"

EXCLUDED_TOP_LEVEL = {".git", "ai"}


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def iter_documents() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in EXCLUDED_TOP_LEVEL for part in path.relative_to(ROOT).parts):
            continue
        yield path


def iter_csharp_files() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*.cs")):
        if any(part in EXCLUDED_TOP_LEVEL for part in path.relative_to(ROOT).parts):
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(
            data,
            handle,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


def load_all_metadata() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(NOTES_META_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if isinstance(data, dict):
            data["_meta_path"] = relative_path(path)
            records.append(data)
    return records


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_doc_id(path: Path) -> str:
    rel = path.relative_to(ROOT).with_suffix("").as_posix()
    value = unicodedata.normalize("NFKC", rel).lower()
    value = value.replace("'", "").replace("’", "")
    value = re.sub(r"[\\/]+", "-", value)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^0-9a-z\u4e00-\u9fff.+-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-.")
    return value or "document"


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def strip_markdown_inline(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_~>|#]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_summary(text: str, limit: int = 240) -> str:
    lines = text.splitlines()
    in_fence = False
    collecting = False
    paragraph: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            if collecting and paragraph:
                break
            continue
        if not collecting:
            if not line:
                continue
            if line.startswith(("![", "[![", "<img", "|", "---")):
                continue
            if re.match(r"^\[[^\]]+\]\([^)]+\)\s*$", line):
                continue
            if re.match(r"^(?:[-*+]\s+|\d+\.\s+)", line):
                continue
            collecting = True
        if collecting:
            if not line:
                break
            paragraph.append(line)

    summary = strip_markdown_inline(" ".join(paragraph))
    if not summary:
        return "该文档整理相关主题内容，具体结论以正文为准。"
    if len(summary) > limit:
        summary = summary[: limit - 1].rstrip() + "…"
    return summary


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(
                json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                + "\n"
            )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def path_exists(relative: str) -> bool:
    return (ROOT / relative).exists()
