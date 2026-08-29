---
title: 北美大厂后端开发CTF面试题解题记录
contest: Fetch Backend CTF (北美大厂面试题)
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [北美大厂面试, Fetch Backend CTF, 列目录漏洞, NaCl secretbox, pynacl, openapi, gRPC, connect+json, JWT]
attack_chain:
  - 题目: Fetch Backend CTF (美国后端开发岗线上面试题)
  - 5 个 token 隐藏, 不需要找全
  - Token1: 列目录漏洞 → /pages/token.md 直接访问
  - Token2: /pages/secretbox.md NaCl secretbox 解密
  - pip install pynacl
  - base64_key = dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g=
  - base64_nonce = usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq
  - 解密 1: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IkpXVF9UT0tFTiJ9.ghpSD18...
  - 解密 2: NA_CL_SECRET_TOKEN
  - Token3: /pages/openapi.yaml 找 /token.v1.TokenService/GetToken + StreamToken
  - POST application/json + Token2 Bearer 拿到第 3 个 token
  - Token4: /StreamToken 接受 application/connect+json (connect+proto/grpc)
  - HTTP/2 415 Unsupported Media Type → connect+json 重试
  - Token5: 未拿到 (作者放弃)
key_payload: 'pynacl nacl.secret.SecretBox + openapi.yaml + connect+json'
one_liner: 北美大厂后端 CTF 5 token: 列目录 + NaCl secretbox 解密 + openapi.yaml 接口 + connect+json gRPC。
lesson: 列目录漏洞是 Web 入门常见; NaCl secretbox 需 pynacl nacl.secret.SecretBox; openapi.yaml 暴露 gRPC 端点; connect+json 是 gRPC-Web 协议。
quality: medium
---

# 北美大厂后端开发CTF面试题解题记录

## 概览
- **来源**: ctfiot 230796
- **题目**: Fetch Backend CTF (美国后端开发岗线上面试题)
- **难度**: ⭐⭐

## 5 个 Token 收集

### Token1: 列目录
- 根目录存在列目录漏洞
- `/pages/token.md` 直接访问

### Token2: NaCl secretbox 解密
- `/pages/secretbox.md` 提供 Base64 key/nonce/value
```python
import nacl.secret
import base64
base64_key = "dGhpc2lzYWtleXdpdGgzMmxldHRlcnNpbml0ZmV0Y2g="
base64_nonce = "usbsgmFzQNjwMEEZVqJ6Hdy8MOJwMOiq"
key = base64.b64decode(base64_key)
nonce = base64.b64decode(base64_nonce)
encrypted_value = base64.b64decode(base64_encrypted_value)
box = nacl.secret.SecretBox(key)
decrypted_value = box.decrypt(encrypted_value)
# 1: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IkpXVF9UT0tFTiJ9.ghpSD18-j76IdRH3xqaKk1-PrnyzOq3E5kiqUGLXzBI
# 2: NA_CL_SECRET_TOKEN
```

### Token3: openapi.yaml 接口
- `/pages/openapi.yaml` 暴露 gRPC 端点
```yaml
/token.v1.TokenService/GetToken (POST, application/json)
/token.v1.TokenService/StreamToken (POST, application/json)
```
- 携带 Token2 Bearer 头 POST 拿 token

### Token4: connect+json (gRPC-Web)
- Accept-Post: `application/connect+json, application/connect+proto, application/grpc, application/grpc+json, application/grpc+proto, application/grpc-web, application/grpc-web+json, application/grpc-web+proto`
- 用 connect+json 重新请求
- HTTP/2 415 Unsupported Media Type

### Token5: 未拿到
- 作者放弃, 提交 3 个 token + 1 个 Authorization

## 工具
- `pip install pynacl`
- nacl.secret.SecretBox (libsodium)

## 教学
- 列目录漏洞: Apache/IIS/Nginx 缺 index 文件时
- NaCl secretbox = XSalsa20-Poly1305 AEAD
- gRPC-Web 协议栈: grpc-web / grpc-web+json / grpc-web+proto / connect+json
- 美国后端大厂年薪 ~9w USD
