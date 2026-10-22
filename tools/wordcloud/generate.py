from __future__ import annotations

import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "Pictures" / "wordcloud"
PNG_PATH = OUTPUT_DIR / "game-programming-knowledge-wordcloud.png"
SVG_PATH = OUTPUT_DIR / "game-programming-knowledge-wordcloud.svg"

WIDTH = 2400
HEIGHT = 1600
SEED = 20261022

BACKGROUND = "#F4F7F8"
INK = "#18272D"
MUTED = "#5E7078"
RULE = "#D8E1E4"

CATEGORIES = {
    "engine": ("引擎与图形", "#0F766E"),
    "architecture": ("架构与设计", "#C2410C"),
    "network": ("网络与服务端", "#BE123C"),
    "engineering": ("工程质量", "#15803D"),
    "math_ai": ("数学与 AI", "#5B5BD6"),
}


@dataclass(frozen=True)
class Term:
    canonical: str
    aliases: tuple[str, ...]
    category: str


@dataclass(frozen=True)
class ScoredTerm:
    text: str
    category: str
    score: float
    count: int
    breadth: int


TERMS = [
    Term("Unity", ("Unity", "Unity3D", "Unity 3D"), "engine"),
    Term("Shader", ("Shader", "着色器"), "engine"),
    Term("渲染", ("渲染",), "engine"),
    Term("渲染管线", ("渲染管线",), "engine"),
    Term("图形学", ("图形学",), "engine"),
    Term("GPU", ("GPU",), "engine"),
    Term("CPU", ("CPU",), "engine"),
    Term("Draw Call", ("Draw Call", "Drawcall", "绘制调用"), "engine"),
    Term("纹理", ("纹理",), "engine"),
    Term("光照", ("光照",), "engine"),
    Term("PBR", ("PBR", "基于物理的渲染"), "engine"),
    Term("HDRP", ("HDRP",), "engine"),
    Term("URP", ("URP",), "engine"),
    Term("后处理", ("后处理", "Post Processing"), "engine"),
    Term("阴影", ("阴影", "Shadow"), "engine"),
    Term("批处理", ("批处理", "Batching"), "engine"),
    Term("Mipmap", ("Mipmap", "MipMap"), "engine"),
    Term("抗锯齿", ("抗锯齿", "MSAA", "Anti-Aliasing"), "engine"),
    Term("模型", ("模型",), "engine"),
    Term("动画", ("动画",), "engine"),
    Term("骨骼动画", ("骨骼动画", "SkinnedMeshRenderer"), "engine"),
    Term("相机", ("相机", "摄像机"), "engine"),
    Term("屏幕空间", ("屏幕空间", "Screen Space"), "engine"),
    Term("渲染目标", ("渲染目标", "Render Target"), "engine"),
    Term("AssetBundle", ("AssetBundle",), "engine"),
    Term("LOD", ("LOD", "Level of Detail"), "engine"),
    Term("空间分区", ("空间分区", "Spatial Partition"), "engine"),
    Term("架构", ("架构",), "architecture"),
    Term("设计模式", ("设计模式", "Design Pattern"), "architecture"),
    Term("命令模式", ("命令模式", "Command Pattern"), "architecture"),
    Term("状态模式", ("状态模式", "State Pattern"), "architecture"),
    Term("观察者模式", ("观察者模式", "Observer Pattern"), "architecture"),
    Term("单例模式", ("单例模式", "Singleton Pattern"), "architecture"),
    Term("组件模式", ("组件模式", "Component Pattern"), "architecture"),
    Term("对象池", ("对象池", "Object Pool"), "architecture"),
    Term("事件队列", ("事件队列", "Event Queue"), "architecture"),
    Term("服务定位器", ("服务定位器", "Service Locator"), "architecture"),
    Term("数据局部性", ("数据局部性", "Data Locality"), "architecture"),
    Term("脏标记", ("脏标记", "脏标识", "Dirty Flag"), "architecture"),
    Term("双缓冲", ("双缓冲", "Double Buffer"), "architecture"),
    Term("游戏循环", ("游戏循环", "Game Loop"), "architecture"),
    Term("更新方法", ("更新方法", "Update Method"), "architecture"),
    Term("字节码", ("字节码", "Bytecode"), "architecture"),
    Term("类型对象", ("类型对象", "Type Object"), "architecture"),
    Term("子类沙箱", ("子类沙箱", "Subclass Sandbox"), "architecture"),
    Term("享元模式", ("享元模式", "Flyweight"), "architecture"),
    Term("原型模式", ("原型模式", "Prototype Pattern"), "architecture"),
    Term("游戏感", ("游戏感", "Game Feel"), "architecture"),
    Term("用户体验", ("用户体验", "UX"), "architecture"),
    Term("交互设计", ("交互设计", "Interaction Design"), "architecture"),
    Term("反馈", ("反馈",), "architecture"),
    Term("系统设计", ("系统设计", "System Design"), "architecture"),
    Term("可维护性", ("可维护性",), "architecture"),
    Term("可扩展性", ("可扩展性",), "architecture"),
    Term("网络", ("网络",), "network"),
    Term("TCP", ("TCP",), "network"),
    Term("UDP", ("UDP",), "network"),
    Term("Socket", ("Socket", "套接字"), "network"),
    Term("HTTP", ("HTTP",), "network"),
    Term("服务端", ("服务端", "服务器端"), "network"),
    Term("客户端", ("客户端",), "network"),
    Term("网关", ("网关", "Gateway"), "network"),
    Term("RPC", ("RPC",), "network"),
    Term("Actor", ("Actor",), "network"),
    Term("ECS", ("ECS", "Entity Component System"), "network"),
    Term("帧同步", ("帧同步", "Lockstep"), "network"),
    Term("状态同步", ("状态同步", "State Sync"), "network"),
    Term("分布式", ("分布式",), "network"),
    Term("Redis", ("Redis",), "network"),
    Term("数据库", ("数据库",), "network"),
    Term("MySQL", ("MySQL",), "network"),
    Term("MongoDB", ("MongoDB",), "network"),
    Term("消息队列", ("消息队列", "Message Queue"), "network"),
    Term("微服务", ("微服务", "Microservice"), "network"),
    Term("消息代理", ("消息代理", "Message Broker"), "network"),
    Term("一致性", ("一致性",), "network"),
    Term("可用性", ("可用性",), "network"),
    Term("热更新", ("热更新",), "network"),
    Term("负载均衡", ("负载均衡", "Load Balancing"), "network"),
    Term("重构", ("重构", "Refactoring"), "engineering"),
    Term("测试", ("测试",), "engineering"),
    Term("单元测试", ("单元测试", "Unit Test"), "engineering"),
    Term("代码规范", ("代码规范", "Clean Code"), "engineering"),
    Term("命名", ("命名",), "engineering"),
    Term("函数", ("函数",), "engineering"),
    Term("接口", ("接口",), "engineering"),
    Term("依赖倒置", ("依赖倒置", "Dependency Inversion"), "engineering"),
    Term("开闭原则", ("开闭原则", "Open Closed"), "engineering"),
    Term("单一职责", ("单一职责", "Single Responsibility"), "engineering"),
    Term("SOLID", ("SOLID",), "engineering"),
    Term("性能优化", ("性能优化", "性能调优", "Optimization"), "engineering"),
    Term("内存", ("内存",), "engineering"),
    Term("GC", ("GC", "垃圾回收"), "engineering"),
    Term("缓存", ("缓存",), "engineering"),
    Term("协程", ("协程", "Coroutine"), "engineering"),
    Term("多线程", ("多线程",), "engineering"),
    Term("异步", ("异步",), "engineering"),
    Term("调试", ("调试", "Debug"), "engineering"),
    Term("性能分析", ("性能分析", "Profiler"), "engineering"),
    Term("版本控制", ("版本控制", "Git"), "engineering"),
    Term("架构演化", ("架构演化", "架构演进"), "engineering"),
    Term("数学", ("数学",), "math_ai"),
    Term("向量", ("向量", "Vector"), "math_ai"),
    Term("矩阵", ("矩阵", "Matrix"), "math_ai"),
    Term("四元数", ("四元数", "Quaternion"), "math_ai"),
    Term("物理", ("物理",), "math_ai"),
    Term("碰撞检测", ("碰撞检测",), "math_ai"),
    Term("刚体", ("刚体", "Rigidbody"), "math_ai"),
    Term("寻路", ("寻路", "Pathfinding"), "math_ai"),
    Term("导航", ("导航", "NavMesh"), "math_ai"),
    Term("行为树", ("行为树", "Behavior Tree"), "math_ai"),
    Term("状态机", ("状态机", "State Machine"), "math_ai"),
    Term("AI", ("AI", "人工智能"), "math_ai"),
    Term("机器学习", ("机器学习", "Machine Learning"), "math_ai"),
    Term("强化学习", ("强化学习", "Reinforcement Learning"), "math_ai"),
    Term("神经网络", ("神经网络", "Neural Network"), "math_ai"),
    Term("搜索算法", ("搜索算法", "A*", "A星"), "math_ai"),
    Term("图论", ("图论", "Graph Theory"), "math_ai"),
    Term("动态规划", ("动态规划", "Dynamic Programming"), "math_ai"),
    Term("数据模型", ("数据模型", "Data Model"), "math_ai"),
    Term("数据分析", ("数据分析", "Data Analysis"), "math_ai"),
    Term("流处理", ("流处理", "Stream Processing"), "math_ai"),
]


def clean_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_~>|]", " ", text)
    return re.sub(r"\s+", " ", text)


def alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias)
    if re.search(r"[A-Za-z0-9]", alias):
        escaped = rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])"
    return re.compile(escaped, flags=re.I)


def load_documents() -> list[tuple[Path, str]]:
    docs: list[tuple[Path, str]] = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if "Library" in relative.parts or path.name == "CONTENT_AUDIT.md":
            continue
        docs.append((path, clean_markdown(path.read_text(encoding="utf-8"))))
    return docs


def score_terms(docs: list[tuple[Path, str]]) -> list[ScoredTerm]:
    scored: list[ScoredTerm] = []
    total_docs = len(docs)
    for term in TERMS:
        total = 0.0
        breadth = 0
        patterns = [alias_pattern(alias) for alias in term.aliases]
        for path, text in docs:
            count = sum(len(pattern.findall(text)) for pattern in patterns)
            if count:
                breadth += 1
                total += count * (0.22 if path == ROOT / "README.md" else 1.0)
        if total <= 0:
            continue
        breadth_factor = 1.0 + 0.28 * math.log1p(breadth)
        distribution_factor = 0.85 + 0.15 * math.sqrt(breadth / total_docs)
        scored.append(
            ScoredTerm(
                text=term.canonical,
                category=term.category,
                score=total * breadth_factor * distribution_factor,
                count=int(round(total)),
                breadth=breadth,
            )
        )
    return sorted(scored, key=lambda item: item.score, reverse=True)


def pick_font(size: int, bold: bool) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\Deng.ttf"),
    ]
    for path in candidates:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size, index=0)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def text_metrics(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top, -left


def intersects(candidate: tuple[int, int, int, int], placed: list[tuple[int, int, int, int]]) -> bool:
    x0, y0, x1, y1 = candidate
    for px0, py0, px1, py1 in placed:
        if x0 < px1 and x1 > px0 and y0 < py1 and y1 > py0:
            return True
    return False


def layout_terms(terms: list[ScoredTerm]) -> list[dict[str, object]]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    rng = random.Random(SEED)

    cloud = (130, 330, WIDTH - 130, 1370)
    cx = (cloud[0] + cloud[2]) / 2
    cy = (cloud[1] + cloud[3]) / 2

    positive = [term.score for term in terms]
    low = math.log1p(min(positive))
    high = math.log1p(max(positive))

    placed_boxes: list[tuple[int, int, int, int]] = []
    placements: list[dict[str, object]] = []

    for term in terms:
        raw = (math.log1p(term.score) - low) / max(high - low, 1.0)
        base_size = round(23 + 99 * (raw**0.84))
        chosen: dict[str, object] | None = None

        for size in (base_size, base_size - 5, base_size - 10):
            if size < 20:
                continue
            font = pick_font(size, size >= 44)
            width, height, offset_x = text_metrics(draw, term.text, font)
            margin = 11
            max_radius = 760 + rng.random() * 40
            phase = rng.random() * math.tau

            for index in range(9000):
                progress = index / 9000
                radius = max_radius * math.sqrt(progress)
                angle = phase + index * 2.399963229728653
                x = round(cx + radius * math.cos(angle) * 1.48 - width / 2)
                y = round(cy + radius * math.sin(angle) * 0.74 - height / 2)
                box = (x - margin, y - margin, x + width + margin, y + height + margin)
                if box[0] < cloud[0] or box[1] < cloud[1] or box[2] > cloud[2] or box[3] > cloud[3]:
                    continue
                if intersects(box, placed_boxes):
                    continue
                chosen = {
                    "text": term.text,
                    "category": term.category,
                    "count": term.count,
                    "breadth": term.breadth,
                    "size": size,
                    "x": x + offset_x,
                    "y": y,
                    "width": width,
                    "height": height,
                }
                placed_boxes.append(box)
                break
            if chosen:
                break

        if chosen:
            placements.append(chosen)

    return placements


def draw_png(
    placements: list[dict[str, object]],
    document_count: int,
    line_count: int,
) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    title_font = pick_font(78, True)
    subtitle_font = pick_font(30, False)
    legend_font = pick_font(24, False)
    meta_font = pick_font(21, False)
    body_fonts: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}

    draw.text((124, 86), "游戏程序员学习知识图谱", font=title_font, fill=INK)
    subtitle = f"基于 {document_count} 篇笔记 · {line_count:,} 行内容的主题词云"
    draw.text((128, 194), subtitle, font=subtitle_font, fill=MUTED)
    draw.line((124, 274, WIDTH - 124, 274), fill=RULE, width=2)

    for placement in placements:
        size = int(placement["size"])
        key = (size, size >= 44)
        if key not in body_fonts:
            body_fonts[key] = pick_font(size, size >= 44)
        color = CATEGORIES[str(placement["category"])][1]
        draw.text(
            (int(placement["x"]), int(placement["y"])),
            str(placement["text"]),
            font=body_fonts[key],
            fill=color,
        )

    legend_items = list(CATEGORIES.values())
    item_widths = [draw.textlength(label, font=legend_font) + 34 for label, _ in legend_items]
    total_width = int(sum(item_widths) + 52 * (len(legend_items) - 1))
    cursor_x = (WIDTH - total_width) // 2
    legend_y = 1438

    for index, (label, color) in enumerate(legend_items):
        draw.rounded_rectangle((cursor_x, legend_y + 4, cursor_x + 18, legend_y + 22), radius=4, fill=color)
        draw.text((cursor_x + 28, legend_y), label, font=legend_font, fill=INK)
        cursor_x += int(item_widths[index] + 52)

    draw.line((124, 1512, WIDTH - 124, 1512), fill=RULE, width=1)
    draw.text((126, 1532), "按主题分类着色 · 字号表示内容权重 · 颜色仅用于区分类别", font=meta_font, fill=MUTED)
    draw.text((WIDTH - 712, 1532), "TastSong / GameProgrammerStudyNotes", font=meta_font, fill=MUTED)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(PNG_PATH, format="PNG", optimize=True)


def draw_svg(
    placements: list[dict[str, object]],
    document_count: int,
    line_count: int,
) -> None:
    legend_items = list(CATEGORIES.values())
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        "<title>游戏程序员学习知识图谱</title>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>',
        '<g font-family="Microsoft YaHei, Noto Sans SC, sans-serif">',
        f'<text x="124" y="154" font-size="78" font-weight="700" fill="{INK}">游戏程序员学习知识图谱</text>',
        f'<text x="128" y="232" font-size="30" fill="{MUTED}">基于 {document_count} 篇笔记 · {line_count:,} 行内容的主题词云</text>',
        f'<line x1="124" y1="274" x2="{WIDTH - 124}" y2="274" stroke="{RULE}" stroke-width="2"/>',
    ]

    for placement in placements:
        color = CATEGORIES[str(placement["category"])][1]
        size = int(placement["size"])
        svg.append(
            f'<text x="{placement["x"]}" y="{placement["y"]}" font-size="{size}" '
            f'font-weight="{"700" if size >= 44 else "400"}" fill="{color}" '
            f'dominant-baseline="text-before-edge">{escape(str(placement["text"]))}</text>'
        )

    legend_width = 280
    total_width = legend_width * len(legend_items)
    cursor_x = (WIDTH - total_width) // 2
    for label, color in legend_items:
        svg.append(f'<rect x="{cursor_x}" y="1442" width="18" height="18" rx="4" fill="{color}"/>')
        svg.append(f'<text x="{cursor_x + 28}" y="1458" font-size="24" fill="{INK}">{escape(label)}</text>')
        cursor_x += legend_width

    svg.extend(
        [
            f'<line x1="124" y1="1512" x2="{WIDTH - 124}" y2="1512" stroke="{RULE}" stroke-width="1"/>',
            f'<text x="126" y="1554" font-size="21" fill="{MUTED}">按主题分类着色 · 字号表示内容权重 · 颜色仅用于区分类别</text>',
            f'<text x="{WIDTH - 712}" y="1554" font-size="21" fill="{MUTED}">TastSong / GameProgrammerStudyNotes</text>',
            "</g>",
            "</svg>",
        ]
    )
    SVG_PATH.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    docs = load_documents()
    line_count = sum(len(path.read_text(encoding="utf-8").splitlines()) for path, _ in docs)
    scored = score_terms(docs)
    selected = scored[:84]
    placements = layout_terms(selected)

    print(f"Documents: {len(docs)}")
    print(f"Lines: {line_count}")
    print(f"Placed terms: {len(placements)}")
    print("Top terms:")
    for term in scored[:22]:
        print(f"  {term.text:12s} score={term.score:7.1f} count={term.count:4d} docs={term.breadth:2d}")

    draw_png(placements, len(docs), line_count)
    draw_svg(placements, len(docs), line_count)
    print(f"PNG: {PNG_PATH}")
    print(f"SVG: {SVG_PATH}")


if __name__ == "__main__":
    main()
