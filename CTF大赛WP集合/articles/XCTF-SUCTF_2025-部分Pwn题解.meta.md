---
title: XCTF-SUCTF 2025-部分 Pwn 题解
contest: SUCTF 2025
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [custom_command, syscall_open_read_write, pwntools_shellcraft, oob_write_neg_offset, heap_to_buf_leak_libc, buf_to_heap_edit, custom_vm_xor_opcode, pwntools_disasm, libc_2_35]
attack_chain: SU_baby:命令菜单 1/2/3 + addfile(name, content) 写多次 → 输入 nop nop nop 触发 gadget 0x04028A6 → shellcraft.open('flag') + read('rax','rsp',0x40) + write(1,'rsp',0x40) shellcode 直接弹 / SU_text:add(0,0x418) + add(1,0x418) + rm(0) + add(0,0x418) 堆布局 → heap_to_buf(0) 自定义指令 0x15 写 buf 指针到栈 → write(0,0xffffffe7+8) OOB 读 → leak libc_base = uu64(r(8)) - 0x203b20 → buf_to_heap(0, 0, 0) + buf_to_heap(0, 8, 0) 改堆指针 → add(2,0x428) + add(3,0x428) pad + add(4,0x418)
key_payload: gadget=0x04028A6 (mov edi,eax; push rsp; pop rsi; syscall) / sc=asm(shellcraft.open('flag'))+asm(shellcraft.read('rax','rsp',0x40'))+asm(shellcraft.write(1,'rsp',0x40)) / libc_base = uu64(r(8)) - 0x203b20 / heap_to_buf(0) + write(0,0xffffffe7+8) OOB
one_liner: SUCTF 2025 imLZH1 两道 Pwn 题解：SU_baby 自定义命令菜单触发 syscall(open+read+write flag) + SU_text 自定义指令集 (0x10/0x11/0x12/0x14/0x15) heap OOB 改 buf 指针泄 libc。
lesson: pwntools shellcraft.open+read+write 是 shellcode 速写标配；自定义指令集逆向时先用 0x10/0x11/0x12 等 opcode 编号+操作数长度暴力枚举是快速理解捷径。
quality: high
---
