---
title: 春秋杯WP | 2024春秋杯冬季赛第一天题目部分解析
contest: 春秋杯2024冬季赛
year: 2024
difficulty: medium
vuln_type: reverse
tags: [魔改XTEA, custom_md5, Franklin-Reiter, Coppersmith, lcm公倍数, polynomial ring, flag格式]
attack_chain: EzRSA/ez_vm/ezre/RSA1/Gender_Simulation/Gotar六题混合解析→ez_vm手撕VM识别魔改XTEA(delta=0x20252025,右移6,异或0x42,异或3)→RSA1 Franklin-Reiter + Coppersmith解e→联立方程gcm解m1
key_payload: "decipher(32, m, key={2,0,2,5});v[10]={0x83845981,...};delta=0x20252025;xtea var:((v1<<4)^(v1>>6)^0x42)+v1;Coppersmith X=2^128 beta=1 epsilon=0.05;flag{e8ff1a85-5ccd-4171-9f2a-ce6eea614a54};flag{b799eb3a-59ee-4b3b-b49d-39080fc23e99}"
one_liner: 春秋杯2024冬季赛D1六题混合：ez_vm魔改XTEA+ezre custom_md5+RSA1 Franklin-Reiter+Coppersmith
lesson: 魔改XTEA常通过改delta/移位位数/异或常数实现；RSA Franklin-Reiter可联立Coppersmith解高位
quality: high
---

# 春秋杯WP | 2024春秋杯冬季赛第一天题目部分解析

**赛事**：春秋杯2024冬季赛 Day 1

**包含题目**：EzRSA / ez_vm / ezre / RSA1 / Gender_Simulation / Gotar

**关键题目解析**：

**1. ez_vm（魔改XTEA + VM）**
- 手撕VM识别为XTEA变种
- 特征：delta=0x20252025，移位右移6位（非常规5位），异或0x42，末轮再异或3
- Key: `{2, 0, 2, 5}`
- 密文：10个uint32数组
- 256字节S盒做字节替换
- flag: `flag{e8ff1a85-5ccd-4171-9f2a-ce6eea614a54}`

**2. ezre（custom_md5 + 异或）**
- custom_md5_init计算从该函数向后1024字节的MD5
- MD5作为伪随机数种子 → 生成key流
- 密文与key流异或
- flag: `flag{b799eb3a-59ee-4b3b-b49d-39080fc23e99}`

**3. RSA1（Franklin-Reiter + Coppersmith + lcm公倍数）**
- m1 = bytes_to_long(flag)
- m2 = bytes_to_long(''.join(chr((ord(i)+3) % 128) for i in flag.decode()).encode())
- 特殊处理：flag末尾'}' ascii=125 + 3 mod 128 = 0
- 联立c2^7 - (c3-x)^5 = 0 (因lcm(2025,2835)=14175, 2025*7=2835*5)
- Coppersmith解e: `f.small_roots(X=2**128, beta=1, epsilon=0.05)`
- 求e后用Franklin-Reiter联立c1和c2解m1
- flag格式：`flag{<uuid>}` 后接大素数二进制

**4. 其他题（EzRSA / Gender_Simulation / Gotar）**：
- EzRSA / Gender_Simulation / Gotar 在本WP中未详细展开解析

**技术总结**：
- 魔改XTEA常见改动：delta值、右移位数、末轮异或常数
- RSA Franklin-Reiter + Coppersmith组合解e未知
- lcm(2025,2835)=14175 → 7和5倍互相替换

**质量评估**：高（多题payload + flag）
