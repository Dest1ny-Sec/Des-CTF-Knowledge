---
title: NewstarCTF 2025 Week1 REVERSE 全解 WP
contest: NewstarCTF 2025 Week1
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags:
- reverse
- custom-base64
- xorshift
- two-stage-xor
- android
- apk
- aes-ecb
- pwntools-flag
attack_chain:
- '题目 1 Easy_Encrypt: 自定义 base64 字母表 HElLo!A=CrQzy-B4S3|is''waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF'
- 目标密文 T>6uTqOatL39aP!YIqruyv(YBA!8y7ouCa9=
- 还原 flag{Wh4t_a_cra2y_8as3!!!}
- '题目 2 EzAndroid: APK 中 base64 + AES-ECB k=b"1145141919810000'
- base64.b64decode("cTz2pDhl8fRMfkkJXfqs2t8JBsqLkvQZDLYpWjEtkLE=")
- 去除 PKCS#7 填充得 flag{@_g00d_st@r7_f0r_ANDROID}
- '题目 3 It3_debug: ptrace 反调试 + 双层 XOR'
- 第一层 v5=[0x13,0x13,0x51] 循环 XOR
- 第二层按 i%3 分 0x14/0x11/0x45 XOR
- flag{It3_D3bugG_T11me!_le3_play}
- '题目 4 Jigsaw: 三段拼接 Do_Y0u_ + 1e_Gam3 + Like_7his_Jig'
- part3 [0xDE,0xED,0xDA,0xF2,0xDD,0xD8,0xD7,0xD7] XOR 0xAD = s@w_puzz
- flag{Do_Y0u_Like_7his_Jigs@w_puzz1e_Gam3}
- '题目 5 XOR: strcmp "anu`ym7wKLl$P]v3q%D]lHpi" + 双层 XOR'
- 还原 flag{y0u_Kn0W_b4s1C_xOr}
key_payload: alpha="HElLo!A=CrQzy-B4S3|is'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF" + v5=[0x13,0x13,0x51]
one_liner: NewstarCTF 2025 Week1 Reverse 全解 (5 题)：自定义 base64 + AES-ECB Android + 双层 XOR + jigsaw 拼接 + 基础 XOR。
lesson: 自定义 base64 字母表逆向关键看 alpha 数组；AES-ECB 单密钥无需 IV；双层 XOR 先反 v5 循环再反 i%3 分组；jigsaw 题把 flag 分 3 段算 Xor 拼接。
quality: high
full_path: NewstarCTF2025-Week1-REVERSE全解wp.full.md
meta_path: NewstarCTF2025-Week1-REVERSE全解wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'NewstarCTF 2025 Week1 REVERSE 全解 WP。NewstarCTF 2025 Week1 Reverse 全解 (5 题)：自定义 base64 + AES-ECB Android + 双层 XOR + jigsaw 拼接 + 基础 XOR。。关键路径：题目 1 Easy_Encrypt: 自定义 base64 字母表 HElLo!A=CrQzy-B4S3|is''w...'
category: misc
subcategory: misc_other
tools_used:
- pwntools
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/300688.html
reasoning_chain:
- Easy_Encrypt 题 → 触发点：自定义 base64 字母表 HElLo!A=CrQzy-B4S3|is'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF
- 目标密文 T>6uTqOatL39aP!YIqruyv(YBA!8y7ouCa9= → 假设：base64 逆 + XOR
- 动作：逆向 XOR v5=[0x13,0x13,0x51] 循环 → 观察：得到字母表索引
- 再 base64 解码 → 观察：flag{Wh4t_a_cra2y_8as3!!!}
- EzAndroid 题：APK 中 base64 + AES-ECB k='1145141919810000' → 触发点：硬编码 key
- 动作：base64.b64decode('cTz2pDhl8fRMfkkJXfqs2t8JBsqLkvQZDLYpWjEtkLE=') → 观察：去掉 PKCS#7 填充
- flag{@_g00d_st@r7_f0r_ANDROID}
- It3_debug 题 → 触发点：ptrace 反调试 + 双层 XOR
- 动作：第一层 v5=[0x13,0x13,0x51] 循环 XOR → 第二层 i%3 分 0x14/0x11/0x45 XOR
- Jigsaw 题 → 触发点：三段拼接 Do_Y0u_ + 1e_Gam3 + Like_7his_Jig
- part3 [0xDE,0xED,...] XOR 0xAD → 动作：解出 s@w_puzz → flag{Do_Y0u_Like_7his_Jigs@w_puzz1e_Gam3}
- XOR 题：strcmp 双层 XOR → 先逆外层再逆内层 → 观察：flag{y0u_Kn0W_b4s1C_xOr}
failed_attempts:
- 试图不解 v5 循环直接 base64 解 → 失败：明文先被 XOR
- AES-ECB 不去 PKCS#7 填充 → 失败：填充字节污染明文
- Jigsaw 不解 part3 硬拼 → 失败：part3 单独 XOR 0xAD
key_observations:
- 自定义 base64 字母表逆向看 alpha[] 数组
- AES-ECB 单密钥无需 IV
- 双层 XOR 先反 v5 循环再反 i%3 分组
- Jigsaw 题 flag 分 3 段分别算 XOR
- ptrace 反调试 + 双层 XOR 是入门 RE 套路
prerequisites:
- Base64 编码原理 + 自定义字母表
- AES-ECB + PKCS#7 填充
- XOR 加密与循环 key
- Android APK + jadx 反编译
---
# NewstarCTF2025-Week1-REVERSE全解wp

> 原文: https://www.ctfiot.com/300688.html
> ID: 300688

NewstarCTF2025也是结束好久了，到现在才发的原因是比较懒，另外就是PicGO抽疯，图片上传不到图床，现在用gitee作图床好多了

最终排名是第三，主方向是逆向，可惜最后有两道没解出来，不然re是全解，后续也会发其他方向的

week1全解

读取输入 Str。

用一个自定义字母表做 Base64 编码：base64_encode(Str, Buf1, strlen(Str))。

把结果和常量串 Buf2 = "T>6uTqOatL39aP!YIqruyv(YBA!8y7ouCa9=" 比较，完全一致就通过。

先对目标串 c 逆向第二步（再 XOR 一次 v5）。

再对结果逆向第一步（根据位置还原原 flag）。


```
Do_Y0u_
1e_Gam3
Like_7his_Jig
part3 = [0xDE, 0xED, 0xDA, 0xF2, 0xDD, 0xD8, 0xD7, 0xD7, 0x00]
v2 = 8
flag_part3 = [x ^ 0xAD for x in part3[:v2]]
print(''.join(map(chr, flag_part3)))
s@w_puzz
flag{Do_Y0u_Like_7his_Jigs@w_puzz1e_Gam3}
aHelloACrqzyB4s db 'HElLo!A=CrQzy-B4S3|is',27h,'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXV'
db 'KJNMF',0
HElLo!A=CrQzy-B4S3|is'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF
def decode_custom_base64(s, alpha):
    idx = {ch: i for i, ch in enumerate(alpha)}
    out = bytearray()
    i = 0
    while i < len(s):
        c0, c1, c2, c3 = s[i:i+4]; i += 4
        a = idx[c0]; b = idx[c1]
        if c2 == '=':
            out.append(((a << 2) | (b >> 4)) & 0xFF)
            break
        c = idx[c2]
        if c3 == '=':
            out += bytes([
                ((a << 2) | (b >> 4)) & 0xFF,
                (((b & 0xF) << 4) | (c >> 2)) & 0xFF,
            ])
            break
        d = idx[c3]
        out += bytes([
            ((a << 2) | (b >> 4)) & 0xFF,
            (((b & 0xF) << 4) | (c >> 2)) & 0xFF,
            (((c & 0x3) << 6) | d) & 0xFF,
        ])
    return bytes(out)

alpha = "HElLo!A=CrQzy-B4S3|is'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF"
buf2  = "T>6uTqOatL39aP!YIqruyv(YBA!8y7ouCa9="
print(decode_custom_base64(buf2, alpha).decode())
flag{Wh4t_a_cra2y_8as3!!!}
from Crypto.Cipher import AES
import base64
ct = base64.b64decode("cTz2pDhl8fRMfkkJXfqs2t8JBsqLkvQZDLYpWjEtkLE=")
k = b"1145141919810000"
pt = AES.new(k, AES.MODE_ECB).decrypt(ct)
# 去除 PKCS#7 填充
pt = pt[:-pt[-1]]
print(pt.decode())
flag{@_g00d_st@r7_f0r_ANDROID}
flag{It3_D3bugG_T11me!_le3_play}
for ( i = 0; i < v7; ++i )
  if ( i % 3 == 0 )      Str[i] ^= 0x14;
  else if ( i % 3 == 1 ) Str[i] ^= 0x11;
  else                   Str[i] ^= 0x45;
v5[0]=19; v5[1]=19; v5[2]=81;     // 即 0x13, 0x13, 0x51
for ( j = 0; j < v7; ++j )
  Str[j] ^= v5[j % 3];
strcpy(Str2, "anu`ym7wKLl$P]v3q%D]lHpi");
if (!strcmp(Str, Str2)) …
v5 = [19, 19, 81]
c = "anu`ym7wKLl$P]v3q%D]lHpi"
v7 = len(c)

tmp = [ord(c[i]) ^ v5[i % 3] for i in range(v7)]

flag_chars = []
for i in range(v7):
    if i % 3 == 0:
        flag_chars.append(chr(tmp[i] ^ 0x14))
    elif i % 3 == 1:
        flag_chars.append(chr(tmp[i] ^ 0x11))
    else:
        flag_chars.append(chr(tmp[i] ^ 0x45))

flag = "".join(flag_chars)
print(flag)
flag{y0u_Kn0W_b4s1C_xOr}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]