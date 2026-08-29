---
title: Beating the kCTF PoW with AVX-512 IFMA for $51k
contest: kCTF
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [kCTF PoW, Mersenne 2^1279-1, 1277平方, 7337迭代, GMP, mpz_mul + mpz_mod_2exp, AVX-512 IFMA, vpmadd52luq, vpmadd52huq, 25个52-bit limbs, _mm512_mask_madd52lo_epu64, _mm512_madd52hi_epu64, $21,337 base + $10,000 stability + $20,000 0-day]
attack_chain:
  - sloth_root: 1277 次 x^2 % (2^1279-1) + 翻转 LSB, difficulty=7337
  - Mersenne 模运算: (x & p) + (x >> 1279), if r >= p: r -= p
  - GMP 实现: mpz_mul + mpz_mod_2exp(low) + mpz_fdiv_q_2exp(high) + mpz_add
  - GMP Rust 2.4 秒 vs C++ 略快
  - AVX-512 IFMA: vpmadd52luq 52-bit multiply-add
  - 25 个 52-bit limbs (1279/52 ≈ 24.6)
  - 7 个 __m512i accumulators, 滑动窗口 i ∈ [-7, 24]
  - _mm512_mask_madd52lo_epu64 + _mm512_mask_madd52hi_epu64
  - carry 处理: 4 段 accum, carry = srli 52, carry_into = alignr_epi64
  - 测试 cmp = bit_1279 检查 >= 2^1279-1
key_payload: 'sloth_root difficulty=7337 / Mersenne 2^1279-1 / mpz_mod_mersenne / AVX-512 IFMA vpmadd52luq / 25 52-bit limbs / 7 accumulators 滑动窗口 / carry2 循环'
one_liner: kCTF PoW 51k 美元奖金 — Mersenne 2^1279-1 模 + 1277 平方 + 7337 迭代 + AVX-512 IFMA vpmadd52luq + 25 个 52-bit limbs + 7 个 zmm accumulators 滑动窗口爆破。
lesson: kCTF PoW 是 Memory-hard 算法 (Mersenne 模乘),AVX-512 IFMA 52-bit 乘加是加速核心;滑动窗口 + carry propagation 是大数乘法模板。
quality: high
---

# Beating the kCTF PoW with AVX-512 IFMA for $51k

## 速读
kCTF PoW 利用 AVX-512 IFMA 指令打 Mersenne 模乘 — 5.1 万美元奖金题解。

## 奖金结构
- $21,337 base reward
- $10,000 stability (>90% runs)
- $20,000 0-day bug

## sloth_root 算法
```python
def sloth_root(x, difficulty=7337):
    for i in range(difficulty):
        for j in range(1277):  # 平方 1277 次
            x = (x * x) % (2 ** 1279 - 1)  # Mersenne 模
        x = x.bit_flip(0)  # 翻转 LSB
    return int(x)
```

## GMP 实现
```cpp
constexpr int MERSENNE_EXP = 1279;
mpz_t low, high, p;

void mpz_mod_mersenne(mpz_t r, const mpz_t x) {
    mpz_mod_2exp(low, x, MERSENNE_EXP);
    mpz_fdiv_q_2exp(high, x, MERSENNE_EXP);
    mpz_add(r, low, high);
    if (mpz_cmp(r, p) >= 0) mpz_sub(r, r, p);
}

void the_powmod(mpz_t x) {
    for (int i = 0; i < 1277; ++i) {
        mpz_mul(x, x, x);
        mpz_mod_mersenne(x, x);
    }
}
```

## AVX-512 IFMA
- 25 个 52-bit limbs (1279 / 52 ≈ 24.6)
- 7 个 __m512i accumulators
- `_mm512_mask_madd52lo_epu64` / `_mm512_mask_madd52hi_epu64`
- 滑动窗口 i ∈ [-7, 24]
- carry 处理: 4 段, `_mm512_alignr_epi64`, `_mm512_srli_epi64` 52
- `cmp = bit_1279` 测试 >= 2^1279-1
