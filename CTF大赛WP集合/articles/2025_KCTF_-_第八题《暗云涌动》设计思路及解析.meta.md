---
title: 2025 KCTF 第八题《暗云涌动》设计思路及解析（自定义 VM+指针标记+整数溢出）
contest: 2025 KCTF
year: 2025
difficulty: hard
vuln_type: [pwn_unknown, vm, integer_overflow]
tags: [KCTF 2025 第八题 暗云涌动, 自定义 VM, 0x4000000000000000 指针标记 bit63, adjust_pointer dmem/stack 范围校验, 整数溢出 0x4000000000200000 + 0x4000000000000000 = 0x8000000000200000 变指针, 任意地址读写, 堆地址爆破, libc 偏移, IO 链劫持, 星盟安全团队]
attack_chain:
  - VM 结构：pc/sp/stack(256 QWORD)/dmem(0x200000 1KB)/imem(0x1000 512 条 8B 指令)/regs(8 QWORD)
  - 指针标记：bit63=1 视为指针
  - adjust_pointer: 检查地址是否在 dmem[..+0xFF8] 或 stack[..+0x7F8] → 标记
  - 整数溢出：两非指针数加法高位溢出变指针，绕过 adjust_pointer 校验
  - 0x4000000000200000 + 0x4000000000000000 = 0x8000000000200000（溢出 bit63=1 → 标记为指针）
  - 任意地址读 + libc 偏移 + IO 链劫持
  - 堆地址爆破 4-bit
key_payload: "0x4000000000200000 + 0x4000000000000000 = 0x8000000000200000 (整数溢出→指针)"
one_liner: 2025 KCTF 第八题 暗云涌动：自定义 VM + 指针标记 + 整数溢出 bypass adjust_pointer → 任意地址读写 + IO 链劫持。星盟出题。
lesson: 自定义 VM PWN 必看 ALU 整数溢出是否破坏指针标记；堆地址爆破 4-bit（16 试 1 中）时考虑 async 并发。
quality: high
---

# 2025 KCTF 第八题《暗云涌动》设计思路及解析

## KCTF 评委团队点评

> 这道 Pwn 题设计了一个自定义虚拟机，通过精妙的指针标记与算术运算规则，在 ALU 操作中隐藏了整数溢出漏洞：当两个非指针数值运算后高位溢出成为"指针"时，可绕过 adjust_pointer 校验，实现任意地址读写。利用需结合堆地址爆破、libc 偏移计算和 IO 链劫持，综合考察了虚拟机逆向、漏洞链构造和爆破技巧，难度较高但逻辑严密。

## 设计思路

出题团队：星盟安全团队

```python
# 关键：0x4000000000200000 + 0x4000000000000000 = 0x8000000000200000
# 通用寄存器 + 通用寄存器 = 指针寄存器（整数溢出！）

# adjust_pointer(invalid_pointer) = data_pointer
# adjust_pointer(stack_addr) = stack_addr
```

## VM 结构

```c
typedef struct VM {
    uint32_t pc;           // ctx->pc         程序计数器（按"指令"为单位）
    uint32_t sp;           // ctx->field_4    栈指针（元素个数，单位=8字节槽）
    uint64_t *stack;       // ctx->field_8    (256 个 QWORD，大小 0x800)
    uint8_t  *dmem;        // ctx->field_10   (mmap 到 0x200000, 0x1000 字节)
    uint8_t  *imem;        // ctx->instructions (0x1000 字节, 512 条 * 8B)
    uint64_t *regs;        // ctx->field_20   (8 个 QWORD，大小 0x40)
} VM;
```

`initcontext()`：
```c
imem = zmmap(NULL, 0x1000)  // 随机基址
dmem = zmmap((void*)0x200000, 0x1000)  // 必须固定地址 0x200000
regs = zalloc(0x40)
stack = zalloc(0x800)
read(0, imem, 0x1000)  // 字节码直接读入
```

## 指针标记与校验

```c
// 标记位：bit63=1 表示"被 VM 认可的指针"
int sub_12FE(v) { return v >> 63; }  // 判断指针
uint64_t sub_128B(p) {  // 打标函数
    if (p 落在 dmem [..+0xFF8] || 落在 stack [..+0x7F8])
        return p | 0x8000000000000000;  // bit63=1
    else
        return p;  // 不打标
}
```

## 整数溢出漏洞

两**非指针**寄存器 `0x4000000000200000 + 0x4000000000000000 = 0x8000000000200000`  
→ 高位溢出 bit63=1 → 满足 `sub_12FE == 1` → 视为"指针" → 绕过 `adjust_pointer` 校验  
→ 任意地址读写

## 利用链

1. **堆地址爆破**：4-bit → 16 次并发试
2. **libc 偏移**：environ/leak libc base
3. **IO 链劫持**：FSOP / House of Apple 2
4. **getshell**：`system("/bin/sh")` 或 `ORW` open/read/write
