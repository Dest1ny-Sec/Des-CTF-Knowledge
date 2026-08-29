---
title: 强网拟态防御/zerocalc
contest: 强网拟态
year: 2021
difficulty: medium
vuln_type:
- ssti
- ssrf
- rce
tags:
- notevil patched eval
- cookieSession key 可控
- cookie pollution
- readFile
- /etc/passwd 泄露
- /flag 随机名
attack_chain:
- 题目给 notevil（patched 过的 eval）但还接受额外 utils 参数
- 注入：readFile('/etc/passwd') 直接读 /etc/passwd（notevil 不挡 fs.readFile）
- cookieSession 用 Math.random().toString(16) 作 secret（弱但难爆破）
- 注入读 /proc/self/environ 或 /proc/1/environ 找 secret
- 用 secret 伪造 session 注入 cookieSession 污染
- 注入 hi.unshift(`${e} = ${ret}`) 让历史记录显示任意内容
- flag 路径随机：find / -name 'flag*' 2>/dev/null 遍历目录
- 读 flag 文件
key_payload: "e = \"readFile('/etc/passwd')\""
one_liner: notevil 注入 readFile 读 /etc/passwd + 找 cookieSession secret 伪造 session
lesson: "patched" 库接受额外参数时仍可注入；cookieSession secret 用弱熵 Math.random 易被读 /proc 还原
quality: high
---

# 强网拟态防御/zerocalc

**notevil 注入 readFile + cookieSession secret 泄露**

> 强网拟态 · 2021 · medium · ssti/ssrf/rce · quality=high
> 思路: notevil 注入 readFile('/etc/passwd') → 找 cookieSession secret → 伪造 session 污染 → 找随机名 flag 文件
> 套路: "patched" 库接受额外参数时仍可注入；cookieSession secret 用弱熵 Math.random 易被读 /proc 还原

**关键 payload**:
```javascript
e = "readFile('/etc/passwd')"
```
