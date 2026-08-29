---
title: Realworld CTF 2023 - Ferris_proxy 逆向分析
contest: Realworld CTF 2023
year: 2023
difficulty: high
vuln_type: crypto_oracle
tags: [rust, reverse, custom-protocol, rc4-encrypt, rsa-key-exchange, aes-128-cbc, sha256-hmac, pcapng, serde-yaml]
attack_chain:
  - Rust binary (有符号) server 监听 8888 + client 二进制
  - 协议: TCP 包头 12 字节 = length(4) + action(4) + streamid(4)
  - action 0=open / 1=transfer / 2=close
  - rc4 全流量加密 + 密钥 explorer
  - serde_yaml::from_str 读硬编码 RSA 密钥
  - RSA 公钥加密 AES 密钥 = key_exchange
  - rsa_encrypt 自己的随机数 + rsa_decrypt 对方随机数
  - AES 密钥 = 双方随机数 ZIP XOR (rust 同域匿名函数)
  - 每个 stream 都进行 key_exchange: 256 字节 RSA + 2 字节长度 (0100) + AES key sha256
  - aes_128_cbc IV 每次 16 字节新生成
  - 包头: 4 字节 length + 16 字节 IV
  - 完整解密: 拆 c2s/s2c 流 → 解析 streamid → RSA 解 AES key → 算 XOR 双方 key
  - SHA256 校验双方 AES key
  - 找到 HTTP/1.0 200 OK SimpleHTTP/0.6 Python/3.6.9 响应
  - flag.txt 内容: rwctf{l1fe_1s_sh0rt_DO0...}
  - 提示: rust 闭包 + zip + map lambda (a^b) 计算 AES key
key_payload: d_lst[streamid] = concat(0x0100+RSA(rand_self)+RSA(rand_other)) + SHA256(aes_key) + AES_CBC(data, iv)
one_liner: Realworld CTF 2023 Ferris_proxy：Rust 协议逆向 (有符号) + pcapng 全流量 rc4 解密 + RSA 加密 AES 密钥交换 + AES-128-CBC IV 16 字节 + ZIP XOR 双方 key。
lesson: Rust 协议逆向关键是找闭包 (a^b) = zip+map 模式；rc4 全流量加密是初阶 (key=explorer)；RSA+AES key_exchange 模式在 4 stream 中重复；SHA256(aes_key) 校验保证双方 key 一致。
quality: high
---
