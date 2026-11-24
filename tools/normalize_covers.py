from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Pictures" / "cover-manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def trim_border(image: Image.Image) -> Image.Image:
    """Remove transparent or near-white outer margins before fitting."""
    image = ImageOps.exif_transpose(image).convert("RGBA")
    alpha = image.getchannel("A")
    if alpha.getextrema()[0] < 250:
        bbox = alpha.getbbox()
        if bbox:
            image = image.crop(bbox)

    rgb = image.convert("RGB")
    corner = rgb.getpixel((0, 0))
    if min(corner) >= 235:
        difference = ImageChops.difference(rgb, Image.new("RGB", rgb.size, corner)).convert("L")
        mask = difference.point(lambda value: 255 if value > 12 else 0)
        bbox = mask.getbbox()
        if bbox:
            left, top, right, bottom = bbox
            margin = 2
            image = image.crop(
                (
                    max(0, left - margin),
                    max(0, top - margin),
                    min(image.width, right + margin),
                    min(image.height, bottom + margin),
                )
            )
    return image


def fit_image(image: Image.Image, width: int, height: int) -> Image.Image:
    image = trim_border(image)
    return ImageOps.contain(image, (width, height), Image.Resampling.LANCZOS)


def render_item(item: dict, spec: dict, base: Path) -> dict:
    source = base / item["source"]
    target = base / item["target"]
    if not source.exists():
        raise FileNotFoundError(f"missing source image: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)

    canvas_size = (int(spec["asset_width"]), int(spec["asset_height"]))
    padding = int(spec["padding"])
    canvas = Image.new("RGBA", canvas_size, "#F6F7F9")
    with Image.open(source) as opened:
        fitted = fit_image(opened, canvas_size[0] - padding * 2, canvas_size[1] - padding * 2)
    x = (canvas_size[0] - fitted.width) // 2
    y = (canvas_size[1] - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))

    quality = int(spec.get("quality", 88))
    max_bytes = int(spec.get("max_bytes", 153600))
    while True:
        canvas.convert("RGB").save(target, format="WEBP", quality=quality, method=6)
        size = target.stat().st_size
        if size <= max_bytes or quality <= 60:
            break
        quality -= 6
    return {
        "source": str(source.relative_to(ROOT)),
        "target": str(target.relative_to(ROOT)),
        "width": canvas_size[0],
        "height": canvas_size[1],
        "bytes": size,
        "quality": quality,
        "ok": size <= max_bytes,
    }


def build(check: bool = False) -> list[dict]:
    manifest = load_manifest()
    base = ROOT / manifest["base_dir"]
    specs = manifest["specs"]
    results = []
    for item in manifest["items"]:
        if check and not (base / item["target"]).exists():
            results.append({"target": item["target"], "ok": False, "error": "missing"})
            continue
        if not check:
            results.append(render_item(item, specs[item["kind"]], base))
            continue
        spec = specs[item["kind"]]
        target = base / item["target"]
        with Image.open(target) as image:
            size = target.stat().st_size
            results.append(
                {
                    "target": str(target.relative_to(ROOT)),
                    "width": image.width,
                    "height": image.height,
                    "bytes": size,
                    "ok": image.size == (spec["asset_width"], spec["asset_height"]) and size <= spec["max_bytes"],
                }
            )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize README book covers into fixed-size WebP assets.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    results = build(check=args.check)
    failures = [item for item in results if not item.get("ok")]
    for item in results:
        print(
            f"{'OK' if item.get('ok') else 'FAIL':4} "
            f"{item.get('target')} {item.get('width', '?')}x{item.get('height', '?')} "
            f"{item.get('bytes', 0) / 1024:.1f} KiB"
        )
    if failures:
        print(f"{len(failures)} cover assets failed validation", file=sys.stderr)
        raise SystemExit(1)
    print(f"validated {len(results)} cover assets")


if __name__ == "__main__":
    main()
