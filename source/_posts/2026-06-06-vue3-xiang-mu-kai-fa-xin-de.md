---
title: Vue3 项目开发心得
date: 2026-06-06 15:00:00
tags: [vue, javascript, frontend, typescript]
categories: tech
description: 分享在 Vue3 项目开发中的一些实践经验
---

## Composition API 的优势

Vue3 的 Composition API 让代码逻辑更加清晰，尤其在大中型项目中，比 Options API 更易于维护。

## 状态管理

Pinia 相比 Vuex 更加轻量，TypeScript 支持也更好。

## 性能优化

- 合理使用 `v-memo` 和 `shallowRef`
- 组件懒加载减少首屏时间
- 使用 `defineAsyncComponent` 实现异步组件
