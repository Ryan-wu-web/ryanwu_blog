---
title: 如何用Python写爬虫
date: 2026-06-06 12:00:00
tags: [python, tutorial, spider]
categories: tech
description: 一篇面向初学者的Python爬虫入门教程，包含requests和BeautifulSoup的基础用法
---

## 引言

爬虫是数据采集的重要工具。本文将带你用Python快速上手爬虫开发。

## 正文

### 环境准备

```bash
pip install requests beautifulsoup4
```

### 发送HTTP请求

```python
import requests

url = "https://example.com"
response = requests.get(url)
print(response.status_code)
print(response.text[:500])
```

### 解析HTML

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')
titles = soup.find_all('h1')
for title in titles:
    print(title.get_text())
```

### 保存数据

```python
import json

data = {
    'title': '示例标题',
    'url': url
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 总结

本文介绍了Python爬虫的基础流程：发送请求 -> 解析页面 -> 提取数据 -> 保存数据。后续可以学习Scrapy框架和反爬策略。
