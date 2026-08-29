---
title: 2024 L3HCTF writeup by Arr3stY0u
contest: L3HCTF
year: 2024
difficulty: hard
vuln_type: [lattice, ecdsa, reverse, crypto_rsa, block_cipher, aes]
tags: [格基规约, DSA nonce 复用, SPN 自定义分组密码, 32位XTEA 变种 delta=0x114514, Cyclotomic Polynomial 攻击, python bytecode 提取, AES-128-CBC]
attack_chain: 1. 格攻击 DSA LCG PRNG nonce：构造 15x15 矩阵 LLL 还原 sk / 2. 4 轮 SPN 自定义分组密码爆破密钥：2^24 候选 + sha256 比对 / 3. 32 位 XTEA 变种 delta=0x114514 还原 8 个 uint32 / 4. Cyclotomic Polynomial LLL 攻击 1024 阶多项式还原低 64 字节 / 5. Python bytecode regex 提取 LOAD_CONST 序列调用 solution 求 LCS / 6. AES-128-CBC 'secret' XOR + base64 解 / 7. H3C ppp chap cipher $c$3$ 解 IV/CT 拿密码 / 8. SHA512 顺序混编算 HASH / 9. IDA Python sub+stk2 弹栈指令 hook
key_payload: M = Matrix(RR,15,15) ; t = abs(LLL[0][:5]) ; 32-bit TEA delta=0x114514 ; Cyclotomic 1024 阶多项式 b=... s=... ; solution(['a', 'ba', 'ab', 'bc', 'cb', 'bda', 'bdca', 'bacd', 'bbbb', 'acdb', ...])
one_liner: LLL DSA LCG 还原 + SPN 密钥爆破 + XTEA 变种 + Cyclotomic LLL + bytecode LCS。
lesson: L3HCTF 风格偏论文题：DSA PRNG LLL / Cyclotomic 格基 / 自定义 SPN 都要懂。
quality: high
---
# 2024 L3HCTF writeup by Arr3stY0u

Arr3stY0u 队整理 9+ 题高质量 WP。

## 1. 线性同余 DSA nonce 攻击（格基规约）

DSA 签名的 nonce 由 LCG 生成：

```python
state = [1] + [randint(0, N) for i in range(t)]
new_state = sum([state[i] * c[i] for i in range(t+1)]) % N
```

构造 15x15 矩阵：

```python
q = 313199526393254794805899275326380083313
a = [258948702106389340127909287396807150259, ...]
RR = RationalField(256)
M = Matrix(RR, 15, 15)
for i in range(4):
    M[0, i] = a[i+1]
    M[i+1, i] = -a[0]
    M[5+i, i] = q
# ...
M[i, i+10] = 1
res = M.LLL()
```

LLL 第一行就是 t[] 的倍数。`gcd(t[3], t[1])` 约分，再 `(a[1] + e1) * invert(t[1], q) % q` 还原 sk。flag = `L3HSEC{ad4adc3d4b2001d0ddfa81e313cff80}`。

## 2. SPN 4 轮分组密码爆破

```python
Pbox = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
Sbox = [14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6]
# 4 轮 enc + 1 轮白化；密钥 32 bit
```

- base（24 bit）2^24 穷举 + 单 bit 触发加密 → 选 4 个 mask 收窄到 2^8
- aa（8 bit）2^8 穷举 → sha256(long_to_bytes(K)) 比对
- flag = `L3HCTF{852e3b2ae059c411ee14c7c460dcbaed483b3858cb680e10d211e256cf4b639e}`

## 3. 32 位 XTEA 变种（delta=0x114514）

```c
delta = 0x114514;
for (i = 0; i < 32; i++) {
    v0 += ((v1<<4 ^ v1>>5) + v1) ^ (sum + key[sum & 3]);
    sum += delta;
    v1 += ((v0<<4 ^ v0>>5) + v0) ^ (sum + key[(sum>>11) & 3]);
}
```

`decrypt` 反推，key 是题目给的 `{0x1cd43eea, 0x47d7cb70, 0xdbca5e98, 0x2b390c53}`，明文 → `L3HCTF{C0M_Th3C0d3_1s_FuN!!!!!!}`。

## 4. Cyclotomic Polynomial LLL 攻击

```python
q = 1219077173
N = 1024
b = 216047404*x^1023 + 1008199117*x^1022 + ...  # 1024 项
s = 735531500*x^1023 + 684755229*x^1022 + ...  # 1024 项
```

`M[0, 0:65] = b[::-1][:65]`, `M[1:65, 0:65] = s[::-1]` 构造 130x130 矩阵，LLL 后第一行低 64 字节就是 flag：

```
Y0u_R@411Y_Kn0w_CyclOtom1c_Poly!AK@Co!<J>^5#DQ}oDo=o(j7$%<1T8h1r
```

## 5. Python bytecode LCS 还原

正则 `.*?LOAD_CONST.*?\((.*?)\)` 提取 LOAD_CONST 参数 → `solution(args)` 求最长公共子序列 → `func2(n)` Fibonacci + `random.gauss(num2, 0.2)` → flag = `202817711117711x25763695063`。

## 6. AES-128-CBC + 静态密钥

```python
key = "secret"
enc = "JFYvMVU5QDoNQjomJlBULSQaCihTAFY="   # base64
enc_de = list(base64.b64decode(enc))
for i in range(len(enc_de)):
    enc_de[i] ^= ord(key[i % len(key)])
print(bytes(enc_de))
# W3LC0M3_n0_RU57_AnyM0r3
```

## 7. H3C ppp chap cipher 还原

```
$c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg==
```

取 IV (4C A6 09 5D...) + CT 反推 KEY。

## 8. SHA512 拼接顺序

```python
a = sha512()
a.update(unk[0x40:0x80])
a.update(unk[0x0:0x40])
a.update(unk[0x80:])
print(a.digest()[:0x20].hex())
```

## 9. IDA Python hook 弹栈指令

```python
# 4023AE sub
rbp = ida_dbg.get_reg_val('rbp')
stk2_addr = ida_bytes.get_qword(0x406050)
stk2_size = ida_bytes.get_dword(0x406050+8)
size = ida_bytes.get_byte(rbp-0x15C)
stk2_data = ida_bytes.get_bytes(stk2_addr+stk2_size-size*2, size*2)
if size == 4:
    v1, v2 = struct.unpack('<2I', stk2_data)
    v = (v1 - v2) & 0xFFFFFFFF
    print(f'0x{v1:08X}-0x{v2:08X}=0x{v:08X}')
```

hook 自定义虚拟机的 add/sub/xor 指令，导出每步操作还原算法。
