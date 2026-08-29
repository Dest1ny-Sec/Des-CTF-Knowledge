---
title: CTF 汇编题目：x86 与 ARM 汇编基础
contest: 内部训练
year: 2022
difficulty: easy
vuln_type: reverse
tags: [x86, ARM, AT&T syntax, 看雪论坛, 入门]
attack_chain: |
  1. x86_64 (Ubuntu 11.4.0-1ubuntu1~22.04) AT&T 语法 .s 文件，main 循环 i=0..36:
     - movzbl (%rax,%rdx) → flag[i]
     - if i % 2 == 0 (偶数): flag[i] = flag[i] ^ i 输出
     - if i % 2 == 1 (奇数): tmp = flag[i-1] ^ (i-1); 输出 flag[i] ^ tmp (注意先改了 flag[i-1])
  2. C 等价代码:
     for i in range(39):
       if i % 2 == 0: print(chr(crypto[i] ^ i))
       else: crypto[i-1] ^= (i-1); print(chr(crypto[i-1] ^ crypto[i]))
  3. ARM (gcc 11.1 linux) thumb 语法，flag[] 27 字节:
     - 循环 i=0..26
     - if (i & 1) == 0: printf("%c", flag[i] ^ 57)
     - if (i & 1) == 1: printf("%c", flag[i])
  4. 等价 C 代码: while (i <= 26) { if ((i & 1) != 0) printf("%c", flag[i]); else printf("%c", flag[i] ^ 57); i++; }
  5. ARM 关键指令: push {r7, lr} 保存现场 + sub sp, sp, #8 8 字节栈 + add r7, sp, #0 形成帧指针 + ldrb r3, [r3] zero_extendqisi2
key_payload: |
  # x86 flag 解密:
  crypto = [0x66,0x0a,0x63,0x06,0x7f,0x1e,0x37,0x00,0x38,0x03,0x6f,0x04,0x6e,0x56,0x3d,0x55,
            0x22,0x06,0x26,0x51,0x72,0x04,0x21,0x03,0x21,0x01,0x7c,0x05,0x2b,0x0e,0x7c,0x50,
            0x17,0x56,0x10,0x0b,0x16,0x4f,0x26]
  flag = ''
  for i in range(39):
    if i % 2 == 0:
      flag += chr(crypto[i] ^ i)
    else:
      crypto[i-1] ^= (i-1)
      flag += chr(crypto[i-1] ^ crypto[i])
  print(flag)
  
  # ARM flag 解密:
  flag = [0x7d,0x41,0x6a,0x43,0x6d,0x46,0x42,0x31,0x5c,0x74,0x0c,0x64,0x09,0x5f,0x78,0x72,
          0x74,0x5f,0x6d,0x72,0x0d,0x31,0x57,0x69,0x57,0x47,0x44]
  for i in range(27):
    if (i & 1) != 0: print(chr(flag[i]), end='')
    else: print(chr(flag[i] ^ 57), end='')
one_liner: 看雪 NYSECbao 整理的 x86/ARM 汇编入门题，两段加密 flag 用 ^i/^(i-1) 和 ^57/直出 两种 XOR trick。
lesson: 读 .s 汇编文件先看 LFB/LFE 标函数边界 + .string/.ascii 找数据；AT&T 语法 movzbl (%rax,%rdx) 等价 *(uint8_t*)(rax+rdx)；ARM thumb 指令 ldrb + uxtb 是字节加载 + 零扩展。
quality: low
---

# CTF 汇编题目：x86 与 ARM 汇编基础

> 来源: ctfiot.com 141955 - 看雪论坛 NYSECbao 原创

## 题目一：x86 汇编 (gcc 11.4.0-1ubuntu1~22.04)

`main` 函数把 `encode` 字符串（39 个 `*`）当 flag 处理，循环 i=0..36：

```gas
.L5:                              # 循环
    addl $1, -4(%rbp)             # i++
.L2:
    movl -4(%rbp), %eax           # eax = i
    cltq                          # rax = sign_extend(eax)
    leaq encode(%rip), %rdx       # rdx = &encode
    movzbl (%rax,%rdx), %eax      # eax = encode[i] (zero_extend)
    movsbl %al, %ecx              # ecx = sign_extend(al)
    movl -4(%rbp), %eax           # eax = i
    andl $1, %eax                 # eax = i & 1
    testl %eax, %eax
    je .L3                        # 偶数 → 跳 .L3
    # 奇数: tmp = encode[i-1] ^ (i-1); print(tmp ^ encode[i])
    subl $1, %eax                 # eax = i-1
    cltq
    leaq encode(%rip), %rdx
    movzbl (%rax,%rdx), %eax      # eax = encode[i-1]
    movsbl %al, %eax
    jmp .L4
.L3:
    # 偶数: encode[i] ^ i
    movl -4(%rbp), %eax           # eax = i
.L4:
    xorl %ecx, %eax               # eax = eax ^ ecx
    movl %eax, %edi
    call putchar@PLT
    ...
    cmpq $37, %rax
    jbe .L5
```

**等价 C 代码：**
```c
for (size_t i = 0; i < 39; i++) {
    if (i % 2 == 0) {                              // 偶数
        printf("%c", crypto[i] ^ i);
    } else {                                       // 奇数
        crypto[i-1] ^= (i-1);                       // 先改前一个字节
        printf("%c", crypto[i-1] ^ crypto[i]);
    }
}
```

## 题目二：ARM 汇编 (gcc 11.1 linux)

```gas
main:
    push {r7, lr}                  # 保存 r7+lr
    sub sp, sp, #8                 # 8 字节栈
    add r7, sp, #0                 # 帧指针 = sp
    movs r3, #0
    str r3, [r7, #4]               # [r7+4] = 0 (i)
    b .L2
.L5:                              # 循环
    ldr r3, [r7, #4]               # r3 = i
    and r3, r3, #1
    cmp r3, #0
    bne .L3                        # 奇数 → 不操作
    # 偶数: flag[i] ^ 57
    movw r3, #:lower16:flag
    movt r3, #:upper16:flag
    ldr r2, [r7, #4]               # r2 = i
    add r3, r3, r2                 # r3 = &flag[i]
    ldrb r3, [r3]                  # r3 = flag[i]
    eor r3, r3, #57                # r3 ^= 57
    uxtb r3, r3                    # 零扩展
    mov r1, r3
    movw r0, #:lower16:.LC0
    movt r0, #:upper16:.LC0
    bl printf
    b .L4
.L3:                              # 奇数
    ldrb r3, [r3]                  # 直接 printf flag[i]
    mov r1, r3
    bl printf
.L4:
    ldr r3, [r7, #4]
    adds r3, r3, #1
    str r3, [r7, #4]
.L2:
    ldr r3, [r7, #4]
    cmp r3, #26
    ble .L5
    movs r3, #0
    mov r0, r3
    adds r7, r7, #8
    mov sp, r7
    pop {r7, pc}
```

**等价 C 代码：**
```c
int main() {
    char flag[] = { 0x7d, 0x41, 0x6a, ..., 0x44 };
    int i = 0;
    while (i <= 26) {
        if ((i & 1) != 0) {           // 奇数
            printf("%c", flag[i]);
        } else {                      // 偶数
            printf("%c", flag[i] ^ 57);
        }
        i++;
    }
}
```

## 评价

NYSECbao 整理的汇编入门训练，x86 用 AT&T 语法 + LFB/LFE 段边界定位 + 寄存器寻址模式；ARM thumb 用 r7 帧指针 + ldrb 零扩展。x86 关键 trick 是奇数分支会先 `crypto[i-1] ^= (i-1)` 再做 XOR，注意这个隐式副作用。

文章主要是分析过程 + 等价 C 代码，没有"我做题的思考路径"，所以作为汇编入门参考材料价值中等。
