from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from parse_markdown import parse_markdown_document  # noqa: E402


class MarkdownParserTest(unittest.TestCase):
    def test_heading_chunks_preserve_paths_and_lines(self) -> None:
        content = """# 示例文档

简介段落。

## 第一节

第一节内容。

### 细节

代码块：

```csharp
void Update()
{
}
```

## 第二节

第二节内容。
"""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.md"
            path.write_text(content, encoding="utf-8")
            metadata = {
                "id": "sample",
                "content_path": "tests/sample.md",
                "title": "示例文档",
                "status": "reviewed",
                "category": "client-engine",
                "difficulty": "intermediate",
                "summary": "示例摘要",
                "version_scope": ["Unity 2019.4"],
                "tags": ["unity"],
                "aliases": [],
                "code_paths": [],
                "test_paths": [],
                "reviewed_at": None,
            }
            catalog, chunks = parse_markdown_document(path, metadata)

        self.assertEqual(catalog["section_count"], len(chunks))
        by_heading = {chunk["heading"]: chunk for chunk in chunks}
        self.assertEqual(by_heading["细节"]["heading_path"], ["示例文档", "第一节", "细节"])
        self.assertIn("void Update()", by_heading["细节"]["text"])
        self.assertLess(by_heading["第一节"]["start_line"], by_heading["细节"]["start_line"])
        self.assertEqual(by_heading["第二节"]["heading_path"], ["示例文档", "第二节"])

    def test_long_section_is_split_without_breaking_fence(self) -> None:
        body = "\n\n".join(f"段落 {i} " + "内容" * 120 for i in range(10))
        content = "# 文档\n\n## 长章节\n\n" + body + "\n\n```csharp\n" + "var x = 1;\n" * 80 + "```\n"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "long.md"
            path.write_text(content, encoding="utf-8")
            metadata = {
                "id": "long",
                "content_path": "tests/long.md",
                "title": "文档",
                "status": "summary",
                "category": "client-engine",
                "difficulty": "intermediate",
                "summary": "长文档",
                "version_scope": [],
                "tags": [],
                "aliases": [],
                "code_paths": [],
                "test_paths": [],
                "reviewed_at": None,
            }
            _, chunks = parse_markdown_document(path, metadata, max_chars=900)

        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertEqual(chunk["text"].count("```") % 2, 0)


if __name__ == "__main__":
    unittest.main()
