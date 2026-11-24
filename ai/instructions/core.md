# Core Agent Instructions

本仓库是一个中文游戏开发知识库。原始 Markdown、C# 源码和实际测试是唯一事实来源；
`ai/meta/` 是元数据，`ai/indexes/` 是派生索引。

## 开始任务前

1. 阅读 `ai/README.md` 和本文件。
2. 运行或确认索引状态：

   ```bash
   python3 ai/scripts/build_index.py --check
   ```

3. 如果索引缺失或过期，运行：

   ```bash
   python3 ai/scripts/build_index.py
   ```

4. 不要默认读取整个仓库。先检索，再读取命中内容。

## 检索仓库知识

优先使用：

```bash
python3 ai/scripts/search.py "问题" --json
```

需要代码符号时：

```bash
python3 ai/scripts/search.py "InputHandler Redo" --symbol --json
```

可根据目标版本和内容状态过滤：

```bash
python3 ai/scripts/search.py "对象池 GC" \
  --status reviewed,verified \
  --version "Unity 2022.3" \
  --json
```

## 回答前必须读取原文

检索结果只是定位信息。回答前必须使用：

```bash
python3 ai/scripts/read_source.py --chunk-id "<chunk_id>" --json
```

或：

```bash
python3 ai/scripts/read_source.py --path "<path>" --lines <start>-<end> --json
```

不能只根据 `summary`、`snippet` 或模型记忆作答。

## 引用格式

所有仓库内事实必须引用原始位置：

```text
[GameProgrammingPatterns/ObjectPool.md:20-28]
```

如果引用了代码，也应引用代码位置：

```text
[GameProgrammingPatterns/Assets/OptimizationPatterns/ObjectPool/Script/Core/PoolManager.cs:80-116]
```

版本差异、外部资料和模型推断必须明确标记。

## 内容状态规则

- `verified`、`reviewed`：可以作为主要依据，但仍要核对版本。
- `summary`：可以使用，但必须提示是摘要。
- `outline`：只能用于导航，不能当作完整结论。
- `draft`、`stale`：默认不能作为可靠依据，必须说明风险。

完整状态规则见 `ai/instructions/review.md`。

## 修改仓库内容

1. 修改 Markdown、代码或元数据。
2. 同步更新 `ai/meta/notes/<id>.yaml`。
3. 重新生成索引：

   ```bash
   python3 ai/scripts/build_index.py
   ```

4. 运行测试与检查。

5. 不得手工编辑 `ai/indexes/` 中的文件。

## 代码修改

- 优先修复被文档引用的最小示例。
- 修改后运行相关测试。
- 若当前环境无法运行 Unity，必须明确说明“未编译/未运行”，不能声称已验证。
- 不得为了让测试通过而隐藏错误或删除失败用例。

## 安全与边界

- 不读取或提交密钥、令牌、私钥和个人凭据。
- 不执行与任务无关的破坏性命令。
- 历史重写、强制推送和删除分支必须得到用户明确要求。
- `ai/runtime/` 只存放本地缓存，不提交。
