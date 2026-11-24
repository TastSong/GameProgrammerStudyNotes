from __future__ import annotations

import argparse
import json
import logging
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import jieba

from common import INDEX_DIR, read_jsonl

jieba.setLogLevel(logging.ERROR)

ENGLISH_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.+#-]*")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]+")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
    "it", "of", "on", "or", "that", "the", "this", "to", "with", "为什么", "怎么",
    "如何", "什么", "一个", "以及", "进行", "相关", "内容",
}


@lru_cache(maxsize=8192)
def tokenize(text: str) -> tuple[str, ...]:
    lowered = text.casefold()
    tokens: list[str] = []
    for match in ENGLISH_TOKEN_RE.finditer(lowered):
        token = match.group(0).casefold()
        tokens.append(token)
        tokens.extend(part for part in re.split(r"[._-]+", token) if part)
    for sequence in CHINESE_RE.findall(lowered):
        if len(sequence) <= 12:
            tokens.append(sequence)
        tokens.extend(
            piece.strip()
            for piece in jieba.lcut_for_search(sequence)
            if piece.strip() and len(piece.strip()) > 1
        )
        for size in (2, 3, 4):
            tokens.extend(sequence[index : index + size] for index in range(len(sequence) - size + 1))
    deduplicated: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if token and token not in STOPWORDS and token not in seen:
            seen.add(token)
            deduplicated.append(token)
    return tuple(deduplicated)


def load_aliases(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("groups", []))


def expand_query(query: str, alias_groups: Iterable[dict[str, Any]]) -> str:
    lowered = query.casefold()
    additions: list[str] = []
    for group in alias_groups:
        canonical = str(group.get("canonical", ""))
        aliases = [str(item) for item in group.get("aliases", [])]
        if canonical and any(term.casefold() in lowered for term in [canonical, *aliases]):
            additions.extend([canonical, *aliases])
    return " ".join([query, *additions])


def _contains_any(value: str, filters: list[str] | None) -> bool:
    if not filters:
        return True
    return value.casefold() in {item.casefold() for item in filters}


def _matches_version(record: dict[str, Any], version: str | None) -> bool:
    if not version:
        return True
    scopes = [str(item).casefold() for item in record.get("version_scope", [])]
    if not scopes:
        return True
    needle = version.casefold()
    return any(needle in scope or scope in needle for scope in scopes)


def _matches_common(record: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.status and not _contains_any(str(record.get("status", "")), args.status):
        return False
    if args.category and not _contains_any(str(record.get("category", "")), args.category):
        return False
    return _matches_version(record, args.version)


def _bm25_scores(
    query: str,
    records: list[dict[str, Any]],
    text_builder: Any,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[float]:
    query_tokens = list(dict.fromkeys(tokenize(query)))
    if not query_tokens or not records:
        return [0.0] * len(records)

    document_tokens = [tokenize(text_builder(record)) for record in records]
    lengths = [len(tokens) for tokens in document_tokens]
    avg_length = sum(lengths) / max(len(lengths), 1)
    doc_freq: Counter[str] = Counter()
    term_freqs: list[Counter[str]] = []
    for tokens in document_tokens:
        counts = Counter(tokens)
        term_freqs.append(counts)
        for token in set(tokens):
            doc_freq[token] += 1

    total_docs = len(records)
    scores: list[float] = []
    for counts, length in zip(term_freqs, lengths):
        score = 0.0
        for token in query_tokens:
            frequency = counts.get(token, 0)
            if not frequency:
                continue
            df = doc_freq.get(token, 0)
            idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
            denominator = frequency + k1 * (1 - b + b * length / max(avg_length, 1.0))
            score += idf * (frequency * (k1 + 1)) / denominator
        scores.append(score)
    return scores


def _snippet(text: str, query: str, limit: int = 220) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    lowered = compact.casefold()
    positions = [lowered.find(token) for token in tokenize(query) if lowered.find(token) >= 0]
    center = min(positions) if positions else 0
    start = max(0, center - limit // 3)
    end = min(len(compact), start + limit)
    prefix = "…" if start else ""
    suffix = "…" if end < len(compact) else ""
    return f"{prefix}{compact[start:end].strip()}{suffix}"


def search_chunks(
    query: str,
    *,
    top_k: int = 6,
    status: list[str] | None = None,
    category: list[str] | None = None,
    version: str | None = None,
    index_dir: Path = INDEX_DIR,
) -> list[dict[str, Any]]:
    args = argparse.Namespace(status=status, category=category, version=version)
    chunks = [record for record in read_jsonl(index_dir / "chunks.jsonl") if _matches_common(record, args)]
    expanded = expand_query(query, load_aliases(index_dir / "aliases.json"))
    scores = _bm25_scores(
        expanded,
        chunks,
        lambda record: " ".join(
            [
                str(record.get("title", "")),
                str(record.get("heading", "")),
                " ".join(record.get("heading_path", [])),
                " ".join(record.get("tags", [])),
                " ".join(record.get("aliases", [])),
                str(record.get("summary", "")),
                str(record.get("text", "")),
            ]
        ),
    )
    ranked = sorted(
        zip(chunks, scores),
        key=lambda item: (-item[1], item[0]["content_path"], item[0]["start_line"]),
    )
    results = []
    for record, score in ranked:
        if score <= 0:
            continue
        results.append(
            {
                "kind": "chunk",
                "chunk_id": record["id"],
                "doc_id": record["doc_id"],
                "path": record["content_path"],
                "title": record["title"],
                "heading": record["heading"],
                "heading_path": record["heading_path"],
                "lines": f"{record['start_line']}-{record['end_line']}",
                "start_line": record["start_line"],
                "end_line": record["end_line"],
                "status": record["status"],
                "category": record["category"],
                "difficulty": record["difficulty"],
                "version_scope": record["version_scope"],
                "summary": record["summary"],
                "snippet": _snippet(record["text"], query),
                "score": round(score, 6),
            }
        )
        if len(results) >= top_k:
            break
    return results


def search_symbols(
    query: str,
    *,
    top_k: int = 6,
    status: list[str] | None = None,
    category: list[str] | None = None,
    version: str | None = None,
    index_dir: Path = INDEX_DIR,
) -> list[dict[str, Any]]:
    symbols = read_jsonl(index_dir / "symbols.jsonl")
    catalogs = {record["id"]: record for record in read_jsonl(index_dir / "catalog.jsonl")}
    expanded = expand_query(query, load_aliases(index_dir / "aliases.json"))

    filtered: list[dict[str, Any]] = []
    for symbol in symbols:
        docs = [catalogs[doc_id] for doc_id in symbol.get("related_doc_ids", []) if doc_id in catalogs]
        if status and not any(_contains_any(str(doc.get("status", "")), status) for doc in docs):
            if docs:
                continue
        if category and not any(_contains_any(str(doc.get("category", "")), category) for doc in docs):
            if docs:
                continue
        if version and docs and not any(_matches_version(doc, version) for doc in docs):
            continue
        filtered.append(symbol)

    scores = _bm25_scores(
        expanded,
        filtered,
        lambda record: " ".join(
            [
                str(record.get("name", "")),
                str(record.get("qualified_name", "")),
                str(record.get("signature", "")),
                str(record.get("path", "")),
                " ".join(record.get("related_doc_ids", [])),
            ]
        ),
    )
    ranked = sorted(zip(filtered, scores), key=lambda item: (-item[1], item[0]["path"], item[0]["start_line"]))
    results = []
    for record, score in ranked:
        if score <= 0:
            continue
        docs = [catalogs[doc_id] for doc_id in record.get("related_doc_ids", []) if doc_id in catalogs]
        results.append(
            {
                "kind": "symbol",
                "symbol_id": record["id"],
                "name": record["name"],
                "qualified_name": record["qualified_name"],
                "symbol_kind": record["kind"],
                "path": record["path"],
                "lines": f"{record['start_line']}-{record['end_line']}",
                "start_line": record["start_line"],
                "end_line": record["end_line"],
                "signature": record["signature"],
                "related_doc_ids": record.get("related_doc_ids", []),
                "status": docs[0]["status"] if docs else None,
                "category": docs[0]["category"] if docs else None,
                "version_scope": docs[0]["version_scope"] if docs else [],
                "score": round(score, 6),
            }
        )
        if len(results) >= top_k:
            break
    return results


def search(
    query: str,
    *,
    kind: str = "chunks",
    top_k: int = 6,
    status: list[str] | None = None,
    category: list[str] | None = None,
    version: str | None = None,
    index_dir: Path = INDEX_DIR,
) -> list[dict[str, Any]]:
    if kind == "symbols":
        return search_symbols(
            query,
            top_k=top_k,
            status=status,
            category=category,
            version=version,
            index_dir=index_dir,
        )
    return search_chunks(
        query,
        top_k=top_k,
        status=status,
        category=category,
        version=version,
        index_dir=index_dir,
    )


def _split_filter(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    result: list[str] = []
    for value in values:
        result.extend(part.strip() for part in value.split(",") if part.strip())
    return result or None


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the local AI indexes.")
    parser.add_argument("query", help="Natural-language or symbol query")
    parser.add_argument("--top", type=int, default=6)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--kind", choices=["chunks", "symbols"], default="chunks")
    parser.add_argument("--symbol", action="store_true", help="Search code symbols instead of chunks")
    parser.add_argument("--status", action="append", help="Filter by status; comma-separated values allowed")
    parser.add_argument("--category", action="append", help="Filter by category")
    parser.add_argument("--version", help="Filter by version substring")
    args = parser.parse_args()

    kind = "symbols" if args.symbol else args.kind
    results = search(
        args.query,
        kind=kind,
        top_k=args.top,
        status=_split_filter(args.status),
        category=_split_filter(args.category),
        version=args.version,
    )
    payload = {
        "query": args.query,
        "kind": kind,
        "filters": {
            "status": _split_filter(args.status),
            "category": _split_filter(args.category),
            "version": args.version,
        },
        "results": results,
    }
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return

    print(f"query: {args.query}")
    for index, result in enumerate(results, 1):
        if result["kind"] == "chunk":
            print(f"{index}. [{result['score']:.3f}] {result['path']}:{result['lines']}")
            print(f"   {' > '.join(result['heading_path'])}")
            print(f"   status={result['status']} category={result['category']} version={result['version_scope']}")
            print(f"   {result['snippet']}")
        else:
            print(f"{index}. [{result['score']:.3f}] {result['qualified_name']} ({result['symbol_kind']})")
            print(f"   {result['path']}:{result['lines']}")
            print(f"   {result['signature']}")
        if index < len(results):
            print()


if __name__ == "__main__":
    main()
