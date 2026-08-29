---
title: 2024 KCTF 大赛 - 第四题《神秘信号》设计思路及解析
contest: KCTF大赛
year: 2024
difficulty: hard
vuln_type: [reverse, misc_math]
tags: [PyInstaller反编, code对象反序列化, 假CrackMe实为base64, 自定义base64字符表, XOR 0x55, swap pair, crackme.main=base64.main, hook input 偷数据, kernel32.dll 遍历]
attack_chain: PyInstaller 解包 → main.py 在 _internal/ → import CrackMe 实际指向 base64 模块（importlib hook 把 CrackMe 名字替换成 base64）→ `CrackMe.main(data)` 实为 base64 编码 + XOR 0x55 + swap pair → hook input 拿到 CrackMe("KCTF") → convertinput("KCTF") = (ord(c) ^ 0x77) + 21 → crackme.main(convertinput("KCTF")) = "QQMlP7!!" → 写 ztokey 拼密钥 → 用 真实账号密码 得到验证码 → hook input 注入打印 → reverse 编码：rstrip ! → translate 字符表 → base64 decode → ^ 0x55 → 解得原始输入
key_payload: convertinput(s) = bytes((ord(c) ^ 0x77) + 21 for c in s) ; CrackMe.main(KCTF) = "QQMlP7!!" ; ztokey(z) = "dZpK" + z[0:4] + "drsi" + z[4:8] + "B6cn" + z[8:12] + "drGY" + z[12:16] + z[16:] ; 字符表 ZQ+U7tSBEKVzyf5coCwb94Dd6raT0eLNin12Hp8mOxFuvMgIPlhRY3WjksqJAXG/
one_liner: PyInstaller CrackMe 替换 base64 + XOR 0x55 + swap pair + hook input 偷数据。
lesson: PyInstaller CrackMe 在 hook 后模块名会被换，看 import sys.modules["CrackMe"] 才能看到真相。
quality: high
---
# 2024 KCTF 大赛 - 第四题《神秘信号》设计思路及解析

**出题战队 one team · 一血 Li0kle 用时 4h19m1s · 23 队提交**

## 题目结构

PyInstaller 打包的 EXE，启动后：
```
请输入账号：KCTF
请输入验证码：Hello World!KCTF
Success
```

## 关键发现

```python
# 解包 PyInstaller
import _frozen_importlib
tmp = importlib._bootstrap_external._code_to_timestamp_pyc(
    _frozen_importlib._find_and_load.__code__)
with open("_frozen_importlib._find_and_load.__code__.pyc", "wb") as f:
    f.write(tmp)
```

发现 `import CrackMe` 实际指向 base64（**模块名替换**）：

```c
// importlib._find_and_load 内部
a = 0;
if (len(name) == 7 && name[0] == 'C' && name[1] == 'r' && ... && name[6] == 'e') {
    name = 'base64';  // CrackMe → base64
    a = 1;
}
```

`import CrackMe; print(CrackMe)` → `<module 'base64' from '...main\_internal\base64.pyc'>`

## 真实 main 函数

base64 源码被 patch：

```python
def main(data):
    encoded_str = ''
    padding = 0
    base64_chars = 'ZQ+U7tSBEKVzyf5coCwb94Dd6raT0eLNin12Hp8mOxFuvMgIPlhRY3WjksqJAXG/'
    ww = b''
    for i in data:
        i = i ^ 85  # 0x55
        ww = ww + i.to_bytes(1, 'little')
    data = ww
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        binary_str = ''.join(format(byte, '08b') for byte in chunk)
        for j in range(0, len(binary_str), 6):
            six_bits = binary_str[j:j+6]
            if len(six_bits) < 6:
                padding += 6 - len(six_bits)
                six_bits += '0' * (6 - len(six_bits))
            encoded_str += base64_chars[int(six_bits, 2)]
    encoded_str += '!' * (padding // 2)
    # swap pair
    for i in range(len(encoded_str) // 2):
        a = encoded_str[i*2]; b = encoded_str[i*2+1]
        encoded_str = encoded_str[:i*2] + b + a + encoded_str[i*2+2:]
    return encoded_str
```

## 偷数据

```python
old_input = input
def hook_input(*args, **kwargs):
    r = old_input(*args, **kwargs)
    print(repr(old_input), hex(id(old_input)), repr(r))
    return r
__builtins__["input"] = hook_input
```

运行：
```
请输入账号：KCTF
0x18e4b220a90  b'QI8F'
```

`QI8F` 是被预先 XOR + 21 处理过的，对应 `KCTF`：
```python
def convertinput(s):
    return bytes((ord(c) ^ 0x77) + 21 for c in s)
assert convertinput("KCTF") == b'QI8F'
```

## 还原算法

```python
def rev(encoded_str):
    tmp = encoded_str
    # 反 swap pair
    tmp = "".join(tmp[2*i+1]+tmp[2*i] for i in range(len(tmp)//2))
    tmp = tmp.rstrip("!")
    # 反 base64 字符表
    trans = str.maketrans(
        "ZQ+U7tSBEKVzyf5coCwb94Dd6raT0eLNin12Hp8mOxFuvMgIPlhRY3WjksqJAXG/",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
    tmp2 = tmp.translate(trans)
    tmp2 += "=" * ((4-len(tmp2))%4)
    tmp3 = base64.b64decode(tmp2)
    return bytes(c ^ 0x55 for c in tmp3).decode()
```

## 拼验证码

```python
def ztokey(z):
    if len(z) < 20:
        return 'dZpKdrsiB6cndrGY' + z
    return z[0:4]+'dZpK'+z[4:8]+'drsi'+z[8:12]+'B6cn'+z[12:16]+'drGY'+z[16:]

# 输入账号 = "Hello World!KCTF"
z = main(convertinput("Hello World!KCTF"))     # dZpKdrsiB6cndrGYQQMlP7!!
key = ztokey(z)                                  # dZpKdZpKdrsidrsiB6cnB6cndrGYdrGYQQMlP7!!
m = main(convertinput(账号))                      # == key 时 Success
```

**关键洞察**：本题通过 `code.replace()` 替换 `__code__`，把 base64 源码换成自定义 base64 + XOR + swap pair 编码，**模块名 CrackMe 只是 hook 后的伪装**。
