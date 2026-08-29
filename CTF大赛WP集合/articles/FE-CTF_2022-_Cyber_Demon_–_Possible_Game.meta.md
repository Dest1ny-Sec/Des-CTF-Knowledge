---
title: FE-CTF 2022: Cyber Demon – Possible Game
contest: FE-CTF 2022
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [pwn, secret-key, urandom, hlt, dev-urandom, file-not-found, asm]
attack_chain:
  - ./game运行需要secret_key文件
  - 缺文件→open ENOENT→exit(1)
  - echo much secret > secret_key绕过
  - 反汇编main:
  - sub_4068DD初始化off_40D0C0/D140/D040三个1024字节
  - sub_405D9B打开/dev/urandom
  - sub_404D8C/sub_405BD2读urandom
  - 汇编hlt指令触发
  - pop rdi; mov rsi,rsp; push rdi; lea rdx,[rsi+rdi*8+8]
  - mov cs:qword_40D340, rdx; call sub_4060AA; call sub_408AA1; hlt
key_payload: echo much secret > secret_key  # 绕过文件检查
one_liner: FE-CTF Possible Game：secret_key缺失+urandom初始化+汇编hlt
lesson: 写secret_key文件绕过文件存在性检查
quality: medium
---

# FE-CTF 2022: Cyber Demon – Possible Game

## 题目信息
- 比赛：FE-CTF 2022
- 题目：Cyber Demon – Possible Game
- 类型：PWN

## 关键攻击链
### 1. 程序运行
```bash
$ ./game
open: No such file or directory
$ strace ./game
open("/dev/urandom", O_RDONLY) = 3
open("secret_key", O_RDONLY) = -1 ENOENT
write(2, "open", 4) ...
exit(1)
$ echo much secret > secret_key  # 绕过
```

### 2. main 函数反编译
```c
int main(int argc, const char **argv, const char **envp) {
    sub_4068DD(off_40D0C0, 0, 0, 1024);  // 初始化 3 个 1024 字节
    sub_4068DD(off_40D140, 0, 0, 1024);
    sub_4068DD(off_40D040, 0, 0, 1024);
    dword_40D220 = sub_405D9B("/dev/urandom", 0);
    if (dword_40D220 == -1) {
        sub_405EBC("open", 0);
        return 1;
    }
    sub_404D8C("/dev/urandom", 0);
    sub_405BD2("/dev/urandom");
    return 0;
}
```

### 3. 关键汇编
```asm
pop rdi
mov rsi, rsp
push rdi
lea rdx, [rsi+rdi*8+8]
mov cs:qword_40D340, rdx
call sub_4060AA
mov rdi, rax
call sub_408AA1
hlt
```

### 4. setvbuf 配置
```c
setvbuf(stdin, NULL, 0, _IONBF, BUFSIZ);
setvbuf(stdout, NULL, 0, _IONBF, BUFSIZ);
setvbuf(stderr, NULL, 0, _IONBF, BUFSIZ);
```

## 评分
- quality: medium（secret_key 绕过 + 汇编 hlt 触发）
