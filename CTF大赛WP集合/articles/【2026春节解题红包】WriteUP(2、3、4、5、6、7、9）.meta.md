---
title: 2026春节解题红包 WriteUP(2,3,4,5,6,7,9)
contest: 春节活动
year: 2026
difficulty: mixed
vuln_type: misc_unknown
tags: [Android-JEB, IDA-static, UPX-unpack, Lua-main, wasm-gen, HMAC-base64, AI-assisted, 逍遥模拟器, JADX, IDA, 7zip]
attack_chain: 题目2 逍遥模拟器 + JEB 全盘分析得 Flag 字节码/题目3 把字节码存到文档 + AI 翻译/题目4 main.lua 7zip 解压 + AI 翻译/题目5 UPX 自动脱壳 + IDA/题目6 check_num 反推函数恢复图片/题目7 wasm gen 函数 HMAC + base64 内存 dump 1295903 地址
key_payload: 题目7 base64 码表 a-zA-Z0-9?!  内存地址 1295903
one_liner: 2026 春节解题红包 8 道题 WP 复盘，Android/IDA/Lua/wasm/UPX 综合实战 + AI 辅助分析。
lesson: 逍遥模拟器+JEB 是 Android 动态调试标配；AI 翻译字节码/WASM 提速但要给足上下文；UPX 自动脱壳工具链成熟；wasm 模块化函数逆向需要逐函数跟入；内存 dump + base64 表逆向比纯算法还原快。
quality: high
---

# 2026 春节解题红包 WriteUP(2,3,4,5,6,7,9)

## 概览
nanaqilin 的 2026 春节 8 道题 WP 复盘，含 Android/IDA/Lua/wasm/UPX 综合实战 + AI 辅助分析。

## 工具栈
- **IDA**: 二进制程序静态分析
- **逍遥模拟器**: 安卓运行与动态调试
- **JEB**: APK 静态分析
- **JADX**: APK 静态分析
- **Python 3.14**: 题目 4 用到
- **DeepSeek**: AI 辅助解决

## 题目2 (Android)
- 逍遥模拟器运行 APK
- 关心 C.q0 方法 case 25
- 用 JEB 全盘分析直接得到 Flag
- 简单但胜之不武

## 题目3 (字节码)
- 字节码存到文档
- AI 翻译字节码逻辑
- 翻译后再人工分析得 flag

## 题目4 (Lua)
- 7zip 解压附件
- main.lua 含核心代码
- AI 翻译 Lua 还原逻辑

## 题目5 (UPX)
- 壳是 UPX，支持自动脱壳
- 用现成工具脱壳
- IDA 分析主程序逻辑
- 主函数逻辑清晰，跟进关键函数

## 题目6 (check_num 反推)
- 写反推 check_num 的函数
- 理论上把图片恢复
- flag 在图片里

## 题目7 (wasm + HMAC + base64)
- 跟进 wasm 的 gen 函数（非常长）
- 核心流程：uid + 特定随机数 → HMAC hash → base64
- base64 码表在内存中固定地址 1295903，可直接查看 `a-zA-Z0-9?!`
- 算出来的 base64 值是语音播报内容
- dump 内存即可得 flag
- 计算内存偏移的核心部分用 AI 翻译（不要给 AI 太多数据会崩）

## 经验提炼
- 逍遥模拟器 + JEB 是 Android 动态调试标配
- AI 翻译字节码/WASM 提速但要给足上下文
- UPX 自动脱壳工具链成熟（`upx -d`）
- wasm 模块化函数逆向需要逐函数跟入
- 内存 dump + base64 表逆向比纯算法还原快
- check_num 反推函数是图像解密常见模式
- AI 给太多数据会"崩溃"（指上下文超限），要分块喂
