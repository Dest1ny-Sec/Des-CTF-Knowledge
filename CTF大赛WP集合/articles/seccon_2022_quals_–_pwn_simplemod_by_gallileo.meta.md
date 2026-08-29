---
title: seccon 2022 quals – pwn simplemod by gallileo
contest: SECCON
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [limited-write, naked-attribute, sys-exit, glibc-32, ofs-bound, alarm-30]
attack_chain:
  - alarm(30) 限时 30 秒
  - modify() 单字节写 gbuf[0..0x2000]
  - 30 次操作限制
  - 改 exit_imm 写入 syscall
  - 触发 fini() 调 exit_imm(0)
  - 修改 syscall 号触发其他系统调用
key_payload: 单字节写 gbuf 任意位置 + naked syscall
one_liner: SECCON 2022 quals simplemod 复盘，30 次单字节写 + naked syscall。
lesson: 有限次数的 1 字节写可以拼凑出任意 syscall gadget。
quality: high
---

SECCON 2022 quals simplemod 复盘（来源 ctfiot，作者 gallileo）。

**题目结构**
```c
__attribute__((constructor)) static int init() {
    alarm(30);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    return 0;
}
__attribute__((destructor)) static void fini() {
    exit_imm(0);
}
char gbuf[0x100];  // 全局 0x100 字节

void modify(void) {
    uint64_t ofs;
    if ((ofs = getint()) > 0x2000) return;
    gbuf[ofs] = getint();  // 单字节写
}

__attribute__((naked))
void exit_imm(int status) {
    asm(
        "xor rax, rax\n"
        "mov al, 0x3c\n"
        "syscall"  // 调 exit
    );
}
```

**关键限制**：
- 30 秒 alarm 限制
- 30 次操作（主循环 30 次）
- 单字节写，偏移最多 0x2000

**利用**：
- `modify()` 单字节写 → 修改 `gbuf` 数组
- 写入精心构造字节到 `gbuf[0..0x100]`（覆盖）
- 关键是 `exit_imm` 是 naked 函数 + 栈不对齐 → 改 syscall 号

**攻击链**：
1. 触发 fini() 调 exit_imm(0)
2. exit_imm 内部改 rax=0x3c 触发 sys_exit
3. 单字节改 0x3c → 0x3b (sys_execve) → 0x3b 改成 0x3b
4. 改 rdi 指向 /bin/sh
5. 触发弹 shell

**naked 函数 + 单字节写** 是 SECCON 经典技巧：naked 函数没有 prologue，攻击者可以单字节修改 syscall 指令。

**质量**：高质量逆向 + pwn 组合。
