from __future__ import annotations

import json
import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from PIL import Image

from common import ROOT

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
IMG_TAG_RE = re.compile(r"<img\b([^>]*)>", re.I)
ATTR_RE = re.compile(r"([\w:-]+)\s*=\s*[\"']([^\"']*)[\"']")
COVER_MANIFEST = ROOT / "Pictures" / "cover-manifest.json"


class ReferenceParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() not in {"a", "img"}:
            return
        attributes = dict(attrs)
        value = attributes.get("href") if tag.lower() == "a" else attributes.get("src")
        if value:
            self.references.append(value)


def markdown_files() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.relative_to(ROOT).parts:
            continue
        yield path


def local_target(source: Path, reference: str) -> Path | None:
    value = reference.strip()
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    else:
        value = value.split(" ", 1)[0]
    value = value.strip("\"'")
    if not value or value.startswith("#") or SCHEME_RE.match(value) or value.startswith("//"):
        return None
    path_part = urllib.parse.unquote(value.split("#", 1)[0].split("?", 1)[0])
    if not path_part:
        return None
    return (source.parent / path_part).resolve()


def check_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    references = [match.group(1).strip() for match in MARKDOWN_LINK_RE.finditer(text)]
    parser = ReferenceParser(path)
    parser.feed(text)
    references.extend(parser.references)
    for reference in references:
        target = local_target(path, reference)
        if target is None:
            continue
        try:
            target.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: reference escapes repository: {reference}")
            continue
        if not target.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing target: {reference}")
    return errors


def check_fences(path: Path) -> list[str]:
    errors: list[str] = []
    marker: str | None = None
    start_line = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        token = match.group(1)
        if marker is None:
            marker = token[0]
            start_line = line_number
        elif token[0] == marker:
            marker = None
    if marker is not None:
        errors.append(f"{path.relative_to(ROOT)}: unclosed code fence opened at line {start_line}")
    return errors


def check_readme_covers() -> list[str]:
    errors: list[str] = []
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8", errors="replace")
    if re.search(r"style\s*=\s*[\"'][^\"']*zoom", text, re.I):
        errors.append("README.md must not use style zoom for images")
    manifest = json.loads(COVER_MANIFEST.read_text(encoding="utf-8"))
    specs = manifest["specs"]
    base = ROOT / manifest["base_dir"]
    image_tags = list(IMG_TAG_RE.finditer(text))
    for item in manifest["items"]:
        target_ref = f"./Pictures/{item['target']}"
        source_ref = f"./Pictures/{item['source']}"
        if source_ref in text:
            errors.append(f"README.md references legacy image instead of standardized asset: {source_ref}")
        tags = [match for match in image_tags if target_ref in match.group(0)]
        if not tags:
            errors.append(f"README.md is missing standardized image: {target_ref}")
            continue
        attrs = dict(ATTR_RE.findall(tags[0].group(1)))
        spec = specs[item["kind"]]
        if attrs.get("width") != str(spec["display_width"]):
            errors.append(f"{target_ref} must use width={spec['display_width']}")
        if not attrs.get("alt", "").strip():
            errors.append(f"{target_ref} must have non-empty alt text")
        if "style" in attrs:
            errors.append(f"{target_ref} must not use inline style")
        image_path = base / item["target"]
        if not image_path.exists():
            errors.append(f"missing standardized image file: {image_path.relative_to(ROOT)}")
            continue
        with Image.open(image_path) as image:
            if image.size != (spec["asset_width"], spec["asset_height"]):
                errors.append(
                    f"{image_path.relative_to(ROOT)} must be "
                    f"{spec['asset_width']}x{spec['asset_height']}, got {image.width}x{image.height}"
                )
        if image_path.stat().st_size > spec["max_bytes"]:
            errors.append(
                f"{image_path.relative_to(ROOT)} exceeds {spec['max_bytes']} bytes"
            )
    return errors


def check_agent_adapters() -> list[str]:
    errors: list[str] = []
    core = ROOT / "ai" / "instructions" / "core.md"
    if not core.exists():
        errors.append("missing ai/instructions/core.md")
        return errors
    adapters = [
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "GEMINI.md",
        ROOT / ".github" / "copilot-instructions.md",
        ROOT / ".cursor" / "rules" / "game-notes.mdc",
    ]
    for path in adapters:
        if not path.exists():
            errors.append(f"missing agent adapter: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for reference in ("@ai/instructions/core.md", "@ai/agent-contract.yaml"):
            if reference not in text:
                errors.append(f"{path.relative_to(ROOT)} does not import {reference}")
    return errors


def run_checks() -> list[str]:
    errors: list[str] = []
    for path in markdown_files():
        errors.extend(check_links(path))
        errors.extend(check_fences(path))
    errors.extend(check_agent_adapters())
    errors.extend(check_readme_covers())
    return errors


def main() -> None:
    errors = run_checks()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"markdown files checked: {len(list(markdown_files()))}")
    print("repository links, standardized covers and agent adapters: OK")


if __name__ == "__main__":
    main()
