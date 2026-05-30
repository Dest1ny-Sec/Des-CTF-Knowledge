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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-4f3e3704dbbaf0442dbd33c8f38ff9b6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-3d2fecb055384e4ebbe68a29a349be28.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-3d2fecb055384e4ebbe68a29a349be28.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-3d2fecb055384e4ebbe68a29a349be28.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-a977c693450e687d03032f41fbab59b0.gif)