from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import AI_DIR
from search import search

CASES_PATH = AI_DIR / "tests" / "retrieval_cases.jsonl"


def load_cases(path: Path = CASES_PATH) -> list[dict[str, Any]]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def _chunk_match(result: dict[str, Any], case: dict[str, Any]) -> bool:
    if result["path"] not in case.get("expected_paths", []):
        return False
    headings = " ".join(result.get("heading_path", [])).casefold()
    expected_headings = [str(item).casefold() for item in case.get("expected_heading_any", [])]
    return not expected_headings or any(item in headings for item in expected_headings)


def _symbol_match(result: dict[str, Any], case: dict[str, Any]) -> bool:
    expected = [str(item) for item in case.get("expected_symbols", [])]
    qualified = result.get("qualified_name", "")
    return qualified in expected or any(item in qualified for item in expected)


def evaluate_case(case: dict[str, Any], top_k: int) -> dict[str, Any]:
    kind = case.get("kind", "chunks")
    results = search(
        case["query"],
        kind=kind,
        top_k=top_k,
        status=case.get("status"),
        category=case.get("category"),
        version=case.get("version"),
    )
    rank = None
    for index, result in enumerate(results, 1):
        matched = _symbol_match(result, case) if kind == "symbols" else _chunk_match(result, case)
        if matched:
            rank = index
            break
    return {
        "id": case["id"],
        "query": case["query"],
        "kind": kind,
        "passed": rank is not None,
        "rank": rank,
        "top_results": [
            {
                "path": result.get("path"),
                "qualified_name": result.get("qualified_name"),
                "heading_path": result.get("heading_path"),
                "lines": result.get("lines"),
                "score": result.get("score"),
            }
            for result in results
        ],
    }


def evaluate(cases: list[dict[str, Any]], top_k: int) -> dict[str, Any]:
    details = [evaluate_case(case, top_k) for case in cases]
    passed = sum(1 for item in details if item["passed"])
    total = len(details)
    return {
        "top_k": top_k,
        "passed": passed,
        "total": total,
        "recall": round(passed / total, 4) if total else 0.0,
        "cases": details,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval against curated repository questions.")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--min-recall", type=float, default=0.8)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    args = parser.parse_args()

    report = evaluate(load_cases(args.cases), args.top)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"recall@{args.top}: {report['passed']}/{report['total']} = {report['recall']:.2%}")
        for item in report["cases"]:
            status = "PASS" if item["passed"] else "FAIL"
            rank = f"rank={item['rank']}" if item["rank"] else "not found"
            print(f"{status:4} {item['id']}: {rank} | {item['query']}")
            if not item["passed"]:
                for result in item["top_results"]:
                    print(f"     - {result['path']} {result.get('qualified_name') or ''} {result.get('heading_path') or ''}")
    if report["recall"] < args.min_recall:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
