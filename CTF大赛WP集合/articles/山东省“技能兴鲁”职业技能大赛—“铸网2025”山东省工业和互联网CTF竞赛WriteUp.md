# 山东省“技能兴鲁”职业技能大赛—“铸网2025”山东省工业和互联网CTF竞赛WriteUp

> 原文: https://www.ctfiot.com/269821.html
> ID: 269821

前言

山东省“技能兴鲁”职业技能大赛—“铸网2025”山东省工业和互联网网络安全职业技能竞赛题解。

欢迎关注公众号【Real返璞归真】回复【铸网2025】获取完整题目附件。

解题情况
image-20250909164737302
image-20250909164758568

ICS

失窃的工艺

下载后test.PCZ文件，需要使用力控软件打开。

但电脑没有安装这个软件，尝试把后缀名改为.zip，解压后直接搜索flag文本：
image-20250909163733777

成功在文件中找到flag：flag{D076-4D7E-92AC-A05ACB788292}。

工控协议分析

WireShark打开分析，追踪TCP流，flag被逐字符藏在流量中：
image-20250909165641380

拼凑起来得到flag：flag{c93650241853da240f9760531a79cbcf}。

Misc

总线流量分析

一辆汽车在试验道路上行驶，测试人员监控了一段时间的车内通信报文，报文抓取时间间隔为36s，尝试找出与仪表显示车速相关的CAN通信报文，估算车辆在这段时间的行驶路程（m）得到flag。已知车速在80千米每小时左右，车速信息只占用1字节长度，且具备较高优先级。flag{行驶路程距离}

打开后按ID分组观察，根据题目提示找只有1字节变化的can报文：
image-20250909163749620

发现ID=0x0000280的can报文数据只有1字节在变化且在0x50左右浮动，说明速度为80km/h左右。

编写脚本计算即可：

speeds_hex = ["46","48","50","50","55","58","52","5A","58","58",
              "56","54","55","4F","4F","4F","4D","4D","4D","4E",
              "4E","53","56","56","59","59","51","52","4F","46"]

speeds = [int(h,16) for h in speeds_hex]
delta_t = 36

distance_km = 0
for v in speeds:
    distance_km += v * delta_t / 3600

distance_m = distance_km * 1000
print(distance_km, distance_m)

# 24.469999999999995 24469.999999999996
# flag{24470}

OTA流量分析

车机/IOT设备的OTA（Over-The-Air）流程：

设备发起请求到服务器，比如 /api/v1/vehicle/handshake，带上设备信息。

服务器生成一个 会话密钥 session_key，通过 HTTPS 或者加密通道下发给设备。

后续敏感数据（固件包、授权信息）会用这个 session_key 进行对称加密（常见 AES-CBC/CTR）。

设备用 session_key 解密得到明文，然后执行升级或拿到控制指令。

爆 k1 段：

对 c3 做三次 AES-CBC 解密，并对每次解密结果进行 PKCS7 补位校验。

当三次解密都成功且补位合法时，说明该 k1 值正确，对应的解密结果即为 c0。

爆 k0 段：

对 c0 做一次 AES-CBC 解密并校验 PKCS7 补位，同时验证明文是否符合 flag 的 UUID 格式。

找到匹配的 k0 后，即可得到最终 flag。

优化思路：

k1 的搜索空间和 k0 相比较大，可利用多进程或批量处理加速暴力搜索。

PKCS7 补位校验和 UUID 格式校验可以作为快速剪枝条件，大幅减少无效解尝试。


```
speeds_hex = ["46","48","50","50","55","58","52","5A","58","58",
              "56","54","55","4F","4F","4F","4D","4D","4D","4E",
              "4E","53","56","56","59","59","51","52","4F","46"]

speeds = [int(h,16) for h in speeds_hex]
delta_t = 36

distance_km = 0
for v in speeds:
    distance_km += v * delta_t / 3600

distance_m = distance_km * 1000
print(distance_km, distance_m)

# 24.469999999999995 24469.999999999996
# flag{24470}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_ota_flag.py
Usage:
  pip install scapy pycryptodome
  python3 extract_ota_flag.py ota.pcapng

What it does:
  - 尝试用 scapy 读取 pcap 并抽取 TCP/UDP payload（若 scapy 不可用则直接读取原始 pcap 字节进行搜索）
  - 搜索 HTTP 区段、提取 session_key、查找长 base64 段并 decode
  - 假设 decoded blob 为 IV(16) + AES-CBC(ciphertext)，使用每个 session_key (hex -> bytes) 作为 AES-256 key 遍历解密
  - 尝试移除 PKCS#7 填充并解析为文本，输出含 'flag{' 的解密文本
"""
import sys
import os
import re
import json
import base64
from pathlib import Path

pcap_path = Path(sys.argv[1]) if len(sys.argv) > 1else Path("ota.pcapng")
ifnot pcap_path.exists():
    print("pcap not found:", pcap_path)
    sys.exit(1)

# helpers
def find_session_keys(text):
    keys = set()
    # match "session_key": "hex..."
    for m in re.finditer(r'"session_key"s*:s*"([0-9a-fA-F]{32,128})"', text):
        keys.add(m.group(1))
    return keys

def find_long_base64(text, min_len=80):
    # return unique base64-like substrings (alnum+/ and optional padding)
    found = set()
    for m in re.finditer(r'([A-Za-z0-9+/]{%d,}={0,2})' % min_len, text):
        found.add(m.group(1))
    return list(found)

# Try scapy first (if installed)
payload_blobs = []  # list of bytes objects
http_texts = []     # list of decoded http-like text blocks
try:
    from scapy.all import rdpcap, TCP, UDP, Raw
    pkts = rdpcap(str(pcap_path))
    sessions = pkts.sessions()
    for s, pkts in sessions.items():
        data = bytearray()
        for p in pkts:
            if p.haslayer(Raw):
                data.extend(bytes(p[Raw].load))
        if data:
            # try decode for text
            try:
                txt = data.decode('utf-8', errors='replace')
                if"HTTP"in txt or"POST"in txt or"GET "in txt or"session_key"in txt:
                    http_texts.append(txt)
            
except Exception:
                pass
            payload_blobs.append(bytes(data))
    print("scapy path used: extracted %d payload blobs, %d http text blocks" % (len(payload_blobs), len(http_texts)))
except Exception as e:
    # fallback: raw bytes search (robust when scapy not installed)
    print("scapy not available or failed (%s). Falling back to raw-byte scan." % e)
    raw = pcap_path.read_bytes()
    # extract long printable runs (likely HTTP payloads)
    runs = []
    cur = bytearray()
    for b in raw:
        if32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= 40:
                runs.append(bytes(cur))
            cur = bytearray()
    if len(cur) >= 40:
        runs.append(bytes(cur))
    for r in runs:
        try:
            txt = r.decode('utf-8', errors='replace')
            http_texts.append(txt)
        
except:
            pass
    # also keep raw as one blob for base64 search
    payload_blobs.append(raw)
    print("raw scan found %d printable runs, payload_blobs=%d" % (len(runs), len(payload_blobs)))

# gather session keys from http_texts
session_keys = set()
for t in http_texts:
    session_keys |= find_session_keys(t)

print("session_key candidates found:", session_keys)

# gather base64 candidates from http_texts and from raw payload blobs (text decode)
b64_candidates = set()
for t in http_texts:
    for b in find_long_base64(t):
        b64_candidates.add(b)
# also scan payload blobs as text for base64
for blob in payload_blobs:
    try:
        txt = blob.decode('utf-8', errors='replace')
        for b in find_long_base64(txt):
            b64_candidates.add(b)
    
except:
        pass

print("base64 candidates found:", len(b64_candidates))

# decode base64 candidates to binary blobs
decoded_blobs = []
for b64 in b64_candidates:
    try:
        data = base64.b64decode(b64)
        if data:
            decoded_blobs.append(data)
    
except Exception:
        continue

print("decoded binary blobs:", len(decoded_blobs))

# AES decryption attempts using session_keys
try:
    from Crypto.Cipher import AES
    have_crypto = True
except Exception:
    have_crypto = False
    print("PyCryptodome not found. Install with: pip install pycryptodome")

found = []
if have_crypto and decoded_blobs and session_keys:
    for blob in decoded_blobs:
        if len(blob) <= 16:
            continue
        iv = blob[:16]
        ct = blob[16:]
        for keyhex in session_keys:
            try:
                key = bytes.fromhex(keyhex)
                if len(key) notin (16,24,32):
                    # try require 32 bytes for AES-256
                    if len(key) < 32:
                        # pad? skip
                        continue
                cipher = AES.new(key, AES.MODE_CBC, iv)
                pt = cipher.decrypt(ct)
                # PKCS#7 removal
                pad = pt[-1]
                if isinstance(pad, int) and1 <= pad <= 16:
                    pt2 = pt[:-pad]
                else:
                    pt2 = pt
                try:
                    s = pt2.decode('utf-8', errors='replace')
                
except:
                    s = repr(pt2)
                # check for JSON / 'flag{' / 'admin'
                if ('flag{'in s) or ('"flag"'in s) or ('admin'in s.lower()) or ('nonce'in s.lower()):
                    entry = {
                        "key": keyhex,
                        "plaintext": s
                    }
                    print("=== possible cleartext with key %s ===n%sn" % (keyhex, s))
                    found.append(entry)
            
except Exception as e:
                # ignore key failures
                pass

ifnot found:
    print("No flags found with available session_keys + decoded blobs.")
else:
    print("Total found items:", len(found))
    # print flags explicitly
    for ent in found:
        m = re.search(r'flag{[^}]+}', ent["plaintext"], re.IGNORECASE)
        if m:
            print("FOUND FLAG:", m.group(0))

# As fallback: search raw for flag{...}
rawbytes = pcap_path.read_bytes()
m = re.search(rb'flag{[^}rn]{1,200}}', rawbytes, re.IGNORECASE)
if m:
    try:
        print("RAW-FOUND FLAG (from pcap bytes):", m.group(0).decode())
    
except:
        print("RAW-FOUND FLAG (bytes):", m.group(0))
scapy not available or failed (No module named 'scapy'). Falling back to raw-byte scan.
raw scan found 26 printable runs, payload_blobs=1
session_key candidates found: {'9dbbe057c3b0c7e547701d5ccab3d676c0de24cdd49f2e4f34f5bc99e0e666a0', 'b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90', 'bc27b70ea1b27768c1ad58314005ee2ee0a09977b150e570465d6247675e1eab', '0d53164fe1c89a4f09512492f2236d86d52c4fdd8b9018195b791b634bfe9e83'}
base64 candidates found: 4
decoded binary blobs: 4
=== possible cleartext with key bc27b70ea1b27768c1ad58314005ee2ee0a09977b150e570465d6247675e1eab ===
{"ok": true, "nonce": 2, "admin": false}

=== possible cleartext with key 0d53164fe1c89a4f09512492f2236d86d52c4fdd8b9018195b791b634bfe9e83 ===
{"ok": true, "nonce": 2, "admin": false}

=== possible cleartext with key 9dbbe057c3b0c7e547701d5ccab3d676c0de24cdd49f2e4f34f5bc99e0e666a0 ===
{"ok": true, "nonce": 2, "admin": true, "flag": "flag{62173234ab6b0f3349ed89685fba5fff}", "hint": "admin vehicle received a confidential note."}

=== possible cleartext with key b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90 ===
{"ok": true, "nonce": 2, "admin": false}

Total found items: 4
FOUND FLAG: flag{62173234ab6b0f3349ed89685fba5fff}
enc = [0x3C, 0x36, 0x3B, 0x3D, 0x21, 0x1B, 0x1F, 0x09, 0x77, 0x32, 0x3B, 0x2A, 0x2A, 0x23, 0x27]
for x in enc:
    print(chr(x ^ 0x5A), end="")
    
# flag{AES-happy}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 依赖：pip install pycryptodome
from hashlib import sha256
from Crypto.Cipher import AES
import re
import itertools
import multiprocessing as mp

# ========== 配置 ==========
c3_hex = "62343dfc3e978a1d580b54f345e1ed719c85ab15781acfe8ba3bcef1560c9cf54f187bc204c302a5ed4ebb5b5454151ba9b8b73841e17dc391c30a637ef8cfa14a25d01765231ef93a6faede2d66bad5d124201a2d278522bfd416de294677046d47f2827580cdcb9c0d3b18e4c0c68c8948aaefe4e684c7386b426db7898b5c2090047ff433bb6a75b38beaf81b7ad9404d2f09c642179697e9d3721eefc0eb12ba8c780a8d07672f70b00b9cadef74"
data = bytes.fromhex(c3_hex)
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
UUID_RE = re.compile(rb"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$")

WORKERS = mp.cpu_count()  # 可调整为 4~8
BATCH_SIZE = 256
# 每个任务分配的 k1 数量

# ========== AES 工具函数 ==========
def unpad32(b: bytes) -> bytes:
    pad = b[-1]
    if pad < 1or pad > 32or b[-pad:] != bytes([pad])*pad:
        raise ValueError("bad pad")
    return b[:-pad]

def dec32(key: bytes, blob: bytes) -> bytes:
    iv, ct = blob[:16], blob[16:]
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return unpad32(pt)

def triple_dec_check(k_bytes: bytes, c3_bytes: bytes):
    """三次解密并校验 PKCS7"""
    try:
        t1 = dec32(k_bytes, c3_bytes)
        t2 = dec32(k_bytes, t1)
        t3 = dec32(k_bytes, t2)
        return t3
    
except Exception:
        returnNone

# ========== worker 初始化 ==========
def init_worker(keys0_list_param):
    global KEYS0_LIST
    KEYS0_LIST = keys0_list_param

# ========== worker 函数 ==========
def worker_k1_batch(batch):
    """尝试一个 k1 批次"""
    global KEYS0_LIST, data
    for seg in batch:
        k1_bytes = sha256(seg.encode()).digest()
        c0_candidate = triple_dec_check(k1_bytes, data)
        if c0_candidate isNone:
            continue
        # 找到 k1，尝试 k0
        for k0_seg, k0_bytes in KEYS0_LIST:
            try:
                pt = dec32(k0_bytes, c0_candidate)
            
except Exception:
                continue
            if UUID_RE.match(pt):
                return (seg, k0_seg, pt.decode())
    returnNone

# ========== 主流程 ==========
def main():
    # 生成 k0 候选列表
    keys0_list = [(a+b+c, sha256((a+b+c).encode()).digest())
                  for a in ALPHABET for b in ALPHABET for c in ALPHABET]

    # 生成 k1 流式批次
    def k1_batch_gen(batch_size):
        it = (a+b+c for a in ALPHABET for b in ALPHABET for c in ALPHABET)
        whileTrue:
            batch = list(itertools.islice(it, batch_size))
            ifnot batch:
                break
            yield batch

    pool = mp.Pool(WORKERS, initializer=init_worker, initargs=(keys0_list,))
    try:
        for result in pool.imap_unordered(worker_k1_batch, k1_batch_gen(BATCH_SIZE), chunksize=1):
            if result:
                k1_seg, k0_seg, flag = result
                print("找到结果！")
                print("k1 segment =", k1_seg)
                print("k0 segment =", k0_seg)
                print("flag =", flag)
                pool.terminate()
                return
    finally:
        pool.close()
        pool.join()
    print("遍历完成，没有找到 flag")

if __name__ == "__main__":
    main()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473793-wxsync-2025-09-f1b458ffa17e53f72ed4089fd62a27e0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473794-wxsync-2025-09-7c0606eaad4c82bc5fa279f9196979b4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473796-wxsync-2025-09-616ac3b585b0dc39da7ee240190b3954.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473798-wxsync-2025-09-5248fcba4cb360d03c17e1394e7d8d64.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473800-wxsync-2025-09-ad17be38e89c5fc0632b2e927db2e6c3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473801-wxsync-2025-09-08519778c6a265d51fc2b6fcaa17937b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473803-wxsync-2025-09-bb8acda5ac3e85a36be4101b5fee563c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473805-wxsync-2025-09-680d5bd86ac3d9320393480322d3eb46.png)