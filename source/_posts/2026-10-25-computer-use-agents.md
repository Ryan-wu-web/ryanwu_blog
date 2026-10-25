---
title: "AI 智能体操作电脑：能力、代价与安全边界"
date: 2026-10-25 12:00:00
tags: [news, ai, agent]
categories: [tech, tech-news]
description: "OpenAI、微软、谷歌把 computer use 变成正式商品，但社区实测：同样的任务比结构化 API 慢数百倍、贵约 45 倍；提示注入是结构性威胁。一份砍掉营销水分的盘点。"
cover: "/images/posts/computer-use-agents/cover.webp"
---

2026 年 9–10 月，「智能体操作电脑」（computer use / agentic browsing）集中变成了正式商品：OpenAI 在 DevDay（9-29）把 Agents API 的 computer use 正式开放，谷歌发布 Agent Compute Engine（10-22），微软 Copilot Studio 持续更新。但基准测试与社区实测给出的图景一致：**短任务基本可用，长链路任务零人工干预成功率仍只有约 35%（OpenAI 自报）**。这篇把营销话术逐条对到实际证据上。

## 五类方案速览

| 方案 | 状态 | 执行环境 | 代表定价 |
|---|---|---|---|
| OpenAI Agents API | 9-29 正式开放 | OpenAI 托管浏览器/虚拟机 | GPT-6.1 Sol $2/$10 每百万 token；第三方测单任务 $0.72 |
| 微软 Copilot Studio | 5 月 GA | 托管 Windows（网页 + 桌面应用） | 按动作计费：5 credits/动作 ≈ $0.05 |
| 谷歌 Agent Compute Engine | 10-22 客户预览 | 每 agent 独立 microVM（Titanium 芯片硬件隔离） | 未公开 |
| Anthropic computer use | 2024-10 首发、持续迭代 | API-only，VM 与编排自建 | token 计费，每步一张截图 |
| 开源 Browser Use 等 | 持续演进（118K+ GitHub stars） | 本地或自选云 | 框架免费，模型自选 |

## 最重要的定性结论：基准分数 ≠ 生产可靠性

- Snorkel 对 OSWorld 2.0 的分析：**在 OSWorld 拿 85% 的系统，真实工作流失败率仍可达约 80%**——基准任务有明确起终点和干净环境，生产环境有弹窗、多因素认证、动态 DOM。
- OpenAI 自己的披露同样保守：8–16 小时长任务的零人工干预成功率从 2026 年 1 月的 10% 升至 7 月的 35%——三分之二的长任务仍需要人介入。
- OSWorld 最好成绩「已超人类」（AGI Inc 自报 76.26%），但公开可复现轨迹的最佳成绩只有约 41.4%——**自报分数与可验证成绩的差距，是本领域营销水分的主要来源**。

## 开发者社区的声音：computer use 是最后手段

Hacker News 9 月的热帖《Computer Use 比结构化 API 贵 45 倍》值得整段转述：同一个网页表单任务，视觉 agent 走 computer use 花 **17 分钟**，结构化 API 方案 **0.5–2.8 秒**，成本差约 45 倍。高赞评论的总结：「Computer use 是惊人的 demo，但结构化 API 才是付得起服务器账单的生产方案。」

社区公认的合理落点：**没有 API 的遗留系统**（酒店 PMS、XP 时代内部系统、不给 API 的医疗 EHR）、**端到端测试**（有团队一次跑出 116 条用户流）、本地 GUI 调试。另一个高频技术观察：无障碍树 / Playwright MCP 常常比纯视觉方案更稳。

对微软的口碑更直接：r/copilotstudio 的高赞讽刺帖是有人用 Claude 的 computer use 在浏览器里**替他搭建** Copilot Studio 智能体——「唯一能让复杂东西真正跑起来的方式」。

## 「Agentic PC」的营销与事实

| 说法 | 核查结论 |
|---|---|
| AMD「已出货 50 万+ 台 Agentic PC」 | 出货量而非使用量；类别为 AMD 自创标签，无方法论 |
| 「对比 Intel 领先 1.1–32.2 倍」 | 上限来自对方内存墙，且未对比 5 天后上市的 RTX Spark |
| 「本地跑 320B 模型」 | 技术真实（稀疏 MoE、约 20 token/s）但属演示级吞吐，撑不起视觉智能体循环 |
| 微软「每月 2 万亿次本地推理」 | 数字真实但主要由搜索、图像等系统级轻负载贡献 |

**判断：硬件是真进步（192GB 统一内存让本地跑百亿至三千亿参数稀疏模型成为可能），品类是营销先行。** 真正的分水岭是出现只有本地 NPU 才能跑的常驻智能体负载——目前还没有。

## 网络生态正在「设卡收费」

- **Cloudflare 转折点**：自 2026-09-15 起对广告支持页面**默认拦截** AI 训练与 Agent 爬虫（20 种），付费放行（HTTP 402）——智能体在公开网页上的默认身份从「用户」变成「需付费的爬虫」。
- **MCP 成为事实标准**：OpenAI、谷歌、微软、AWS 全部支持；2026 年被称为「MCP 企业落地元年」。
- **身份与支付**：Entra Agent ID、1Password×Claude 的凭据隔离、AP2/x402 支付协议群——「按任务计费」的智能体商务基础设施已就位。

## 安全：最大的落地阻力

**间接提示注入是结构性威胁**：网页、邮件、隐藏白字中埋藏指令，劫持已登录、有凭据的智能体。Akamai 的「CometJacking」证明攻击者不再需要偷密码——劫持那个已登录的智能体就够了；其 7 月研究演示了从侦察到「免费机票」的完整注入链。另有统计称 40%+ 企业已安装浏览器侧 AI 扩展，「影子 IT」治理问题同步浮现。

防御现状：Anthropic 用 RL + 分类器把特定攻击场景的成功率压到 1%（自报，且自认「不是解决方案」）；谷歌 ACE 走架构级路线——**凭据彻底放在沙箱之外、经代理注入**，按「智能体一定会被攻陷」设计。业界共识：纵深防御（模型鲁棒 + 架构隔离 + 边界检测 + 人工审批）是当前唯一可行解；高危动作（付款、删除、外发）强制 human-in-the-loop。

## 真正上岗的案例

最接近「数字员工规模化」的公开案例在医疗：Asteroid.ai 基于 Anthropic computer use 的智能体每周数千个在医疗系统运行（6 个月增长 8 倍）；AKASA 的住院编码平台出院后约 90 秒完成编码——EHR 不给 API，正是 computer use 的典型甜区。但要诚实：落地集中在**窄场景、封闭系统、有人类审批**的三角内；「替代完整岗位」的可验证公开案例，目前没有找到。

## 给开发者与企业的三句话

1. 优先级永远是 **API > MCP > DOM 自动化 > 视觉 computer use**——把后者当最后手段与测试工具。
2. 长任务按「35% 零干预成功率」做工程预算：重试、状态恢复、人工介入 UI 都是必需品。
3. 采购 Agentic PC 前问两个问题：要跑的模型吞吐是多少 token/s？有没有必须本地的合规约束？两个都答不上，普通 PC + 云 API 更划算。

## 参考来源

- **官方**：[OpenAI DevDay 回顾](https://openai.com/index/devday-2026-recap)、[OpenAI computer use 指南](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)、[微软 Copilot Studio computer use GA](https://techcommunity.microsoft.com/blog/copilot-studio-blog/computer-using-agents-in-microsoft-copilot-studio-are-now-generally-available/4519427)、[微软 hybrid intelligence](https://blogs.windows.com/windowsexperience/2026/10/07/building-windows-for-hybrid-intelligence)、[谷歌 ACE 发布](https://cloud.google.com/blog/topics/ai-infrastructure/introducing-agent-compute-engine-and-expanded-agent-governance)、[Anthropic computer use 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[Anthropic 提示注入防御](https://www.anthropic.com/research/prompt-injection-defenses)
- **基准与核查**：[OSWorld](https://osworld-v1.xlang.ai)、[Snorkel：OSWorld 2.0 分析](https://snorkel.ai/blog/osworld-2-0-why-computer-use-agents-fail-most-tasks)、[shattered.io：AMD 50 万台核查](https://shattered.io/amd-500k-agentic-pcs-shipped-before-rtx-spark-2026)、[Tom's Hardware：AMD 报道](https://www.tomshardware.com/pc-components/cpus/amd-attempts-to-get-ahead-of-expected-rtx-spark-launch-with-gorgon-halo-ai-benchmarks-company-says-it-has-shipped-over-half-a-million-agentic-pcs-to-date)
- **社区与案例**：[HN：贵 45 倍](https://news.ycombinator.com/item?id=48024859)、[Browser Use](https://github.com/browser-use/browser-use)、[Asteroid.ai 医疗案例](https://asteroid.ai/blog/computer-use-in-healthcare)、[Akamai CometJacking](https://www.akamai.com/blog/security/cometjacking-how-one-click-can-turn-perplexitys-comet-ai-browser-against-you)、[Cloudflare AI 流量新政](https://blog.cloudflare.com/content-independence-day-ai-options)、[McKinsey State of AI（40% 大企业部署）](https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points)

> 说明：OSWorld 类基准为动态快照；厂商自报成绩（UiPath 82%、AGI Inc 76%）均需打折读；Reddit/HN 为方向性参考而非统计结论。

## 本系列其他篇目

- [人形机器人量产竞赛：中国出货占 95%](/2026/10/25/2026-10-25-humanoid-robot-mass-production/)
- [算力狂潮撞上电力瓶颈](/2026/10/25/2026-10-25-ai-infrastructure-energy/)
- [前沿模型 10 月战报](/2026/10/25/2026-10-25-frontier-model-race-october/)
- [特斯拉与 SpaceX 拟合并](/2026/10/25/2026-10-25-tesla-spacex-merger/)
- 相关阅读：[AI 周报（Agent 安全事件链）](/2026/10/02/2026-10-02-ai-weekly/)
