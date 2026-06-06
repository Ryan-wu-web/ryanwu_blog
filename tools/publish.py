#!/usr/bin/env python3
"""
一键发布工具 - Windows兼容版
用法: python tools/publish.py
"""

import os
import subprocess
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_cmd(cmd, description):
    print("\n[%s]..." % description)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=BASE_DIR)
    if result.returncode != 0:
        print("失败: %s" % result.stderr)
        return False
    print("完成")
    if result.stdout.strip():
        print(result.stdout.strip())
    return True

def get_git_status():
    result = subprocess.run("git status --short", shell=True, capture_output=True, text=True, cwd=BASE_DIR)
    return result.stdout.strip()

def publish():
    print("=" * 50)
    print("一键发布到线上")
    print("=" * 50)
    
    status = get_git_status()
    if not status:
        print("\n没有检测到改动，无需发布")
        return
    
    print("\n检测到的改动:")
    print(status)
    
    print("\n请选择提交类型:")
    print("  1. post: 发布新文章")
    print("  2. update: 更新页面")
    print("  3. style: 样式/图片调整")
    print("  4. fix: 修复内容")
    print("  5. 自定义")
    
    choice = input("\n选择 [5]: ").strip() or "5"
    
    if choice == "1":
        default_msg = "post: add new article"
    elif choice == "2":
        default_msg = "update: page content"
    elif choice == "3":
        default_msg = "style: update design"
    elif choice == "4":
        default_msg = "fix: correct content"
    else:
        default_msg = "update: blog content"
    
    msg = input("提交信息 [%s]: " % default_msg).strip() or default_msg
    
    confirm = input("\n确认发布? (y/n) [y]: ").strip().lower() or "y"
    if confirm != 'y':
        print("已取消")
        return
    
    print("\n" + "=" * 50)
    
    if not run_cmd("git add .", "添加改动"):
        return
    
    if not run_cmd('git commit -m "%s"' % msg, "提交代码"):
        return
    
    if not run_cmd("git push origin main", "推送到远程"):
        return
    
    print("\n" + "=" * 50)
    print("发布成功！")
    print("=" * 50)
    print("\n等待 1-2 分钟后，访问 https://ryanwu.cn 查看更新")

if __name__ == "__main__":
    try:
        publish()
    except KeyboardInterrupt:
        print("\n\n已取消")
