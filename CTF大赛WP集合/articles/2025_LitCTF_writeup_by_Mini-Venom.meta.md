---
title: 2025 LitCTF writeup by Mini-Venom（NestJS 爆破 + 多重宇宙日记原型链污染 + 星愿信箱 SSTI）
contest: 2025 LitCTF
year: 2025
difficulty: medium
vuln_type: [web_unknown, ssti, deserialize, auth_bypass]
tags: [LitCTF nest_js 爆破 admin:password, 星愿信箱 {{ 过滤 SSTI, 多重宇宙日记 settings update JSON 解析, /api/profile/update POST 任意 settings 字段, settingsPayload 构造原型链污染, 升级 isAdmin=true]
attack_chain:
  - nest_js: admin/password 爆破登入即得 flag
  - 星愿信箱: 过滤 {{ 的 SSTI，需绕括号/下划线
  - 多重宇宙日记: 注册 a/a 登入 → 个人资料源代码 → /api/profile/update
  - 构造 JSON {"settings": {"theme": ..., "isAdmin": true, ...}} 注入管理员
  - 设置 isAdmin=true 后 page reload 看导航栏 admin 菜单 → 拿 flag
key_payload: "settingsPayload.isAdmin = true → setTimeout(reload, 1000) → page reload 拿 flag"
one_liner: 2025 LitCTF Web 三题：NestJS admin 弱密码爆破 + SSTI 绕 {{ 过滤 + 多重宇宙日记 settings JSON 注入 isAdmin=true 提权。
lesson: settings 类 JSON 接口常见原型链污染：把 admin 权限字段注入到 settings 后端会被 merge 到 user 对象 → 提权；SSTI 过滤 `{{` 时可考虑 `${ }` 或 `{% %}` 或 `#{ }`。
quality: medium
---

# 2025 LitCTF writeup by Mini-Venom

## Web

### nest_js（弱密码爆破）
admin / password 登入即得 flag。

### 星愿信箱（SSTI 绕 `{{` 过滤）
服务端渲染时过滤 `{{`，但其他模板语法 `${ }` / `{% %}` / `#{ }` 仍可触发。

### 多重宇宙日记（settings 注入 isAdmin）
注册 a/a 登入 → 个人资料看源代码：
```js
// /api/profile/update
const formData = new FormData(event.target);
const settingsPayload = {};
if (formData.get('theme')) settingsPayload.theme = formData.get('theme');
if (formData.get('language')) settingsPayload.language = formData.get('language');
// ...可以添加其他字段
const response = await fetch('/api/profile/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ settings: settingsPayload })
});
```

`sendRawJson()` 走用户原始 JSON：
```js
const rawJson = document.getElementById('rawJsonSettings').value;
// ...
body: JSON.stringify(parsedJson)  // 直接发用户 JSON
```

**攻击**：在 rawJson 框输入：
```json
{"settings": {"theme": "x", "isAdmin": true, "language": "en"}}
```
后端把 `settings.*` 合并到 user 对象 → `isAdmin=true` 提权 → `setTimeout(() => window.location.reload(), 1000)` 刷新页面看到 admin 菜单 → 拿 flag。
