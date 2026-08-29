---
title: 红明谷 2024/dualrsa
contest: 红明谷
year: 2024
difficulty: hard
vuln_type:
- crypto_rsa
- lsb_oracle
- rce
tags:
- RSA
- eval
- LSB Oracle
- gmpy2.iroot
- 双层 RSA
- 整数根求解
attack_chain:
- 审计 RSASystem 类发现 encrypt/decrypt 接受字符串
- encrypt/decrypt 内部 try: pow(eval(m), e, n) 存在 eval 漏洞
- eval 被限制，只能短字符串触发
- 构造 b"__import__('os').system('ls')" + \xff 填充到 512 字节
- 走 83 次方根（外层 RSA e=83）求 m
- 提交 m 让服务端 encrypt 后转字符串触发 eval
- 利用 LSB Oracle（选项 3 + decrypt）逐字节还原 flag
key_payload: "rce = b\"__import__('os').system('ls')\" + b'\\xff' * (512 - len(rce)); m = gmpy2.iroot(bytes_to_long(rce), 83)[0]"
one_liner: 83 次方根求 RCE 字符串 + eval 触发 + LSB Oracle 还原 flag
lesson: RSA 加密函数中 eval 漏洞用 iroot 求整数根构造可执行 Python 字节；LSB Oracle 配合多步签名链路还原明文
quality: medium
---

# 红明谷 2024/dualrsa

**83 次方根求 RCE 字符串 + eval 触发 + LSB Oracle 还原 flag**

> 红明谷 · 2024 · hard · crypto_rsa/lsb_oracle/rce · quality=medium
> 思路: 审计 RSASystem 类发现 encrypt/decrypt 接受字符串 → encrypt/decrypt 内部 try: pow(eval(m), e, n) 存在 eval 漏洞 → eval 被限制，只能短字符串触发 → 构造 b"__import__('os').system('ls')" + \xff 填充到 512 字节 → 走 83 次方根（外层 RSA e=83）求 m → 提交 m 让服务端 encrypt 后转字符串触发 eval → 利用 LSB Oracle（选项 3 + decrypt）逐字节还原 flag
> 套路: RSA 加密函数中 eval 漏洞用 iroot 求整数根构造可执行 Python 字节；LSB Oracle 配合多步签名链路还原明文

**关键 payload**:
```python
rce = b"__import__('os').system('ls')" + b'\xff' * (512 - len(rce))
m = gmpy2.iroot(bytes_to_long(rce), 83)[0]
```
