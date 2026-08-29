---
title: 看雪2022 KCTF 春季赛 | 第六题设计思路及解析
contest: 看雪2022 KCTF春季赛
year: 2022
difficulty: hard
vuln_type: rop
tags: [纯汇编栈溢出, SROP, sigreturn系统调用, BROP盲打, syscall;retn gadget, vsyscall 0xffffffffff600000]
attack_chain: 纯汇编栈溢出覆盖返回地址→sigreturn系统调用号15(64位)/77(32位)→用vsyscall syscall;retn gadget 0xffffffffff600000→SROP构造sigframe→调用read+execve(/bin/sh)
key_payload: "栈缓冲区0x10溢出;read返回字节数触发SROP;vsyscall=0xffffffffff600000 syscall;retn;syscall号15(64)/77(32)"
one_liner: KCTF2022春Q6《废土末世》PWN：纯汇编+SROP+vsyscall syscall;retn 0xffffffffff600000
lesson: 无libc栈溢出用SROP（sigreturn 15/77）+vsyscall=0xffffffffff600000 gadget
quality: high
---

# 看雪2022 KCTF 春季赛 | 第六题设计思路及解析

**赛事**：看雪2022 KCTF春季赛 Q6《废土末世》

**难度**：围观8341人，4队破解，一血6h44min（辣鸡战队）

**题目设计**：
- **纯汇编**编写（无libc）
- 系统调用写入0x400数据到v1（v1只有0x10大小） → 栈溢出
- 没有libc → 不能用普通ROP

**核心利用**：
- 系统调用号15（64位）/ 77（32位）触发 **Sigreturn**
- sigreturn从用户栈恢复所有寄存器
- 攻击者控制栈 → 控制所有寄存器
- 只需 `syscall; retn` gadget

**vsyscall gadget**：
- 地址 `0xffffffffff600000`（老系统未随机化）
- 内含 `syscall; retn`

**BROP攻击流程**：
1. 探测溢出长度
2. 探测特殊gadget
3. 泄露程序代码段内存
4. 白盒分析

**具体探测**：
- 缓冲区0x10
- 试探：输入16字符正常，17字符无输出 → 长度16
- 探测栈上字节原始值：
  - 17字节前缀+遍历第17字节
  - 发现 `0xce` 让程序正常（"TNT TNT!"）→ 原始值
- 探测18字节：`0xce 0x00` → 唯一normal
- 探测19字节：`0xce 0x00 0x40` 或 `0x60` → 两个地址
  - `0x4000ce` = 代码段基地址（非PIE）
  - `0x6000ce` = 数据段基地址
- 确认64位非PIE程序

**SROP构造**：
```python
frame = SigreturnFrame()
frame.rax = constants.SYS_execve
frame.rdi = constants.SYS_execve  # /bin/sh
frame.rsi = 0
frame.rdx = 0
frame.rip = 0xffffffffff600000  # syscall;retn
```

**关键技术**：
- **Sigreturn**：系统调用号15（64位）/77（32位）→ 不做frame检查直接恢复所有寄存器
- **vsyscall**：`0xffffffffff600000` 含 `syscall; retn`（老Linux未随机化）
- **BROP**：盲打探测栈溢出长度、gadget、内存地址
- 无libc情况下唯一可用的栈溢出利用方式

**质量评估**：高（SROP原理清晰 + BROP探测步骤）
