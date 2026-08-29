---
title: Real World CTF 5 - Teewars (Teeworlds) Writeup
contest: Real World CTF 5
year: 2022
difficulty: high
vuln_type: pwn_unknown
tags: [teeworlds, map-file, cdatafile-format, zlib, env-point, integer-overflow, rop, execve, ctf-pwn]
attack_chain:
  - Teeworlds (DDNet) 自定义 CDataFile 格式: header(40) + item_types + item_offsets + data_offsets + data_sizes + items + zlib deflate data
  - 头 40 字节: aID[4]="DATA" + Version + Size + Swaplen + NumItemTypes + NumItems + NumRawData + ItemSize + DataSize
  - CDatafileItem m_Type: Version=0/Info=1/Image=2/Envelope=3/Group=4/Layer=5/Envelope_Points=6
  - Envelope_Points 解析: m_Size/sizeof(CEnvPoint) 数组 + POINT_VERSION
  - CEnvPoint m_Time + m_Curvetype + m_aValues[4] 22.10 fixed point
  - 漏洞: envelope channel 数量 + 数组 size 计算溢出
  - 准备 prepared.map 复制 start + 改 num_channels
  - 攻击: 改 0x24c 偏移 4 字节 = (len(rop_chain) + 0x90) / 4 整数除法
  - 复制 items 0x250-0x750+0x90 + ROP chain 覆盖 buffer
  - ROP: pop rdi 0x6c0000 bss + pop rax argv strings + mov [rdi],rax + execve 59
  - 完整 chain: 写 argv[0]="/bin/sh" + argv[1]="-c" + argv[2]="cat /home/rwctf/flag" → execve("/bin/sh", argv, 0)
  - 服务端: rwctf 5 - Teewars 服务器崩溃后 crash 分析
key_payload: 0x45f135 mov qword ptr [rdi], rax; ret + rop.rax + rop.rdi + rop.rsi + rop.rdx + rop.syscall
one_liner: Real World CTF 5 Teewars (Teeworlds) 自定义 map 文件 CDataFile 格式 Envelope_Points 整数除法溢出 + 写 ROP 链到 bss 触发 execve /bin/sh -c "cat /home/rwctf/flag"。
lesson: 自定义二进制文件格式 (CDataFile) 解析时整数除法溢出是经典漏洞 (size/count → 负数 → 后续 memcpy 越界)；Teeworlds/DDNet 引擎 ROP 利用 bss 段写入 argv 是无 shellcode 场景必备。
quality: high
---
