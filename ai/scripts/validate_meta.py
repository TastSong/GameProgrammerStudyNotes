from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from common import (
    META_DIR,
    NOTES_META_DIR,
    ROOT,
    iter_documents,
    load_yaml,
    path_exists,
    relative_path,
)

SCHEMA_PATH = ROOT / "ai" / "schemas" / "note.schema.json"


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate() -> list[str]:
    errors: list[str] = []
    schema = load_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    seen_ids: dict[str, str] = {}
    seen_paths: dict[str, str] = {}
    statuses: Counter[str] = Counter()
    categories: Counter[str] = Counter()

    for path in sorted(NOTES_META_DIR.glob("*.yaml")):
        try:
            record = load_yaml(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{relative_path(path)}: YAML parse error: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{relative_path(path)}: root must be an object")
            continue

        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"{relative_path(path)}:{location}: {error.message}")

        record_id = str(record.get("id", ""))
        content_path = str(record.get("content_path", ""))
        if record_id in seen_ids:
            errors.append(f"duplicate id {record_id!r}: {seen_ids[record_id]} and {relative_path(path)}")
        seen_ids[record_id] = relative_path(path)
        if content_path in seen_paths:
            errors.append(
                f"duplicate content_path {content_path!r}: {seen_paths[content_path]} and {relative_path(path)}"
            )
        seen_paths[content_path] = relative_path(path)

        if content_path and not path_exists(content_path):
            errors.append(f"{relative_path(path)}: content_path does not exist: {content_path}")
        for key in ("code_paths", "test_paths"):
            for target in record.get(key, []):
                if not path_exists(target):
                    errors.append(f"{relative_path(path)}: {key} target does not exist: {target}")

        statuses[str(record.get("status"))] += 1
        categories[str(record.get("category"))] += 1

    document_paths = {relative_path(path) for path in iter_documents()}
    missing_metadata = sorted(document_paths - set(seen_paths))
    orphan_metadata = sorted(set(seen_paths) - document_paths)
    errors.extend(f"missing metadata for document: {path}" for path in missing_metadata)
    errors.extend(f"metadata points to unknown document: {path}" for path in orphan_metadata)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return errors

    print(f"metadata records: {len(seen_ids)}")
    print(f"documents: {len(document_paths)}")
    print("status:", ", ".join(f"{key}={value}" for key, value in sorted(statuses.items())))
    print("category:", ", ".join(f"{key}={value}" for key, value in sorted(categories.items())))
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate note metadata against the JSON Schema and repository.")
    parser.parse_args()
    errors = validate()
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
