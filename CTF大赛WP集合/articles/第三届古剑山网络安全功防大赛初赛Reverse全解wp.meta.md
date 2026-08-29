---
title: 第三届古剑山网络安全功防大赛初赛Reverse全解wp
contest: 第三届古剑山网络安全功防大赛初赛
year: 2025
difficulty: hard
vuln_type: reverse
tags: [古剑山RE全解, base64+rc4+0x22222222异或, HelloWorld字节码, VM opcodes 0x101-0x504, sys_ptrace反调试, RC4加密, CVE-2010-2967 VxWorks固件]
attack_chain: easyre(base64+rc4+0x22222222异或)→HelloWorld(字节码v3[idx]=v28[src_idx] op=3)→veryez(VM opcodes 0x101/0x102/0x103/0x201/0x202/0x203)→babyre(sys_ptrace反调试+RC4 key="is_good}")→final(VxWorks固件+CVE-2010-2967 loginDefaultEncrypt hash)
key_payload: "easyre:异或0x90504956+0x22222222+RC4+base64;HelloWorld字节码(v3[idx]=v28[src_idx] op=3);VM opcodes 0x101 add, 0x102 and, 0x201 sub;RC4 key='is_good}';VxWorks PowerPC + loginDefaultEncrypt CVE-2010-2967"
one_liner: 古剑山初赛Reverse全解5题：easyre RC4+异或+HelloWorld字节码+VM+RC4 key is_good}+VxWorks固件
lesson: RE题常见组合：字节码VM+字符串异或+RC4；固件逆向CVE编号对应函数
quality: high
---

# 第三届古剑山网络安全功防大赛初赛Reverse全解wp

**赛事**：第三届古剑山初赛（2025）

**Reverse全解5题**：

**1. easyre（签到题）**
- 逻辑：base64 → RC4 → 异或
- 关键：v7的判断决定11组密文是否再和0x22222222异或
- 总体异或密钥流：
  ```
  00 00 00 00 22 22 22 22 22 22 22 22 22 22 22 22 22 22 22 22 
  00 00 00 00 00 00 00 00 00 00 00 00 
  22 22 22 22 22 22 22 22 
  00 00 00 00
  ```
- Cyberchef逆序解密：异或0x90504956(v12) → 异或密钥流 → RC4解密 → base64解密

**2. Helloworld（字节码生成）**
- 操作码Buffer解析：每2字节一个操作
- 高4位op = (d1 >> 4) & 0xF
- 低4位idx = d1 & 0xF
- op=3：v3[idx] = v28[src_idx]（精确赋值）
- v28 = "abcdefghijklmnopqrstuvwxyz"
- 目标：v3[0:10] = "HelloWorld"
- 用op=3设小写+op=1转大写

**3. veryez（VM题）**
- dword_408254存操作码VM code
- 0x101: add, 0x102: and, 0x103: exit, 0x104: push const, 0x105: read int
- 0x201: sub, 0x202: or, 0x203: jmp, 0x205: print
- 0x304: call gets, 0x401: cmp, 0x504: byte load
- Key: viryualM（v3+后续加密）

**4. babyre（反调试+RC4）**
- sys_ptrace反调试
- 运行后patch掉qword_6D1D60
- RC4加密，key为flag后半段"is_good}"
- Cyberchef解密

**5. final（VxWorks固件+CVE-2010-2967）**
- patch.bin → binwalk -e 提取385二进制
- VxWorks 2.5系统
- PowerPC架构，大端序
- 基址 0x10000
- 指令多以0x7C开头
- 符号表位置：0x301E74
- 漏洞函数：loginDefaultEncrypt (CVE-2010-2967)
- 符号表格式：name_offset (4B) + func_offset (4B) + sym_type (4B) + reserved (4B)
- sym_type = 0x500 为函数
- IDA恢复符号 → 找hash算法
- 输入"SimpleXue"计算哈希 → flag格式提交

**核心技术**：
- 5道RE题综合：RC4+异或+字节码+VM+反调试+VxWorks固件
- VxWorks符号表解析（大端序+0x500函数类型）
- sys_ptrace反调试patch

**质量评估**：高（5题全解 + 完整代码 + 固件逆向）
