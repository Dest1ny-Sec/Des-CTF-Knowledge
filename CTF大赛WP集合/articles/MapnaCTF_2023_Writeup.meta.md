---
title: MapnaCTF 2023 Writeup
contest: MapnaCTF
year: 2023
difficulty: easy
vuln_type: misc_unknown
tags: [packet_t 结构体, JPEG 字节级修复, data 段解析]
attack_chain: |
  1. 数据格式: packet_t 结构体 {u8 size, u32 always_one, u8 size_minus_2, u8 seq_number, u8 type, u8 contents[0]}
  2. JPEG 字节级修复: 提取的数据用 \x1f 字符替换多个常见字符
     - 原文 "JPEG" 被改成 "J\x1fY" / "!M49e_3nC0DeR" 变 "!M\x139e_3nC1DeR" 等
  3. flag 在修复后的 JPEG 文档中出现多次: MAPNA{__ZiG__JPEG_!M49e_3nC0DeR_rEv3R5e!!!}
  4. 多次变体:
     - MAPNA{__ZiG__JPEG_!M49e_3nD0DeR_rEv3R5e!!!}
     - MAPNA{__ZiG__JPEG_!M49e_3nC0DdR_rEv3R5e!!!}
     - MAPNA{`_ZiG__KPEG_!M49e_3nC0DeR_rEv3R5e"!!}
     - MAPNA{__ZiG__JOEG_!M39e_2nC1DeR^rEv3R5e"! }
  5. 标准答案: MAPNA{__ZiG__JPEG_!M49e_3nC0DeR_rEv3R5e!!!}
key_payload: |
  # packet_t 结构体:
  typedef struct {
      u8 size;
      u32 always_one;
      u8 size_minus_2;
      u8 seq_number;
      u8 type;
      u8 contents[0];  // size-7 bytes
  } packet_t;
  
  # flag: MAPNA{__ZiG__JPEG_!M49e_3nC0DeR_rEv3R5e!!!}
one_liner: MapnaCTF 2023: packet_t 结构体解析 JPEG 字节流，修复 \x1f 替换字符，得 flag。
lesson: |
  - packet_t 7 字节头: size + always_one (4 字节 magic) + size_minus_2 + seq + type
  - JPEG 文档中常含 flag 字符串
  - 字节级字符替换 (0x1f) 干扰 OCR / 直接显示
  - MapnaCTF 是伊朗电力公司组织的 CTF
quality: low
---

# MapnaCTF 2023 Writeup

> 来源: ctfiot.com 158539

## 数据格式

```c
typedef struct {
    u8 size;
    u32 always_one;
    u8 size_minus_2;
    u8 seq_number;
    u8 type;
    u8 contents[0];  // size-7 bytes
} packet_t;
```

7 字节头 + contents 变长数据。

## flag 提取

数据是 JPEG 文档字节流，含 `\x1f` 字符替换常见字符。修复后看到 flag 出现多次：

```
MAPNA{__ZiG__JPEG_!M49e_3nD0DeR_rEv3R5e!!!}
MAPNA{__ZiG__JPEG_!M49e_3nC0DdR_rEv3R5e!!!}
MAPNA{`_ZiG__KPEG_!M49e_3nC0DeR_rEv3R5e"!!}
MAPNA{__ZiG__JOEG_!M39e_2nC1DeR^rEv3R5e"! }
```

**标准答案**：`MAPNA{__ZiG__JPEG_!M49e_3nC0DeR_rEv3R5e!!!}`

## 评价

MapnaCTF 2023 入门 Misc 题，packet_t 格式 + JPEG 字节流修复。MapnaCTF 是伊朗 MAPNA 集团（电力公司）组织的 CTF。

文章内容短，主要展示 packet_t 解析 + 字符替换还原。
