# Generated Indexes

本目录中的文件由 `ai/scripts/build_index.py` 生成，请勿手工编辑。

- `catalog.jsonl`：文档目录
- `chunks.jsonl`：按标题切分的知识块
- `symbols.jsonl`：C# 类型和方法符号
- `aliases.json`：术语别名
- `graph.json`：文档、代码、测试与符号关系
- `manifest.json`：索引版本、文件哈希和内容指纹

本地 SQLite、向量和缓存文件应放在 `ai/runtime/`，不要提交。
