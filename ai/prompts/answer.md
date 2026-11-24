# Answer Prompt Template

用户问题：

```text
{{question}}
```

执行步骤：

1. 使用 `search.py` 检索索引。
2. 使用 `read_source.py` 读取命中的原始内容。
3. 必要时使用 `search.py --symbol` 查找代码。
4. 只依据读取到的原文回答。
5. 给出结论、原因、版本条件、验证建议和引用。

引用格式：

```text
[path:start_line-end_line]
```

如果证据不足，明确说明不足，不要补写未经验证的事实。
