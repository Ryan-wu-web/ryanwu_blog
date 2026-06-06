#!/usr/bin/env python3
"""
交互式项目卡片创建工具
用法: python tools/new-project.py
"""

import os
import re

PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', 'projects', 'index.md')

def get_input(prompt, required=True, default=None):
    """获取用户输入"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if default is not None:
            return default
        if not required:
            return ""
        print("  ⚠️ 此项为必填，请重新输入")

def get_multiline_input(prompt):
    """获取多行输入（按空行结束）"""
    print(f"\n{prompt}")
    print("(每行一个亮点，输入空行结束)")
    lines = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        lines.append(line)
    return lines

def add_project():
    """添加新项目到项目页面"""
    print("=" * 50)
    print("💼 添加新项目")
    print("=" * 50)
    
    # 1. 项目名称
    name = get_input("项目名称")
    
    # 2. 时间
    time_range = get_input("项目时间 (如: 2025/09 - 2025/11)")
    
    # 3. 角色
    role = get_input("你的角色 (如: 全栈工程师, 前端开发)")
    
    # 4. 技术栈
    tech = get_input("技术栈 (如: Vue3, SpringBoot, MySQL)")
    
    # 5. 项目链接（可选）
    has_link = input("\n是否有项目链接? (y/n) [n]: ").strip().lower()
    link = ""
    if has_link == 'y':
        link = get_input("项目链接")
    
    # 6. 一句话简介
    summary = get_input("一句话项目简介")
    
    # 7. 核心亮点
    highlights = get_multiline_input("核心亮点")
    
    # 生成项目卡片 Markdown
    card_lines = [
        "",
        f"### {name}",
        "",
        f"**时间：** {time_range}  ",
        f"**角色：** {role}  ",
        f"**技术栈：** {tech}",
    ]
    
    if link:
        card_lines.append(f"**链接：** [{link}]({link})")
    
    card_lines.extend([
        "",
        summary,
        "",
        "**核心亮点：**",
    ])
    
    for hl in highlights:
        card_lines.append(f"- {hl}")
    
    card_content = "\n".join(card_lines)
    
    # 读取现有文件
    with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在文件末尾添加新项目（在最后一个分隔线之前）
    # 找到最后一个 "---" 或文件末尾
    if "---\n\n*更多项目即将上线" in content:
        # 替换占位符
        content = content.replace(
            "---\n\n*更多项目即将上线，敬请期待！*",
            "---" + card_content + "\n"
        )
    else:
        # 在文件末尾添加
        content = content.rstrip() + "\n" + card_content + "\n"
    
    # 写回文件
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 50)
    print(f"✅ 项目 [{name}] 已添加到项目页面")
    print("=" * 50)
    print(f"\n📝 接下来:")
    print(f"   1. 查看效果: git add source/projects/ && git commit -m \"update: add project {name}\" && git push origin main")

if __name__ == "__main__":
    try:
        add_project()
    except KeyboardInterrupt:
        print("\n\n❌ 已取消")
