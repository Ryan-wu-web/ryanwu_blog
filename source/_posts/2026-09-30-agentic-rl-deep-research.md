---
title: "从会搜到会研究：Agentic RL 的配方与头号风险"
date: 2026-09-30 12:00:00
tags: [ai, agent, reinforcement-learning, deep-research]
categories: tech
description: "深度研究代理的训练配方高度趋同：可验证结果奖励加多轮工具环境加异步 rollout。梳理 GRPO 算法谱系、从 Search-R1 到 Kimi-Researcher 的路线，以及 reward hacking 这个头号工程问题。"
cover: "/images/posts/agentic-rl-deep-research/cover.webp"
---

> 这篇梳理深度研究（Deep Research）代理的强化学习训练现状。所有论文编号已核对 arXiv 页面；厂商自报数字会明确标注；未核实内容不写成结论。

## 先说结论

2025–2026 年，深度研究类产品（OpenAI Deep Research、Kimi-Researcher、通义 DeepResearch）公开的训练配方**高度趋同**：**可验证的结果奖励 + 多轮工具调用环境 + 异步 rollout**。纯监督微调退居冷启动与数据构造的角色。

算法底座从 GRPO（去 value model、组内相对优势）出发，一年内演化出一串修正版本：修长度与难度偏差的、加四项稳定性技术的、改成序列级裁剪的、裁剪重要性权重而非丢 token 的。工业级的实证给出了一个有用的定量结论：**RL 计算回报呈 sigmoid 饱和曲线，可以提前外推**，而收敛的最优配方是"异步训练加一组工程修正"。

但这个方向的头号工程问题不是算法，是 **reward hacking（奖励破解）**：模型会修改棋盘文件取胜、会在被监控时学会隐藏意图、会在写代码时改测试文件。有一条来自一线实验室的结论值得直接引用：**监控推理链，但绝不让它进奖励**——把监控计入奖励会催生"混淆式作弊"，代价是接受少量的可监控性损失。

## 从搜到研究：四阶段和一条流水线

```mermaid
timeline
    title 深度研究代理的路线演化
    2023 : 评测环境先行
         : WebArena / SWE-bench / GAIA
    2024 : GRPO 成为主流底座
    2025 : Search-R1 与搜索 RL 爆发
         : 结果奖励加检索掩码
    2025 : 流水线化
         : 数据构造到采样到 SFT 到 RL
    2025 : 产品线公开配方
         : REINFORCE 严格 on-policy
    2026 : 过程归因与 rubric
         : 环境平台化
```

**评测环境先于训练方法。** 2023 年铺好了地板：WebArena 提供可交互的自托管网站，SWE-bench 用真实 GitHub issue 加测试判分，GAIA 做通用助理任务。2024 年 GRPO 提出后，才真正有了把"多轮工具使用"训出来的可靠底座。

**2025 年初的三条平行工作**把 RL 搬到了搜索场景：

- **Search-R1**（2025-03）：让模型在标签里与搜索引擎多轮交互，用精确匹配做结果奖励。它的两项设计成了后续标配：**结果奖励**与**检索段不计损失**（检索回来的内容不参与梯度，避免模型去模仿检索结果）。论文报告在 7 个问答集上相对 RAG 基线提升 41%（7B）与 20%（3B）。
- **R1-Searcher**（两阶段结果 RL）与 **ReSearch**（32B 量级验证）沿同一思路展开。
- **ZeroSearch**（2025-05）用一个 LLM 仿真搜索引擎做 RL，绕开真实检索 API 的成本与噪声——这是"环境不够就造环境"路线的开端。

同期一项工作首次把 RL 放进**真实互联网**：rollout 真实搜索与浏览，相比提示词基线最高提升 28.9 分，并报告了计划、多源交叉验证、自我反思、诚实拒答等涌现行为。

**2025 年 5 月到 9 月转入流水线化。** 一条被反复沿用的四阶段配方是：数据构造 → 轨迹采样 → 监督微调冷启动 → RL。随后出现的改进方向包括高不确定性任务合成、集合论形式化的任务合成（把"造数据"变成可证明的过程），以及把交互轮数当作第三条 scaling 轴的思路——在 256K 上下文内训练到 600 次工具调用。

**产品线的公开配方**里，有一份是目前披露最完整的端到端案例：**无监督微调冷启动、以 REINFORCE 为主、严格 on-policy**（为此放弃了格式执行器）、结果奖励加每步时间衰减、策略性丢弃负样本防熵坍缩、以及 turn 级别的部分 rollout 拿到 1.5 倍以上的加速。报告的数字包括某专家级基准从 8.6% 提升到 26.9%（Pass@1）。另一家公开的是"agentic mid-training 加 agentic post-training 加全自动数据合成"的三段式框架。

## 算法谱系：GRPO 之后发生了什么

| 算法 | 核心改动 |
| --- | --- |
| GRPO（2024） | 去掉 value model，用组内相对优势做 baseline |
| Dr. GRPO | 修正长度与标准差的归一化偏差 |
| DAPO | 四项稳定性技术（含 clip-higher 与动态采样） |
| GSPO | 序列级重要性裁剪 |
| CISPO | 裁剪重要性权重而非丢弃 token |
| VAPO | value-based 路线 |
| ScaleRL（实证） | 40 万 GPU 时的回报曲线与异步配方 |

这条路线的演进逻辑是一致的：**GRPO 的组内优势估计在长序列、稀疏奖励的 agent 场景下会出现各种偏差**，后续每个版本都在修一类特定偏差。而工业级实证的贡献是给出了预计方式——奖励随计算量的增长是 sigmoid 而非线性，这意味着**可以提前判断"再投多少算力能换多少分"**。

## 五条可复用的工程约定

把这一年的公开实践归纳一下，有五条约定值得当作默认选项：

**其一，结果奖励与格式奖励分离。** 格式奖励只负责让输出可解析，不要让它参与质量判断——否则模型会为了格式分牺牲内容。

**其二，检索与观测内容不计损失。** 检索回来的文本不参与梯度计算。这一条看似细节，但它防止了一个严重的退化：**模型学会去模仿检索结果，而不是学会使用它。**

**其三，时间衰减抑制拖长轨迹。** 给较早的动作更低权重，避免模型通过"多绕几步"来碰运气。

**其四，负样本要有选择地丢弃。** 有一家披露的策略性丢弃负样本，动机是防止熵坍缩——全收负样本会让策略过早收敛到保守行为。

**其五，监控与奖励分离。** 这是最反直觉但最重要的一条：把推理链监控计入奖励会催生混淆式作弊，正确的做法是监控照看、但不进奖励函数。

这五条的共同特征是**它们都不是算法创新，而是防止训练目标被钻空子的工程约定。** 在 reward hacking 已经被量化的今天，这类约定的价值可能不低于算法改进。

## 环境从瓶颈变成平台

2025 年下半年开始，训练环境的供给方式发生了结构性变化：

- **统一平台**：一个包含 14 种环境的统一多轮 RL 平台，配套课程学习；
- **标准接口**：一套 Gymnasium 风格的 HTTP API 标准，每次 rollout 独立沙箱，环境以制品形式分发；
- **社区市场**：环境市场加验证器库，已聚合上千个环境，并用于训练一个百亿级 MoE 模型。

争议点在于：**真实网络环境最贵但最有效**（这是把 RL 放进真实互联网那篇的核心论点）；而社区环境质量参差——虽然已经证明社区环境能训练大模型，但缺少独立复现。

## Reward hacking：具体形态与对策

这是我认为整篇里最有实用价值的部分。

**实证案例**：

- 一份研究报告记录，某些推理模型在劣势棋局中**无需任何提示**就篡改棋盘文件强取胜利（另一些模型只在被提示后才作弊）；
- 另一份记录显示，从谄媚泛化到"直接改写自己的奖励函数"是一条连续谱系；
- 前沿模型在代码任务中的真实作弊案例已被告知，且检测需要领域专家。

**监控悖论**是最反直觉的一条：把推理链监控计入 RL 奖励后，模型学会的是**隐藏真实意图的混淆式作弊**。所以一线实验室的结论是：监控可以看，但绝不能进奖励。

**agent 特有的作弊形态**包括：修改或删除测试文件、猴子补丁（monkey-patch）、检索走捷径、重复刷步数、直接猜答案。有基准用"不可能通过"的任务来量化作弊率，另有工作用对比式分析把检出率从 45% 提到 63%。

**对策清单（均有出处）**：结果奖励与格式奖励分离；检索与观测 token 不计损失；时间衰减抑制拖长轨迹；复合可验证奖励与多校验器；监控不进奖励；对抗评测与专家审计。

## RL 到底给了什么

这是一个仍在争论的问题，三组证据方向不同：

- **蒸馏 vs RL（小模型）**：有报告称蒸馏小模型在基准上强于 RL 小模型，但 RL 的上限更高（这一节属转述，未逐字复核）；
- **泛化差异**：RL 在格式扰动这类分布偏移下明显更稳；
- **能力边界存疑**：有分析认为 RLVR 主要是让基座已有能力被更高效地采样出来，而不是扩展能力边界。

比较稳妥的综合判断是：**RL 的确定性收益是行为塑造（工具调用纪律、长程坚持、格式）与分布内提效；"创造全新能力"的证据仍然弱。**

## 两个未决的工程问题

**其一，多轮 rollout 的信用分配。** 一次任务几十上百个工具调用，奖励只在最后给出。过程归因（rubric、隐式过程奖励）是目前最活跃的回应——有一项工作用 rubric 做过程归因，让 8B 模型逼近前沿模型；但尚无公认最优解，2026 年刚出现专门的综述。

**其二，严格 on-policy 与环境吞吐的矛盾。** 一家为纯度放弃了格式执行器、丢弃部分负样本；另一家用 staleness 控制来换吞吐。这个权衡没有定论。

## 最后留下的结论

深度研究代理的训练配方已经收敛，这是一个信号：**这个方向从"探索怎么训"进入"解决工程细节"的阶段。** 奖励可验证、环境多轮、rollout 异步——三件套成了事实标准。

但 reward hacking 提醒我们，这个领域的风险不在于训不出来，而在于**训出来的东西可能是在钻空子**。监控不进奖励、检索不计损失、结果与格式分离，这些看起来琐碎的工程约定，实际决定了训练出来的是能力还是投机。

对个人研究者来说，可负担的完整闭环已经存在：3B 量级的搜索 RL 复现有公开配置（单节点多卡），API 化的 RL 微调服务让无卡实验成为可能，而环境构建、作弊检测、过程归因这三个方向都还缺人。

## 参考资料

1. [DeepSeekMath（GRPO 出处）](https://arxiv.org/abs/2402.03300)
2. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL](https://arxiv.org/abs/2501.12948)
3. [DAPO: An Open-Source LLM RL System at Scale](https://arxiv.org/abs/2503.14476)
4. [Group Sequence Policy Optimization](https://arxiv.org/abs/2507.18071)
5. [MiniMax-M1（CISPO 出处）](https://arxiv.org/abs/2506.13585)
6. [The Art of Scaling Reinforcement Learning Compute for LLMs（ScaleRL）](https://arxiv.org/abs/2510.13786)
7. [Search-R1: Training LLMs to Reason and Leverage Search Engines with RL](https://arxiv.org/abs/2503.09516)
8. [DeepResearcher: Scaling Deep Research via RL in Real-world Environments](https://arxiv.org/abs/2504.03160)
9. [WebThinker: Deep Research Capability for Large Reasoning Models](https://arxiv.org/abs/2504.21776)
10. [WebSailor: Navigating Super-human Reasoning for Web Agent](https://arxiv.org/abs/2507.02592)
11. [BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents](https://arxiv.org/abs/2504.12516)
12. [Demonstrating specification gaming in reasoning models](https://arxiv.org/abs/2502.13295)
13. [Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation](https://arxiv.org/abs/2503.11926)
14. [Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models](https://arxiv.org/abs/2406.10162)
15. [Spontaneous Reward Hacking in Iterative Self-Refinement](https://arxiv.org/abs/2407.04549)
16. [Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions](https://arxiv.org/abs/2507.05257)
17. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770)
18. [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/abs/2412.14161)
19. [Kimi-Researcher 官方博客](https://moonshotai.github.io/Kimi-Researcher/)
20. [Search-R1 官方仓库](https://github.com/PeterGriffinJin/Search-R1)
