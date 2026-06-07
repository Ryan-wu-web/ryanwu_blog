# Ryan's Blog

<p align="center">
  <a href="https://ryanwu.cn" target="_blank">
    <img src="https://img.shields.io/badge/website-ryanwu.cn-blue?style=flat-square&logo=internet-explorer" alt="Website">
  </a>
  <a href="https://github.com/Ryan-wu-web/ryanwu_blog/actions" target="_blank">
    <img src="https://img.shields.io/github/deployments/Ryan-wu-web/ryanwu_blog/github-pages?style=flat-square&logo=github" alt="Deploy">
  </a>
  <img src="https://img.shields.io/badge/hexo-7.x-blueviolet?style=flat-square&logo=hexo" alt="Hexo">
  <img src="https://img.shields.io/badge/theme-butterfly-pink?style=flat-square" alt="Butterfly">
</p>

<p align="center">
  <b>Ryan 的个人博客</b> — 热爱技术，热爱生活
</p>

---

## 预览

线上地址：[https://ryanwu.cn](https://ryanwu.cn)

## 技术栈

- **静态生成器**：[Hexo](https://hexo.io/) 7.x
- **主题**：[Butterfly](https://butterfly.js.org/) 4.x
- **评论系统**：[Twikoo](https://twikoo.js.org/)
- **部署平台**：GitHub Pages + GitHub Actions
- **自定义域名**：ryanwu.cn

## 项目结构

```
ryanwu_blog/
├── source/                      # 博客内容源文件
│   ├── _posts/                  # 文章目录（技术笔记 + 生活随笔）
│   ├── about/                   # 关于我页面
│   ├── projects/                # 项目展示页面
│   ├── images/                  # 图片资源
│   └── ...
├── tools/                       # 内容维护工具
│   ├── new-post.py              # 创建新文章
│   ├── new-project.py           # 添加新项目
│   ├── edit-project.py          # 修改/删除项目
│   └── publish.py               # 一键发布
├── docs/                        # 文档
│   └── content-guide.md         # 内容维护规范
├── _config.yml                  # Hexo 主配置
├── _config.butterfly.yml        # Butterfly 主题配置
└── .github/workflows/           # GitHub Actions 自动部署
```

## 快速开始

### 本地预览

```bash
npm install
npx hexo server
```

访问 `http://localhost:4000`

### 发布内容

```bash
# 创建新文章
python tools/new-post.py

# 添加新项目
python tools/new-project.py

# 修改/删除项目
python tools/edit-project.py

# 一键发布到线上
python tools/publish.py
```

## 内容规范

详细规范请查看：[docs/content-guide.md](./docs/content-guide.md)

### 文章分类

| 分类 | 路径 | 说明 |
|------|------|------|
| 技术笔记 | `categories/tech/` | 编程、AI、项目经验 |
| 生活随笔 | `categories/life/` | 旅行、运动、日常记录 |

### 标签规范

标签统一使用**英文小写**，避免中文路径编码问题。

## 特性

- 深色 / 浅色双主题切换
- 首页打字机效果
- 分类/标签/归档页自定义打字机标语
- 全站街头风景背景图
- Twikoo 评论系统
- 站内搜索
- 代码高亮 + 复制按钮
- 文章目录导航
- GitHub Actions 自动部署

## 更新日志

- **2026-06-06** — 博客正式上线，完善关于我、项目、标签云等内容
- **2026-06-05** — 搭建 Hexo + Butterfly 框架，配置主题、背景图、打字机效果

## License

MIT License

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Ryan-wu-web">Ryan</a>
</p>
