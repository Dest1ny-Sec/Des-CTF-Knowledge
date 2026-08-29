---
title: FE-CTF 2022: Cyber Demon – Blackbox
contest: FE-CTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [pwn, black-box, recon, fuzzing, binary-fuzz, eof-detection]
attack_chain:
  - file: data 二进制格式
  - hexdump查看80 42 4d 8a 40 38魔数
  - nc blackbox.hack.fe-ctf.dk 1337
  - proof-of-work: disabled
  - 发送空行触发返回
  - 4字节EOF关闭连接
  - recon fuzz测试不同输入
key_payload: b'\n'  # 触发返回
one_liner: FE-CTF Cyber Demon Blackbox：黑盒fuzz测试+EOF检测
lesson: 黑盒题先试简单输入观察响应
quality: medium
---

# FE-CTF 2022: Cyber Demon – Blackbox

## 题目信息
- 比赛：FE-CTF 2022
- 题目：Cyber Demon – Blackbox
- 类别：PWN 黑盒
- 服务：blackbox.hack.fe-ctf.dk:1337

## 关键攻击链
### 1. 文件分析
```bash
$ file file
file: data  # 未知格式
$ hexdump -C file
00000000  80 42 4d 8a 40 38 00 00 28 54 00 8a 29 7c 2a 05
00000010  28 d0 82 02 28 01 00 20 00 03 2a 79 01 c3 0e 00
00000020  e2 0a d4 ff 87 e9 d3 9b 42 47 52 73 17 df bf 77
00000030  2f 07 01 04 07 04 f0 5e 2a 12 ff e2 c6 87 47 8f
00000040  07 07 07 01 6b 52 15 e2 ff c6 07 07 07 07 07 a7
```
- 头部 `80 42 4d 8a 40 38 00 00` 非标准 magic

### 2. 服务交互
```python
from pwn import *
sock = remote('blackbox.hack.fe-ctf.dk', 1337)
for i in iters.count(1):
    sock.send(b'\n')
    print(f'sent {i} bytes')
    print('>>>', sock.recv(timeout=1))
```
- 多次发送空行
- 第 4 字节后 EOF 关闭连接

### 3. fuzz 测试
- 逐字节发送测试响应
- 异常响应 → 协议识别线索
- 黑盒逆向从异常入手

## 评分
- quality: medium（黑盒 fuzz 思路 + 4 字节 EOF 触发关闭）
