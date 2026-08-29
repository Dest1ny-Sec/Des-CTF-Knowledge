---
title: 第七届西湖论剑·中国杭州网络安全技能大赛初赛Writeup
contest: 第七届西湖论剑初赛
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [西湖论剑, 签到题二维码, CSV数据分析, users/permissions/tables/actionlog关联]
attack_chain: 二维码图片属性详情找flag→CSV数据分析(用户/权限/表/日志关联)→flag
key_payload: "users.csv;permissions.csv;tables.csv;actionlog.csv;user[0,1,3];permissions[0,2,3];tables[0,1,2];actionlog[0,1,2,3]"
one_liner: 第七届西湖论剑初赛：签到二维码属性+CSV四表关联分析
lesson: 签到题常藏flag在文件属性/EXIF/隐藏流；CSV数据库分析是基本功
quality: low
---

# 第七届西湖论剑·中国杭州网络安全技能大赛初赛Writeup

**赛事**：第七届西湖论剑初赛（2024）

**MISC-2024签到题**：

**Step 1：图片属性**
- 附件是公众号二维码图片
- 在图片的属性详情里发现flag线索

**Step 2：CSV数据分析**
- 4个CSV文件：users / permissions / tables / actionlog
- Python csv.reader读取
- user取 [0, 1, 3] 列
- permissions取 [0, 2, 3] 列
- tables取 [0, 1, 2] 列
- actionlog取 [0, 1, 2, 3] 列
- 循环关联对比，提取符合条件的记录

```python
import csv
lists = ['users', 'permissions', 'tables', 'actionlog']
for log in actionlog[1:]:
    log_id = log[0]
    log_name = log[1]
    log_time = log[2].split(' ')[1]
    log_opt = log[3]
    
    for users_A in users[1:]:
        users_id = users_A[0]
        users_name = users_A[1]
        users_per = users_A[3]
        if users_name == log_name:
            name_ti = 0
            for per_A in permissions[1:]:
                # ... 关联
```

**质量评估**：低（签到题，无详细解法）
