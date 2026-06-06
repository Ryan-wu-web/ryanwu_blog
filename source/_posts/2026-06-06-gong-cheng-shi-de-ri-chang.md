---
title: 工程师的日常工具链
date: 2026-06-06 17:00:00
tags: [git, docker, linux, tools, devops]
categories: tech
description: 分享日常开发中离不开的工具和最佳实践
---

## 版本控制

Git 是团队协作的基础，合理使用分支策略：
- main：生产环境代码
- develop：开发分支
- feature/*：功能分支

## 容器化

Docker 让开发环境统一，避免"在我电脑上能跑"的问题。

## 命令行效率

- 使用 zsh + oh-my-zsh 增强终端体验
-  alias 简化常用命令
-  tmux 会话管理保持工作环境
