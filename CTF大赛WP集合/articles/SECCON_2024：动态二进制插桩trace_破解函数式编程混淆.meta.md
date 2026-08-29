---
title: SECCON 2024 - 动态二进制插桩 trace 破解函数式编程混淆
contest: SECCON 2024
year: 2024
difficulty: high
vuln_type: misc_unknown
tags: [functional-programming, obfuscation, cpp, std-variant, std-shared_ptr, pyda, dynamic-binary-instrumentation, sub_byte, mul, rotl, sbox, cons-trace]
attack_chain:
  - SECCON 2024 函数式编程混淆 C++ (std::variant + std::shared_ptr<Cons>)
  - IDA 逆向: ZNKR3fixIZ4mainEUlT_St7variantIJj... 模板函数链
  - level 1 _Function_handler::M_invoke
  - level 2 std::__invoke_r
  - level 3 std::__invoke_impl
  - level 4 main::lambda::operator()
  - level 5 Cons + variant 操作
  - Cons 节点 (rdi, rsi, rdx) 构造链表
  - pyda 动态二进制插桩 + objdump 找 cmp 位置
  - cmp_locs 解析 + p.hook(e.address+x, cmp_hook) 跟踪每次比较
  - 关键 cmp: 0x1891b rcx vs rdx 比较目标密文
  - 用户输入 ABCDEFGH 0x40 字节触发多次 cons() 调
  - 还原加密 4 步: 
  - 1) sub_byte: 0x41414141 -> 0x4e4e4e4e (SubBytes AES-like)
  - 2) mul: 0x4e4e4e4e * 0xe14de95e = 0x93af4e5e (Galois mul)
  - 3) rotl(0x93af4e5e, 29) ^ rotl(0x93af4e5e, 17) ^ rotl(0xd36975c1, 7) ^ 0xe14de95e = 0xac0af82
  - 4) 再 sub_byte 0x4e4e4e4e (循环)
  - flag: SECCON{fUnCt10n4l_pRoGr4mM1n6_1s_pR4c7iC4lLy_a_pUr3_0bfu5c4T1oN}
  - gdb + ida + pyda backtrace 跟踪 0x8741 first_transform 函数
  - Cons 链表每节点 (rdi, rsi, rdx) -> (cons_value, op_target, next_cons)
  - Frame #6: 0x8741 = first_transform 调用入口
  - Frame #5: 0x3bfe = level 5 std::variant 操作
  - 完整调用栈: 0x1007c → 0x12afe → 0x1430f → ... → 0x8741
  - cmp @ 0x1891b rcx=0xc3df45f3 rdx=0x11793013 失败 = "Wrong"
  - cmp @ 0x15787 rdx=0x100000001 rax=0x100000001 True 多次验证
key_payload: pyda cmplog.py + p.hook(0x15a06, cons) 跟踪 Cons(rdi=0, rsi, rdx) 节点
one_liner: SECCON 2024 函数式编程混淆 C++ 逆向：std::variant + std::shared_ptr<Cons> 节点链表 + pyda 动态二进制插桩 trace cmp + Cons 节点 4 步加密 (sub_byte + mul + rotl + XOR) 还原。
lesson: 函数式编程混淆 (variant + shared_ptr<Cons>) 是高级 C++ 反混淆难点；pyda 动态二进制插桩跟踪 cmp/cons 节点是还原 Cons 链表算法的高阶工具；cmp 位置 + cmp 值对比可爆破密钥。
quality: high
---
