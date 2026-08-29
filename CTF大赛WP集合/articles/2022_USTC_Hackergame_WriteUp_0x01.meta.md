---
title: 2022 USTC Hackergame WriteUp 0x01
contest: 2022 USTC Hackergame (中科大信安赛)
year: 2022
difficulty: medium
vuln_type: [forensic_disk, misc_math, web_unknown, reverse, crypto_oracle]
tags: [rclone.conf, AES-CTR, Obscure, Reveal, Go-crypt, heilang, SHA256, HTTP, URL编码, 抓包, Planet]
attack_chain: ["Q1 grep: grep 'flag{' . -aR 找 flag", "Q2 rclone: 从 .config/rclone/rclone.conf 找 obfuscated password", "Q3 Go AES-CTR 还原: 拿 cryptKey 32 字节 + Obscure 源码 → 写 Reveal", "Q4 heilang 数组: a[1225|2381|...]=978 写正则提取", "Q5 HTTP 抓包: curl -v 看 Host 头", "Q6 URL 编码绕过: 双重 URL 编码", "Q7 Planet 物理题", "Q8 XSS / 内网穿透", "Q9 LFSR / 流密码", "Q10 0day PDF 解析"]
key_payload: "flag{get_rclone_password_from_config!_2oi3dz1}"
one_liner: USTC Hackergame 多题混战：rclone密码还原+Go AES-CTR+heilang正则
lesson: 通用工具 rclone/curl/wireshark/python 都能解
quality: high
---

# 2022 USTC Hackergame WriteUp 0x01

原文 https://www.ctfiot.com/71252.html （中科大信安赛 / USTC Hackergame）

## 系列题
- Q1: 通用文件搜索 `grep "flag{" . -aR`
- Q2: **rclone 配置泄露** + AES-CTR 还原
- Q3: **Go obscure/reveal 还原密码**
- Q4: **heilang 数组正则还原**
- Q5: HTTP 抓包改 Host
- Q6: 双重 URL 编码绕过
- Q7: 物理题（Planet）
- Q8: 内网穿透 / XSS
- Q9: LFSR 还原
- Q10: PDF 0day

## Q2: rclone 配置文件泄露
```ini
# .config/rclone/rclone.conf
[flag2]
type = ftp
host = ftp.example.com
user = user
pass = tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ
```

rclone 用 Go 写的 `Obscure()` AES-CTR 加密密码，密钥硬编码：
```go
var cryptKey = []byte{
    0x9c, 0x93, 0x5b, 0x48, 0x73, 0x0a, 0x55, 0x4d,
    0x6b, 0xfd, 0x7c, 0x63, 0xc8, 0x86, 0xa9, 0x2b,
    0xd3, 0x90, 0x19, 0x8e, 0xb8, 0x12, 0x8a, 0xfb,
    0xf4, 0xde, 0x16, 0x2b, 0x8b, 0x95, 0xf6, 0x38,
}
func crypt(out, in, iv []byte) error {
    stream := cipher.NewCTR(cryptBlock, iv)
    stream.XORKeyStream(out, in)
}
func Reveal(x string) (string, error) {
    ciphertext, _ := base64.RawURLEncoding.DecodeString(x)
    iv := ciphertext[:aes.BlockSize]
    buf := ciphertext[aes.BlockSize:]
    crypt(buf, buf, iv)
    return string(buf), nil
}
```

直接 `rclone reveal` 即可：
```bash
$ rclone reveal 'tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ'
flag{get_rclone_password_from_config!_2oi3dz1}
```

## Q3: heilang 数组正则
```python
a = [0] * 10000
a[1225 | 2381 | 2956 | 3380 | ...] = 978
a[412 | 5923 | ...] = 51
```
启发式语言（hei），用正则 `a[(.*)] = (\d+)` 提取所有索引/值，然后 sha256 校验：
```python
import re
r = re.findall(r"a\[(.*)\] = (\d+)", s, re.M)
for d in r:
    indices = d[0].split(' | ')
    for i in indices:
        a[int(i)] = int(d[1])

def get_flag(a):
    if sha256(('heilang' + ''.join(str(x) for x in a)).encode()).hexdigest() == '76bd735ba6f0ca6213528caa474714a5322f668d6748e4214c79df4306ec9439':
        t = ''.join([chr(x % 255) for x in a])
        flag = sha256(t[:-16].encode()).hexdigest()[:16] + '-' + sha256(t[-16:].encode()).hexdigest()[:16]
        print(f"flag{{{flag}}}")
```

## 教学价值
- **rclone 密码泄漏**是真实云存储配置常见漏洞
- **Go 硬编码密钥** 是 1-day 的常见形态
- **AES-CTR** 加 base64 编码（RawURLEncoding）是 Go 生态标配
- **正则 + sha256 校验** 是数组题快速通关套路
- USTC Hackergame 题目"杂"且"广"，适合培养综合能力

## flag
- Q2: `flag{get_rclone_password_from_config!_2oi3dz1}`
- Q3: 启发式语言（hei）数组 → sha256 校验
