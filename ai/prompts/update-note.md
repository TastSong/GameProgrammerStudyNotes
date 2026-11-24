# Update Note Prompt Template

更新知识文档时：

1. 保持正文自然可读，不把文章写成机器字段表。
2. 只给关键章节增加简短结论卡。
3. 将分类、状态、版本、来源和关联路径写入 `ai/meta/notes/`。
4. 代码和测试使用仓库相对路径。
5. 更新后运行：

   ```bash
   python3 ai/scripts/validate_meta.py
   python3 ai/scripts/build_index.py
   python3 ai/scripts/build_index.py --check
   ```
