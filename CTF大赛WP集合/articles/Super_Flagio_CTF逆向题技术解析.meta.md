---
title: Super Flagio CTF 逆向题技术解析
contest: Super Flagio CTF
year: 2025
difficulty: hard
vuln_type: reverse
tags: [cocos2d-x, luajit-bytecode, xxtea-decrypt, custom-vm, lua-encrypt, frida-hook]
attack_chain:
- unzip flagio.apk 提取 assets/src/ 加密 Lua 脚本
- strings libgame.so | grep XXTEA 发现 xctf-flagio-2dx 密钥
- LuaJIT 2.1.0-beta3 字节码格式识别
- frida hook luaL_loadbuffer 拦截解密后字节码
- 自定义 opcode 顺序：PUSH_IMM(0x41)/PUSH_REG(0x42)/PUSH_IN(0x32)/POP_REG(0x25)/POP_OUT(0x31)/INC_REG(0x21)/DEC_REG(0x22)/XOR_REG(0x24)/XOR_IMM(0x23)/RET(0x90)
- 模拟执行 12 指令 + 链式 XOR
- 加密算法：output[0] = (input[0]^30)-1; output[i] = (output[i-1]^input[i])±1
- 奇偶差异处理：i%2==0 或 i==31 减 1；奇数加 1
- 32 字节密文 [94,106,91,110,86,100,82,20,...]
- 解密脚本从后向前 XOR+±1
- 验证 SHA256 哈希
- flag = A766957A53EDA9290CCF8E03F1A9B7E0
key_payload: frida -l hook.js -f com.flagio.app
one_liner: Super Flagio CTF：cocos2d-x Android 游戏逆向，XXTEA 解 LuaJIT + 自定义 opcode VM 还原。
lesson: 加密字节码 + 自定义 opcode 是游戏反外挂常见组合，Frida hook luaL_loadbuffer 是标准破法。
quality: high
---
# Super Flagio CTF 逆向题技术解析

## 1. APK 结构
```
extracted/
├── assets/
│   ├── res/        # 图片、音效
│   └── src/        # 加密的 Lua 脚本
│       ├── 1024446525/
│       ├── 1975478612/    # checker 脚本
│       │   └── 526018661  # 1323 字节
│       ├── 33309236/
│       ├── 3914622949/
│       └── 537350069
├── lib/arm64-v8a/libgame.so
├── classes.dex
└── AndroidManifest.xml
```

## 2. 关键字符串
```bash
$ strings lib/arm64-v8a/libgame.so | grep -E "XXTEA|main.py|luajit|key"
main.py
./?.py;/usr/local/share/luajit-2.1.0-beta3/?.py
XXTEA
xctf-flagio-2dx   <-- XXTEA 密钥
```

## 3. 字节码格式
```bash
xxd assets/src/1975478612/526018661 | head
# 字节 0-1: 0xFFFF (签名)
# 字节 2-5: 0xDBEE66 (XXTEA 标志)
# 字节 6+: 加密数据
```

## 4. Frida hook
```javascript
Interceptor.attach(Module.findExportByName("libgame.so", "luaL_loadbuffer"), {
    onEnter: function(args) {
        var size = args[2].toInt32();
        var bytecode = Memory.readByteArray(args[1], size);
        // 保存 bytecode 到文件
    }
});
```

## 5. 自定义 opcode 还原
| Opcode | Dec | 助记符 | 操作数 | 功能 |
|--------|-----|--------|--------|------|
| 0x11   | 17  | INC_INPUT | n | input[n]++ |
| 0x12   | 18  | DEC_INPUT | n | input[n]-- |
| 0x21   | 33  | INC_REG | r | reg[r-8]++ |
| 0x22   | 34  | DEC_REG | r | reg[r-8]-- |
| 0x23   | 35  | XOR_IMM | r, imm | reg[r-8] ^= imm |
| 0x24   | 36  | XOR_REG | r1, r2 | reg[r1-8] ^= reg[r2-8] |
| 0x25   | 37  | POP_REG | r | reg[r-8] = pop() |
| 0x31   | 49  | POP_OUT | n | output[n] = pop() |
| 0x32   | 50  | PUSH_IN | n | push(input[n]) |
| 0x41   | 65  | PUSH_IMM | imm | push(imm) |
| 0x42   | 66  | PUSH_REG | r | push(reg[r-8]) |
| 0x90   | 144 | RET | - | 返回 |

## 6. 链式加密算法
```python
def encrypt(plaintext):
    buf = list(plaintext)  # 32 bytes
    buf[0] = (buf[0] ^ 30) - 1
    for i in range(1, 32):
        buf[i] ^= buf[i-1]
        if i % 2 == 0 or i == 31:
            buf[i] -= 1
        else:
            buf[i] += 1
        buf[i] &= 0xFF
    return buf
```

## 7. 解密 (从后向前)
```python
cipher = [94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98,
          81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]

for i in range(31, 0, -1):
    if i % 2 == 0 or i == 31:
        cipher[i] += 1
    else:
        cipher[i] -= 1
    cipher[i] &= 0xFF
    cipher[i] ^= cipher[i-1]
cipher[0] = (cipher[0] + 1) ^ 30

flag = ''.join(chr(c) for c in cipher)
# A766957A53EDA9290CCF8E03F1A9B7E0
```

## 8. 游戏验证
- 两排砖块，上排对应 flag 前 16 字符，下排后 16 字符
- 顶正确砖块 → 出现蘑菇
- 吃蘑菇 + 碰板栗 → 墙壁消失
- 触旗帜通关

## 技术栈
- APK 文件结构分析
- Native 库静态分析
- cocos2d-x 框架理解
- Lua 脚本加载机制
- XXTEA 加密识别
- LuaJIT 字节码格式
- 自定义 opcode 映射还原
- 64 位反编译器适配
- 自定义 VM 架构逆向
- 链式加密算法识别
- 数学推导 + 解密脚本
