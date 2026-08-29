---
title: 春节领红包 9 Web 中级题 wasm 逆向
contest: 春节领红包
year: 2026
difficulty: hard
vuln_type: web_unknown
tags: [WASM, HMAC-SHA1, custom-Base64, SHA-256, audio-stitching, WebAssembly.instantiate-hook, crypto.getRandomValues-hook, audio-wav, XaraMysteria, voice-captcha]
attack_chain:
  - 目标: WASM gen(uid, voice) 函数生成 50 位自定义 Base64 验证码
  - Step 1: 生成 17 字节随机数 rand
  - Step 2: uid (小端序) ^ rand[0:4] 拼接 rand[0:17] = 21 字节 msg
  - Step 3: 14 字节硬编码 HMAC Key (WASM 内存 1295967 偏移) 对 msg HMAC 签名
  - Step 4: msg + HMAC 前 16 字节 = 37 字节，自定义字典 Base64 编码 → 50 位字符
  - Step 5: 50 位验证码明文 SHA-256 嵌套 8230 次得到 hash
  - Step 6: 验证码字符 → 内置 wav 碎片拼接音频返回前端
  - 漏洞 1: 劫持 WebAssembly.instantiate 暴露 window.wasmMem
  - 漏洞 2: 劫持 crypto.getRandomValues 填 0 消除随机性
  - 漏洞 3: 内存扫描定位 HMAC Key (1295967 偏移) + 自定义字典 (1295903 偏移)
  - 漏洞 4: 截取原生匹配文本，扫描整个 WASM 内存找 flag
key_payload: 'uid=2406132, rand=17 字节全 0, HMAC Key = 0001010101010100010001000502 (14 字节)'
one_liner: WASM 验证码生成：劫持 instantiate 暴露 memory + 劫持 getRandomValues 消除随机 + 内存扫描提 HMAC Key + Base64 字典。
lesson: WASM 加密逻辑不是黑盒，memory 暴露后 key + 算法全可被逆向；crypto API 钩子是 WASM 加密验证类 CTF 的核心突破口。
quality: high
---

# 春节领红包之九 {Web 中级题} 题解 – wasm 逆向

**来源**: ctfiot.com ID 303352
**作者论坛账号**: XaraMysteria

## 题目结构
- WASM 模块：gen(uid, voice) 返回 {h: hash, a: audioBlob}
- 前端：50 位自定义 Base64 验证码 + wav 音频

## WASM 核心逻辑

### 1. 生成 17 字节随机数
```js
wbg_wbg_getRandomValues_1c61fac11405ffdc(d + 80, 17);
```

### 2. 拼装 21 字节 msg
```c
j = f_zb(37, 1);  // 37 字节 buffer
// uid (4 字节小端序) ^ rand[0:4]
j[3] = d[83] ^ a >> 24;  // UID MSB
j[2] = d[82] ^ a >> 16;
j[1] = d[81] ^ a >> 8;
j[0] = d[80] ^ a;       // UID LSB
// 17 字节 rand 拼接
```

### 3. HMAC 签名
```c
a = g_a - 352;
memory_copy(a, 1295967, 14);  // 从数据段 1295967 拷贝 14 字节 HMAC Key
// HMAC-SHA1(msg, 14 字节 Key) → 20 字节
```

### 4. 自定义 Base64
字典起始 1295903：`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!`
- 6 bit 一组
- 37 字节 → ceil(37 × 8 / 6) = 50 字符

### 5. SHA-256 嵌套 8230 次
```c
b = 8229;  // 初始 1 次，循环 8229 次
loop L_te {
    f_j(c, i, 1);  // SHA-256 压缩函数
    b = b - 1;
    if (b) continue L_te;
}
```

## 攻击链

### 1. 提取 WASM 二进制
```js
const wasmBytes = globalThis.getWasmBuffer();
const blob = new Blob([wasmBytes], {type: 'application/wasm'});
const url = URL.createObjectURL(blob);
// <a download="challenge.wasm" />
```

### 2. 劫持 WebAssembly.instantiate 暴露 memory
```js
const origInstantiate = WebAssembly.instantiate;
WebAssembly.instantiate = async function(...args) {
    const result = await origInstantiate.apply(this, args);
    window.wasmMem = (result.instance || result).exports.memory;
    return result;
};
```

### 3. 劫持 crypto.getRandomValues 填 0
```js
crypto.getRandomValues = function(array) {
    array.fill(0);
    return array;
};
```

### 4. 内存扫描
```js
// 字典在 1295903
let dict = new TextDecoder().decode(memView.slice(1295903, 1295903 + 64));
// 硬编码字典: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!

// HMAC Key 在 1295967
let keyBytes = memBuffer.slice(1295967, 1295967 + 14);
console.log("Hex Key: " + Array.from(keyBytes).map(b => b.toString(16).padStart(2, '0')).join(''));
// 输出: 0001010101010100010001000502
```

### 5. 复现验证码
```python
import struct, hmac, hashlib, base64

UID = 2406132
RAND_BYTES = bytes([0] * 17)
HMAC_KEY = bytes.fromhex("0001010101010100010001000502")

# 小端序 UID ^ RAND[0:4]
uid_bytes = struct.pack("<I", UID)
msg = bytes(a ^ b for a, b in zip(uid_bytes, RAND_BYTES[:4])) + RAND_BYTES
# 21 字节 msg

mac = hmac.new(HMAC_KEY, msg, hashlib.sha1).digest()[:16]
blob37 = msg + mac
# 自定义 Base64 编码
```

## 评价
春节领红包 Web 中级 wasm 逆向精品。考察 WASM 内部算法逆向 + 浏览器 API 钩子（instantiate + getRandomValues）+ 内存扫描找隐藏常量 + 截断/差分侧信道。展现了现代前端加密验证类题目的标准攻击面。
