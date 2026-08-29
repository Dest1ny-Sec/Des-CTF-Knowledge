---
title: 看雪2022 KCTF 秋季赛 | 第六题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: easy
vuln_type: reverse
tags: [CrackMe, srand爆破, 随机数种子穷举, KCTF固定字符串, 14位序列号, 0-99999爆破]
attack_chain: 14位序列号→5+4+5拆分→5字节→int→srand(14725)→20个rand==arrSeed_14725→中间"KCTF"→srand(83690)→20个rand==arrSeed_83690→success
key_payload: "14位序列号=14725KCTF83690;srand爆破0-99999;arrSeed_14725[20]={15356,8563,...};arrSeed_83690[20]={11190,27482,...};KCTF固定"
one_liner: KCTF2022秋Q6《病疫先兆》CrackMe：srand种子爆破+rand对比+KCTF固定14位序列号
lesson: srand种子爆破范围小时（0-99999）只需1分钟穷举；20个rand值固定可反推种子
quality: medium
---

# 看雪2022 KCTF 秋季赛 | 第六题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q6《病疫先兆》

**难度**：24小时内41支战队成功提交

**答案**：`14725KCTF83690`

**题目设计**：
- CrackMe(Windows)
- 使用方案一（老规则）
- 穷举爆破随机数种子（0-99999，1分钟内）
- 输入序列号 → 输出success/error

**校验逻辑**：
```c
1. 判断输入文本长度 == 14
2. 拆分为3份(5字节 + 4字节 + 5字节)
3. 2个5字节转为int，作为随机数种子调用srand
4. 调用rand生成20个int数据
5. rand生成的数据和全局数组相等 + 4字节文本==KCTF → success
```

**关键数组**：
```c
unsigned int arrSeed_14725[] = {15356, 8563, 9659, 14347, 11283, 30142, 29542, 18083, 5057, 5531, 23391, 21327, 20023, 14852, 4865, 23820, 16725, 18665, 25042, 24920};

unsigned int arrSeed_83690[] = {11190, 27482, 980, 5419, 28164, 9548, 16558, 22218, 6113, 21959, 13889, 11580, 2625, 19397, 25139, 8167, 28165, 3950, 25496, 27351};
```

**爆破代码**：
```c
int main() {
    int i, j, isSuccess = 0;
    for (i = 0; i < 99999; i++) {
        isSuccess = 1;
        srand(i);
        for (j = 0; j < 20; j++) {
            if (rand() != arrSeed_14725[j]) {
                isSuccess = 0;
                break;
            }
        }
        if (isSuccess) printf("种子1:[%d]\n", i);
    }
    // 同理种子2
}
```

**输入**：`14725KCTF83690`
- 前5字节 "14725" → srand(14725)
- 中间4字节 "KCTF"
- 后5字节 "83690" → srand(83690)

**核心代码逻辑**（IDA反编译）：
```c
srand(preValueCopy);
v7 = dword_B9F000;
while (rand() == *v7) {
    if ((int)++v7 >= (int)dword_B9F050) goto LABEL_7;
}
v14 = 0;

srand(sufValueCopy);
v8 = dword_B9F050;
while (rand() == *v8) {
    if ((int)++v8 >= (int)&dword_B9F0A0) goto LABEL_12;
}
v14 = 0;

if (szKCTF[0] == 'K' && szKCTF[1] == 'C' && szKCTF[2] == 'T' && szKCTF[3] == 'F')
    v13 = 1;

if (v14 && v13) printf("success : %s\n", inputSN);
```

**技术总结**：
- srand种子范围小时（0-99999）可1分钟穷举
- 20个rand值固定 → 反推种子唯一
- 中间固定KCTF字符串
- _getptd() + 0x14 = 种子存储位置

**质量评估**：中（爆破payload完整 + flag）
