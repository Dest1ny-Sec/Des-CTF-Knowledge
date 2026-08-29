---
title: 湖南省第二届职工数字化应用技术技能大赛-数据安全管理员赛项选拔赛-科目二-wp
contest: 湖南省第二届职工数字化应用技术技能大赛
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [base16解码, RSA+LCG, 数据脱敏逆向, dirsearch扫描, JS前端加密绕过, 身份证号]
attack_chain: 题目1 base16解码身份证号→题目2 RSA+LCG（AI解）→题目3 缺失（poem.png）→题目4 ds_re5 IDA逆向→题目5 dirsearch扫描robots.txt发现/tjhack/→题目6 JS前端加密请求体构造+两个账号登录+查询接口
key_payload: "base16解码;RSA+LCG;dirsearch robots.txt;JS加密timestamp+user_id+data"
one_liner: 湖南省第二届职工数安赛D2：base16+RSA+LCG+数据脱敏+dirsearch+JS前端加密绕过
lesson: 数据安全管理员赛题偏简单基础+AI辅助解题（DeepSeek比qwen本地0.6b强）
quality: medium
---

# 湖南省第二届职工数字化应用技术技能大赛-数据安全管理员赛项选拔赛-科目二-wp

**赛事**：湖南省第二届职工数字化应用技术技能大赛（科目二数据安全管理员，2025）

**8道题速解**：

**1. b.zip（基础编码）**
- 一串字符串 → base16解码 → 身份证号
- flag: `140825195506302668`

**2. RSA_LCG.zip（密码学）**
- RSA + LCG组合
- 现场本地 qwen3:0.6b 解不出
- 复盘用腾讯元宝 DeepSeek 可解
- flag: `2c532af14547ff78756d2695d11787af`

**3. poem.rar（图片隐写）**
- 缺失的poem.txt文件
- 复盘都未看出

**4. ds_re5（逆向数据脱敏）**
- IDA逆向 + AI分析核心代码

**5. bmm_web_20250807（Web敏感路径）**
- 网页源代码加载CSS，登录框无反应
- dirsearch扫描发现 robots.txt
- flag: `/tjhack/`

**6. js-drox（前端加密绕过）**
- 前端JS加密请求体：`{"timestamp": 1758420734, "user_id": 1001, "data": "VtjTr5gaWd0vs7uWu6g4gGNXWjE1VWLKFfga4Np1OK+s9bb3iDz3Zs3owyXlYhal"}`
- 响应包含 base64加密的 balance/id_card/name
- 给了两个账号登录后台
- 后台"查询用户信息"接口绕过权限控制
- flag: `350122199703073498`（王成）

**7-8. 数据分析1/数据分析2**：
- 在本WP中部分涉及，详情略

**技术总结**：
- base16/64/32/CTF编码工具一键识别
- AI辅助解RSA+LCG（DeepSeek > qwen3:0.6b本地）
- dirsearch扫描robots.txt
- JS前端加密请求体可逆向/重放

**质量评估**：中（基础题型，AI辅助思路）
