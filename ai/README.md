# AI Knowledge System

这个目录是仓库的机器可读层，供 AI Agent、检索脚本和维护工具使用。
人类阅读的原始 Markdown 与 Unity 源码仍然是唯一事实来源。

## 数据源优先级

1. 原始 Markdown、C# 源码和实际测试：最高优先级。
2. `ai/meta/`：人工维护的结构化元数据。
3. `ai/indexes/`：由脚本生成的派生索引，只用于定位和检索。

索引中的摘要不能替代原文。Agent 在回答前必须读取命中的原始文件片段。

## 目录说明

| 路径 | 用途 |
| --- | --- |
| `instructions/` | 所有 Agent 共用的核心行为规则 |
| `schemas/` | JSON Schema 与统一数据结构 |
| `meta/notes/` | 每篇文档的稳定 ID、状态、版本与关联关系 |
| `indexes/` | 可提交的文本索引和生成清单 |
| `scripts/` | 元数据校验、索引构建、检索、读取与评测工具 |
| `prompts/` | 可复用的回答、审阅和更新提示词 |
| `tests/` | 检索评测集与脚本测试 |
| `runtime/` | 本地缓存、SQLite、日志和临时文件，不提交 |

## 常用命令

```bash
python3 ai/scripts/validate_meta.py
python3 ai/scripts/build_index.py
python3 ai/scripts/build_index.py --check
python3 ai/scripts/search.py "对象池为什么产生 GC" --json
python3 ai/scripts/read_source.py \
  --path GameProgrammingPatterns/ObjectPool.md \
  --lines 1-40
```

## Agent 使用规则

1. 先阅读 `ai/instructions/core.md`。
2. 检查 `ai/indexes/manifest.json` 的 `content_fingerprint` 是否与当前仓库一致。
3. 优先调用 `search.py`，不要默认扫描整个仓库。
4. 回答必须引用原始文件路径和行号。
5. 修改文档、代码或元数据后运行 `build_index.py` 并提交索引变化。


## Agent 入口文件

- `AGENTS.md`：Codex / AGENTS 兼容 Agent
- `CLAUDE.md`：Claude Code
- `GEMINI.md`：Gemini Agent
- `.github/copilot-instructions.md`：GitHub Copilot
- `.cursor/rules/game-notes.mdc`：Cursor

这些文件都指向 `ai/instructions/core.md`，避免规则分散和漂移。

## 索引可复现性

索引文件使用稳定的 JSON 排序和相对路径，不包含当前时间。
相同输入应产生完全相同的索引文件，便于 CI 执行 `build_index.py --check`。
