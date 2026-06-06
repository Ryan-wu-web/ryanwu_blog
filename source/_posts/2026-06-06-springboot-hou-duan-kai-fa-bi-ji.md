---
title: SpringBoot 后端开发笔记
date: 2026-06-06 15:30:00
tags: [springboot, java, backend, mysql, redis]
categories: tech
description: SpringBoot 项目开发中的一些实践经验
---

## 分层架构设计

Controller -> Service -> Mapper -> Database 的分层结构清晰明了。

## 常用注解

- `@RestController` 快速构建 RESTful API
- `@MapperScan` 自动扫描 MyBatis 接口
- `@Cacheable` 配合 Redis 实现缓存

## 数据库优化

- 合理使用索引提升查询效率
- 使用连接池管理数据库连接
- 分页查询避免大数据量一次性加载
