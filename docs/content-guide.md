# Ryan's Blog - 内容维护规范

> 本文档是博客的长期内容维护指南，确保所有内容格式统一、发布流程标准化。

---

## 一、博客内容结构总览

```
source/
├── _posts/                    # 文章目录（技术笔记 + 生活随笔）
│   ├── 2026-06-06-文章标题.md
│   └── ...
├── about/
│   └── index.md               # 关于我页面
├── projects/
│   └── index.md               # 项目展示页面
├── categories/
│   └── index.md               # 分类汇总页（自动生成，勿动）
├── tags/
│   └── index.md               # 标签汇总页（自动生成，勿动）
└── images/                    # 文章配图存放（可选）
```

---

## 二、文章发布规范（技术笔记 & 生活随笔）

### 2.1 文件命名规范

```
YYYY-MM-DD-文章标题.md
```

示例：
- `2026-06-06-python爬虫入门.md`
- `2026-06-10-端午节杭州旅行.md`

### 2.2 Front-matter 模板

**技术笔记模板：**

```markdown
---
title: 文章标题
date: 2026-06-06 14:30:00
tags: [python, 爬虫, 教程]      # 英文标签，小写
categories: tech                # 固定为 tech
description: 这是一篇关于...的文章   # 可选：文章摘要，SEO用
cover: /images/文章封面.jpg      # 可选：文章封面图
---

正文内容...
```

**生活随笔模板：**

```markdown
---
title: 文章标题
date: 2026-06-06 14:30:00
tags: [旅行, 杭州]              # 英文标签，小写
categories: life                # 固定为 life
description:  optional
cover: /images/文章封面.jpg      # 可选
---

正文内容...
```

### 2.3 标签（tags）命名规范

| 类别 | 推荐标签 | 说明 |
|------|---------|------|
| 技术类 | python, javascript, vue, react, ml, dl, algorithm, linux, git, docker, database, frontend, backend | 技术栈 |
| 项目类 | project, internship, competition, bootcamp, open-source | 项目经历 |
| 生活类 | travel, sports, photography, reading, daily, food, movie | 生活记录 |

> ⚠️ **标签统一使用英文小写**，避免 GitHub Pages 中文路径编码问题。

### 2.4 发布流程

**方法一：手动创建（推荐）**

1. 在 `source/_posts/` 下新建 `.md` 文件
2. 按照模板填写 Front-matter
3. 写 Markdown 正文
4. 保存

**方法二：命令行创建**

```bash
cd C:\Users\Lenovo\Desktop\ryanwu_blog
npx hexo new "文章标题"
```

这会生成 `source/_posts/文章标题.md`，然后你编辑内容即可。

**发布到线上：**

```bash
cd C:\Users\Lenovo\Desktop\ryanwu_blog
git add source/_posts/
git commit -m "post: add 文章标题"
git push origin main
```

等待 1-2 分钟，网站自动更新。

---

## 三、关于我页面更新规范

### 3.1 文件位置

`source/about/index.md`

### 3.2 更新方式

直接编辑该文件，修改 Markdown 内容即可。不需要改 Front-matter。

### 3.3 推荐内容结构

```markdown
---
title: 关于我
date: 2026-06-05 12:00:00
aside: true
top_img: /about-bg.jpg
---

## 👋 你好，我是 Ryan

一段个人简介...

### 🎓 教育背景

- 学校 | 专业 | 时间

### 💼 工作经历

- 公司 | 岗位 | 时间 | 简介

### 🏆 比赛与荣誉

- 比赛名称 | 奖项 | 时间

### 🛠️ 技能栈

- **语言**：Python, JavaScript...
- **框架**：Vue, React...
- **工具**：Git, Docker...

### 📫 联系方式

- GitHub: [Ryan-wu-web](https://github.com/Ryan-wu-web)
- Email: your-email@example.com
```

**更新后发布：**

```bash
git add source/about/
git commit -m "update: about page"
git push origin main
```

---

## 四、项目页面更新规范

### 4.1 文件位置

`source/projects/index.md`

### 4.2 项目卡片格式（推荐）

```markdown
---
title: 项目
aside: false
top_img: /projects-bg.jpg
---

## 💼 我的项目

### 项目名称 1

![项目封面](/images/project1-cover.jpg)

**简介：** 一句话描述项目做什么

**技术栈：** Python · Flask · MySQL

**时间：** 2026.03 - 2026.06

**链接：** [GitHub](https://github.com/xxx) · [在线演示](https://xxx.com)

---

### 项目名称 2

...
```

### 4.3 修改或删除已有项目

**方式一：用工具（推荐）**

```powershell
python tools/edit-project.py
```

按提示选择要修改或删除的项目即可。

**方式二：手动编辑**

直接打开 `source/projects/index.md`，找到对应项目段落：

```markdown
### 项目名称

**时间：** xxx
**角色：** xxx
...
```

- **修改**：直接编辑文字内容
- **删除**：删除从 `### 项目名称` 到下一个 `###` 之间的全部内容

**更新后发布：**

```powershell
python tools/publish.py
```

---

## 五、常用 Markdown 语法速查

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

![图片描述](/images/xxx.jpg)

> 引用文字

| 表头 | 表头 |
|------|------|
| 内容 | 内容 |
```

---

## 六、图片管理规范

### 6.1 存放位置

文章配图建议放在 `source/images/` 目录下：

```
source/
├── images/
│   ├── posts/           # 文章配图
│   │   ├── 2026-06-06-python爬虫/
│   │   │   ├── img1.png
│   │   │   └── img2.png
│   │   └── ...
│   └── projects/        # 项目封面图
│       ├── project1-cover.jpg
│       └── ...
```

### 6.2 引用方式

**在文章中引用图片：**

```markdown
![图片描述](/images/posts/你的图片.jpg)
```

**完整操作流程：**

```powershell
# 1. 把图片复制到博客目录
copy "C:\Users\你的电脑\Desktop\照片.jpg" "C:\Users\Lenovo\Desktop\ryanwu_blog\source\images\posts\"

# 2. 在文章 md 文件中引用
# ![照片](/images/posts/照片.jpg)

# 3. 发布到线上
python tools/publish.py
```

**设置文章封面图（在 front-matter 中）：**

```markdown
---
title: 文章标题
date: 2026-06-06 12:00:00
tags: [python]
categories: tech
cover: /images/posts/文章封面.jpg
---
```

---

## 七、本地预览（可选）

写文章时想先看看效果：

```bash
cd C:\Users\Lenovo\Desktop\ryanwu_blog
npx hexo server
```

浏览器访问 `http://localhost:4000`

按 `Ctrl+C` 停止预览。

---

## 八、Git 提交信息规范

| 类型 | 用途 | 示例 |
|------|------|------|
| `post:` | 发布新文章 | `post: add python爬虫入门` |
| `update:` | 更新页面内容 | `update: about page` |
| `fix:` | 修复内容错误 | `fix: 修正项目链接` |
| `style:` | 样式/图片调整 | `style: 更换项目封面图` |
