---
title: 2024 春秋杯夏季赛 WP（py一下&zwhubuntu 视角：Hijack / ezecc / Signatrue / 2024happy）
contest: 2024 春秋杯网络安全联赛夏季赛
year: 2024
difficulty: hard
vuln_type: [deserialize, sqli, rce, ecdsa, lattice, crypto_rsa, block_cipher]
tags: [ENV/DIFF/FILE/FUN POP 链, Hijack LD_PRELOAD 绕 disable_functions, brother 反弹 MySQL udf, ezecc ECC 256bit p=gcd 求曲线参数+爆破 k, Signatrue DSA LCG nonce 复用 HNP 格, 2024happy N^2+2024 Coppersmith + HSSP 正交格]
attack_chain:
  - Hijack: ENV.__toString → putenv LD_PRELOAD + system
  - 拿 shell → 找 mysql 凭据 → udf 提权
  - ezecc: 已知 a,b, K=(G=k*G 公开) → p = gcd(f1, f2) 求曲线素数
  - k 私钥 < 1e6 爆破 → m = C1 - k*C2, cipher_left/invert(m[0])%p = flag 前半
  - Signatrue: DSA 8 次签名, 同 nonce 复用 → HNP 格 A=R[i]*s0/(r0*S[i]), B=(r0*H[i]-R[i]*h0)/(r0*S[i])
  - 构造 Ge = [q*I; A; B; 0 0 K 1]，BKZ-30 → 还原 d, 重签 admin
  - pass_proof 爆破 2^19 大小写
  - 2024happy: N=n^2+2024, hint=(3^2022 p^2 + 5^2022 q^2) mod N, Coppersmith 还原 p,q
  - 4x4 LLL 矩阵 [[1,0,Ta*2^pbit,0],[0,1,Tb*2^qbit,0],[0,0,TN,0],[0,0,T*hh,N]] 找 p,q
  - AES-CBC key 解出 (key=mylove_in_summer)
  - HSSP part2: 31 个 As, 80 维 binary vectors xs, M=256bit, B=As*xs % M
  - find_ortho_fp kernel_LLL → recoverBinary all_ones {-1,0,1} → 求 As
  - AES IV=sha256(sum(As)).digest()[:16]
key_payload: "p = gcd(G[0]^3 + a*G[0] + b - G[1]^2, c1[0]^3 + a*c1[0] + b - c1[1]^2)"
one_liner: 春秋杯夏季赛三大 crypto + 一 web：Hijack LD_PRELOAD + ezecc gcd 求 ECC 曲线 + Signatrue DSA nonce 复用 HNP 格 + 2024happy N^2 Coppersmith + HSSP 正交格；全是密码学与 POP 链硬菜。
lesson: ezecc 的关键观察是 "K = (..., 4359... : 4359...) K = (G, kG)，求 p 时所有点代入曲线方程再 gcd" 一步出 p；Signatrue 用 A,B 矩阵构造 LLL 求 d 是教科书 HNP；2024happy 把 RSA 与 HSSP 拼接是密码学综合题经典套路。
quality: high
---

# 2024 春秋杯夏季赛 WP（py一下&zwhubuntu 战队）

## Web

### Hijack（LD_PRELOAD 绕 disable_functions）
```php
class ENV {
    public function __toString() {
        putenv("$key=$value");
        system("cat hints.txt");
    }
}
class DIFF { ... public function __isset($arg1) { system("cat /flag"); $this->callback->p; } }
class FILE { ... public function __call(...) { file_put_contents(...); rename(...); } }
class FUN { public function __get($name) { $this->fun->getflag($this->value); } }
```
POP 链：ENV.__wakeup → math=DIFF → flag 触发 __isset → callback=FUN → fun=FILE → FILE.__call 写 .so → putenv LD_PRELOAD → .so 加载时 system 反弹。

### brother
反弹 shell → 找 PHP 文件中 mysql 凭据 → 进 MySQL → udf 提权读 flag。

## Misc 1：勒索病毒
`class _377AbcaF(): def _1459BC58(self): if -9462 < 3956: os.system('cat /flag')`  
grep 'system' -B3 抽出函数调用链 `_O0._O0._O0...`，按链拼出混淆 python 字节码 → 反混淆 → 读 data.7z 拿 flag。

## Crypto

### ezecc（ECC 256bit p 隐变量）
p 未给，但 K = (G, kG) 在曲线上 → p = gcd(f1, f2)：
```python
f1 = G[0]^3 + a*G[0] + b - G[1]^2
f2 = c1[0]^3 + a*c1[0] + b - c1[1]^2
p = gcd(int(f1), int(f2))
# p = 35119411868157074664430974548068674543332670208412768267028980956903083749789
```
E = EllipticCurve(GF(p), [a, b])，k < 1e6 爆破：
```python
for k in tqdm(range(166000, 1000000)):
    m = C1 - k*C2
    left = cipher_left * invert(int(m[0]), p) % p
    right = cipher_right * invert(int(m[1]), p) % p
    if b'flag{' in long_to_bytes(int(left)): break
# flag{2d6a7e4e-02d3-11ef-8836-a4b1c1c5a2d2}
```

### Signatrue（DSA nonce 复用 HNP）
8 次签名，r/s 都给，目标是 8 次后伪造 admin 签名。

```python
# 8 个 (R[i], S[i], H[i]) 关系: s = k^-1 (H + x*r) mod q
# 同一 nonce 重用 → 已知 R[i], S[i], H[i] + A, B 矩阵
for i in range(1, len(R)):
    a = R[i]*s0 * invert(r0*S[i], q) % q
    b = (r0*H[i] - R[i]*h0) * invert(r0*S[i], q) % q
    A.append(a); B.append(b)
n = len(A)
Ge = Matrix(ZZ, n+2, n+2)
for i in range(n): Ge[i, i] = q
Ge[-2, :] = A + [0, 0]
Ge[-1, :] = B + [0, 0]
K = 2**128
Ge[-1, -1] = K
for line in Ge.BKZ(block_size=30):
    if abs(line[-1]) == K:
        k0 = line[-2]
        d = (k0 * s0 - h0) * invert(r0, q) % q
```

pass_proof 爆破 `happytheyearofloong` 大小写组合 2^19：
```python
table = itertools.product([0,1], repeat=19)
for i in tqdm(table):
    getin = ''.join(password[j].lower() if i[j]==0 else password[j].upper() for j in range(19))
    msg = getin[:5]+"_"+getin[5:8]+"_"+getin[8:12]+"_"+getin[12:14]+"_"+getin[14:]
    h = hashlib.sha256(msg.encode()).hexdigest()
    if h[:6] == head: return msg
```
**flag{7b640bd1-367c-4c8e-b656-315e7596ad85}**。

### 2024happy（N^2 + 2024 + HSSP）
```python
N = n**2 + 2024
hint = (pow(3, 2022, N) * p**2 + pow(5, 2022, N) * q**2) % N
c = pow(bytes_to_long(CBC_key), 65537, n)
```
4x4 LLL 矩阵找 p, q：
```python
T = 2^2048
L = matrix(ZZ, 4, 4, [
    [1, 0, T*a*2^pbit, 0],
    [0, 1, T*b*2^qbit, 0],
    [0, 0, T*N, 0],
    [0, 0, T*hh, N]
])
res = L.LLL()
for row in res:
    if abs(row[-1]) == N:
        p = gcd(n, abs(row[0])*2^pbit + lp)
        q = gcd(n, abs(row[1])*2^qbit + lq)
```
**key = b'mylove_in_summer'**。

Part 2 HSSP（Hidden Subset Sum Problem）：
```python
n, m = 31, 80
M = random_prime(2^256)
As = [random.randrange(0, M) for i in range(n)]
xs = [random_vector(GF(2), m).change_ring(ZZ) for i in range(n)]
Bs = sum(As[i] * vector(Zmod(M), xs[i]) for i in range(n)).change_ring(ZZ)
```
**Orthogonal Lattice Attack**（参考 https://tanglee.top/2023/12/12/Orthogonal-Lattice-Attack/）：
- `find_ortho_fp` / `find_ortho_zz` 用 block_matrix + LLL 求 kernel
- `recoverBinary` 用 `allones` 在 {-1,0,1} 上 greedy 拼出 binary basis
- AES IV = `sha256(str(int(sum(As)))).digest()[:16]`
- key = `'mylove_in_summer'`，解 flag。
