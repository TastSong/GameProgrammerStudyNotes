from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from read_source import find_chunk, read_lines, resolve_path  # noqa: E402
from search import search_chunks, search_symbols, tokenize  # noqa: E402


class SearchTest(unittest.TestCase):
    def test_tokenize_chinese_and_english(self) -> None:
        tokens = tokenize("Unity 对象池 GC Alloc")
        self.assertIn("unity", tokens)
        self.assertIn("对象池", tokens)
        self.assertIn("gc", tokens)

    def test_chunk_search_finds_object_pool(self) -> None:
        results = search_chunks("对象池 Object Pool", top_k=5)
        self.assertTrue(any(result["path"] == "GameProgrammingPatterns/ObjectPool.md" for result in results))

    def test_symbol_search_finds_redo(self) -> None:
        results = search_symbols("InputHandler Redo", top_k=5)
        self.assertTrue(any(result["qualified_name"] == "InputHandler.Redo" for result in results))

    def test_read_chunk_resolves_source_lines(self) -> None:
        results = search_chunks("对象池", top_k=1)
        chunk = find_chunk(results[0]["chunk_id"])
        source = read_lines(resolve_path(chunk["content_path"]), chunk["start_line"], chunk["end_line"])
        self.assertTrue(source["text"])
        self.assertEqual(source["path"], chunk["content_path"])


if __name__ == "__main__":
    unittest.main()
