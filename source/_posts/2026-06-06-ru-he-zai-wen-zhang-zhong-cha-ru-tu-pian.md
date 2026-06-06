---
title: 如何在文章中插入图片
date: 2026-06-06 14:00:00
tags: [tutorial, hexo, frontend, blog]
categories: tech
description: 教你如何在博客文章中上传和引用图片
---

## 引言

在博客文章中插入图片非常简单，只需要两步：上传图片 + 引用图片。

## 第一步：上传图片

把图片文件放到这个目录：

```
source/images/posts/
```

例如：
- `source/images/posts/my-photo.jpg`
- `source/images/posts/screenshot.png`
- `source/images/posts/diagram.svg`

## 第二步：在文章中引用

使用 Markdown 图片语法：

```markdown
![图片说明](/images/posts/my-photo.jpg)
```

## 示例

下面是一张示例图片：

![示例封面图](/images/posts/example-cover.jpg)

## 完整流程总结

```powershell
# 1. 复制图片到博客目录
copy "C:\Users\你的电脑\Desktop\照片.jpg" "C:\Users\Lenovo\Desktop\ryanwu_blog\source\images\posts\"

# 2. 在文章中引用
# ![照片](/images/posts/照片.jpg)

# 3. 发布
python tools/publish.py
```

## 小贴士

- 图片格式支持：jpg, png, gif, svg
- 建议图片宽度不超过 1200px，避免加载过慢
- 文章封面图可以在 front-matter 中设置：`cover: /images/posts/xxx.jpg`
