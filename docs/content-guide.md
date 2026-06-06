# Ryan's Blog - 博客内容维护规范

> 本文档是 Ryan 个人博客的完整维护指南，涵盖内容发布、页面更新、图片管理、工具使用等全部操作。
>
> **最后更新：** 2026-06-06

---

## 目录

1. [项目结构](#一项目结构)
2. [文章发布规范](#二文章发布规范)
3. [图片上传指南](#三图片上传指南)
4. [项目页面管理](#四项目页面管理)
5. [关于我页面更新](#五关于我页面更新)
6. [工具使用指南](#六工具使用指南)
7. [发布流程](#七发布流程)
8. [Markdown 速查](#八markdown-速查)

---

## 一、项目结构

```
ryanwu_blog/
├── docs/
│   └── content-guide.md          # 本规范文档
├── source/
│   ├── _posts/                   # 文章目录（技术笔记 + 生活随笔）
│   │   ├── 2026-06-06-文章标题.md
│   │   └── ...
│   ├── about/
│   │   └── index.md              # 关于我页面
│   ├── projects/
│   │   └── index.md              # 项目展示页面
│   ├── categories/
│   │   └── index.md              # 分类汇总页（自动生成，勿动）
│   ├── tags/
│   │   └── index.md              # 标签汇总页（自动生成，勿动）
│   ├── images/
│   │   ├── posts/                # 文章配图
│   │   └── projects/             # 项目封面图
│   └── js/
│       └── page-typed.js         # 页面打字机效果（勿动）
├── tools/                        # 内容创建工具
│   ├── new-post.py               # 创建新文章
│   ├── new-project.py            # 添加新项目
│   ├── edit-project.py           # 修改/删除项目
│   └── publish.py                # 一键发布
├── _config.yml                   # Hexo 主配置（勿动）
├── _config.butterfly.yml         # 主题配置（勿动）
└── package.json                  # 依赖（勿动）
```

---

## 二、文章发布规范

### 2.1 文件命名

```
YYYY-MM-DD-文章标题.md
```

示例：
- `2026-06-06-python爬虫入门.md`
- `2026-06-10-杭州西湖游记.md`

### 2.2 Front-matter 模板

**技术笔记：**

```markdown
---
title: 文章标题
date: 2026-06-06 14:30:00
tags: [python, 爬虫, tutorial]
categories: tech
description: 文章摘要，用于SEO和列表展示
cover: /images/posts/封面图.jpg
---

## 引言

简述背景...

## 正文

主要内容...

## 总结

总结要点...
```

**生活随笔：**

```markdown
---
title: 文章标题
date: 2026-06-06 14:30:00
tags: [travel, daily]
categories: life
description: 文章摘要
cover: /images/posts/封面图.jpg
---

正文...
```

### 2.3 Front-matter 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 文章标题 |
| `date` | 是 | 发布日期时间 |
| `categories` | 是 | `tech`（技术笔记）或 `life`（生活随笔） |
| `tags` | 是 | 英文标签，多个用逗号分隔 |
| `description` | 否 | 文章摘要，SEO用 |
| `cover` | 否 | 封面图路径 |

### 2.4 标签命名规范

| 类别 | 推荐标签 |
|------|---------|
| 技术 | python, javascript, vue, react, ml, algorithm, linux, git, docker, database |
| 项目 | project, internship, competition, bootcamp |
| 生活 | travel, sports, photography, reading, daily, food, movie |

> **规则：标签统一使用英文小写**，避免 GitHub Pages 中文路径编码问题。

### 2.5 创建文章的三种方式

**方式一：使用工具（推荐）**

```powershell
cd C:\Users\Lenovo\Desktop\ryanwu_blog
python tools/new-post.py
```

按提示回答问题即可自动生成规范文件。

**方式二：复制模板**

1. 复制 `scaffolds/post.md`（技术笔记）或 `scaffolds/life.md`（生活随笔）
2. 粘贴到 `source/_posts/`
3. 重命名为 `YYYY-MM-DD-标题.md`
4. 修改内容

**方式三：命令行创建**

```powershell
npx hexo new "文章标题"
```

---

## 三、图片上传指南

### 3.1 存放位置

文章配图统一放在：

```
source/images/posts/
```

### 3.2 上传步骤

**第一步：复制图片到博客目录**

```powershell
copy "C:\Users\你的电脑\Desktop\照片.jpg" "C:\Users\Lenovo\Desktop\ryanwu_blog\source\images\posts\"
```

**第二步：在文章中引用**

```markdown
![图片描述](/images/posts/照片.jpg)
```

**第三步：发布**

```powershell
python tools/publish.py
```

### 3.3 设置文章封面图

在文章 Front-matter 中添加：

```markdown
---
title: 文章标题
date: 2026-06-06 12:00:00
tags: [python]
categories: tech
cover: /images/posts/文章封面.jpg
---
```

### 3.4 图片规范

- **格式**：jpg, png, gif, svg
- **建议宽度**：不超过 1200px（避免加载过慢）
- **命名**：使用英文或数字，避免中文和特殊字符

---

## 四、项目页面管理

项目页面文件：`source/projects/index.md`

### 4.1 添加新项目

**使用工具（推荐）：**

```powershell
python tools/new-project.py
```

按提示输入项目信息即可自动追加到页面。

**手动添加格式：**

```markdown
### 项目名称

**时间：** 2025/09 - 2025/11  
**角色：** 全栈工程师  
**技术栈：** Next.js, TailwindCSS, OpenAI

一句话项目简介...

**核心亮点：**
- 亮点一
- 亮点二
- 亮点三
```

### 4.2 修改已有项目

**使用工具：**

```powershell
python tools/edit-project.py
```

选择 "修改项目"，按提示操作。

**手动修改：**

1. 打开 `source/projects/index.md`
2. 找到对应项目段落（从 `### 项目名称` 开始）
3. 直接编辑文字内容

### 4.3 删除项目

**使用工具：**

```powershell
python tools/edit-project.py
```

选择 "删除项目"，输入项目编号即可。

**手动删除：**

1. 打开 `source/projects/index.md`
2. 找到要删除的项目段落（从 `### 项目名称` 到下一个 `###` 之间）
3. 删除整个段落

---

## 五、关于我页面更新

文件位置：`source/about/index.md`

**更新方式：** 直接用编辑器打开文件，修改 Markdown 内容即可。

**推荐结构：**

```markdown
---
title: 关于我
date: 2026-06-05 12:00:00
aside: true
top_img: /about-bg.jpg
---

## 你好，我是 Ryan

个人简介...

### 教育背景

| 学校 | 专业 | 学历 | 时间 |
|------|------|------|------|
| 南京邮电大学 | 通信工程 | 本科 | 2024/09 - 2028/06 |

### 技能栈

**前端开发**
- 框架：React, Vue 3
- ...

**联系方式**
- GitHub: [Ryan-wu-web](https://github.com/Ryan-wu-web)
- Email: 3047967569@qq.com
```

---

## 六、工具使用指南

### 6.1 工具清单

| 工具 | 功能 | 命令 |
|------|------|------|
| `new-post.py` | 交互式创建文章 | `python tools/new-post.py` |
| `new-project.py` | 交互式添加项目 | `python tools/new-project.py` |
| `edit-project.py` | 修改/删除项目 | `python tools/edit-project.py` |
| `publish.py` | 一键发布到线上 | `python tools/publish.py` |

### 6.2 使用前提

所有工具需要在 **PowerShell** 中运行，先进入博客目录：

```powershell
cd C:\Users\Lenovo\Desktop\ryanwu_blog
```

### 6.3 new-post.py 使用示例

```
==================================================
创建新文章
==================================================

文章类型:
  1. 技术笔记
  2. 生活随笔
请选择 (输入数字): 1

文章标题: Python爬虫入门实战

发布日期 [2026-06-06]:

标签设置
常用技术标签: python, javascript, vue...
标签: python, 爬虫, tutorial

文章描述/摘要（可选）:

==================================================
文章已创建: source/_posts/2026-06-06-python-pa-ru-men-shi-zhan.md
==================================================

接下来:
  1. 用编辑器打开文件继续写作
  2. 写完后执行: python tools/publish.py
```

### 6.4 publish.py 使用示例

```
==================================================
一键发布到线上
==================================================

检测到的改动:
 M source/_posts/...

请选择提交类型:
  1. post: 发布新文章
  2. update: 更新页面
  3. style: 样式/图片调整
  4. fix: 修复内容
  5. 自定义

选择 [5]: 1

提交信息 [post: add new article]:

确认发布? (y/n) [y]: y

==================================================
发布成功！
==================================================

等待 1-2 分钟后，访问 https://ryanwu.cn 查看更新
```

---

## 七、发布流程

### 7.1 发布文章

```powershell
cd C:\Users\Lenovo\Desktop\ryanwu_blog

# 方式一：使用工具
python tools/new-post.py      # 创建文章
# ... 用编辑器写作 ...
python tools/publish.py        # 发布

# 方式二：手动命令
python tools/new-post.py
git add source/_posts/
git commit -m "post: add 文章标题"
git push origin main
```

### 7.2 更新页面（关于我/项目）

```powershell
cd C:\Users\Lenovo\Desktop\ryanwu_blog

# 修改文件后
python tools/publish.py

# 或手动
# git add source/about/
# git commit -m "update: about page"
# git push origin main
```

### 7.3 本地预览

写文章时想看效果：

```powershell
cd C:\Users\Lenovo\Desktop\ryanwu_blog
npx hexo server
```

浏览器访问 `http://localhost:4000`

按 `Ctrl+C` 停止预览。

---

## 八、Markdown 速查

```markdown
# 一级标题
## 二级标题
### 三级标题

**加粗**
*斜体*
~~删除线~~

- 无序列表
- 无序列表

1. 有序列表
2. 有序列表

`行内代码`

```python
# 代码块
print("hello")
```

[链接文字](https://example.com)

![图片描述](/images/posts/xxx.jpg)

> 引用文字

| 表头 | 表头 |
|------|------|
| 内容 | 内容 |

---  # 分割线
```

---

## 附录：Git 提交信息规范

| 类型 | 用途 | 示例 |
|------|------|------|
| `post:` | 发布新文章 | `post: add python爬虫入门` |
| `update:` | 更新页面内容 | `update: about page` |
| `fix:` | 修复内容错误 | `fix: 修正项目链接` |
| `style:` | 样式/图片调整 | `style: 更换项目封面图` |
| `tools:` | 工具更新 | `tools: add edit-project tool` |

---

> **提示：** 本规范文档会随博客迭代持续更新，如有疑问随时查阅或询问。
