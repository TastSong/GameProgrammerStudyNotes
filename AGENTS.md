# Repository Agent Guide

本仓库是中文游戏开发知识库。处理任何任务前：

1. 完整阅读 `ai/README.md` 与 `ai/instructions/core.md`。
2. 检查索引是否最新：

   ```bash
   python3 ai/scripts/build_index.py --check
   ```

3. 查询仓库知识时必须先使用：

   ```bash
   python3 ai/scripts/search.py "问题" --json
   ```

4. 回答前必须用 `read_source.py` 读取命中的原始内容。
5. 回答必须引用原始路径和行号，格式为 `[path:start-end]`。
6. `ai/indexes/` 是生成文件，禁止手工编辑。
7. 修改文档、代码或元数据后，必须重新生成索引并提交索引变化。
8. `outline`、`stale`、`draft` 内容只能作为线索，必须明确提示限制。
9. 不要默认扫描整个仓库；先检索，再按需读取。
10. 无法运行 Unity 或测试时，必须明确说明未验证，不能声称已验证。
