---
title: "把 Agent 系统从「能演示」做到「敢签字」：一套 AI 协作链路的工程复盘"
date: 2026-10-25 12:00:00
tags: [ai, agent, engineering]
categories: [tech, dev-notes]
description: "状态机与防重发、记忆发布门禁、三凭据身份分离、用实测数字否决自己、评测先于扩量——把一段从零搭建模型网关与记忆系统的实习经验，压缩成可复用的工程笔记。内部细节已脱敏。"
cover: "/images/posts/auditable-agent-system-lessons/cover.webp"
---

实习里我做过一件贯穿始终的事：从零搭一条「模型网关 + 个人长期记忆 + 团队记忆」的部门级 AI 协作链路（[about 页](/about/)里写过的那套）。最近把整个过程从头到尾复盘了一遍，最大的感受是：**Agent 系统的难点不在「能演示」，在「敢签字」**——敢让它跑在生产里、出了事能定位、错了能回滚。这篇把可复用的工程结论整理出来，内部细节已全部脱敏，只留方法论。

## 第一课：可靠性语义先于价值语义

系统最早的版本连「这次请求到底成没成功」都说不清。后来花力气最多的不是智能，是把状态机做实：

- **每个任务一条明确的状态机**：受理 → 生成 → 提取 → 发布/无记忆，每个终态都有名字；
- **UNKNOWN ≠ FAILED**：流式响应中断、用量无法核实时记为 UNKNOWN，绝不假装成成功，也绝不静默重试——重试由 once 语义 + 台账防重发控制，同一请求不会被重复扣费、重复写入；
- **预算熔断**：额度、Token 上限、STOP 阈值三层，超限即停而不是「先跑完再说」。

事后看这套东西的价值：**它回答的是企业内网环境最稀缺的问题——「这笔钱扣没扣、这条记忆写没写、写进去的是什么」**。McKinsey 2026 年的调查里 88% 的组织在用 AI、79% 在用 agent，但单职能规模化部署的不超过 10%——卡住的大多不是演示，是这种可信语义。

## 第二课：记忆不是存进去就行，发布要有门禁

记忆系统的核心设计只有一句话：**任何内容不经发布门禁不算「已保存」**。

原始对话先落 L0（原始层），由独立的提取模型结构化成 L1（可发布层），状态机走 PUBLISHED 门禁后才对召回和页面可见；UNKNOWN/FAILED/提取中的一律不展示为「已保存」。这个姿态不是洁癖——2026 年关于记忆投毒的研究已经很具体：四条写入通道、九种攻击模式（[arXiv:2606.04329](https://arxiv.org/html/2606.04329v1)），注入成功率可超过 95%（[arXiv:2601.05504](https://arxiv.org/html/2601.05504v2)）；Unit 42 也演示过通过间接注入污染长期记忆建立持久行为（[Unit 42](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory)）。一次错误写入被永久召回放大，就是记忆系统的死亡方式。

一个具体的工程决策：提取模型从大模型换成轻量快模型，单次提取从 15–60 秒降到约 2.3 秒、成本省约 20–30%——**提取链路值得独立选型**，它和主对话的成本曲线、延迟要求完全不同。

## 第三课：凭据分离与身份委托

系统里三种凭据严格分离：网关计费 Key、调用方 Key、用户身份 Key，各管各的。多人共享记忆时用「身份映射 + 委托签名 + 纪元撤销」：委托可撤销、旧会话在权限变更后立即失效。

后来看到微软把 agent 定义为一等身份类型的 [Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities)（带 sponsor/owner/访问策略），我意识到当时手工搭的那套身份映射，方向和行业是同构的——**agent 需要可担责的身份主体，这件事正在变成企业 IAM 的标配**，而绝大多数团队还没有动手的实践经验。

## 第四课：用实测数字否决自己

整个项目里我认为最有工程价值的决定，是一次自我否决：当时有一份很漂亮的平台化扩张计划（多 Agent 分工、知识库、高可用），可行性审查用两个实测数字把它否了——**提取输出 296/304 超过 256 的输出合同上限**、部分任务终态为 UNKNOWN——于是目标降级为「把单链路做成可重复、可观测、可回滚的闭环」，原则是「单链路门禁未通过前不引入多 Agent」。

这比任何愿景文档都值钱。Gartner 预测 40%+ 的 agentic 项目会在 2027 年底前取消，归因正是成本不清、价值不明、风控不足（[Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)）；MIT 那份「95% 试点无财务回报」的报告结论相同。**死法清单是共通的：范围过大、评测缺失、权限失控、记忆污染、成本失控、无人维护。**

## 第五课：我们做得最差的一块是评测

诚实地说：这套系统「不重复扣费、不误写记忆」做得很扎实，但「记忆到底让回答变好了没有」一直停留在零指标——检索是词法加时间兜底，没有召回命中率，没有引用准确率。这不是我们独有的坑：2026 年九大厂商的产品矩阵里，**评测与可观测是唯一没有任何独立产品的空白层**（[McKinsey State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) 里「EBIT 可归因于 AI 的比例一年持平」是同一件事的宏观投影）。

所以我的结论是：**评测会从可选项变成上线门禁**。三个最小指标就够起步：召回命中率（人工抽检「召回的内容确实相关」）、引用准确率（回答与来源一致）、任务一次通过率。没有这三个数字，扩量就是在放大一个无法证明价值的东西。

## 一张自检清单

复盘最后我给自己留了几个领先指标，任何做 Agent 系统的团队可以直接拿去用：

- UNKNOWN 请求占比 < 1%（升高 = 账务与记忆开始不可信，先于事故）；
- 回滚耗时 < 30 分钟（变长 = 发布纪律在松懈）；
- 人工验收等待 < 5 天（拖长 = 瓶颈已从代码转移到「他人时间」）；
- 记忆周活跃人数（连续一季走低 = 平台正在退化成演示）；
- 影子 AI 使用率不降 = 自建平台的体验输给了私人工具，先修体验再谈治理。

## 写在最后

协议层在快速标准化（[MCP](https://blog.modelcontextprotocol.io/posts/2026-07-28) 已是无状态的 web 规模设计），治理面在被商品化（[Agent 365](https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations) 按席位卖控制面）——这些都不值得自研。值得自研的是两块没人替你做的：**私有数据的记忆层，和「什么算干好了」的评测层**。

到 2028 年，企业要招的大概不是「会用 agent 的人」，而是**敢把 agent 放进生产并签字的人**。这篇笔记是我朝那个方向攒的第一块砖。

## 参考来源

- **协议与身份**：[MCP 2026-07 无状态规范](https://blog.modelcontextprotocol.io/posts/2026-07-28)、[Entra Agent ID 文档](https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities)、[GitHub Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents)
- **治理与效果**：[Microsoft Agent 365 GA](https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations)、[McKinsey State of AI 2026](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)、[Gartner：40% agentic 项目将被取消](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)、[METR：长任务时间地平线](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks)
- **记忆安全**：[arXiv:2606.04329（记忆投毒四通道九模式）](https://arxiv.org/html/2606.04329v1)、[arXiv:2601.05504（注入成功率）](https://arxiv.org/html/2601.05504v2)、[Unit 42：长期记忆投毒](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory)

> 说明：本文为个人实习复盘的方法论部分，单位、部署环境、同事信息、内部文档与合规细节均已剔除；文中系统架构描述与[关于我](/about/)页面的公开介绍一致。相关外部趋势的更多报道见[AI 智能体操作电脑](/2026/10/25/2026-10-25-computer-use-agents/)与[AI 安全「黑色十月」](/2026/10/25/2026-10-25-ai-security-black-october/)。
