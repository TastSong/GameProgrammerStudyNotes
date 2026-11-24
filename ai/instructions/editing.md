# Editing Workflow

## 修改知识文档

1. 找到文档对应的元数据文件 `ai/meta/notes/*.yaml`。
2. 修改正文。
3. 更新 `summary`、`status` 和 `reviewed_at`。
4. 如果增加代码或测试，更新 `code_paths` 和 `test_paths`。
5. 运行：

   ```bash
   python3 ai/scripts/build_index.py
   python3 ai/scripts/build_index.py --check
   ```

6. 提交正文、元数据和索引变化。

## 新增文档

1. 按仓库现有目录放置 Markdown。
2. 运行：

   ```bash
   python3 ai/scripts/init_meta.py
   python3 ai/scripts/validate_meta.py
   python3 ai/scripts/build_index.py
   ```

3. 人工补充标题、摘要、版本、标签和来源。

## 禁止事项

- 不手工编辑 `ai/indexes/*.json*`。
- 不让索引与正文不一致。
- 不把未验证内容标成 `reviewed` 或 `verified`。
