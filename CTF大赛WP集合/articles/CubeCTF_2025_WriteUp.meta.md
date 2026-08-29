---
title: CubeCTF 2025 WriteUp
contest: CubeCTF 2025
year: 2025
difficulty: medium
vuln_type: reverse
tags: [forensics, reverse, pcap, 流量分析, ELF, 后门逆向, 加密通信]
attack_chain:
  - pcap筛选tcp.flags==0x0018 [PSH,ACK]
  - 发现攻击者执行id, nc -lvp 2025 > /tmp/xcat传输ELF
  - 三段TCP重组为ELF文件/tmp/xcat
  - /tmp/xcat -l 2025加密传输密文到/tmp/supersecret
  - 逆向xcat解密sub_15D0(sub_16A0(s1))双重函数
  - 还原6段密文得到明文
key_payload: tcp.flags == 0x0018; nc -lvp 2025 > /tmp/xcat
one_liner: CubeCTF 2025 Operator取证题，pcap提取ELF后门逆向解密
lesson: 多段TCP重组需按顺序拼接；自写加密工具逆向需识别sub_15D0/sub_16A0
quality: high
---

# CubeCTF 2025 WriteUp

## 题目信息
- 比赛：CubeCTF 2025（作者获得第 40 名）
- 类别：Forensics / Reverse
- 题目：Operator（综合取证+逆向）

## 关键攻击链
1. **PCAP 流量分析**：
   - 筛选 `tcp.flags == 0x0018`（PSH,ACK）
   - 流 58338→1776：执行 `id` 返回 `uid=0(root) gid=0(root) groups=0(root)`
   - 流 58338→1776：`nc -lvp 2025 > /tmp/xcat` 启动接收
2. **ELF 传输**：
   - 流 47924→2025 三段 TCP 传输 ELF 文件
   - `chmod +x /tmp/xcat` + `/tmp/xcat -l 2025 > /tmp/supersecret`
3. **逆向 xcat ELF**：
   - `main(n3, a2, a3)`：判断 `-l` 参数
   - 无 `-l`：`sub_16A0(s1)` 加密
   - 有 `-l`：`sub_15D0(v7)` 解密
4. **解密 6 段密文**：
   - 流 53930→2025 共 6 段密文
   - 调用 xcat 解密还原 /tmp/supersecret

## 关键技术点
- TCP PSH+ACK 过滤
- nc 多段传输 ELF 重组
- ELF 反编译 sub_15D0 / sub_16A0 双重加解密
- 6 段密文拼接还原

## 评分
- quality: high（PCAP 分析 + ELF 提取 + 逆向解密完整链路）
