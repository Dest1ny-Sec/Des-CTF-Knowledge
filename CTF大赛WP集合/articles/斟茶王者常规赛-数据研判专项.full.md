---
title: 斟茶王者常规赛 数据研判专项
contest: 斟茶王者
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags:
- grep-access_key_id
- admin-log-IP
- user-log-login
- balance-log-recursive
- order-time-range
- pymysql-team-sales
- data-forensics
attack_chain:
- '1. grep 搜 access_key_id: `grep -rn ''/www/wwwroot/testing-2th.ns'' -e ''access_key_id'
- '2. admin_log 按 IP 聚合:'
- SELECT ip, COUNT(*) as count FROM admin_log GROUP BY ip ORDER BY count DESC;
- '3. user_log login_ip 聚合:'
- SELECT login_ip, COUNT(*) as count FROM user_log GROUP BY login_ip ORDER BY count DESC;
- '4. balance_log 627 下级 sum:'
- SELECT SUM(amount) FROM hdk.balance_log WHERE uid='627' AND desc LIKE '%下级%';
- '5. order 时间范围 + goods_id 范围:'
- SELECT * FROM order WHERE order_time BETWEEN 1696089600 AND 1698768000 AND goods_id IN (4,5,6,7,8,9,10,11);
- '6. pymysql 递归团队销售额:'
- 'team_members = {pid: [uid, ...]} 建图'
- count_sales(uid) 递归 SUM(pay_amount)
key_payload: '''grep -rn + admin_log + user_log + balance_log + order 1696089600-1698768000 + pymysql 递归'''
one_liner: 斟茶王者数据研判：grep access_key_id + admin_log IP 聚合 + user_log 登录 + balance_log 下级 + order 范围 + pymysql 团队销售。
lesson: CTF 数据研判题目以 SQL 聚合 + grep 检索 + Python 递归为主。
quality: medium
full_path: 斟茶王者常规赛-数据研判专项.full.md
meta_path: 斟茶王者常规赛-数据研判专项.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '斟茶王者常规赛 数据研判专项。斟茶王者数据研判：grep access_key_id + admin_log IP 聚合 + user_log 登录 + balance_log 下级 + order 范围 + pymysql 团队销售。。关键路径：1. grep 搜 access_key_id: `grep -rn ''/www/wwwroot/testing-2th.ns'' -e ''acce...'
category: misc
subcategory: misc_other
tools_used:
- Python
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/154785.html
reasoning_chain:
- Q1 题目让搜 /www/wwwroot/testing-2th.ns 下 access_key_id → 触发点：必须用 grep 递归搜
- 动作：grep -rn '/www/wwwroot/testing-2th.ns' -e 'access_key_id' → 观察：找到 access_key_id 文件 → 下一步：拼 admin_log
- Q2 admin_log 按 IP 聚合 → 触发点：找访问最频繁 IP → 动作：SELECT ip,COUNT(*) GROUP BY ip ORDER BY count DESC
- 观察：得到 max count IP → 下一步：转向 user_log login_ip 聚合
- Q3 user_log login_ip 聚合 → 假设：登录源 IP 也能 GROUP BY → 动作：同上模板
- Q4 627 下级销售总和 → 触发点：balance_log uid=627 + desc 含下级 → 动作：SELECT SUM(amount) WHERE uid='627' AND desc LIKE '%下级%'
- Q5 order 时间范围 + goods_id 范围 → 假设：1696089600-1698768000 是指定窗口 → 动作：goods_id IN (4-11)
- Q6 团队递归销售额 → 触发点：uid→pid 是树形 → 假设：DFS 累加 pay_amount → 动作：pymysql 建 team_members 字典递归
failed_attempts:
- 试图直接 cat /root 文件 → 失败：flag 在数据库表里，不在文件系统
- 试图手写 SQL 不用 pymysql → 失败：递归团队销售额必须 Python 端建图
key_observations:
- grep -rn + GROUP BY + 递归是数据研判三大件
- uid→pid 是树形结构，递归前必须先一次性 SELECT 全部节点建图
- BETWEEN 范围 + IN 列表是 order 表筛选的标准组合
- PyMySQL 是 Python 端 SQL 操作的官方库
prerequisites:
- Linux 命令行（grep -rn 递归搜索）
- SQL 聚合（GROUP BY + ORDER BY + SUM）
- PyMySQL 库基础 + Python 递归函数
---
# 斟茶王者常规赛-数据研判专项

> 原文: https://www.ctfiot.com/154785.html
> ID: 154785

要在 Linux 的 /www/wwwroot/testing-2th.ns 目录下搜索文件内容包含 access_key_id 的命令，你可以使用 grep 命令。请在终端中运行以下命令：

grep -rn '/www/wwwroot/testing-2th.ns' -e 'access_key_id'

这个命令的参数解释如下：

-r：递归搜索目录及其子目录。

-n：显示匹配行的行号。

'/www/wwwroot/testing-2th.ns'：要搜索的目录路径。

-e 'access_key_id'：要搜索的字符串（在这里是 access_key_id）。

这个命令将返回所有包含 access_key_id 的文件列表。

SELECT ip, COUNT(*) as count
FROM admin_log
GROUP BY ip
ORDER BY count DESC;

SELECT login_ip, COUNT(*) as count
FROM user_log
GROUP BY login_ip
ORDER BY count DESC;

SELECT SUM(`amount`) as total_amount
FROM `hdk`.`balance_log`
WHERE `uid` = '627' AND `desc` LIKE '%下级%';

SELECT *
FROM `order`
WHERE order_time BETWEEN 1696089600 AND 1698768000 
AND goods_id IN (4, 5, 6, 7, 8, 9, 10, 11);

pip install pymysql

# -*- coding:
utf-8 -*-
import pymysql

# 连接到MySQL数据库
connection = pymysql.connect(host='你的数据库地址',
                             user='你的数据库地址用户名',
                             password='你的数据库地址密码',
                             db='你的数据库')

# 创建一个游标
cursor = connection.cursor()

# 查询所有用户及其上级
cursor.execute("SELECT uid, pid FROM users")
users = cursor.fetchall()

# 构建一个字典，其中键是用户ID，值是包含该用户所有下级的列表
team_members = {}
for user in users:
    uid, pid = user
    if pid not in team_members:
        team_members[pid] = []
    team_members[pid].append(uid)

# 定义一个递归函数，用于计算uid的销售额以及其所有下线的销售额
def count_sales(uid):
    sales = 0
    # 查询uid的订单总额
    cursor.execute(f"SELECT SUM(pay_amount) FROM `order2` WHERE uid = '{uid}'")
    result = cursor.fetchone()
    if result and result[0]:
        sales += result[0]
    # 计算下线的销售额
    if uid in team_members:
        for member_uid in team_members[uid]:
            sales += count_sales(member_uid)
    return sales

# 计算UID团队的销售额并输出
for uid in team_members :
    team_sales = count_sales(uid)
    print(f"团队 {uid} 的销售额: {team_sales}")

# 关闭游标和数据库连接
cursor.close()
connection.close()


```
要在 Linux 的 /www/wwwroot/testing-2th.ns 目录下搜索文件内容包含 access_key_id 的命令，你可以使用 grep 命令。请在终端中运行以下命令：

grep -rn '/www/wwwroot/testing-2th.ns' -e 'access_key_id'

这个命令的参数解释如下：

-r：递归搜索目录及其子目录。

-n：显示匹配行的行号。

'/www/wwwroot/testing-2th.ns'：要搜索的目录路径。

-e 'access_key_id'：要搜索的字符串（在这里是 access_key_id）。

这个命令将返回所有包含 access_key_id 的文件列表。
SELECT ip, COUNT(*) as count
FROM admin_log
GROUP BY ip
ORDER BY count DESC;
SELECT login_ip, COUNT(*) as count
FROM user_log
GROUP BY login_ip
ORDER BY count DESC;
SELECT SUM(`amount`) as total_amount
FROM `hdk`.`balance_log`
WHERE `uid` = '627' AND `desc` LIKE '%下级%';
SELECT *
FROM `order`
WHERE order_time BETWEEN 1696089600 AND 1698768000 
AND goods_id IN (4, 5, 6, 7, 8, 9, 10, 11);
pip install pymysql
# -*- coding:
utf-8 -*-
import pymysql

# 连接到MySQL数据库
connection = pymysql.connect(host='你的数据库地址',
                             user='你的数据库地址用户名',
                             password='你的数据库地址密码',
                             db='你的数据库')

# 创建一个游标
cursor = connection.cursor()

# 查询所有用户及其上级
cursor.execute("SELECT uid, pid FROM users")
users = cursor.fetchall()

# 构建一个字典，其中键是用户ID，值是包含该用户所有下级的列表
team_members = {}
for user in users:
    uid, pid = user
    if pid not in team_members:
        team_members[pid] = []
    team_members[pid].append(uid)

# 定义一个递归函数，用于计算uid的销售额以及其所有下线的销售额
def count_sales(uid):
    sales = 0
    # 查询uid的订单总额
    cursor.execute(f"SELECT SUM(pay_amount) FROM `order2` WHERE uid = '{uid}'")
    result = cursor.fetchone()
    if result and result[0]:
        sales += result[0]
    # 计算下线的销售额
    if uid in team_members:
        for member_uid in team_members[uid]:
            sales += count_sales(member_uid)
    return sales

# 计算UID团队的销售额并输出
for uid in team_members :
    team_sales = count_sales(uid)
    print(f"团队 {uid} 的销售额: {team_sales}")

# 关闭游标和数据库连接
cursor.close()
connection.close()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]