---
title: TetCTF 2023 All crypto + misc writeup by Neobeo
contest: TetCTF
year: 2023
team: Neobeo
difficulty: hard
vuln_type: crypto_rsa
tags: [negative-amount, biased-bits, lll-attack-ecdsa, weak-entropy-3n, aes-cbc-bitflip-json, sqli-postgres]
attack_chain:
- Casino 注册 + Bet 负数 -10^100 拿无限余额
- ShowBalanceWithProof 拿 Balance + Proof
- FlagSeller PrintFlag 拿 flag: TetCTF{fr0m_n3g4t1v3n3ss_t0_b4nkruptcy}
- biased PRNG seed(2023) + 多次 random.shuffle 恢复
- 7dfdf6e...baf3c1 29 行 37 字节 hex: 1 bit/行 + 跨 37*8 shuffle
- Counter bits + majority voting: bit 出现 > len/2 次 → 1
- TetCTF{fr0m_buggy_sw4p_t0_r4nd0m_b14s!}
- 64 签名 ECDSA 弱 nonce: nonce = 1 byte (256 个候选)
- LLL reduce matrix 24 bit = 256 (248 候选)
- 64 sigs 矩阵 BKZ 还原私钥 1 byte
- 验证 (m + r*k) * s^-1 * G == r 即正确 key
- key 8JPNOogLTn8CPhlHzCkrywaSJciX5ygSkOff3P+kRes= → flag{TetCTF{0n3_byt3_0v3rfl0w_l34ds_t0_full_pr1v4t3_k3y_r3c0v3r}}
- Toy 加密 AES-CBC + key+iv 硬编码
- 位翻 + JSON 模 n 整除
- 1529 inputs 二分位爆破 + LLL
- Web: AES-CBC + jwt 伪造 + PostgreSQL INSERT INTO orders (image) VALUES ('/flag') SQL 注入
- TetCTF{R_u_4_f0rm3r_d3v_0f_th3_c0mp4ny?}
key_payload: {"Command":"Bet","Amount":-10**100}
one_liner: TetCTF 2023 Neobeo 综合：负数赌场 + biased PRNG + 1-byte nonce ECDSA LLL + AES-CBC 位翻 LLL + PostgreSQL SQLi。
lesson: 整数溢出 (int 类型足够大) + 弱 PRNG 种子 (seed=2023) + 1 字节 ECDSA nonce (256^2 候选) 三个经典漏洞组合。
quality: high
---
# TetCTF 2023 All crypto + misc by Neobeo

## 1. Casino - 负数 Bet
```python
get({"Recipient":"Casino","Command":"Register"})
get({"Command":"Bet","Amount":-10**100})
bal, proof = get({"Command":"ShowBalanceWithProof"}).decode().split()
print(get({"Recipient":"FlagSeller","Command":"PrintFlag","Balance":int(bal[:-1]),"Proof_Data":proof}))
# b'Your flag is: TetCTF{fr0m_n3g4t1v3n3ss_t0_b4nkruptcy}'
```
- 整数下溢变成天文正数，绕过余额检查

## 2. Insufficient Entropy (biased bits)
- 28 行 37 字节 hex
- 每行 bit i 由 `random.shuffle(range(37*8))` 决定
- `random.seed(2023)` 固定，多行投票恢复
- 多数投票: `2*cnt > len(lines)` 为 1
```python
random.seed(2023)
test = set()
for line in lines:
    x = list(range(37*8))
    random.shuffle(x)
    test.update(zip(x[::8], [b >> 7 for b in bytes.fromhex(line)]))
int(''.join([str(i) for _,i in sorted(test)]), 2).to_bytes(37, 'big')
# b'TetCTF{____1nsuff1c13nt_3ntr0py_____}'
```

## 3. Buggy Swap (xor bias)
- 39 字节 hex × 30 行
- xor base `aaaa` + Counter
```python
random.seed(2023)
test = Counter()
bias = b64decode('aaaa')
for line in lines:
    x = list(range(39*8))
    random.shuffle(x)
    test.update(zip(x, bits(xor(bytes.fromhex(line), bias))))
test = {a for a,b in test.items() if 2*b > len(lines)}
int(''.join([str(i) for _,i in sorted(test)]), 2).to_bytes(39, 'big')
# b'TetCTF{fr0m_buggy_sw4p_t0_r4nd0m_b14s!}'
```

## 4. 1-byte Overflow ECDSA
- 64 签名, nonce 1 byte (0-255)
- LLL 248 bit 候选
- 矩阵构造 + 还原私钥
```python
from crack_weak_ECDSA_nonces_with_LLL import order, make_matrix, privkeys_from_reduced_matrix

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
E = EllipticCurve(GF(p), [0,7])
G = -E.lift_x(Integer(0x79BE667E...81798))

data = []
for _ in trange(64):
    with remote('192.53.115.129', 31340) as sh:
        sh.send(bytes(48))
        data.append([bytes_to_long(b64decode(sh.readline(0)[3:]+b'=')) for _ in 'mrs'])

msgs = [m for m,r,s in data]
sigs = [(r,s) for m,r,s in data]
mat = make_matrix(msgs, sigs, None, 248)
keys = privkeys_from_reduced_matrix(msgs, sigs, None, mat.LLL())

m,r,s = data[0]
keys = [key for key in keys if ((m + r * key) * pow(s, -1, order) % order * G)[0] == r]
soln = b64encode(long_to_bytes(keys[0]))
# b'8JPNOogLTn8CPhlHzCkrywaSJciX5ygSkOff3P+kRes='
# TetCTF{0n3_byt3_0v3rfl0w_l34ds_t0_full_pr1v4t3_k3y_r3c0v3r}
```

## 5. Toy (AES-CBC bitflip + JSON)
- 32 字节 XOR pad + AES-CBC 加密
- 1529 inputs 二分位爆破 XOR pad
- LLL 构造 magic 数 `magic` 满足 `int.from_bytes(test, 'big') % n == 0`
```python
# 二分 + LLL
mat = matrix(MAX+2, MAX+2)
for i in range(MAX):
    mat[i,i] = 1
    mat[i,-2] = 256**(2+i) * W1
mat[-2,-2] = n * W1
mat[-1,-2] = residue * W1
mat[-1,-1] = W2
lll = mat.LLL()[-1]
magic = list(lll[:MAX])
# json.loads(test) 仍合法
send_input(xor(test + bytes(32), xorpad))
# TetCTF{____t0y_1s_just_t0y____}
```

## 6. Order (Web SQL Injection)
- JWT 伪造 + AES-CBC 加密订单
- 注入点: `{"id":1,"title":"',0,0); INSERT INTO orders (image) VALUES ('/flag'); --"}`
- PostgreSQL 注入修改 image 字段
- 读取 `/order/218351` 拿 flag
- `TetCTF{R_u_4_f0rm3r_d3v_0f_th3_c0mp4ny?}`
