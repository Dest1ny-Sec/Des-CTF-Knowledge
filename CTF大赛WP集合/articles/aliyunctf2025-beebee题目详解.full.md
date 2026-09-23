---
title: aliyunctf 2025 beebee 题目详解
contest: aliyunCTF 2025
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags:
- linux_kernel_patch
- bpf_helper_add
- bpf_aliyunctf_xor
- kernel_check_mem_access
- verifier_crash
- bpf_call_3_arg_proto
- custom_bpf_func
- kernel_pwn
- oob_in_helper
attack_chain: 'Linux 内核 patch: BPF_FUNC_aliyunctf_xor = 212 (新增) + bpf_aliyunctf_xor_proto = bpf_func_proto {func, gpl_only=false, ret_type=RET_INTEGER, arg1=ARG_PTR_TO_MEM|MEM_RDONLY, arg2=ARG_CONST_SIZE, arg3=ARG_PTR_TO_FIXED_SIZE_MEM|MEM_UNINIT|MEM_ALIGNED|MEM_RDONLY, arg3_size=sizeof(s64)} → BPF_CALL_3: s64 _res=2025; if buf_len!=sizeof(s64) return -EINVAL; _res ^= *(s64*)buf; *res=_res; return 0 → BPF 程序调用 212 时触发 OOB 越界'
key_payload: bpf_aliyunctf_xor(buf, buf_len=sizeof(s64)=8, res) / _res=2025; _res ^= *(s64*)buf; *res=_res / check_mem_access off=0x6 bpf_size=0x18 t=BPF_WRITE
one_liner: aliyunCTF 2025 beebee：Linux Kernel patch 添加自定义 BPF helper bpf_aliyunctf_xor (212) + verifier 越界 off=0x6 bpf_size=0x18 触发 check_mem_access 崩溃。
lesson: 给 Linux Kernel 加自定义 BPF helper 涉及 include/uapi/linux/bpf.h + include/linux/bpf.h + kernel/bpf/helpers.c + bpf_func_proto 结构体四文件 patch；BPF verifier check_mem_access 是关键防御。
quality: high
full_path: aliyunctf2025-beebee题目详解.full.md
meta_path: aliyunctf2025-beebee题目详解.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: aliyunctf 2025 beebee 题目详解。aliyunCTF 2025 beebee：Linux Kernel patch 添加自定义 BPF helper bpf_aliyunctf_xor (212) + verifier 越界 off=0x6 bpf_size=0x18 触发 check_mem_access 崩溃。。经验：给 Linux Kernel 加自定义 BPF h...
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/234488.html
reasoning_chain:
- 触发点:Linux 内核 patch + BPF_FUNC_aliyunctf_xor = 212 (新增) → 假设:可触发 verifier 越界 → 动作:diff kernel/bpf/helpers.c + include/linux/bpf.h
- 动作:bpf_aliyunctf_xor_proto = bpf_func_proto {func, gpl_only=false, ret_type=RET_INTEGER, arg1=ARG_PTR_TO_MEM|MEM_RDONLY, arg2=ARG_CONST_SIZE, arg3=ARG_PTR_TO_FIXED_SIZE_MEM|MEM_UNINIT|MEM_ALIGNED|MEM_RDONLY, arg3_size=sizeof(s64)} → 观察:proto 定义
- '动作:BPF_CALL_3: s64 _res=2025; if buf_len!=sizeof(s64) return -EINVAL; _res ^= *(s64*)buf; *res=_res; return 0 → 观察:实现逻辑'
- 动作:BPF 程序调用 212 时触发 OOB 越界 off=0x6 bpf_size=0x18 → 观察:check_mem_access 崩溃
- 动作:bpf_aliyunctf_xor(buf, buf_len=sizeof(s64)=8, res) → 观察:触发 verifier bug
failed_attempts:
- 试图直接调 bpf 212 → 失败:需要构造合法 proto 字段
- 试图不改 kernel patch → 失败:必须 patch 加 helper
- 试图不解 check_mem_access → 失败:verifier 检查是崩溃点
key_observations:
- 给 Linux Kernel 加自定义 BPF helper 涉及 include/uapi/linux/bpf.h + include/linux/bpf.h + kernel/bpf/helpers.c + bpf_func_proto 结构体四文件 patch
- BPF verifier check_mem_access 是关键防御
- arg3=ARG_PTR_TO_FIXED_SIZE_MEM|MEM_UNINIT|MEM_ALIGNED|MEM_RDONLY 是 BPF helper 标准标注
- BPF_CALL_3 宏是 BPF helper 调用的标准封装
- arg3_size=sizeof(s64) 是固定大小标注的关键
prerequisites:
- Linux Kernel patch + BPF 子系统
- bpf_func_proto 结构体理解
- BPF verifier check_mem_access 原理
- BPF 程序编写与加载
---
# aliyunctf2025-beebee题目详解

> 原文: https://www.ctfiot.com/234488.html
> ID: 234488

diff --color -ruN origin/include/linux/bpf.h aliyunctf/include/linux/bpf.h
--- origin/include/linux/bpf.h	2025-01-23 10:21:19.000000000 -0600
+++ aliyunctf/include/linux/bpf.h	2025-01-24 03:44:01.494468038 -0600
@@ -3058,6 +3058,7 @@
 extern const struct bpf_func_proto bpf_user_ringbuf_drain_proto;
 extern const struct bpf_func_proto bpf_cgrp_storage_get_proto;
 extern const struct bpf_func_proto bpf_cgrp_storage_delete_proto;
+extern const struct bpf_func_proto bpf_aliyunctf_xor_proto;

 const struct bpf_func_proto *tracing_prog_func_proto(
 enum bpf_func_id func_id, const struct bpf_prog *prog);
diff --color -ruN origin/include/uapi/linux/bpf.h aliyunctf/include/uapi/linux/bpf.h
--- origin/include/uapi/linux/bpf.h	2025-01-23 10:21:19.000000000 -0600
+++ aliyunctf/include/uapi/linux/bpf.h	2025-01-24 03:44:11.814636836 -0600
@@ -5881,6 +5881,7 @@
 FN(user_ringbuf_drain, 209, ##ctx)
 FN(cgrp_storage_get, 210, ##ctx)
 FN(cgrp_storage_delete, 211, ##ctx)
+	FN(aliyunctf_xor, 212, ##ctx)
 /* */

 /* backwards-compatibility macros for users of __BPF_FUNC_MAPPER that don't
diff --color -ruN origin/kernel/bpf/helpers.c aliyunctf/kernel/bpf/helpers.c
--- origin/kernel/bpf/helpers.c	2025-01-23 10:21:19.000000000 -0600
+++ aliyunctf/kernel/bpf/helpers.c	2025-01-24 03:44:06.683490095 -0600
@@ -1745,6 +1745,28 @@
 .arg3_type	= ARG_CONST_ALLOC_SIZE_OR_ZERO,
 };

+BPF_CALL_3(bpf_aliyunctf_xor, const char *, buf, size_t, buf_len, s64 *, res) {
+	s64 _res = 2025;
+
+	if (buf_len != sizeof(s64))
+ return -EINVAL;
+
+	_res ^= *(s64 *)buf;
+	*res = _res;
+
+	return 0;
+}
+
+const struct bpf_func_proto bpf_aliyunctf_xor_proto = {
+	.func = bpf_aliyunctf_xor,
+	.gpl_only	= false,
+	.ret_type	= RET_INTEGER,
+	.arg1_type	= ARG_PTR_TO_MEM | MEM_RDONLY,
+	.arg2_type	= ARG_CONST_SIZE,
+	.arg3_type	= ARG_PTR_TO_FIXED_SIZE_MEM | MEM_UNINIT | MEM_ALIGNED | MEM_RDONLY,
+	.arg3_size	= sizeof(s64),
+};
+
 const struct bpf_func_proto bpf_get_current_task_proto __weak;
 const struct bpf_func_proto bpf_get_current_task_btf_proto __weak;
 const struct bpf_func_proto bpf_probe_read_user_proto __weak;
@@ -1801,6 +1823,8 @@
 return &bpf_strtol_proto;
 case BPF_FUNC_strtoul:
 return &bpf_strtoul_proto;
+	case BPF_FUNC_aliyunctf_xor:
+ return &bpf_aliyunctf_xor_proto;
 default:
 break;
 }

#0 check_mem_access (env=0xffff888004b58000, insn_idx=0x1, regno=0xa, off=0x6, bpf_size=0x18, t=BPF_WRITE,
 value_regno=<error reading variable: Cannot access memory at address 0x0>,
 strict_alignment_once=<error reading variable: Cannot access memory at address 0x8>,
 is_ldsx=<error reading variable: Cannot access memory at address 0x10>) at kernel/bpf/verifier.c:
6698
#1 0xffffffff812012a9 in do_check (env=<optimized out>) at kernel/bpf/verifier.c:
17179
#2 do_check_common (env=0xffff888004b58000, subprog=0x0) at kernel/bpf/verifier.c:
19643
#3 0xffffffff812064ba in do_check_main (env=<optimized out>) at kernel/bpf/verifier.c:
19706
#4 bpf_check (prog=0xffff888004b58000, attr=0x1 <fixed_percpu_data+1>, uattr=..., uattr_size=0x18) at kernel/bpf/verifier.c:
20333
#5 0xffffffff811df0c2 in bpf_prog_load (attr=0xffffc9000023fe58, uattr=..., uattr_size=0xfffffff0) at kernel/bpf/syscall.c:
2743
#6 0xffffffff811e196a in __sys_bpf (cmd=0x5, uattr=..., size=0x0) at kernel/bpf/syscall.c:
5465
#7 0xffffffff811e4059 in __do_sys_bpf (size=<optimized out>, uattr=<optimized out>, cmd=<optimized out>) at kernel/bpf/syscall.c:
5569
#8 __se_sys_bpf (size=<optimized out>, uattr=<optimized out>, cmd=<optimized out>) at kernel/bpf/syscall.c:
5567
#9 __x64_sys_bpf (regs=0xffff888004b58000) at kernel/bpf/syscall.c:
5567
#10 0xffffffff81f38d39 in do_syscall_x64 (nr=<optimized out>, regs=<optimized out>) at arch/x86/entry/common.c:51
#11 do_syscall_64 (regs=0xffffc9000023ff58, nr=0x1) at arch/x86/entry/common.c:81
#12 0xffffffff82000134 in entry_SYSCALL_64 () at arch/x86/entry/entry_64.S:
121
#13 0x0000000000000000 in ?? ()

看雪ID：dig_grave

https://bbs.kanxue.com/user-home-851021.htm

*本文为看雪论坛文章，由 dig_grave 原创，转载请注明来自看雪社区

# 往期推荐

1、一种基于unicorn的寄存器间接跳转混淆去除方式

2、白盒SM4的DFA方案

3、VNCTF-2025-赛后复现

4、IDA Pro 9 SP1 安装和插件配置

5、初探 android crc 检测及绕过

球分享

球点赞

球在看

点击阅读原文查看更多


```
diff --color -ruN origin/include/linux/bpf.h aliyunctf/include/linux/bpf.h
--- origin/include/linux/bpf.h	2025-01-23 10:21:19.000000000 -0600
+++ aliyunctf/include/linux/bpf.h	2025-01-24 03:44:01.494468038 -0600
@@ -3058,6 +3058,7 @@
 extern const struct bpf_func_proto bpf_user_ringbuf_drain_proto;
 extern const struct bpf_func_proto bpf_cgrp_storage_get_proto;
 extern const struct bpf_func_proto bpf_cgrp_storage_delete_proto;
+extern const struct bpf_func_proto bpf_aliyunctf_xor_proto;

 const struct bpf_func_proto *tracing_prog_func_proto(
 enum bpf_func_id func_id, const struct bpf_prog *prog);
diff --color -ruN origin/include/uapi/linux/bpf.h aliyunctf/include/uapi/linux/bpf.h
--- origin/include/uapi/linux/bpf.h	2025-01-23 10:21:19.000000000 -0600
+++ aliyunctf/include/uapi/linux/bpf.h	2025-01-24 03:44:11.814636836 -0600
@@ -5881,6 +5881,7 @@
 FN(user_ringbuf_drain, 209, ##ctx)
 FN(cgrp_storage_get, 210, ##ctx)
 FN(cgrp_storage_delete, 211, ##ctx)
+	FN(aliyunctf_xor, 212, ##ctx)
 /* */

 /* backwards-compatibility macros for users of __BPF_FUNC_MAPPER that don't
diff --color -ruN origin/kernel/bpf/helpers.c aliyunctf/kernel/bpf/helpers.c
--- origin/kernel/bpf/helpers.c	2025-01-23 10:21:19.000000000 -0600
+++ aliyunctf/kernel/bpf/helpers.c	2025-01-24 03:44:06.683490095 -0600
@@ -1745,6 +1745,28 @@
 .arg3_type	= ARG_CONST_ALLOC_SIZE_OR_ZERO,
 };

+BPF_CALL_3(bpf_aliyunctf_xor, const char *, buf, size_t, buf_len, s64 *, res) {
+	s64 _res = 2025;
+
+	if (buf_len != sizeof(s64))
+ return -EINVAL;
+
+	_res ^= *(s64 *)buf;
+	*res = _res;
+
+	return 0;
+}
+
+const struct bpf_func_proto bpf_aliyunctf_xor_proto = {
+	.func = bpf_aliyunctf_xor,
+	.gpl_only	= false,
+	.ret_type	= RET_INTEGER,
+	.arg1_type	= ARG_PTR_TO_MEM | MEM_RDONLY,
+	.arg2_type	= ARG_CONST_SIZE,
+	.arg3_type	= ARG_PTR_TO_FIXED_SIZE_MEM | MEM_UNINIT | MEM_ALIGNED | MEM_RDONLY,
+	.arg3_size	= sizeof(s64),
+};
+
 const struct bpf_func_proto bpf_get_current_task_proto __weak;
 const struct bpf_func_proto bpf_get_current_task_btf_proto __weak;
 const struct bpf_func_proto bpf_probe_read_user_proto __weak;
@@ -1801,6 +1823,8 @@
 return &bpf_strtol_proto;
 case BPF_FUNC_strtoul:
 return &bpf_strtoul_proto;
+	case BPF_FUNC_aliyunctf_xor:
+ return &bpf_aliyunctf_xor_proto;
 default:
 break;
 }
#0 check_mem_access (env=0xffff888004b58000, insn_idx=0x1, regno=0xa, off=0x6, bpf_size=0x18, t=BPF_WRITE,
 value_regno=<error reading variable: Cannot access memory at address 0x0>,
 strict_alignment_once=<error reading variable: Cannot access memory at address 0x8>,
 is_ldsx=<error reading variable: Cannot access memory at address 0x10>) at kernel/bpf/verifier.c:
6698
#1 0xffffffff812012a9 in do_check (env=<optimized out>) at kernel/bpf/verifier.c:
17179
#2 do_check_common (env=0xffff888004b58000, subprog=0x0) at kernel/bpf/verifier.c:
19643
#3 0xffffffff812064ba in do_check_main (env=<optimized out>) at kernel/bpf/verifier.c:
19706
#4 bpf_check (prog=0xffff888004b58000, attr=0x1 <fixed_percpu_data+1>, uattr=..., uattr_size=0x18) at kernel/bpf/verifier.c:
20333
#5 0xffffffff811df0c2 in bpf_prog_load (attr=0xffffc9000023fe58, uattr=..., uattr_size=0xfffffff0) at kernel/bpf/syscall.c:
2743
#6 0xffffffff811e196a in __sys_bpf (cmd=0x5, uattr=..., size=0x0) at kernel/bpf/syscall.c:
5465
#7 0xffffffff811e4059 in __do_sys_bpf (size=<optimized out>, uattr=<optimized out>, cmd=<optimized out>) at kernel/bpf/syscall.c:
5569
#8 __se_sys_bpf (size=<optimized out>, uattr=<optimized out>, cmd=<optimized out>) at kernel/bpf/syscall.c:
5567
#9 __x64_sys_bpf (regs=0xffff888004b58000) at kernel/bpf/syscall.c:
5567
#10 0xffffffff81f38d39 in do_syscall_x64 (nr=<optimized out>, regs=<optimized out>) at arch/x86/entry/common.c:51
#11 do_syscall_64 (regs=0xffffc9000023ff58, nr=0x1) at arch/x86/entry/common.c:81
#12 0xffffffff82000134 in entry_SYSCALL_64 () at arch/x86/entry/entry_64.S:
121
#13 0x0000000000000000 in ?? ()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]