#!/usr/bin/env python3
"""Generate a post cover in the blog's fixed template.

Every geometry constant below was reverse-engineered from a published cover, so
covers produced by this tool line up with the existing series to the pixel. To
restyle the template later, edit the "TEMPLATE" block only.

Usage examples:
    # local photo
    python tools/gen_cover.py --slug my-post --series tech-news \
        --title1 "Agent 框架" --title2 "怎么选" --image ./photo.jpg

    # search and pick the first usable candidate
    python tools/gen_cover.py --slug my-post --series dev-notes \
        --title1 "从能演示" --title2 "到敢签字" --source burst --query "code screen"

    # only list candidates
    python tools/gen_cover.py --slug my-post --source commons --query "reading" --list-only

    # re-verify an existing cover
    python tools/gen_cover.py --verify source/images/posts/my-post/cover.webp
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = Path(__file__).resolve().parents[1]
MEDIA_ROOT = ROOT / "source" / "images" / "posts"

# --------------------------------------------------------------------------
# TEMPLATE — 改版式只改这一段
# --------------------------------------------------------------------------
CANVAS = (1600, 900)
BG = (13, 17, 23)

PANEL = (600, 100, 1426, 800)        # left, top, right, bottom
FRAME = (597, 97, 1429, 803)         # 2px outline box
DASH = (172, 236, 218, 241)          # copper accent, 46x6
RULE = (172, 516, 471, 517)          # 300x2 divider

TEXT_X = 172
DATE_X = 173
EYEBROW_TOP = 273
TITLE1_TOP = 347
TITLE2_TOP = 427
DATE_TOP = 547
TEXT_SAFE_RIGHT = 580                # text must stop 20px before the panel

INK_HEIGHT = {"eyebrow": 20, "title": 55, "date": 14}

COLOR_TITLE = (243, 247, 253)
COLOR_TITLE_ALT = (192, 162, 130)
COLOR_EYEBROW = (164, 170, 178)
COLOR_DATE = (161, 168, 174)
COLOR_DASH = (182, 143, 104)
COLOR_RULE = (158, 129, 98)
COLOR_FRAME = (155, 155, 155)

GRAIN_SIGMA = 2.0
VIGNETTE_STRENGTH = 0.10
WEBP_QUALITY = 90
CARD_SIZE = (364, 235)

FONT_CN = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_EN = r"C:\Windows\Fonts\bahnschrift.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"

# 眉标按栏目区分（不含年份，年份取自 --date）
SERIES_EYEBROW = {
    "tech-news": "TECH NEWS",
    "dev-notes": "DEV NOTES",
    "agent": "AGENT NOTES",
    "llm": "LLM NOTES",
    "robotics": "ROBOTICS NOTES",
    "autonomous-driving": "AUTONOMOUS DRIVING",
    "image-generation": "IMAGE GENERATION",
    "tech": "TECH NOTES",
    "reading": "READING NOTES",
    "fitness": "FITNESS NOTES",
    "career": "CAREER NOTES",
    "journal": "LIFE NOTES",
    "life": "LIFE NOTES",
}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MIN_WIDTH = 1600
ALLOWED_CC = ("public domain", "cc0", "cc by 2.0", "cc by 3.0", "cc by 4.0")

BURST_PATTERN = re.compile(r"https://burst\.shopifycdn\.com/photos/[^\"'\s\\]+?\.(?:jpe?g|png)")
SKIP_NAME = re.compile(r"logo|icon|avatar|placeholder|sprite", re.I)


# --------------------------------------------------------------------------
# text measurement
# --------------------------------------------------------------------------
def measure_ink(font: ImageFont.FreeTypeFont, text: str) -> tuple[int, int, int, int]:
    """Ink bbox (left, top, right, bottom) relative to the draw origin."""
    canvas = Image.new("L", (2400, 500), 0)
    ImageDraw.Draw(canvas).text((100, 100), text, font=font, fill=255)
    box = canvas.getbbox()
    if not box:
        return 0, 0, 0, 0
    return box[0] - 100, box[1] - 100, box[2] - 100, box[3] - 100


def pick_font_size(font_path: str, sample: str, target_h: int,
                   sizes: range = range(16, 80)) -> int:
    best_size, best_delta = None, None
    for size in sizes:
        font = ImageFont.truetype(font_path, size)
        _, top, _, bottom = measure_ink(font, sample)
        delta = abs(bottom - top + 1 - target_h)
        if best_delta is None or delta < best_delta:
            best_size, best_delta = size, delta
    assert best_size is not None
    return best_size


def draw_ink(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
             font: ImageFont.FreeTypeFont, fill: tuple[int, int, int]) -> tuple[int, int]:
    """Draw so that the ink's top-left lands exactly on xy. Returns ink width/height."""
    left, top, right, bottom = measure_ink(font, text)
    draw.text((xy[0] - left, xy[1] - top), text, font=font, fill=fill)
    return right - left + 1, bottom - top + 1


# --------------------------------------------------------------------------
# image sources
# --------------------------------------------------------------------------
def curl(url: str, dest: Path | None = None, timeout: int = 60) -> bytes:
    cmd = ["curl", "-sL", "--max-time", str(timeout), "-A", UA]
    if dest is not None:
        cmd += ["-o", str(dest)]
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, timeout=timeout + 20)
    return result.stdout if dest is None else b""


def download_image(url: str, dest: Path) -> tuple[int, int] | None:
    """Download and validate; returns (width, height) or None."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        curl(url, dest)
    except Exception:
        return None
    if not dest.exists() or dest.stat().st_size < 20_000:
        dest.unlink(missing_ok=True)
        return None
    try:
        with Image.open(dest) as probe:
            probe.load()
            return probe.size
    except Exception:
        dest.unlink(missing_ok=True)
        return None


def burst_candidates(query: str, limit: int) -> list[dict]:
    page = curl("https://burst.shopify.com/photos/search?q=" + quote(query), timeout=45)
    html = page.decode("utf-8", errors="replace")
    urls = []
    for url in BURST_PATTERN.findall(html):
        name = url.rsplit("/", 1)[-1]
        if SKIP_NAME.search(name) or url in urls:
            continue
        urls.append(url)
    return [{"url": u, "label": u.rsplit("/", 1)[-1], "license": "Burst 免费商用"}
            for u in urls[: limit * 4]]


def nasa_candidates(query: str, limit: int) -> list[dict]:
    body = curl(
        "https://images-api.nasa.gov/search?media_type=image&page_size="
        + str(limit * 3) + "&q=" + quote(query),
        timeout=45,
    ).decode("utf-8", errors="replace")
    start = body.find("{")
    if start < 0:
        return []
    try:
        payload, _ = json.JSONDecoder().raw_decode(body[start:])
    except Exception:
        return []
    items = payload.get("collection", {}).get("items", [])
    out = []
    for item in items:
        data = item["data"][0]
        nasa_id = data.get("nasa_id", "")
        if not nasa_id:
            continue
        out.append({
            "url": f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~orig.jpg",
            "fallbacks": [f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~large.jpg"],
            "label": f"{nasa_id} · {(data.get('title') or '')[:48]}",
            "license": "NASA 公有领域",
        })
    return out


def commons_candidates(query: str, limit: int) -> list[dict]:
    url = (
        "https://commons.wikimedia.org/w/api.php?action=query&format=json"
        "&generator=search&gsrsearch=" + quote(f"filetype:bitmap {query}")
        + "&gsrnamespace=6&gsrlimit=" + str(limit * 3)
        + "&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1920"
    )
    body = curl(url, timeout=45).decode("utf-8", errors="replace")
    start = body.find("{")
    if start < 0:
        return []
    try:
        payload, _ = json.JSONDecoder().raw_decode(body[start:])
    except Exception:
        return []
    out = []
    for page_data in (payload.get("query", {}).get("pages", {}) or {}).values():
        info = (page_data.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        license_name = str(meta.get("LicenseShortName", {}).get("value", "")).strip()
        thumb = info.get("thumburl")
        if not thumb or not license_ok(license_name):
            continue
        out.append({
            "url": thumb,
            "label": f"{str(page_data.get('title', '')).replace('File:', '')[:48]}",
            "license": license_name,
        })
    return out


def license_ok(name: str) -> bool:
    """CC BY-SA is rejected on purpose: it would force the cover to share alike."""
    lowered = name.strip().lower()
    if "sa" in lowered.replace("cc0", ""):
        return False
    return any(lowered == allowed or lowered.startswith(allowed) for allowed in ALLOWED_CC)


def relevance(label: str, query: str) -> int:
    """Rough relevance: how many query tokens appear in the candidate name/title.

    Search pages (Burst especially) mix in promo and unrelated photos, so the
    first URL on the page is not the best match.
    """
    haystack = label.lower()
    tokens = [t for t in re.split(r"[^a-z0-9]+", query.lower()) if len(t) >= 3]
    score = 0
    for token in tokens:
        if token in haystack or token[:-1] in haystack:
            score += 1
    return score


def collect_candidates(args: argparse.Namespace, workdir: Path) -> list[dict]:
    handlers = {
        "burst": burst_candidates,
        "nasa": nasa_candidates,
        "commons": commons_candidates,
    }
    raw = handlers[args.source](args.query, args.limit)
    # Rank before filtering: search pages return promo/unrelated photos first.
    raw.sort(key=lambda item: relevance(item["label"], args.query), reverse=True)
    needed = max(args.limit, args.pick)
    print(f"[素材] {args.source} · {args.query} · 原始 {len(raw)} 个，按词面相关性排序")

    usable = []
    for index, cand in enumerate(raw, 1):
        if len(usable) >= needed:
            break
        local = workdir / f"cand-{index:02d}.jpg"
        size = download_image(cand["url"], local)
        for fallback in cand.get("fallbacks", []):
            if size:
                break
            size = download_image(fallback, local)
        if not size:
            print(f"  - {cand['label'][:52]} → 下载/解码失败，跳过")
            continue
        width, height = size
        if width < MIN_WIDTH:
            print(f"  - {cand['label'][:52]} → {width}px 宽度不足，跳过")
            continue
        if not args.allow_portrait and width < height:
            print(f"  - {cand['label'][:52]} → 竖构图 {width}x{height}，跳过")
            continue
        cand.update({"path": local, "size": (width, height)})
        usable.append(cand)
        print(f"  + {cand['label'][:52]} → {width}x{height} · {cand['license']}")
    return usable


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def cover_crop(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / source.width, target_h / source.height)
    resized = source.resize(
        (max(target_w, round(source.width * scale)),
         max(target_h, round(source.height * scale))),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def render(photo: Path, title1: str, title2: str | None, eyebrow: str,
           date_text: str) -> Image.Image:
    panel_w = PANEL[2] - PANEL[0]
    panel_h = PANEL[3] - PANEL[1]

    with Image.open(photo) as raw:
        source = raw.convert("RGB")
    crop = cover_crop(source, (panel_w, panel_h))

    canvas = Image.new("RGB", CANVAS, BG)
    canvas.paste(crop, (PANEL[0], PANEL[1]))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle(FRAME, outline=COLOR_FRAME, width=2)
    draw.rectangle(DASH, fill=COLOR_DASH)

    f_eyebrow = ImageFont.truetype(
        FONT_EN, pick_font_size(FONT_EN, eyebrow, INK_HEIGHT["eyebrow"], range(14, 40)))
    f_title = ImageFont.truetype(
        FONT_CN, pick_font_size(FONT_CN, title1 or "标题", INK_HEIGHT["title"], range(36, 84)))
    f_date = ImageFont.truetype(
        FONT_MONO, pick_font_size(FONT_MONO, date_text, INK_HEIGHT["date"], range(12, 34)))

    draw_ink(draw, (TEXT_X, EYEBROW_TOP), eyebrow, f_eyebrow, COLOR_EYEBROW)
    draw_ink(draw, (TEXT_X, TITLE1_TOP), title1, f_title, COLOR_TITLE)
    if title2:
        draw_ink(draw, (TEXT_X, TITLE2_TOP), title2, f_title, COLOR_TITLE_ALT)

    draw.rectangle(RULE, fill=COLOR_RULE)
    draw_ink(draw, (DATE_X, DATE_TOP), date_text, f_date, COLOR_DATE)

    arr = np.asarray(canvas).astype(np.float32)
    seed = int(hashlib.sha256(f"{title1}|{date_text}".encode()).hexdigest()[:8], 16)
    arr += np.random.default_rng(seed).normal(0, GRAIN_SIGMA, arr.shape).astype(np.float32)
    yy, xx = np.mgrid[0:CANVAS[1], 0:CANVAS[0]]
    radius = np.sqrt(((xx - CANVAS[0] / 2) / (CANVAS[0] / 2)) ** 2
                     + ((yy - CANVAS[1] / 2) / (CANVAS[1] / 2)) ** 2)
    arr *= (1.0 - VIGNETTE_STRENGTH * np.clip(radius - 0.30, 0, 1.2))[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# --------------------------------------------------------------------------
# verification
# --------------------------------------------------------------------------
EXPECTED_ROWS = (
    ("铜色短横", 236, 242),
    ("眉标", 273, 292),
    ("标题1", 347, 401),
    ("标题2", 427, 481),
    ("细分隔线", 516, 518),
    ("日期", 547, 560),
)
ROW_TOLERANCE = 3


def ink_rows(arr: np.ndarray, top: int, bottom: int) -> tuple[int, int] | None:
    window = arr[max(0, top - 8):bottom + 8, 150:TEXT_SAFE_RIGHT]
    delta = np.abs(window - np.array(BG)).sum(axis=2)
    rows = np.where((delta > 45).any(axis=1))[0]
    if not len(rows):
        return None
    return int(rows.min()) + max(0, top - 8), int(rows.max()) + max(0, top - 8)


def text_width(arr: np.ndarray, top: int, bottom: int) -> int | None:
    """Right-most ink column of a text row, scanning up to but excluding the panel frame."""
    window = arr[top:bottom, 150:FRAME[0] - 1]
    delta = np.abs(window - np.array(BG)).sum(axis=2)
    cols = np.where((delta > 45).any(axis=0))[0]
    if not len(cols):
        return None
    return int(cols.max()) + 150


def verify(image: Image.Image, expect_title2: bool) -> list[tuple[str, bool, str]]:
    arr = np.asarray(image.convert("RGB"))
    checks: list[tuple[str, bool, str]] = []

    for label, top, bottom in EXPECTED_ROWS:
        if label == "标题2" and not expect_title2:
            continue
        found = ink_rows(arr, top, bottom)
        if found is None:
            checks.append((f"行位·{label}", False, f"期望顶部 y={top}，实际无墨迹"))
            continue
        actual_top = found[0]
        ok = abs(actual_top - top) <= ROW_TOLERANCE
        checks.append((f"行位·{label}", ok, f"期望 y={top}，实际 y={actual_top}"))

    for label, top, bottom in (("标题1", 347, 401), ("标题2", 427, 481)):
        if label == "标题2" and not expect_title2:
            continue
        right = text_width(arr, top, bottom)
        if right is None:
            continue
        ok = right <= TEXT_SAFE_RIGHT
        checks.append((f"宽度·{label}", ok,
                       f"墨迹右缘 x={right}，上限 {TEXT_SAFE_RIGHT}（超出会压到图片面板）"))

    panel = arr[PANEL[1]:PANEL[3], PANEL[0]:PANEL[2]].astype(np.float32)
    std = float(panel.std())
    checks.append(("面板内容", std > 15, f"裁切区标准差 {std:.1f}（需 > 15）"))
    return checks


def card_preview(image: Image.Image, dest: Path) -> tuple[Path, list[tuple[str, bool, str]]]:
    scale = CARD_SIZE[1] / image.height
    scaled = image.resize((round(image.width * scale), CARD_SIZE[1]), Image.Resampling.LANCZOS)
    cut = (scaled.width - CARD_SIZE[0]) // 2
    card = scaled.crop((cut, 0, cut + CARD_SIZE[0], CARD_SIZE[1]))
    dest.parent.mkdir(parents=True, exist_ok=True)
    card.save(dest, "WEBP", quality=92, method=6)

    arr = np.asarray(card.convert("RGB")).astype(int)
    zone = arr[40:220, 8:160]
    delta = np.abs(zone - np.array(BG)).sum(axis=2)
    ink_ratio = float((delta > 45).mean())
    checks = [("卡片·文字区", ink_ratio > 0.01,
               f"卡片文字区墨迹占比 {ink_ratio:.1%}（需 > 1%，过低说明文字被裁）")]
    return dest, checks


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="生成符合本站模板的文章封面（1600×900 WebP，含自检）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--slug", help="文章 slug，决定输出路径 source/images/posts/<slug>/cover.webp")
    parser.add_argument("--title1", help="标题第一行（关键词式，建议 ≤6 个汉字）")
    parser.add_argument("--title2", help="标题第二行（可省略）")
    parser.add_argument("--series", choices=sorted(SERIES_EYEBROW), help="栏目，决定眉标")
    parser.add_argument("--eyebrow", help="直接指定眉标（覆盖 --series）")
    parser.add_argument("--date", default=dt.date.today().isoformat(),
                        help="封面日期 YYYY-MM-DD，默认今天")
    parser.add_argument("--image", help="使用本地图片")
    parser.add_argument("--source", choices=("burst", "nasa", "commons"), help="在线图源")
    parser.add_argument("--query", help="检索词（配合 --source）")
    parser.add_argument("--pick", type=int, default=1, help="选用第几个可用候选，默认 1")
    parser.add_argument("--limit", type=int, default=8, help="最多检查几个候选，默认 8")
    parser.add_argument("--allow-portrait", action="store_true", help="允许竖构图")
    parser.add_argument("--out", help="输出路径（默认按 slug 推导）")
    parser.add_argument("--force", action="store_true", help="允许覆盖已存在的封面")
    parser.add_argument("--preview", help="卡片预览输出路径")
    parser.add_argument("--list-only", action="store_true", help="只列候选，不生成")
    parser.add_argument("--verify", help="校验已有封面")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出结果（供编排器消费）")
    return parser.parse_args()


def emit(args: argparse.Namespace, payload: dict, ok: bool) -> int:
    if args.json:
        payload["ok"] = ok
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()

    # --- verify mode ---
    if args.verify:
        path = Path(args.verify)
        if not path.exists():
            print(f"找不到文件：{path}", file=sys.stderr)
            return 2
        with Image.open(path) as raw:
            image = raw.convert("RGB")
        checks = verify(image, expect_title2=True)
        for name, ok, detail in checks:
            print(f"{'OK  ' if ok else 'FAIL'} {name}: {detail}")
        ok = all(item[1] for item in checks)
        print("结论：通过" if ok else "结论：未通过")
        return emit(args, {"checks": [{"name": n, "ok": o, "detail": d} for n, o, d in checks]}, ok)

    # --- list-only mode ---
    if args.list_only:
        if not (args.source and args.query):
            print("--list-only 需要 --source 与 --query", file=sys.stderr)
            return 2
        workdir = Path(tempfile.mkdtemp(prefix="gen-cover-"))
        try:
            candidates = collect_candidates(args, workdir)
        finally:
            for leftover in workdir.glob("*"):
                leftover.unlink(missing_ok=True)
            workdir.rmdir()
        if args.json:
            return emit(args, {"candidates": [
                {"label": c["label"], "size": list(c["size"]), "license": c["license"]}
                for c in candidates]}, True)
        return 0

    # --- generation mode ---
    if not args.slug or not args.title1:
        print("生成模式需要 --slug 与 --title1", file=sys.stderr)
        return 2
    if not args.image and not (args.source and args.query):
        print("需要 --image，或 --source 配合 --query", file=sys.stderr)
        return 2

    date_value = dt.date.fromisoformat(args.date)
    date_text = date_value.strftime("%Y.%m.%d")
    year = date_value.strftime("%Y")
    if args.eyebrow:
        eyebrow = args.eyebrow
    elif args.series:
        eyebrow = f"{SERIES_EYEBROW[args.series]} / {year}"
    else:
        print("需要 --series 或 --eyebrow", file=sys.stderr)
        return 2

    out_path = Path(args.out) if args.out else MEDIA_ROOT / args.slug / "cover.webp"
    if out_path.exists() and not args.force:
        print(f"封面已存在：{out_path}\n如需覆盖请加 --force", file=sys.stderr)
        return 2

    workdir = Path(tempfile.mkdtemp(prefix="gen-cover-"))
    try:
        if args.image:
            photo = Path(args.image)
            if not photo.exists():
                print(f"找不到图片：{photo}", file=sys.stderr)
                return 2
            with Image.open(photo) as probe:
                probe.load()
                print(f"[素材] 本地图片 {photo.name} · {probe.width}x{probe.height}")
            source_label, license_label = photo.name, "用户提供"
        else:
            candidates = collect_candidates(args, workdir)
            if len(candidates) < args.pick:
                print(f"可用候选不足（需要第 {args.pick} 个，只有 {len(candidates)} 个）", file=sys.stderr)
                return 1
            chosen = candidates[args.pick - 1]
            photo = chosen["path"]
            source_label, license_label = chosen["label"], chosen["license"]

        print("[渲染] 1600x900 模板")
        image = render(photo, args.title1, args.title2, eyebrow, date_text)

        print("[校验]")
        checks = verify(image, expect_title2=bool(args.title2))
        for name, ok, detail in checks:
            print(f"{'  OK  ' if ok else '  FAIL'} {name}: {detail}")

        preview_path = (Path(args.preview) if args.preview
                        else Path(tempfile.gettempdir()) / f"{args.slug}-card.webp")
        preview_path, card_checks = card_preview(image, preview_path)
        for name, ok, detail in card_checks:
            print(f"{'  OK  ' if ok else '  FAIL'} {name}: {detail}")
        checks += card_checks

        ok = all(item[1] for item in checks)
        if not ok:
            print("\n校验未通过，未写入文件。请缩短标题（建议 ≤6 汉字/行）或换图。", file=sys.stderr)
            return emit(args, {"checks": [{"name": n, "ok": o, "detail": d} for n, o, d in checks]}, False)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(out_path, "WEBP", quality=WEBP_QUALITY, method=6)
        digest = hashlib.sha256(out_path.read_bytes()).hexdigest()[:16]
        try:
            display_path = out_path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            display_path = str(out_path.resolve())
        print(f"\n[输出] {out_path}")
        print(f"[预览] {preview_path}")
        print(f"[信息] 眉标 {eyebrow} · 日期 {date_text} · 素材 {source_label[:40]} · {license_label}")
        print(f"[哈希] {digest}")
        print(f"[引用] 在 Front Matter 写 cover: \"/images/posts/{args.slug}/cover.webp\"")
        return emit(args, {
            "slug": args.slug,
            "cover": display_path,
            "preview": str(preview_path),
            "eyebrow": eyebrow,
            "date": date_text,
            "source": source_label,
            "license": license_label,
            "sha256_16": digest,
            "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in checks],
        }, True)
    finally:
        for leftover in workdir.glob("*"):
            leftover.unlink(missing_ok=True)
        workdir.rmdir()


if __name__ == "__main__":
    raise SystemExit(main())
