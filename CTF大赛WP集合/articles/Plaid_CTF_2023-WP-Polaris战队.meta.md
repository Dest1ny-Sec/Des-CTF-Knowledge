---
title: Plaid CTF 2023 - WP - Polaris 战队
contest: Plaid CTF 2023
year: 2023
difficulty: high
vuln_type: pwn_unknown
tags: [wine, windows-pwn, heap-overflow, ret2user, reverse, source-map, vlq, lfsr, mt19937]
attack_chain:
  - Emu Exploit Pwn (baby heap question mark): wine 启动 windows 程序
  - write 功能无长度限制 → 堆溢出
  - 第一个 node 堆地址在 node 地址结构前 → 溢出覆盖 node 结构任意读写
  - 中间内存备份后填充避开崩溃
  - node 指向栈地址 → ROP 调 execve("/getFlag", NULL, NULL)
  - SYS_execve = 59 syscall + pop rax/rdx/rdi/rsi + 0x21fad8 syscall gadget
  - The Check Reverse: PIE 程序 16 字节启动参数校验
  - GDB b *PIE+0xec56 断 CMP R12,[RAX] 计时爆破
  - 每个 idx 跑 26+26+10+1=63 字符 + starti 重新启动
  - Treasure Map Reverse Web: 200 个 .js 文件 + 0.js.map sourceMappingURL
  - VLQ 编码 + b64 alphabet 解析 source map mappings 字段
  - 还原每文件跳转关系 → 25 字符路径回溯到 success.js
  - Need+a+map/How+about+200!
  - CSS Reverse: 14 组 div × 3 字符 = 27^3=19683 组合
  - path top/left 滑动 + 78 details 折叠对齐
  - window.getComputedStyle.top 提取目标 top
  - Bivalves Crypto: LFSR 系统加密 + z3 恢复密码状态
  - Fastrology Crypto: 多个 JS 程序 alphabet[Math.floor(Math.random()*alphabet.length)]
  - 恢复内部随机状态预测后续输出
key_payload: b'dump_memory' (备份中间内存 0xa10 字节) + flat({0: 0x00000003af6b3fa9 pop rdx, 0x00000003af686040 pop rax, 0x00000003af686177 pop rdi, 0x00000003af68655a pop rsi, 0x00000003af67bb76 syscall}) + b'/getFlag0'
one_liner: Plaid CTF 2023 Polaris 第 4 名联合战队：wine Windows 堆溢出 ROP+execve 任意读写、GDB 计时爆破 16 字符、source map VLQ 解码还原 200 文件跳转路径、CSS path top 滑动对齐、MT19937/LFSR 密码恢复。
lesson: wine 调 Windows 堆题无地址随机化，gdb attach 直接用真实地址；sourceMappingURL 末尾 token 是 source map 路径，VLQ 编码 + b64 alphabet 是固定套路；Math.random() 实际是 MT19937 PRNG 可爆破。
quality: high
---
