---
title: "中国开源模型生态：四大家族贴近前沿，采用度是两个世界"
date: 2026-10-25 12:00:00
tags: [news, ai, llm]
categories: [tech, tech-news]
description: "BI 口径中美差距 10 月缩至约 3%；OpenRouter 上中国家族合计约 44%，但美国大企业生产环境仅约 1%。成本三层逻辑、华为共生与管制悖论。"
cover: "/images/posts/china-open-source-models-2026/cover.webp"
---

中国开源大模型在 2026 年的处境可以用一句话概括：**能力贴近前沿，采用度是两个世界**——开发者与应用路由层已成主流，美国大企业生产环境几乎缺席。这篇拆解四大家族的现状、成本逻辑与国际变量。

> 口径提醒：差距数字高度依赖测量方式，引用任何数字必须附带口径；厂商自报基准统一设置的第三方复测不存在。

## 四大家族：年内全部完成代际更新且均开放权重

| 家族 | 2026 年主线 | 许可 |
|---|---|---|
| DeepSeek | V4（4-24）→ V4-Pro-0813 → V4.1-Flash（9-10，10-17 更新） | 全部 MIT |
| 阿里 Qwen | Qwen3.5（2-16）→ Qwen3.8-Max（8-08，2.4T 总参/95B 激活） | 次旗舰 Apache-2.0，旗舰自定义 |
| 智谱 GLM | GLM-5.2（6-16）→ GLM-5.3（8-25）+ Flash | 5.2 与 Flash 为 MIT，主模型自定义 |
| 月之暗面 Kimi | K3（6-13 上传权重）→ K3.1 Pro（**API-only，无开源权重**） | K3 为 Modified MIT |

三家年内至少两次代际更新，节奏不低于美国三巨头。**但注意「开源」标签正在稀释**：Qwen3.8-Max、GLM-5.3 主模型、Kimi K3.1 Pro 均非宽松开源——「旗舰收紧、次旗舰宽松」的分层已经出现。

## 差距：多口径收敛但未归零

- Bloomberg Intelligence 基准口径：年初约 15% → 5 月 9% → 6 月 **6%** → 10 月 **约 3%**。
- Stanford HAI（Elo 口径，截至 3 月）：美国最佳领先 2.7%。
- LMArena（10-13 快照，人类偏好）：MIT 完全开源模型与榜首仍差 **37–50 Elo**。
- 单点已贴脸：Kimi K3 在 Vals Index 上距 Anthropic 最强仅 0.3 分；DeepSeek V4 Pro 的 SWE-bench Verified 96.4% 对闭源第一的 97.0%。

**结论：BI 类混合基准口径「接近前沿」成立，「完全持平」不成立**——剩余差距集中在顶级 Elo、多模态与可靠性工程。

## 采用度：相差两个数量级的两个世界

- **开发者层（主流）**：OpenRouter 周榜（10-23）DeepSeek 以 **24.4%** 居单一厂商第一，中国背景家族合计约 **44.3%**；美国公司在中国模型上的 token 占比每周超 30%、峰值 46%（CNBC 引 OpenRouter）。Qwen 半年全球下载超 30 亿次（Bloomberg）。
- **美国企业生产层（缺席）**：Menlo Ventures 调查显示企业 LLM API 中中国开源模型合计**约 1%**（Anthropic 40% / OpenAI 27% / Google 21%）。

下载量与路由份额不等于生产使用——中国开源模型的全球胜利目前发生在「开发者与应用长尾层」，尚未穿透「受合规与采购流程约束的企业核心生产层」。

## 成本优势：三层逻辑，但护城河在收窄

1. **算法效率**：DeepSeek V4 的混合注意力把 1M 上下文下单 token FLOPs 降至 V3.2 的 27%、KV cache 降至 10%；V4.1-Flash 进一步压至 890 bytes/token。
2. **工程效率**：2,048 张出口管制下的 H800 达到 272.8B tokens/天（MFU 43.7%、FP8 精度损失 <0.25%）——这批论文的开源本身就是「工程溢出」，全球推理成本曲线因此下移。
3. **以功率换算力**：SemiAnalysis《华为-DeepSeek 共生》判断 2027–28 年 DeepSeek 推理将主要运行在华为栈上；代价是 CloudMatrix 384 以约 5 倍功耗换同级能力，HBM 供给是最硬物理约束。

价格上中国旗舰约为美国旗舰的 1/3–1/7（V4-Pro $0.66/$1.98 vs Astra $10/$50），**但美国已反击**：GPT-6 Luna 与 Haiku 5.5 的 $0.10/$0.50 已压到中国 flash 档之下——「最低价」标签首次旁落。

## 管制悖论：打击反而放大开源

Nvidia 对华收入实质归零（H200 1 月获批即被北京方面禁入）；10 月美国监管密集升级（国土安全部联邦禁令、FCC 10-29 表决）。但 2026 年 6 月美国商务部首次把「闭源模型本身」纳入出口管制，**开放权重仍豁免**——制度层面意外强化了开源权重的可扩散性。另一个耐人寻味的信号：Nvidia 主动为 DeepSeek/Qwen/GLM 优化 RTX 与 DGX Spark，员工表述「每个模型都应在美国技术栈上跑得最好」——硬件厂商开始围绕中国模型做优化。

## 参考来源

- **模型官方**：[DeepSeek V4.1-Flash 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)、[DeepSeek 定价](https://api-docs.deepseek.com/quick_start/pricing)、[Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)、[GLM-5.3](https://huggingface.co/zai-org/GLM-5.3)、[Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)
- **差距量化**：[TNW：BI 6% 口径](https://thenextweb.com/news/china-ai-gap-us-record-low-6-percent-bloomberg-intelligence)、[China Daily：BI 约 3%](https://www.chinadailyasia.com/article/640782)、[Stanford HAI AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report/technical-performance)、[LMArena](https://arena.ai/leaderboard/chat/text)、[Bloomberg：中美 AI 竞赛](https://www.bloomberg.com/graphics/2026-us-china-ai-race)
- **采用度**：[OpenRouter 周榜](https://openrouter.ai/rankings)、[CNBC：美国公司 30%+ token 用中国模型](https://www.cnbc.com/2026/07/07/chinese-ai-models-costs-us-openai-anthropic.html)、[Menlo Ventures 企业调查](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise)、[Bloomberg：Qwen 30 亿下载](https://www.bloomberg.com/news/articles/2026-08-15/alibaba-ai-models-hit-3-billion-downloads-passing-meta-google)
- **成本与芯片**：[DeepSeek V3 技术报告](https://arxiv.org/html/2412.19437v1)、[《Insights into DeepSeek-V3》（ISCA 2025）](https://arxiv.org/html/2505.09343v1)、[SemiAnalysis：华为-DeepSeek 共生](https://semianalysis.com)、[CNBC：Nvidia 优化中国模型](https://www.cnbc.com/2026/08/27/nvidia-chinese-ai-models.html)、[Reuters：H200 获批即被禁](https://www.reuters.com/world/asia-pacific/us-eases-regulations-nvidia-h200-chip-exports-china-2026-01-13)
- **监管**：[Reuters：各国收紧 DeepSeek 审查](https://www.reuters.com/legal/litigation/governments-regulators-increase-scrutiny-deepseek-2026-10-20)、[Mayer Brown：模型权重管制](https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners)

> 说明：GPT-6 Astra 定价、Qwen3.8-Max 定价、GLM-5.3 参数量、Kimi K3 定价均为第三方转述；「中国模型 6 月用量首超美国」仅有 Bloomberg 转引、OpenRouter 原文未核实；相关模型竞争的月度战报见[前沿模型 10 月战报](/2026/10/25/2026-10-25-frontier-model-race-october/)。

## 本系列其他篇目

- [Robotaxi 竞争格局](/2026/10/25/2026-10-25-robotaxi-race-2026/)
- [AI 安全「黑色十月」](/2026/10/25/2026-10-25-ai-security-black-october/)
- [量子计算转折点](/2026/10/25/2026-10-25-quantum-magic-state-2026/)
- [全球 AI 监管 10 月动态](/2026/10/25/2026-10-25-ai-regulation-october-2026/)
- 相关阅读：[前沿模型 10 月战报](/2026/10/25/2026-10-25-frontier-model-race-october/)
