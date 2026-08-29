---
title: 【2026春节】初十 Windows 高级题目 WriteUp & 提示词分享
contest: 春节活动
year: 2026
difficulty: hard
vuln_type: reverse
tags: [whitebox-crypto, MBA-obfuscation, opaque-predicate, SSE-MBA, Unicorn-emulation, CHIMERA1, SipHash-variant, PRISMWB3]
attack_chain: PE 映射到 Unicorn 内存 / HookD3B20 比较函数读 rdx 期望值 / 白盒密码 20 轮 PRISMWB3 / 642 行 SSE/MBA 派生函数 / MBA 状态机包裹的 memcpy / 280 字节派生 / 32 字节 SipHash 变体
key_payload: RVA 0x154E50 已知白盒密码上下文 (~2.7MB) + RVA 0xAD7660 自定义白盒密码上下文 (~28.8MB) + CHIMERA1 头验证
one_liner: 2026 春节初十 Windows 高级题，~95M 指令白盒密码 + MBA 混淆 + Unicorn 全指令模拟逆向。
lesson: MBA(mixed boolean arithmetic) 表达式 n*(n+1) 或 n*(n-1) 是不透明谓词；白盒密码 20 轮 + 28.8MB 查找表让 IDA F5 失败；Unicorn 全指令模拟 + Hook 关键函数是处理混淆巨无霸二进制唯一可行路径。
quality: high
---

# 【2026春节】初十 Windows 高级题目 WriteUp & 提示词分享

## 概览
Tokeii 2026 春节初十 Windows 高级逆向题，PE 大小 40MB，含白盒密码 + MBA 混淆 + Unicorn 模拟实战。

## 题目分析
- 约 40MB PE 文件，大部分为数据段中嵌入的密码学查找表
- **已知白盒密码上下文**（RVA 0x154E50）：~2.7MB
- **自定义白盒密码上下文**（RVA 0xAD7660）：~28.8MB（0x1B4F428 字节）
- 自绘窗口，输入 UID 和 flag 后触发验证函数
- 几乎所有关键函数控制流被 **MBA 表达式混淆**，使用 `n*(n+1)` 或 `n*(n-1)` 等恒偶不透明谓词控制状态机跳转

## 关键函数
| 函数 | RVA | 功能 | 特点 |
|------|-----|------|------|
| UID → 32 字节哈希 | - | SipHash 变体 | 纯计算 |
| 32 字节 → 280 字节派生 | - | 642 行 SSE/MBA | 无外部调用 |
| CHIMERA1 blob → 堆上下文 | - | MBA 状态机包裹的 memcpy | 验证 "CHIMERA1" 头 |
| 白盒密码核心变换 | - | 反编译失败 | ~95M 指令 |
| 白盒分组密码 | - | 20 轮 | 仅适用于 PRISMWB3 |
| 64 字节内存比较 | - | MBA 混淆的 memcmp | - |

## 攻击路径
1. **Unicorn 模拟**：将 PE 完整映射到 Unicorn 内存空间
2. **Hook 关键函数**：HookD3B20（比较函数），在比较时读取 rdx（期望值 m2）
3. **失败教训**：
   - Frida GUI 自动化无法正确触发按钮点击
   - 曾捕获一个 m2 值，但无法确认其对应的 UID
4. **白盒密码提取**：白盒密码 20 轮 + 查找表让 IDA F5 失败，需要动态执行提取 key+plaintext 对

## 经验提炼
- MBA (mixed boolean arithmetic) 表达式 `n*(n+1)` 或 `n*(n-1)` 是恒偶不透明谓词
- 白盒密码 20 轮 + 28.8MB 查找表让 IDA F5 失败，必须动态执行
- PRISMWB3 / CHIMERA1 是商业白盒密码实现，常见于 DRM
- Unicorn 全指令模拟 + Hook 关键函数是处理混淆巨无霸二进制唯一可行路径
- 动态分析中"提取 key+plaintext 对"是破解白盒密码标准做法
- 0x154E50 / 0xAD7660 等 RVA 标识白盒密码上下文位置
