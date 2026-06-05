# RyanWu 个人博客 - 设计规格文档

> **日期：** 2026-06-05  
> **主题：** Hexo + Butterfly 个人博客搭建  
> **状态：** 待实现计划

---

## 1. 项目概述

使用 Hexo 静态博客框架 + Butterfly 主题，搭建 Ryan 的个人博客网站。部署在 GitHub Pages，绑定自定义域名 `ryanwu.cn`。

### 1.1 博客定位
- **主要内容：** 技术博客（项目展示、实习/比赛/训练营经历、技术学习笔记）
- **辅助内容：** 生活随笔（旅游、运动等日常记录）
- **目标读者：** 中文技术社区
- **内容策略：** 从零开始撰写，网站成型后由作者自行补充内容

### 1.2 参考站点
- Butterfly 官方 Demo：[crazywong.com](https://crazywong.com)
- 参考其首页打字机效果、导航结构、文章卡片布局

---

## 2. 架构概览

```
ryanwu_blog/
├── docs/                          # 开发文档（Superpowers 流程文档）
│   └── superpowers/
│       ├── specs/                 # 设计规格（本文档）
│       └── plans/                 # 实现计划
├── source/                        # 博客内容源文件
│   ├── _posts/                    # 文章（Markdown 格式）
│   ├── about/                     # 关于我页面（独立页面）
│   ├── projects/                  # 项目展示页面（独立页面）
│   └── images/                    # 博客图片资源
├── themes/butterfly/              # Butterfly 主题（npm 安装）
├── _config.yml                    # Hexo 主配置文件
├── _config.butterfly.yml          # Butterfly 主题配置文件
├── package.json                   # Node.js 依赖
├── .github/
│   └── workflows/
│       └── pages.yml              # GitHub Actions 自动部署工作流
└── CNAME                          # 自定义域名配置（ryanwu.cn）
```

### 2.1 技术栈

| 层级 | 技术 | 版本/说明 |
|------|------|-----------|
| 静态生成器 | Hexo | ^7.x |
| 主题 | hexo-theme-butterfly | ^4.x |
| 评论系统 | Twikoo | 通过 CDN 引入 |
| 搜索 | hexo-generator-search | 本地搜索 |
| 部署 | GitHub Actions | 自动推送到 gh-pages 分支 |
| 托管 | GitHub Pages | 绑定 ryanwu.cn |
| 包管理器 | npm | Node.js 配套 |

---

## 3. 配色方案

采用手动切换的深浅双主题模式。

### 3.1 深色模式（默认）

| 用途 | 色值 | 说明 |
|------|------|------|
| 页面背景 | `#0d1117` | GitHub Dark 风格，深邃不刺眼 |
| 主色调 | `#3b82f6` | 亮蓝色，用于链接、按钮、高亮 |
| 文字主色 | `#f0f6fc` | 纯白偏冷，阅读舒适 |
| 文字次要 | `#8b949e` | 灰色，用于元信息、描述 |
| 代码块背景 | `#161b22` | 略浅于页面背景 |
| 边框/分割线 | `#30363d` | 低调分割线 |
| 卡片背景 | `#21262d` | 悬浮卡片底色 |

### 3.2 浅色模式

| 用途 | 色值 | 说明 |
|------|------|------|
| 页面背景 | `#ffffff` | 纯白 |
| 主色调 | `#60a5fa` | 浅蓝色，柔和不刺眼 |
| 文字主色 | `#1f2937` | 深灰色，接近纯黑 |
| 文字次要 | `#6b7280` | 中灰色 |
| 代码块背景 | `#f6f8fa` | GitHub 浅灰 |
| 边框/分割线 | `#e5e7eb` | 浅灰边框 |
| 卡片背景 | `#f9fafb` | 微灰卡片底色 |

### 3.3 主题切换配置

- Butterfly 配置 `theme_color.mode: [dark, light]` 启用双主题
- 默认深色模式（`dark` 在前）
- 切换按钮位于导航栏右侧
- 切换状态保存在 `localStorage`

---

## 4. 页面结构

### 4.1 导航菜单

| 显示名称 | 路径 | 图标 | 类型 |
|----------|------|------|------|
| 首页 | `/` | fas fa-home | 自动 |
| 关于我 | `/about/` | fas fa-user | 独立页面 |
| 项目 | `/projects/` | fas fa-briefcase | 独立页面 |
| 技术笔记 | `/categories/tech/` | fas fa-code | 分类页面 |
| 生活随笔 | `/categories/life/` | fas fa-coffee | 分类页面 |
| 归档 | `/archives/` | fas fa-archive | 自动 |
| 标签 | `/tags/` | fas fa-tags | 自动 |

### 4.2 首页（/）

- **顶部全屏区：**
  - 背景图（可配置一张高质量图片或纯色渐变）
  - 打字机效果标题（如 "Hello, I'm Ryan" / "热爱技术，热爱生活"）
  - 向下滚动箭头动画
- **文章列表区：**
  - 最新文章卡片（技术 + 生活混合展示）
  - 每篇文章显示：封面图、标题、摘要、日期、分类、标签
  - 分页或"加载更多"

### 4.3 关于我（/about/）

- 个人头像（圆形）
- 简介文字
- 技能标签（如 Python、Vue、Machine Learning 等）
- 联系方式（GitHub、Email）
- 个人经历时间线（可选，后续作者自行补充）

### 4.4 项目（/projects/）

- 项目卡片网格布局（2-3 列响应式）
- 每个项目卡片包含：
  - 项目封面图
  - 项目名称
  - 技术标签
  - 一句话简介
  - GitHub 链接 / 在线演示链接
- 项目数据通过 Front Matter 配置，便于作者后续自行添加

### 4.5 技术笔记 & 生活随笔

- 两者均为文章列表页，通过 `categories` 区分
- 统一的文章卡片样式
- 支持标签筛选
- 生活随笔文章通常较短，但样式上与技本笔记一致（方案 1）

### 4.6 归档（/archives/）

- Butterfly 内置归档页面
- 按年份/月份分组列出所有文章

### 4.7 标签（/tags/）

- Butterfly 内置标签云页面
- 标签大小根据文章数量动态调整

---

## 5. 功能模块详细设计

### 5.1 评论系统 - Twikoo

| 配置项 | 值 |
|--------|-----|
| 提供商 | Twikoo |
| 部署方式 | 使用 Vercel 免费版部署 Twikoo 后端（MongoDB Atlas 免费版做数据库）|
| 前端引入 | Butterfly 内置 Twikoo 支持，仅需配置 `envId` |
| 显示位置 | 每篇文章底部 |
| 功能 | Markdown 支持、邮件通知、表情包、博主标识 |

### 5.2 站内搜索

| 配置项 | 值 |
|--------|-----|
| 方案 | hexo-generator-search 生成 JSON 搜索索引 |
| 触发方式 | 导航栏搜索图标点击 |
| 搜索范围 | 文章标题、内容、标签、分类 |

### 5.3 访问量统计

| 配置项 | 值 |
|--------|-----|
| 方案 | Busuanzi（不蒜子）|
| 显示位置 | 页脚（站点总访问量）+ 文章页（单篇文章阅读量）|
| 成本 | 免费 |

### 5.4 打字机效果

| 配置项 | 值 |
|--------|-----|
| 方案 | Butterfly 内置 subtitle.typed |
| 文案示例 | "Hello, I'm Ryan", "热爱技术，热爱生活", "Coding & Living" |
| 打字速度 | 中等（100ms/字符）|
| 循环 | 是，循环播放多条文案 |

### 5.5 代码高亮

| 配置项 | 值 |
|--------|-----|
| 方案 | Butterfly 内置 highlight |
| 主题 | 深色：atom-one-dark，浅色：atom-one-light |
| 功能 | 行号显示、代码复制按钮、代码折叠 |
| 语言支持 | 全语言（通过 highlight.js）|

### 5.6 动态背景

**决策：不使用动态背景**

- 用户明确要求"简洁无背景"
- 首页使用静态背景图或纯色渐变即可
- 不启用 canvas_fluttering_ribbon、canvas_nest 等任何动态效果

---

## 6. 文章分类与标签策略

### 6.1 Categories（大类）

| 分类名 | 用途 |
|--------|------|
| 技术 | 所有技术相关文章 |
| 生活 | 所有生活随笔 |

### 6.2 Tags（细分标签）

预设标签供作者参考（后续可自由扩展）：

**技术类：** Python、JavaScript、Vue、React、Machine Learning、Deep Learning、Algorithm、Linux、Git、Docker、Project、Internship、Competition、Bootcamp

**生活类：** Travel、Sports、Photography、Reading、Daily

---

## 7. 部署架构

### 7.1 GitHub Actions 工作流

```yaml
name: Pages
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### 7.2 自定义域名配置

- 文件：`CNAME`，内容为 `ryanwu.cn`
- GitHub Pages 设置中绑定自定义域名
- 阿里云域名解析配置：
  - 记录类型：CNAME
  - 主机记录：@
  - 记录值：`<username>.github.io`
  - 同时配置 www 子域名（可选）

### 7.3 HTTPS

- GitHub Pages 自动提供 HTTPS 证书
- 阿里云域名无需额外 SSL 配置

---

## 8. 开发环境

| 工具 | 版本要求 |
|------|---------|
| Node.js | >= 18.x（推荐 20.x LTS）|
| npm | >= 9.x |
| Git | 任意最新版 |

### 8.1 本地开发命令

```bash
# 安装依赖
npm install

# 本地预览
npm run server    # 或 hexo server

# 生成静态文件
npm run build     # 或 hexo generate

# 清理缓存
npm run clean     # 或 hexo clean
```

---

## 9. 错误处理策略

| 场景 | 处理方式 |
|------|---------|
| Hexo 构建失败 | 检查 `_config.yml` 语法（YAML 缩进敏感），查看错误日志定位问题 |
| Butterfly 主题配置错误 | 对照官方文档检查 `_config.butterfly.yml` 字段名和层级 |
| GitHub Actions 部署失败 | 检查工作流 YAML 语法、Node 版本、npm install 是否成功 |
| 自定义域名不生效 | 检查 CNAME 文件、GitHub Pages 设置、阿里云 DNS 解析（通常需 5-30 分钟生效）|
| Twikoo 评论不显示 | 检查 envId 配置、Vercel 服务状态、浏览器控制台报错 |
| 搜索功能异常 | 确认 hexo-generator-search 已安装并生成 search.xml |

---

## 10. 测试策略

| 测试项 | 方法 |
|--------|------|
| 本地构建 | `hexo generate` 无报错，`public/` 目录生成完整 |
| 本地预览 | `hexo server` 启动后，浏览器访问 `http://localhost:4000` 检查各页面 |
| 响应式测试 | 浏览器 DevTools 切换手机/平板/桌面尺寸检查布局 |
| 主题切换 | 手动点击切换按钮，确认深色/浅色模式正确切换且无闪烁 |
| 评论功能 | 部署后访问文章页，测试 Twikoo 评论框加载和提交 |
| 搜索功能 | 输入关键词测试搜索结果准确性和跳转 |
| 部署验证 | GitHub Actions 绿钩后，访问 `ryanwu.cn` 确认线上版本 |

---

## 11. 后续扩展计划（V2）

以下功能不在初始版本中实现，但架构预留扩展空间：

- **生活随笔特殊样式：** 方案 2 的"朋友圈/动态"式展示
- **项目页面增强：** 添加项目详情页、项目时间线
- **国际化：** 中英双语支持
- **PWA：** 离线访问支持
- **RSS 订阅：** 如后续需要可启用
- **友情链接：** 如后续需要可添加

---

## 12. 决策记录（ADR）

| 决策 | 选项 | 选择 | 理由 |
|------|------|------|------|
| 评论系统 | Twikoo / Gitalk / Valine | **Twikoo** | 国内访问快，支持 Markdown，作者倾向 |
| 生活随笔展示 | 方案 1（统一）/ 方案 2（特殊样式）| **方案 1** | 简单快速上线，V2 可迭代 |
| 动态背景 | 启用 / 禁用 | **禁用** | 作者要求简洁无背景 |
| 部署平台 | GitHub Pages / Vercel / 自有服务器 | **GitHub Pages** | 免费、稳定、与 Git 工作流天然整合 |
| 默认主题 | 深色 / 浅色 | **深色** | 技术博客常见默认，护眼 |

---

## 13. 规格自检

- [x] **占位符扫描：** 无 TBD、TODO、待补充内容
- [x] **内部一致性：** 配色方案与功能配置一致，所有决策在 ADR 中有记录
- [x] **范围检查：** 聚焦初始版本，扩展计划明确标注为 V2
- [x] **歧义检查：** 所有配置项均有具体值，颜色有 Hex 色值

---

> **下一步：** 通过用户审查后，调用 `writing-plans` skill 编写实现计划。
