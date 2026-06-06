#!/usr/bin/env python3
"""
交互式项目卡片创建工具 - Windows兼容版
用法: python tools/new-project.py
"""

import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', 'projects', 'index.md')

def add_project():
    print("=" * 50)
    print("添加新项目")
    print("=" * 50)
    
    name = input("\n项目名称: ").strip()
    time_range = input("项目时间 (如: 2025/09 - 2025/11): ").strip()
    role = input("你的角色 (如: 全栈工程师): ").strip()
    tech = input("技术栈 (如: Vue3, SpringBoot): ").strip()
    
    has_link = input("\n是否有项目链接? (y/n) [n]: ").strip().lower() or "n"
    link = ""
    if has_link == 'y':
        link = input("项目链接: ").strip()
    
    summary = input("\n一句话项目简介: ").strip()
    
    print("\n核心亮点 (每行一个，输入空行结束):")
    highlights = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        highlights.append(line)
    
    # Build card
    card_lines = [
        "",
        "### %s" % name,
        "",
        "**时间：** %s  " % time_range,
        "**角色：** %s  " % role,
        "**技术栈：** %s" % tech,
    ]
    
    if link:
        card_lines.append("**链接：** [%s](%s)" % (link, link))
    
    card_lines.extend([
        "",
        summary,
        "",
        "**核心亮点：**",
    ])
    
    for hl in highlights:
        card_lines.append("- %s" % hl)
    
    card_content = "\n".join(card_lines)
    
    # Read and update file
    with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the marker to insert before
    marker = "---\n\n*更多项目即将上线，敬请期待！*"
    if marker in content:
        content = content.replace(marker, "---" + card_content + "\n")
    else:
        content = content.rstrip() + "\n" + card_content + "\n"
    
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 50)
    print("项目 [%s] 已添加到项目页面" % name)
    print("=" * 50)
    print("\n接下来:")
    print("  1. 用编辑器查看效果")
    print("  2. 执行: python tools/publish.py 发布到线上")

if __name__ == "__main__":
    try:
        add_project()
    except KeyboardInterrupt:
        print("\n\n已取消")
