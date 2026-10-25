---
title: "两篇 Agent 开源框架调研：AgentScope 2.0 与 Gas Town 的 Refinery"
date: 2026-10-25 12:00:00
tags: [ai, agent, open-source]
categories: [tech, dev-notes]
description: "一个是从原型到生产的国内全栈 Agent 框架，一个是 Steve Yegge 的多代理工作区管理器——两份调研合并成一篇选型笔记：什么时候该用框架，什么时候需要合并队列。"
cover: "/images/posts/agentscope-and-gastown-review/cover.webp"
---

最近调研了两个很有代表性的 Agent 开源项目：阿里的 **AgentScope 2.0**（33.9k stars）和 Steve Yegge 的 **Gas Town**（18.5k stars）。前者回答「单个 Agent 怎么造得又强又可控」，后者回答「一堆 Agent 并行干活怎么不互相踩死」。这篇是两份调研的合并选型笔记。

## AgentScope 2.0：生产级全栈框架

### 它是什么

通义实验室 SysML 团队出品（Apache-2.0，Python ≥3.11），官方口号从 1.0 的「更简单地构建多 Agent 应用」升级为 2.0 的「**构建并运行看得见、可理解、可信赖的智能体**」。版本演进三阶段：2024 论文期（0.x）→ 2025 框架化（1.x）→ 2026 生产化（2.0），2.0 发布后两个月内密集迭代了 10 个 minor 版本。

### 设计哲学：给模型让路

当模型本身越来越 agentic（自带推理、规划、工具调用），框架该做的是让路而不是用僵硬的 prompt 约束模型。三大支柱：

1. **ReAct 循环是唯一主干**，扩展点全部挂在循环上；
2. **Toolkit 是能力的唯一真相源**：Python 函数、MCP server、Skill 统一注册进一个工具箱；
3. **事件流是通用通信信道**：类型化事件把 Agent 逻辑与终端、Web UI、IM 机器人解耦——它们消费的是同一条流。

### 三层安全与内置 Service 层

2.0 最有分量的两个增量。安全上：**工具级审查 + 人审（RequireUserConfirm 事件）+ 沙箱**三层防护内置，沙箱后端有 8 种（Local/Docker/E2B/K8s 等）；权限系统可按细粒度规则拦截危险操作。工程上：**Agent Service 层**是一个开箱即用的 FastAPI 后端 + Web UI——多租户多会话、用户认证、飞书/钉钉/Discord IM 渠道、分布式 RAG、定时任务、SQL/Redis/S3 持久化全部内置。「从原型到生产」这段最费工程的路，它铺好了。

### 选型速记

**适合**：需要快速从原型走向生产；企业内要权限管控/审计/沙箱（合规敏感）；主用国内模型（Qwen/DeepSeek/Kimi/豆包/MiniMax 原生接入，10 个模型类）；需要 IM 机器人与多租户 SaaS。

**斟酌**：已有 LangGraph 状态机资产（迁移成本高于收益）；只做轻量脚本原型（2.0 概念面较大）；存量代码强依赖 1.x——**2.0 是 breaking change，不可混用**，网上大量 1.x 教程已过时。

## Gas Town：多代理工作区管理器与 Refinery 合并队列

### 它是什么

Steve Yegge（前 Amazon/Google）2026 年元旦官宣的开源项目（Go，MIT），定位是「多智能体工作区管理器」：协调 Claude Code、Copilot、Codex 等多个 AI 编码代理并行工作，用 git worktree 持久化状态，用 Bors 风格的合并队列（**Refinery**）保证代码落地。配套的 Beads（`bd`，基于 Dolt 的分布式 issue 跟踪）被定位为「编码代理的记忆系统」——一切协调状态都以 bead 形式存在。

### 最值得学的设计：beads 即状态

队列状态、安全开关、合并槽、认领——**全部放进 bead 标签与字段，不落任何文件**（ZFC，零文件状态）。重启机器后不存在「陈旧锁」问题，崩溃后可无损恢复。这是分布式系统里少见的干净取舍。

另一条金句原则（GUPP）：「如果你在自己钩子上发现了东西，你就去做」——代理领到任务立即执行，监工只观察和提醒，不当完成门禁，避免监工成为瓶颈。

### Refinery 合并队列：为 AI 工人重造 Bors

传统合并队列服务的是人类的 PR；Refinery 接的是「每分钟可能产出多条 MR 的 AI 工人」。核心规则一条：**任何人不许直推 main**。几个精巧设计：

- **batch-then-bisect**：N 条 MR 叠栈当作一个原子单元跑门禁，绿了全进、红了二分定位罪魁——吞吐与 main 的绿色兼得；
- **双层门禁**：合并前测源分支自身（并行），合并后推送前测**组合代码**（串行）——专抓「跨模块 import 断裂」这类组合才暴露的问题；
- **并发三重防**：Merge Slot 对 push 全局串行化（指数退避）+ 推送前 TOCTOU 复查 + 终态关闭时的快照校验，每一环防一类具体竞态；
- **防饥饿评分**：车队年龄每小时加分、优先级加权、重试每次扣分封顶 300——同时压住车队饿死、优先级倒置、重试刷分三种经典队列病；
- **Safety Stop**：急停就是一个 bead 标签，永不自动过期，重启后依然生效——人类否决权没有被自动化吃掉。

**局限也要说清**：tmux 是核心依赖（原生 Windows 只有最小模式）；refinery 默认以 `claude --dangerously-skip-permissions` 运行，安全性靠门禁兜底，需要自行权衡；依赖栈较重（Dolt/beads/tmux/Claude Code）。

## 合并选型笔记

两个项目其实回答的是两个不同层面的问题，放在一起看正好是一张地图：

| 需求 | 用什么 |
|---|---|
| 造一个能力强、可控、可观察的 Agent | AgentScope SDK（ReAct + Toolkit + 中间件） |
| 把 Agent 变成多人在线服务 | AgentScope Service 层（多租户/IM/RAG 开箱即用） |
| 多个编码代理并行开发同一批仓库、main 时刻保持绿色 | Gas Town（Refinery 合并队列） |
| 7×24 长任务、崩溃不丢状态 | Gas Town（Beads 账本 + worktree） |
| 企业级权限/审计/沙箱 | AgentScope 三层防护；审计面参考此前写的[可审计 Agent 系统](/2026/10/25/2026-10-25-auditable-agent-system-lessons/) |

一个共同的启发：**两者的「可靠性」都不是靠模型智能，而是靠工程结构**——AgentScope 靠状态机、权限拦截与事件类型化，Gas Town 靠合并队列、beads 状态与防饥饿评分。这和我此前写[可审计 Agent 系统](/2026/10/25/2026-10-25-auditable-agent-system-lessons/)的结论完全一致：把 agent 放进生产的门槛，从来不在模型。

## 参考来源

- **AgentScope**：[GitHub 仓库](https://github.com/agentscope-ai/agentscope)、[官方文档](https://docs.agentscope.io/)、[NEWS.md 时间线](https://github.com/agentscope-ai/agentscope/blob/main/docs/NEWS.md)、[出身论文 arXiv:2402.14034](https://arxiv.org/abs/2402.14034)、[PyPI](https://pypi.org/project/agentscope/)、[zread.ai 深度解读](https://zread.ai/agentscope-ai/agentscope)
- **Gas Town**：[GitHub 仓库](https://github.com/gastownhall/gastown)、[Refinery 源码目录](https://github.com/gastownhall/gastown/tree/main/internal/refinery)、[Steve Yegge 官宣文](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04)、[Beads 文档](https://beads.gascity.com)、[DoltHub 评测](https://www.dolthub.com/blog/2026-01-15-a-day-in-gas-town)、[zread.ai 第 14 章](https://zread.ai/gastownhall/gastown/14-refinery-merge-queue)

> 说明：两项目均为动态迭代的开源项目（AgentScope 2.0.10、Gas Town main 分支日更），数据快照 2026-10-25；Gas Town 最新 Release 停在 v1.2.1 而 main 日更，生产使用建议跟 Release；横向对比为定性判断，选型前建议以最新版本实测验证。

## 本系列其他篇目

- [把 Agent 系统从「能演示」做到「敢签字」](/2026/10/25/2026-10-25-auditable-agent-system-lessons/)
- [AI 智能体操作电脑：能力、代价与安全边界](/2026/10/25/2026-10-25-computer-use-agents/)
- [人形机器人量产竞赛](/2026/10/25/2026-10-25-humanoid-robot-mass-production/)
