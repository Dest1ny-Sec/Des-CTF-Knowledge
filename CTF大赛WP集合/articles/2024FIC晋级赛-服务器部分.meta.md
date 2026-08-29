---
title: 2024 FIC 晋级赛 - 服务器部分
contest: FIC晋级赛
year: 2024
difficulty: medium
vuln_type: [forensic_disk, sqli, misc_unknown]
tags: [MySQL 邀请人排行, 收入汇总, 提现总额, app_group_member, app_user_record, app_user_withdraw]
attack_chain: 登录服务器 MySQL → 选业务库 → 查 app_group_member.inviter_id NOT NULL GROUP BY inviter_id 排行 → 查 app_user_record WHERE object_type=2 AND money>0 GROUP BY user_id 算总收入 → 查 app_user_withdraw WHERE status=3 提现成功总额
key_payload: SELECT inviter_id, COUNT(*) AS total_invited FROM app_group_member WHERE inviter_id IS NOT NULL GROUP BY inviter_id ORDER BY total_invited DESC; SELECT user_id, SUM(money) AS total_money FROM app_user_record WHERE object_type=2 AND money>0 GROUP BY user_id ORDER BY total_money DESC; SELECT SUM(amount) AS total_successful_withdrawn_amount FROM app_user_withdraw WHERE status=3
one_liner: 邀请人数 + 用户收入 + 提现总额三联查。
lesson: 邀请人排行靠 GROUP BY inviter_id COUNT，用户收入靠 object_type=2 过滤正向流水。
quality: low
---
# 2024 FIC 晋级赛 - 服务器部分

**核心 SQL 模板**

```sql
-- 邀请人排行（推广数）
SELECT inviter_id, COUNT(*) AS total_invited
FROM app_group_member
WHERE inviter_id IS NOT NULL
GROUP BY inviter_id
ORDER BY total_invited DESC;

-- 用户总收入（object_type=2 业务流水，money>0 正向）
SELECT user_id, SUM(money) AS total_money
FROM app_user_record
WHERE object_type = 2 AND money > 0
GROUP BY user_id
ORDER BY total_money DESC;

-- 提现成功总额（status=3 已完成）
SELECT SUM(amount) AS total_successful_withdrawn_amount
FROM app_user_withdraw
WHERE status = 3;
```

**关键字段解读**

| 表 | 字段 | 含义 |
|------|------|------|
| `app_group_member` | `inviter_id` | 谁邀请的（NULL=自然注册） |
| `app_user_record` | `object_type` | 1=支出 2=收入 3=退款 |
| `app_user_withdraw` | `status` | 1=待审 2=处理中 3=已打款 4=拒绝 |

> 三个查询分别对应"推广人数排行" / "用户收入排行" / "总提现金额"，原文没给具体数据结果，**仅给 SQL 模板**。
