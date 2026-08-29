---
title: 看雪·众安 2021 KCTF 秋季赛 | 第八题设计思路及解析
contest: 看雪·众安 2021 KCTF秋季赛
year: 2021
difficulty: hard
vuln_type: reverse
tags: [Android CrackMe, ArmVMP, DES加密, Frida hook, 轮密钥swap, libart.so hook, NewStringUTF, 双输入name/serial, 双重DES]
attack_chain: IDA发现DES→Frida hook 0x789打印参数→输入转hex再加密+相同内容再加密→swap 48个轮密钥倒序→hook libart NewStringUTF("恭喜成功")→同一name不同serial+不同name同serial 爆破得正确密文→DES解密
key_payload: "Frida hook sub_788 DES;swapkey(48轮密钥倒序);encdata1=[0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4];encdata2=[0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5];hex=638f6773593bd91d788e891e6cf42efa"
one_liner: 看雪众安KCTF2021秋Q8《群狼环伺》Android CrackMe：双重DES+Frida hook 48轮密钥倒序+双输入爆破
lesson: DES轮密钥swap函数可解密；hook NewStringUTF+debugger断点爆破
quality: high
---

# 看雪·众安 2021 KCTF 秋季赛 | 第八题设计思路及解析

**赛事**：看雪·众安 2021 KCTF秋季赛 Q8《群狼环伺》

**难度**：3队破解（辣鸡战队/金左手/mininep），一血100442秒（约28h）

**题目**：Android CrackMe（ArmVMP保护）

**题目设计**：
- ArmVMP保护（参考Q4《迷雾散去》）
- DES加密算法
- 双输入：name + serial

**破解步骤**：

**Step 1：找DES**
- IDA打开，发现很多函数被VM化
- 密码学常量识别出DES
- 手动Create Function识别未识别函数
- `sub_788` 是DES过程

**Step 2：Frida hook DES**：
```javascript
Interceptor.attach(baseAddr.add(0x789), {
    onEnter: function(args) {
        console.log(hexdump(args[0], {offset:0, length:128*3, header:true, ansi:true}));  // Enc Data
        console.log(hexdump(args[1], {offset:0, length:8, header:true, ansi:true}));     // Key
    },
    onLeave: function(ret) {
        console.log(hexdump(args[2], {offset:0, length:8, header:true, ansi:true}));     // Output
    }
});
```

**Step 3：双重DES结构**
- 输入转hex → 加密一次
- 相同内容再加密一次
- **轮密钥swap**：
  ```javascript
  function swapkey(addr) {
      var key = [];
      for (var i = 0; i < 48; i++) key.push(addr.add(i*8).readU64());
      for (var i = 0; i < 48; i++) addr.add(i*8).writeU64(key[47-i]);
  }
  ```

**Step 4：hook NewStringUTF 找"恭喜成功"**
```javascript
Interceptor.attach(baseAddr.add(0xae765), {
    onEnter: function(args) {
        if (args[1].readCString() == "恭喜成功" || args[1].readCString() == "输入错误") {
            debugger;  // frida debugger命中会暂停当前线程
        }
    }
});
```

**Step 5：爆破正确密文**
- 保持name相同，serial不同 → 找到一个DES结果：
  `bd 3a b0 69 39 40 f8 cd 42 0d e3 8a 79 db 52 bd`
- 保持name不同（KCTF），serial相同 → 找到另一个：
  `45 68 97 A3 29 2A 7F D4 F5 90 73 57 46 02 AE D5`

**Step 6：解出最终输入**
```javascript
if (true) {
    swapkey(args[0]);  // 倒序48轮密钥
    
    // Data 1 (lr=0xe8b5)
    if (lr == 0xe8b5) {
        var encdata1 = [0x45,0x68,0x97,0xa3,0x29,0x2a,0x7f,0xd4];
        args[1].writeByteArray(encdata1);
    }
    
    // Data 2 (lr=0xe8e5)
    if (lr == 0xe8e5) {
        var encdata2 = [0xf5,0x90,0x73,0x57,0x46,0x02,0xae,0xd5];
        swapkey(args[0]);  // 再次swap回原顺序
        args[1].writeByteArray(encdata2);
    }
}
```

**最终输入hex**：`63 8f 67 73 59 3b d9 1d 78 8e 89 1e 6c f4 2e fa`

**核心技术**：
- ArmVMP下手动识别DES + Create Function
- Frida hook 0x789 入口+0xae765 NewStringUTF
- 轮密钥48个u64倒序swap
- 双输入爆破（固定name变serial / 固定serial变name）
- debugger 暂停命中点

**质量评估**：高（Frida hook完整 + 双重DES swapkey + 爆破思路）
