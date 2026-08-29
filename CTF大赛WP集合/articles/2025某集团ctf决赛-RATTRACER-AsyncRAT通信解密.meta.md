---
title: 2025 某集团 ctf 决赛 RATTRACER - AsyncRAT 通信解密（TLS 私钥 + gzip + MsgPack + RDP JPEG）
contest: 2025 某集团 ctf 决赛
year: 2025
difficulty: hard
vuln_type: [forensic_traffic, pwn_unknown, web_unknown]
tags: [RATTRACER 2025 决赛, AsyncRAT-C-Sharp 开源项目, ST.p12 PKCS#12 私钥, openssl pkcs12 -info -in ST.p12 无密码, openssl pkcs12 -legacy -in ST.p12 -nocerts -nodes -out key.pem, Wireshark TLS 解密 ip port 私钥, 1f 8b 08 gzip 头, MsgPack 解析, 0xc4 0xc6 二进制标记, gzip_uncompress 批量, RDP JPEG ffd8 ffd9 提取, remoteDesktop- 流量]
attack_chain:
  - 1. 看到证书 p12 → openssl pkcs12 -info -in ST.p12 检密码（无密码）
  - 2. openssl pkcs12 -legacy -in ST.p12 -nocerts -nodes -out key.pem 提私钥
  - 3. Wireshark → 编辑→首选项→protocols→tls → 填 ip port 私钥
  - 4. 解密后看到 AsyncRAT 特征（NYAN-x-CAT/AsyncRAT-C-Sharp 开源）
  - 5. 内层 = 1f 8b 08 gzip 头 → gunzip
  - 6. MsgPack 解析 (parseMsgPack readstring readbinary getbuflen)
  - 7. 0xc4 = short binary, 0xc6 = long binary
  - 8. JPEG SOI ffd8ffd8 / EOI ffd9 提取 RDP 远程桌面截图
  - 9. flag 在 RDP 截图里
key_payload: "1f 8b 08 gzip 头 + MsgPack 0xc4 0xc6 标记"
one_liner: 2025 某集团决赛 RATTRACER：ST.p12 私钥解 TLS + AsyncRAT 通信解密 gzip+MsgPack + RDP JPEG 截图提取 flag。
lesson: AsyncRAT 通信 = TLS 1.x 外层 + gzip+MsgPack 内层 + 0xc4/0xc6 binary 标记；p12 无密码直接 openssl 提私钥；Wireshark TLS 解密后用协议特征搜索开源项目代码分析。
quality: high
---

# 2025 某集团 ctf 决赛 RATTRACER - AsyncRAT 通信解密

## 1. 提取私钥

```bash
# 检 p12 密码（无密码）
openssl pkcs12 -info -in ST.p12
# 直接回车
# 提私钥
openssl pkcs12 -legacy -in ST.p12 -nocerts -nodes -out key.pem
# 直接回车
```

## 2. Wireshark TLS 解密

编辑 → 首选项 → protocols → tls → 填 ip port 私钥（key.pem）  
解密后看到流量，但内容还是"加密的"——但有 AsyncRAT 特征。

## 3. AsyncRAT 识别

特征搜索发现 = [NYAN-x-CAT/AsyncRAT-C-Sharp](https://github.com/NYAN-x-CAT/AsyncRAT-C-Sharp) 开源 RAT。

参考：https://mp.weixin.qq.com/s/AJUQ8Zd_4Q3Ub9TarQx5Gg

## 4. 内层解密

- 内层 = `1f 8b 08` gzip 头（不是 TLS 内层）  
- 批量 gunzip + MsgPack 解析
- 0xc4 = short binary, 0xc6 = long binary 标记
- 长度前缀大小端：reverse_data + bytes_to_int

```python
def getbuflen(buf, isreverse=False):
    tmp = buf[:]
    if isreverse: tmp = reverse_data(tmp)
    return bytes_to_int(tmp)

def readbinary(buf):
    byteflag = buf[0]
    if byteflag == 0xc4:  # short binary
        len_zipdata = buf[1]
        len_data = getbuflen(buf[2:6], True)
        zipdata = buf[6:6+len_zipdata-4]
        data = gzip_uncompress(zipdata)
        return parseMsgPack(data), 2 + len_zipdata
    elif byteflag == 0xc6:  # long binary
        ...
```

## 5. RDP 流量提取 JPEG

```python
soi_index = decodedata.find(b'\xff\xd8\xff\xe0')  # JPEG SOI
eoi_index = jpeg_data.find(b'\xff\xd9')  # JPEG EOI
jpeg_data = jpeg_data[:eoi_index + 2]
```

`remoteDesktop-` 流量提取 → 看攻击者 RDP 进主机看了 `up.exe` 程序 → flag 在 RDP 截图里。

## 6. flag

flag 包含在 RDP 远程桌面截图里（PNG/JPEG），需解析所有 RDP 流量后从图像中读取。

## 总结

- **TLS 1.x 解密**：p12 私钥 → Wireshark
- **AsyncRAT 识别**：开源项目特征匹配
- **gzip + MsgPack**：0xc4/0xc6 标记 + reverse_data 大小端
- **RDP JPEG 提取**：SOI/EOI 标记
