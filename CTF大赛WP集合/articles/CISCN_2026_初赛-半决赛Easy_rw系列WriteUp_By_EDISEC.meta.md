---
title: CISCN 2026 初赛-半决赛 Easy_rw 系列 WriteUp By EDISEC
contest: CISCN
year: 2026
difficulty: hard
vuln_type: pwn_unknown
tags: [Easy_rw, 自定义packet协议, header+packet_len+payload, struct.pack!II, Easy_rw_revenge, RC4 KSA, libc.srand(time()) 32字节key, 0xFFFF2525 AUTH_MAGIC, 0x7F687985 FORWARD_MAGIC, rtsp:// proxy转发, libc 0x21b110, libc leak, _IO_list_all, ORW ROP, /flag 0123456789ABCDEF ECB]
attack_chain:
  - Easy_rw: 自定义 packet 协议 header(4) + packet_len(4) + payload
  - Easy_rw_revenge: proxy 192.168.18.137:9999 → server 127.0.0.1:7777
  - RC4: libc.srand(time()) 生成 32 字节 key, KSA 初始化
  - AUTH_MAGIC=0xFFFF2525 认证, FORWARD_MAGIC=0x7F687985 转发
  - rtsp:// 协议 + XOR 0x41*8 + 转发到 server
  - server: add/delete/show/edit 命令, cookie 认证
  - libc leak: large=u64(pack[0:6].ljust(8,b'\x00')), libc_base=large-0x21b110
  - ORW ROP: open /flag + read + write stdout
  - 加密数据 AES-ECB 0123456789ABCDEF 解密
key_payload: 'struct.pack!II / RC4 KSA / libc.srand(time()) / AUTH_MAGIC 0xFFFF2525 / FORWARD_MAGIC 0x7F687985 / rtsp:// proxy / libc 0x21b110 / ORW ROP / AES-ECB 0123456789ABCDEF'
one_liner: CISCN 2026 Easy_rw 系列 — 自定义 packet 协议 (header+len+payload) + Easy_rw_revenge proxy RC4 转发 + rtsp:// 命令注入 + libc leak + ORW ROP + AES-ECB 0123456789ABCDEF 解密。
lesson: 自定义二进制协议 reverse: header+length+payload 模板;RC4 + libc.srand(time()) 是经典 PRNG 漏洞;rtsp:// 是 rfc 协议伪装;ORW 是无 system 时的标准解法。
quality: high
---

# CISCN 2026 初赛-半决赛 Easy_rw 系列 WriteUp By EDISEC

## 速读
CISCN 2026 Easy_rw + Easy_rw_revenge — 自定义 packet 协议 + RC4 proxy 转发。

## Easy_rw
- 自定义 packet: header(4 字节) + packet_len(4 字节) + payload
- `struct.pack('!II', header, length) + payload_bytes`

## Easy_rw_revenge
### 协议
- proxy 192.168.18.137:9999 → server 127.0.0.1:7777
- AUTH_MAGIC=0xFFFF2525, FORWARD_MAGIC=0x7F687985
- AUTH_PAYLOAD=b"#welcome!_c1sCn_2026"

### RC4
```python
class RC4:
    def __init__(self, key):
        self.S = list(range(256))
        self.i = 0
        self.j = 0
        self.ksa(key)
    
    def crypt(self, data):
        for byte in data:
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.S[self.i]) % 256
            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
            k = self.S[(self.S[self.i] + self.S[self.j]) % 256]
            result.append(byte ^ k)
```

### 认证
```python
libc.srand(test_time)
rc4_key_list = [libc.rand() & 0xFF for _ in range(32)]
rc4_key = bytes(rc4_key_list)
rc4 = RC4(rc4_key)
rc4_encrypted = rc4.crypt(AUTH_PAYLOAD)
xor_encrypted = xor_encrypt(rc4_encrypted, bytes([0x41]*8))
```

### rtsp:// 转发
- `rtsp://03561714/{command:index:size:content}`
- cookie 32 字节 + rtsp 请求 → server 解析为 add/delete/show/edit

### 利用
- add(0x508) + add(0x510) + ... → unsortedbin 泄堆地址
- `libc_base = large - 0x21b110`
- ORW ROP: open /flag + read 0x50 字节 + write
- AES-ECB(0123456789ABCDEF) 解密 flag
