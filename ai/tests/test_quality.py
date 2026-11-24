from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_repo import run_checks  # noqa: E402
from evaluate_retrieval import evaluate, load_cases  # noqa: E402
from validate_indexes import validate as validate_indexes  # noqa: E402


class QualityGateTest(unittest.TestCase):
    def test_repository_links_and_adapters(self) -> None:
        self.assertEqual(run_checks(), [])

    def test_indexes_are_valid(self) -> None:
        self.assertEqual(validate_indexes(), [])

    def test_retrieval_recall(self) -> None:
        report = evaluate(load_cases(), top_k=5)
        self.assertGreaterEqual(report["recall"], 0.8, report)


if __name__ == "__main__":
    unittest.main()
