---
title: AI 大模型应用实践
date: 2026-06-06 16:30:00
tags: [ai, openai, gpt, prompt-engineering, vision]
categories: tech
description: 分享在实际项目中接入 AI 大模型的经验
---

## 模型选择

- OpenAI GPT-4o：通用能力强，适合对话场景
- 智谱 AI GLM-4V：中文理解优秀，支持视觉
- 腾讯混元：国内场景适配好

## Prompt 工程

- 使用角色设定提升回答质量
- 通过 Few-shot 示例引导输出格式
- 温度参数调节创造性 vs 准确性

## 流式输出

使用 SSE (Server-Sent Events) 实现打字机效果，提升用户体验。
