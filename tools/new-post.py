#!/usr/bin/env python3
"""
交互式文章创建工具 - Windows兼容版
用法: python tools/new-post.py
"""

import os
import re
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', '_posts')

def slugify(text):
    text = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text)
    return text.strip('-')

def create_post():
    print("=" * 50)
    print("创建新文章")
    print("=" * 50)
    
    # Article type
    print("\n文章类型:")
    print("  1. 技术笔记")
    print("  2. 生活随笔")
    choice = input("请选择 (输入数字): ").strip()
    category = "tech" if choice == "1" else "life"
    
    # Title
    title = input("\n文章标题: ").strip()
    
    # Date
    today = datetime.now().strftime("%Y-%m-%d")
    date_str = input("发布日期 [%s]: " % today).strip() or today
    
    # Tags
    print("\n标签设置")
    print("常用技术标签: python, javascript, vue, react, ml, algorithm, linux, git, docker")
    print("常用生活标签: travel, sports, photography, reading, daily, food")
    print("(多个标签用英文逗号分隔)")
    tags_str = input("标签: ").strip()
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    # Description
    desc = input("\n文章描述/摘要（可选）: ").strip()
    
    # Generate filename
    filename = "%s-%s.md" % (date_str, slugify(title))
    filepath = os.path.join(POSTS_DIR, filename)
    
    # Check if exists
    if os.path.exists(filepath):
        overwrite = input("\n文件已存在，是否覆盖? (y/n) [n]: ").strip().lower() or "n"
        if overwrite != "y":
            print("已取消")
            return
    
    # Build content
    lines = [
        "---",
        "title: %s" % title,
        "date: %s 12:00:00" % date_str,
        "tags: [%s]" % ", ".join(tags),
        "categories: %s" % category,
    ]
    if desc:
        lines.append("description: %s" % desc)
    lines.extend([
        "---",
        "",
        "## 引言",
        "",
        "简述这篇文章的背景和目的。",
        "",
        "## 正文",
        "",
        "主要内容...",
        "",
        "### 小标题 1",
        "",
        "详细内容...",
        "",
        "## 总结",
        "",
        "总结要点...",
        "",
    ])
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print("\n" + "=" * 50)
    print("文章已创建: %s" % filepath)
    print("=" * 50)
    print("\n文件名: %s" % filename)
    print("\n接下来:")
    print("  1. 用编辑器打开文件继续写作")
    print("  2. 写完后执行: python tools/publish.py")

if __name__ == "__main__":
    try:
        create_post()
    except KeyboardInterrupt:
        print("\n\n已取消")
