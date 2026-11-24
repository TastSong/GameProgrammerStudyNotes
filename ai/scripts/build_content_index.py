from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    INDEX_DIR,
    iter_documents,
    load_all_metadata,
    relative_path,
    write_jsonl,
)
from parse_markdown import parse_markdown_document


def build(output_dir: Path = INDEX_DIR) -> tuple[int, int]:
    metadata = load_all_metadata()
    by_path = {str(item["content_path"]): item for item in metadata}
    catalogs = []
    chunks = []
    for path in iter_documents():
        rel = relative_path(path)
        meta = by_path.get(rel)
        if meta is None:
            raise SystemExit(f"missing metadata for {rel}")
        catalog, doc_chunks = parse_markdown_document(path, meta)
        catalogs.append(catalog)
        chunks.extend(doc_chunks)

    catalogs.sort(key=lambda item: item["id"])
    chunks.sort(key=lambda item: (item["content_path"], item["start_line"], item["id"]))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "catalog.jsonl", catalogs)
    write_jsonl(output_dir / "chunks.jsonl", chunks)
    return len(catalogs), len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the document catalog and heading-aware chunk index.")
    parser.add_argument("--output-dir", type=Path, default=INDEX_DIR)
    args = parser.parse_args()
    docs, chunks = build(args.output_dir)
    print(f"catalog records: {docs}")
    print(f"chunks: {chunks}")
    print(f"output: {args.output_dir}")


if __name__ == "__main__":
    main()
