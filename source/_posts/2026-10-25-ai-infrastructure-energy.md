---
title: "算力狂潮撞上电力瓶颈：四大厂两年 1.1 万亿美元 capex"
date: 2026-10-25 12:00:00
tags: [news, infrastructure, energy]
categories: [tech, tech-news]
description: "四大云厂商 2025-2026 资本开支合计约 1.13-1.17 万亿美元；核电长协锁的是存量，真正的边际供给是燃气与储能；并网排队 2,060 GW、PJM 容量价两年涨约 10 倍。"
cover: "/images/posts/ai-infrastructure-energy/cover.webp"
---

「万亿」在 2026 年从预测变成了财报数字：四大云厂商 2025 年实际资本开支约 4,110 亿美元，2026 年官方指引合计约 7,200–7,600 亿美元——**两年合计约 1.13–1.17 万亿美元**。而供给侧的真相与新闻标题相反：声势最大的核电长协锁定的是存量，真正的边际供给是燃气与储能，两者都撞上并网排队。这篇把「钱、电、政治」三条线各自核清。

> 口径说明：capex 为各公司全部资本开支（AI 是主要但非唯一去向）；2025 年为财报实数、2026 年为指引；媒体估计与待核项单独标注。

## 钱：四大厂两年 1.1 万亿，中国以 1/6 的钱追 88% 的增速

| 公司 | 2025 实际 | 2026 指引 |
|---|---|---|
| 亚马逊 | ~1,318 亿美元 | ≤2,000 亿（官方），机构估 2,000–2,200 亿 |
| 微软 | ~1,180 亿（日历年换算） | ~1,900 亿（媒体换算） |
| Alphabet | ~914 亿 | 1,750–1,850 亿（官方） |
| Meta | ~697 亿 | 1,250–1,450 亿 |

「2026 年全球数据中心支出超 1 万亿美元」出自 Dell'Oro（2026 年 6 月上调，其 2025 年 2 月版原预测 2029 年才破万亿）——注意与 IDC 的口径区分（IDC 的 1 万亿指 2029 年 AI 支出）。

**谷歌云「96 万颗 GPU」核实**：NVIDIA 与 Google Cloud 官方博客确认的是**多站点集群规划上限 96 万颗** Rubin GPU（单站点上限 8 万颗）——规划上限，非已部署量。

**中国侧**：阿里、腾讯、字节、三大运营商 2025 年合计约 6,000–6,500 亿元，2026 年约 9,000 亿元以上——约为美国四大厂的 1/5–1/6；但 IDC/浪潮预计 2026 年中国智算规模 2,576.5 EFLOPS、**同比 +87.9%**，且华为昇腾已拿下中国 AI 芯片 28% 份额（IDC，2026-10）。

## 电：签了的合同 vs 2030 年能亮起来的灯

### 核电长协：锁存量，不是新增

滚动 12 个月六笔核电大单加总约 8.4 GW（扩展到 18–24 个月窗口约 10 GW——「超 10 GW」是更宽松口径）。微软-Constellation（三里岛重启 835 MW）、Meta-Vistra（>2,600 MW）、亚马逊-Talen（1,920 MW）等签约项目中，**物理新增仅 2–3 GW，其余为存量转购**。SMR（小型堆）2030 年前实际并网不足 1 GW——Bulletin of the Atomic Scientists 的判断：多数 SMR 宣传实为 PR，交付普遍滑至 2030 年代，与 2026–2028 的需求拥堵期错配。

### 真正的边际供给：燃气与储能

GE Vernova 燃机积压 + 槽位预留达 **116 GW**（交付排至 2028/2029，CEO 预计年底槽位售罄至 2030）；Siemens Energy 积压近 70 GW、Mitsubishi Power 35 GW——「三大主机厂 2028/2029 年前售罄」成立。典型配套：Meta 路易斯安那 Hyperion 园区（Entergy 三座 CCGT 约 2.26 GW + 再加 7 台燃气机组）。储能方面 IEA 估计 2030 年需 20–25 GW 电池配套数据中心——但两者都撞上同一个墙：**并网排队**。

### 电网：2,060 GW 排队，容量价两年 10 倍

LBNL《Queued Up 2026》：全美活跃并网排队 2,060 GW（约 8,200 个项目）；建成项目从申请到商运中位时长超 5 年；2000–2020 年提出申请的容量中仅 13% 最终建成——排队数字对真实供给严重高估。价格信号更直接：PJM 容量拍卖从 2025/26 年度的 $28.92/MW-day 涨到 2027/28 年度的约 $330（触及上限），**两年约 10 倍**；PJM 独立监测机构测算数据中心负荷已给其他用户增加约 231 亿美元成本。

**核心判断：供给侧弹性在 2029–2032 年（燃气新机组批量投运、首批 SMR、新输电投产），与算力需求曲线存在约 3 年错位——是「算力等电」，不是「电等算力」。**

## 政治：52% 要暂停，但 32% 怕输给中国

CNBC 10 月 24 日全国民调：**52% 注册选民支持暂停先进 AI 开发直到国会通过监管，63% 反对在家附近建数据中心**。2025 年弗吉尼亚州长选举（数据税、电价成为两党共同议题）是模板；孟菲斯 xAI 暂停令表决（18 个月暂停被市议会 6:6 否决）、佐治亚县级暂停令扩散显示地方阻力显性化。联邦的 EO 14318 能加速联邦许可，却无法取消地方分区否决权——**「联邦快、地方慢」是净效果**。

## Vera Rubin：平台兑现与产能天花板

Rubin GPU（约 3,360 亿晶体管、288GB HBM4）机柜 2026 下半年起出货，OpenAI-NVIDIA 10 GW 合作首个 1 GW 于 2026 下半年部署（[芯片周报此前报道过交付落地](/2026/10/02/2026-10-02-semiconductors-weekly/)）。但 TrendForce 因 HBM/CoWoS 供给约束已把 Rubin 占 2026 年 Nvidia 高端出货比例从 29% 下调至约 22%；NVL144 机柜良率年初 45–52%、目标 6 月约 70%。按 Wolfe 口径 2026 年全球 Rubin 机柜约 2 万台——「96 万颗」级别的多站点集群是平台叙事，实际节奏取决于 CoWoS/HBM4 与电力到位。

## 中美模式分岔

| 维度 | 美国 | 中国 |
|---|---|---|
| 决策机制 | 资本市场驱动；并网排队 + 地方否决权 | 国家规划（东数西算）；运营商/国企执行 |
| 电源结构 | 燃气为主增量 + 核电长协锁存量 | 西部风光 + 特高压西电东送 |
| 电价 | PJM 容量价两年 10 倍、231 亿美元转嫁争议 | 电力总体充裕，数据中心占总用电约 2–3% |
| 芯片 | Nvidia 垂直整合 | 华为 28% 份额；CloudMatrix 384 算力约 NVL72 的 1.7 倍、功耗约 4 倍 |

**制度含义**：美国的瓶颈不在钱而在「许可-电网-政治」三重约束；中国的瓶颈在芯片与能效，不在土地、电网或选民。若出口管制持续，中美**每瓦算力**的差距将比总量差距更持久。

## 参考来源

- **资本开支**：[Statista：Big Tech capex](https://www.statista.com/chart/35046/capital-expenditure-of-meta-alphabet-amazon-and-microsoft/)、[Bloomberg：2026 约 6,500 亿](https://www.bloomberg.com/news/articles/2026-02-06/how-much-is-big-tech-spending-on-ai-computing-a-staggering-650-billion-in-2026)、[Dell'Oro 万亿预测](https://www.delloro.com/news/ai-infrastructure-buildouts-and-memory-cost-inflation-drove-data-center-capex-higher-in-1q-2026)、[NVIDIA×Google Cloud：Vera Rubin](https://blogs.nvidia.com/blog/google-cloud-vera-rubin-infrastructure)
- **能源**：[IEA：Energy and AI](https://www.iea.org/reports/energy-and-ai)、[LBNL：数据中心能耗报告](https://eta-publications.lbl.gov)、[Bulletin of the Atomic Scientists：SMR 现实核查](https://thebulletin.org)、[Carbon Brief：中国数据中心能耗](https://www.carbonbrief.org/explainer-how-china-is-managing-the-rising-energy-demand-from-data-centres)
- **电网与政治**：[LBNL：Queued Up 2026](https://emp.lbl.gov/queues)、[IEEFA：PJM 容量价 10 倍](https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10)、[PJM 监测报告](https://www.monitoringanalytics.com/reports/Reports/2026/IMM_Analysis_of_the_20272028_RPM_Base_Residual_Auction_Part_A_20260105.pdf)、[CNBC 民调](https://www.cnbc.com/2026/10/24/trump-ai-data-centers-voter-backlash-midterms.html)、[白宫 EO 14318](https://www.whitehouse.gov/presidential-actions/2025/07/accelerating-federal-permitting-of-data-center-infrastructure)
- **中国对比**：[Reuters/IDC：华为 28% 份额](https://www.reuters.com/business/retail-consumer/nvidias-china-ai-chip-share-falls-huawei-closes-gap-report-finds-2026-10-13)、[SemiAnalysis：CloudMatrix 384](https://newsletter.semianalysis.com/p/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72)、[TrendForce：Rubin 占比下调](https://www.trendforce.com/presscenter/news/20260408-13003.html)

> 说明：微软 PPA「160 亿美元」、EPRI 2026 版「9–17%」区间、Dell'Oro 2030 年 3 万亿预测、字节跳动全部数字均为媒体估计或转引，未获一手核实；Meta/Alphabet/微软/亚马逊 9 月季度财报在截稿时尚未全部发布，指引可能再上调。

## 本系列其他篇目

- [人形机器人量产竞赛：中国出货占 95%](/2026/10/25/2026-10-25-humanoid-robot-mass-production/)
- [AI 智能体操作电脑：能力、代价与安全边界](/2026/10/25/2026-10-25-computer-use-agents/)
- [前沿模型 10 月战报](/2026/10/25/2026-10-25-frontier-model-race-october/)
- [特斯拉与 SpaceX 拟合并](/2026/10/25/2026-10-25-tesla-spacex-merger/)
- 相关阅读：[芯片周报（Vera Rubin 开始交付）](/2026/10/02/2026-10-02-semiconductors-weekly/)
