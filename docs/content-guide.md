# Ryan's Blog 内容维护指南

> 适用于当前的 Hexo 8.1.2 + Butterfly 5.7.0。最后更新：2026-09-16。

## 1. 推荐写作链路

```text
创建文章 → 放入文章媒体 → 内容检查 → 本地预览 → 发布前检查 → 合并到 main → 发布
```

常用命令：

```powershell
npm run post:new
npm run content:check
npm run preview
npm run prepublish:check
```

`npm run preview` 会持续运行本地服务器，访问 `http://localhost:4000`，结束时按 `Ctrl+C`。

### 1.1 写作定位与声音

开始写作前，以项目根目录的两份文件为长期标准：

- [`BRAND.md`](../BRAND.md)：定义“Ryanwu 的 AI / 技术 / 生活博客”定位、内容边界和读者价值；
- [`VOICE.md`](../VOICE.md)：定义真诚、克制、具体、有判断的默认写作声音。

AI 协作时，先判定文章类型：AI、技术分析、行业观察这类需要完整论证的走深度文章流程——**动笔前先把外部引用逐条核实到一手来源**，再搭结构、写正文、配图表与封面；普通生活日志采用轻量整理，不强制套用 SEO、统计、图表或 FAQ。

内容能力与仓库工具分工如下：

```text
原始素材
  → 判断写作模式、核实外部引用
  → 深度写作或轻量整理生成草稿
  → post:new 创建 Hexo 文件和媒体目录
  → content:check / preview / prepublish:check
  → 人工确认后发布
```

博客现有检查命令是最终交付门禁；外部写作 Skill 中当前环境不存在的脚本或代理，不作为发布成功的依据。

### 1.2 三种写作模板

| 写作模式 | 适合内容 | 模板 |
| --- | --- | --- |
| 深度文章 | AI、技术分析、行业观察 | [`templates/deep-article.md`](./templates/deep-article.md) |
| 工作与项目复盘 | 技术项目、AI 产品、销售、管理、职业复盘 | [`templates/work-retrospective.md`](./templates/work-retrospective.md) |
| 生活日志 | 日常、旅行、阅读、求职、情绪和阶段记录 | [`templates/life-journal.md`](./templates/life-journal.md) |

模板是写作骨架，不是必须填满的表格。先运行 `npm run post:new`，再用所选模板替换新文章中的默认正文。

当前仍使用两个 Hexo 分类：

- `tech`：AI、开发、产品、工程和技术项目；
- `life`：生活、职业、销售、管理和个人随笔。

使用 `ai`、`product`、`sales`、`management`、`career`、`journal` 等标签表达细分主题。AI 内容积累到足够规模后，再评估是否增加独立分类。

## 2. 创建文章

运行：

```powershell
npm run post:new
```

工具会要求填写：

- `title`：文章标题；
- `date`：`YYYY-MM-DD`；
- `tags`：至少一个，小写字母、数字、中文或连字符；
- `categories`：只能是 `tech` 或 `life`；
- `description`：用于列表摘要和搜索描述，不能为空；
- `cover`：文章封面，默认指向该文章的媒体目录。

它会同时创建：

```text
source/_posts/YYYY-MM-DD-文章-slug.md
source/images/posts/文章-slug/
```

已有文章不会被覆盖。

也可使用参数创建，适合重复操作：

```powershell
python tools/new-post.py `
  --title "AI 产品复盘" `
  --category tech `
  --date 2026-09-14 `
  --tags "ai,product-management" `
  --description "一次 AI 产品从想法到验证的完整复盘" `
  --slug "ai-product-retrospective"
```

## 3. Front Matter 规范

新文章必须包含以下字段：

```yaml
---
title: "AI 产品复盘"
date: 2026-09-14 12:00:00
tags: [ai, product-management]
categories: tech
description: "一句完整、具体的文章摘要"
cover: "/images/posts/ai-product-retrospective/cover.jpg"
---
```

| 字段 | 规则 |
| --- | --- |
| `title` | 非空，表达文章主题 |
| `date` | `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS` |
| `tags` | 至少一个；统一小写，可用数字、中文和连字符 |
| `categories` | 只能是 `tech` 或 `life` |
| `description` | 新文章必填，不直接复制标题 |
| `cover` | 新文章必填；本地路径必须真实存在，也可使用完整的远程 URL |

历史文章暂未补齐 `description` 或 `cover` 时，普通检查只给出警告；Git 新增文章在发布前会自动启用严格检查。不要为了消除警告给旧文章机械复用同一张大图。

## 4. 图片、视频和音频

每篇文章使用独立目录：

```text
source/images/posts/<post-slug>/
├── cover.jpg
├── architecture.webp
├── demo.mp4
└── narration.mp3
```

正文引用：

```markdown
![架构图中的数据流向](/images/posts/<post-slug>/architecture.webp)

<video controls preload="metadata" src="/images/posts/<post-slug>/demo.mp4"></video>

<audio controls preload="metadata" src="/images/posts/<post-slug>/narration.mp3"></audio>
```

规则：

1. 图片必须写有意义的 alt 文本，不使用 `![图片]` 这类无信息描述；
2. 文件名使用小写字母、数字和连字符；
3. 图片优先使用 WebP/JPEG，控制尺寸和体积；
4. 大视频优先放稳定的视频平台或对象存储，避免 Git 仓库快速膨胀；
5. 本地媒体路径必须位于 `source/` 内，内容检查器会验证文件是否存在。

## 5. 检查与预览

检查全部文章：

```powershell
npm run content:check
```

严格检查某一篇文章：

```powershell
python tools/check-content.py --strict source/_posts/2026-09-14-ai-product-retrospective.md
```

检查器会验证：

- Front Matter 是否完整；
- 日期、分类和标签是否合法；
- 封面、Markdown 图片及 HTML 音视频文件是否存在；
- 图片是否有 alt 文本；
- 媒体引用是否越过 `source/` 目录。

预览：

```powershell
npm run preview
```

重点查看首页卡片、文章封面、文章正文、目录、归档、搜索和移动端布局。

## 6. 安全发布

先执行无副作用的发布前检查：

```powershell
npm run prepublish:check
```

该命令只会：

1. 对 Git 新增文章启用严格内容检查；
2. 执行 `hexo clean`；
3. 执行生产构建；
4. 显示当前分支和改动。

它不会暂存、提交或推送。

还可以运行：

```powershell
python tools/publish.py --dry-run
```

正式发布命令：

```powershell
python tools/publish.py
```

安全边界：

- 非 `main` 分支会被阻止发布；
- 默认确认选项为 `N`；
- 不使用 `shell=True`；
- 已跟踪文件照常暂存；新文件只从博客内容、配置、工具与主题目录加入，避免误收本地临时文件；
- 只有明确确认后才会执行 commit 和 `git push origin main`。

推荐做法仍然是：在功能分支完成检查和审查，合并到 `main` 后再发布。

## 7. 页面与项目维护

- 关于页面：直接编辑 `source/about/index.md`；
- 项目页面：直接编辑 `source/projects/index.md`，或使用：

```powershell
python tools/new-project.py
python tools/edit-project.py
```

主题优先通过 `_config.butterfly.yml` 配置，不直接修改 `themes/butterfly/` 的官方源码，避免后续升级冲突。

## 8. Markdown 速查

````markdown
## 二级标题

**加粗**、*斜体*、`行内代码`

- 无序列表
1. 有序列表

```python
print("hello")
```

[链接文字](https://example.com)
![准确描述](/images/posts/<post-slug>/image.webp)

> 引用文字
````

## 9. 提交信息建议

| 类型 | 用途 | 示例 |
| --- | --- | --- |
| `post:` | 新文章 | `post: add AI 产品复盘` |
| `update:` | 页面或文章更新 | `update: about page` |
| `fix:` | 内容或功能修复 | `fix: correct broken media path` |
| `style:` | 视觉调整 | `style: refine dark copper palette` |
| `tools:` | 写作工具更新 | `tools: validate post media` |
