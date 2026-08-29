---
title: DataCon2021优秀解题思路分享：域名体系安全（清华大学-叽里呱啦）
contest: DataCon 2021
year: 2021
difficulty: medium
vuln_type: misc_unknown
tags: [dns, domain, 涉赌, 涉黄, 涉诈, ca-cert, html, graph, 团伙分析]
attack_chain:
  - 27万黑白域名分类：涉赌/涉黄/涉诈
  - 黑产团伙关联分析
  - 7种关联边（强到弱）：CA Alternative Name/HTML IP邮箱/统计ID/动态跳转URL/统计链接/人工特征/HTML相似度
  - 并查集维护子图
  - HTML相似度：最长公共子序列+桶排序优化+O(100N)复杂度
  - C++实现+多进程
key_payload: \b[CA证书Alternative Name]\b | \b[HTML相似度>90%]\b  # 7种关联边
one_liner: DataCon2021域名体系安全：27万域名分类+并查集团伙分析+HTML相似度优化
lesson: 大规模域名分析需用并查集+LCS优化+多进程并行
quality: high
---

# DataCon2021优秀解题思路分享：域名体系安全（清华大学-叽里呱啦）

## 题目信息
- 比赛：DataCon 2021
- 方向：域名体系安全
- 战队：清华大学 - 叽里呱啦
- 规模：27 万黑白域名

## 关键攻击链
### 1. 数据采集
- `dns-crawler` 抓取 DNS/HTTP/HTTPS 信息
- `Playwright + Chromium` 动态渲染
- 多进程并行

### 2. 关联图（7 种边，按关联性强弱）
1. **CA 证书 Alternative Name**（最强）
2. HTML 硬编码 IP/邮箱
3. 统计链接 ID
4. 动态跳转后 URL 一致
5. 动态加载时统计链接一致
6. 人工提取 HTML 特征
7. HTML 源码相似度极高（最弱）

### 3. 团伙识别算法
- 并查集维护同子图节点集合
- 按关联性强弱顺序聚类

### 4. HTML 相似度优化
```python
# 过滤非ASCII、字母、数字、&#;转义
# 两两计算LCS（最长公共子序列）
# 改进：判定性问题（相似度>90%且差<100字符）
# 桶排序：长度差大的域名对不参与
# C++实现+多进程
# 时间复杂度从O(N²L²)降到O(100N)
```

### 5. 人工干预
- 排除域名过期跳转域名服务商
- 同模板不同黑产、404 页面相似度误判
- 相似度数据用于辅助人工判断

## 评分
- quality: high（27 万域名 + 7 种关联边 + LCS 优化 + 并查集）
