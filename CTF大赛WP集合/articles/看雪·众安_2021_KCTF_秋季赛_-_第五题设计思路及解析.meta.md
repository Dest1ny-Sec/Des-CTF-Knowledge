---
title: 看雪·众安 2021 KCTF 秋季赛 | 第五题设计思路及解析
contest: 看雪·众安 2021 KCTF秋季赛
year: 2021
difficulty: hard
vuln_type: misc_unknown
tags: [Codelets细粒度线程, DARTS运行时, 多项式商环RSA, 16轮Feistel网络, PolyBlock 24bit, xorshift PRF, Luby-Rackoff]
attack_chain: blockHasher(xorshift PRF)处理username→PolyRSA(GF(61)下模多项式t^24+...+t+38的商环加密)→16轮6路Feistel网络(Luby-Rackoff将PRF转PRP)→反演：分解多项式求phi(61^11-1)*(61^13-1)→逆PolyRSA→反Feistel
key_payload: "blockHasher:xorshift+0x2545F4914F6CDD1D;Poly:t^24+51*t^21+...+t+38 mod 61;phi=(61^11-1)*(61^13-1);6路16轮Feistel;Username=KCTF SN=4E6B0C83AA2E6B6E946477B2149A8816D730"
one_liner: 看雪众安KCTF2021秋Q5《拔刀相向》数据流混淆：DARTS并行+Codelets打断控制流+多项式商环RSA+Feistel
lesson: 数据流混淆（Dataflow flattening）+ DARTS并行codelet调度干扰控制流分析；多项式商环RSA用Sage分解
quality: high
---

# 看雪·众安 2021 KCTF 秋季赛 | 第五题设计思路及解析

**赛事**：看雪·众安 2021 KCTF秋季赛 Q5《拔刀相向》

**难度**：围观1094人，**无人攻破**（4天）

**纪念**：高光荣教授（1945-2021.9.12），中国第一位MIT计算机博士

**核心创新**：
- 基于Codelets细粒度线程执行模型 + DARTS运行时
- **多线程调度打断传统控制流分析**
- 高度并行化 → 任意时刻断点内存无严格算法中间状态

**三部分算法**：

**1. blockHasher (xorshift PRF)**：
```cpp
void blockHasher::fire() {
    uint64_t x = *(uint64_t*)hh.data;
    x ^= hh.data[8];
    x ^= x >> 12; x ^= x << 25; x ^= x >> 27;
    x *= 0x2545F4914F6CDD1DULL;
    *((uint8_t*)result) = x&0xFF;
    *((uint8_t*)result+1) = (x >> 8)&0xFF;
    *((uint8_t*)result+2) = (x >> 16)&0xFF;
    toSignal->decDep();
}
```
- 输入 3个PolyBlock（9字节）→ 输出 1个PolyBlock（3字节）
- 类似PRF

**2. Poly结构**：
- 24项多项式（最高次23）
- 6个PolyBlock × 4系数 = 24个系数
- 每系数模61 → 6 bit
- PolyBlock = 4*6 = 24 bit = 3 bytes
- bits顺序打乱 + XOR固定mask = 混淆二进制表示

**3. PolyRSA (GF(61)多项式商环)**：
- 模多项式 t^24 + 51*t^21 + 55*t^20 + 2*t^19 + 3*t^18 + 35*t^17 + 13*t^16 + 5*t^15 + 25*t^14 + 40*t^13 + 11*t^12 + 17*t^11 + 48*t^10 + 26*t^9 + 48*t^8 + 54*t^7 + 5*t^6 + 19*t^5 + 28*t^4 + 43*t^2 + t + 38
- **SageMath分解**：
  - (t^11 + 19*t^6 + 55*t^5 + 2*t^4 + 7*t^3 + 30*t^2 + 59*t + 30) * (t^13 + 51*t^10 + ...)
  - **phi = (61^11-1) * (61^13-1)**
- 类似RSA指数：2^0 + 2^7 + 2^21 + 2^31

**4. 16轮6路Feistel网络**：
- Luby-Rackoff定理：PRF转PRP
- 上一层随机选3个polyBlock作blockHash输入
- 输出与剩下3个polyBlock相加（多项式环中）
- hash block + blockAdder输出 → 随机排列成下一层
- **可逆**

**Hash算法**：
- 基于blockHash的简易Hash
- 不可逆，无需研究
- 做题时只需从内存提取 'KCTF' 对应的Hash数据

**数据依赖混淆**：
- 算法描述Declaration位置 ≠ 实际计算位置
- 声明与运行解耦

**两个公开序列号**：
- 第一组：Username=56DF4D8D86305660, SN=4A2CD38229906B47E4C04723C0BEAD86A599
- **第二组：Username=KCTF, SN=4E6B0C83AA2E6B6E946477B2149A8816D730**

**核心技术**：
- DARTS Codelets 多线程并行调度
- 6路Feistel网络（Luby-Rackoff PRF→PRP）
- 多项式商环RSA（GF(61)模多项式）
- SageMath分解多项式求phi
- 数据流混淆（Dataflow flattening）

**质量评估**：高（设计理念先进 + 两组SN完整）
