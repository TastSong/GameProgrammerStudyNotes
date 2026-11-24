from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import (
    NOTES_META_DIR,
    ROOT,
    dump_yaml,
    extract_summary,
    extract_title,
    iter_documents,
    read_text,
    relative_path,
    stable_doc_id,
)

REVIEWED_DIRS = {
    "ProfessionalUnity3D",
    "Refactoring",
    "QFramework",
}
OUTLINE_DIRS = {
    "TheGameServerArchitectureAndOptimization",
    "TencentGameDevelopment1",
    "Butterfly",
    "Reconsitution",
}
ADVANCED_DIRS = {
    "ProfessionalUnity3D",
    "GameEngineArchitecture",
    "UnityShader",
    "UnityHDRP",
    "UnityNetworkGame",
    "BigGameServerDevelopment",
    "Multi-playerOnlineGameArchitectureCombat",
    "MicroservicesPatterns",
    "DesigningDataIntensiveApplications",
    "JavaGameServerArchitectureOfActualCombat",
}
BEGINNER_DIRS = {
    "CleanCode",
    "DontMakeMeThink",
    "DesignWithinDesign",
    "TheNon-Designer'sDesignBook",
    "MythicalManMonth",
    "ColdStart",
    "Butterfly",
}

CATEGORY_BY_DIR = {
    "ProfessionalUnity3D": "client-engine",
    "QFramework": "client-engine",
    "GameProgrammingPatterns": "client-engine",
    "GameEngineArchitecture": "client-engine",
    "UnityAI": "client-engine",
    "UnityHDRP": "client-engine",
    "UnityNetworkGame": "client-engine",
    "UnityShader": "client-engine",
    "UnityVR": "client-engine",
    "UnityGameOptimization": "client-engine",
    "UnityPerformanceTuningBible": "client-engine",
    "BigGameServerDevelopment": "server-architecture",
    "JavaGameServerArchitectureOfActualCombat": "server-architecture",
    "MicroservicesPatterns": "server-architecture",
    "Multi-playerOnlineGameArchitectureCombat": "server-architecture",
    "TheGameServerArchitectureAndOptimization": "server-architecture",
    "DesigningDataIntensiveApplications": "server-architecture",
    "TencentGameDevelopment1": "server-architecture",
    "TencentGameDevelopment2": "server-architecture",
    "TencentGameDevelopment3": "server-architecture",
    "CleanCode": "engineering-design",
    "Refactoring": "engineering-design",
    "Reconsitution": "engineering-design",
    "MythicalManMonth": "engineering-design",
    "TheArtofComputerProgramming": "engineering-design",
    "AgenticDesignPatterns": "engineering-design",
    "DontMakeMeThink": "design-product",
    "DesignWithinDesign": "design-product",
    "TheNon-Designer'sDesignBook": "design-product",
    "Butterfly": "design-product",
    "ColdStart": "design-product",
    "GameFell": "game-design",
    "GameTrip": "game-design",
    "GameProgrammingEssence1": "game-design",
    "MathematicsFor3DGameProgrammingAndComputerGraphics": "math-ai",
}

UNITY_DIRS = {
    "ProfessionalUnity3D",
    "QFramework",
    "GameProgrammingPatterns",
    "GameEngineArchitecture",
    "UnityAI",
    "UnityHDRP",
    "UnityNetworkGame",
    "UnityShader",
    "UnityVR",
    "UnityGameOptimization",
    "UnityPerformanceTuningBible",
}

VERSION_SCOPE_BY_DIR = {
    "GameProgrammingPatterns": ["Unity 2019.4"],
    "ProfessionalUnity3D": ["Unity 2019.4+"],
    "UnityNetworkGame": ["Unity 2019.4+"],
    "UnityHDRP": ["Unity 2019.4+"],
    "UnityShader": ["Unity 5", "Unity 2020+"],
    "UnityGameOptimization": ["Unity 5"],
    "UnityPerformanceTuningBible": ["Unity 2022+"],
}

VERSION_NOTE_BY_DIR = {
    "ProfessionalUnity3D": "部分运行时、GC 和平台结论具有版本依赖性，需在目标 Unity/.NET/IL2CPP 版本复核。",
    "UnityShader": "部分内容基于旧版 ShaderLab 和内置管线；SRP、URP、HDRP 与 Shader Graph 场景需另行核对。",
    "UnityGameOptimization": "内容包含 Unity 5/Mono 时代结论，容量、分配和性能数值应在当前目标版本实测。",
    "UnityPerformanceTuningBible": "性能倍数和平台结论必须结合目标硬件、Unity 版本与构建后端实测。",
}

PATTERN_CODE_PATHS = {
    "Bytecode.md": "GameProgrammingPatterns/Assets/BehavioralPatterns/Bytecode",
    "SubclassSandbox.md": "GameProgrammingPatterns/Assets/BehavioralPatterns/SubclassSandbox",
    "TypeObject.md": "GameProgrammingPatterns/Assets/BehavioralPatterns/TypeObject",
    "Component.md": "GameProgrammingPatterns/Assets/DecouplingPatterns/Component",
    "EventQueue.md": "GameProgrammingPatterns/Assets/DecouplingPatterns/EventQueue",
    "ServiceLocator.md": "GameProgrammingPatterns/Assets/DecouplingPatterns/ServiceLocator",
    "Command.md": "GameProgrammingPatterns/Assets/DesignPatternsRevisited/CommandPattern",
    "Flyweight.md": "GameProgrammingPatterns/Assets/DesignPatternsRevisited/FlyweightPattern",
    "Observer.md": "GameProgrammingPatterns/Assets/DesignPatternsRevisited/ObserverPattern",
    "Prototype.md": "GameProgrammingPatterns/Assets/DesignPatternsRevisited/PrototypePattern",
    "Singleton.md": "GameProgrammingPatterns/Assets/DesignPatternsRevisited/SingletonPattern",
    "State.md": "GameProgrammingPatterns/Assets/DesignPatternsRevisited/StatePattern",
    "DataLocality.md": "GameProgrammingPatterns/Assets/OptimizationPatterns/DataLocality",
    "DirtyFlag.md": "GameProgrammingPatterns/Assets/OptimizationPatterns/DirtyFlag",
    "ObjectPool.md": "GameProgrammingPatterns/Assets/OptimizationPatterns/ObjectPool",
    "DoubleBuffer.md": "GameProgrammingPatterns/Assets/SequencingPatterns/DoubleBuffer",
    "UpdateMethod.md": "GameProgrammingPatterns/Assets/SequencingPatterns/UpdateMethod",
}

PATTERN_ALIASES = {
    "ObjectPool.md": ["Object Pool", "对象池模式"],
    "Command.md": ["Command Pattern", "命令模式"],
    "Observer.md": ["Observer Pattern", "观察者模式"],
    "State.md": ["State Pattern", "状态模式"],
    "Singleton.md": ["Singleton Pattern", "单例模式"],
    "Component.md": ["Component Pattern", "组件模式"],
    "EventQueue.md": ["Event Queue", "事件队列"],
    "ServiceLocator.md": ["Service Locator", "服务定位器"],
    "DataLocality.md": ["Data Locality", "数据局部性"],
    "DirtyFlag.md": ["Dirty Flag", "脏标识"],
    "DoubleBuffer.md": ["Double Buffer", "双缓冲"],
    "UpdateMethod.md": ["Update Method", "更新方法"],
    "Bytecode.md": ["Bytecode", "字节码"],
    "TypeObject.md": ["Type Object", "类型对象"],
    "SubclassSandbox.md": ["Subclass Sandbox", "子类沙箱"],
    "Flyweight.md": ["Flyweight Pattern", "享元模式"],
    "Prototype.md": ["Prototype Pattern", "原型模式"],
}


def infer_category(rel_path: Path) -> str:
    if rel_path.parent == Path("."):
        return "overview" if rel_path.name == "README.md" else "meta"
    return CATEGORY_BY_DIR.get(rel_path.parts[0], "engineering-design")


def infer_status(rel_path: Path) -> str:
    if rel_path.parent == Path("."):
        return "reviewed"
    top = rel_path.parts[0]
    if top in REVIEWED_DIRS:
        return "reviewed"
    if top in OUTLINE_DIRS:
        return "outline"
    return "summary"


def infer_difficulty(rel_path: Path) -> str:
    if rel_path.parent == Path("."):
        return "beginner"
    top = rel_path.parts[0]
    if top in ADVANCED_DIRS:
        return "advanced"
    if top in BEGINNER_DIRS:
        return "beginner"
    return "intermediate"


def infer_tags(rel_path: Path, category: str) -> list[str]:
    tags: set[str] = set()
    if rel_path.parent != Path("."):
        tags.add(rel_path.parts[0].lower().replace("_", "-"))
    if category == "client-engine":
        tags.add("game-development")
    if category == "server-architecture":
        tags.update({"server", "architecture"})
    if category == "engineering-design":
        tags.add("software-engineering")
    if category == "design-product":
        tags.update({"design", "user-experience"})
    if category == "game-design":
        tags.add("game-design")
    if category == "math-ai":
        tags.add("mathematics")
    if rel_path.parts[0] in UNITY_DIRS:
        tags.add("unity")
    if rel_path.parts[0] == "GameProgrammingPatterns" and rel_path.name.endswith(".md"):
        if rel_path.name != "README.md":
            tags.add("design-pattern")
    return sorted(tags)


def build_record(path: Path) -> dict[str, Any]:
    rel = path.relative_to(ROOT)
    text = read_text(path)
    title = extract_title(text, path.stem)
    category = infer_category(rel)
    top = rel.parts[0] if len(rel.parts) > 1 else ""
    code_paths: list[str] = []
    if top == "GameProgrammingPatterns":
        code_path = PATTERN_CODE_PATHS.get(path.name)
        if code_path:
            code_paths.append(code_path)
    aliases = PATTERN_ALIASES.get(path.name, []) if top == "GameProgrammingPatterns" else []
    version_note = VERSION_NOTE_BY_DIR.get(top)
    record: dict[str, Any] = {
        "schema_version": 1,
        "id": stable_doc_id(path),
        "content_path": relative_path(path),
        "title": title,
        "category": category,
        "status": infer_status(rel),
        "difficulty": infer_difficulty(rel),
        "summary": extract_summary(text),
        "version_scope": VERSION_SCOPE_BY_DIR.get(top, []),
        "tags": infer_tags(rel, category),
        "aliases": aliases,
        "code_paths": code_paths,
        "test_paths": [],
        "sources": [],
        "reviewed_at": None,
    }
    if version_note:
        record["version_note"] = version_note
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="Create missing per-document metadata records.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata records.")
    args = parser.parse_args()

    created = 0
    skipped = 0
    for path in iter_documents():
        record = build_record(path)
        target = NOTES_META_DIR / f"{record['id']}.yaml"
        if target.exists() and not args.force:
            skipped += 1
            continue
        dump_yaml(target, record)
        created += 1

    print(f"documents={len(list(iter_documents()))} created={created} skipped={skipped}")


if __name__ == "__main__":
    main()
