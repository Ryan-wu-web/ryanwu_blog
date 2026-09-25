---
title: 关于我
date: 2026-06-05 12:00:00
aside: true
top_img: /about-bg.jpg
---

## 👋 你好，我是 Ryan

我是吴启文，南京邮电大学通信工程本科在读。

用一句话介绍自己：**我能把东西做出来，也能把它讲清楚、推着它落地。**

这两年我的精力分在几个看上去不太相干的方向——工业现场的 AI 落地、校园市场的从零开拓、技术活动的组织。但它们底层是同一件事：**把模糊的目标拆成能交付的东西，然后推动它真的跑起来，而不是停在演示阶段。**

> 这页写得有点长。想快速了解的话，看每节的第一段就够；想细看某一段，我把过程和数据都留在下面了。

---

## 🚀 现在在做的事

2026 年 7 月起，我在**中国中车数字科技**做 AI Agent 开发实习。手上有两条线。

### 让机器看懂电力设备

我独立负责**电力设备智能巡检机器人的视觉算法模块**——把巡检现场"看一眼设备状态"这件事，拆成四类可识别、可验证的视觉任务：

| 巡检对象 | 要读出什么 | 难在哪 |
| --- | --- | --- |
| 仪表 | 读数、单位 | 视角偏、反光、刻度密、指针细 |
| 开关 | 开/合、档位 | 类别外观接近、角度变化、遮挡 |
| 指示灯 | 亮/灭、颜色 | 环境光干扰、目标本身很小 |
| 温度 | 温度值 | 小字符、模糊、字段容易混 |

方案不是"把所有图片丢给一个大模型"，而是**按任务分工**：检测模型负责定位和稳定类别，OCR 负责数字字段，多模态模型处理语义复杂的画面和复核，最后统一成结构化字段输出。

<div class="about-note">
  <div class="about-note-img">
    <img src="/images/about/crrc-building.webp" alt="中车数字科技办公楼外景">
  </div>
  <div class="about-note-text">
    <p>2026 年 7 月，我进入中国中车数字科技做 AI Agent 开发实习。这也是我第一次完整参与「从现场需求到系统落地」的过程——不再是做完一个 Demo 就结束，而是要真的有人用、真的要能一直跑住。</p>
  </div>
</div>

我做的不只是模型本身——还包括**设计模型输出的字段契约**，让结果能被上位机消费、能给机械臂链路提供定位和位姿信息。这一步才是算法能不能真正进系统的分水岭：**下游系统没办法靠一段自然语言去猜下一步该做什么。**

### 让一群人和一群 Agent 一起干活

另一条线，我独立负责了**部门级 AI Agent 协作体系**的方案设计、组件选型、部署集成和内部推广。

它要解决几个很具体的问题：模型入口太分散、Agent 的执行过程没法追踪、项目背景每换一次会话就要重新讲一遍。

我设计的核心是一条**双路径**：标准化、低风险的任务交给角色型 Agent 团队去跑；重要任务则通过记忆系统把上下文完整带到员工本地的 AI 编程工具里，由人接着做。

> 这里有个我后来才想明白的判断：**"人工接管"不等于"Agent 失败"。** 计划内的人工审核本来就是安全设计的一部分，和异常接管完全是两回事——把它们混进同一个指标里，就永远看不清系统到底哪里不行。

---

## 📈 我也把一件事从零卖出去过

这段经历我自己都没想到会写进一个技术博客里。

2024 年 8 月到 2026 年 7 月，我在**优课达**做学校经理，负责南京邮电大学多个学院的校园市场。业务是面向在校生的 AI 编程学习、项目实践与职业发展课程。

完整的链路是这样：

```text
获客 → 需求诊断 → 方案匹配 → 异议处理 → 成交 → 交付服务 → 复购转介绍
```

我在里面具体做的是：

- 组织团队累计开展 **1000+ 人次**一对一需求沟通——不是群发消息，是先搞清楚对方的专业、年级、基础和真实目标，再决定要不要推；
- 把做得好的人的打法沉淀成**可复制的流程**：线索怎么记、需求怎么打标签、高频异议怎么答，让新人不用从零摸索；
- 搭建并运营覆盖 **50+ 人**的三级校园团队，直接培养 4 名学校负责人和 10 名实习生。

**结果**：负责的团队累计实现约 **100 万元销售额**，获客线索至成交转化率 **60%**，课程客单价约 1.6 万元。

> 口径说明：1000+ 是团队累计的沟通**人次**，100 万是**团队**业绩、不是我个人的。我把这些讲清楚，是因为含糊过去没有意义——真被追问起来，边界不清反而更减分。

**这段经历对我后来做产品的影响，比看上去大。** 它让我很早就习惯一件事：用户说出来的需求，往往不是他真正的问题。价格高、没时间、怕学不会——这些异议背后各有各的真实顾虑。所以现在做 AI 产品，我会先问"他到底卡在哪一步"，而不是先想功能。

---

## 🧪 我自己做的一个项目：Smart Price AI

起因是我自己买东西时的一个真实卡点：**在店里看到一件商品，拍照、搜同款、比参数、看价格——中间要跳好几个 App，最后还是不确定该买哪个。**

所以我做了一个 AI 拍照识物与购物决策助手：

```text
拍照识别 → 补充需求 → 检索商品知识 → 约束过滤 → 候选排序 → 证据化推荐 → 继续追问
```

它最初是**字节跳动 AI 全栈挑战赛**的参赛原型，赛后我把它继续往完整产品做。核心想法是：**别让模型"给你一段建议"，而是让它把"为什么推荐这个"的依据摊开。**

比如你拍一双鞋，问"适不适合每天通勤，预算 800 以内还有没有更舒服的"——系统要能把图片里识别到的商品，和你说的预算、场景这些约束接上，再去检索和排序，而不是凭空生成一段听起来很合理的推荐。

有个设计我印象很深：**硬约束不能未经用户确认就自动放宽。** 预算就是预算，检索不到就直接说检索不到，不能悄悄推一个超预算的给你。

评测这块我做得还不够正式——当时主要是靠日志和一个现成的评测工具在观察效果，没有搭起完整的评测体系。**这是这个项目下一步最该补的地方。**

- 代码开源在 GitHub：[Ryan-wu-web/smart_price_ai](https://github.com/Ryan-wu-web/smart_price_ai)
- 参加了 2026 年字节 AI 全栈挑战赛并顺利完赛

---

## 🎓 教育 · 荣誉 · 证书

**教育**

| 学校 | 专业 | 学历 | 时间 |
| --- | --- | --- | --- |
| 南京邮电大学 | 通信工程 | 本科 | 2024/09 – 2028/06 |

大学英语四级（CET-4）、大学英语六级（CET-6）

**证书**

- **AIGC 高级 AI 生成应用师** — 工业和信息化部教育与考试中心，2026/07
- **携程 2026 前端训练营 · 日常实习绿卡**
- **字节跳动 2025 训练营 · 客户端方向结营证书**

**比赛与角色**

- **江苏大学生创新大赛 · 省二等奖** — 2026 年
- **字节 AI 全栈挑战赛 · 顺利完赛** — 2026 年
- **字节跳动高校合伙人** — 2026/09 – 2027/06：负责南京邮电大学方向的招聘宣发、字节校园活动的落地与宣传，以及和学校相关部门的沟通对接
- **技术型俱乐部校负责人**：组织技术分享活动，并完成商业赞助的洽谈与合作落地

<div class="about-note is-flipped">
  <div class="about-note-img">
    <img src="/images/about/innovation-contest.webp" alt="江苏大学生创新大赛省赛现场合影">
  </div>
  <div class="about-note-text">
    <p><strong>江苏大学生创新大赛</strong>（前身是大家更熟悉的「互联网+」）——2026 年我和队友组队参赛，拿了<strong>省二等奖</strong>。照片是省赛现场拍的。</p>
  </div>
</div>

**发明专利**

- 《一种台面式居家养老 AI 陪伴机器人》—— **共同申请人 · 已受理**（申请号 202611174942.0）
- 《一种台面养老型智能 AI 陪伴机器人》—— **共同申请人 · 已受理**（申请号 202611173717.5）

> 这两项是 2026 年 8 月提交的发明专利申请，目前处于**受理**阶段，尚未经过实质审查，也未授权。

---

## 🛠️ 我能做什么

**前端开发**
- 框架：React (Next.js), Vue 3/2, 微信小程序
- 语言：TypeScript, JavaScript (ES6+), HTML5, CSS3
- UI / 动画：TailwindCSS, Radix UI, Lottie, Live2D, ECharts

**移动端开发**
- 原生：Kotlin / Java, OpenGL ES
- 跨端：Flutter, Capacitor, 微信小程序 (Vant Weapp)

**后端与数据**
- 框架：SpringBoot, SpringMVC, MyBatis-Plus, FastAPI, Flask, Node.js
- 数据：MySQL, Redis, SQLite
- 爬虫：Python requests / BeautifulSoup

**AI 与多模态**
- 视觉：YOLO 目标检测、PP-OCRv6、Qwen3-VL
- 大模型：OpenAI GPT-4o / Whisper、智谱 GLM-4V、腾讯混元、火山引擎 Doubao VLM
- 工程：SSE 流式输出、Prompt 工程、结构化输出约束、RAG 与 Agent 工作流

---

## 🌿 生活里的我

上面几节全是工作，其实我的生活不只有这些。

<div class="about-note">
  <div class="about-note-img">
    <img src="/images/about/highschool-ballgame.webp" alt="高中篮球联赛夺冠后的班级队伍合影">
  </div>
  <div class="about-note-text">
    <p><strong>篮球</strong>是我打得最久的一件事。打得最痛快的一次不是大学的比赛，是<strong>高中那场联赛</strong>——我带着我们班一路打到全校男子组第一，最后发下来一个特别大的奖杯。这张照片就是那时候拍的。</p>
  </div>
</div>

<div class="about-note is-flipped">
  <div class="about-note-img">
    <img src="/images/about/basketball-team.webp" alt="大学体育馆里的院队合影">
  </div>
  <div class="about-note-text">
    <p>到了大学我进了<strong>院队</strong>，打<strong>小前锋</strong>，主要负责得分和内线的对抗。大一打得最多，大二开始变少，现在大三基本一个月一次。</p>
  </div>
</div>

<div class="about-note is-flipped">
  <div class="about-note-img">
    <img src="/images/about/gym-training.webp" alt="健身房里的训练记录">
  </div>
  <div class="about-note-text">
    <p><strong>健身</strong>差不多练了两年，不算系统训练，就是有空就去，但已经是我现在最频繁的体育活动了。主要练肩、胸、背、腿和腹肌。</p>
    <p>有个愿望：<strong>大四想上台打一次中国大学生自然组的健体比赛。</strong>我最崇拜的选手是何局，特别喜欢他的形体。当然不指望练成那样，只希望自己有清晰的肌肉线条，练得好看一点。</p>
  </div>
</div>

<div class="about-note">
  <div class="about-note-img">
    <img src="/images/about/travel-huangshan.webp" alt="黄山之行，在山间观景台远望">
  </div>
  <div class="about-note-text">
    <p>2024 年 7 月去的<strong>黄山</strong>，和我表哥一起。</p>
    <p>夏天爬山，山下热得不行，爬到山顶突然狂风大作还下起了雨，冷到发抖。上山的时候身体已经开始打颤，<strong>下山就真的发烧了。</strong>风景是真好，但这段记忆里最清楚的，其实是那场雨。</p>
  </div>
</div>

<div class="about-note is-flipped">
  <div class="about-note-img">
    <img src="/images/about/xuanwu-lake-night.webp" alt="玄武湖夜景，湖面上是远处城市的灯光">
  </div>
  <div class="about-note-text">
    <p>大学过得挺满的，但也会有压力大的时候。那种时候我一般会去<strong>玄武湖</strong>走一走，吹吹风。</p>
    <p>不用干什么，走两圈，看看水面，人就能缓过来。</p>
  </div>
</div>

<div class="about-note">
  <div class="about-note-img">
    <img src="/images/about/fuzimiao-night.webp" alt="夜里的夫子庙，河面上倒映着两岸的灯火">
  </div>
  <div class="about-note-text">
    <p>另一个常去的地方是<strong>夫子庙</strong>。</p>
    <p>和玄武湖不一样——那边是安静，这边是人声鼎沸。热闹的街市、河上的灯影，走一圈心情就会舒展开。散步、发呆、把情绪放一放，对我来说是挺重要的一件事。</p>
  </div>
</div>

<div class="about-note is-flipped">
  <div class="about-note-img">
    <img src="/images/about/street-view.webp" alt="夜晚路灯下被照亮的树叶">
  </div>
  <div class="about-note-text">
    <p>这张说不上具体是哪天拍的。每次去玄武湖或者夫子庙，我常常会随手拍两张，这张就是这么留下来的。</p>
    <p>我喜欢这种路灯把树叶照亮的画面，安静，但是有人气。</p>
  </div>
</div>

<div class="about-note">
  <div class="about-note-img">
    <img src="/images/about/cat-huihui.webp" alt="布偶猫灰灰从白色圆筒里探出头">
  </div>
  <div class="about-note-text">
    <p>我家还有一只猫，叫<strong>灰灰</strong>，布偶，今年一岁半。</p>
    <p>性格超级好——乖，不怎么咬人，也不拆家，就是安安静静地陪着我们。写代码写烦了抬头看一眼，挺治愈的。</p>
  </div>
</div>

<div class="about-note is-flipped">
  <div class="about-note-img">
    <img src="/images/about/highschool-graduation.webp" alt="高中毕业那天，同学们在操场上合影">
  </div>
  <div class="about-note-text">
    <p>最后放一张<strong>高中毕业</strong>的照片。</p>
    <p>高中那帮人当时玩得特别好，毕业之后就各奔东西了。大学过得热闹，但偶尔还是会想起那段日子——把它放在这里，算是留个念想。</p>
  </div>
</div>

---

## 📫 找我

- **GitHub**：[Ryan-wu-web](https://github.com/Ryan-wu-web)
- **个人网站**：[ryanwu.cn](https://ryanwu.cn)
- **Email**：3047967569@qq.com
- **坐标**：南京邮电大学仙林校区
