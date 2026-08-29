---
title: 侧信道攻击赛题Power Trajectory Diagram官方WP - 大鲲智联+信安国赛
contest: 第十七届全国大学生信息安全竞赛-创新实践能力赛初赛(2024 CISCN)
year: 2024
difficulty: medium
vuln_type: crypto_rsa
tags: [侧信道攻击, 功耗轨迹, Power_Trace, npz文件, numpy, matplotlib, 皮尔逊相关系数, corrcoef, 伽玛实验场, 大鲲智联, CISCN_2024, 智能网联汽车]
attack_chain: 加载npz查看files(index/input/output/trace) → 4键值trace 520长度 → 思路1:plot每组trace人工判断正确密码(波谷X坐标异常) → 思路2:argmin(trace[i])找最低峰X坐标,max_index对应正确字符 → 思路3:corrcoef(avg_trace, trace[i])皮尔逊相关系数,阈值0.90过滤正确字符
key_payload: 40字符输入 × 13轮 × trace长度520 + corrcoef阈值0.90
one_liner: 大鲲智联+CISCN 2024侧信道功耗分析3种思路破解_ciscn_2024_12位密码:人工作图/argmin最低峰/皮尔逊相关系数自动。
lesson: 侧信道功耗分析经典三法:plot肉眼比较、argmin最低峰位置(正确密码因CPU执行不同而波谷X偏移)、corrcoef皮尔逊相关系数(正确字符与平均值corr<0.90,错误≥0.99);密码12位(题目说13位但第13位无效);npz格式含index/input/output/trace四键值。
quality: high
---
