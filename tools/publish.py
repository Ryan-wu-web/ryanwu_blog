#!/usr/bin/env python3
"""Validate, build, commit, and publish the blog from the main branch."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISH_PATHS = (
    ".github",
    "docs",
    "scaffolds",
    "source",
    "themes/butterfly",
    "tools",
    "README.md",
    "package.json",
    "package-lock.json",
    "_config.yml",
    "_config.butterfly.yml",
)
NPM_COMMAND = "npm.cmd" if os.name == "nt" else "npm"
COMMIT_DEFAULTS = {
    "1": "post: add new article",
    "2": "update: page content",
    "3": "style: update design",
    "4": "fix: correct content",
    "5": "update: blog content",
}


def configure_console() -> None:
    """Keep Chinese diagnostics readable in Windows terminals and captured output."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="发布前检查，并在 main 分支上安全提交和推送。")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-only", action="store_true", help="只执行内容检查和 Hexo 构建。")
    mode.add_argument("--dry-run", action="store_true", help="检查、构建并展示将发布的状态，不写入 Git。")
    return parser.parse_args()


def run(command: list[str], description: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print(f"\n[{description}] {' '.join(command)}", flush=True)
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if capture and result.stdout.strip():
        print(result.stdout.rstrip())
    if result.returncode != 0:
        if capture and result.stderr.strip():
            print(result.stderr.rstrip(), file=sys.stderr)
        raise RuntimeError(f"{description}失败（退出码 {result.returncode}）")
    return result


def output(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"命令失败：{' '.join(command)}")
    return result.stdout.strip()


def validate_and_build() -> None:
    run([sys.executable, "tools/check-content.py", "--strict-new"], "检查文章内容")
    run([NPM_COMMAND, "run", "clean"], "清理 Hexo 缓存")
    run([NPM_COMMAND, "run", "build"], "构建静态站点")


def git_status() -> str:
    return output(["git", "status", "--short"])


def current_branch() -> str:
    return output(["git", "branch", "--show-current"])


def stage_changes() -> None:
    # Stage all tracked edits/deletions, but admit new files only from blog-owned paths.
    run(["git", "add", "--update"], "暂存已跟踪文件的改动")
    existing_paths = [path for path in PUBLISH_PATHS if (ROOT / path).exists()]
    run(["git", "add", "--", *existing_paths], "暂存博客内容与配置")


def has_staged_changes() -> bool:
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if result.returncode not in {0, 1}:
        raise RuntimeError("无法确认暂存区状态")
    return result.returncode == 1


def prompt_commit_message() -> str:
    print("\n提交类型：\n  1. post  2. update  3. style  4. fix  5. 自定义")
    choice = input("选择 [5]: ").strip() or "5"
    default = COMMIT_DEFAULTS.get(choice, COMMIT_DEFAULTS["5"])
    return input(f"提交信息 [{default}]: ").strip() or default


def main() -> int:
    configure_console()
    args = parse_args()
    try:
        validate_and_build()
        status = git_status()
        branch = current_branch()
        print(f"\n当前分支：{branch or '(detached HEAD)'}")
        print("\n当前改动：")
        print(status or "（无改动）")

        if args.check_only:
            print("\n检查通过：未执行暂存、提交或推送。")
            return 0
        if args.dry_run:
            print("\nDry run 完成：未执行暂存、提交或推送。")
            return 0
        if not status:
            print("\n没有检测到改动，无需发布。")
            return 0
        if branch != "main":
            print("\n已阻止发布：只有 main 分支可以推送线上。请先审查并合并当前分支。", file=sys.stderr)
            return 2

        message = prompt_commit_message()
        confirmation = input("\n确认暂存全部有效改动、提交并推送 origin/main？(y/N): ").strip().lower()
        if confirmation != "y":
            print("已取消，Git 状态未改变。")
            return 0

        stage_changes()
        if not has_staged_changes():
            print("没有可发布的博客改动；本地临时文件未被加入暂存区。")
            return 0
        run(["git", "commit", "-m", message], "提交代码")
        run(["git", "push", "origin", "main"], "推送到远程")
        print("\n发布已触发。等待 GitHub Actions 完成后再访问线上站点。")
        return 0
    except RuntimeError as exc:
        print(f"\n{exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n已取消")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
