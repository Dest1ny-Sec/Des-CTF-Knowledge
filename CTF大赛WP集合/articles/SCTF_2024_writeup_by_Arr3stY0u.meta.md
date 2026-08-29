---
title: SCTF 2024 writeup by Arr3stY0u
contest: SCTF 2024
year: 2024
difficulty: high
vuln_type: misc_unknown
tags: [iot-firmware, mips, aes-ecb, xor-0x66, tea-xor, lua-obfuscation, unluac, ptrace-anti-debug, pyinstaller, anything-permutation, s-box-substitution, lfsr-mt19937]
attack_chain:
  - IoT 1 Wlc_t0_the_wd_oF_IOT_s3cur: 魔改 AES + 字节 ROL1 + 异或链
  - 还原: flag[i] = ROR1(flag[i], 3) + flag[i] ^= flag[i+1] + flag[i] ^= 0xFF
  - AES ECB key=2E 35 7D 6A ED 44 F3 4D AD B9 11 34 13 EA 32 4E
  - flag: SCTF{Wlc_t0_the_wd_oF_IOT_s3cur}
  - IoT 2 SCTF{470b-a3e5c-9beb-60337-84ef2-5194d-aedc}: TEA 变种 + 12 uint32 加解密
  - DELTA=0x99C922E9 (实际 0x9E3779B9 取负) + ROUND=42
  - 异或 12 + 18 还原 v0/v1
  - Reverse Lua unluac 解混淆 (3a.lua + test_obf.luac)
  - lua opmap 重写 + unluac_2023_09_20.jar 解出 SGAME_3.luac
  - 源 lua 含 pctbbgf padding + bcdef TEA-like 加密 (DELTA=2576980377)
  - 还原 enc_flag=[12 uint32] + key={19088743,...} + arrrrrrrrrr
  - flag: SCTF{470b-a3e5c-9beb-60337-84ef2-5194d-aedc}
  - RE AES 异或 0x66 + 4 把子 key 切片: hey_syclover2024 / 2024hey_sycl / over2024hey_sycl / syclover2024hey_
  - flag: IHopeTheDebuggingProcessDidn1tTortureYouAndHopeYouHaveFunInSCTF!
  - RE bpftrace watchpoint 跟踪魔改异或 0x66 + go_memcmp 比对
  - RE TEA 加密 case 6 + verify + RC4 + 字节解析
  - 完整 Python 还原 + ARC4 解密 W0L000043MB541337
  - RE PyInstaller 解包 + Python 3.8 + PyNumber_Add/Subtract/And/Rshift/Index/Long/Lshift/TrueDivide/Xor
  - XXTea_Encrypt/Decrypt 5 rounds + DELTA 0x9E3779B9
  - key={83,'y',67,49,48,86,101,82,102,48,82,86,101,114}
  - flag: SCTF{w0w_y0U_wE1_kNOw_of_cYtH0N}
  - CRYPTO RSA + 反转 anything 函数 (双段 perfect + circle + rightCircle)
  - anything: 递归置换 + reverse(a, from1, to) 3 次
  - 100 次循环还原 flag
  - flag: SCTF{wshm56yt7ujhg}
  - CRYPTO Break: rev_crc + xor_num 40 + base64 字母表替换
  - string1="nopqrstDEFGHIJKLhijklUVQRST/WXYZabABCcdefgmuv6789+wxyz012345MNOP" -> standard
  - 还原: Y0u_@re_r1ght_r3ver53_is_easy!
  - CRYPTO RSA d=254 bit + (p^2+p+1)(q^2+q+1) = phi
  - Continued Fraction 攻击 e/(...) 求 d
  - solve p*q==N + (p^2+p+1)(q^2+q+1)==phi
  - md5(p) md5(q) 生成 flag
  - CRYPTO Permutation + Lattice + LLL 攻击
  - 25+100+1 x 100 矩阵 + mat.LLL() 还原 MP
  - AA * DPM.inverse() 还原 A + 65537 GF 域
key_payload: rev_crc + xor_num=[185,173,127,...] + str1.translate(str.maketrans(string1, string2))
one_liner: SCTF 2024 Arr3stY0u 多方向全 WP：IoT 魔改 AES+ROL1 + TEA 变种 + Lua unluac 解混淆 + Python PyInstaller XXTea + CRYPTO RSA 254-bit 攻击 + anything 置换 + Lattice LLL。
lesson: PyInstaller 包可解 Python 3.8 PyNumber_* 符号表 + unluac.jar + opmap.txt 是 Lua 字节码反编译标准工具；anything 置换函数 100 次循环还原是 Reverse 经典模式；Continued Fraction 攻击 254-bit d 配合 (p^2+p+1)(q^2+q+1)=phi 是特殊 RSA 还原关键。
quality: high
---
