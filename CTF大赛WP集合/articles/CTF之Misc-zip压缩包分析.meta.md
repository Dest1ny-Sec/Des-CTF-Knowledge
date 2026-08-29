---
title: CTF 之 Misc - zip 压缩包分析
contest: Misc CTF
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags: [zip结构, 文件头 50 4B 03 04, 目录头 50 4B 01 02, 结束符 50 4B 05 06, 伪加密 1400XX0008, fcrackzip暴力破解, CRC32爆破, 5字符, 明文攻击, ARCHPR, 看雪 wx_酸菜鱼]
attack_chain:
  - zip 3 部分: 数据区 + 目录区 + 结束符
  - 文件头 50 4B 03 04, 目录 50 4B 01 02, 结束 50 4B 05 06
  - 伪加密: 目录文件标记后 4 字节 1400XX0008, XX 改 9 → 伪加密, 改 0 还原
  - 暴力破解: fcrackzip -b -l 6-6 -c 1 -p 000000 passwd.zip
  - CRC32 爆破: 5 字符全字典 ascii_letters + _ + 0-9
  - 明文攻击: 已知文件 ZIP 加密后, 对比 hex 找 3 个 key
  - linux 0A vs windows 0D0A 换行符差异
key_payload: 'zip 文件头 50 4B 03 04 / 目录 50 4B 01 02 / 伪加密 1400XX0008 / fcrackzip -b -l 6-6 -c 1 / CRC32 5 字符爆破 / 明文攻击 hex 对比 / linux 0A vs windows 0D0A'
one_liner: CTF Misc zip 压缩包分析 — 伪加密 (1400XX0008 改 9) + fcrackzip 暴力破解 + CRC32 5 字符爆破 + 明文攻击 (hex 对比) + linux/windows 换行符 0A vs 0D0A 差异。
lesson: zip 伪加密是改目录 14 00 XX 00 08 中 XX 第 1 位 (0/1 切换);CRC32 爆破只适合 ≤5 字符;明文攻击需已知明文 + 相同压缩算法。
quality: medium
---

# CTF 之 Misc - zip 压缩包分析

## 速读
看雪 wx_酸菜鱼 zip 压缩包分析教程 — 4 种攻击方式。

## zip 结构
```
[文件头 + 文件数据 + 数据描述符]  (数据区)
[目录文件头]                       (目录区)
[50 4B 05 06 + 0]                 (结束符)
```

| 标记 | 含义 |
|------|------|
| 50 4B 03 04 | 文件头 |
| 50 4B 01 02 | 目录头 |
| 50 4B 05 06 | 结束符 |

## 4 种攻击

### ① 伪加密
- 目录文件标记后 4 字节: `1400 XX 00 08`
- 改 XX 第 1 位 0→1 (如 00→09): 伪加密
- 改回 0: 还原

例题: 强网杯 2020 misc-study level5

### ② 暴力破解
```bash
fcrackzip -b -l 6-6 -c 1 -p 000000 passwd.zip
# -b 暴力, -c 1 数字, -l 6-6 长度 6, -p 起始点
```

Windows: ARCHPR

### ③ CRC32 爆破
```python
import string, binascii
dic = string.ascii_letters + "_" + "0123456789"
def aa(crc):
    for i in dic:
        for j in dic:
            for k in dic:
                for p in dic:
                    for q in dic:
                        st = i+j+k+p+q
                        if crc == (binascii.crc32(st) & 0xffffffff):
                            print(st)
```

- 适合 ≤5 字符
- 例题: 强网杯 2020 level6, ByteCTF 2020 PT Site

### ④ 明文攻击
- 已知明文 → ZIP 加密 → 对比 hex 找 3 个 key
- linux 换行 `\n` (0A), windows 换行 `\r\n` (0D0A)
- 删除 0D 即可
- 例题: ByteCTF 2020 PT Site
