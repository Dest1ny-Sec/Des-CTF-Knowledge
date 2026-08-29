---
title: DataCon2023软件安全赛道，冠军战队WP分享
contest: DataCon 2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [metasploit, cobaltstrike, shellcode, shikata_ga_nai, upx, stager, smc, x86-x64]
attack_chain:
  - 200个Metasploit/CobaltStrike PE样本
  - 6个UPX壳：upx -d脱壳
  - 无Encoder: hash(0x6B8029 WSAStartup)+call ebp
  - IP/端口加载: 32位 0x80BEA8C0→C0A8BE80→192.168.190.128 0x33050002→1331
  - 64位: 0x5c110002→0x115c→4444
  - shikata_ga_nai: 内存特征 xd9x74x24xf4 (fnstenv)
  - fcmovu st,st(1)+fnstenv byte[esp-0Ch]+xor+loop SMC
  - 上百轮自修改解密
key_payload: ida_search.find_binary(0, 0xffffffffffffffff, '29 80 6B 00', 16, idc.SEARCH_DOWN)
one_liner: DataCon2023软件安全：Metasploit/CobaltStrike shellcode stager分析
lesson: shikata_ga_nai内存特征xd9x74x24xf4是fnstenv指令
quality: high
---

# DataCon2023软件安全赛道，冠军战队WP分享

## 题目信息
- 比赛：DataCon 2023
- 方向：软件安全
- 冠军：武汉大学 N0nE429
- 任务：200 个 Metasploit/CobaltStrike PE 样本 shellcode stager 配置信息提取

## 关键攻击链
### 1. 提交格式
```json
{
  "xxxxxxx": {
    "C2": "101.42.166.216:80",
    "Arch": "x86",
    "Encoder": "shikata_ga_nai:15"
  }
}
```

### 2. UPX 脱壳
- 6 个样本加 UPX 壳
- `upx -d` 全部脱壳

### 3. Metasploit 无 Encoder
- 32 位特征：`push 0x006B8029` (WSAStartup hash) + `call ebp`
- 64 位特征：`mov r10d, 0x006B8029` + `call rbp`
- 搜索关键字节：`ida_search.find_binary(0, 0xffffffffffffffff, '29 80 6B 00', 16, idc.SEARCH_DOWN)`

### 4. IP/端口加载
- 32 位：`0x80BEA8C0` → `0xC0A8BE80` → `C0 A8 BE 80` → `192.168.190.128`
- 端口 `0x33050002` → `0x533` → 1331
- 64 位：`0x5c110002` → `0x115c` → 4444

### 5. shikata_ga_nai Encoder
- 内存特征：`\xD9\x74\x24\xF4`（fnstenv 指令）
- 多轮自修改解密（SMC）：
  ```asm
  fcmovu st, st(1)
  fnstenv byte ptr [esp-0Ch]
  mov REG1, XORCONST
  pop REG2
  sub ecx, ecx
  mov cl, XORLEN
  loc_loop:
      xor [REG2+OFFSET], REG1
      add REG2, 4
      sub REG2, 0FFFFFFFCh
      add REG1, [REG2+OFF-4]
  loop loc_loop
  ```
- 解密出原始 shellcode 再分析

## 评分
- quality: high（Metasploit 源码级分析 + IP/端口提取 + shikata_ga_nai 完整解密）
