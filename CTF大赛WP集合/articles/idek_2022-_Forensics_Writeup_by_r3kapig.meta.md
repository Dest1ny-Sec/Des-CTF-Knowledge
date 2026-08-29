---
title: idek 2022: Forensics Writeup by r3kapig
contest: idekCTF
year: 2022
difficulty: hard
vuln_type: forensic_memory
tags: [pgp-private-key, gpg2john, hashcat-17010, rockyou, netascii-7z, ssh-aes-gcm, network-parser, openssh, pidstat, volatility, proc-mem]
attack_chain:
  - PGP 私钥 gpg2john → hashcat -m 17010 爆破
  - Netascii 7z 修复 (CR/LF 替换)
  - SSH AES-GCM 密钥 + IV 解析
  - network-parser 解密 SSH 流量
  - proc mem 提取 root 密码
  - 总结报告
key_payload: PGP 爆破 + Netascii 修复 + SSH AES-GCM 解密
one_liner: idekCTF 2022 r3kapig 战队 Forensics 套题，PGP+SSH+流量+内存取证综合。
lesson: 真实企业环境中 PGP/SSH 凭据泄露是高频事件，forensic 套题模拟完整流程。
quality: high
---

idekCTF 2022 r3kapig 战队 Forensics 完整套题复盘。

**阶段 1：PGP 私钥爆破**
```bash
gpg2john 1.txt > hash.txt
hashcat -m 17010 hash.txt -a 0 ./webtools/rockyou.txt --force
```
爆破 PGP 私钥口令（rockyou 字典）。

**阶段 2：Netascii 7z 修复**
Netascii 是 ASCII 的 8-bit 扩展，定义在 RFC 764：
- 0x20-0x7F（可打印字符 + 空格）
- 8 个控制字符（含 NUL 0x00、LF 0x0A、CR 0x0D）
- 主机端 EOL 必须翻译为 CR+LF 传输

```python
data = open('Confidential.7z', 'rb').read()
data = data.replace(b'\x0d\x0a', b'\x0a').replace(b'\x0d\x00', b'\x0d')
open('out.7z', 'wb').write(data)
```

**阶段 3：SSH AES-GCM 流量解密**
从 sshd 内存提取 key + iv：
```json
{"task_name": "sshd", "sshenc_addr": 94122048527088, "cipher_name": "aes256-gcm@openssh.com",
 "key": "895688678410a0b9b358b0b04ab909d49333791e864c89593c66d5ce5083b8e5",
 "iv": "40e87818bef3d68c45c9a9f5"}
```
然后用 `network-parser` 解析 pcapng 提取 SSH 流：
```bash
network-parser -p Stealth.pcapng --popt keyfile=key.json --proto ssh -o dump/
```

**阶段 4：进程内存取证**
用 `volatility` / `vol3` 提取 root 密码等敏感信息。

整题模拟企业渗透测试中"网络流量 + 凭据 + 内存"完整取证链。
