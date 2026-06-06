---
title: Android 开发入门记录
date: 2026-06-06 16:00:00
tags: [android, kotlin, mobile, opengl]
categories: tech
description: 记录 Android 原生开发的学习过程
---

## Kotlin vs Java

Kotlin 的语法更加简洁，空安全机制减少了大量 NPE 问题。

## UI 开发

- RecyclerView 实现列表展示
- ViewPager2 + TabLayout 实现页面切换
- ConstraintLayout 构建复杂布局

## 性能优化

- 使用 OpenGL ES 实现高性能图像渲染
- 图片加载使用 Glide 进行缓存管理
- 避免内存泄漏，合理使用生命周期
