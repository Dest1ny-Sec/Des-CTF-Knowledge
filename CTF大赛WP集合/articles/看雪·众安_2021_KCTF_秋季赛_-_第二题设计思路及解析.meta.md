---
title: 看雪·众安 2021 KCTF 秋季赛 | 第二题设计思路及解析
contest: 看雪·众安 2021 KCTF秋季赛
year: 2021
difficulty: hard
vuln_type: reverse
tags: [codeLSalt 256字节置换, gbsA[256][256]统计, inner_code_bin前8字节爆破, codeL/codeH 32位序列号, 40320种排列]
attack_chain: codeLSalt前8字节从固定集合[30,40,75,109,140,163,210,251]中排列组合40320种→遍历生成gbsA[256][256]统计→找唯一有效排列12399→得到codeL[0x4B,0x6D,0x28,0x8C,0xFB,0xD2,0x1E,0xA3]→codeH[0x9D,0x6B,0xEA,0x2F,0xA4,0x08,0xBC,0x22]
key_payload: "codeLSalt[0x100] 256字节置换;csl=[30,40,75,109,140,163,210,251]前8字节40320排列;codeL={0x4B,0x6D,0x28,0x8C,0xFB,0xD2,0x1E,0xA3};codeH={0x9D,0x6B,0xEA,0x2F,0xA4,0x08,0xBC,0x22};SN=B4D682C8BF2DE13AD9B6AEF24A80CB22"
one_liner: 看雪众安KCTF2021秋Q2《迷失丛林》：codeLSalt 256字节置换+前8字节排列爆破40320种+codeH爆破
lesson: 256字节S盒前8字节可从固定集合排列爆破；gbsA统计+有效性筛选
quality: high
---

# 看雪·众安 2021 KCTF 秋季赛 | 第二题设计思路及解析

**赛事**：看雪·众安 2021 KCTF秋季赛 Q2《迷失丛林》

**难度**：围观2708人，38队破解，一血13492秒（约3.7h）

**SN**：`B4D682C8BF2DE13AD9B6AEF24A80CB22`

**题目设计**：
- codeLSalt[0x100]：256字节S盒置换
- gbsA[256][256]：统计数组
- inner_code_bin[0x10]：输入hex转bin

**四部分算法**：
1. 第一部分：codeLSalt演化（每i生成bts[0x200]）→ gbsA统计
2. 第二部分：codeLSalt变换（类似permute）
3. 第三部分：codeH按位操作（8次循环）
4. 第四部分：hash比较

**爆破思路**：

**Step 1：codeLSalt前8字节爆破**
```python
cst = set(ida_bytes.get_bytes(0x404000+8, 0x100-8))  # tail 248字节集合
csa = set([i for i in range(0x100)])  # 全0x100
csl = list(csa - cst)  # 差集 = 前8字节
# csl = [30, 40, 75, 109, 140, 163, 210, 251]
# 8! = 40320 种排列
from itertools import permutations
pl = [p for p in permutations(csl, 8)]  # 40320排列
```

**Step 2：遍历排列找有效codeL**
- 编译执行 `find_codeLSalt.c`
- 命令：`find_codeLSalt.exe 0 40230 pbs.bin`
- 找到第12399号排列：
  ```c
  codeL[0..7] = {0x4B, 0x6D, 0x28, 0x8C, 0xFB, 0xD2, 0x1E, 0xA3};
  ```

**Step 3：codeLSalt变换xcs**
- `gen_xcs.exe 12399 pbs.bin` 生成xcs
- 第二部分变换：循环置换codeLSalt

**Step 4：codeH爆破**
- `find_codeH.c` 编译执行
- 给出"正确"提示 GoodJob~
- codeH[0..7] = `{0x9D, 0x6B, 0xEA, 0x2F, 0xA4, 0x08, 0xBC, 0x22}`

**SN组合**：
- codeL对应输入 `B4D682C8BF2DE13A`
- codeH对应输入 `D9B6AEF24A80CB22`
- **完整SN = B4D682C8BF2DE13AD9B6AEF24A80CB22**

**inner_code_bin**：
- input code hex = "0123456789ABCDEF" + "0123456789ABCDEF"
- 转bin: `1032547698BADCFE::1032547698BADCFE`
- 即每2字符转1字节
- `'01'→0x10, '23'→0x32, ..., 'EF'→0xFE`

**核心技术**：
- 256字节S盒前8字节从差集 = 8元素排列爆破（40320种）
- gbsA[256][256]统计每个i的0x100衍生片段
- 遍历找唯一有效排列
- IDA Python提取`ida_bytes.get_bytes(addr, size)`获取尾部字节

**质量评估**：高（爆破代码完整 + SN）
