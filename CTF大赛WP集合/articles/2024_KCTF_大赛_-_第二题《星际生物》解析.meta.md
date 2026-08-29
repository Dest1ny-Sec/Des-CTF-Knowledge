---
title: 2024 KCTF 大赛 - 第二题《星际生物》解析
contest: KCTF大赛
year: 2024
difficulty: medium
vuln_type: [reverse, misc_math]
tags: [.NET逆向, dnSpy, 数独求解, 迷宫, flag拼接]
attack_chain: 拖入 dnSpy 定位 main 函数 → GPT 提炼有效信息 → 前 56 字节是 9x9 数独 → 后 8 字节是 WASD 迷宫指令 → 在线数独求解得 34689155813271746868579324125982187492581517263447389126 → 迷宫路径 SDSDDWWA → 拼 flag
key_payload: xx xx 02 xx xx 07 xx xx x / xx 06 xx 09 xx xx 04 xx / xx 09 xx 02 05 xx xx xx 03 / ... / 路径 SDSDDWWA ; flag{34689155813271746868579324125982187492581517263447389126SDSDDWWA}
one_liner: .NET 数独 + 迷宫路径拼接。
lesson: .NET CrackMe 优先用 dnSpy 反编 main，关键算法用 GPT 提炼效率高。
quality: medium
---
# 2024 KCTF 大赛 - 第二题《星际生物》解析

**围观 2000+，41 队提交 flag，前 3：崇文路大专 / hzqmwne / Nepnep**

**题目结构**

输入 70 字节 `flag{...}`，分两段：
- 前 56 字节 → 9x9 数独的解
- 后 8 字节 → WASD 迷宫移动指令

**解题步骤**

1. **.NET 逆向**：dnSpy 打开 PE，反编 main → 调用 GPT 提炼"前 56 位是数独、后 8 位是迷宫"
2. **数独求解**：从内存提取 9x9 数独原始数组
   ```
   xx xx 02 xx xx 07 xx xx x
   xx 06 xx 09 xx xx 04 xx x
   xx 09 xx 02 05 xx xx xx 03
   xx xx xx 04 xx xx 01 xx xx
   07 03 xx xx 06 xx xx xx x
   xx xx 09 05 03 xx xx 06 x
   xx xx 06 03 04 xx xx 07 x
   08 xx xx xx xx xx xx xx 09
   xx xx xx xx xx xx xx 05 x
   ```
   在线求解 → `34689155813271746868579324125982187492581517263447389126`
3. **迷宫导航**：
   ```
   ! – ? + + + – + – + + + + – – +
   ```
   路径 `SDSDDWWA`（S=下 D=右 W=上 A=左）走到 `?` 终点
4. **拼 flag**：`flag{34689155813271746868579324125982187492581517263447389126SDSDDWWA}`
