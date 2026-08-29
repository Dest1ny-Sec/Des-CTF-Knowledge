---
title: 2024 KCTF 大赛 - 第五题《废弃星球》设计思路及解析
contest: KCTF大赛
year: 2024
difficulty: hard
vuln_type: [crypto_rsa, ecdsa, misc_unknown, reverse]
tags: [BF-IBE, BLS12-381, IBE身份加密, HMAC伪碰撞, 子群攻击, Pohlig-Hellman, Rust逆向, pairing-ce]
attack_chain: Rust 逆向 + pairing-ce 库 → 找到 BF-IBE 标准实现 → HMAC 伪碰撞 admin@pubkey.com + \x00 等同私钥 → 拿到 admin 凭证 → blind_recovery 输入自定义 x 坐标 → 服务端未校验 256-bit 素数阶子群 → 选光滑子群 64-bit Pohlig-Hellman 爆破 d 模 64bit → 三次 reset_system(mul) 重置 PKG 私钥 d → LSB Leak 类比 RSA-LSB 拼多组方程恢复 d → 拿 flag
key_payload: admin@pubkey.com\x00 ; uname as HMAC key blocksize 64 pad equivalence ; E.order() = 3 * 11^2 * 10177^2 * 859267^2 * 52437899^2 * 52435875175126190479447740508185965837690552500527637822603658699938581184513
one_liner: BF-IBE + HMAC 密钥等价伪碰撞 + BLS12-381 光滑子群攻击 + LSB 多次 reset 拼方程。
lesson: IBE 类题目三大套路：HMAC 密钥块长等价、BLS 子群未校验、Pohlig-Hellman 光滑子群爆破。
quality: high
---
# 2024 KCTF 大赛 - 第五题《废弃星球》设计思路及解析

**出题战队 98k · 设计 tl2cents · 0 队提交**

## 题目架构

- 远程 docker + 附件（Rust 源码 + 编译产物）
- IBE 邮件注册 / 登录 / 恢复，密码学核心是 **BF-IBE on BLS12-381**
- 漏洞 1：**HMAC 伪碰撞** + 漏洞 2：**BLS12-381 子群攻击** + 漏洞 3：**LSB Leak Oracle**

## 漏洞 1：HMAC 伪碰撞拿 admin

```rust
pub fn hmac2g1<T>(msg: &str, pk: &T) -> G1Affine where T: Hashable {
    let data = pk.hash();
    let mut keyed_hmac = <HmacFunc as Mac>::new_from_slice(msg.as_bytes()).unwrap();
    keyed_hmac.update(&data);
    let result = keyed_hmac.finalize().into_bytes();
    let x = BigUint::from_bytes_be(result);
    let xr = Fr::from_str(&x.to_string()).unwrap();
    G1::one().into_affine().mul(xr).into_affine()
}
```

`uname` 作为 HMAC 密钥，长度 ≠ 64 字节（SHA256 blocksize）时，HMAC 内部 pad 处理：

> `admin@pubkey.com` + `admin@pubkey.com\x00` 生成的 HMAC 等价
> → 注册 `admin@pubkey.com\x00` 拿到与 `admin@pubkey.com` 相同的私钥

## 漏洞 2：BLS12-381 光滑子群

```python
p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
E = EllipticCurve(GF(p), (0, 4))
G = E(0x17F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB, 0x08B3F481E3AAA0F1A09E30ED741D8AE4FCF5E095D5D00AF600DB18CB2C04B3EDD03CC744A2888AE40CAA232946C5E7E1)
# E.set_order(...) ; factor(E.order())
# 3 * 11^2 * 10177^2 * 859267^2 * 52437899^2 * 52435875175126190479447740508185965837690552500527637822603658699938581184513
```

curve order 存在光滑子群，最大光滑子群 64 比特（Pohlig-Hellman 爆破）。

```rust
pub fn make_key_blind(&self, x: Fq) -> Option<PrivateKey> {
    if let Some(g) = get_point_from_x(x, false) {
        Some(PrivateKey::new(self.pk, g.mul(self.x).into_affine()))
    } else { None }
}
fn blind_recovery(&self, x: Fq) -> Option<Hash> {
    if let Some(sk) = self.pkg.make_key_blind(x) {
        Some(sk.gx.hash())  // 只返回哈希
    } else { None }
}
```

- `admin blind_recovery(x)` 接受用户输入的 x 坐标
- 服务端只检查点是否在曲线上，没校验是否在 256-bit 素数阶子群
- 选 64-bit 光滑子群的生成元作为 x → 3 次爆破恢复 `d mod 64bit`

## 漏洞 3：LSB Leak

```rust
fn reset_system(&mut self, mul: &Fr) -> Option<bool> {
    if mul == &Fr::from_str("1").unwrap() || mul == &Fr::from_str("0").unwrap() {
        return Some(false);
    }
    let mut super_x = self.pkg.x.clone();
    super_x.mul_assign(mul);
    let pkg = PKG::new(super_x);  // 新私钥 = 旧私钥 * mul
    ...
}
```

- `reset_system(m)` 重置 PKG 私钥为 `d * m`
- 类比 RSA-LSB-Leak，d 的 p 进制展开各位可恢复
- 多次 reset 拼方程 → 完整恢复 d
- 拿到 d 后用 IBE 私钥解 admin 邮件 → 拿 flag

## 攻击链总结

1. **Phase 1**：注册 `admin@pubkey.com\x00` → HMAC 伪碰撞拿到 admin 私钥
2. **Phase 2**：调用 `blind_recovery` 选光滑子群生成元 → Pohlig-Hellman 拆 64 比特
3. **Phase 3**：多次 `reset_system(mul)` 拼 LSB 方程组恢复完整 d
4. **Phase 4**：用 d 解密 admin 凭证 → 拿 flag

> 完整 exp 见 `cargo run --release`，源码 `challenge-src.zip`。
