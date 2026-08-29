---
title: 第二届职工数字化应用技术技能大赛-数据安全管理员-线上技能大比武WriteUp
contest: 职工数字化应用技术技能大赛
year: 2025
difficulty: easy
vuln_type: crypto_rsa
tags: [数据安全,Cookie伪造,URL编码,符号替代,Base32魔改,XOR,key循环]
attack_chain: 数据泄露: 伪造auth cookie username=administrator&date=UTC时间戳+URL编码→访问index.php|数据混淆: 符号替代(!→1,@→2,#→3,$→4,%→5,^→6,&→7,*→8,(→9,)→0)→|数据脱敏: 自定义Base32字母表FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX+首字节^0x33+其余字节循环XOR key=37704cf0(8字节)→取第12行第2列
key_payload: cookie_value=quote_plus('username=administrator&date=2025-11-XX+0000&')|FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX|unxor: res[0] ^= 0x33; for i in range(1,len): res[i] ^= key[i & 7]
one_liner: 3道数据安全题,11名成绩,涵盖cookie伪造(username+date+URL编码)+符号替代密码表(!→1..)→0)+自定义Base32(32字母表)解码+首字节^0x33+8字节循环XOR key(37704cf0)
lesson: 1) 服务端可能只验证cookie中username+date而不验证签名,直接quote_plus伪造; 2) 符号替代密码本质是字符替换,优先级!@#$%^&*()对应1234567890; 3) 自定义Base32字母表(FNT5...)要识别反查索引; 4) XOR解密三层:首字节单值^0x33+其余循环XOR 8字节key; 5) 完整文件解密后需定位行+列(本例第12行第2列=865975201629227428)
quality: medium
---

## 备注

原文(https://www.ctfiot.com/281761.html)作者第一次以职工身份参加线上比武,总成绩11名,博客https://blog.csdn.net/Aluxian_。3道数据安全题均为解密/伪造类。

### 题目详情

**1. 数据泄露** — flag{5956462019654412}
- 服务端读取`$_COOKIE['auth']`,URL解码后检查`username=administrator&date=...`
- 构造cookie_value=quote_plus(f"username=administrator&date={utc_now()}&")
- 完整Python脚本使用requests.Session+headers伪装Cookie-Test/1.0

**3. 数据混淆** — flag{622622591307890225}
- 符号替代密码表:
  - ! → 1
  - @ → 2
  - # → 3
  - $ → 4
  - % → 5
  - ^ → 6
  - & → 7
  - * → 8
  - ( → 9
  - ) → 0
- 将题目中!@#$%^&*()序列按表替换成数字

**4. 数据脱敏** — flag{865975201629227428}
- 自定义Base32字母表:`FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX`(32个字符)
- 加密:先Base32编码→XOR
  - 首字节 ^= 0x33
  - 其余字节循环XOR key='37704cf0'(8字节,索引 i&7)
- 解密:b32_custom_decode → unxor
- 取第12行明文:`25813085410865975201629227428a7d1979@b9.com`
- 第2列(按空白/逗号分列):`865975201629227428`

## 评级

- **quality: medium** — 3道题payload完整,Python/C双脚本齐全,解密算法清晰(自定义Base32+双层XOR)
- **vuln_type: crypto_rsa** — 主分类用crypto_rsa兜底;实际是自定义Base32+XOR密码
- 数据脱敏类考题常考:符号替换、Base32魔改、XOR key循环
