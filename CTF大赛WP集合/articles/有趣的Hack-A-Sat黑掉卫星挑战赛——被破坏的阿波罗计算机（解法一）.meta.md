---
title: Hack-A-Sat 阿波罗导航计算机被破坏的 PI 值
contest: Hack-A-Sat
year: 2020
difficulty: hard
vuln_type: misc_unknown
tags: [Apollo, AGC, DSKY, VirtualAGC, Commanche055, PI, octal, DP-float, rope-memory, history]
attack_chain:
  - 用 VirtualAGC 模拟器定位 Commanche055 固件中 PI/16 存储的 0o27 Bank 0o3355 address
  - netcat 连 172.17.0.1:19008 与 yaDSKY 交互
  - DSKY 协议发送 V27N02E 进入"读取 ROM"模式
  - 输入 0o57355（Bank×0o2000+addr-0o2000）按 ENTR 循环读 ROM
  - 在 PI/16 邻位找到 0o37777 标记反向读出两个 DP 字
  - 拼接 0o6413 0o11416 按 AGC DP 浮点格式解出 3.26103293895721435546875
key_payload: '0o6413 0o11416 → PI = 3.26103293895721435546875'
one_liner: VirtualAGC 复现 Apollo AGC 的 DSKY 命令，从 ROM rope-memory 中挖出被篡改的 PI/16 DP 值。
lesson: 历史向 CTF 考察领域知识（AGC 八进制 + Bank 寻址 + DP 浮点 + V/N 命令），解题关键是搞清 V27N02E 查表语义。
quality: high
---

# 有趣的 Hack-A-Sat 黑掉卫星挑战赛——被破坏的阿波罗计算机（解法一）

**来源**: ctfiot.com ID 97721（出书《Hack-A-Sat 太空信息安全挑战赛深度解析》节选）

## 题目背景
2020 年美国白宫发布首份《航天政策第 5 号令》太空网络空间安全指令，同年起举办 Hack-A-Sat 大赛。本题出自"apollo_gcm"——基于阿波罗导航计算机 AGC（Apollo Guidance Computer），被藏在其中的 PI 值被偷偷改了一点，选手要通过 DSKY 找出来。

## 关键知识点
- **AGC 硬件**：RAM 2048 字 × 15 bit / ROM 36864 字 × 15 bit / 85000 指令/秒 / 28V 5A 供电
- **线存储器（rope memory）**：磁环改变电压状态，1 个字 15 bit + 1 bit 奇偶校验
- **Bank 寻址**：1 Bank = 1024 字，Bank×0o2000 + addr - 0o2000 = 实际地址（如 0o27 Bank 0o3355 = 0o57355）
- **DSKY 命令**：V27N02E 进入"读 ROM 数据"模式 → 输入 address → ENTR
- **AGC 双精度浮点 DP**：2 个 15 bit 字，字 1 第 15 位符号位 + 高位有效位，字 0 低位有效位

## 解题步骤
1. **定位 PI/16 存储位置**：VirtualAGC 源码检索 Commanche055 固件，PI/16 存在 0o27 Bank 0o3355 address
2. **连接 DSKY**：netcat 172.17.0.1:19008 进入 yaDSKY 模拟器
3. **V27N02E + address 0o57355**：从 PI/16 位置开始往后读 ROM，直到碰到 0o37777 终止符
4. **回退读出 2 个 DP 字**：得到 0o6413 0o11416
5. **DP 解码**：(0o6413×2^14 + 0o11416) / 2^28 × 16 = 3.26103293895721435546875

## 复现要点
- `make build` + `make test` 在 Ubuntu 14.04 32 位（Virtual AGC 仅支持 32 位 Linux）
- 用阿里云 Debian bullseye 镜像 sources.list 加速 python:3.7-slim
- 测试 30-60 秒后输出 PI 值

## 工具链
VirtualAGC（yaDSKY）+ Python + DSKY V/N 协议 + 八进制寻址

## 评价
历史向高难度题，结合 1960 年代计算机体系结构（八进制 + Bank + DP float + DSKY）。解法优雅，揭示了 AGC 寻址公式的精妙。适合作为航天/嵌入式/复古计算 CTF 教学案例。
