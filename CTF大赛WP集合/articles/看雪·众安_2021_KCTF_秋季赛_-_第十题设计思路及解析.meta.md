---
title: 看雪·众安 2021 KCTF 秋季赛 | 第十题设计思路及解析
contest: 看雪·众安 2021 KCTF秋季赛
year: 2021
difficulty: hard
vuln_type: reverse
tags: [10种jmp混淆, CodeLineToExpand, lea esp堆栈平衡, 平方剩余算法, CrackMe bug修复, 情感短视频]
attack_chain: 10种jmp混淆混淆代码→6个call+lea esp堆栈平衡找真实指令→平方剩余算法→发现并修复CrackMe中的bug
key_payload: "CodeLineToExpand结构;10种jmp混淆长度:6/0x1C/0xC/0x2D/0x34/0x86/0x59/0x42/0x99/0x46;6 call后lea esp [esp+N]后为真实指令;平方剩余算法"
one_liner: 看雪众安KCTF2021秋Q10《生命的馈赠》10种jmp混淆+平方剩余+情感短视频+CrackMe bug修复
lesson: 6 call+lea esp堆栈平衡识别真实指令；平方剩余算法；KCTF首部配短视频的CTF题
quality: high
---

# 看雪·众安 2021 KCTF 秋季赛 | 第十题设计思路及解析

**赛事**：看雪·众安 2021 KCTF秋季赛 Q10《生命的馈赠》

**难度**：围观1957人，4队破解（金左手、中娅之戒、mininep、辣鸡战队）

**特色**：**首部配短视频的CTF赛题**（《生命的馈赠》情感微电影）

**三层难度**：
- 初级：对抗混淆
- 中级：熟悉平方剩余算法
- 高级：发现并修复CrackMe中的bug

**10种jmp混淆类型**：

| 类型 | 长度 | 模式 |
|------|------|------|
| 1 | 6 | `push Addr; ret` |
| 2 | 0x1C | push eax + 复杂栈操作 |
| 3 | 0xC | `mov [esp-4], Addr; jmp [esp-4]` 或 `sub esp, 4; ret` |
| 4 | 0x2D | push eax + jmp间接 |
| 5 | 0x34 | push Addr + push eax多层 |
| 6 | 0x86 | 4+5组合 |
| 7 | 0x59 | push 0x7FFA08AC + jmp [esp]（API call） |
| 8 | 0x42 | pushfd + mul + jne + add esp |
| 9 | 0x99 | 7+8组合 |
| 10 | 0x46 | pushfd + xor + jmp [esp-C]（API ret） |

**CodeLineToExpand结构**：
```cpp
struct CodeLineToExpand {
    OrderType m_Type;          // 原来代码的类型
    Param1; Param2;
    OldAddr;                  // 原来代码的地址
    OldAddrToJmpOrCall;       // 原来代码中要跳转的目标地址
    OldIndexValue;
    NewSize;                  // 加入远相对jmp后的大小
    NewAddr;
    NewAddrToJmpOrCall;
    RamdomValue;              // 随机值
    NewCode;                  // 新的代码
};
int MapNewToOld[nCodeLines]; // 新旧Line对应关系
```

**混淆规律破解**：
- **6个call之后，类似下面这样平衡堆栈的指令下面一条，就是真实指令**
  ```asm
  lea esp, dword ptr ss:[esp+0x14]
  lea esp, dword ptr ss:[esp+0x8]
  ```

**真实指令识别**：
- 寻找 `lea esp, [esp+N]` 模式
- 前6个call + 1个lea esp + 1条真实指令
- 例：`call $+0x2E; mov eax, eax; call $+0xB; ... lea esp, [esp+0x14] ; 真实指令`

**算法**：
- 平方剩余算法
- 涉及`fs:[30h]`+8h+PEB+检查PEB.BeingDebugged
- popfd恢复eflags+add esp 4 + jmp间接

**关键技术**：
- 10种jmp混淆的CodeLineToExpand结构化识别
- 6 call+lea esp堆栈平衡的真实指令提取
- 平方剩余算法（需熟悉）
- CrackMe bug发现与修复

**质量评估**：高（设计思路+混淆模板+情感短视频）
