#!/usr/bin/env python3
"""
交互式文章创建工具
用法: python tools/new-post.py
"""

import os
import re
from datetime import datetime

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', '_posts')

def slugify(text):
    """将中文标题转换为URL友好的文件名"""
    # 保留中文、英文、数字，其他字符替换为-
    text = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text)
    text = text.strip('-')
    return text

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

def get_choice(prompt, choices):
    """获取用户选择"""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    
    while True:
        try:
            idx = int(input("请选择 (输入数字): ").strip()) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        print("  ⚠️ 无效选择，请重新输入")

def get_tags():
    """获取标签列表"""
    print("\n🏷️ 标签设置")
    print("常用技术标签: python, javascript, vue, react, ml, algorithm, linux, git, docker")
    print("常用生活标签: travel, sports, photography, reading, daily, food")
    print("(多个标签用英文逗号分隔，如: python, 爬虫, tutorial)")
    
    tags_str = get_input("标签")
    tags = [t.strip() for t in tags_str.split(',') if t.strip()]
    return tags

def create_post():
    """创建新文章"""
    print("=" * 50)
    print("📝 创建新文章")
    print("=" * 50)
    
    # 1. 选择文章类型
    post_type = get_choice("文章类型", ["技术笔记", "生活随笔"])
    category = "tech" if post_type == "技术笔记" else "life"
    
    # 2. 文章标题
    title = get_input("文章标题")
    
    # 3. 日期
    today = datetime.now().strftime("%Y-%m-%d")
    date_str = get_input("发布日期", default=today)
    
    # 4. 标签
    tags = get_tags()
    
    # 5. 一句话描述（可选）
    description = get_input("文章描述/摘要（可选，用于SEO）", required=False)
    
    # 6. 是否有封面图（可选）
    has_cover = get_choice("是否有封面图?", ["否", "是"])
    cover = ""
    if has_cover == "是":
        cover = get_input("封面图路径 (如: /images/posts/xxx.jpg)")
    
    # 生成文件名
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    filename = f"{date_str}-{slugify(title)}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    # 检查文件是否已存在
    if os.path.exists(filepath):
        overwrite = get_choice(f"文件 {filename} 已存在，是否覆盖?", ["否", "是"])
        if overwrite == "否":
            print("❌ 已取消")
            return
    
    # 生成文件内容
    tags_str = ", ".join(tags)
    
    lines = [
        "---",
        f"title: {title}",
        f"date: {date_str} 12:00:00",
        f"tags: [{tags_str}]",
        f"categories: {category}",
    ]
    
    if description:
        lines.append(f"description: {description}")
    if cover:
        lines.append(f"cover: {cover}")
    
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
        "```python",
        "# 代码示例",
        'print("hello")',
        "```",
        "",
        "## 总结",
        "",
        "总结要点...",
        "",
    ])
    
    content = "\n".join(lines)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 50)
    print(f"✅ 文章已创建: {filepath}")
    print("=" * 50)
    print(f"\n📄 文件名: {filename}")
    print(f"📂 位置: source/_posts/")
    print(f"\n📝 接下来:")
    print(f"   1. 用编辑器打开文件继续写作")
    print(f"   2. 写完后执行: git add source/_posts/ && git commit -m \"post: add {title}\" && git push origin main")
    print(f"\n💡 提示: 你可以直接复制粘贴图片到 source/images/posts/ 目录，然后在文章中引用")

if __name__ == "__main__":
    try:
        create_post()
    except KeyboardInterrupt:
        print("\n\n❌ 已取消")
