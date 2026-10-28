---
title: "电磁场期中备考指南：传输线、Smith 圆图与那些易错点"
date: 2026-10-25 12:00:00
tags: [study, electromagnetics, notes]
categories: [life, journal]
mathjax: true
description: "写给修电磁场（英文授课）的学弟学妹：期中四大模块的分量、最可能考的 11 类题型、传输线与 Smith 圆图的标准解题流程，以及每一条都对应丢分点的易错清单。"
cover: "/images/posts/emag-midterm-guide/cover.webp"
---

期中临近，把这学期电磁场（PIN 332，英文授课）前半程的考点整理成一篇给学弟学妹的备考指南。范围覆盖 Week 1 电磁学基础、Week 2–3 传输线理论、Smith Chart 专题；所有考点与例题数值都来自课件正文和课堂讲过的原题。

先说两句重要的实话：**这份整理是我对课件的分析归纳，不是老师公布的官方考纲**；考试范围最终以任课老师通知为准。另外课件截图涉及课程材料，这里就不贴了——好在公式和表格本身是自足的，文字版反而更方便检索。

## 期中全景：先搞清楚考什么

### 四大模块与分量

| 模块 | 课件 | 核心内容 | 复习分量 |
|---|---|---|---|
| Week 1 电磁学基础 | Week 1 | 场的概念、库仑定律、E/B 场、行波参数、复数与相量 | ★★ 概念题 + 小计算，分值不大但不能丢 |
| Week 2 传输线理论 | Week 2 | R′L′G′C′、电报方程、反射/驻波/VSWR、输入阻抗、匹配、暂态 | ★★★★★ 绝对核心 |
| Week 3 传输线理论 2 | Week 3 | Week 2 全部内容的重讲与加深，暂态/脉冲/TDR 完整例题 | ★★★★★ 与 Week 2 合并复习 |
| Smith Chart | Smith Chart Extra | 圆图操作、VSWR 读图、L 型匹配、单支节匹配 | ★★★★ 大题工具，必须练熟 |

**一个重要认知**：Week 2 和 Week 3 内容高度重叠（Week 3 相当于把传输线理论再讲一遍并补齐暂态部分），连例题都是同几道（比如 λ/4 变换器的 70.7 Ω、驻波 S=1.86）。这说明**老师极度重视传输线理论**——复习请以传输线为中心，Week 1 保住概念题和基本计算即可。

### 最可能考的题型（按优先级）

稳态综合题几乎都是同一条流水线：

```mermaid
flowchart LR
    A["ZL, Z0, f"] --> B["ΓL = (ZL−Z0)/(ZL+Z0)"]
    B --> C["S = (1+ρ)/(1−ρ)"]
    C --> D["Vmax/Vmin 与 dmax/dmin"]
    B --> E["Γ(d) = ΓL·e^(−j2βd)"]
    E --> F["Zin(d) 或 Smith 圆图"]
    F --> G["源端分压求 V0+ 等未知量"]
```

| # | 题型 | 核心公式/方法 |
|---|---|---|
| 1 | 给 Z<sub>L</sub>、Z<sub>0</sub> 求 Γ<sub>L</sub>、VSWR、V<sub>max</sub>/V<sub>min</sub> 及第一电压极值位置 | Γ<sub>L</sub>、S、极值条件 2βd−θ<sub>r</sub>=2nπ / (2n+1)π |
| 2 | 矩形脉冲的负载电压波形（6 V / −1.8 V / 0.54 V 那道） | 双阶跃分解 + (1+Γ<sub>L</sub>)V₁⁺ + q=Γ<sub>g</sub>Γ<sub>L</sub> |
| 3 | TDR 故障定位三问（Vg、故障距离、故障电阻） | d=u<sub>p</sub>Δt/2、Γ<sub>f</sub>=ΔV/V₁⁺、R<sub>f</sub> 并联拆解 |
| 4 | 用 Smith 圆图求输入阻抗 / 极值位置 | 归一化 → 等 ∣Γ∣ 圆 → WTG 顺时针 → 乘回 Z<sub>0</sub> |
| 5 | R′L′G′C′ 参数计算（同轴/双导线） | 查表公式，注意半径 vs 直径 |
| 6 | 输入阻抗、短/开路线等效元件、λ/4 变换器设计 | Z<sub>in</sub> 公式、jZ<sub>0</sub>tanβl、Z<sub>02</sub>=√(Z<sub>01</sub>R<sub>L</sub>) |
| 7 | L 型匹配网络 / 双电容匹配设计 | 串元件沿等 r 圆、并元件沿等 g 圆，实部匹配 + 虚部抵消 |
| 8 | 阶跃激励反弹图、固定点波形 | V₁⁺=Z<sub>0</sub>V<sub>g</sub>/(R<sub>g</sub>+Z<sub>0</sub>)、Γ<sub>L</sub>、Γ<sub>g</sub>、逐次累加 |
| 9 | 行波表达式读参数（A、f、T、λ、u<sub>p</sub>、方向） | y=A·cos(ωt−βx+φ₀) 各符号 |
| 10 | 相量法解串联 R-C 正弦稳态 | Z=R−j/(ωC)、电流相量=电压相量/Z |
| 11 | 概念判断/简答（真空波速、光子、右手定则、四场量单位） | 见下节 |

## Week 1｜电磁学基础：送分题都在这

### 四个场量与介质关系

**E** 电场强度（V/m）、**D** 电通量密度（C/m²）、**B** 磁通量密度（T）、**H** 磁场强度（A/m）；线性各向同性介质满足 **D**=ε**E**、**B**=μ**H**。静止电荷对应静电（Electrostatics），恒定电流对应静磁（Magnetostatics），时变电流才是电场磁场相互耦合（Dynamics）。

$$F_g=\frac{Gm_1m_2}{R^2},\qquad F_e=\frac{k_e|q_1q_2|}{R^2},\quad k_e=\frac{1}{4\pi\epsilon_0}\approx 9.0\times10^9\ \mathrm{N}\cdot\mathrm{m}^2/\mathrm{C}^2$$

$$\mathbf E=\frac{q}{4\pi\epsilon_0 R^2}\hat{\mathbf R},\qquad \mathbf F=q_t\mathbf E,\qquad \mathbf B_{\text{长直导线}}=\frac{\mu_0 I}{2\pi r}\ \text{（切向，右手定则）}$$

两个概念坑：负试验电荷受力方向与 **E** **相反**；**E** 只由**源电荷**决定、与试探电荷无关。长直导线磁场按 **1/r** 衰减（不是 1/r²），方向用**右手握持定则**：拇指沿电流，四指即磁场方向。

### 正弦行波（Week 1 计算题最大来源）

$$y(x,t)=A\cos(\omega t-\beta x+\phi_0),\qquad f=\frac1T,\quad \omega=2\pi f,\quad \beta=\frac{2\pi}{\lambda},\quad u_p=\frac{\omega}{\beta}=f\lambda$$

读图要点考试直接考：固定 t 的图读波长 λ，固定 x 的图读周期 T；ωt−βx=常数 → 沿 +x 传播，ωt+βx=常数 → 沿 −x；T/4 后波形前移 λ/4；φ₀=+π/4 表示超前参考波 T/8。

### 衰减

$$y(x,t)=Ae^{-\alpha x}\cos(\omega t-\beta x+\phi_0)\ (\alpha\ \text{单位 Np/m}),\qquad d_{1/2}=\frac{\ln 2}{\alpha}$$

包络 A·e^(−αx) 是**幅度**，不是瞬时值；幅度比 A(x₂)/A(x₁)=e^(−α(x₂−x₁))。

### 电磁波与频谱

真空中所有电磁波同速（c=1/√(μ₀ε₀)≈3.0×10⁸ m/s，c=fλ；无线电波和 X 射线一样快——课件原题答案 True，注意限定 in vacuum）；平面波中 **E⊥B** 且都垂直传播方向，传播方向用 **E×B** 判断（次序不能反）。要会按频率排序频段：HF(3–30 MHz) → VHF(30–300 MHz) → UHF(300 MHz–3 GHz) → SHF(3–30 GHz) → EHF(30–300 GHz)；常用换算：100 MHz → λ=3 m（VHF）、2.4 GHz → 12.5 cm（UHF）、60 GHz → 5 mm（EHF）。

### 复数与相量（Week 1 压轴）

$$z=a+jb=|z|e^{j\theta},\quad |z|=\sqrt{a^2+b^2}\ge 0,\quad e^{j\theta}=\cos\theta+j\sin\theta,\quad \frac1j=-j$$

$$A\cos(\omega t+\phi)\ \leftrightarrow\ A\angle\phi,\qquad \sin\theta=\cos(\theta-\pi/2),\qquad \frac{d}{dt}\leftrightarrow j\omega,\quad \int dt\leftrightarrow \frac{1}{j\omega}$$

串联 R-C 正弦稳态（课堂主线）：Z<sub>RC</sub>=R−j/(ωC)，电流相量等于电压相量除以 Z<sub>RC</sub>；电流超前电压的相角 δ=arctan[1/(ωRC)]。

**Week 1 易错点 Top 5**：词头不换算就代入（μC、nC、cm 必须先换 SI，(20 cm)²=0.04 m²）；把 ω 当 f、把 β 当 1/λ（都差一个 2π）；相角不修象限（−3+j4 的辐角是 126.87°，不是 −53.13°，用 atan2）；正弦源不转余弦直接写相量（10sin(1000t+30°) 的相量是 10∠(−60°)）；峰值与 RMS 混用（V<sub>rms</sub>=V₀/√2）。

> ⚠️ 课件 p.32 的式 (26)(28) 存在疑似排版错误，且 p.30 电路图未给数值参数。复习时以「建模 → 转相量 → 复数除法 → 恢复时域」这个方法流程为准，不要照抄那一页的公式结果。

## 传输线理论（Week 2+3 合并讲）：期中的绝对核心

### 电长度：什么时候必须用传输线理论

$$\lambda=\frac{u_p}{f},\qquad \beta l=\frac{2\pi l}{\lambda},\qquad T=\frac{l}{u_p}$$

判断标准是电长度 l/λ，不是导线的几何长度。课件原例：f=1 kHz 时 λ=300 km，60 km 线的 l/λ=0.2（相移 72°，必须按传输线算），0.6 m 线可忽略；**同一根 0.6 m 线在 100 MHz（λ=3 m）下就必须按传输线处理**。经验警戒线 l/λ ≳ 0.01。

### 单位长度参数 R′L′G′C′

R′（Ω/m）导体损耗｜L′（H/m）磁场储能｜G′（S/m）介质漏电｜C′（F/m）电场储能；理想导体 → R′=0，理想介质 → G′=0（两个独立条件）。**算完必查一致性**：均匀介质 TEM 线满足 **L′C′=με**、**G′/C′=σ/ε**。

课件原题（参数题模板）：

| 题 | 结构 | 已知 | 答案 |
|---|---|---|---|
| 2-1 | 双导线空气线（理想导体） | 半径 1 mm，中心距 2 cm | R′=0，L′≈1.20 μH/m，G′=0，C′≈9.29 pF/m |
| 2-2 | 铜同轴空气线 | 1 MHz，内外导体直径 0.6/1.2 cm | R′≈2.07×10⁻² Ω/m，L′≈0.139 μH/m，G′=0，C′≈80.3 pF/m |

> ⚠️ 拿到题先分清**半径还是直径**：双导线题给半径 1 mm，直径是 2 mm，D/d=10（不是 20）；同轴题给直径先除以 2。

### 电报方程与传播参数

$$\gamma=\sqrt{(R^{\prime}+j\omega L^{\prime})(G^{\prime}+j\omega C^{\prime})}=\alpha+j\beta,\qquad Z_0=\sqrt{\frac{R^{\prime}+j\omega L^{\prime}}{G^{\prime}+j\omega C^{\prime}}}$$

无耗线（R′=G′=0）退化出全套常用结论：

$$\alpha=0,\quad \beta=\omega\sqrt{L^{\prime}C^{\prime}},\quad Z_0=\sqrt{\frac{L^{\prime}}{C^{\prime}}},\quad u_p=\frac{1}{\sqrt{L^{\prime}C^{\prime}}}=\frac{c}{\sqrt{\epsilon_r}},\quad \lambda=\frac{u_p}{f}$$

α 单位 Np/m，β 单位 rad/m。注意 Z<sub>0</sub> 是**单个行波**的电压电流比，≠ 任意点的总电压/总电流；行波项 e^(−γz) 向 +z、e^(+γz) 向 −z；反向电流波带负号 I₀⁻=−V₀⁻/Z<sub>0</sub>。

### 反射、驻波与 VSWR

$$\Gamma_L=\frac{Z_L-Z_0}{Z_L+Z_0}=\rho e^{j\theta_r},\qquad S=\mathrm{VSWR}=\frac{1+\rho}{1-\rho},\qquad \rho=\frac{S-1}{S+1}$$

$$V_{\max}=|V_0^+|(1+\rho),\qquad V_{\min}=|V_0^+|(1-\rho)$$

$$\text{电压最大：}2\beta d_{\max}-\theta_r=2n\pi,\qquad \text{电压最小：}2\beta d_{\min}-\theta_r=(2n+1)\pi$$

**课件原例**（Z<sub>0</sub>=50 Ω，∣V₀⁺∣=1 V，Γ<sub>L</sub>=0.3e^(j30°)）：V<sub>max</sub>=1.3 V，V<sub>min</sub>=0.7 V，S=1.86；补充 d<sub>max</sub>=λ/24，d<sub>min</sub>=7λ/24，I<sub>max</sub>=26 mA，I<sub>min</sub>=14 mA。

必须形成条件反射的几条：匹配 Γ<sub>L</sub>=0｜开路 Γ<sub>L</sub>=+1｜短路 Γ<sub>L</sub>=−1｜纯电抗负载 ∣Γ<sub>L</sub>∣=1；相邻同类极值间隔 λ/2，最大与最小间隔 λ/4；**电压最大处电流最小**；V<sub>max</sub> 处 Z=Z<sub>0</sub>S（纯电阻）、V<sub>min</sub> 处 Z=Z<sub>0</sub>/S；只给 S 只能得 ρ，**定不出复负载**（相角丢了）。

### 沿线阻抗与特殊线长

$$\Gamma(d)=\Gamma_L e^{-j2\beta d}\ (d\ \text{从负载朝源量取}),\qquad Z(d)=Z_0\frac{1+\Gamma(d)}{1-\Gamma(d)}$$

$$Z_{\mathrm{in}}=Z_0\frac{Z_L+jZ_0\tan\beta l}{Z_0+jZ_L\tan\beta l}$$

| 线长 | 结果 | 备注 |
|---|---|---|
| l=nλ/2 | Z<sub>in</sub>=Z<sub>L</sub> | 阻抗不变，电压相位可能变 |
| l=(2n+1)λ/4 | Z<sub>in</sub>=Z<sub>0</sub>²/Z<sub>L</sub> | 倒置：开路↔短路互换 |
| 短路线 | Z<sub>in</sub><sup>sc</sup>=jZ<sub>0</sub>tanβl | l<λ/4 感性，可当电感 |
| 开路线 | Z<sub>in</sub><sup>oc</sup>=−jZ<sub>0</sub>cotβl | l<λ/4 容性，可当电容 |
| 开短路测量 | Z<sub>0</sub>=√(Z<sub>in</sub><sup>sc</sup>·Z<sub>in</sub><sup>oc</sup>) | 反求参数，注意 tan 分支 |

课件原例：50 Ω 馈线匹配 100 Ω 负载 → 变换段 Z<sub>02</sub>=√(50×100)=70.7 Ω，长度为**变换段内**波长的 λ/4。只对设计频率、实数负载成立。

### 集总参数匹配网络

解题思想只有两条：**实部匹配到位 + 虚部彻底抵消**。课件原题只给符号解：

$$Y_A=\frac{1}{R_s+jX},\ X=\omega L_s-\frac{1}{\omega C_1};\qquad \operatorname{Re}Y_A=\frac{1}{R_T}\ \Rightarrow\ X=\sqrt{R_s(R_T-R_s)}$$

$$C_1=\frac{1}{\omega(\omega L_s-X)},\qquad C_2=\frac{X}{\omega R_s R_T};\qquad \text{可实现条件：}R_T>R_s>0,\ \omega L_s>X$$

配套笔记的数值练习（非课件原题）：R<sub>T</sub>=50 Ω，R<sub>s</sub>=10 Ω，L<sub>s</sub>=1 μH，f=13.56 MHz → C₁≈180.0 pF，C₂≈469.5 pF。

### 暂态：反弹图、脉冲与 TDR（Week 3 的招牌大题）

四个基本量（源在 z=0、负载在 z=l 的坐标系）：

$$V_1^+=\frac{Z_0 V_g}{R_g+Z_0},\qquad \Gamma_L=\frac{R_L-Z_0}{R_L+Z_0},\qquad \Gamma_g=\frac{R_g-Z_0}{R_g+Z_0},\qquad T=\frac{l}{u_p}$$

反弹图读图规则：每次波到达端点乘该端反射系数；观察点电压是**已到达各波代数和**；负载端每次跳变是 **(1+Γ<sub>L</sub>)A**（不是 Γ<sub>L</sub>A）；反向波电流要带负号；直流终值校验 V<sub>∞</sub>=V<sub>g</sub>·R<sub>L</sub>/(R<sub>g</sub>+R<sub>L</sub>)。

**原题 ①：脉冲传播**（务必独立复现）。已知 5 V 矩形脉冲、τ=1 ns、R<sub>g</sub>=12.5 Ω、Z<sub>0</sub>=50 Ω、R<sub>L</sub>=150 Ω、l=0.6 m、u<sub>p</sub>=c。求解链：T=l/c=2 ns → V₁⁺=4 V → Γ<sub>L</sub>=0.5、Γ<sub>g</sub>=−0.6、q=Γ<sub>g</sub>Γ<sub>L</sub>=−0.3。负载波形：**6 V**（2–3 ns）→ **−1.8 V**（6–7 ns）→ **0.54 V**（10–11 ns）。为什么负载能出现比源还高的 6 V？因为负载电压增量是 (1+Γ<sub>L</sub>)V₁⁺=1.5×4=6 V。

**原题 ②：TDR 故障定位**（务必独立复现）。观测：75 Ω 匹配线（Teflon ε<sub>r</sub>=2.1），源端电压 0 → 6 V，12 μs 后降到 3 V。(a) R<sub>g</sub>=Z<sub>0</sub> 时源端分压一半 → V<sub>g</sub>=12 V；(b) u<sub>p</sub>=c/√2.1≈2.07×10⁸ m/s，d=u<sub>p</sub>·Δt/2≈1242 m（**往返必须除 2**）；(c) 跳变量 3−6=−3 V → Γ<sub>f</sub>=−0.5 → 故障处等效 R<sub>Lf</sub>=25 Ω → 由 R<sub>Lf</sub>=R<sub>f</sub>∥Z<sub>0</sub> 得 **R<sub>f</sub>=37.5 Ω**。

### 传输线易错点汇总（每条都对应一个丢分点）

1. **半径/直径**：双导线与同轴题动笔第一步先统一成半径。
2. **往返除 2**：TDR 距离 d=u<sub>p</sub>·Δt/2；漏除会得 2484 m。
3. **负载跳变**：(1+Γ<sub>L</sub>)V<sub>inc</sub>，不是 Γ<sub>L</sub>V<sub>inc</sub>。
4. **TDR 反射系数用跳变量**：6 V→3 V 是 Γ<sub>f</sub>=−0.5，不是 +0.5；25 Ω 是等效阻抗，真正并联故障电阻是 37.5 Ω。
5. **tan 的分支与角度制**：βl 用 rad，计算器 deg/rad 先确认；反求线长时解不唯一，需给范围取最小非负解。
6. **两套坐标不混用**：稳态部分负载在 z=0、朝源距离 d=−z；暂态部分源在 z=0、负载在 z=l。
7. **三个阻抗分清**：η=√(μ/ε) 是介质场阻抗；Z<sub>0</sub> 是线特性阻抗；Z(d) 是该点总电压/总电流。
8. **撇号是「每米」**：L′ 是单位长度电感，不是导数。

## Smith Chart：会画图，大题稳拿

### 圆图上有什么

底层坐标是复反射系数 Γ=Γ<sub>r</sub>+jΓ<sub>i</sub>，等电阻圆和等电抗弧是画在上面的「网格」：

| 关键点/区域 | 位置 | 含义 |
|---|---|---|
| 圆心 | Γ=0，z=1 | 匹配 |
| 最左端 | Γ=−1，z=0 | 短路 |
| 最右端 | Γ=+1，z→∞ | 开路 |
| 上半平面 | x>0 | 感性 |
| 下半平面 | x<0 | 容性 |
| 水平轴 | x=0 | 纯电阻；右交点 z<sub>max</sub>=S，左交点 z<sub>min</sub>=1/S |

课堂原题速查（Exercise 2.15，七种负载的 Γ）：z<sub>L</sub>=2 → Γ=1/3；z<sub>L</sub>=1−j1 → 0.447∠−63.4°；z<sub>L</sub>=0.5−j2 → 0.825∠−50.9°；z<sub>L</sub>=−j3 → 1∠−36.9°；短路 → −1；开路 → +1；匹配 → 0。

### 必背公式

$$z=\frac{Z}{Z_0}\ (\text{无单位！}),\qquad \Gamma=\frac{z-1}{z+1},\qquad z=\frac{1+\Gamma}{1-\Gamma}$$

$$\Gamma(d)=\Gamma_L e^{-j2\beta d},\qquad \Delta\theta=2\beta d=720^\circ\cdot\frac{d}{\lambda},\qquad S=\frac{1+|\Gamma|}{1-|\Gamma|}$$

$$y=\frac1z=\frac{Y}{Y_0},\qquad X_L=\omega L,\ X_C=-\frac{1}{\omega C},\ B_C=\omega C,\ B_L=-\frac{1}{\omega L}$$

### 标准操作流程（照做就能得分）

1. **归一化**：z<sub>L</sub>=Z<sub>L</sub>/Z<sub>0</sub>，在图上标点（等 r 圆 × 等 x 弧交点）；
2. **画等 ∣Γ∣ 圆**（即等 S 圆）：以圆心到负载点距离为半径；
3. **旋转**：向源（WTG / toward generator）**顺时针**，向负载（WTL）逆时针；转角 =720°·d/λ，**一整圈对应 λ/2**（不是 λ！）；
4. **读数并反归一化**：读出 z<sub>in</sub> 后乘 Z<sub>0</sub> 恢复 Ω。

课件原例（P25，同款题也出现在 W2 p.45–47 和 W3 第 21–23 页）：z<sub>L</sub>=2−j1，WTG 刻度 0.287 → 0.387（移 0.1λ）→ z(d)=0.6−j0.66。**WTG 外圈刻度差是电长度（距离），不是电阻——别把 0.387 当输入电阻！**

操作口诀（配套笔记总结）：

```text
上图先除 Z0，下答乘回 Z0；z、y 不带单位。
沿线等|Γ|圆，串联等 r 圆，并联等 g 圆。
朝源顺时针，一圈半波长，转角两倍电长度。
电感正抗负纳，电容负抗正纳。
匹配 = r=1 且 x=0（圆心）；并联先找 g=1，串联先找 r=1。
d 管实部到位，ℓ 管虚部清零；双解成对写，回代核验。
```

### L 型匹配网络（带完整数值的课堂原题）

**原题**：Z<sub>L</sub>=10+j5 Ω 匹配到 Z<sub>S</sub>=50 Ω，f=50 MHz，要求网络兼作高通滤波器（HPF → 串 C 并 L）。

**解题链**（答案为课件原值）：

1. 归一化 z<sub>L</sub>=0.2+j0.1，目标 z<sub>in</sub>=1；
2. 串 C₁：沿等 r=0.2 圆向下（减电抗）到与 g=1 等电导圆交点 z<sub>A</sub>=0.2−j0.4 → X<sub>C</sub>=Z<sub>0</sub>×0.4=25 Ω → C₁=1/(2πf·25)≈**127.32 pF**；
3. 并 L：此时 y<sub>A</sub>=1+j2，需并联电纳抵消 b=2 → B<sub>L</sub>=−2/50=−0.04 S → L=1/(2πf·0.04)≈**79.58 nH**；
4. **回代验证** Z<sub>in</sub>=50+j0 Ω，不能只看图上「接近圆心」。

### 单支节匹配（流程要会，数值可读图近似）

两类距离不要混：**支节位置 d**（主线上）与**支节长度 ℓ**（支节上）。并联支节（最常考）：主线沿等 ∣Γ∣ 圆找 g=1 的两个交点 → 得两组 d；支节提供 y<sub>s</sub>=−j·b<sub>d</sub> 清虚部 → 得对应 ℓ。支节与主线同 Z<sub>0</sub> 时：y<sub>oc</sub>=j·tanβℓ，y<sub>sc</sub>=−j·cotβℓ。**两组解必须同组配对**，不能交叉混搭；问 first 时取最小非负距离；负的 arctan 结果加 λ/2 取物理正长度。

### Smith Chart 易错点

1. 归一化量 z、y **不带单位**（课件 P15 原图就误标了 Ω，别学它）；
2. 朝源**顺时针**；转角是 2βd=720°·d/λ，不是 βd；
3. 一圈 = λ/2，半圈 = λ/4；
4. 相角必须用 atan2 判象限：−0.5−j0.2 是 202°，不是 21.8°；Γ=0 相角无定义；
5. 串联电容加**负**电抗、并联电感加**负**电纳（符号方向别反）；
6. 导纳反归一化是 Y=Z₀·y？——不对，是 Y=y/Z₀（Y₀=1/Z₀）；
7. 读图结果是近似值，卷面上写「≈」并回代公式核验。

## 考前冲刺清单

### 「必须会」清单（达不到就别上考场）

- [ ] 给复数 Z<sub>L</sub>：3 分钟内算出 Γ<sub>L</sub>、S、V<sub>max</sub>/V<sub>min</sub>、最近 d<sub>max</sub>/d<sub>min</sub>；
- [ ] 独立复现两道暂态原题：脉冲 6/−1.8/0.54 V 与 TDR 12 V/1242 m/37.5 Ω（W3 第 32、33 页）；
- [ ] 不看公式表写出 Z<sub>in</sub> 一般式、短/开路线输入阻抗、λ/4 与 λ/2 结论；
- [ ] 给 z<sub>L</sub> 和 d/λ：用圆图完成「标点 → 画等 S 圆 → 顺时针旋转 → 读数乘 Z<sub>0</sub>」全套；
- [ ] 复现 L 网络例题（127.32 pF + 79.58 nH），并能回代验证；
- [ ] 同轴/双导线 R′L′G′C′ 参数题：分清半径直径，算完用 L′C′=με 自查；
- [ ] 行波表达式读全参数 + 相量法 R-C 电路一条龙。

### 三天复习路线建议

| 天 | 内容 | 方法 |
|---|---|---|
| 第 1 天 | 传输线稳态（2.1–2.5 节） | 推一遍电报方程；重做 Exercise 2-1/2-2、驻波例题、λ/4 例题 |
| 第 2 天 | 暂态 + TDR + Smith Chart（2.7、3 节） | 白纸画反弹图；两道原题闭卷重做；圆图拿铅笔直尺练 3 道 |
| 第 3 天 | Week 1 + L 网络/单支节 + 公式默写 | 概念题过一遍；匹配题重做；合上资料默写全部必背公式 |

### 符号与约定速记（考前最后扫一眼）

相量约定 e^(jωt)，余弦参考，峰值相量；稳态：负载 z=0，向源 d=−z，暂态：源 z=0，负载 z=l；L′、C′、R′、G′ 撇号 = 每单位长度，归一化 z、y 无单位；电流反射系数 = −Γ<sub>L</sub>；u<sub>p</sub> 永远用**线内介质**的值 c/√ε<sub>r</sub>；常数：ε₀=8.854×10⁻¹² F/m，μ₀=4π×10⁻⁷ H/m，e=1.602×10⁻¹⁹ C，G=6.67×10⁻¹¹。

### 视频与工具资源（配套笔记里核实过的）

1. B 站 · 鼎阳科技《一个视频带你看懂史密斯圆图》(8 min)——第一遍建立图形直觉；
2. B 站 ·《史密斯圆图知识点整理及例题讲解》(17 min)——配合圆图基础题；
3. B 站 ·《史密斯圆图：L 网络阻抗匹配电路的设计》(11 min)——对应 L 网络例题；
4. B 站 ·《Smith 圆图应用之单支节匹配》(6 min)——单支节作图流程；
5. QuickSmith 网页工具（quicksmith.online）——纸面作图后核验轨迹。

## 写在最后

这份指南覆盖的是「课件里真实讲过、真实算过」的内容。传输线这部分初学时觉得抽象，但把反弹图画熟、圆图转顺之后会发现它其实是整门课最「讲道理」的部分——每一步都有明确的几何与代数对应。把每一道课件原题独立复现出来，期中就不会有意外。

祝考试顺利。

## 参考来源

- 课件：Week 1、Week 2 Transmission Line Theory、Week 3 Transmission Line Theory 2、Smith Chart Extra（本文考点与例题数值均出自课件正文与课堂讲解；课件截图涉及课程材料，此处未收录，需要图示的同学可以对照原课件）
- 考点归纳参考了本人的备考笔记、逐周知识点清单与易错点归纳；文中标注「课件原题/原例」的数值照抄课件，标注「练习」的为自编题，**不是教师公布的题目**；考试范围最终以任课教师通知为准
- B 站视频：鼎阳科技《一个视频带你看懂史密斯圆图》等四期（见正文）；QuickSmith（quicksmith.online）
