# Retrieval Workflow

1. 先检查 `ai/indexes/manifest.json` 的 `source.content_fingerprint` 和当前索引状态。
2. 使用 `search.py` 检索相关章节。
3. 查看结果的 `status`、`version_scope`、`path` 和 `lines`。
4. 使用 `read_source.py` 读取原始片段。
5. 需要代码时，使用 `--symbol` 搜索代码符号并读取源文件。
6. 如果 Top 5 没有足够证据，再扩大范围；不要一开始读取全部文档。

## 检索升级顺序

1. 标题、标签、别名检索。
2. 全文 BM25 检索。
3. 元数据过滤后再检索。
4. 读取 `graph.json` 查找关联代码和文档。
5. 仍无结果时，才允许按目录浏览原文。

## 结果不足时

回答必须说明：

- 检索没有找到足够证据。
- 当前只能提供通用建议。
- 哪些内容尚未验证。
- 下一步需要测试或补充哪些资料。
