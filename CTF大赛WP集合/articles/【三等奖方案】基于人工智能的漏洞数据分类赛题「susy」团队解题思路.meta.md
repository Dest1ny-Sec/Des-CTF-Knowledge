---
title: CCF BDCI 2022 三等奖 - AI漏洞数据分类 susy战队
contest: CCF BDCI 2022 数字安全公开赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [CVE, 漏洞分类, TF-IDF, 词向量, 集成模型, LightGBM, NLP, privilege_required, attack_vector, impact]
attack_chain: 加载数据 → TF-IDF构造词向量 → 降维 → 提取CVE编号特征 → 词向量+人工特征拼接 → 三个字段分别训练分类器 → 阈值调整 → 合并结果
key_payload: TF-IDF(降维) + LightGBM分类 + 三级标签分开训练
one_liner: 北工大硕士+中大博士用TF-IDF+集成学习做CVE漏洞三级分类,线上第3。
lesson: 漏洞分类三级标签分开训练比合并训练效果好;TF-IDF降维既降内存又加速训练;集成模型相对深度网络速度更快、性能更稳定;换榜后不易过拟合。
quality: high
---
