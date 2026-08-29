---
title: 【WP】第二届"红明谷"杯数据安全大赛题目解析（二）
contest: 红明谷
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [SM2-Biased-nonce-attack, HNP-lattice, DPAPI-blob, Master-Key, volatility-imageinfo, hashdump-getsids, mftparser, CVE-2022]
attack_chain: 1. SM2: nonce 前 6 bits 永远 0 + 构造 HNP 格子解密钥 /2. MissingFile: volatility imageinfo + filescan + mftparser + hivelist + hashdump + getsids + dpapi masterkey 解 + dpapi blob 解得 flag{Hide_Behind_Windows}
key_payload: dpapi masterkey  SID=S-1-5-21-206512979-2006505507-2644814589-1001  password=123456  flag{Hide_Behind_Windows}
one_liner: 第二届红明谷杯题解（二），SM2 biased nonce 攻击 + DPAPI masterkey/blob 内存取证解密。
lesson: SM2 nonce 偏差攻击用 HNP (Hidden Number Problem) 构造 LLL 格；DPAPI Master Key 用用户密码 + SID + 16 字节随机数加密；volatility mftparser + hivelist + hashdump 是 Windows 内存取证三件套。
quality: high
---

# 【WP】第二届"红明谷"杯数据安全大赛题目解析（二）

## 概览
第二届红明谷杯数据安全大赛题解（第二部分），SM2 biased nonce 攻击 + DPAPI 内存取证。

## SM2 (Biased nonce attack)

### 题目知识点
- Biased nonce attack
- 观察代码发现 nonce 有一定 bias
- 前 6 bits 永远是 0
- 构造格子解 HNP (Hidden Number Problem) 得到密钥
- 解密得到 flag

### POC
- https://raw.githubusercontent.com/chunqiugame/cqb_writeups/master/2022hmgb/sm2_poc.sage

## MissingFile (DPAPI 内存取证)

### 题目背景
- 某日 Akira 检查电脑时发现好像中毒
- 抢救时被病毒发现，只剩一份快照
- 病毒自我数据删除，内存中有数据残留
- 模拟"数据已加载到内存但被删除"场景

### 加密数据发现（Volatility）
```bash
volatility_2.6_win64_standalone.exe -f memory imageinfo
volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 filescan
# 找到 Users\NewGuest\Desktop\Hacker
volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 mftparser > mtfparser.txt
```

### DPAPI 概念
- **DPAPI** = Data Protection Application Programming Interface
- **DPAPI blob**: 一段密文，可使用 Master Key 对其解密
- **Master Key**: 64 字节，用于解密 DPAPI blob，使用用户登录密码 + SID + 16 字节随机数加密后保存在 Master Key file 中
- **Master Key file**: 二进制文件，可使用用户登录密码对其解密获得 Master Key

### 解密流程
```bash
volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 hivelist
volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 hashdump
volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 getsids

dpapi::masterkey /in:"master.key" /sid:S-1-5-21-206512979-2006505507-2644814589-1001 /password:123456
dpapi::blob /in:dump_S3cret /masterkey:092c4220064c30bc7f8b15d2d48957c4926af0632149b9c08cd87f34fc43aa1204d775bdc6ab429a0d4d0826fb80b08250b125d92913e2f7578cf778073bfe38
```

### flag
`flag{Hide_Behind_Windows}`

## 经验提炼
- SM2 nonce 偏差攻击用 HNP (Hidden Number Problem) 构造 LLL 格
- DPAPI Master Key 用用户密码 + SID + 16 字节随机数加密
- volatility mftparser + hivelist + hashdump 是 Windows 内存取证三件套
- Mimikatz 的 dpapi 模块是解密 DPAPI 的标准工具
- SID 用于标识 Windows 用户安全主体
- HNP 是格密码学经典问题
- 内存取证中"自我删除"数据仍可能残留
- 6 bits 偏差 = 64 倍信息泄露，足够恢复 256 位密钥
- Win7SP1x86 是常见的 volatility profile
- NewGuest 是测试账号，Hacker 是攻击者目录
