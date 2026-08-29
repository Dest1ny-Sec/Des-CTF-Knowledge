---
title: DownUnderCTF 2022 Writeups
contest: DownUnderCTF 2022
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [crypto, aes-ofb, rsa-interval-oracle, mongodb-nosqli, symlink, sqli-quine, ast-parse, compilerbot, python, php]
attack_chain:
  - ofb 加密：已知前缀+两次加密还原明文
  - rsa-interval-oracle-i: 区间预言机二分爆破
  - rsa-interval-oracle-ii: Manger 攻击
  - pay-to-win: 椭圆曲线阶利用multiplicative_order
  - mongo: NoSQL注入 n0sql1_is_th3_new_5qli
  - symlink web: 软链接读取/flag
  - sqli-quine: 自包含SQL注入
  - last-digit: CVE-2020-10735 hash长度截断
  - ast-parse: 编译错误信息泄露源码
  - compilerbot: 二分查找flag字符
key_payload: ofb ct2[i] XOR ct1[i+1] = pt2[i]  # 已知前缀还原
one_liner: DownUnderCTF 2022 14题writeup：OFB+RSA+NoSQL+Symlink+SQLi+Python
lesson: OFB可利用前缀+两次IV构造完整明文；RSA区间预言机二分
quality: high
---

# DownUnderCTF 2022 Writeups

## 题目信息
- 比赛：DownUnderCTF 2022
- 涵盖：14+ 道题

## 关键攻击链
### 1. ofb 加密
```python
def main():
    key = urandom(16)
    for _ in range(2):
        iv = bytes.fromhex(input('iv: '))
        aes = AES.new(key, iv=iv, mode=AES.MODE_OFB)
        ct = aes.encrypt(MESSAGE.encode())
        print(ct.hex())
```
- 利用：第 1 次 IV=0 加密 + 第 2 次 IV=prefix XOR ct1[0:16]
- 解：`pt2[i] = ct2[i] XOR ct1[i+1] XOR pt2[i-16]`
- flag: `DUCTF{0fb_mu5t_4ctu4lly_st4nd_f0r_0bvi0usly_f4ul7y_bl0ck_c1ph3r_m0d3_0f_0p3ra710n_7b9cb...}`

### 2. rsa-interval-oracle
- 区间预言机二分爆破
- Manger 攻击
- flag: `DUCTF{d1d_y0u_us3_b1n4ry_s34rch?}` / `DUCTF{Manger_w0uld_b3_pr0ud_0f_y0u}`

### 3. pay-to-win
- 椭圆曲线阶利用 `multiplicative_order`
- p-1 最大素因子 68 bits

### 4. mongo
- NoSQL 注入
- flag: `DUCTF{n0sql1_1s_th3_new_5qli}`

### 5. symlink web
- 软链接读取 /flag
- flag: `DUCTF{are_symlinks_really_worth_the_trouble_they_cause?????}`

### 6. sqli-quine
- 自包含 SQL 注入（参考 splitline My-CTF-Challenges）
- CHAR(0x61) || CHAR(0x62) 拼接
- flag: `DUCTF{alternative_solution_was_just_to_crack_the_hash_:p}`

### 7. last-digit
- CVE-2020-10735 hash 长度截断
- Python 3.10.7 修复

### 8. ast-parse
- 编译错误信息泄露源码
- flag: `DUCTF{next_time_ill_just_use_ast.parse}`

### 9. compilerbot
- 二分查找 flag 字符
- 参考 hxp-26c3-ctf
- flag: `DUCTF{pr3pr0c3ssOrPoWer3dPHPpEEk1ngPuzZLe_2b842b}`

## 评分
- quality: high（14+ 题完整 writeup + OFB 前缀还原 + RSA 区间二分）
