---
title: 2024 CISCN x 长城杯 初赛逆向 0 解题 - VT 解题全流程
contest: CISCN x 长城杯
year: 2024
difficulty: medium
vuln_type: [reverse, misc_math]
tags: [CRC32爆破, 短密钥, XOR轮密钥, IDA条件断点, KeyList提取]
attack_chain: IDA 找主函数 + 子函数 → 看到 CRC32-style 函数（0xEDB88320 多项式）→ 找到 48 字节密文 KeyList → 2 字节密钥 Param1（0~0xFFFF 爆破）→ 48 字节密文 = KeyList[i] ^ pParam1[i%2] → 喂 calc 函数算 CRC32 → 比对 0xF703DF16 → 找到 Param1 = 0xXXXX → 拼 flag
key_payload: uint8_t KeyList[] = {82,225,68,226,57,225,94,155,81,220,25,152,80,146,57,193,80,158,82,130,39,130,38,231,83,128,36,128,66,220,57,158,2,148,39,129,69,131,81,147,2,128,68,129,68,129,68,129} ; if (calc_value == 0xF703DF16) printf("Cracked:%02X%02X", pParam1[0], pParam1[1])
one_liner: 2 字节密钥爆破 + CRC32 反推 + KeyList XOR。
lesson: 短密钥 + 标准 CRC32 函数 + 已知 48 字节密文是爆破黄金组合。
quality: high
---
# 2024 CISCN x 长城杯 初赛逆向 0 解题 - VT 解题全流程

**分析过程**

IDA 打开二进制，主函数结构是：
1. 读 2 字节 `Param1`（短密钥）
2. 调 `calc(Enc, 48)` 计算某种 hash
3. 对比 48 字节结果是否等于目标值

`calc` 函数实现是标准 CRC32（多项式 0xEDB88320）：

```c
uint32_t calc(uint8_t* data, int len) {
    uint32_t ret_value = -1;
    for (int count = 0; count < len; count++) {
        ret_value ^= data[count];
        for (int i = 0; i < 8; i++) {
            if (ret_value & 1) ret_value = (ret_value >> 1) ^ 0xEDB88320;
            else ret_value >>= 1;
        }
    }
    return ~ret_value;
}
```

**爆破脚本**

IDA 条件断点提取 48 字节 `KeyList`，然后爆破 2 字节 Param1：

```c
int main() {
    for (int i = 0; i < 0xffff; i++) {
        short Param1 = i;
        uint8_t KeyList[] = {
            82,225,68,226,57,225,94,155,81,220,25,152,80,146,57,193,
            80,158,82,130,39,130,38,231,83,128,36,128,66,220,57,158,
            2,148,39,129,69,131,81,147,2,128,68,129,68,129,68,129
        };
        uint8_t Enc[48] = {};
        uint8_t* pParam1 = (uint8_t*)(uint64_t)(&Param1);
        for (int j = 0; j < 48; j++) {
            Enc[j] = pParam1[j % 2] ^ KeyList[j];
        }
        auto calc_value = calc(Enc, 48);
        if (calc_value == 0xF703DF16) {
            printf("Cracked:%02X%02X\n", pParam1[0], pParam1[1]);
            break;
        }
    }
    return 0;
}
```

**关键点**

1. **KeyList 提取**：用 IDA 条件断点 `if (count == 47 && ret_value == 0xF703DF16)` 在断点处 dump 数组
2. **爆破空间 0xFFFF = 65536**：单线程 1 秒内必出
3. **加密逻辑**：`Enc[j] = pParam1[j%2] ^ KeyList[j]` 是 2 字节密钥循环复用 XOR
4. **校验**：`~ret_value` 末尾取反 → CRC32 final xor
5. **拼 flag**：Param1 字节序敏感（little-endian），C 中 `Param1 = 0x1234` → pParam1[0]=0x34, pParam1[1]=0x12
