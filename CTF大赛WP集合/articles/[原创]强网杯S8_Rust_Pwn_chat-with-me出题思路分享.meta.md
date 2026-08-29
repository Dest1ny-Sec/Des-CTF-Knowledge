---
title: [原创] 强网杯 S8 Rust Pwn chat-with-me 出题思路分享
contest: 强网杯 S8 (强网杯 2024)
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [rust_static_lifetime, cve_rs_extension, vec_realloc_arbitrary_addr, msg_list_poisoning, arb_write_via_rax_pop_rdi, msg_static_mut_ref_lifetime_extension, ctf_qwb_rust, show_leak_addr, rust_unsafe_misuse]
attack_chain: Rust cve-rs UIUCTF 2024 Rusty Pointer POC + get_ptr 函数生命周期扩展返回 &'static mut Msg → add/show/edit/delete 5 菜单 (Vec<&'static mut Msg>) → show 0 泄 stack+elf+heap 地址 → edit(0) 伪造 0x91 堆块劫持 vec 指针数组 → arb_qword 任意写 8 字节 → 多轮 ROP 链写返回地址 → pop_rdi+pop_rsi+pop_rax+syscall execve /bin/sh
key_payload: const S: &&() = &&(); let f: fn(_, &'a mut T) -> &'b mut T = ident / vec 三指针 start/finish/end_of_storage realloc / arb_qword: edit(1, p64(0)*5+p64(0x51)+p64(addr)) + edit(0, qword) / ret_addr = stack_addr+0x3D0
one_liner: 强网杯 S8 Rust Pwn chat-with-me：cve-rs 静态生命周期扩展 POC + Vec<&'static mut Msg> 指针数组劫持 + 任意 8 字节写 + ROP 链 execve /bin/sh。
lesson: Rust cve-rs 项目暴露了生命周期扩展的 UAF 漏洞；Vec 内部是 realloc 扩容的指针数组，可通过堆块伪造劫持；Rust PWN 出题关键是"如何在无 unsafe 的代码里构造漏洞"。
quality: high
---
