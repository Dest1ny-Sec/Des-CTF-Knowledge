---
title: 看雪2022 KCTF 春季赛 | 第12题设计思路及解析
contest: 看雪2022 KCTF春季赛
year: 2022
difficulty: hard
vuln_type: lattice
tags: [自定义MD5, LWE问题, MT19937爆破seed, 矩阵乘法mod 127, 增广格构造, 多空间分层]
attack_chain: MT19937爆破K1/K2 seed→生成s0/s1/s2矩阵→A*l+A*r1+29*err1=ans1 mod 127 + B*l+B*r2+29*err2=ans2 mod 127 LWE→增广格构造3空间（lr+err+约束）→LLL求解
key_payload: "init_genrand(0x91941ABB) seed爆破;A*l mod 127;LLL增广格64*2+48+1维;ANS[i][-1] in {127, -127};flag=7032240d5e5a1d0e021c04656d2b7c4c"
one_liner: KCTF2022春Q12《尊严之战》：MT19937+自定义MD5+LWE矩阵乘mod 127+增广LLL格密码
lesson: LWE问题可构造增广格分层（err严格0/1，lr宽0-126），权重L=M^2+结果向量留痕
quality: high
---

# 看雪2022 KCTF 春季赛 | 第12题设计思路及解析

**赛事**：看雪2022 KCTF春季赛 Q12《尊严之战》

**难度**：仅3队成功提交flag

**flag**：`kctf{7032240d5e5a1d0e021c04656d2b7c4c}`

**题目设计**：
- 自定义MD5
- 缺陷的格密码理论LWE问题
- 必须在输入flag且在合适时间内输出"一模一样"的格子
- 给出2组由flag生成的矩阵，看似随机但可恢复flag

**逆向算法**：
```c
// 32x32矩阵乘法
int s0[1024];  // 32x32=1024 随机数
int s1[32] = {FLAG[0..15], rand[16..31]};  // 前16=flag
int s2[32] = {(rand&1)*29};  // 0或29
int sA[32] = {0};
for(int i=0; i<32; i++) {
    int s = 0;
    for(int j=0; j<32; j++) {
        s += s1[j] * s0[32*i+j];
    }
    sA[i] = (s + s2[i]) % 0x7f;
}
```

**LWE问题构造**：
- A,B为已知32x32矩阵
- l = [flag(16), 0(16)]
- r1, r2 = [0(16), rand(16)]
- err1, err2 = [rand(0或1) * 29] * 32
- `A*l + A*r1 + 29*err1 = ans1 mod 127`
- `B*l + B*r2 + 29*err2 = ans2 mod 127`

**MT19937 seed爆破**：
```c
for (K = 0xffffffff; K >= 0x1; K--) {
    init_genrand(K);
    char s[8] = {0};
    for (int i = 0; i < 8; i++) s[i] = genNumber();
    if (memcmp(s, A1, 8) == 0) printf("A1:%x\n", K);
    if (memcmp(s, A2, 8) == 0) printf("A2:%x\n", K);
}
```

**增广LLL格构造**（3空间分层）：
```sage
MK1 = Matrix(ZZ, 64*2+48+1, 64*2+48+1)
# 对角：原空间 + err空间 + 标识
for i in range(64): MK1[i,i] = 127^5  # 原空间大权重
for i in range(48): MK1[i+64+48, i+64+48] = 127^2 * 2  # err空间
for i in range(48): MK1[i+64+48, i] = 29 * 127^4  # err耦合
# A/B矩阵转置×127^4
for i in range(16):
    for j in range(32):
        MK1[i+64, j] = ZZ(A[j,i]) * 127^4
        MK1[i+64, j+32] = ZZ(B[j,i]) * 127^4
        MK1[i+64+16, j] = ZZ(A[j,i+16]) * 127^4
        MK1[i+64+32, j+32] = ZZ(B[j,i+16]) * 127^4
# 单位矩阵
for i in range(48): MK1[i+64, i+64] = 1
# 标识行：结果向量
MK1[-1, -65:-1] = vector([127*127]*64)
MK1[-1, :64] = vector(ZZ, ans1+ans2) * 127^4
MK1[-1, -1] = 127
ANS = MK1.LLL()
```

**求解**：
- 找最后一列绝对值为t=sqrt(127^2)=127的结果
- 第二部分绝对值均为L的值即为合法解
- 前16位 = 输入负值 % 127
- flag = `7032240d5e5a1d0e021c04656d2b7c4c`

**技术总结**：
- LWE + 增广LLL格密码分层
- err空间严格0/1（不lr宽0-126），权重L=M^2
- 用 f(x)=1-2x 映射err保持地位均等
- 结果向量留痕 t=sqrt(L)

**质量评估**：高（LLL构造详尽 + flag）
