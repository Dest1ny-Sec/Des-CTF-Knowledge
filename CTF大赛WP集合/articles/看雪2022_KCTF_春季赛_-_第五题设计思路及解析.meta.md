---
title: 看雪2022 KCTF 春季赛 | 第五题设计思路及解析
contest: 看雪2022 KCTF春季赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [天堂之门, x86/x64混合, 代码混淆, SEH异常, base64字符串, CheatEngine, 一血6h40m]
attack_chain: 程序32位应用分割算法3部分（64+32+64）→天堂之门CS=0x33切换+retf→cpp异常处理干扰调试→上方有base64字符串（硬件断点）→输入64个0观察加密结果→与KCTF2021春季赛第7题对比
key_payload: "天堂之门: 切换到64位CS=0x33 retf;#pragma pack(1);LEFTMOVE/RIGHTMOVE;XOR_NUMBER=0x8160C68FF6C4875E^0x090A0B004654434B;hex2string;DecM"
one_liner: KCTF2022春季赛Q5《危机四伏》：32/64天堂之门+SEH+三段混淆算法+base64非预期
lesson: 天堂之门对抗大部分调试器；非预期思路：硬件断点+base64字符串+比对历史KCTF题目
quality: high
---

# 看雪2022 KCTF 春季赛 | 第五题设计思路及解析

**赛事**：看雪2022 KCTF春季赛 Q5《危机四伏》

**难度**：围观2036人，仅4支战队成功破解

**一血**：Lixinist战队【上学困难户】6小时40分11秒

**题目设计**：
- 32位Windows应用
- **核心算法分3部分**：第1部分用64位指令、第2部分用32位指令、第3部分用64位指令
- 使用 **天堂之门**（CS=0x33 + retf）切换运行模式
- C++异常处理干扰调试
- 64位混淆：指令等价替换、流程干扰、花指令、垃圾代码、栈地址修改（带随机性）
- 32位混淆：64位功能基础上+SEH异常+指令异或加密（天堂之门解密后切回32位继续执行）

**技术要点**：
1. 天堂之门（Heaven's Gate）
2. x86/x64代码混淆
3. SEH异常处理
4. 算法设计

**破解非预期思路**（上学困难户6h40min一血）：
1. 偶然发现程序上方有 **base64字符串**
2. 下硬件断点
3. 输入64个0，观察加密结果
4. 发现与 **KCTF2021春季赛第7题** 相似（**非预期！**）
5. 找到加密内容后用CheatEngine搜索KCTF
6. 改写出题人keygen算法 → xor后再xor

**KeyGen核心（DecM）**：
```c
// 32位数据数组 d[8]
unsigned short int d[8] = { 0 };
for (int i = 0; i <= 7; i++) {
    d[i] = (((unsigned char*)(g_uhSerial))[(x2 ^ (x1 + 2*i)) % 16] << 8) 
         + ((unsigned char*)(g_uhSerial))[(x2 ^ (x1 + 2*i + 1)) % 16];
}
unsigned short int A = d[0] ^ d[1];
unsigned short int B = d[2] + d[3];
unsigned short int C = d[4] - d[5];
// D = popcount(d[6] ^ d[7])
unsigned short int D = d[6] ^ d[7];
D = (D & 0x55555555) + ((D >> 1) & 0x55555555);
D = (D & 0x33333333) + ((D >> 2) & 0x33333333);
D = (D & 0x0F0F0F0F) + ((D >> 4) & 0x0F0F0F0F);
D = (D & 0x00FF00FF) + ((D >> 8) & 0x00FF00FF);
```

**正确flag**：`39ED62B341BC560217EAB3BF90265D101067856B36495264144A5B487264CB4B`

**质量评估**：高（KeyGen代码 + flag + 出题人设计思路）
