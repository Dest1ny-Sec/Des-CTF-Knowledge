---
title: H&NCTF RE 部分题解
contest: H&NCTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [rev, enigma-virtual-box, anti-vm, anti-av, shellcode-injection, kernel32-hash, ldr-list]
attack_chain:
  - enigma virtual box 打包exe+多个dll
  - main函数: 在C盘用户视频目录创建副本svchsst.exe
  - 副本启动: 删除txt+原文件+继续执行
  - 实体机跑: v48=16 走主逻辑
  - 检测VMware tools/VirtualBox Guest Additions
  - 进程快照遍历LDR双向链表
  - kernel32名字hash比对
  - 杀软检测: Process Snapshot遍历
  - sub_140001320 shellcode自解密+注入exp10rer.exe
  - shellcode自修改XOR+位运算
key_payload: sub_140001320 解密shellcode → 注入 exp10rer.exe
one_liner: H&NCTF RWhackA：Enigma打包+反VM+反杀软+shellcode注入
lesson: Enigma Virtual Box打包需用动态调试+反VM检测绕过
quality: high
---

# H&NCTF RE 部分题解

## 题目信息
- 比赛：H&NCTF
- 题目：RWhackA（恶意程序逆向）
- 类别：Reverse

## 关键攻击链
### 1. Enigma Virtual Box 打包
- 多个 exe + dll 一起打包
- 解包工具失败，需硬分析

### 2. 启动逻辑
- main 函数：在 C:\Users\<user>\Videos 创建副本 `svchsst.exe`
- 副本启动后：
  - 打开 txt 失败 → 复制自己到副本
  - 副本启动后检测到 txt → 删除 txt + 原文件
  - 继续执行

### 3. 虚拟机/杀软检测
- v48 = system_info 结构内容
- 实体机跑：v48=16
- 枚举进程：检测 VMware tools / VirtualBox Guest Additions
- 进程快照遍历 LDR 双向链表
- kernel32 名称 hash 比对

### 4. 主逻辑：Shellcode 注入
- sub_140001320 函数：
  - 自解密 shellcode
  - 注入到 `exp10rer.exe` 进程
  - flag 藏在 shellcode 中

### 5. Shellcode 自修改
```c
v4 = &unk_140003450;
v5 = 7i64;
do {
    v3 += 32;
    v6 = *v4; v7 = v4[1]; v4 += 8;
    *(v3 - 8) = v6;
    v8 = *(v4 - 6); *(v3 - 7) = v7;
    // ... 字节重排 ...
} while (--v5);
```

## 评分
- quality: high（Enigma 打包 + 反VM + 反杀软 + shellcode 注入完整）
