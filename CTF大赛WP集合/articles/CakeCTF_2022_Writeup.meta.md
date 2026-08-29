---
title: CakeCTF 2022 Writeup
contest: CakeCTF 2022
year: 2022
difficulty: easy
vuln_type: reverse
tags: [rev, nim, luau, lua-bytecode, forensics, welcome, eqStrings]
attack_chain:
  - welcome: 直接从Discord拿flag
  - nimrev: gdb-peda断eqStrings看参数x/24c
  - luau: viruscamp/luadec构建反编译Lua 5.3字节码
  - zundamon: 日语语音合成软件+隐写
  - 典型: 直接调用eqStrings比较flag
key_payload: gdb-peda$ x/24c 0x7ffff7d0f0e0 → CakeCTF{s0m3t1m3s_n0t_C}
one_liner: CakeCTF 2022 5题writeup：welcome+nimrev+luau+zundamon+survey
lesson: NimMainModule中找eqStrings直接拿flag；Lua字节码用luadec反编译
quality: medium
---

# CakeCTF 2022 Writeup

## 题目信息
- 比赛：CakeCTF 2022（yoshiking / theoremoon / ptr-yudait 主办）
- 覆盖题目：welcome / nimrev / luau / zundamon / survey

## 关键攻击链
1. **[welcome]** 676 解：Discord 直接拿 flag `CakeCTF{p13a53_tast3_0ur_5p3cia1_cak35}`
2. **[nimrev]** 246 解：Nim 编译二进制，找 `NimMainModule` 中 `eqStrings` 调用
   - `gdb-peda$ x/24c 0x7ffff7d0f0e0` 拿到 flag 字节
   - Flag: `CakeCTF{s0m3t1m3s_n0t_C}`
3. **[luau]** 64 解：Lua 5.3 字节码反编译
   - `git clone https://github.com/viruscamp/luadec`
   - `luadec -dis libflag.lua` 反汇编得 CLOSURE/NEWTABLE/SETTABLE
   - 找 libflag.checkFlag
4. **[zundamon]** 20 解：日语语音合成软件 + 隐写（forensics/rev 混合）
5. **[survey]** 226 解：填问卷

## 评分
- quality: medium（5 题 writeup 但每题内容较短，主要给思路 + 关键命令）
