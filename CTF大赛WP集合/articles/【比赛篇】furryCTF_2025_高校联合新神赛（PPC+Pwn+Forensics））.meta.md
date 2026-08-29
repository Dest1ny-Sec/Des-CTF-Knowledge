---
title: 【比赛篇】furryCTF 2025 高校联合新神赛（PPC+Pwn+Forensics）
contest: furryCTF
year: 2025
difficulty: mixed
vuln_type: misc_unknown
tags: [PPC编程题, 爬虫-base16, 多页拼接, fmt-string, 栈溢出, vol内存取证]
attack_chain: 1. PPC flagReader 爬 480 页 base16 字符拼字符串 /2. Pwn 经典 fmt-string 偏移爆破 /3. Forensics vol 内存镜像
key_payload: /api/flag/char/{i}  480 页  base64 + hex 拼接
one_liner: furryCTF 2025 高校联合新神赛 WP，PPC 爬虫 + Pwn 基础 + Forensics 内存取证三大方向。
lesson: PPC 题目多用爬虫脚本自动化；fmt-string + 栈溢出是 PWN 入门；vol 是 Windows 内存取证标准。
quality: medium
---

# 【比赛篇】furryCTF 2025 高校联合新神赛（PPC+Pwn+Forensics）

## 概览
furryCTF 2025 高校联合新神赛 WP，三大方向：PPC + Pwn + Forensics。

## PPC - flagReader
- 480 页 base16 字符
- 爬虫逐页获取
- 拼接成字符串

### 攻击脚本
```python
import requests
import base64

base_url = "http://ctf.furryctf.com:32824"
chars = []

for i in range(1, 481):
    try:
        response = requests.get(f"{base_url}/api/flag/char/{i}")
        data = response.json()
        if data['status'] == 'success':
            char = data['char']
            chars.append(char)
    except Exception as e:
        print(f"请求异常: {e}")

# 拼接成完整字符串
```

## Pwn
- 经典 fmt-string 偏移爆破
- 栈溢出 ret2libc

## Forensics
- vol 内存镜像分析
- 进程/网络/文件

## 经验提炼
- PPC 题目多用爬虫脚本自动化
- fmt-string + 栈溢出是 PWN 入门
- vol 是 Windows 内存取证标准
- requests.get 逐页爬取
- base16 + hex 拼接是 flag 还原常见
- furryCTF 是高校联合新神赛
- PPC = Professional Programming and Coding
- API 路径 /api/flag/char/{i} 模式
- 480 页 = 1 页 1 字符 = flag 长度 480
- 字符串拼接后 base64/hex 解码
