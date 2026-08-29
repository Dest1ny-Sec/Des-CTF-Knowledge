---
title: 京麒CTF 2024初赛Writeup
contest: 京麒CTF 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [走迷宫, shellcode约束, WASM, HSP3, Tauri, secp256k1, ECDSA, LLL格基, UTF-8 Overlong, 反序列化, Rome]
attack_chain:
  - MazeCodeV1: DFS 走迷宫得路径 + 末位&3 序列当 shellcode
  - 序列: 111122110011221122110011112211222211222222110011112211221100110000001100001100001122222222332222332211223333223322221122333322111122110011112222332211222233003322221111
  - 0=xchg esi,eax/1=push rcx/2=xchg edx,eax/3=push rbx
  - easy-wasm: window['😘😘❤️😘😘'] 加密函数 + 每位加密 16 长 + 逐位爆破
  - Hot Soup: HSP3 + HSPdeco 反编译 + srand(2333333) + AES-128 SHA256 派生
  - possible-door: Tauri 解包 index.html + index-C9fLaX_M.js + rust pdb 看 main
  - js 调 rust get_rand_num 生成 secp256k1 私钥 + AES key/iv 共享 call_once
  - secp256k1 41 比特 nonce + 7 个签名 → LLL 7×7 矩阵还原私钥
  - 私钥 = 39313219724394204510065149548180909443668279642741674773372964155008434357587
  - ezjvav: admin/admin → /source jsrc base64 作 jwt key 伪 root
  - ByteCompare 黑名单 HashMap/TemplatesImpl/fastjson → UTF-8 Overlong 绕
  - Rome 链 EqualsBean + TemplatesImpl + HashMap 反序列化
key_payload: '京麒CTF{*} + ecdsa_nonce_LLL_recover + 0x404dd0 /bin/sh 栈迁移'
one_liner: 京麒 2024 初赛全栈：迷宫 shellcode + WASM 爆破 + HSP3 AES + Tauri ECDSA-LLL + Java UTF-8 Overlong Rome 反序列化。
lesson: ECDSA 弱 nonce (41 比特时间戳) 用 LLL 7×7 矩阵 (BB=1716708884867*2) 一发还原私钥；Java ByteCompare 黑名单字节比对可用 UTF-8 Overlong Encoding (2 字节表示 1 字节) 绕过。
quality: high
---

# 京麒CTF 2024初赛Writeup

## 概览
- **来源**: ctfiot 184181
- **赛事**: 京麒CTF 2024 初赛
- **难度**: ⭐⭐⭐

## 1. Pwn - MazeCodeV1
- 走迷宫 + 路径当 shellcode，末位 &3 = 实际指令
- 0=xchg esi,eax, 1=push rcx, 2=xchg edx,eax, 3=push rbx
- DFS 路径: `111122110011221122110011112211222211222222110011112211221100110000001100001100001122222222332222332211223333223322221122333322111122110011112222332211222233003322221111`
- 栈迁移到 0x404e02, ORW /bin/sh 0x404dd0, 0x3b execve

## 2. Reverse

### 2.1 easy-wasm
- `window['😘😘❤️😘😘']` 加密函数
- 每位加密为 16 长 base64 串，位之间互不相关
- 逐位爆破 charset=`A-Za-z0-9 !"#...~`

### 2.2 Hot Soup
- HSP3 + HSPdeco 反编译 bin
- `srand(2333333)` 生成 32 字节 var_20
- CryptCreateHash SHA-256 + CryptDeriveKey AES-128
- CryptDecrypt + XOR xor_data[45]

### 2.3 possible-door (Tauri)
- 解包 index.html + index-C9fLaX_M.js
- rust pdb 看 main: list_dir/read_file 用 AES-128-CBC 加密
- key/iv 来自 `Once::call_once` 闭包 (与 ECDSA 私钥共享)
- js 用 secp256k1 签名 (DER 格式)
- nonce 41 比特时间戳范围
- **7 个签名 LLL 攻击还原私钥**:
  ```python
  n = 7
  BB = 1716708884867 * 2
  M = Matrix(QQ, n+2, n+2)
  for i in range(n):
      M[i,i] = q
      M[-2, i] = rs[i] * inverse_mod(ss[i], q) % q
      M[-1, i] = hs[i] * inverse_mod(ss[i], q) % q
  M[-2,-2] = BB / q
  M[-1,-1] = BB
  L = M.LLL()
  ks = L[1][:-2]
  x = (ks[0]*s0 - h0) * inverse_mod(r0, q) % q
  # x = 39313219724394204510065149548180909443668279642741674773372964155008434357587
  ```

## 3. Web - ezjvav
- admin/admin → /source 返回 "you are not root need jsrc"
- **jwt 伪 root**: key=base64("jsrc")
- **Jsrc 反序列化**:
  - 黑名单: HashMap, TemplatesImpl, JSONArrayLlist
  - **UTF-8 Overlong Encoding 绕** (2 字节编码 1 字节)
  - **Rome 链**: EqualsBean(String.class,"") + TemplatesImpl + HashMap(map1, map2) put 触发 hashCode
  - TemplatesImpl 加载 base64 bash reverse shell
