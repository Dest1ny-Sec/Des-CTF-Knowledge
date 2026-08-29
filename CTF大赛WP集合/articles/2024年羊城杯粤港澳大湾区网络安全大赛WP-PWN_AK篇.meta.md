---
title: 2024 羊城杯 PWN AK 篇（4 题：pstack / Travel / C++String catch / bigbin HoA2）
contest: 2024 羊城杯粤港澳大湾区网络安全大赛
year: 2024
difficulty: hard
vuln_type: [rop, ret2libc, heap_exploit, srop]
tags: [pstack 控制 rbp, ret2libc, House of Apple 2, setcontext ORW, _IO_wfile_jumps, largebin attack, C++ String catch, system command]
attack_chain:
  - pstack: 0x10 字节溢出覆盖 rbp、leave;ret 二次跳到 bss 写 ROP
  - pstack: puts_plt(puts_got) 泄 libc → system("/bin/sh")
  - Travel: 增删改查菜单城市 + 大小堆 + 0x510 触发 largebin
  - Travel: 泄露 heap+libc → House of Apple 2 + setcontext 53 ROP
  - Travel: _IO_wfile_jumps -0x40 偏 0xc8 + orw pop_rdi/pop_rsi/pop_rdx 弹
  - C++: try/catch String 异常 → system(command) 直读 command 寄存器
  - bigbin: tcache+largebin overlap → UAF → House of Apple 2
key_payload: "payload = p64(bss)+p64(pop_rdi)+p64(bin_sh)+p64(ret)+p64(system)"
one_liner: 4 道堆栈综合：rbp 控 ret2libc、城市菜单 House of Apple 2 ORW、C++ String catch system、largebin 复用 HoA2——一题一 House of Apple 工业流水线。
lesson: pstack 0x10 字节溢出看上去不够拿 shell，但 leave;ret + 二次 leave 就能把栈劫到 bss 上 ROP；House of Apple 2 + setcontext 53 是 libc ≥ 2.34 失 _IO_str_overflow 后唯一通用 ORW 出口。
quality: high
---

# 2024 羊城杯 PWN AK 篇

4 道 PWN 全 AK，覆盖栈/堆/异常处理三件套：

## pstack（栈）
`.text:0x4006C4` 是 `read(0, rbp+buf, 0x40)`，主函数 `leave; ret` 收尾。  
0x10 字节溢出覆盖 rbp → `payload=b'a'*0x30+p64(bss)+p64(0x4006C4)` → 再次进 read，把 ROP 写到 bss，p64(bss-0x30)+leave;ret 把栈迁过去。  
`pop_rdi(puts_got)+puts_plt+main` 泄 libc → system("/bin/sh")。

## Travel（堆，House of Apple 2 + setcontext）
菜单支持 car/train/plane 三种交通方式增删改查+计算距离。  
`add(0,2,1, "x70")` 把 size 卡进 0x70 触发 `show` 泄 heap；`add(2,1,0, "A"*0x510)` 触发 largebin，`show` 泄 libc address。  
House of Apple 2 打法：  
- 劫持 `chunk` 到 `_IO_list_all - 0x20`  
- payload 头部放 p64(0)+p64(0x531)+p64(fd)*2+`chunk`  
- `_IO_wfile_jumps - 0x40` 写到 0xc8 偏移  
- 触发 `_IO_wfile_overflow` → `_wide_data->_wide_vtable->_doallocate`  
- 跳 `setcontext+53`，从 0xa0 起恢复 rdi/rsi/rdx/rcx/r8/r9，再 pop rsp 到 ROP_addr  
- ORW 链：open("/flag", 0) → read(3, buf, 0x30) → write(1, buf, 0x30)。

## C++ String catch（C++ 异常处理）
看到 `loc_401BD9: mov rdi, rax; call ___cxa_begin_catch` 跟紧的 `[rbp+command], rax; mov rax,[rbp+command]; mov rdi, rax; call _system` 就是典型 C++ try/catch String 漏洞——catch String 异常时直接 system(command)，command 由 record_data 写入。  
`record_data(p64(0x404020)*2)` 9 次堆出栈布局，最后 `record_data("/bin/sh")` 把 "/bin/sh" 写到 read_addr+0x18，再 `send_warning(b'x00'*0x70+p64(read_addr+0x18)+p64(0x401bc7))` 跳转触发 system("/bin/sh")。

## bigbin HoA2（largebin attack 重做）
菜单 9 chunk，`add(0,0x520)` + `add(1,0x508)` + `delete(0)` + `show(0)` 触发 unsorted bin 残留泄 libc。后续 `delete(2); delete(3); show(3)` 泄 heap，`add(5,0x558); add(7,0x548)` 触发 tcache→largebin 重叠，put `_IO_list_all` + `_IO_wfile_jumps` 第二次打 House of Apple 2 收尾。
