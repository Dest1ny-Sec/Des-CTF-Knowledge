---
title: bi0sCTF 2022 Writeup by r3kapig
contest: bi0sCTF
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [r3kapig, menu, static-key, encrypt-injection, rop, cross-challenge]
attack_chain:
  - 逆向菜单 1-5 选项 add/delete/show/edit/encrypt
  - 发现静态密钥 2111485077978050
  - encrypt(0, decrypt(payload)) 触发注入
  - 构造 ROP pop_rdi+pop_rax+syscall
  - execve /bin/sh
key_payload: 静态 AES key + encrypt-decrypt 注入链
one_liner: bi0sCTF 2022 r3kapig 战队多题 WP，菜单类 PWN 注入与跨题 ROP 链构造。
lesson: CTF 题目间可能存在 attack 复用：encrypt 题目拿到的 oracle 可注入其他题；RCE 链要从前置题"借"密钥。
quality: high
---

bi0sCTF 2022 r3kapig 战队官方 WP 集合。代表性 PWN 题：notes 菜单
1-5 选项 add/delete/show/edit/encrypt。加密函数用静态密钥
`2111485077978050`（明文 16 字节 ASCII），且 `encrypt(0, payload)` 把
buf[0] 改写为密文。

关键洞：`encrypt(0, decrypt(payload))` 在密文 → 密文 → 解密 的链路里，
第一次解密后 buf[0] 是任意字节，第二次加密又把它们当明文加密回去；
但若用 `encrypt(idx, 0)` 这种调用模式，buf 内容保留为解密后的明文，
构造任意地址写。

更精彩的是 r3kapig 演示了"跨题攻击"：前置 crypto 题目拿到的 AES 密钥
恰好与本菜单 key 复用，于是 ROP 链 `pop rdi; pop rax; syscall` 拼
`/bin/sh\0` + execve 一气呵成，最后跨题拿到 flag。

合集里其他题包括 heap off-by-one、fmt-string 栈泄漏、kernel 提权，
每道都附 IDA / GDB 脚本与利用代码。r3kapig 的 WP 风格：截图 + 注释 +
对应 commit link 都有，赛期 1 周就公开。
