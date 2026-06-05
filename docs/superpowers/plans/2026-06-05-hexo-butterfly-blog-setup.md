# RyanWu 个人博客搭建 - 实现计划

> **给代理工作者：** 必需子skill：使用 executing-plans 逐个任务执行此计划。步骤使用复选框（- [ ]）语法跟踪。

**目标：** 从零搭建 Hexo + Butterfly 个人博客，配置深色/浅色双主题、Twikoo 评论、站内搜索、访问量统计，部署到 GitHub Pages 并绑定 ryanwu.cn。

**架构：** 使用 Hexo 7.x 作为静态生成器，Butterfly 4.x 作为主题，Twikoo 处理评论，Busuanzi 处理统计，GitHub Actions 自动部署到 gh-pages 分支。

**技术栈：** Node.js 20, Hexo 7.x, Butterfly 4.x, Twikoo, Busuanzi, GitHub Actions

---

## 文件结构

```
ryanwu_blog/
├── docs/superpowers/            # 已存在
├── source/
│   ├── _posts/                  # 文章目录（后续作者使用）
│   ├── about/                   # 关于我页面
│   │   └── index.md
│   └── projects/                # 项目展示页面
│       └── index.md
├── .github/
│   └── workflows/
│       └── pages.yml            # GitHub Actions 工作流
├── _config.yml                  # Hexo 主配置
├── _config.butterfly.yml        # Butterfly 主题配置
├── package.json                 # 项目依赖
├── .gitignore                   # Git 忽略文件
└── CNAME                        # 自定义域名
```

---

## 任务 1：初始化 Git 仓库并关联远程

**文件：**
- 创建：`.gitignore`
- 修改：无

- [ ] **步骤 1：初始化 Git 仓库**

在 `C:\Users\Lenovo\Desktop\ryanwu_blog` 目录下执行：

```bash
git init
git remote add origin https://github.com/Ryan-wu-web/ryanwu_blog.git
```

- [ ] **步骤 2：创建 .gitignore**

```gitignore
.DS_Store
Thumbs.db
db.json
*.log
node_modules/
public/
.deploy*/
```

- [ ] **步骤 3：提交初始文件**

```bash
git add docs/ .gitignore
git commit -m "chore: init repo with superpowers design docs"
git push -u origin main
```

预期：`main` 分支成功推送到远程仓库，包含 `docs/` 目录和 `.gitignore`。

---

## 任务 2：初始化 Hexo 项目

**文件：**
- 创建：`package.json`, `_config.yml`

- [ ] **步骤 1：初始化 package.json**

```bash
cd C:\Users\Lenovo\Desktop\ryanwu_blog
npm init -y
```

- [ ] **步骤 2：安装 Hexo 及相关依赖**

```bash
npm install hexo hexo-cli hexo-generator-archive hexo-generator-category hexo-generator-index hexo-generator-tag hexo-renderer-ejs hexo-renderer-stylus hexo-renderer-marked hexo-server hexo-generator-search hexo-deployer-git
```

- [ ] **步骤 3：初始化 Hexo 配置 _config.yml**

```yaml
# Hexo Configuration
title: Ryan's Blog
subtitle: '热爱技术，热爱生活'
description: 'Ryan 的个人博客，记录技术成长与生活点滴'
keywords: '技术博客, Ryan, Python, JavaScript, 生活随笔'
author: Ryan
language: zh-CN
timezone: Asia/Shanghai

# URL
url: https://ryanwu.cn
permalink: :year/:month/:day/:title/
permalink_defaults:
pretty_urls:
  trailing_index: true
  trailing_html: true

# Directory
source_dir: source
public_dir: public
tag_dir: tags
archive_dir: archives
category_dir: categories
code_dir: downloads/code
i18n_dir: :lang
skip_render:

# Writing
new_post_name: :title.md
default_layout: post
titlecase: false
external_link:
  enable: true
  field: site
  exclude: ''
filename_case: 0
render_drafts: false
post_asset_folder: false
relative_link: false
future: true
highlight:
  enable: false
prismjs:
  enable: false

# Home page setting
index_generator:
  path: ''
  per_page: 10
  order_by: -date

# Category & Tag
default_category: uncategorized
category_map:
tag_map:

# Metadata elements
meta_generator: true

# Date / Time format
date_format: YYYY-MM-DD
time_format: HH:mm:ss
updated_option: mtime

# Pagination
per_page: 10
pagination_dir: page

# Include / Exclude file(s)
include:
exclude:
ignore:

# Extensions
theme: butterfly

# Deployment
deploy:
  type: git
  repo: https://github.com/Ryan-wu-web/ryanwu_blog.git
  branch: gh-pages
```

- [ ] **步骤 4：提交 Hexo 初始化**

```bash
git add package.json package-lock.json _config.yml
git commit -m "chore: init hexo project"
```

---

## 任务 3：安装 Butterfly 主题

**文件：**
- 创建/修改：`package.json`（新增依赖）

- [ ] **步骤 1：安装 Butterfly 主题**

```bash
cd C:\Users\Lenovo\Desktop\ryanwu_blog
npm install hexo-theme-butterfly
```

- [ ] **步骤 2：复制主题默认配置**

```bash
cp node_modules/hexo-theme-butterfly/_config.yml _config.butterfly.yml
```

- [ ] **步骤 3：提交**

```bash
git add package.json package-lock.json _config.butterfly.yml
npm install  # 确保 lock 文件更新
```

---

## 任务 4：配置 Butterfly 主题 - 基础设置

**文件：**
- 修改：`_config.butterfly.yml`

- [ ] **步骤 1：配置基础信息**

在 `_config.butterfly.yml` 中修改以下字段：

```yaml
# Navigation
menu:
  首页: / || fas fa-home
  关于我: /about/ || fas fa-user
  项目: /projects/ || fas fa-briefcase
  技术笔记: /categories/tech/ || fas fa-code
  生活随笔: /categories/life/ || fas fa-coffee
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
```

- [ ] **步骤 2：配置主题色模式**

```yaml
# Theme color mode
theme_color:
  enable: true
  mode: dark
  mode_css:
    dark: # 深色模式变量
      --global-bg: '#0d1117'
      --font-color: '#f0f6fc'
      --hr-border: '#30363d'
      --hr-before-color: '#3b82f6'
      --search-bg: '#161b22'
      --search-input-color: '#f0f6fc'
      --search-a-color: '#f0f6fc'
      --preloader-bg: '#0d1117'
      --preloader-color: '#3b82f6'
      --tab-botton-bg: '#161b22'
      --tab-botton-color: '#f0f6fc'
      --tab-button-hover-bg: '#3b82f6'
      --tab-button-hover-color: '#f0f6fc'
      --card-bg: '#21262d'
      --sidebar-bg: '#161b22'
      --btn-hover-color: '#3b82f6'
      --btn-color: '#f0f6fc'
      --btn-bg: '#3b82f6'
      --text-bg-hover: '#3b82f6'
      --light-grey: '#8b949e'
      --dark-grey: '#f0f6fc'
      --white: '#f0f6fc'
      --text-highlight-color: '#f0f6fc'
      --blockquote-color: '#8b949e'
      --blockquote-bg: '#161b22'
      --reward-pop: '#21262d'
      --toc-link-color: '#f0f6fc'
      --hl-color: '#f0f6fc'
      --hl-bg: '#161b22'
      --hltools-bg: '#21262d'
      --hltools-color: '#f0f6fc'
      --hlnumber-bg: '#161b22'
      --hlnumber-color: '#8b949e'
      --hlscrollbar-bg: '#30363d'
      --hlexpand-bg: '#21262d'
    light: # 浅色模式变量
      --global-bg: '#ffffff'
      --font-color: '#1f2937'
      --hr-border: '#e5e7eb'
      --hr-before-color: '#60a5fa'
      --search-bg: '#f6f8fa'
      --search-input-color: '#1f2937'
      --search-a-color: '#1f2937'
      --preloader-bg: '#ffffff'
      --preloader-color: '#60a5fa'
      --tab-botton-bg: '#f6f8fa'
      --tab-botton-color: '#1f2937'
      --tab-button-hover-bg: '#60a5fa'
      --tab-button-hover-color: '#ffffff'
      --card-bg: '#f9fafb'
      --sidebar-bg: '#f6f8fa'
      --btn-hover-color: '#60a5fa'
      --btn-color: '#1f2937'
      --btn-bg: '#60a5fa'
      --text-bg-hover: '#60a5fa'
      --light-grey: '#6b7280'
      --dark-grey: '#1f2937'
      --white: '#ffffff'
      --text-highlight-color: '#1f2937'
      --blockquote-color: '#6b7280'
      --blockquote-bg: '#f6f8fa'
      --reward-pop: '#f9fafb'
      --toc-link-color: '#1f2937'
      --hl-color: '#1f2937'
      --hl-bg: '#f6f8fa'
      --hltools-bg: '#f9fafb'
      --hltools-color: '#1f2937'
      --hlnumber-bg: '#f6f8fa'
      --hlnumber-color: '#6b7280'
      --hlscrollbar-bg: '#e5e7eb'
      --hlexpand-bg: '#f9fafb'
```

- [ ] **步骤 3：配置首页打字机效果**

```yaml
subtitle:
  enable: true
  # Typewriter Effect
  effect: true
  # Custom Effect
  startDelay: 300
  typeSpeed: 100
  backSpeed: 50
  # loop
  loop: true
  # source: false 关闭默认的subtitle获取
  source: false
  # 自定义打字机文字
  sub:
    - Hello, I'm Ryan
    - 热爱技术，热爱生活
    - Coding & Living
    - Keep Learning, Keep Growing
```

- [ ] **步骤 4：配置首页背景**

```yaml
# Background image
cover:
  enable: true
  # Images URL
  index_img: # 可配置一张首页背景图URL，如 https://xxx.com/bg.jpg
    - # 留空则使用纯色/渐变
  # full_screen: true  # 是否全屏
  full_screen: true
```

- [ ] **步骤 5：提交**

```bash
git add _config.butterfly.yml
git commit -m "config: setup butterfly base config with dark/light theme"
```

---

## 任务 5：配置 Butterfly 主题 - 功能模块

**文件：**
- 修改：`_config.butterfly.yml`

- [ ] **步骤 1：配置 Twikoo 评论**

```yaml
comments:
  use: Twikoo
  text: true
  lazyload: false
  count: false
  card_post_count: false

# Twikoo
# https://github.com/imaegoo/twikoo
twikoo:
  envId: # 后续部署 Twikoo 后填写，如 https://xxx.vercel.app
  region: ap-shanghai
  path: window.location.pathname
  visitor: false
  option:
```

- [ ] **步骤 2：配置搜索**

```yaml
# Local Search
local_search:
  enable: true
  preload: false
  CDN:
```

- [ ] **步骤 3：配置访问量统计（Busuanzi）**

```yaml
# busuanzi count for PV and UV
busuanzi:
  enable: true
  site_uv: true
  site_pv: true
  page_pv: true
```

- [ ] **步骤 4：配置代码高亮**

```yaml
highlight_theme: dark # 深色模式代码主题
highlight_copy: true
highlight_lang: true
highlight_shrink: false
highlight_height_limit: false
```

- [ ] **步骤 5：配置文章目录 TOC**

```yaml
toc:
  enable: true
  number: true
  expand_all: false
  init_open: true
```

- [ ] **步骤 6：配置社交链接**

```yaml
social:
  fab fa-github: https://github.com/Ryan-wu-web || Github
  fas fa-envelope: mailto:your-email@example.com || Email
```

- [ ] **步骤 7：提交**

```bash
git add _config.butterfly.yml
git commit -m "config: enable twikoo, search, busuanzi, code highlight, toc"
```

---

## 任务 6：创建独立页面

**文件：**
- 创建：`source/about/index.md`
- 创建：`source/projects/index.md`

- [ ] **步骤 1：创建关于我页面**

```markdown
---
title: 关于我
date: 2026-06-05 12:00:00
aside: true
top_img: false
---

## 👋 Hello, I'm Ryan

欢迎来到我的个人博客！

### 关于我

我是一名热爱技术的开发者，喜欢探索新技术，记录学习过程中的点滴收获。

### 技能栈

- Python
- JavaScript / Vue / React
- Machine Learning / Deep Learning
- Linux / Git / Docker

### 联系方式

- GitHub: [Ryan-wu-web](https://github.com/Ryan-wu-web)
- Email: your-email@example.com

---

> 📝 **注意：** 这个页面后续你可以自己补充更多内容，比如实习经历、比赛经历、时间线等。
```

- [ ] **步骤 2：创建项目展示页面**

```markdown
---
title: 项目
aside: false
top_img: false
---

## 💼 我的项目

以下是我参与或独立完成的一些项目：

### 示例项目

这里将展示你的项目作品集。每个项目可以包含：

- 项目名称和简介
- 技术栈标签
- 项目截图或封面图
- GitHub 链接 / 在线演示链接

> 📝 **提示：** 你可以在 Hexo 的 Front Matter 中配置项目数据，或者后续直接编辑这个页面添加项目卡片。

---

*更多项目即将上线，敬请期待！*
```

- [ ] **步骤 3：提交**

```bash
git add source/
git commit -m "feat: add about and projects pages"
```

---

## 任务 7：创建示例文章

**文件：**
- 创建：`source/_posts/hello-world.md`
- 创建：`source/_posts/my-first-tech-note.md`
- 创建：`source/_posts/my-first-life-post.md`

- [ ] **步骤 1：创建欢迎文章**

```markdown
---
title: Hello World
subtitle: 欢迎来到 Ryan 的博客
date: 2026-06-05 12:00:00
tags: [随笔]
categories: 生活
---

欢迎来到我的个人博客！

这里是我记录技术学习和生活点滴的地方。

### 博客规划

- **技术笔记**：分享编程、算法、AI 等方面的学习心得
- **项目展示**：展示我参与或独立完成的项目
- **生活随笔**：记录旅行、运动等生活趣事

希望这个博客能帮助到有需要的人，也欢迎交流讨论！
```

- [ ] **步骤 2：创建技术笔记示例**

```markdown
---
title: 我的第一篇技术笔记
date: 2026-06-05 12:00:00
tags: [Python, 入门]
categories: 技术
---

这是一篇技术笔记的示例文章。

### 代码示例

```python
def hello_world():
    print("Hello, World!")
    return "success"

hello_world()
```

### 后续计划

后续我会在这里分享更多技术文章，包括但不限于：

- Python 编程技巧
- 前端开发经验
- 机器学习项目实践
- 算法题解
```

- [ ] **步骤 3：创建生活随笔示例**

```markdown
---
title: 开始记录生活
date: 2026-06-05 12:00:00
tags: [日常]
categories: 生活
---

今天开始在这个博客记录生活！

### 为什么记录生活？

生活不只是代码和算法，还有：

- 🏃 运动健身
- ✈️ 旅行探索
- 📷 摄影记录
- 📚 阅读思考

希望这里能成为我回忆的宝库。
```

- [ ] **步骤 4：提交**

```bash
git add source/_posts/
git commit -m "feat: add sample posts"
```

---

## 任务 8：配置 GitHub Actions 自动部署

**文件：**
- 创建：`.github/workflows/pages.yml`
- 创建：`CNAME`

- [ ] **步骤 1：创建工作流文件**

```yaml
name: Pages

on:
  push:
    branches:
      - main  # default branch

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Cache NPM dependencies
        uses: actions/cache@v4
        with:
          path: node_modules
          key: ${{ runner.os }}-npm-cache
          restore-keys: |
            ${{ runner.os }}-npm-cache

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        if: github.ref == 'refs/heads/main'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

- [ ] **步骤 2：创建 CNAME 文件**

```
ryanwu.cn
```

- [ ] **步骤 3：提交**

```bash
git add .github/workflows/pages.yml CNAME
git commit -m "ci: add GitHub Actions for auto deploy"
```

---

## 任务 9：本地构建测试

**文件：**
- 无新增/修改

- [ ] **步骤 1：安装依赖并构建**

```bash
cd C:\Users\Lenovo\Desktop\ryanwu_blog
npm install
npm run build
```

预期：构建成功，`public/` 目录生成，无报错。

- [ ] **步骤 2：本地预览（可选）**

```bash
npm run server
```

预期：控制台显示 `Hexo is running at http://localhost:4000`。

- [ ] **步骤 3：检查构建产物**

确认 `public/` 目录包含：
- `index.html`（首页）
- `about/` 目录
- `projects/` 目录
- `archives/` 目录
- `tags/` 目录
- `categories/` 目录

---

## 任务 10：首次推送并启用部署

**文件：**
- 无新增/修改

- [ ] **步骤 1：推送所有代码到 main 分支**

```bash
git push origin main
```

- [ ] **步骤 2：验证 GitHub Actions 运行**

登录 GitHub 仓库页面，确认 Actions 工作流正常运行并成功部署到 `gh-pages` 分支。

- [ ] **步骤 3：配置 GitHub Pages**

在仓库 Settings > Pages 中：
- Source 选择 "Deploy from a branch"
- Branch 选择 `gh-pages`
- Custom domain 填写 `ryanwu.cn`
- 勾选 "Enforce HTTPS"

- [ ] **步骤 4：配置阿里云 DNS**

登录阿里云域名控制台，为 `ryanwu.cn` 添加解析记录：

| 主机记录 | 记录类型 | 解析线路 | 记录值 | TTL |
|---------|---------|---------|--------|-----|
| @ | CNAME | 默认 | ryan-wu-web.github.io | 10分钟 |
| www | CNAME | 默认 | ryan-wu-web.github.io | 10分钟 |

- [ ] **步骤 5：等待 DNS 生效**

通常 5-30 分钟内生效。访问 `https://ryanwu.cn` 验证网站是否正常显示。

---

## 任务 11：Twikoo 评论系统部署（可选后续）

**注意：** Twikoo 需要单独部署后端，此任务可在博客主体上线后执行。

**文件：**
- 修改：`_config.butterfly.yml`（填写 envId）

- [ ] **步骤 1：部署 Twikoo 到 Vercel**

参考 Twikoo 官方文档：https://twikoo.js.org/quick-start.html

1. 点击 Vercel 一键部署按钮
2. 绑定 MongoDB Atlas 免费数据库
3. 获取部署后的 URL（如 `https://twikoo-xxx.vercel.app`）

- [ ] **步骤 2：配置 Butterfly**

在 `_config.butterfly.yml` 中填入：

```yaml
twikoo:
  envId: https://your-twikoo-url.vercel.app
  region: ap-shanghai
```

- [ ] **步骤 3：提交并重新部署**

```bash
git add _config.butterfly.yml
git commit -m "config: add twikoo comment system"
git push origin main
```

---

## 自检

- [ ] **规格覆盖：** 所有设计文档中的需求（配色、导航、功能、部署）均已在任务中体现
- [ ] **占位符扫描：** 无 TBD、TODO；所有配置值已明确或标注后续补充
- [ ] **类型一致性：** 所有文件路径、命令、配置字段名称前后一致
