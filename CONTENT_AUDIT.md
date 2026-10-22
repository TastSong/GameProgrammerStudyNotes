# 内容状态与质量清单

本文件用于区分完整笔记、专题摘要和章节提纲，并记录已修正的技术问题与仍需人工复核的内容。

## 状态定义

- **完整笔记**：包含概念解释、实现思路或案例，能够独立阅读。
- **专题摘要**：保留主要内容与结论，但省略推导、代码或完整案例。
- **章节提纲**：主要用于列出目录、章节顺序和阅读索引，尚不足以替代正文学习。

## 当前分布

| 文档组 | 状态 | 说明 |
| --- | --- | --- |
| `ProfessionalUnity3D` | 完整笔记 | 10 个章节，约 4,000 行，包含原理、代码片段与图示。 |
| `Refactoring`、`QFramework` | 完整笔记 | 篇幅较长，包含结构与代码案例。 |
| `MicroservicesPatterns`、`DesigningDataIntensiveApplications`、`MathematicsFor3DGameProgrammingAndComputerGraphics` | 专题摘要 | 主题覆盖较完整，但仍属于对原书的提炼。 |
| `GameProgrammingPatterns` | 模式摘要加示例 | 每种模式篇幅较短，需结合 Unity 场景或原始资料阅读。 |
| `GameEngineArchitecture`、`UnityShader`、`UnityNetworkGame`、`TencentGameDevelopment3` | 专题摘要 | 具备章节结构和主要内容，部分章节仍依赖配图。 |
| `TheGameServerArchitectureAndOptimization`、`TencentGameDevelopment1`、`Butterfly` | 章节提纲 | 当前主要是目录或核心观点，尚未展开为完整笔记。 |
| `ColdStart`、`AgenticDesignPatterns`、`TheArtofComputerProgramming` | 简要摘要 | 适合作为阅读索引，技术或案例细节有限。 |
| 其余书籍笔记 | 专题摘要或提纲 | 深度差异较大，阅读时需结合文首状态判断。 |

## 一致性规范

- 根 README 仅保留一个一级标题，各书籍和专题使用二级标题。
- 本地相对链接统一使用正斜杠 `/`，避免 Windows 反斜杠在 GitHub 上失效。
- Unity 框架名称统一写为 `QFramework`，C# 章节统一写为 `C# 技术要点`。
- 罗马数字章节编号统一使用 `I`、`II`、`III`。
- 同一章节的标题、根 README 链接文字和正文标题应保持一致。
- 历史目录名和文件名为兼容旧链接暂时保留，后续移动时需要同步更新所有引用。

## 本轮专项校对

- 根 README 从 35 个一级标题整理为 1 个一级标题和 35 个二级标题。
- 统一根 README 中 QFramework、Unity、C#、3D 和罗马数字的标题格式。
- 修正 ProfessionalUnity3D 第二章、第四章、第五章、第六章和第七章的标题层级与名称。
- 将 18 处 Windows 反斜杠相对链接改为跨平台正斜杠格式。
- 将 `Reconsitution` 重复正文收敛为历史兼容入口，只保留指向 `UnityGameOptimization` 的链接。

## OCR 与结构清理

- 清理 46 篇文档中由 OCR 和 PDF 断行产生的 1,100 余行中文词间空格。
- 移除 39 个零宽 BOM 字符，并压缩代码块外的 308 处连续空行。
- 补齐全部文档的一级标题，修复标题层级跳级、空标题和模式笔记重复标题。
- 重建 `ColdStart` 中被空行和列表符号打散的结构。
- 恢复 Tencent II 的正常章节层级，去掉标题外层的列表标记和重复一级标题。
- 将 `GameProgrammingPatterns/README_GameProgrammingPatterns.md` 重命名为标准 `README.md`。
- 修正 Unity VR、游戏感、Unity 优化、网络层等文档中的重复字、OCR 错字、英文技术词和 API 拼写。

## 本次已修正

- 将 `Reconsitution` 重复正文收敛为历史兼容入口，只保留唯一维护入口。
- 修正根 README 中的 OCR 错词、模式描述和失效导航。
- 将 SOLID 从错误的“六大原则”修正为五个原则，并把迪米特法则明确标记为补充原则。
- 修正命令模式示例中的全角分号，使代码片段可直接编译。
- 修正 `foreach` 堆分配、`Array.Sort` 算法和 `List<T>` 性能的绝对化表述。
- 修正帧同步示例中的单位换算和集合遍历顺序表述。
- 修正数学笔记中的乱码标题，以及 Unity VR 章节中的明显 OCR 错误。
- 为 Unity 示例补充工程版本、场景使用方式和示例完整度说明，并恢复标准 `README.md` 文件名。

## 仍需人工复核

- Unity 2019、Unity 5 和老版 Mono 相关的性能结论需要按具体版本重新验证。
- 书摘、封面和截图可能涉及第三方版权，需确认仓库发布范围和授权来源。
- 长文中仍可能存在 OCR 错字、术语不统一或章节编号问题，需要逐篇校对。
- 部分表格和公式使用纯文本排版，在 GitHub 之外的工具中可能需要重新格式化。
- `GameFell` 和历史图片文件名仍使用旧拼写，改名时需要同步处理外部链接。
