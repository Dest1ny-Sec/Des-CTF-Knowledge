---
title: aliyunctf 2025 beebee 题目详解
contest: aliyunCTF 2025
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [linux_kernel_patch, bpf_helper_add, bpf_aliyunctf_xor, kernel_check_mem_access, verifier_crash, bpf_call_3_arg_proto, custom_bpf_func, kernel_pwn, oob_in_helper]
attack_chain: Linux 内核 patch: BPF_FUNC_aliyunctf_xor = 212 (新增) + bpf_aliyunctf_xor_proto = bpf_func_proto {func, gpl_only=false, ret_type=RET_INTEGER, arg1=ARG_PTR_TO_MEM|MEM_RDONLY, arg2=ARG_CONST_SIZE, arg3=ARG_PTR_TO_FIXED_SIZE_MEM|MEM_UNINIT|MEM_ALIGNED|MEM_RDONLY, arg3_size=sizeof(s64)} → BPF_CALL_3: s64 _res=2025; if buf_len!=sizeof(s64) return -EINVAL; _res ^= *(s64*)buf; *res=_res; return 0 → BPF 程序调用 212 时触发 OOB 越界
key_payload: bpf_aliyunctf_xor(buf, buf_len=sizeof(s64)=8, res) / _res=2025; _res ^= *(s64*)buf; *res=_res / check_mem_access off=0x6 bpf_size=0x18 t=BPF_WRITE
one_liner: aliyunCTF 2025 beebee：Linux Kernel patch 添加自定义 BPF helper bpf_aliyunctf_xor (212) + verifier 越界 off=0x6 bpf_size=0x18 触发 check_mem_access 崩溃。
lesson: 给 Linux Kernel 加自定义 BPF helper 涉及 include/uapi/linux/bpf.h + include/linux/bpf.h + kernel/bpf/helpers.c + bpf_func_proto 结构体四文件 patch；BPF verifier check_mem_access 是关键防御。
quality: high
---
