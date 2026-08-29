---
title: 祥云杯 2022/Misc super_electric
contest: 祥云杯
year: 2022
difficulty: hard
vuln_type:
- stego_traffic
- reverse
- block_cipher
tags:
- MMS 协议
- 工控流量分析
- tshark 提取
- MZ 头识别
- 反调试
- 自解压壳
- AES/CBC/PKCS7
- IV 还原
attack_chain:
- 拿到 pcapng 流量，IPv4-TCP-MMS 占绝大多数，确认是 MMS 协议
- 过滤 mms.confirmedServiceRequest，发现 LLN0$CO$FunEna1$Oper / FunEna2$Oper 两种
- FunEna2$Oper 一直是 172.20.1.23（无用），FunEna1$Oper 是 4d5a9000 开头的 exe
- tshark 提取 mms.octet_string 字段 → data.txt（hex 串）
- 拼 hex 写回 test.exe，发现是带窗口的 Windows 程序
- 找输入校验逻辑：常量 C96F278C370C43299F1EE98257CCBD8A + dword_449CB0 = memcmp
- 输入正确后用 x32dbg 看后续：SendMessageA WM_CLOSE 关闭窗口
- 找脱壳逻辑：sub_43CD50 创建窗体后跟内存处理 → 最后当函数调用的内存块
- 反调试插桩：sub_43D2A0 触发异常，nop 掉
- 脱壳后 IDA 找真实 main：byte_42D624 与输入异或 0x89 比较
- 还原 byte_42D624 的异或下标 [0, 717) 解出 Python 脚本
- Python 脚本：已 sha256(key)[:10] 拼 message + AES/CBC/PKCS7 + 已知明文 → IV 还原
- 用 padding 特性（最后 2 字节 = 0x02 0x02）爆破 16 字节 key
- 倒推 IV 还原 flag{72713126e9b90eab}
key_payload: "data = b''; [data += bytes.fromhex(line.strip()) for line in open('data.txt')]; open('test.exe','wb').write(data)"
one_liner: MMS 工控流量 tshark 提取 exe → 反调试脱壳 → XOR 解出 Python 还原脚本 → AES/CBC padding 爆破 key 倒推 IV
lesson: MMS 协议工控场景下 mms.itemId 字段可作为 exe 二进制传输通道；AES/CBC 已知 message 倒推 IV 是经典 padding oracle 反向题
quality: high
---

# 祥云杯 2022/Misc super_electric

**MMS 工控流量 + tshark 提取 exe + 反调试脱壳 + AES/CBC 倒推 IV**

> 祥云杯 · 2022 · hard · stego_traffic/reverse/block_cipher · quality=high
> 思路: 拿到 pcapng 流量，IPv4-TCP-MMS 占绝大多数 → 过滤 mms.confirmedServiceRequest → FunEna1$Oper 是 4d5a9000 exe → tshark 提取 → 反调试脱壳 → XOR 解出 Python → AES/CBC padding 爆破 key → 倒推 IV
> 套路: MMS 协议工控场景下 mms.itemId 字段可作为 exe 二进制传输通道；AES/CBC 已知 message 倒推 IV 是经典 padding oracle 反向题

**关键 payload**:
```python
data = b''
[data += bytes.fromhex(line.strip()) for line in open('data.txt')]
open('test.exe','wb').write(data)
```
