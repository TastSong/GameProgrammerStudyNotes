from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_symbols import parse_csharp  # noqa: E402


class SymbolParserTest(unittest.TestCase):
    def test_parses_types_methods_and_constructor(self) -> None:
        source = """using UnityEngine;

namespace Demo
{
    public class Example : MonoBehaviour
    {
        public Example()
        {
        }

        public void Run(int value)
        {
            if (value > 0)
            {
                Debug.Log(value);
            }
        }

        private static int Answer() => 42;
    }
}
"""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Example.cs"
            path.write_text(source, encoding="utf-8")
            symbols = parse_csharp(path, [{"id": "demo-note", "code_paths": [temp]}])

        qualified = {symbol["qualified_name"]: symbol for symbol in symbols}
        self.assertIn("Demo.Example", qualified)
        self.assertIn("Demo.Example.Example", qualified)
        self.assertIn("Demo.Example.Run", qualified)
        self.assertIn("Demo.Example.Answer", qualified)
        self.assertEqual(qualified["Demo.Example.Run"]["related_doc_ids"], ["demo-note"])
        self.assertGreater(qualified["Demo.Example.Run"]["end_line"], qualified["Demo.Example.Run"]["start_line"])


if __name__ == "__main__":
    unittest.main()
