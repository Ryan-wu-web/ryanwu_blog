#!/usr/bin/env python3
"""Create a Hexo post and its dedicated media directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "source" / "_posts"
MEDIA_ROOT = ROOT / "source" / "images" / "posts"
SLUG_PATTERN = re.compile(r"^[a-z0-9\u4e00-\u9fff]+(?:-[a-z0-9\u4e00-\u9fff]+)*$")


def configure_console() -> None:
    """Keep Chinese prompts readable in Windows terminals and captured output."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="创建文章和独立媒体目录。省略参数时进入交互模式。")
    parser.add_argument("--title")
    parser.add_argument("--category", choices=("tech", "life"))
    parser.add_argument("--date")
    parser.add_argument("--tags", help="英文逗号分隔")
    parser.add_argument("--description")
    parser.add_argument("--slug")
    parser.add_argument("--cover")
    return parser.parse_args()


def prompt_required(label: str, initial: str | None = None) -> str:
    while True:
        prompt = f"{label} [{initial}]: " if initial else f"{label}: "
        value = input(prompt).strip() or (initial or "")
        if value:
            return value
        print("该项不能为空，请重新输入。")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text.lower()).strip("-")
    return slug


def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("发布日期必须使用 YYYY-MM-DD 格式") from exc
    return value


def parse_tags(value: str) -> list[str]:
    tags = [tag.strip().lower() for tag in value.split(",") if tag.strip()]
    if not tags:
        raise ValueError("至少填写一个标签")
    invalid = [tag for tag in tags if not SLUG_PATTERN.fullmatch(tag)]
    if invalid:
        raise ValueError(f"标签只能包含小写字母、数字、中文和连字符：{', '.join(invalid)}")
    return list(dict.fromkeys(tags))


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def choose_category(value: str | None) -> str:
    if value:
        return value
    print("\n文章类型:\n  1. 技术笔记\n  2. 生活随笔")
    while True:
        choice = input("请选择 (1/2): ").strip()
        if choice in {"1", "2"}:
            return "tech" if choice == "1" else "life"
        print("请输入 1 或 2。")


def create_post(args: argparse.Namespace) -> Path:
    print("=" * 56)
    print("创建新文章")
    print("=" * 56)

    category = choose_category(args.category)
    title = args.title or prompt_required("\n文章标题")
    date_value = validate_date(args.date or prompt_required("发布日期", datetime.now().strftime("%Y-%m-%d")))
    tags = parse_tags(args.tags or prompt_required("标签（英文逗号分隔）"))
    description = args.description or prompt_required("文章描述/摘要")

    default_slug = slugify(title)
    slug = (args.slug or prompt_required("URL/媒体目录名", default_slug)).lower()
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError("slug 只能包含小写字母、数字、中文和连字符")

    default_cover = f"/images/posts/{slug}/cover.jpg"
    cover = args.cover or default_cover
    post_path = POSTS_DIR / f"{date_value}-{slug}.md"
    media_dir = MEDIA_ROOT / slug

    if post_path.exists():
        raise FileExistsError(f"文章已存在，不会覆盖：{post_path.relative_to(ROOT)}")

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    media_dir.mkdir(parents=True, exist_ok=True)
    content = "\n".join(
        [
            "---",
            f"title: {yaml_string(title)}",
            f"date: {date_value} 12:00:00",
            f"tags: [{', '.join(tags)}]",
            f"categories: {category}",
            f"description: {yaml_string(description)}",
            f"cover: {yaml_string(cover)}",
            "---",
            "",
            "## 引言",
            "",
            "简述这篇文章的背景和目的。",
            "",
            "## 正文",
            "",
            "开始写作……",
            "",
            "## 总结",
            "",
            "总结核心观点与后续行动。",
            "",
        ]
    )
    post_path.write_text(content, encoding="utf-8")
    return post_path


def print_next_steps(post_path: Path) -> None:
    slug = post_path.stem.split("-", 3)[-1]
    media_url = f"/images/posts/{slug}"
    print(f"\n文章：{post_path.relative_to(ROOT)}")
    print(f"媒体目录：source/images/posts/{slug}/")
    print("\n写作时可使用：")
    print(f"  图片：![准确描述]({media_url}/image.jpg)")
    print(f'  视频：<video controls preload="metadata" src="{media_url}/video.mp4"></video>')
    print(f'  音频：<audio controls preload="metadata" src="{media_url}/audio.mp3"></audio>')
    print("\n请先把 cover 对应文件放入媒体目录，然后执行：")
    print(f'  python tools/check-content.py --strict "{post_path.relative_to(ROOT)}"')
    print("  npm run preview")
    print("  python tools/publish.py --check-only")


def main() -> int:
    configure_console()
    try:
        post_path = create_post(parse_args())
        print_next_steps(post_path)
        return 0
    except (ValueError, FileExistsError) as exc:
        print(f"\n创建失败：{exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n已取消")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
