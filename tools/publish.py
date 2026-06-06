#!/usr/bin/env python3
"""
一键发布工具
用法: python tools/publish.py
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_cmd(cmd, description):
    """执行命令并显示结果"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"❌ 失败: {result.stderr}")
        return False
    print(f"✅ {description} 完成")
    if result.stdout.strip():
        print(result.stdout.strip())
    return True

def get_git_status():
    """获取Git状态"""
    result = subprocess.run("git status --short", shell=True, capture_output=True, text=True, cwd=BASE_DIR)
    return result.stdout.strip()

def publish():
    """一键发布"""
    print("=" * 50)
    print("🚀 一键发布到线上")
    print("=" * 50)
    
    # 检查改动
    status = get_git_status()
    if not status:
        print("\n⚠️ 没有检测到改动，无需发布")
        return
    
    print("\n📋 检测到的改动:")
    print(status)
    
    # 询问提交信息
    print("\n💬 请输入提交信息 (直接回车使用默认):")
    print("   1. post: add 新文章")
    print("   2. update: 更新页面")
    print("   3. style: 样式/图片调整")
    print("   4. fix: 修复内容")
    print("   5. 自定义")
    
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
    
    msg = input(f"提交信息 [{default_msg}]: ").strip() or default_msg
    
    # 确认
    confirm = input(f"\n确认发布? (y/n) [y]: ").strip().lower() or "y"
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    # 执行发布流程
    print("\n" + "=" * 50)
    
    if not run_cmd("git add .", "添加改动"):
        return
    
    if not run_cmd(f'git commit -m "{msg}"', "提交代码"):
        return
    
    if not run_cmd("git push origin main", "推送到远程"):
        return
    
    print("\n" + "=" * 50)
    print("🎉 发布成功！")
    print("=" * 50)
    print("\n⏰ 等待 1-2 分钟后，访问 https://ryanwu.cn 查看更新")

if __name__ == "__main__":
    try:
        publish()
    except KeyboardInterrupt:
        print("\n\n❌ 已取消")
