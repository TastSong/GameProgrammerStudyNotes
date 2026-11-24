from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from build_index import source_fingerprint
from common import INDEX_DIR, ROOT, read_jsonl, read_text, sha256_text

SCHEMAS = {
    "catalog.jsonl": "catalog.schema.json",
    "chunks.jsonl": "chunk.schema.json",
    "symbols.jsonl": "symbol.schema.json",
}
JSON_FILES = {
    "aliases.json": None,
    "graph.json": "graph.schema.json",
    "manifest.json": "manifest.schema.json",
}


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((ROOT / "ai" / "schemas" / name).read_text(encoding="utf-8"))


def validate_schema(name: str, data: Any) -> list[str]:
    errors: list[str] = []
    schema_name = SCHEMAS.get(name) or JSON_FILES.get(name)
    if not schema_name:
        return errors
    validator = Draft202012Validator(load_schema(schema_name))
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{name}:{location}: {error.message}")
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    records: dict[str, list[dict[str, Any]]] = {}
    for name in SCHEMAS:
        path = INDEX_DIR / name
        if not path.exists():
            errors.append(f"missing index: {name}")
            continue
        items = read_jsonl(path)
        records[name] = items
        for item in items:
            errors.extend(validate_schema(name, item))

    for name in JSON_FILES:
        path = INDEX_DIR / name
        if not path.exists():
            errors.append(f"missing index: {name}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        errors.extend(validate_schema(name, data))

    catalogs = records.get("catalog.jsonl", [])
    chunks = records.get("chunks.jsonl", [])
    symbols = records.get("symbols.jsonl", [])
    doc_ids = {item["id"] for item in catalogs}
    doc_line_counts = {item["id"]: item["line_count"] for item in catalogs}

    if len(doc_ids) != len(catalogs):
        errors.append("catalog contains duplicate document IDs")
    chunk_ids = [item["id"] for item in chunks]
    if len(set(chunk_ids)) != len(chunk_ids):
        errors.append("chunks contain duplicate chunk IDs")
    for chunk in chunks:
        if chunk["doc_id"] not in doc_ids:
            errors.append(f"chunk {chunk['id']} references unknown document {chunk['doc_id']}")
        if chunk["end_line"] > doc_line_counts.get(chunk["doc_id"], 0):
            errors.append(f"chunk {chunk['id']} exceeds document line count")
        if chunk["start_line"] > chunk["end_line"]:
            errors.append(f"chunk {chunk['id']} has invalid line range")

    symbol_ids = [item["id"] for item in symbols]
    if len(set(symbol_ids)) != len(symbol_ids):
        errors.append("symbols contain duplicate IDs")
    for symbol in symbols:
        for doc_id in symbol.get("related_doc_ids", []):
            if doc_id not in doc_ids:
                errors.append(f"symbol {symbol['id']} references unknown document {doc_id}")

    catalog_by_path = {item["content_path"]: item for item in catalogs}
    for catalog in catalogs:
        path = ROOT / catalog["content_path"]
        if path.exists() and sha256_text(read_text(path)) != catalog["content_hash"]:
            errors.append(f"catalog content hash is stale: {catalog['content_path']}")
        metadata_path = catalog.get("metadata_path")
        if metadata_path and not (ROOT / metadata_path).exists():
            errors.append(f"catalog references missing metadata: {metadata_path}")
        if len([chunk for chunk in chunks if chunk["doc_id"] == catalog["id"]]) != catalog["section_count"]:
            errors.append(f"catalog section_count mismatch: {catalog['id']}")

    graph_path = INDEX_DIR / "graph.json"
    if graph_path.exists():
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        node_ids = {node["id"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            if edge["from"] not in node_ids or edge["to"] not in node_ids:
                errors.append(f"graph edge references unknown node: {edge}")

    manifest_path = INDEX_DIR / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_counts = {
            "catalog": len(catalogs),
            "chunks": len(chunks),
            "symbols": len(symbols),
        }
        for key, value in expected_counts.items():
            if manifest.get("counts", {}).get(key) != value:
                errors.append(f"manifest count mismatch for {key}")
        fingerprint, _ = source_fingerprint()
        if manifest.get("source", {}).get("content_fingerprint") != fingerprint:
            errors.append("manifest content fingerprint is stale")
        for name, info in manifest.get("files", {}).items():
            path = INDEX_DIR / name
            if not path.exists():
                errors.append(f"manifest references missing file: {name}")
                continue
            if sha256_text(path.read_text(encoding="utf-8")) != info.get("sha256"):
                errors.append(f"manifest hash mismatch: {name}")
        if len(catalog_by_path) != len(catalogs):
            errors.append("catalog contains duplicate content paths")

    return errors


def main() -> None:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("index schemas, hashes and cross-references: OK")


if __name__ == "__main__":
    main()
