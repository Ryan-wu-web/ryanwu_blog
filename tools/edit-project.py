#!/usr/bin/env python3
"""
项目修改/删除工具 - Windows兼容版
用法: python tools/edit-project.py
"""

import os
import re
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source', 'projects', 'index.md')

def list_projects():
    """列出所有项目"""
    with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all project names (lines starting with ### )
    projects = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('### '):
            name = line[4:].strip()
            projects.append((i, name))
    
    return projects, content, lines

def delete_project():
    """删除项目"""
    projects, content, lines = list_projects()
    
    if not projects:
        print("当前没有项目可删除")
        return
    
    print("\n当前项目列表:")
    for idx, (line_num, name) in enumerate(projects, 1):
        print("  %d. %s" % (idx, name))
    
    choice = input("\n要删除哪个项目? (输入数字): ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(projects):
            print("无效选择")
            return
    except ValueError:
        print("无效输入")
        return
    
    target_line = projects[idx][0]
    target_name = projects[idx][1]
    
    # Find the section to delete (from ### to next ### or end)
    start_idx = target_line
    end_idx = len(lines)
    
    for i in range(target_line + 1, len(lines)):
        if lines[i].startswith('### '):
            end_idx = i
            break
    
    # Remove the section
    new_lines = lines[:start_idx] + lines[end_idx:]
    
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("\n项目 [%s] 已删除" % target_name)
    print("执行 python tools/publish.py 发布到线上")

def edit_project():
    """修改项目"""
    projects, content, lines = list_projects()
    
    if not projects:
        print("当前没有项目可修改")
        return
    
    print("\n当前项目列表:")
    for idx, (line_num, name) in enumerate(projects, 1):
        print("  %d. %s" % (idx, name))
    
    choice = input("\n要修改哪个项目? (输入数字): ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(projects):
            print("无效选择")
            return
    except ValueError:
        print("无效输入")
        return
    
    target_line = projects[idx][0]
    target_name = projects[idx][1]
    
    # Find the section
    start_idx = target_line
    end_idx = len(lines)
    
    for i in range(target_line + 1, len(lines)):
        if lines[i].startswith('### '):
            end_idx = i
            break
    
    old_section = '\n'.join(lines[start_idx:end_idx])
    
    print("\n当前内容:")
    print("-" * 50)
    print(old_section)
    print("-" * 50)
    
    print("\n请选择修改方式:")
    print("  1. 用文本编辑器手动修改")
    print("  2. 在命令行直接编辑")
    
    method = input("选择 [1]: ").strip() or "1"
    
    if method == "1":
        print("\n请用编辑器打开: source/projects/index.md")
        print("找到项目 [%s] 进行修改" % target_name)
        print("修改后执行: python tools/publish.py")
    else:
        print("\n请输入新的项目内容 (输入 END 结束):")
        new_lines_content = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            new_lines_content.append(line)
        
        new_section = "### %s\n" % target_name + '\n'.join(new_lines_content)
        
        new_lines = lines[:start_idx] + [new_section] + lines[end_idx:]
        
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("\n项目 [%s] 已更新" % target_name)
        print("执行 python tools/publish.py 发布到线上")

def main():
    print("=" * 50)
    print("项目修改/删除工具")
    print("=" * 50)
    
    print("\n请选择操作:")
    print("  1. 修改项目")
    print("  2. 删除项目")
    print("  3. 查看项目列表")
    
    choice = input("\n选择: ").strip()
    
    if choice == "1":
        edit_project()
    elif choice == "2":
        delete_project()
    elif choice == "3":
        projects, _, _ = list_projects()
        print("\n当前项目列表:")
        for idx, (line_num, name) in enumerate(projects, 1):
            print("  %d. %s" % (idx, name))
    else:
        print("无效选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
