---
title: CTF经验贴｜我们对PWN都有哪些误会
contest: 公众号文章（安恒信息）
year: 2023
difficulty: easy
vuln_type: misc_unknown
tags: [pwn, 经验, 学习路线, 入门, ROP, ARM]
attack_chain:
  - 讲述PWN学习路径与心态
  - 列出推荐书单与ubuntu版本
  - 给出shaokao例题完整rop()函数源码
  - ARM汇编_funcA/_sum示范
key_payload: rop() 含 add rax,1;ret 0x496710 链 59 次后 syscall
one_liner: PWN学习经验贴，定位"耐得住寂寞"+完整rop示例
lesson: PWN学习无系统问题，难点是耐住寂寞长期投入
quality: low
---

# CTF经验贴｜我们对PWN都有哪些误会

## 题目信息
- 来源：安恒信息公众号（实际为经验分享文章，非真实赛题）
- 时间：2023-08
- 作者视角：从业者反思 PWN 学习路径

## 关键内容
1. **心态问题**：PWN 难在"耐得住寂寞"，前人已修缮得很好，入门后很长一段时间"什么都做不了"
2. **推荐书单**：
   - 操作系统：《操作系统真象还原》《鸟哥的Linux私房菜》
   - 计原：《深入理解计算机系统(CSAPP)》《程序员的自我修养》
   - C/C++：《C Primer plus》《C++ Primer plus》
   - 汇编：王爽《汇编语言》
3. **环境版本**：ubuntu 16.04(glibc-2.23) / 18.04(2.28) / 20.04(2.31) / 22.04(2.34)
4. **完整 ROP 示例**（shaokao 题）：pop rsi;ret → 写 /bin//sh → pop rdi;ret → add rax,1 链 59 次 → syscall
5. **ARM 汇编示例**：_funcA 调 _sum，stp x29,x30,[sp,#-0x10]!

## 评分
- quality: low（经验贴，非赛题 writeup；技术含量集中在 shaokao ROP 链示例，但附图为公众号配图无内容）
