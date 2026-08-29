---
title: corCTF 2024 - the conspiracy writeup
contest: corCTF
year: 2024
difficulty: easy
vuln_type: crypto_oracle
tags: [asymmetric, ascii, simple-divide, packet, network]
attack_chain:
  - 解析 CSV 源/目的/消息
  - 按 num%2 奇偶分流 message_list / key_list
  - 密文 / 密钥 得明文
  - ascii 除法还原
key_payload: 密文 = ascii(字符) * random(1-100)
one_liner: corCTF 2024 misc 入门题，密文 = 明文 ASCII × 随机 key 的简单除法。
lesson: 即使加密看起来"每次随机"，只要没有 padding/modulo，密文/密钥直接除回来就是明文。
quality: low
---

corCTF 2024 一道入门级 misc/crypto 题。原题 8 张图，本 WP 把核心逻辑整理成 1 段 Python：

```python
message_num_list = [[1234, 578, 325], [5958, 4828, 1234, 2222], [2222]]
key_list = [[10, 20, 30], [11, 24, 32, 13], [42]]
# 密文 = ord(char) * random(1..100)
# 3104 / 32 = 97  -> 'a'
```

加密函数读消息中每个字符转为 ASCII，再随机 1-100 的整数 key，密文 = ascii × key。发送方按顺序把密文 + key 都打包发出。

接收端用 Python socket 按 `num % 2 != 0` 区分密文和 key，分别 append 进 message_num_list 和 key_list。最后逐字符 `int(cipher) / int(key)` 还原明文。

题目 trivial，主要考"看到奇偶分流要立刻反应过来密文与 key 一定分开发"。
