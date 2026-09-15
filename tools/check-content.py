#!/usr/bin/env python3
"""Validate Hexo post metadata and local media references without extra dependencies."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "source" / "_posts"
ALLOWED_CATEGORIES = {"tech", "life"}
REQUIRED_FIELDS = ("title", "date", "tags", "categories", "description", "cover")
TAG_PATTERN = re.compile(r"^[a-z0-9\u4e00-\u9fff][a-z0-9\u4e00-\u9fff-]*$")
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\((?:<)?([^\s)>]+)(?:>)?(?:\s+[\"'][^\"']*[\"'])?\)")
HTML_MEDIA_PATTERN = re.compile(r"<(img|video|audio|source)\b[^>]*?\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
ASSET_IMAGE_PATTERN = re.compile(r"{%\s*asset_img\s+(\S+)(?:\s+([^%]*?))?\s*%}")
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class Finding:
    level: str
    path: Path
    message: str


def configure_console() -> None:
    """Keep Chinese diagnostics readable in Windows terminals and captured output."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查文章 Front Matter 与本地媒体引用。")
    parser.add_argument("paths", nargs="*", type=Path, help="要检查的 Markdown；默认检查 source/_posts。")
    parser.add_argument("--strict", action="store_true", help="将历史文章缺少 description/cover 和空图片 alt 视为错误。")
    parser.add_argument("--strict-new", action="store_true", help="仅对 Git 新增/未跟踪文章启用严格规则。")
    parser.add_argument("--quiet", action="store_true", help="仅输出问题和最终汇总。")
    return parser.parse_args()


def split_front_matter(text: str) -> tuple[dict[str, object], str]:
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("缺少以 --- 开始的 Front Matter")

    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError("Front Matter 缺少结束分隔线 ---") from exc

    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw_line in lines[1:end]:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-") and current_list_key:
            value = strip_quotes(stripped[1:].strip())
            cast_list = data.setdefault(current_list_key, [])
            if isinstance(cast_list, list) and value:
                cast_list.append(value)
            continue
        if ":" not in raw_line:
            current_list_key = None
            continue

        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        current_list_key = key if not raw_value else None
        if not raw_value:
            data[key] = []
        elif raw_value.startswith("[") and raw_value.endswith("]"):
            data[key] = [strip_quotes(item.strip()) for item in raw_value[1:-1].split(",") if item.strip()]
        else:
            data[key] = strip_quotes(raw_value)

    return data, "\n".join(lines[end + 1 :])


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].replace(r'\"', '"').replace(r"\'", "'")
    return value


def discover_posts(paths: list[Path]) -> list[Path]:
    if not paths:
        return sorted(POSTS_DIR.glob("*.md"))

    discovered: set[Path] = set()
    for supplied in paths:
        candidate = supplied if supplied.is_absolute() else ROOT / supplied
        if candidate.is_dir():
            discovered.update(candidate.rglob("*.md"))
        elif candidate.suffix.lower() == ".md" and candidate.exists():
            discovered.add(candidate)
        else:
            raise FileNotFoundError(f"找不到 Markdown 文件或目录：{supplied}")
    return sorted(path.resolve() for path in discovered)


def git_new_posts() -> set[Path]:
    commands = (
        ["git", "diff", "--name-only", "--diff-filter=A", "HEAD", "--", "source/_posts"],
        ["git", "ls-files", "--others", "--exclude-standard", "--", "source/_posts"],
    )
    paths: set[Path] = set()
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            paths.add((ROOT / line.strip()).resolve())
    return paths


def scalar(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def list_value(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def add(finds: list[Finding], level: str, path: Path, message: str) -> None:
    finds.append(Finding(level, path, message))


def validate_metadata(path: Path, data: dict[str, object], strict: bool, findings: list[Finding]) -> None:
    for field in REQUIRED_FIELDS:
        value = data.get(field)
        missing = not list_value(value) if field in {"tags", "categories"} else not scalar(value)
        if not missing:
            continue
        level = "ERROR" if field not in {"description", "cover"} or strict else "WARN"
        add(findings, level, path, f"Front Matter 缺少非空字段：{field}")

    date_value = scalar(data.get("date"))
    if date_value:
        parsed = False
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                datetime.strptime(date_value, fmt)
                parsed = True
                break
            except ValueError:
                pass
        if not parsed:
            add(findings, "ERROR", path, f"date 格式无效：{date_value}（应为 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）")

    categories = list_value(data.get("categories"))
    if categories and (len(categories) != 1 or categories[0] not in ALLOWED_CATEGORIES):
        add(findings, "ERROR", path, "categories 必须且只能是 tech 或 life")

    for tag in list_value(data.get("tags")):
        if tag != tag.lower() or not TAG_PATTERN.fullmatch(tag):
            add(findings, "ERROR", path, f"标签格式无效：{tag}（使用小写字母、数字、中文或连字符）")


def content_without_fences(body: str) -> str:
    output: list[str] = []
    in_fence = False
    fence = ""
    for line in body.splitlines():
        match = FENCE_PATTERN.match(line)
        if match:
            marker = match.group(1)
            if not in_fence:
                in_fence, fence = True, marker
            elif marker == fence:
                in_fence = False
            continue
        if not in_fence:
            output.append(line)
    return "\n".join(output)


def local_media_path(reference: str, post_path: Path) -> Path | None:
    reference = reference.strip()
    parsed = urlsplit(reference)
    if parsed.scheme or reference.startswith(("//", "#", "data:")):
        return None
    clean_path = unquote(parsed.path).replace("\\", "/")
    if not clean_path:
        return None
    if clean_path.startswith("/"):
        return (ROOT / "source" / clean_path.lstrip("/")).resolve()
    return (post_path.parent / clean_path).resolve()


def validate_media(path: Path, data: dict[str, object], body: str, strict: bool, findings: list[Finding]) -> None:
    references: list[tuple[str, str]] = []
    cover = scalar(data.get("cover"))
    if cover:
        references.append(("cover", cover))

    clean_body = content_without_fences(body)
    for alt, reference in MARKDOWN_IMAGE_PATTERN.findall(clean_body):
        if not alt.strip():
            add(findings, "ERROR" if strict else "WARN", path, f"图片缺少 alt 文本：{reference}")
        references.append(("图片", reference))

    for element, reference in HTML_MEDIA_PATTERN.findall(clean_body):
        references.append((element.lower(), reference))

    for reference, alt in ASSET_IMAGE_PATTERN.findall(clean_body):
        if not alt.strip():
            add(findings, "ERROR" if strict else "WARN", path, f"asset_img 缺少图片描述：{reference}")
        references.append(("asset_img", reference))

    checked: set[Path] = set()
    for kind, reference in references:
        media_path = local_media_path(reference, path)
        if media_path is None or media_path in checked:
            continue
        checked.add(media_path)
        try:
            media_path.relative_to(ROOT / "source")
        except ValueError:
            add(findings, "ERROR", path, f"{kind} 引用超出 source 目录：{reference}")
            continue
        if not media_path.is_file():
            add(findings, "ERROR", path, f"{kind} 文件不存在：{reference}")


def validate_post(path: Path, strict: bool) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
        data, body = split_front_matter(text)
    except (OSError, UnicodeError, ValueError) as exc:
        add(findings, "ERROR", path, str(exc))
        return findings

    validate_metadata(path, data, strict, findings)
    validate_media(path, data, body, strict, findings)
    return findings


def main() -> int:
    configure_console()
    args = parse_args()
    try:
        posts = discover_posts(args.paths)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 2

    if not posts:
        print("ERROR: 没有找到要检查的 Markdown 文件")
        return 2

    new_posts = git_new_posts() if args.strict_new else set()
    findings: list[Finding] = []
    for post in posts:
        strict = args.strict or post.resolve() in new_posts
        findings.extend(validate_post(post, strict))
        if not args.quiet and not any(item.path == post and item.level == "ERROR" for item in findings):
            label = "严格" if strict else "兼容"
            print(f"OK [{label}] {post.relative_to(ROOT)}")

    for finding in findings:
        print(f"{finding.level}: {finding.path.relative_to(ROOT)} - {finding.message}")

    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARN" for item in findings)
    print(f"\n检查完成：{len(posts)} 篇文章，{errors} 个错误，{warnings} 个警告。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
