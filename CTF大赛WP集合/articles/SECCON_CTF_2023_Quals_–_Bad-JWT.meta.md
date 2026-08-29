---
title: SECCON CTF 2023 Quals - Bad-JWT
contest: SECCON CTF 2023 Quals
year: 2023
difficulty: high
vuln_type: crypto_oracle
tags: [jwt, prototype-pollution, map-vs-object, toprimitive, type-juggling, node-js, alg-constructor]
attack_chain:
  - 自研 JWT: HS256/HS512 algorithms + base64UrlEncode/Decode + parseToken + sign + verify
  - verify 用 Buffer.compare(calculated_buf, expected_buf) !== 0 校验
  - 漏洞: header.alg.toLowerCase() + algorithms[alg](data, secret) 索引
  - 攻击 1: alg='constructor' → algorithms['constructor'] = undefined
  - calculated_signature = undefined(data, secret) → 触发 String 转换
  - crypto.createHmac("sha256", secret) → Hmac 接受 undefined secret 报 TypeError
  - 但 undefined(..., ...) 在 JS 中调用返回 undefined 字符串
  - 攻击 2: alg 改成 "constructor" 后 calculated_signature 包含 base64 字符串
  - 把 calculated_signature 复制到 signature 字段 → 校验通过
  - jwt = header(alg=constructor) + payload(isAdmin=true) + calculated_sig
  - Buffer.compare 接收 "calculated" + "expected" 都是 base64 字符串
  - 关键: 算法名 prototype chain attack + Buffer.from(string, 'base64') 接受 Symbol.toPrimitive
  - 实战: class Bar [Symbol.toPrimitive] = 'eyJ0eXAi...' 触发 Buffer.from 转换
  - 完整 chain: 1) alg=constructor 2) 复制 calculated_signature 3) 提交 session cookie
  - flag: SECCON{Map_and_Object.prototype.hasOwnproperty_are_good}
key_payload: header = {"typ": "JWT", "alg": "constructor"} + body = {"isAdmin": true} + jwt.signature = calculated_signature
one_liner: SECCON CTF 2023 Quals Bad-JWT：自研 JWT alg 字段未白名单 + prototype chain attack + 算法名 'constructor' 触发 Buffer.from(Symbol.toPrimitive) 类型转换 bypass 签名校验。
lesson: JWT 实现 alg 字段必须白名单 (HS256/RS256) 防 prototype 链污染；Map/Object.prototype.hasOwnProperty 是 JS 通用过滤工具；Buffer.from(symbol, 'base64') 接受 Symbol.toPrimitive 是 Node 经典 bypass。
quality: high
---
