---
title: CTF比赛PWN题解题思路(一)
contest: 公众号文章（小话安全）
year: 2024
difficulty: easy
vuln_type: rop
tags:
- pwn
- 栈溢出
- ret2shell
- IDA
- 入门
attack_chain:
- 题1：栈溢出admin+51字符+0x405D36覆盖返回地址shell函数
- 题2：data输入0xc0字节覆盖v7变量与v5比较触发shell
- 题3：gets栈溢出+RDI指向/bin/sh+调用system
- 题4：gets栈溢出+vmmap找可写地址注入/bin/sh再system
key_payload: 'payload = b"a"*32+b"b"*8+rop()  # 含add rax,1;ret 循环'
one_liner: 4道PWN入门题，栈溢出+返回地址覆盖+ROP思路
lesson: 栈溢出三要素：覆盖长度+目标地址+payload构造
quality: medium
full_path: CTF比赛PWN题解题思路(一).full.md
meta_path: CTF比赛PWN题解题思路(一).meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: CTF比赛PWN题解题思路(一)。4道PWN入门题，栈溢出+返回地址覆盖+ROP思路。关键路径：题1：栈溢出admin+51字符+0x405D36覆盖返回地址shell函数 → 题2：data输入0xc0字节覆盖v7变量与v5比较触发shell → 题3：gets栈溢出+RDI指向/bin/sh+调用system。经验：栈溢出三要素：覆盖长度+目标地址+payload构造
category: pwn
subcategory: rop
tools_used:
- IDA
time_required: quick
difficulty_score: 2
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/201125.html
reasoning_chain:
- 题 1 触发点：栈溢出 admin + 51 字符 → 假设：覆盖返回地址 + 跳到 shell 函数
- 动作：payload = 'admin' + 51个 A + 0x405D36（shell 函数地址）→ 观察：跳转成功
- 题 2 触发点：data 输入 0xc0 字节覆盖 v7 → 假设：v7 和 v5 比较触发 shell
- 动作：观察 v7 与 v5 的相对偏移 + 构造等值字符串 → 观察：触发 shell
- 题 3 触发点：gets 栈溢出 + RDI 指向 /bin/sh → 动作：rop pop rdi + /bin/sh + ret system → 观察：shell 弹出
- 题 4 触发点：gets 栈溢出 + vmmap 找可写地址 + /bin/sh 注入 → 动作：payload 注入 /bin/sh + 跳 syscall 或 system
- 观察：4 题都是基础栈溢出三要素 → 总结
failed_attempts:
- 题 1 直接 ret 不知道跳到哪 → 失败：必须先 IDA 找 shell 函数引用地址
- 题 2 覆盖 v7 但 v5 在栈上另一位置 → 失败：偏移没算对
- 题 3 pop rdi gadget 不会找 → 失败：用 ROPgadget 找出 pop rdi; ret
key_observations:
- 栈溢出三要素：覆盖长度 + 目标地址 + payload 构造
- 公众号初学者 PWN 题通常 IDA 已有 shell 函数（看引用字符串）
- ROP pop rdi + /bin/sh + system 是 x64 经典 ret2libc
- vmmap 看可写地址：heap / bss / 段
- 覆盖 v7/v5 变量触发条件跳转是入门技巧
prerequisites:
- IDA 静态分析（找 win 函数）
- 栈溢出原理（覆盖返回地址/变量）
- ROPgadget 工具（pop rdi; ret 寻找）
- pwntools p64 + cyclic pattern
- vmmap 内存段查找
---
# CTF比赛PWN题解题思路(一)

> 原文: https://www.ctfiot.com/201125.html
> ID: 201125

题目一

运行程序如下，输入1，提示no username

用IDA对程序进行逆向，需要输入admin才能继续

程序漏洞点是在输入用户名的地方存在栈溢出

方法一

使用gdb进行调试，在main函数处设置断点

单步调试（ni）到func函数处，进行步入(si)

单步调试到名字输入的位置

输入足够长度的字符串

计算引起溢出的字符串长度，有两种方法，第一种包括admin所以长度为56

将返回地址覆盖成程序中我们想让其返回的地址，这里我们通过IDA查找危险函数

这里有危险的shell函数，地址为0x405D36, 因为小端存储，因此我们需要写入365D40，字符串为6]@

最终payload为admin+51个字符+6]@，成功获得shell

方法二

根据变量长度计算空间大小，再加上8比特，编写脚本

题目二

首先查看伪代码，栈空间建议使用gdb进行调试，伪代码查看可能不准确

程序最终的判断是v7和v5相等即可得到shell，v7是程序里的，v5是我们的输入，然后这里data可以输入0xc0个字节，这里可以覆盖v7的地址空间。

因此本题的解题思路是输入data，覆盖掉v7，然后输入已知的数据，获得shell。

编写脚本获得shell

题目三

查看伪代码 gets处存在栈溢出，必须首先输入设定的字符串

但是溢出后的返回地址，程序里面并没有明显的shell，但是有bin/sh字符串和system函数可以利用

获取RDI地址

编写脚本获得shell

题目四

类似于题目三，不同点在于没有/bin/sh字符，需要使用gets函数写入

使用gdb调试，vmmap命令获得可写的地址空间

编写脚本写入/bin/sh

获得shell

原文始发于微信公众号（小话安全）：CTF比赛PWN题解题思路(一)

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