---
title: SCTF 2024 Writeup - XMCVE-Polaris 战队第 8 名
contest: SCTF 2024
year: 2024
difficulty: high
vuln_type: pwn_unknown
tags: [pwn, go-uaf, tcache-hijack, arm-rev, tea-rc4, anything-transform, rust-reflection, p-q-recovery, dual-rsa, small-roots-lattice]
attack_chain:
  - PWN: Go binary 4 函数 new_user/show_user/delete_user + 后门
  - UAF 漏洞: 劫持 tcache 为堆地址 → show_user 越界读
  - 泄 puts 地址 + 利用后门函数 system("/bin/sh")
  - 关键: show_user 读 [rax+0x100] (user content) + [rbx+0x10C] (length)
  - REVERSE Uds: ARM 架构 + TEA + RC4 + 字节序转换
  - sub_810004C 解析压缩输入 (4 bit count) + 0 byte padding
  - sub_8104CA8_1 标准 TEA 加解密 (delta=0x61C88647 实际 0x9E3779B9)
  - RC4 key=[0x60,0x4a,0x8a,0x6e,0x9d,0xac,0xb1,0x67] 解密
  - Crypto Signin: 隐藏 phi = (p^2+p+1)*(q^2+q+1) 与 e 量级约 2n 推断
  - small_roots LLL (2^496, 2^400) m=2 d=3 找 p+q 偏移
  - phi = p^4*(p-1)*q*(q-1) → d = inverse(e, phi) → 解密
  - Crypto Whisper: Dual RSA 同 e 不同 n 攻击 (Liqiang et al.)
  - 解析两个 cert1.pem + cert2.pem 提取 n1, n2
  - 关键参数 345 bit 推测是 d
  - LLL + small roots + dual_rsa_liqiang_et_al
  - 实战 exp: cert1/cert2 ASN.1 DER 提取 modulus
  - flag: SCTF{0ne_4rgum3nt_1s_r0tt3n_0r4ng3s,_th3_wh0le_cert1fic4t3_1s_r0tt3n_0r4ng3s:XD}
key_payload: small_roots(f, (2^496, 2^400), m=2, d=3) + dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt)
one_liner: SCTF 2024 XMCVE-Polaris 第 8 名 (PWN Go UAF + REV ARM TEA/RC4 + Crypto 隐藏 phi Coppersmith + Dual RSA 同 e 不同 n) 多方向全 WP。
lesson: Go UAF 劫持 tcache 改 show_user 指针是 Go 漏洞经典模式；TEA 实际 delta 0x61C88647 是 -(0x9E3779B9) 的 32-bit 表示；Coppersmith small_roots 是大整数 p+q 偏移恢复关键；Dual RSA 同 e 不同 n 用 LLL+unravelled linearization 攻击。
quality: high
---
