---
title: 【WP】2022数字中国创新大赛车联网安全赛 best_agent 设计思路与解析
contest: 数字中国
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [car-cybersecurity, CAN-bus-analysis, websocket-flow, open_right_door, git-info-leak, python-CRLF-CVE-2019-9947, Apache-HTTPD-header-parse]
attack_chain: 1. CAN 流量分析 + websocket 流量获取 + git 信息泄露 + Python CRLF 注入 CVE-2019-9947 + Apache HTTPD 请求头解析/2. 探索页面 http 触发操作 + 逃跑页面 websocket 触发操作/3. 多次调 open_left 接口 + 抓 CAN 流量 + 找重复开右车门请求/4. eventlet.monkey_patch + websocket.WebSocketApp on_message + 写入 after_{max_round}.log
key_payload: open_left 接口 + 重复 CAN 流量 + websocket on_message
one_liner: 2022 数字中国车联网安全赛 best_agent，CAN 总线流量分析 + websocket 实时流量抓取 + git 信息泄露。
lesson: 车联网 CAN 流量分析 + websocket 实时流量是车联网 CTF 核心；多次触发同操作找重复帧是 CAN 流量特征提取标准方法。
quality: high
---

# 【WP】2022数字中国创新大赛车联网安全赛 best_agent 设计思路与解析

## 概览
2022 数字中国创新大赛网络安全赛道 - 车联网安全赛 `best_agent` 题设计思路与解法。

## 题目要素
1. CAN 流量分析
2. websocket 流量获取
3. git 信息泄露
4. Python CRLF 注入 CVE-2019-9947
5. Apache HTTPD 请求头解析

## 解题路径

### 1. 探索页面 + 逃跑页面
- 探索页面提供 http 方式触发操作，返回流量
- 逃跑页面提供 websocket 方式触发操作
- 流程：触发动作 → 获取流量 → 提交流量

### 2. websocket 抓 CAN 流量
```python
import websocket
import eventlet
import requests
eventlet.monkey_patch()

def on_message(ws, message):
    global max_counts, do_it, max_round
    if not do_it and max_counts > 0:
        max_counts = max_counts - 1
    if max_counts == 0:
        if not do_it:
            with requests.get(f"http://{url}/test/control?op=open_left") as f:
                print(f.text)
        do_it = not do_it
        max_counts = 20
        max_round = max_round - 1
    if do_it and max_counts > 0:
        with open(f"test/after_{max_round}.log", "a+") as f:
            f.write(message)

ws = websocket.WebSocketApp("ws://ip:port/test/log", on_message=on_message)
ws.run_forever()
```

### 3. CAN 流量特征提取
- 调 open_left 接口发出开右车门请求
- 多次调接口
- 后续流量中一直重复的帧 = 开右车门请求帧
- 写入 `after_{max_round}.log` 保存

## 经验提炼
- 车联网 CAN 流量分析 + websocket 实时流量是车联网 CTF 核心
- 多次触发同操作找重复帧是 CAN 流量特征提取标准方法
- CVE-2019-9947 Python CRLF 注入是 Python urllib 漏洞
- Apache HTTPD 请求头解析漏洞（futrue header）需关注
- git 信息泄露可下载 `.git` 目录历史版本
- websocket 长连接可实时抓取车机流量
- eventlet.monkey_patch 兼容同步代码写异步 websocket
- 文件名 `after_{max_round}.log` 是按轮次记录
