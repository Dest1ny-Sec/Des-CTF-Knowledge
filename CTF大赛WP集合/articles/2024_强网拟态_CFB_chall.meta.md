---
title: 2024 强网拟态 CFB_chall
contest: 强网拟态
year: 2024
difficulty: medium
vuln_type: [block_cipher, web_unknown, crypto_unknown]
tags: [AES-CFB 8-bit, 篡改 token, 单字节爆破, error 区分爆破]
attack_chain: 注册用户 admim 密码 a*15+11123456 → token 16 字节密文 → AES-CFB 8-bit 模式篡改第 5 字节 m→n 让 n 后面解密出 \x00 → 第 6 字节爆破 256 次让后面 admin 隔离 → 第 7 字节爆破 256 次让第 23 字节变成 \x00 拆出 123456 → reset 重置 iv/key 继续尝试（总尝试 1/512 概率）→ 登录 admin/123456 拿 flag
key_payload: token = encrypt(f"{username}\x00{password}\x01\x02\x03", key) ; split('\x00') 切出多段时多余段归 _ ; AES CFB 8-bit 改 1 字节影响后续 16 字节
one_liner: AES-CFB 8-bit 单字节爆破 + reset 重置 iv/key 凑运气。
lesson: AES CFB 8-bit 模式每个密文字节是独立流密码块，改 1 字节只影响后续；revenge 用不同 error 文案做 oracle 攻击。
quality: high
---
# 2024 强网拟态 CFB_chall

## 题目分析

```python
def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)  # CFB 默认 8-bit
    return cipher.encrypt(data.encode('utf-8')).hex()

def decrypt(ct, key):
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    return cipher.decrypt(bytes.fromhex(ct))

token = encrypt(f"{username}\x00{password}\x01\x02\x03", key)
```

**矛盾**：不能注册 admin（用户名含 'admin'）、密码长度 ≥ 8、但 admin 登录要密码 = '123456'（6 字符）。

**关键分割逻辑**：
```python
token_username, *_, token_password = decrypted.split(b'\x00')
assert token_password[-3:] == b"\x01\x02\x03"
```

如果 split 超过 2 段，**多余段全部归 _** → 利用这点绕过 admin/123456 限制。

## AES-CFB 8-bit 特性

PyCryptodome `AES.MODE_CFB` 默认 segment_size=8 → 一次只加密 1 字节：
```
K_i = AES_K(ciphertext_{i-1})  # 不是明文
ct_i = pt_i XOR K_i
```

**改 1 字节密文**：进入下一组加密器的输入变了 → 后面 16 字节解密大概率乱。

## 攻击步骤

```python
# 1. 注册 admim + 密码 a*15+11123456 → 拿到 token
username = "admim"
password = 'a'*15 + '11123456'

# 2. 篡改第 5 字节 m → n，让 n 后面解密出 \x00
token_mod = token[:8] + hex(int(token[8:10], 16) ^ (ord('m') ^ ord('n')))[2:].rjust(2, '0') + ...

# 3. 爆破第 6 字节（256 种），让 n 后出现 \x00 把 admin 拆出
for i in range(256):
    s = token[:10] + hex(i)[2:].rjust(2, '0') + '01' + token[14:]
    r = login(s)
    if "wrong" in r: break  # 触发错误 → 改 iv 重来
    if 'flag' in r: print(r)

# 4. reset 重置 iv/key
# 成功率 1/512
```

## CFB_chall revenge

revenge 把 `restart` 接口 ban 掉 → 改用"不同错误返回不同文案"做 oracle：

```python
try:
    decrypted = decrypt(token, key)
    token_username, *_, token_password = decrypted.split(b'\x00')
    assert token_password[-3:] == b"\x01\x02\x03"
    ...
except:
    message = "Login wrong, please try again"
```

利用 "Login wrong" vs "Login failed" 的细微差别做时序/内容 oracle，逐字节爆破。

**关键洞察**：AES CFB 8-bit 模式可单字节位翻转，Python 实现的默认 segment_size 容易踩坑。
