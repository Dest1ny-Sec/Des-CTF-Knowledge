---
title: 强网杯 2025/pwn adventure
contest: 强网杯
year: 2025
difficulty: hard
vuln_type:
- pwn_unknown
tags:
- C++ 游戏
- 整数溢出
- UAF
- tcache poisoning
- 0x60 tcache
- 堆块描述指针
- 堆地址泄露
- libc 泄露
- stderr ROP
- seccomp 绕过
attack_chain:
- 审 C++ 小游戏：warrior/shop/inventory/search/quit 等指令
- 整数溢出：Buy Items 时输入数量 8500600（int32 上限）触发 gold 变负 -2118813696
- 用溢出金钱买大量 Bomb，去 boss 图炸 boss 拿 Paralysis Ring
- 装备描述溢出：手动输入超长 name 触发 cursor 越界写
- UAF：use_item 释放堆块后，物品描述指针仍指向已释放的 0x60 tcache
- tcache 加密指针：利用多次 buy/use 把 0x60 4 个堆块全部分配出去
- 泄露：通过 UAF 读 tcache 堆块首部，heap_addr = (leak << 12) - 0x19000
- 泄露 libc/libstdc++：堆地址 + 描述指针任意读
- 任意地址写：控制物品描述指针 + edit 写
- 找修改 rsp 的 gadget + 通过 stderr 做 ROP
- 用 mprotect 把 shellcode 区段设为可执行
key_payload: "heap_addr = (edit_ring(b'a') << 12) - 0x19000; edit_ring(rop_chain_via_stderr)"
one_liner: 整数溢出 + UAF 装备描述指针 + tcache 泄露 + stderr ROP 绕过 seccomp
lesson: 游戏题整数溢出金币可触发经济崩溃；C++ UAF 装备描述指针是经典 pwn 套路；glibc 2.32+ tcache 加密指针需先 leak heap 再 xor
quality: high
---

# 强网杯 2025/pwn adventure

**整数溢出 + UAF 装备描述指针 + tcache 泄露 + stderr ROP**

> 强网杯 · 2025 · hard · pwn · quality=high
> 思路: 审 C++ 小游戏指令 → Buy Items 整数溢出买大量 Bomb → 炸 boss 拿 Ring → 装备描述溢出触发 cursor 越界 → UAF：use_item 释放堆块但描述指针仍指向已释放 0x60 tcache → 多次 buy/use 耗尽 tcache → 泄露 heap_addr + libc → 任意地址写 → 改 rsp + stderr ROP
> 套路: 游戏题整数溢出金币可触发经济崩溃；C++ UAF 装备描述指针是经典 pwn 套路；glibc 2.32+ tcache 加密指针需先 leak heap 再 xor

**关键 payload**:
```python
heap_addr = (edit_ring(b'a') << 12) - 0x19000
edit_ring(rop_chain_via_stderr)
```
