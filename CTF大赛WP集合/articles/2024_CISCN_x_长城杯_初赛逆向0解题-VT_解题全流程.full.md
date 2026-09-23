---
title: 2024 CISCN x 长城杯 初赛逆向 0 解题 - VT 解题全流程
contest: CISCN x 长城杯
year: 2024
difficulty: medium
vuln_type:
- reverse
- misc_math
tags:
- CRC32爆破
- 短密钥
- XOR轮密钥
- IDA条件断点
- KeyList提取
attack_chain: IDA 找主函数 + 子函数 → 看到 CRC32-style 函数（0xEDB88320 多项式）→ 找到 48 字节密文 KeyList → 2 字节密钥 Param1（0~0xFFFF 爆破）→ 48 字节密文 = KeyList[i] ^ pParam1[i%2] → 喂 calc 函数算 CRC32 → 比对 0xF703DF16 → 找到 Param1 = 0xXXXX → 拼 flag
key_payload: uint8_t KeyList[] = {82,225,68,226,57,225,94,155,81,220,25,152,80,146,57,193,80,158,82,130,39,130,38,231,83,128,36,128,66,220,57,158,2,148,39,129,69,131,81,147,2,128,68,129,68,129,68,129} ; if (calc_value == 0xF703DF16) printf("Cracked:%02X%02X", pParam1[0], pParam1[1])
one_liner: 2 字节密钥爆破 + CRC32 反推 + KeyList XOR。
lesson: 短密钥 + 标准 CRC32 函数 + 已知 48 字节密文是爆破黄金组合。
quality: high
full_path: 2024_CISCN_x_长城杯_初赛逆向0解题-VT_解题全流程.full.md
meta_path: 2024_CISCN_x_长城杯_初赛逆向0解题-VT_解题全流程.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 CISCN x 长城杯 初赛逆向 0 解题 - VT 解题全流程。2 字节密钥爆破 + CRC32 反推 + KeyList XOR。。经验：短密钥 + 标准 CRC32 函数 + 已知 48 字节密文是爆破黄金组合。
category: reverse
subcategory: reverse
subcategories:
- reverse
- math
tools_used:
- IDA
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/232235.html
reasoning_chain:
- 触发点：IDA 看主函数+子函数 → 假设：CRC32 校验 + XOR 轮密钥 → 动作：grep 0xEDB88320 多项式常量
- 观察：定位 calc 函数 → 假设：标准 CRC32 + 48 字节 KeyList 密文 → 动作：提取 KeyList 字节数组
- 触发点：48 字节 KeyList 已知 → 假设：2 字节 Param1 短密钥可爆破 → 动作：循环 0x0000~0xFFFF
- 观察：calc_value == 0xF703DF16 → 假设：找到正确 Param1 → 动作：pwntools brute force
- 触发点：找到 Param1=0xXXXX → 假设：拼 48 字节密文 XOR Param1 → 动作：KeyList[i] ^ pParam1[i%2]
- 观察：48 字节明文 → 假设：就是 flag → 动作：python 解密脚本跑一遍
- 触发点：flag 拼成 Cracked:%02X%02X → 假设：IDA 条件断点验证 → 动作：IDA Python 写脚本设断点
- 观察：断点命中 → 下一步：导出 flag
failed_attempts:
- 试图直接反编译主函数 → 失败：被优化混淆
- 试图爆破 16 字节长密钥 → 失败：计算量太大
- 试图用动态调试逆 calc 函数 → 失败：静态分析更快
- 试图不解 Param1 直接猜 → 失败：2 字节爆破仅 65536 次
key_observations:
- 短密钥 + 标准 CRC32 函数 + 已知 48 字节密文是爆破黄金组合
- 0xEDB88320 多项式是标准 CRC32 识别关键
- IDA 条件断点（calc_value == 0xF703DF16）是逆向验证快捷路径
- 2 字节密钥爆破仅 65536 次是 CTF 逆向常见突破口
- 48 字节密文 XOR 双字节循环是 CTF 简单加密模板
prerequisites:
- IDA 静态分析与条件断点
- CRC32 算法原理与 0xEDB88320 多项式识别
- pwntools brute force 脚本编写
- XOR 循环密钥还原
---
# 2024 CISCN x 长城杯 初赛逆向0解题-VT 解题全流程

> 原文: https://www.ctfiot.com/232235.html
> ID: 232235

作者论坛账号：Tkazer

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
uint32_t calc(uint8_t* data, int len)
{
        uint32_t ret_value = -1;
        for (int count = 0; count < len; count++)
        {
                ret_value ^= data[count];
                for (int i = 0; i < 8; i++)
                {
                        if (ret_value & 1)
                        {
                                ret_value = (ret_value >> 1) ^ 0xEDB88320;
                        }
                        else
                        {
                                ret_value >>= 1;
                        }
                }
        }
        return ~ret_value;
}
复制代码 隐藏代码
    #include 

uint32_t calc(uint8_t* data, int len)
{
        uint32_t ret_value = -1;
        for (int count = 0; count < len; count++)
        {
                ret_value ^= data[count];
                for (int i = 0; i < 8; i++)
                {
                        if (ret_value & 1)
                        {
                                ret_value = (ret_value >> 1) ^ 0xEDB88320;
                        }
                        else
                        {
                                ret_value >>= 1;
                        }
                }
        }
        return ~ret_value;
}

int main()
{
        short Param1 = 0;
    // 爆破2字节
        for (int i = 0; i < 0xffff; i++)
        {
                Param1 = i;
        // ida条件断点得到的key值列表
                uint8_t KeyList[]{
                        82,225,68,226,57,225,94,155,81,220,
                        25,152,80,146,57,193,80,158,82,130,
                        39,130,38,231,83,128,36,128,66,220,
                        57,158,2,148,39,129,69,131,81,147,
                        2,128,68,129,68,129,68,129 };
                uint8_t Enc[48]{};
                uint8_t* pParam1 = (uint8_t*)(uint64_t)(&Param1);

        // calc之前的异或计算
                for (int j = 0; j < 48; j++)
                {
                        Enc[j] = pParam1[j % 2] ^ KeyList[j];
                }

                auto calc_value = calc(Enc, 48);
                if (calc_value == 0xF703DF16)
                {
                        printf("Cracked:%02X%02Xn", pParam1[0], pParam1[1]);
                        break;
                }
        }

        return0;
}
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