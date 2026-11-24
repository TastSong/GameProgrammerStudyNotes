from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_index import INDEX_FILES, build  # noqa: E402


class BuildIndexTest(unittest.TestCase):
    def test_build_is_deterministic_and_complete(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_manifest = build(Path(first))
            second_manifest = build(Path(second))
            self.assertEqual(first_manifest, second_manifest)
            for name in INDEX_FILES:
                self.assertTrue((Path(first) / name).exists(), name)
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())
            graph = json.loads((Path(first) / "graph.json").read_text(encoding="utf-8"))
            aliases = json.loads((Path(first) / "aliases.json").read_text(encoding="utf-8"))
            self.assertGreater(len(graph["nodes"]), 0)
            self.assertTrue(any(group["canonical"] == "对象池" for group in aliases["groups"]))


if __name__ == "__main__":
    unittest.main()
