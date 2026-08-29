---
title: 一次银狐样本分析
contest: 安全研究
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags: [银狐木马, PEB-InMemoryOrderModuleList, DLL-base-遍历, API-Hash-还原, ShellCode-Loader, C2地址, t1-t2-t3]
attack_chain: 1. PEB->InMemoryOrderModuleList 遍历双向链表 找 BaseDllName /2. 比较 DLL 名找基址 /3. API Hash 算法还原 (ROR13 常见) /4. 解析 DLL 导出表 哈希 API 名匹配 /5. 动态调试：自实现 Loader 加载 ShellCode /6. 提取 C2: 156.234.119.138:443 / syumineyt.top:80 / syumingeyt.top:8080
key_payload: PEB InMemoryOrderModuleList  syumineyt.top  syumingeyt.top  API Hash 还原
one_liner: 银狐木马样本分析，PEB 遍历模块 + API Hash 还原 + ShellCode Loader 动态调试 + C2 提取。
lesson: 银狐木马典型用 PEB 隐藏 API 调用；API Hash = 常见 ROR13 算法；动态调试需自实现 Loader；C2 通信地址 t1/t2/t3 区分协议。
quality: medium
---

# 一次银狐样本分析

## 概览
银狐木马样本分析，作者 soma20。涉及 PEB 遍历模块 + API Hash + ShellCode Loader。

## 技术点
- **PEB->InMemoryOrderModuleList**：遍历双向链表找 BaseDllName
- **API Hash 还原**：复杂方法用 ROR13 哈希算法对常见 DLL 名计算
- **动态调试**：自实现 Loader 加载 ShellCode

## 提取的 C2
- `156.234.119.138:443` (t1，可能指 TLS/SSL 加密)
- `syumineyt.top:80` (t2，可能指 HTTP 明文)
- `syumingeyt.top:8080` (t3，可能指 HTTP/其他协议)

## API Hash 还原方法

### 方法 1: 复杂
```python
def ror13_hash(name):
    h = 0
    for c in name:
        h = ((h >> 13) | (h << (32 - 13))) & 0xFFFFFFFF
        h = (h + ord(c)) & 0xFFFFFFFF
    return h
```

### 方法 2: 简单
- 动态调试直接获取目标 API 名
- 自实现 Loader 加载 ShellCode

## 经验提炼
- 银狐木马典型用 PEB 隐藏 API 调用
- API Hash = 常见 ROR13 算法
- 动态调试需自实现 Loader
- C2 通信地址 t1/t2/t3 区分协议
- InMemoryOrderModuleList 是 PEB 第三个成员
- BaseDllName.Buffer 是 UNICODE_STRING
- 银狐是 APT 攻击常用工具
- 自实现 Loader 需要解析 PE 头 + 修复重定位
- 动态调试比静态分析更直观
- PEB->Ldr->InMemoryOrderModuleList 是经典遍历路径
