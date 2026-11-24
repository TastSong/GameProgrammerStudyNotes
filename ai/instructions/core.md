# Core Agent Instructions

本仓库是中文游戏开发知识库。原始 Markdown、C# 源码和实际测试是唯一事实来源；
`ai/meta/` 是人工维护的元数据，`ai/indexes/` 是派生索引。

## 引用的具体规范

@ai/instructions/retrieval.md
@ai/instructions/citation.md
@ai/instructions/editing.md
@ai/instructions/review.md
@ai/agent-contract.yaml

## 共同原则

1. 先检索，再读取命中的原文，不要默认扫描整个仓库。
2. 回答仓库内事实时必须引用原始路径和行号。
3. 索引、摘要和 `snippet` 只用于定位，不能代替原文。
4. 修改文档、代码或元数据后必须重新生成索引。
5. 不手工编辑 `ai/indexes/` 中的生成文件。
6. 无法运行 Unity 或测试时，必须明确说明未验证。
7. 不读取或提交密钥、令牌、私钥和个人凭据。
8. 历史重写、强制推送和删除分支必须得到用户明确要求。
9. `ai/runtime/` 只存放本地缓存，不提交。
