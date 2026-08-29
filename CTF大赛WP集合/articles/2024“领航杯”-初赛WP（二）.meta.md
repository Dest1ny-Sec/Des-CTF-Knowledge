---
title: 2024"领航杯"-初赛WP（二）
contest: 领航杯
year: 2024
difficulty: medium
vuln_type: [lattice, crypto_rsa, web_unknown, auth_bypass, misc_unknown]
tags: [RSA p^4+tp, Amm开方, 身份证号校验和, web sum字符密码, ACXI 注册绕过, AES加密]
attack_chain: 1. CRYPTO_Evaluate: p=p^4+tp (512-bit随机p+20-bit小扰动tp) → AMM 开方 (p^4 mod n) 拿 p / 2. MISC-veee: 1W 个身份证号 → 提取校验位不对的 → 转 ASCII → base64 隐写 / 3. WEB_ACXI_: 注册 test/123456 → 服务器加和 ord(c) 当 hash → 爆破 0x202f5 = 131829 → 多个 7 字符密码 sum 匹配 0x0202f5 → 绕过 admin 校验
key_payload: p, tp = genPrime()  # p^4 + tp 素数 ; AMM(p^4 mod n) 拿 p ; this_is_pwd_j71nas2 ; 0x202f5 = 131829 ; sum(ord(c) for c in 'test123456') = 0x2f5
one_liner: RSA p^4+tp AMM 开方 + 身份证校验和提取 + web sum 哈希碰撞。
lesson: p^4+tp 模数可对 p^4 用 AMM 开方求 p 候选；web 弱哈希常是 sum(ord) 单值校验。
quality: medium
---
# 2024"领航杯"-初赛WP（二）

## 1. CRYPTO_Evaluate

```python
def genPrime():
    while True:
        p = random.getrandbits(512)
        tp = random.getrandbits(20)
        if gmpy2.is_prime(p**4 + tp):
            return p**4 + tp, tp
p, tp = genPrime()
q, tq = genPrime()
m = bytes_to_long(flag)
e = 0x10001
n = p * q
c = pow(m, e, n)
print("n, e, c, tp, tq")
```

**p^4 + tp 形式**：p 是 512-bit 随机数，tp 20-bit 小扰动。

**思路**：
- 计算 `p^4 mod n` → 在 F_p 上 `x = p^4` 的 4 次根是 ±p
- **AMM 算法**（Adleman-Manders-Miller）求 4 次原根
- 多个候选 p → 验证 n % p == 0

> 实际需要更精细分析：p^4 mod n 在 F_n 上不是单根，先 modulo p 再 AMM。

## 2. MISC-veee（身份证号校验和）

```python
class IdNumber(str):
    def get_check_digit(self):
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17-i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'
    @classmethod
    def verify_id(cls, id_number):
        if re.match(const.ID_NUMBER_18_REGEX, id_number):
            return str(cls(id_number).get_check_digit()) == id_number[-1]
        return bool(re.match(const.ID_NUMBER_15_REGEX, id_number))
```

遍历 sfz.txt 每行校验，最后一位不对的就是隐藏的 ASCII → 拼成 hex → base64 → `this_is_pwd_j71nas2`。

## 3. WEB_ACXI_

```python
# 注册 test/123456 → 提示需 admin 拿 flag
hex(773094245109) = 0xb4000202f5
hex(244813267701) = 0x39000202f5
# sum(ord(c) for c in 'test123456') = 0x2f5
# 服务器校验：sum(ord(c)) == 0x202f5 ?
```

爆破 7 字符密码让 sum 匹配 `0x0202f5`：
```python
hix = 0
for c in 'test1234567': hix += ord(c)
# 0x32c
```

找到密码使和为 `0x0202f5` → XOR `0x01????` 拿 admin。
