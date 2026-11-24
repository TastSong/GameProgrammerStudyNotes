from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Iterable

from build_content_index import build as build_content
from build_symbols import build as build_symbols
from common import (
    INDEX_DIR,
    META_DIR,
    ROOT,
    iter_csharp_files,
    iter_documents,
    load_all_metadata,
    load_yaml,
    relative_path,
    write_json,
)

INDEX_FILES = [
    "catalog.jsonl",
    "chunks.jsonl",
    "symbols.jsonl",
    "aliases.json",
    "graph.json",
    "manifest.json",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_aliases(metadata: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, dict[str, Any]] = {}

    glossary_path = META_DIR / "glossary.yaml"
    if glossary_path.exists():
        glossary = load_yaml(glossary_path) or {}
        for term in (glossary.get("terms") or {}).values():
            canonical = str(term.get("canonical", "")).strip()
            aliases = [str(item).strip() for item in term.get("aliases", []) if str(item).strip()]
            if canonical:
                groups[canonical.casefold()] = {
                    "canonical": canonical,
                    "aliases": sorted(set(aliases)),
                    "sources": ["glossary"],
                }

    for record in metadata:
        aliases = [str(item).strip() for item in record.get("aliases", []) if str(item).strip()]
        if not aliases:
            continue
        canonical = str(record["title"])
        key = canonical.casefold()
        group = groups.setdefault(
            key,
            {"canonical": canonical, "aliases": [], "sources": []},
        )
        group["aliases"] = sorted(set(group["aliases"]) | set(aliases))
        source = f"note:{record['id']}"
        if source not in group["sources"]:
            group["sources"].append(source)

    return {
        "schema_version": 1,
        "groups": sorted(groups.values(), key=lambda item: item["canonical"].casefold()),
    }


def _files_for_path(path_text: str, candidates: Iterable[Path]) -> list[Path]:
    base = (ROOT / path_text).resolve()
    result: list[Path] = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved == base or base in resolved.parents:
            result.append(candidate)
    return sorted(result)


def build_graph(metadata: list[dict[str, Any]], symbols: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: set[tuple[str, str, str]] = set()
    code_files = list(iter_csharp_files())
    referenced_tests: set[Path] = set()

    for record in metadata:
        doc_node = f"doc:{record['id']}"
        nodes[doc_node] = {
            "id": doc_node,
            "type": "note",
            "label": record["title"],
            "path": record["content_path"],
        }
        for code_path in record.get("code_paths", []):
            for file_path in _files_for_path(str(code_path), code_files):
                file_node = f"file:{relative_path(file_path)}"
                nodes[file_node] = {
                    "id": file_node,
                    "type": "code",
                    "label": file_path.name,
                    "path": relative_path(file_path),
                }
                edges.add((doc_node, file_node, "documents"))
        for test_path in record.get("test_paths", []):
            candidate = ROOT / str(test_path)
            if candidate.exists():
                referenced_tests.add(candidate)
                test_node = f"test:{relative_path(candidate)}"
                nodes[test_node] = {
                    "id": test_node,
                    "type": "test",
                    "label": candidate.name,
                    "path": relative_path(candidate),
                }
                edges.add((doc_node, test_node, "tested_by"))

    for file_path in code_files:
        file_node = f"file:{relative_path(file_path)}"
        nodes[file_node] = {
            "id": file_node,
            "type": "code",
            "label": file_path.name,
            "path": relative_path(file_path),
        }

    for symbol in symbols:
        symbol_node = f"symbol:{symbol['id']}"
        nodes[symbol_node] = {
            "id": symbol_node,
            "type": "symbol",
            "label": symbol["qualified_name"],
            "path": symbol["path"],
            "kind": symbol["kind"],
        }
        edges.add((symbol_node, f"file:{symbol['path']}", "defined_in"))

    return {
        "schema_version": 1,
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": [
            {"from": source, "to": target, "type": kind}
            for source, target, kind in sorted(edges)
        ],
    }


def source_fingerprint() -> tuple[str, dict[str, int]]:
    sources: list[Path] = []
    sources.extend(iter_documents())
    sources.extend(iter_csharp_files())
    sources.extend(sorted((META_DIR / "notes").glob("*.yaml")))
    glossary = META_DIR / "glossary.yaml"
    if glossary.exists():
        sources.append(glossary)

    digest = hashlib.sha256()
    for path in sorted(set(sources), key=lambda item: relative_path(item)):
        digest.update(relative_path(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest(), {
        "documents": len(list(iter_documents())),
        "csharp_files": len(list(iter_csharp_files())),
        "metadata_records": len(load_all_metadata()),
    }


def build(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = load_all_metadata()
    catalog_count, chunk_count = build_content(output_dir)
    symbols = build_symbols(output_dir)
    aliases = build_aliases(metadata)
    graph = build_graph(metadata, symbols)
    write_json(output_dir / "aliases.json", aliases)
    write_json(output_dir / "graph.json", graph)

    fingerprint, source_counts = source_fingerprint()
    file_info: dict[str, Any] = {}
    record_counts = {
        "catalog.jsonl": catalog_count,
        "chunks.jsonl": chunk_count,
        "symbols.jsonl": len(symbols),
        "aliases.json": len(aliases["groups"]),
        "graph.json": len(graph["nodes"]),
    }
    for name in INDEX_FILES:
        if name == "manifest.json":
            continue
        path = output_dir / name
        file_info[name] = {
            "sha256": sha256_bytes(path.read_bytes()),
            "records": record_counts[name],
        }

    manifest = {
        "schema_version": 1,
        "index_version": 1,
        "source": {
            "content_fingerprint": fingerprint,
            **source_counts,
        },
        "counts": {
            "catalog": catalog_count,
            "chunks": chunk_count,
            "symbols": len(symbols),
            "alias_groups": len(aliases["groups"]),
            "graph_nodes": len(graph["nodes"]),
            "graph_edges": len(graph["edges"]),
        },
        "files": file_info,
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def check() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as temp:
        generated = Path(temp)
        build(generated)
        for name in INDEX_FILES:
            expected = INDEX_DIR / name
            actual = generated / name
            if not expected.exists():
                errors.append(f"missing committed index: ai/indexes/{name}")
                continue
            if expected.read_bytes() != actual.read_bytes():
                errors.append(f"stale index: ai/indexes/{name}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or verify all AI indexes.")
    parser.add_argument("--output-dir", type=Path, default=INDEX_DIR)
    parser.add_argument("--check", action="store_true", help="Fail if committed indexes are stale.")
    args = parser.parse_args()

    if args.check:
        errors = check()
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print("indexes are up to date")
        return

    manifest = build(args.output_dir)
    counts = manifest["counts"]
    print(
        "indexed: "
        + ", ".join(f"{key}={value}" for key, value in counts.items())
    )
    print(f"fingerprint: {manifest['source']['content_fingerprint']}")
    print(f"output: {args.output_dir}")


if __name__ == "__main__":
    main()
