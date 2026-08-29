---
title: 赛题复现:2022-CryptoCTF(一)
contest: CryptoCTF 2022
year: 2022
difficulty: medium
vuln_type: misc_math
tags: [congruence, modular-arith, AES-CBC, known-plaintext, 3DES-MITM, rsa-multi-prime, DLP, RsaCtfTool, Winedemic, differential-cryptanalysis, Sage, sympy]
attack_chain:
- Klamkin (Congruence): 已知(ax+by)%q=0对任意(ar+bs)%q=0成立,求(x,y)满足y是12-bit
- 设x或y为getPrime(n),另一个由inverse计算
- 交互式脚本:循环G/S选项+逆元算x或y
- flag: CCTF{f1nDin9_In7Eg3R_50Lut1Ons_iZ_in73rEStIn9!}
- Baphomet: 已知明文攻击,AES密钥在文件中,plain.txt+cipher.txt+key恢复
- 多题涵盖Congruence+逆向数学题+3DES meet-in-the-middle+RSA多素数攻击
key_payload: CCTF{f1nDin9_In7Eg3R_50Lut1Ons_iZ_in73rEStIn9!}
one_liner: 2022 CryptoCTF复现第一部分,涵盖Congruence同余式+AES已知明文攻击+3DES meet-in-the-middle+RSA多素数等经典密码学考点。
lesson: 任何(a,b)满足(ar+bs)%q=0时(ax+by)%q=0都成立,说明(x,y)与(r,s)同余,可设x或y为getPrime(n)然后inverse算另一个;CCTF的题多覆盖经典数学密码学。
quality: high
---

## 题目列表

第一部分easy和medium-easy难度:
1. Mic-Check (签到)
2. Klamkin (Congruence)
3. Baphomet (已知明文攻击)
+ 其他多题(3DES MITM/RSA多素数/DLP/Winedemic/differential cryptanalysis等)

## 关键考点

### Mic-Check
- 签到:Can you hear me?
- flag: CCTF{Th3_B3sT_1S_Yet_t0_C0m3!!}

### Klamkin
- 已知(ax + by) % q = 0 对任意(ar + bs) % q = 0
- 关键洞察:(x, y)与(r, s)同余
- 解题:
  1. 设x = getPrime(n) (n从题面读)
  2. y = -a*x*inverse(b, q) % q
  3. 验证 (a*x + b*y) % q == 0
  4. 根据题面要求定x或y的位长度
- 交互式:
  ```python
  sh.recvuntil("[Q]uit")
  sh.sendline("G")
  q = int(...)
  r = int(...)
  s = int(...)
  sh.sendline("S")
  while True:
      a = inverse(r, q)
      b = inverse(-s, q)
      ch = sh.recvuntil("bit: \n").split(b" ")
      if ch[-4] == b"x":
          x(int(ch[-2][:2]))
      else:
          y(int(ch[-2][:2]))
  ```
- flag: CCTF{f1nDin9_In7Eg3R_50Lut1Ons_iZ_in73rEStIn9!}

### Baphomet
- 已知明文攻击
- 提供plain.txt+cipher.txt+key文件
- AES-CBC解密

### 其他经典考点
- 3DES meet-in-the-middle
- RSA多素数攻击(Wiener/Boneh-Durfee)
- DLP(Discrete Logarithm Problem)
- Winedemic
- Differential Cryptanalysis(差分分析)
- Sage/sympy辅助

## 实战价值
- CryptoCTF是密码学专项比赛,质量顶级
- Congruence类题用Sage的modular inverse+getPrime是常用技巧
- 已知明文攻击工具:Bash在线AES解密
- 3DES MITM:Birthday attack空间减半
- RSA多素数:Wiener/Boneh-Durfee/RsaCtfTool/yafu
- 差分分析:DPA/模板攻击的密码学基础
