---
title: PWN入门 - 制服 _dl_runtime_resolve
contest: 看雪论坛 ctfiot 系列
year: 2024
difficulty: high
vuln_type: pwn_unknown
tags: [pwn, 教程, glibc, dynamic-linking, _dl_runtime_resolve, _dl_fixup, lazy-binding]
attack_chain:
  - 介绍 ELF 动态链接的两类时机：启动期 vs 调用期（延迟绑定）
  - 详解 .plt/.plt.sec/.got/.got.plt/.rela.plt/.dynsym/.dynstr 协同工作
  - PLT jmp *GOT_ENTRY 触发首次 push reloc_index + jmp _dl_runtime_resolve
  - _dl_runtime_resolve_fxsave 序言 push rbx / mov rsp,rbx / and 0x10 对齐 / sub 0x240
  - 保存 6 个参数寄存器 (rax/rcx/rdx/rsi/rdi/r8/r9) 到栈
  - fxsave 0x40(%rsp) 保存 FPU/MMX/SSE 上下文
  - 从 rbx 取 link_map+reloc_index 调 _dl_fixup
  - _dl_fixup 解析 link_map[0x70] 取 SYMTAB，l_info[] 检索
  - version check + strcmp 匹配 GLIBC_x.y
  - 返回值 r11，最后 jmp *r11 真正调到目标函数
key_payload: A=arch JT=0x00 ... 0006: 0x15 0x00 0x0d 0xc000003e (BPF 过滤 read/write/open)
one_liner: 深度逆向 glibc 动态链接器 _dl_runtime_resolve_fxsave 内部，从 PLT 跳转到 _dl_fixup 查找符号的完整调用链。
lesson: GOT[plt] 首次未解析时跳 _dl_runtime_resolve 触发解析；解析完成后 GOT 写入真实函数地址；_dl_fixup 通过 link_map[0x70] 取 SYMTAB 再用 strcmp 验证 GLIBC 版本号。
quality: high
---
